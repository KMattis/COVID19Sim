import configparser
from simulation import time
from model import place, place_characteristics


def readPlace(configFile, placeName):
    config = configparser.ConfigParser()
    config.read(configFile)
    placeType = place.PlaceType[config[placeName]['type']]
    avgArrival = int(config[placeName]['avgArrival'])
    avgDeparture = int(config[placeName]['avgDeparture'])
    return place_characteristics.PlaceCharacteristics(placeType, avgArrival*time.HOUR, avgDeparture*time.HOUR)
