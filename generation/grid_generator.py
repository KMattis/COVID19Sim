import math
import random

from model import grid, place

def generate(size):
    theGrid = grid.Grid(size)
    
    centerx = size / 2
    centery = size / 2
    for i in range(size):
        for j in range(size):
            radius2 = (i - centerx)**2 + (j - centery)**2
            if radius2 > size**2 / 4:
                t = place.PlaceType.NONE
            else: 
                maxRadius = size / 2
                pService = ((maxRadius - math.sqrt(radius2)) / maxRadius) * 0.5
                pPark = 0.1
                pNonService = 0.15
                
                p = random.random()

                if p < pService:
                    t = place.PlaceType.SERVICE
                elif p < pService + pPark:
                    t = place.PlaceType.OUTDOOR
                elif p < pService + pPark + pNonService:
                    t = place.PlaceType.NONSERVICE
                else:
                    t = place.PlaceType.HOME

            theGrid.addPlace(place.Place(i, j, "", place.PlaceCharacteristics(t)))

    return theGrid

