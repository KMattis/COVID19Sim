import math
import random

from model import grid, place, place_characteristics
from simulation import time
from generation import place_parser
from plotting import logging

def generate(model_data, needTypes):
    needTypesDict = {}
    for needType in needTypes:
        needTypesDict[needType.getName()] = needType

    size = int(model_data["gridSize"])
    places_file = model_data["places"]

    theGrid = grid.Grid(size)
    
    chars = place_parser.readAllPlaceChars(places_file)
    charFreqs = [char.frequency for char in chars]

    centerx = size / 2
    centery = size / 2

    numPlaces = {}
    for placeType in place_characteristics.PlaceType:
        numPlaces[placeType] = 0

    for i in range(size):
        for j in range(size):
            if (i - centerx)**2 + (j - centery)**2 > size**2 / 4:
                c = place_characteristics.NONE_CHAR
            else:
                c = random.choices(chars, charFreqs)[0]
            numPlaces[c.placeType] += 1
            theGrid.addPlace(place.Place(i, j, "", c))

    for placeType in numPlaces:
        logging.write("output", placeType.name, numPlaces[placeType])

    theGrid.getDistanceMap().calcDistances()
    return theGrid

