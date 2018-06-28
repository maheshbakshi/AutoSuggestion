#!/bin/bash
pydoc -w SupportFunctions\SpecLib.py
copy "SpecLib.html" "SupportFunctions.SpecLib.html" 
pydoc -w SupportFunctions\ProcessingLib.py
copy "ProcessingLib.html" "SupportFunctions.ProcessingLib.html"
pydoc -w SupportFunctions\DUTObject.py
copy "DUTObject.html" "SupportFunctions.DUTObject.html"
pydoc -w SupportFunctions\DataLib.py
copy "DataLib.html" "SupportFunctions.DataLib.html"
pydoc -w MeasurementLib
pydoc -w AnalysisLib
pydoc -w AutoSuggestionTester