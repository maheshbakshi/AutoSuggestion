"""
Library containing all functions used for processing data for the analysis framework
functions simply need to be added here and then references in the SPEC file.
The analysis framework will detect and use any and all functions presented here

this is the template for all methods in the class, methods without this
   def processName(data, specInfo):
the data you receive depends on how the measurement is defined in the spec
    if the spec says that you only need one parameter, expect only one,
    if the spec says that you need multiple s-parameters, expect an array of data objects in the same order that it is defined in the spec.
"""
import numpy as np
import json
import math
import os
my_path = os.path.abspath(__file__)

def helperDistance(originLat, originLon, destinationLat, destinationLon):
    """
    Calculate the Haversine distance.
    Reference: https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
    Parameters
    ----------
    origin : tuple of float
        (lat, long)
    destination : tuple of float
        (lat, long)

    Returns
    -------
    distance_in_km : float

    Examples
    --------
    >>> origin = (48.1372, 11.5756)  # Munich
    >>> destination = (52.5186, 13.4083)  # Berlin
    >>> round(distance(origin, destination), 1)
    504.2
    """
    lat1, lon1 = originLat, originLon
    lat2, lon2 = destinationLat, destinationLon
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d


# Take set of S-Parameters and plot them on a file and record margin in a csv
def GETSuggestions(data, specInfo, saveFilePath, logger):
    """
        Helps to get suggestions for a given query string, latitude and longitude
        :param data: the data you receive depends on how the measurement is defined in the spec
            if the specInfo says that you only need one parameter, expect only one,
            if the specInfo says that you need multiple s-parameters, expect an array of data objects in the same order that it is defined in the spec.
        :param specInfo: path
        :param saveFilePath: folder path to save json output
        :return: writes to specified output file
        """
    analysisOrCompareName = specInfo.specAnalysisName

    locationInfo = np.array(data[0].getLocationInfo())

    arrayLocNames = locationInfo[3]
    strToFind = specInfo.query
    strToFind = strToFind.lower()
    #find indices of all the maching string
    neededIndices = [i for i, item in enumerate(arrayLocNames) if strToFind in item.lower()]

    suggestionsList =[]
    keys = ["score", "latitude", "longitude", "name"]
    print("query string = "+ specInfo.query +", latitude = " + str(specInfo.latitude) + ", longitude = " +str(specInfo.longitude))
    logger.debug("query string = "+ specInfo.query +", latitude = " + str(specInfo.latitude) + ", longitude = " +str(specInfo.longitude))
    logger.debug("=======================================================================================================")
    for i in neededIndices:
        initernalSugessionDict = {}
        for j in range(len(keys)):
            if j==0:#compute score if latitude and longitude are not None else score = 1
                if specInfo.latitude != None:
                    #compute distance between searched results and query - Latitude and Longitude
                    dist = helperDistance(specInfo.latitude, specInfo.longitude, (float)(locationInfo[1][i]), (float)(locationInfo[2][i]))
                    if(dist<10):
                        score = 1
                    elif(dist < 100):
                        score = 0.8
                    elif(dist < 250):
                        score = 0.6
                    elif (dist < 500):
                        score = 0.8
                    elif (dist < 750):
                        score = 0.6
                    elif (dist < 1000):
                        score = 0.4
                    elif (dist < 1500):
                        score = 0.2
                    else:
                        score = 0.1
                    initernalSugessionDict[keys[j]] = score
                else:
                    initernalSugessionDict[keys[j]] = 1
            else:
                initernalSugessionDict[keys[j]] =  locationInfo[j][i]
        # debug information
        for x in initernalSugessionDict:
            logger.debug(x + ':' + str(initernalSugessionDict[x]))
        #print(initernalSugessionDict)
        suggestionsList.append(initernalSugessionDict)
    logger.debug("=======================================================================================================")
    results = {"Suggestions":suggestionsList}
    print("=======================================================================================================")
    print(results)
    print("=======================================================================================================")

    savePath = saveFilePath + analysisOrCompareName + '.OUT'
    with open(savePath, 'w') as f:
        #json.dump(suggestionsList, f, ensure_ascii=False)
        json.dump(results, f, ensure_ascii=False)

    return results