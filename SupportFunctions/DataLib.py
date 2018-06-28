"""
Multiple containers for storing and retrieving data easily

Test data loader, need function to be able to load data from a tsv file format
"""


# noinspection PyBroadException Used for Ana
def loadLocationDataOnce(filePath, dataObj, specLib, logger, DUTPath=10):
    """
    Loads data from a TSV file and populates a data object.

    :param filePath: path to MAT data
    :param dataObj: dataobject to populate
    :param specLib: object of specLib (path definitions, sizeOfChunk)
    :params logger:  Object to looger, to log data for information.
    :params DUTPath: path number to fetch
    :return: returns nothing
    """
    #Load raw data, format it and store it in the given dataObj class
    logger.debug("Load tsv data of file: %s."%(filePath))
    try:
        frequency = []
        asciiNames = []
        data = []

        f = open(filePath, encoding="utf8")
        #listNeededInformation = []
        lengthOfPrevChunk = 19 #Do not use constants
        prevUnsavedInfo = ""
        currentPath = specLib.pathDictionary.get(DUTPath)
        for chuck in readInChunks(f, int(specLib.specInfoList["ReadFileChunkSize"])):
            #below function can be run in parallel or on different threads if we make sure chunk ends after a new line character.
            #We assumes new line characters are not present inside each line.
            #We assume tab is not present inside the unicode code characters.
            prevUnsavedInfo, id, ascNames, loc = fetchNeededInformation(chuck, lengthOfPrevChunk, prevUnsavedInfo, frequency, asciiNames, data)
            #copy list to our global data (not just reference)
            frequency.extend(id[:])
            asciiNames.extend(ascNames[:])
            data.extend(loc[:])
        f.close()
        # now add this data to the data object at the start index
        storeData = list(zip(*data))
        sData = LocationData()
        sData.storeData(frequency, storeData[0], storeData[1], asciiNames)
        # add to complete data matrix
        dataObj.DataContainer.addLocationData(currentPath.portMap[0], currentPath.portMap[1], sData)
        return sData
    except Exception as e:
        print(e)
        #logger.error("Exception in %s" % (specAnalysisDef.specAnalysisName), exc_info=True)


def readInChunks(fileObj, chunkSize=2048):
    """
    Lazy function to read a file piece by piece.
    Default chunk size: 2kB.
    """
    while True:
        data = fileObj.read(chunkSize)
        if not data:
            break
        yield data

def fetchNeededInformation(chuck, lengthOfPrevChunk, prevUnsavedInfo, frequency, asciiNames, data):

    #lines = chuck.readlines()
    lines = chuck.splitlines()
    #lines = chuck.split("\n")
    firstLine = True

    #outout variables
    frequency = []
    asciiNames = []
    locData = []
    # lengthOfPrevChunk = len(line.split("\t"))
    for line in lines:
        #Append prevUnusedInfo if it is first line of chunk
        if(firstLine):
            line = prevUnsavedInfo + line
        # initial prevUnsavedInfo to "" otherwise it may create problem, if last chunk holds entire line but it stores last last message wrongly.
        prevUnsavedInfo = ""
        words = line.split("\t")

        # store header
        if(words[0]=="id"):
            info = words[0] + " " + words[2] + " " + words[4] + " " + words[5]
            #listNeededInformation.append(info)
        elif (len(words) == lengthOfPrevChunk):#Storing data starts here
            #prevUnsavedInfo = ""
            frequency.append(int(words[0]))
            asciiNames.append(words[2])
            locData.append([float(words[4]), float(words[5])])
        # Store last unfinished line in prevUnsavedInfo
        else:
            prevUnsavedInfo = line
        firstLine = False
    return prevUnsavedInfo, frequency, asciiNames, locData

def createEmptySParam():
    """
    Creates an Sparam Container with nothing in it to emulate and 0 value in the matrix.

    :param :
    :return: emptyContainer
    """
    #for storing sections with 0
    emptyContainer = LocationData()
    emptyContainer.storeData([],[],[],[])
    return emptyContainer

