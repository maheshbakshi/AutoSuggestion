'''
Master sequencer, responsible for the skeleton of the framework.
load needed tsv (Tab seperated Values) files
Use Specifications file for all input information.
Queries can also be passed from the command propt.
e.g., GET /suggestions?q=Londo&latitude=43.70011&longitude=-79.4163
Output: AutoSuggestionData/CmdLine.OUT

Set of queries can be passed from XML file using AnalyzeData section.
Output: will be stored with AutoSuggestionData//<XMLQueryName>.OUT

We can run in parallel loading set of tsv files and running queries once data is loaded.
e.g., load cities_Canada-USA.tsv and run set of queries as soon as its data is loaded.
      similarly load cities_asia and run set of queries as soon as its data is loaded.

      As we use load one tsv file and run multiple queties on it. At present it is done in a single thread.
      But if we have multiple tsv files to load and run queries on each of them, then using as multi-thrading fastens things and works.
        ....
'''
from SupportFunctions import *
import AnalysisLib
import logging, time
import MeasurementLib, queue

import sys
import pydoc

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

#Skeloton code for running multi-threaded search
# Percentage queue
percentQueue = queue.Queue()
measurementControl = MeasurementLib.MeasurementController("%s\\Specifications.xml" % DataPath, currentSuggestion.DUTResultPath,
                                                                              currentSuggestion, logger)
measurementControl.RunTests(percentQueue)

#Single threaded execution: as we have one tsv file for now.
# load all the tsv files provided in the path definitions of the Specifications path
pathIds = specInfo.pathDictionary.keys()
for PathNum in pathIds:
    TsvFileAc = r'%s\\' % DataPath + specInfo.pathDictionary[PathNum].DUTPath
    DataLib.loadLocationDataOnce(TsvFileAc, currentSuggestion, specInfo, logger, PathNum)

# Create a processing object and run set of queries using already loaded information
processor = AnalysisLib.ATSProcessor(specInfo, currentSuggestion, currentSuggestion.DUTResultPath, logger)

# Run set of queries
for i in range(len(specInfo.analysisList)):
    processor.callProcessingFunction(specInfo.getAnalysisByIndex(i))
    logger.info('Done Query: ' + specInfo.getAnalysisByIndex(i).specAnalysisName)
    print('Done Query: ' + specInfo.getAnalysisByIndex(i).specAnalysisName)