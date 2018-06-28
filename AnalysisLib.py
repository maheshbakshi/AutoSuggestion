#Analysis library for performing multi-threaded post processing on data
#Includes reading raw data, reading spec data 
"""
Analysis library for performing multi-threaded post processing on data
Includes reading raw data, reading spec data
"""



from SupportFunctions import *
import queue
import time

# noinspection PyBroadException
class ATSProcessor:
    dataQueue = ""  #stuff in this queue must be formatted as: filePath, measurementNumber
    specInfo = ""
    loadedDUTs = dict()
    currentSuggestion = ""
    saveFilePath = ""
    isActive = True
    logger = ""

    measurementsCompleted = False #When this value is true, all analyses are forced and you no longer wait for data

    def __init__(self, specInfo, DUTObj, saveFilePath, logger):
        """
        Construct a new 'ATSProcessor' object.

        :param parent: as needed
        :return: returns nothing
        """
        self.dataQueue = queue.Queue() #this queue is accessible from the measurement thread and is populated by it,
        #In python queues are thread safe by default
        self.specInfo = specInfo
        self.currentSuggestion = DUTObj
        self.saveFilePath = saveFilePath
        self.measurementsCompleted = False
        self.isActive = True
        self.logger = logger

    def RunAnalysis(self, percentQueue):
        """
        Full analysis functionality. Performs analysis on data provided in the dataQueue. Updates the DUT object.
        Used only for multi-threading. Unused for this non-threaded code.

        :param percentQueue: helps to track progress
        :return: returns nothing
        """
        #this runs in separate thread. The data is passed as it is ready through the queue object.
        while self.isActive:
            #check to see if the measurements have completed,
            # if they have then no more data will arrive and you should finish everything and stop even if not all the analyses are completed
            if self.measurementsCompleted:
                self.isActive = False
            #check the queue and empty any elements that are in it
            while not self.dataQueue.empty():
                #Queue contains file paths, so simply add the data from that file path using the data library
                self.currentSuggestion.lockObject.acquire()
                nextDataFileInfo = self.dataQueue.get()
                nextDataFilePath = nextDataFileInfo.split(',')[0]
                nextDataFilePath = nextDataFilePath.lower()
                if nextDataFilePath.endswith(".tsv"):
                    #Do we need else here??? load as mat file, all other files should be ignored
                    DataLib.loadLocationDataOnce(nextDataFilePath, self.currentSuggestion, self.specInfo, self.logger )
                self.currentSuggestion.lockObject.release()

                #check the analyses, check those that require data you have and that have not already been done
                # (Check the frequencies, that are required by the analysis for the specific S Param)
                for analysis in self.specInfo.analysisList:
                    #first check that the analysis has not been done
                    if not analysis.evaluated:
                        #second check that the data is present for this analysis
                        dataPresent = False#True

                        xLow = analysis.xAnalysisLimits[0]
                        xHigh = analysis.xAnalysisLimits[1]
                        #iterate over the sParams required
                        cnt = 0
                        cntDataPresence = 0
                        for requiredSParam in analysis.sParams:
                            requiredSParam = requiredSParam.split(',')
                            requiredSParam = requiredSParam[0].split('-')

                            sParamIndex1 = int(list(requiredSParam)[1])
                            sParamIndex2 = int(list(requiredSParam)[2])
                            if not self.currentSuggestion.DataContainer.checkDataPresence(sParamIndex1, sParamIndex2):
                                dataPresent = False
                            else:
                                cntDataPresence = cntDataPresence +1
                            cnt = cnt + 1
                        if cntDataPresence == len(analysis.sParams):
                            dataPresent = True
                        if dataPresent:
                            #this means that the analysis still needs to be performed and that all the data required is available
                            self.callProcessingFunction(analysis)
                            self.logger.info("Processing function %s : Done" % (
                                analysis.specAnalysisName))
                            analysis.evaluated = True
                            #update percent complete by 5 percent as we will have approx. 20 processing functions
                            percentIncrementPerAnalysis = 90.0/len(self.specInfo.analysisList)
                            percentQueue.put(percentIncrementPerAnalysis)
                if self.specInfo.isEverythingEvaluated():
                    #terminate analysis thread is everything has been evaluated
                    self.isActive = False

            time.sleep(2) #make sure to idle a bit

    def callProcessingFunction(self, specAnalysisDef):
        """
        Intermediate function for calling the processing functions in a way that the processing library can be updated without changing this object.
        Process functions are called by name and supplied the data and the requirements

        :param specAnalysisDef: definition of analysis
        :return: returns nothing
        """
        #Process functions are called by name and supplied the data and the requirements
        # noinspection PyBroadException
        self.currentSuggestion.lockObject.acquire()
        try:
            #first get the method instance we are looking for
            method = getattr(ProcessingLib, specAnalysisDef.processingFunctionName)
            if not method:
                raise NotImplementedError("Process not implemented")
            #get the data
            dataUsed = self.buildAnalysisDataVector(specAnalysisDef.sParams)
            #call the appropriate function
            outputs = method(dataUsed, specAnalysisDef, self.saveFilePath, self.logger)
            self.currentSuggestion.resultSummary[specAnalysisDef.specAnalysisName] = outputs
        except Exception as e:
            #print(e)
            self.logger.error(e)
            self.logger.error("Exception in %s"%(specAnalysisDef.specAnalysisName), exc_info=True)
            self.currentSuggestion.resultSummary[specAnalysisDef.specAnalysisName] = {"Suggestions":[]}
        self.currentSuggestion.lockObject.release()

    def buildAnalysisDataVector(self, sParamList):
        """
        Function used to package the data for use by the processing functions. It will also get previous data from files if needed.

        :param sParamList: parameter list to follow.
        :return: returns dataVector
        """
        # iterate through the parameter list and build a list of dataObjects
        dataVector = []
        for sp in sParamList:
            sParameterNeeded = sp.split("-")
            index1 = int(sParameterNeeded[1])
            index2 = int(sParameterNeeded[2])
            dataVector.append(self.currentSuggestion.DataContainer.getLocationData(index1, index2))
        return dataVector