from model import person
from simulation import time
from model import person_behaviour

class DefaultBehaviour(person_behaviour.PersonBehaviour):
    def __init__(self):
        self.sleep = None
        self.work = None
        self.eat = None
        self.outdoor = None
        self.social = None
        self.health = None

        self.needUpdateDict = None
        self.needCaps = None

    def initialize(self, needTypes):
        self.sleep = [k for k in needTypes if k.getName() == "SLEEP"][0]
        self.work = [k for k in needTypes if k.getName() == "WORK"][0]
        self.eat = [k for k in needTypes if k.getName() == "EAT"][0]
        self.outdoor = [k for k in needTypes if k.getName() == "OUTDOOR"][0]
        self.social = [k for k in needTypes if k.getName() == "SOCIAL"][0]
        self.health = [k for k in needTypes if k.getName() == "HEALTH"][0]

        self.needUpdateDict = {
            self.sleep : {
                self.sleep : -1,
                self.work : +2,
                self.eat : +0.2,
                self.outdoor : +0.5,
                self.social : +0.5,
                self.health : 0,
            },
            self.work : {
                self.sleep : +0.5,
                self.work : -1,
                self.eat : +2,
                self.outdoor : +0.5,
                self.social : +0.5,
                self.health : 0,
            },
            self.eat : {
                self.sleep : +0.5,
                self.work : 0,
                self.eat : -100,
                self.outdoor : +0.5,
                self.social : +0.5,
                self.health : 0,
            },
            self.outdoor : {
                self.sleep : +2,
                self.work : +1,
                self.eat : +1,
                self.outdoor : -1,
                self.social : +0.5,
                self.health : 0,
            },
            self.social : {
                self.sleep : +0.2,
                self.work : +0.2,
                self.eat : +0.2,
                self.outdoor : +0.5,
                self.social : -100,
                self.health : 0,
            },
            self.health : {
                self.sleep : 0,
                self.work : 0,
                self.eat : 0,
                self.outdoor : 0,
                self.social : 0,
                self.health : -1,
            },
        }

        self.needCaps = {
            self.sleep: 10,
            self.work: 8,
            self.eat: 10,
            self.outdoor: 4,
            self.social: 10,
            self.health: 100,
        }

    def getNeedPrio(self, thePerson):
        sortedNeeds = sorted([k for k in thePerson.needs.keys() if thePerson.needs[k] > 2],
                key=lambda k: thePerson.needs[k], reverse=True)
        sortedNeeds.append(self.sleep)
        return sortedNeeds

    def updateNeeds(self, thePerson):
        duration = thePerson.task.getDuration()

        for need in thePerson.needs:
            thePerson.needs[need] += (duration / time.HOUR) * self.needUpdateDict[thePerson.task.activity][need]
            thePerson.needs[need] = max(0, thePerson.needs[need])
            thePerson.needs[need] = min(self.needCaps[need], thePerson.needs[need])

    def getFrequency(self):
        return 1

