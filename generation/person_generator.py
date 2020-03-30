import random
from model import person, grid, place, needs, sickness
from generation import need_parser, sickness_parser

def generate(grid, numPersons):
    homes = [thePlace for thePlace in grid.internal_grid
            if thePlace is not None
            and thePlace.char.placeType is place.PlaceType.HOME]
    workplaces = [thePlace for thePlace in grid.internal_grid
            if thePlace is not None
            and (thePlace.char.placeType is place.PlaceType.WORK)]
        
    eat, sleep, work, outdoor = need_parser.readNeeds('simconfig/needs.ini', 'default')
    updateFunc, contProbFunc = sickness_parser.parseSickness('simconfig/sickness.ini', 'default')
        
    persons = []
    for i in range(numPersons):
        home = random.choice(homes)
        workplace = random.choice(workplaces)
        thePerson = person.Person(str(i), random.randrange(0, 100), home,workplace, needs.Needs(eat, sleep, work, outdoor), sickness.Sickness(updateFunc, contProbFunc))
        persons.append(thePerson)

    return persons
