import math
import random

from model import grid, place, place_characteristics
from simulation import time
from generation import place_parser

def generate(size, needTypes):

    needTypesDict = {}
    for needType in needTypes:
        needTypesDict[needType.getName()] = needType

    theGrid = grid.Grid(size)
    
    workplaceChars = place_parser.readPlacesWithPrefix("simconfig/places.ini", "work", needTypesDict)
    workplaceCharFreqs = [char.frequency for char in workplaceChars]

    outdoorChars = place_parser.readPlacesWithPrefix('simconfig/places.ini', 'outdoor', needTypesDict)
    homeChars = place_parser.readPlacesWithPrefix('simconfig/places.ini', 'home', needTypesDict)
    noneChar = place_characteristics.PlaceCharacteristics(place_characteristics.PlaceType.NONE,0,0,0,0, [None], place_characteristics.SubType.NONE, 0)
    healthcareChars = place_parser.readPlacesWithPrefix('simconfig/places.ini', 'healthcare', needTypesDict)

    centerx = size / 2
    centery = size / 2
    for i in range(size):
        for j in range(size):
            radius2 = (i - centerx)**2 + (j - centery)**2
            if radius2 > size**2 / 4:
                c = noneChar
            else: 
                maxRadius = size / 2
                pWork = ((maxRadius - math.sqrt(radius2)) / maxRadius) * 0.6
                pPark = 0.1
                pHealthcare = 0.002
                
                p = random.random()

                if p < pWork:
                    c = random.choices(workplaceChars, workplaceCharFreqs)[0]
                elif p < pWork + pPark:
                    c = random.choice(outdoorChars)
                elif p < pWork + pPark + pHealthcare:
                    c = random.choice(healthcareChars)
                else:
                    c = random.choice(homeChars)
            theGrid.addPlace(place.Place(i, j, "", c))
    theGrid.getDistanceMap().calcDistances()
    return theGrid

