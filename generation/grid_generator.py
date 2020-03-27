import random

from model import grid, place

def generate(size):
    theGrid = grid.Grid(size)
    numGridPoints = size * size
    
    population = []
    for i in range(int(numGridPoints * 0.5)):
        population.append(place.PlaceCharacteristics(place.PlaceType.HOME))
    for i in range(int(numGridPoints * 0.1)):
        population.append(place.PlaceCharacteristics(place.PlaceType.SERVICE))
    for i in range(int(numGridPoints * 0.1)):
        population.append(place.PlaceCharacteristics(place.PlaceType.NONSERVICE))
    for i in range(int(numGridPoints * 0.3)):
        population.append(place.PlaceCharacteristics(place.PlaceType.OUTDOOR))

    random.shuffle(population)

    for i in range(size):
        for j in range(size):
            thePlace = place.Place(i, j, "Place", population[i + j * size])
            theGrid.addPlace(thePlace)  

    return theGrid

