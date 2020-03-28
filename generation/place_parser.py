import configparser
from simulation import time
from model import place, place_characteristics

def readPlace(configFile, placeName):
    config = configparser.ConfigParser()
    config.read(configFile)
    placeType = place.PlaceType[config[placeName]['type']]
    avgArrival_tmp = config[placeName]['avgArrival'].split(',')
    avgArrival = [int(x) * time.HOUR for x in avgArrival_tmp]
    avgDuration = int(config[placeName]['avgDuration']) * time.HOUR
    return place_characteristics.PlaceCharacteristics(placeType, avgArrival, avgDuration)
