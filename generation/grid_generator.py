import math
import random

from model import grid, place, place_characteristics, needs
from simulation import time
from generation import place_parser

def generate(size):
    theGrid = grid.Grid(size)
    
    centerx = size / 2
    centery = size / 2
    for i in range(size):
        for j in range(size):
            radius2 = (i - centerx)**2 + (j - centery)**2
            if radius2 > size**2 / 4:
                c = place_characteristics.PlaceCharacteristics(place.PlaceType.NONE,0,0,0,0, [needs.NeedType.NONE], place.SubType.NONE)
            else: 
                maxRadius = size / 2
                pWork = ((maxRadius - math.sqrt(radius2)) / maxRadius) * 0.6
                pPark = 0.1
                
                p = random.random()

                if p < pWork:
                    k = random.randrange(0, 3)
                    c = place_parser.readPlace('places.ini', 'work.' + str(k))
                    c.openHours[0] += random.triangular(-0.5 * time.HOUR, 0.5 * time.HOUR, 0)
                elif p < pWork + pPark:
                    c = place_parser.readPlace('places.ini', 'outdoor')
                else:
                    c = place_parser.readPlace('places.ini', 'home')
            theGrid.addPlace(place.Place(i, j, "", c))
    theGrid.getDistanceMap().calcDistances()
    return theGrid
