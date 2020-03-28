import math
import random

from model import grid, place, place_characteristics
from simulation import time

def generate(size):
    theGrid = grid.Grid(size)
    
    centerx = size / 2
    centery = size / 2
    for i in range(size):
        for j in range(size):
            radius2 = (i - centerx)**2 + (j - centery)**2
            if radius2 > size**2 / 4:
                c = place_characteristics.PlaceCharacteristics(place.PlaceType.NONE, 0, 0)
            else: 
                maxRadius = size / 2
                pService = ((maxRadius - math.sqrt(radius2)) / maxRadius) * 0.5
                pPark = 0.1
                pNonService = 0.15
                
                p = random.random()

                if p < pService:
                    c = place_characteristics.PlaceCharacteristics(place.PlaceType.SERVICE, 9*time.HOUR, 16 * time.HOUR)
                elif p < pService + pPark:
                    c = place_characteristics.PlaceCharacteristics(place.PlaceType.OUTDOOR, 0, 0)
                elif p < pService + pPark + pNonService:
                    c = place_characteristics.PlaceCharacteristics(place.PlaceType.NONSERVICE, 7 * time.HOUR, 17 * time.HOUR)
                else:
                    c = place_characteristics.PlaceCharacteristics(place.PlaceType.HOME, 0, 0)
            theGrid.addPlace(place.Place(i, j, "", c))

    return theGrid

