import configparser
from simulation import time
from model import place_characteristics, needs

def parseTimeList(listasstring) -> [int]:
    tmplist = listasstring.split(',')
    return [int(x)*time.HOUR for x in tmplist]

def parseNeedList(listasstring, needTypesDict):
    tmplist = listasstring.split(',')
    return [needTypesDict[x] for x in tmplist]

def readPlace(configFile, placeName, needTypesDict) -> place_characteristics.PlaceCharacteristics:
    config = configparser.ConfigParser()
    config.read(configFile)
    placeType = place_characteristics.PlaceType[config[placeName]['type']]
    avgArrival = parseTimeList(config[placeName]['avgArrival'])
    avgDuration = int(config[placeName]['avgDuration']) * time.HOUR
    openDays = parseTimeList(config[placeName]['openDays'])
    openHours = parseTimeList(config[placeName]['openHours'])
    needTypes = parseNeedList(config[placeName]['needTypes'], needTypesDict)
    subType = place_characteristics.SubType[config[placeName]['subType']]
    frequency = int(config[placeName]['frequency'])
    return place_characteristics.PlaceCharacteristics(placeType,
            avgArrival,
            avgDuration,
            openDays,
            openHours,
            needTypes,
            subType,
            frequency)
