import random
from model import person, grid, place_characteristics, needs, sickness
from generation import need_parser, sickness_parser

def generate(grid, numPersons, needTypes):
    homes = [thePlace for thePlace in grid.internal_grid
            if thePlace is not None
            and thePlace.char.placeType is place_characteristics.PlaceType.HOME]
    updateFunc, contProbFunc = sickness_parser.parseSickness('simconfig/sickness.ini', 'default')
        
    persons = []
    for i in range(numPersons):
        home = random.choice(homes)
        thePerson = person.Person(str(i), random.randrange(0, 100), home, needs.Needs(needTypes), sickness.Sickness(updateFunc, contProbFunc))
        persons.append(thePerson)

    return persons
