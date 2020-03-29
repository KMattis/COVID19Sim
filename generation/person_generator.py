import random

from model import person, grid, place

def generate(grid, numPersons):
    homes = [thePlace for thePlace in grid.internal_grid
            if thePlace is not None
            and thePlace.char.placeType is place.PlaceType.HOME]
    workplaces = [thePlace for thePlace in grid.internal_grid
            if thePlace is not None
            and (thePlace.char.placeType is place.PlaceType.WORK)]
    
    persons = []
    for i in range(numPersons):
        home = random.choice(homes)
        workplace = random.choice(workplaces)
        thePerson = person.Person(str(i), random.randrange(0, 100), home,workplace)
        persons.append(thePerson)

    return persons
