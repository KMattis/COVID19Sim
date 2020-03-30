import configparser
from simulation import time
from model import place, place_characteristics, needs

def readNeeds(configFile, personType):
    config = configparser.ConfigParser()
    config.read(configFile)
    eat = int(config[personType]['eat']) / time.DAY
    sleep = int(config[personType]['sleep']) / time.DAY
    work = int(config[personType]['work']) / time.DAY
    outdoor = int(config[personType]['outdoor']) / time.DAY
    return eat, sleep, work, outdoor
    
