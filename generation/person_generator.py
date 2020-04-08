import randomfile
from model import person, grid, place_characteristics, disease
from generation import script_loader, disease_parser

def generate(grid, model_data, needTypes, diseaseTypes):
    persons = []
    behaviours = script_loader.readObjectsFromScript(model_data["person_behaviours"], "person_behaviours")
    behaviourFreqs = [b.getFrequency() for b in behaviours]

    for behaviour in behaviours:
        behaviour.initialize(needTypes)

    numPersons = int(model_data["numPersons"])

    for i in range(numPersons):
        behaviour = randomfile.randomchoices(behaviours, behaviourFreqs)[0]
        thePerson = person.Person(str(i),
                randomfile.randomrange(0, 100), grid.get(0,0), needTypes,
                diseaseTypes, behaviour, randomfile.randomrandom())
        persons.append(thePerson)
    persons[0].name = "Bobby"
    
    for p in persons:
        for i in range(randomfile.randomint(2,5)):
            q = randomfile.randomchoice(persons)
            person.makeFriends(p, q)

    for p in persons:
        p.computeFriends()

    return persons

