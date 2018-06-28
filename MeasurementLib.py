"""
Measurement library for handing the process sequence for performing test measurements with the tsv data
Used only for multi threading - Skeliton to get an idea not throughly tested.
"""

from multiprocessing.pool import ThreadPool
from SupportFunctions import *
import AnalysisLib


def GetMeasurementsFromTSVFile(processor):
    '''
    Fetches needed file paths for TSV files to load and inserts into the queue.
    This queue is used to fetch TSV data
    :param processor: Object of analysis lib
    :return:
    '''
    try:
        DataPath = 'AutoSuggestionData'
        specPath = "%s\\Specifications.xml" % DataPath
        specInfo = SpecLib.getSpecInfo(specPath)
        pathIds = specInfo.pathDictionary.keys()
        for PathNum in pathIds:
            TsvFileAc = r'%s\\' % DataPath + specInfo.pathDictionary[PathNum].DUTPath
            processor.dataQueue.put(TsvFileAc)
    except Exception as e:
        print(e)

class MeasurementController:
    currentSuggestion = ""
    DataProcessor = ""
    specFolderPath = ""
    specInfo = ""
    resultFolderPath = ""
    logger = ""

    def __init__(self, specFolderPath, resultFolderPath, currentSuggestion, logger):
        """
        Construct a new 'MeasurementController' object.

        :param specFolderPath: spec folder path
        :param resultFolderPath: output data folder path
        :param currentDUT: object for storing DUTInfo
        :param codeOneController: Object of codeOneController
        :param logger: Object of the logger
        :return: returns nothing
        """
        self.logger = logger
        self.resultFolderPath = resultFolderPath
        self.currentSuggestion = currentSuggestion
        self.DataProcessor = AnalysisLib.ATSProcessor(specFolderPath, currentSuggestion, currentSuggestion.DUTResultPath, logger)
        self.specFolderPath = specFolderPath
        self.specInfo = SpecLib.getSpecInfo(specFolderPath)

    def RunTests(self, percentQueue):
        """
        Complete test procedure. Obtains the required measurements and analyses to perform from the Spec file..

        :param percentQueue: needed for user interface updates
        :return: returns nothing
        """
        #Multithread support
        pool = ThreadPool(processes=2)
        processor = AnalysisLib.ATSProcessor(self.specInfo, self.currentSuggestion, self.currentSuggestion.DUTResultPath, self.logger)
        measurementThreadOutput = pool.apply_async(GetMeasurementsFromTSVFile, args=[processor])
        analysisThreadOutput = pool.apply_async(processor.RunAnalysis, args=[percentQueue])

        pool.close()
        pool.join()