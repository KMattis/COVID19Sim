import random
from model import person, grid, place_characteristics, sickness
from generation import script_loader, sickness_parser

def generate(grid, numPersons, needTypes):
    updateFunc, contProbFunc = sickness_parser.parseSickness('simconfig/sickness.ini', 'default')
    persons = []
    behaviours = script_loader.readObjectsFromScript(configFile="simconfig/person_script.py", name="behaviours")
    behaviourFreqs = [b.getFrequency() for b in behaviours]

    for behaviour in behaviours:
        behaviour.initialize(needTypes)

    for i in range(numPersons):
        behaviour = random.choices(behaviours, behaviourFreqs)[0]
        thePerson = person.Person(str(i), random.randrange(0, 100), grid.get(0,0), needTypes, sickness.Sickness(updateFunc, contProbFunc), behaviour)
        persons.append(thePerson)

    return persons
