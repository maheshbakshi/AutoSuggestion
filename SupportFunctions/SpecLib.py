#Finds the spec or the configuration file and reads its contents
#for instructions or query criteria
"""
Finds the spec or the configuration file and reads its contents
for instructions or query criteria
"""

import xml.etree.ElementTree as ET
import sys

def getSpecInfo(specFilePath):
    """
    XML file reading, the format assumed is of the following

    :param specFilePath: path of XML input file
    :return: returns nothing
    """
    specInfo = SpecList()
    #XML file reading, the format assumed is of the following
    tree = ET.parse(specFilePath)
    root = tree.getroot()
    for child in root:
        if child.tag == "Test_Procedure":
            for information in child:
                specInfo.addGeneralInfo(information.tag, information.text)
        elif child.tag == "PathDefinitions":
            #get the paths
            for paths in child:
                pathID = int(paths.tag.replace("P",""))
                S_Params = ""
                for pathInfo in paths:
                    if pathInfo.tag == "S_Params":
                        S_Params = pathInfo.text
                specInfo.addPath(pathID, S_Params)
        elif child.tag == "AnalyseData":
            # Handle command line string
            #GET /suggestions?q=Londo&latitude=43.70011&longitude=-79.4163
            if(len(sys.argv) == 3 and sys.argv[1] == "GET" and "/suggestions?q=" in sys.argv[2]):
                query=""
                latitude=None
                longitude=None
                queryString = sys.argv[2]
                queryString = queryString.replace("/suggestions?","")
                queryList = queryString.split("&")
                for str in queryList:
                    o = str.split("=")
                    if o[0] in ("q"):
                        query = o[1]
                    elif o[0] in ("latitude"):
                        latitude = o[1]
                    elif o[0] in ("longitude"):
                        longitude = o[1]
                sParams=[]
                sParams.append("S-1-1")
                specInfo.addAnalysis("CmdLine", "GETSuggestions", query, latitude, longitude, sParams)
            else:
                print("Invalid command - Pass command line parameters as : GET /suggestions?q=Londo&latitude=43.70011&longitude=-79.4163")

            for analysis in child:
                #get the properties of this analysis
                processingFunctionName = ""
                sParams = []
                query=""
                latitude=None
                longitude=None
                for properties in analysis:
                    if properties.tag == "AnalysisType":
                        processingFunctionName = properties.text
                    elif properties.tag == "QueryString":
                        query = properties.text
                    elif properties.tag == "Latitude":
                        latitude = properties.text
                    elif properties.tag == "Longitude":
                        longitude = properties.text
                    elif properties.tag == "SP":
                        for SP in properties:
                            sParams.append(SP.text)
                specInfo.addAnalysis(analysis.tag, processingFunctionName, query, latitude, longitude,sParams)
    return specInfo

class SpecList:
    """
    Container for all spec requirements that defines the measurement and analsysis sequence.
    """
    specInfoList = dict()
    analysisList = []
    comparisonList = []
    pathDictionary = dict()
    currentMeasNumber = 0
    offset="0"

    def __init__(self):
        """
        Construct a new 'SpecList' object.

        :param :
        :return: returns nothing
        """
        self.specInfoList = dict()
        self.analysisList = []
        self.pathDictionary = dict()
        self.currentMeasNumber = 0
        self.offset="0"

    def addGeneralInfo(self, key, value):
        """
        Helps to store misc global information in a dictionary

        :param key: key to be stored
        :param value: value of the information stored
        :return: returns nothing
        """
        self.specInfoList[key] = value

    def addPath(self, pathID, specStr):
        """
        Add a path definition to the dictionary of paths

        :param pathID: path id
        :param specStr: spec
        :return: returns nothing
        """
        self.pathDictionary[pathID] = PathDefinition(pathID, specStr)

    def addAnalysis(self, specAnalysisName, processingFunctionName, query="Londo", latitude=None, longitude=None,sParams="S-1-1"):
        """
        Add a path definition to the list of analyses

        :param specComparisonName: Comparision name
        :param processingFunctionName: processing function
        :param sParam: sParams used
        :return: returns nothing
        """
        if(latitude!=None):
            latitude = float(latitude)
        if(longitude != None):
            longitude = float(longitude)
        self.analysisList.append(SpecAnalysisDefinition(specAnalysisName, processingFunctionName, query, latitude, longitude, sParams,self.specInfoList))

    def getPath(self, pathNumber):
        """
        Get a path definition for the dictionary

        :param pathNumber: path number
        :return: returns path details
        """
        return self.pathDictionary[pathNumber]

    def getAnalysisByIndex(self, analysisNumber):
        """
        Gets an analysis instance by index

        :param analysisNumber: analysis index
        :return: returns analysis details
        """
        return self.analysisList[analysisNumber]

    def isEverythingEvaluated(self):
        """
        Helps to determine if every thing is evaluated

        :param :
        :return: returns nothing
        """
        for analysis in self.analysisList:
            if not analysis.evaluated:
                return False
        #else
        return True

    def getAnalysisByName(self, analysisName):
        """
        Gets an analysis instance by analysis name

        :param analysisNumber: analysis name
        :return: returns analysis details
        """
        #search for it or else return exception
        for analysis in self.analysisList:
            if analysis.specAnalysisName == analysisName:
                return analysis

class SpecAnalysisDefinition:
    """
    Object containing information about one Analysis.
    """
    specAnalysisName = ""
    processingFunctionName = ""
    query = ""
    latitude = None
    longitude = None
    sParams = []
    specInfoList = dict()

    def __init__(self, specAnalysisName, processingFunctionName, query, latitude, longitude, sParams, specInfoList):
        """
        Construct a new 'SpecAnalysisDefinition' object.

        :param ...: uses above parameters
        :return: returns nothing
        """
        self.specAnalysisName = specAnalysisName
        self.processingFunctionName = processingFunctionName
        self.query = query
        self.latitude = latitude
        self.longitude = longitude
        self.sParams = sParams
        self.evaluated = False
        self.specInfoList = specInfoList

class PathDefinition:
    """
    Object containing information about one path.
    """
    #class to know the path definitions, basically make a dictionary containing this object
    pathID = 0
    DUTPort = ""        #ex: Rx or Tx
    portMap = []        #ex: [3, 2] means that the downlink path of the vna is connected to port 3 of DUT
    allowedSParams = [] #details the allowed sParameters that can be returned when the path is measured
    Gating = []         #Start and Stop of gating interval in ns, used for time domain
    domain = "f"#f for frequency, fd means both frequency and time

    def __init__(self, pathID, specStr ):
        """
        Construct a new 'PathDefinition' object.

        :param pathID: path
        :param specStr: spec
        :param domainStr: domain
        :param gatingStr: gating interval
        :return: returns nothing
        """
        #fill in the info from the config string
        self.pathID = pathID
        self.allowedSParams = []
        specStringParts = specStr.split(",")
        if len(specStringParts) == 2:
            #easy case
            self.DUTPath = specStringParts[0]
            ports = specStringParts[1].split("-")
            self.portMap = [int(ports[1]), int(ports[2])]
            self.allowedSParams.append("S" + "1" + "1")  # why it cannot be S22, we default to S11