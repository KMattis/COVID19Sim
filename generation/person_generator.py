import random
from model import person, grid, place_characteristics, disease
from generation import script_loader, disease_parser

def generate(grid, numPersons, needTypes):
    updateFunc, contProbFunc = disease_parser.parseSickness('simconfig/disease.ini', 'default')
    persons = []
    behaviours = script_loader.readObjectsFromScript(configFile="simconfig/person_script.py", name="behaviours")
    behaviourFreqs = [b.getFrequency() for b in behaviours]

    for behaviour in behaviours:
        behaviour.initialize(needTypes)

    for i in range(numPersons):
        behaviour = random.choices(behaviours, behaviourFreqs)[0]
        thePerson = person.Person(str(i),
                random.randrange(0, 100), grid.get(0,0), needTypes,
                disease.Sickness(updateFunc, contProbFunc), behaviour, random.random())
        persons.append(thePerson)
    
    for p in persons:
        for i in range(random.randint(2,5)):
            q = random.choice(persons)
            person.makeFriends(p, q)

    for p in persons:
        p.computeFriends()

    return persons

