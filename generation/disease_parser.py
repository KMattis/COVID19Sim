import configparser
from simulation import time

def parseDisease(configFile, diseaseName):
    config = configparser.ConfigParser()
    config.read(configFile)
    updateName = config[diseaseName]['updateName']
    contProbName = config[diseaseName]['contProbName']
    return updateName, contProbName
