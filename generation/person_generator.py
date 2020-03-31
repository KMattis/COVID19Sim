import random
from model import person, grid, place_characteristics, needs, sickness
from generation import need_parser, sickness_parser

def generate(grid, numPersons, needTypes):
    updateFunc, contProbFunc = sickness_parser.parseSickness('simconfig/sickness.ini', 'default')
    persons = []
    for i in range(numPersons):
        thePerson = person.Person(str(i), random.randrange(0, 100), grid.get(0,0), needs.Needs(needTypes), sickness.Sickness(updateFunc, contProbFunc))
        persons.append(thePerson)

    return persons
