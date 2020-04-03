import configparser
from simulation import time
from model import place_characteristics

def parseTimeList(listasstring) -> [int]:
    tmplist = listasstring.split(',')
    return [int(x)*time.HOUR for x in tmplist]

def parseNeedList(listasstring, needTypesDict):
    tmplist = listasstring.split(',')
    return [needTypesDict[x] for x in tmplist]

def readPlace(config, placeName, needTypesDict) -> place_characteristics.PlaceCharacteristics:
    placeType = place_characteristics.PlaceType[config[placeName]['type']]
    openDays = parseTimeList(config[placeName]['openDays'])
    openHours = parseTimeList(config[placeName]['openHours'])
    needTypes = parseNeedList(config[placeName]['needTypes'], needTypesDict)
    subType = place_characteristics.SubType[config[placeName]['subType']]
    frequency = int(config[placeName]['frequency'])
    contactFrequency = float(config[placeName]['contactFrequency']) / time.HOUR
    contactDistance = float(config[placeName]['contactDistance'])
    return place_characteristics.PlaceCharacteristics(placeType,
            openDays,
            openHours,
            needTypes,
            subType,
            frequency,
            contactFrequency,
            contactDistance)

def readPlacesWithPrefix(configFile, placeNamePrefix, needTypesDict) -> [place_characteristics.PlaceCharacteristics]:
    config = configparser.ConfigParser()
    config.read(configFile)

    placeNames = list(filter(lambda name: name.startswith(placeNamePrefix) ,config))

    return [readPlace(config, placeName, needTypesDict) for placeName in placeNames]
