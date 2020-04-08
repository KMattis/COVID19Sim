import math 

import randomfile
from plotting import logging

class Disease:
    def __init__(self, diseaseType, isInfected=False, contagiousLev=0, contagiousRadius=0, infectionStarted=-1, healthDamage=0, isImmune=False):
        self.diseaseType = diseaseType

        self.contLevel = contagiousLev #In ~ prop/minute *100; specifics depend on contPropFunction
        self.contRadius = contagiousRadius #In meters
        self.infectionStarted = infectionStarted #-1=no infection

        self.healthDamage = healthDamage
        self.isInfected = isInfected
        self.isImmune = isImmune

    def isContagious(self):
        return self.isInfected and self.contRadius > 0

    def infect(self, now):
        if not self.isImmune and not self.isInfected:
            self.isInfected = True
            self.infectionStarted = now.now()

def simulateContact(now, diseaseType, personsAtPlace, thePerson, thePlace, tickLength):
    if thePerson.diseases[diseaseType].isInfected or thePerson.diseases[diseaseType].isImmune:
        return
    contactProb = thePlace.char.contactFrequency * tickLength * thePerson.socialBehaviour
    if randomfile.randomrandom() <= contactProb:
        #Contact
        otherPerson = randomfile.randomchoice(personsAtPlace)
        if otherPerson.diseases[diseaseType].isContagious():
            infectionProb = getInfectionProb(diseaseType, otherPerson, thePlace)
            if randomfile.randomrandom() <= infectionProb:
                thePerson.diseases[diseaseType].infect(now)
                logging.write("infections", now.now(), diseaseType.getName(), str(thePlace.char.subType),
                        thePerson.name, thePerson.task.activity.getName(),
                        otherPerson.name, otherPerson.task.activity.getName())

def getInfectionProb(diseaseType, contagiousPerson, thePlace):
    return contagiousPerson.diseases[diseaseType].contLevel * \
            max(0,1 - 0.5 * randomfile.randomtriangular(0, thePlace.char.contactDistance*2, thePlace.char.contactDistance)/contagiousPerson.diseases[diseaseType].contRadius)

