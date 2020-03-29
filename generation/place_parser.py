import configparser
from simulation import time
from model import place, place_characteristics, needs

def parseTimeList(listasstring):
    tmplist = listasstring.split(',')
    return [int(x)*time.HOUR for x in tmplist]

def readPlace(configFile, placeName):
    config = configparser.ConfigParser()
    config.read(configFile)
    placeType = place.PlaceType[config[placeName]['type']]
    avgArrival = parseTimeList(config[placeName]['avgArrival'])
    avgDuration = int(config[placeName]['avgDuration']) * time.HOUR
    openDays = parseTimeList(config[placeName]['openDays'])
    openHours = parseTimeList(config[placeName]['openHours'])
    needType =needs.NeedType[config[placeName]['needType']]
    return place_characteristics.PlaceCharacteristics(placeType, avgArrival, avgDuration, openDays, openHours, needType)
