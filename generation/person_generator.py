import random

from model import person, grid, place

def generate(grid, numPersons):
    homes = [thePlace for thePlace in grid.internal_grid
            if thePlace is not None
            and thePlace.char.placeType is place.PlaceType.HOME]
    workplaces = [thePlace for thePlace in grid.internal_grid
            if thePlace is not None
            and (thePlace.char.placeType is place.PlaceType.SERVICE
                or thePlace.char.placeType is place.PlaceType.NONSERVICE)]
    
    persons = []
    for i in range(numPersons):
        thePerson = person.Person(str(i), random.randrange(0, 100), random.choice(homes), random.choice(workplaces))
        persons.append(thePerson)

    return persons
