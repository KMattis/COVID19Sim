import configparser
from simulation import time
from model import place_characteristics

def parseTimeList(listasstring) -> [int]:
    tmplist = listasstring.split(',')
    return [int(x)*time.HOUR for x in tmplist]

def readPlace(config) -> place_characteristics.PlaceCharacteristics:
    placeType = place_characteristics.PlaceType[config['type']]
    openDays = parseTimeList(config['openDays'])
    openHours = parseTimeList(config['openHours'])
    subType = place_characteristics.SubType[config['subType']]
    frequency = int(config['frequency'])
    contactFrequency = float(config['contactFrequency']) / time.HOUR
    contactDistance = float(config['contactDistance'])
    return place_characteristics.PlaceCharacteristics(placeType,
            openDays,
            openHours,
            subType,
            frequency,
            contactFrequency,
            contactDistance)

def readAllPlaceChars(configFile) -> [place_characteristics.PlaceCharacteristics]:
    config = configparser.ConfigParser()
    config.read(configFile)

    return [readPlace(config[placeName]) for placeName in config if placeName != "DEFAULT"]