class DataObject:
    """
    Data Container for all of the RX or TX data. Effectively a matrix of S-Parameters.
    """
    SuggestionType = "" #cities_canada-usa, cities_asia, cities_africa
    locationDataMatrix = []

    def __init__(self, SuggestionType):
        """
        Construct a new 'DataObject' object.

        :param SuggestionType: cities_canada_usa
        :return: returns nothing
        """
        self.SuggestionType = SuggestionType
        self.locationDataMatrix = []
        #default size but also given the possibility for expansion
        #place holder to store location data in a matrix, it can be a list.
        for i in range(6):
            aRow = [createEmptySParam()]
            self.locationDataMatrix.append(aRow)

    def addLocationData(self, sParamIndex1, sParamIndex2, sData):
        """
        Adds Frequency S-Param data to matrix frequencyDataMatrix.
        Increase its default size if needed.

        :param sParamIndex1: S-Param first index
        :param sParamIndex2: S-Param second index
        :param sData: data to append to matrix
        :return: returns nothing
        """
        #check if the matrix is big enough
        if len(self.locationDataMatrix) < sParamIndex1:
            self.increaseLocationSizeTo(sParamIndex1, sParamIndex2)
        elif len(self.locationDataMatrix[sParamIndex1-1]) < sParamIndex2:
            self.increaseLocationSizeTo(sParamIndex1, sParamIndex2)
        #sData must be an SParamData object or 0
        if sData == 0:
            #clear the entry to 0
            self.locationDataMatrix[sParamIndex1-1][sParamIndex2-1] = createEmptySParam("S-" + str(sParamIndex1) +"-"+ str(sParamIndex2), False)
        else:
            self.locationDataMatrix[sParamIndex1-1][sParamIndex2-1]= sData # Just use new data
            #self.locationDataMatrix[sParamIndex1-1][sParamIndex2-1].append(sData)

    def getLocationData(self, sParamIndex1, sParamIndex2):
        """
        fetch Location data to matrix locationDataMatrix.
        Increase its default size if needed.

        :param sParamIndex1: S-Param first index
        :param sParamIndex2: S-Param second index
        :param sData: data to append to matrix
        :return: returns nothing
        """
        return self.locationDataMatrix[sParamIndex1-1][sParamIndex2-1]

    # noinspection PyBroadException
    def checkDataPresence(self, sParamIndex1, sParamIndex2):
        """
        checks if there exists  some data at the specified S-Paramater in out time or frequency data matrix.

        :param sParamIndex1: S-Param first index
        :param sParamIndex2: S-Param second index
        :param isTime: is it time domain or frequency domain.
        :return: returns nothing
        """
        try:
            dataPoint = self.locationDataMatrix[sParamIndex1-1][sParamIndex2-1]
            if len(dataPoint.frequencies) > 0:
                return True
            else:
                return False
        except Exception as e:
            #when there is a problem is means that the data is not ready
            return False

    def increaseLocationSizeTo(self, rowSize, ColumnSize):
        """
        start by checking how many elements are missing in each column
        now do the rows. If there is a need increase MatrixSize

        checks if there exists  some data at the specified S-Paramater in out time or frequency data matrix.

        :param rowSize: size of the row to store data
        :param colSize: size of the column.
        :return: returns nothing
        """
        #start by checking how many elements are missing in each column
        currentColCount = len(self.locationDataMatrix[0])
        currentRowCount = len(self.locationDataMatrix)
        missingCol = max(ColumnSize - currentColCount, 0)
        for i in range(currentRowCount):
            for j in range(missingCol):
                self.locationDataMatrix[i].append(createEmptySParam())
        #now do the rows
        missingRows = max(rowSize - currentRowCount, 0)
        for i in range(missingRows):
            #create a row
            aRow = []
            for j in range(len(self.locationDataMatrix[0])):
                aRow.append(createEmptySParam())
            self.locationDataMatrix.append(aRow)

class LocationData:
    """
    Data container for one S Parameter.
    """
    sParamType = "" #S11, S22, S12, ...
    ids = []
    longitudes = []
    latitudes = []
    asciiNames = []


    def __init__(self):
        """
        Construct a new 'LocationData' object.

        :param ...: Required parameters
        :return: returns nothing
        """
        self.ids = []

    def storeData(self, ids, latitudes, longitudes, asciiNames = []):
        """
        Stores measurement data into the object.

        :param id: id of the location
        :param latitude: location coordinates
        :param longitude: location coordinates
        :param asciiNames: ascii name of the location
        :return: nothing to return
        """
        self.ids = list(ids)
        self.latitudes = list(latitudes)
        self.longitudes = list(longitudes)
        self.asciiNames = list(asciiNames)

    def getLocationInfo(self):
        """
        Fetches all places needed location information(ids, latitudes, longitudes and asciiNames).

        :param:
        :return: list of ids, latitudes, longitudes and ascii names of the location
        """
        return [self.ids, self.latitudes, self.longitudes, self.asciiNames]

    def getLocationName(self):
        """
        etches all locations ids and names.

        :param:
        :return: list of ids and ascii names of the location
        """
        return [self.ids, self.asciiNames]

    def getLocationCoordinates(self):
        """
        Fetches all places location coordinates(ids, latitudes and longitudes).

        :param:
        :return: list of ids latitudes and longitudes of the location
        """
        return [self.ids, self.latitudes, self.longitudes]
