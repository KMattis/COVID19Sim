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
                c = place_characteristics.PlaceCharacteristics(place.PlaceType.NONE,0,0,0,0,needs.NeedType.NONE)
            else: 
                maxRadius = size / 2
                pService = ((maxRadius - math.sqrt(radius2)) / maxRadius) * 0.5
                pPark = 0.1
                pNonService = 0.15
                
                p = random.random()

                if p < pService:
                    k = random.randrange(0, 2)
                    c = place_parser.readPlace('places.ini', 'service.' + str(k))
                elif p < pService + pPark:
                    c = place_parser.readPlace('places.ini', 'outdoor')
                elif p < pService + pPark + pNonService:
                    c = place_parser.readPlace('places.ini', 'nonservice')
                else:
                    c = place_parser.readPlace('places.ini', 'home')
            theGrid.addPlace(place.Place(i, j, "", c))

    return theGrid
