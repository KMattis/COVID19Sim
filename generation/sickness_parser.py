import configparser
from simulation import time

def parseSickness(configFile, sicknessName):
    config = configparser.ConfigParser()
    config.read(configFile)
    updateName = config[sicknessName]['updateName']
    contProbName = config[sicknessName]['contProbName']
    return updateName, contProbName
