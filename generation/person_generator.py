import random
from model import person, grid, place_characteristics, disease
from generation import script_loader, disease_parser

def generate(grid, model_data, needTypesDict, diseaseTypes):
    persons = []
    behaviours = script_loader.readObjectsFromScript(model_data["person_behaviours"], "person_behaviours")
    behaviourFreqs = [b.getFrequency() for b in behaviours]

    for behaviour in behaviours:
        behaviour.initialize(needTypesDict)

    numPersons = int(model_data["numPersons"])

    for i in range(numPersons):
        behaviour = random.choices(behaviours, behaviourFreqs)[0]
        thePerson = person.Person(str(i),
                random.randrange(0, 100), grid.get(0,0), needTypesDict.values(),
                diseaseTypes, behaviour, random.random())
        persons.append(thePerson)
    persons[0].name = "Bobby"
    
    for p in persons:
        for i in range(random.randint(2,5)):
            q = random.choice(persons)
            person.makeFriends(p, q)

    for p in persons:
        p.computeFriends()

    return persons

