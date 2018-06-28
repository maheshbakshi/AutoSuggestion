#DUT object container to encapsulate all information about one of the devices
"""
DUT object container to encapsulate all information about one of the devices.
"""
from SupportFunctions.DataLib import DataObject
from threading import Lock
import os

class DUTObject:
    """
    Container for all of the Suggestion properties pertaining to the database. Includes the measurement data and results.
    """
    
    SuggestionResultPath = ""
    SuggestionNumber = 0
    SuggestionType = ""
    DataContainer = []
    resultSummary = dict() #dictionary of results where each key is the spec analysis name
    lockObject = ""
    logger = ""
    
    def __init__(self, DUTNumber, DUTType, resultFolderPath, logger):
        """
        Construct a new 'DUTObject' object.

        :param DUTNumber: local DUT number to keep track of tested DUT data
        :param DUTType: For a given input data file(s), set of queries to run
        :param resultFolderPath: folder path
        :param logger: Object of the logger.
        :return: returns nothing
        """
        self.DUTNumber = DUTNumber
        self.DUTType = DUTType
        self.resultSummary = dict()
        self.logger = logger
        
        #Create a folder in the results path for these measurements
        if not resultFolderPath.endswith("\\"):
            resultFolderPath = "{0}\\".format(resultFolderPath)
        self.DUTResultPath = resultFolderPath
        if not os.path.exists(self.DUTResultPath):
            os.mkdir(self.DUTResultPath)
        self.DataContainer = DataObject(DUTType)
        self.lockObject = Lock()