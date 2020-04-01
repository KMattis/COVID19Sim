from model import person
from simulation import time

sleep = None
work = None
eat = None

def initialize(needTypes):
    global sleep, work, eat
    sleep = [k for k in needTypes if k.getName() == "SLEEP"][0]
    work = [k for k in needTypes if k.getName() == "WORK"][0]
    eat = [k for k in needTypes if k.getName() == "EAT"][0]

def getNeedPrio(thePerson):
    sortedNeeds = sorted([k for k in thePerson.needs.needs.keys() if thePerson.needs.needs[k] > 0.5],
            key=lambda k: thePerson.needs.needs[k], reverse=True)
    sortedNeeds.append(sleep)
    return sortedNeeds

def updateNeeds(thePerson):
    currentPlace = thePerson.schedule.task.place
    duration = thePerson.schedule.task.getDuration()
    workplace = work.workplaces[thePerson]
    
    for need in currentPlace.char.needTypes:
        if thePerson.schedule.task.activity == eat and need == work:
            continue
        #thePerson.needs.needs[need] = 0
        thePerson.needs.needs[need] -= (duration / time.HOUR)

    for needType in thePerson.needs.needs:
        if needType in currentPlace.char.needTypes:
            continue

        thePerson.needs.needs[needType] = thePerson.needs.needs[needType] + thePerson.needs.deltas[needType] * duration

