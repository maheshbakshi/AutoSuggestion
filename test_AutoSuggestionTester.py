#python -m unittest testAutoSuggestionTester
#python testAutoSuggestionTester.py
import unittest
from SupportFunctions import *
import AnalysisLib
import logging, time
import MeasurementLib, queue

class TestProcessingLib(unittest.TestCase):
    def test_AutoSuggestionExactLocation(self):
        print("Unit test 1")
        # Folder path used to store all input and output files
        DataPath = 'AutoSuggestionData'

        # Information needed for logger
        timeStr = time.strftime("%Y%m%d%H%M")
        logger = logging.getLogger('TestSequencer')
        hdlr = logging.FileHandler('%s\\Logs\\TestSequencer%s.log' % (DataPath, timeStr))
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(logging.DEBUG)  # We can have different granularity of logging (e.g., INFO, DEBUG, WARNING...)

        logger.info("Cities_Canada-USA automated Suggestions in progress....")
        print("Fetching all data and processing. Please wait...")

        # load Specifications input file
        specInfo = SpecLib.getSpecInfo("%s\\UnitTest1_Specifications.xml" % DataPath)
        # Suggestion object to load entire suggestions information.
        # Can store multiple Suggestion objects, helpful if we need to do analysis on all summary data suggestions
        currentSuggestion = DUTObject.DUTObject(1, "cities_canada-usa", DataPath, logger)

        # Skeloton code for running multi-threaded search
        # Percentage queue
        percentQueue = queue.Queue()
        measurementControl = MeasurementLib.MeasurementController("%s\\Specifications.xml" % DataPath,
                                                                  currentSuggestion.DUTResultPath,
                                                                  currentSuggestion, logger)
        ##measurementControl.RunTests(percentQueue)

        # Single threaded execution: as we have one tsv file for now.
        # load all the tsv files provided in the path definitions of the Specifications path
        pathIds = specInfo.pathDictionary.keys()
        for PathNum in pathIds:
            TsvFileAc = r'%s\\' % DataPath + specInfo.pathDictionary[PathNum].DUTPath
            DataLib.loadLocationDataOnce(TsvFileAc, currentSuggestion, specInfo, logger)

        # Create a processing object and run set of queries using already loaded information
        processor = AnalysisLib.ATSProcessor(specInfo, currentSuggestion, currentSuggestion.DUTResultPath, logger)

        # Run set of queries
        #for i in range(len(specInfo.analysisList)):
        analysis = specInfo.getAnalysisByName("QueryLondonExactCoordinates")
        processor.callProcessingFunction(analysis)
        logger.info('Done Query: QueryLondonExactCoordinates')# + specInfo.getAnalysisByIndex(i).specAnalysisName)
        print('Done Query: QueryLondonExactCoordinates')# + specInfo.getAnalysisByIndex(i).specAnalysisName)
        actualResult = currentSuggestion.resultSummary["QueryLondonExactCoordinates"]
        expectedResult = {'Suggestions': [{'longitude': '-81.23304', 'latitude': '42.98339', 'score': 1, 'name': 'London'}]}
        self.assertEqual(expectedResult, actualResult)

    def test_AutoSuggestionQueryLondonLat0Long0(self):
        print("Unit test 2")
        # Folder path used to store all input and output files
        DataPath = 'AutoSuggestionData'

        # Information needed for logger
        timeStr = time.strftime("%Y%m%d%H%M")
        logger = logging.getLogger('TestSequencer')
        hdlr = logging.FileHandler('%s\\Logs\\TestSequencer%s.log' % (DataPath, timeStr))
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(logging.DEBUG)  # We can have different granularity of logging (e.g., INFO, DEBUG, WARNING...)

        logger.info("Cities_Canada-USA automated Suggestions in progress....")
        print("Fetching all data and processing. Please wait...")

        # load Specifications input file
        specInfo = SpecLib.getSpecInfo("%s\\UnitTest1_Specifications.xml" % DataPath)
        # Suggestion object to load entire suggestions information.
        # Can store multiple Suggestion objects, helpful if we need to do analysis on all summary data suggestions
        currentSuggestion = DUTObject.DUTObject(1, "cities_canada-usa", DataPath, logger)

        # Skeloton code for running multi-threaded search
        # Percentage queue
        percentQueue = queue.Queue()
        measurementControl = MeasurementLib.MeasurementController("%s\\Specifications.xml" % DataPath,
                                                                  currentSuggestion.DUTResultPath,
                                                                  currentSuggestion, logger)
        ##measurementControl.RunTests(percentQueue)

        # Single threaded execution: as we have one tsv file for now.
        # load all the tsv files provided in the path definitions of the Specifications path
        pathIds = specInfo.pathDictionary.keys()
        for PathNum in pathIds:
            TsvFileAc = r'%s\\' % DataPath + specInfo.pathDictionary[PathNum].DUTPath
            DataLib.loadLocationDataOnce(TsvFileAc, currentSuggestion, specInfo, logger)

        # Create a processing object and run set of queries using already loaded information
        processor = AnalysisLib.ATSProcessor(specInfo, currentSuggestion, currentSuggestion.DUTResultPath, logger)

        # Run set of queries
        # for i in range(len(specInfo.analysisList)):
        analysis = specInfo.getAnalysisByName("QueryLondonLat0Long0")
        processor.callProcessingFunction(analysis)
        logger.info('Done Query: QueryLondonLat0Long0')  # + specInfo.getAnalysisByIndex(i).specAnalysisName)
        print(
            'Done Query: QueryLondonLat0Long0')  # + specInfo.getAnalysisByIndex(i).specAnalysisName)
        actualResult = currentSuggestion.resultSummary["QueryLondonLat0Long0"]
        expectedResult = {
            'Suggestions': [{'longitude': '-81.23304', 'latitude': '42.98339', 'score': 0.1, 'name': 'London'}]}
        self.assertEqual(expectedResult, actualResult)

    def test_AutoSuggestionQueryLondonNoLatLong(self):
        print("Unit test 3")
        # Folder path used to store all input and output files
        DataPath = 'AutoSuggestionData'

        # Information needed for logger
        timeStr = time.strftime("%Y%m%d%H%M")
        logger = logging.getLogger('TestSequencer')
        hdlr = logging.FileHandler('%s\\Logs\\TestSequencer%s.log' % (DataPath, timeStr))
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(logging.DEBUG)  # We can have different granularity of logging (e.g., INFO, DEBUG, WARNING...)

        logger.info("Cities_Canada-USA automated Suggestions in progress....")
        print("Fetching all data and processing. Please wait...")

        # load Specifications input file
        specInfo = SpecLib.getSpecInfo("%s\\UnitTest1_Specifications.xml" % DataPath)
        # Suggestion object to load entire suggestions information.
        # Can store multiple Suggestion objects, helpful if we need to do analysis on all summary data suggestions
        currentSuggestion = DUTObject.DUTObject(1, "cities_canada-usa", DataPath, logger)

        # Skeloton code for running multi-threaded search
        # Percentage queue
        percentQueue = queue.Queue()
        measurementControl = MeasurementLib.MeasurementController("%s\\Specifications.xml" % DataPath,
                                                                  currentSuggestion.DUTResultPath,
                                                                  currentSuggestion, logger)
        ##measurementControl.RunTests(percentQueue)

        # Single threaded execution: as we have one tsv file for now.
        # load all the tsv files provided in the path definitions of the Specifications path
        pathIds = specInfo.pathDictionary.keys()
        for PathNum in pathIds:
            TsvFileAc = r'%s\\' % DataPath + specInfo.pathDictionary[PathNum].DUTPath
            DataLib.loadLocationDataOnce(TsvFileAc, currentSuggestion, specInfo, logger)

        # Create a processing object and run set of queries using already loaded information
        processor = AnalysisLib.ATSProcessor(specInfo, currentSuggestion, currentSuggestion.DUTResultPath, logger)

        # Run set of queries
        # for i in range(len(specInfo.analysisList)):
        analysis = specInfo.getAnalysisByName("QueryLondonNoLatLong")
        processor.callProcessingFunction(analysis)
        logger.info('Done Query: QueryLondonNoLatLong')  # + specInfo.getAnalysisByIndex(i).specAnalysisName)
        print(
            'Done Query: QueryLondonNoLatLong')  # + specInfo.getAnalysisByIndex(i).specAnalysisName)
        actualResult = currentSuggestion.resultSummary["QueryLondonNoLatLong"]
        expectedResult = {
            'Suggestions': [{'longitude': '-81.23304', 'latitude': '42.98339', 'score': 1, 'name': 'London'}]}
        self.assertEqual(expectedResult, actualResult)

    def test_AutoSuggestionQueryNotExistingName(self):
        print("Unit test 4")
        # Folder path used to store all input and output files
        DataPath = 'AutoSuggestionData'

        # Information needed for logger
        timeStr = time.strftime("%Y%m%d%H%M")
        logger = logging.getLogger('TestSequencer')
        hdlr = logging.FileHandler('%s\\Logs\\TestSequencer%s.log' % (DataPath, timeStr))
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(logging.DEBUG)  # We can have different granularity of logging (e.g., INFO, DEBUG, WARNING...)

        logger.info("Cities_Canada-USA automated Suggestions in progress....")
        print("Fetching all data and processing. Please wait...")

        # load Specifications input file
        specInfo = SpecLib.getSpecInfo("%s\\UnitTest1_Specifications.xml" % DataPath)
        # Suggestion object to load entire suggestions information.
        # Can store multiple Suggestion objects, helpful if we need to do analysis on all summary data suggestions
        currentSuggestion = DUTObject.DUTObject(1, "cities_canada-usa", DataPath, logger)

        # Skeloton code for running multi-threaded search
        # Percentage queue
        percentQueue = queue.Queue()
        measurementControl = MeasurementLib.MeasurementController("%s\\Specifications.xml" % DataPath,
                                                                  currentSuggestion.DUTResultPath,
                                                                  currentSuggestion, logger)
        ##measurementControl.RunTests(percentQueue)

        # Single threaded execution: as we have one tsv file for now.
        # load all the tsv files provided in the path definitions of the Specifications path
        pathIds = specInfo.pathDictionary.keys()
        for PathNum in pathIds:
            TsvFileAc = r'%s\\' % DataPath + specInfo.pathDictionary[PathNum].DUTPath
            DataLib.loadLocationDataOnce(TsvFileAc, currentSuggestion, specInfo, logger)

        # Create a processing object and run set of queries using already loaded information
        processor = AnalysisLib.ATSProcessor(specInfo, currentSuggestion, currentSuggestion.DUTResultPath, logger)

        # Run set of queries
        # for i in range(len(specInfo.analysisList)):
        analysis = specInfo.getAnalysisByName("QueryNotExistingName")
        processor.callProcessingFunction(analysis)
        logger.info('Done Query: QueryNotExistingName')  # + specInfo.getAnalysisByIndex(i).specAnalysisName)
        print(
            'Done Query: QueryNotExistingName')  # + specInfo.getAnalysisByIndex(i).specAnalysisName)
        actualResult = currentSuggestion.resultSummary["QueryNotExistingName"]
        expectedResult = {
            'Suggestions': []}
        self.assertEqual(expectedResult, actualResult)

    def test_AutoSuggestionExactLocationDemoData(self):
        print("Unit test 5")
        # Folder path used to store all input and output files
        DataPath = 'AutoSuggestionData'

        # Information needed for logger
        timeStr = time.strftime("%Y%m%d%H%M")
        logger = logging.getLogger('TestSequencer')
        hdlr = logging.FileHandler('%s\\Logs\\TestSequencer%s.log' % (DataPath, timeStr))
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(logging.DEBUG)  # We can have different granularity of logging (e.g., INFO, DEBUG, WARNING...)

        logger.info("Cities_Canada-USA automated Suggestions in progress....")
        print("Fetching all data and processing. Please wait...")

        # load Specifications input file
        specInfo = SpecLib.getSpecInfo("%s\\Specifications.xml" % DataPath)
        # Suggestion object to load entire suggestions information.
        # Can store multiple Suggestion objects, helpful if we need to do analysis on all summary data suggestions
        currentSuggestion = DUTObject.DUTObject(1, "cities_canada-usa", DataPath, logger)

        # Skeloton code for running multi-threaded search
        # Percentage queue
        percentQueue = queue.Queue()
        measurementControl = MeasurementLib.MeasurementController("%s\\Specifications.xml" % DataPath,
                                                                  currentSuggestion.DUTResultPath,
                                                                  currentSuggestion, logger)
        ##measurementControl.RunTests(percentQueue)

        # Single threaded execution: as we have one tsv file for now.
        # load all the tsv files provided in the path definitions of the Specifications path
        pathIds = specInfo.pathDictionary.keys()
        for PathNum in pathIds:
            TsvFileAc = r'%s\\' % DataPath + specInfo.pathDictionary[PathNum].DUTPath
            DataLib.loadLocationDataOnce(TsvFileAc, currentSuggestion, specInfo, logger)

        # Create a processing object and run set of queries using already loaded information
        processor = AnalysisLib.ATSProcessor(specInfo, currentSuggestion, currentSuggestion.DUTResultPath, logger)

        # Run set of queries
        for i in range(len(specInfo.analysisList)):
            if specInfo.getAnalysisByIndex(i).specAnalysisName=="QueryLondonExactCoordinates":
                processor.callProcessingFunction(specInfo.getAnalysisByIndex(i))
                logger.info('Done Query: ' + specInfo.getAnalysisByIndex(i).specAnalysisName)
                print('Done Query: ' + specInfo.getAnalysisByIndex(i).specAnalysisName)
                actualResult = currentSuggestion.resultSummary[specInfo.getAnalysisByIndex(i).specAnalysisName]
                expectedResult = {'Suggestions': [{'longitude': '-81.23304', 'latitude': '42.98339', 'score': 1, 'name': 'London'}, {'longitude': '-84.08326', 'latitude': '37.12898', 'score': 0.6, 'name': 'London'}, {'longitude': '-76.54941', 'latitude': '38.93345', 'score': 0.6, 'name': 'Londontowne'}, {'longitude': '-83.44825', 'latitude': '39.88645', 'score': 0.8, 'name': 'London'}, {'longitude': '-72.09952', 'latitude': '41.35565', 'score': 0.4, 'name': 'New London'}, {'longitude': '-71.37395', 'latitude': '42.86509', 'score': 0.4, 'name': 'Londonderry'}, {'longitude': '-88.73983', 'latitude': '44.39276', 'score': 0.6, 'name': 'New London'}]}
                print(actualResult)
                print(expectedResult)
                self.assertEqual(expectedResult, actualResult)

if __name__=="__main__":
    unittest.main()
