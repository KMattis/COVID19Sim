import math
import random

from model import grid, place, place_characteristics, needs
from simulation import time
from generation import place_parser

def generate(size, needTypes):

    needTypesDict = {}
    for needType in needTypes:
        needTypesDict[needType.getName()] = needType

    theGrid = grid.Grid(size)
    
    workplaceChars = [place_parser.readPlace("simconfig/places.ini", "work." + str(k), needTypesDict) for k in range(2)]
    workplaceCharFreqs = [char.frequency for char in workplaceChars]

    centerx = size / 2
    centery = size / 2
    for i in range(size):
        for j in range(size):
            radius2 = (i - centerx)**2 + (j - centery)**2
            if radius2 > size**2 / 4:
                c = place_characteristics.PlaceCharacteristics(place_characteristics.PlaceType.NONE,0,0,0,0, [None], place_characteristics.SubType.NONE, 0)
            else: 
                maxRadius = size / 2
                pWork = ((maxRadius - math.sqrt(radius2)) / maxRadius) * 0.6
                pPark = 0.1
                
                p = random.random()

                if p < pWork:
                    c = random.choices(workplaceChars, workplaceCharFreqs)[0]
                elif p < pWork + pPark:
                    c = place_parser.readPlace('simconfig/places.ini', 'outdoor',needTypesDict)
                else:
                    c = place_parser.readPlace('simconfig/places.ini', 'home', needTypesDict)
            theGrid.addPlace(place.Place(i, j, "", c))
    theGrid.getDistanceMap().calcDistances()
    return theGrid
