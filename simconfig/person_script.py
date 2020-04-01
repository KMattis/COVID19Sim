from model import person
from simulation import time

sleep = None
work = None
eat = None
outdoor = None

needUpdateDict = None
needCaps = None

def initialize(needTypes):
    global sleep, work, eat, outdoor, needUpdateDict, needCaps
    sleep = [k for k in needTypes if k.getName() == "SLEEP"][0]
    work = [k for k in needTypes if k.getName() == "WORK"][0]
    eat = [k for k in needTypes if k.getName() == "EAT"][0]
    outdoor = [k for k in needTypes if k.getName() == "OUTDOOR"][0]

    needUpdateDict = {
        sleep : {
            sleep : -1,
            work : +2,
            eat : 0,
            outdoor : +0.5
        },
        work : {
            sleep : +2,
            work : -1,
            eat : +3,
            outdoor : +0.5
        },
        eat : {
            sleep : +2,
            work : 0,
            eat : -1,
            outdoor : +0.5
        },
        outdoor : {
            sleep : +2,
            work : +1,
            eat : +1,
            outdoor : -1
        }
    }

    needCaps = {
        sleep: 10,
        work: 8,
        eat: 4,
        outdoor: 4
    }

def getNeedPrio(thePerson):
    sortedNeeds = sorted([k for k in thePerson.needs.keys() if thePerson.needs[k] > needCaps[k] / 2],
            key=lambda k: thePerson.needs[k], reverse=True)
    sortedNeeds.append(sleep)
    return sortedNeeds

def updateNeeds(thePerson):
    duration = thePerson.schedule.task.getDuration()

    for need in thePerson.needs:
        thePerson.needs[need] += min(needCaps[need], (duration / time.HOUR) * needUpdateDict[thePerson.schedule.task.activity][need])
