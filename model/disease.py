import math 

from simulation import random
from plotting import logging

class ContactProperties:
    def __init__(self, contactDistance, contactFrequency):
        self.contactDistance = contactDistance
        self.contactFrequency = contactFrequency

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

def simulateContact(now, diseaseType, personsAtPlace, thePerson, contactProp, placeName, tickLength):
    if thePerson.diseases[diseaseType].isInfected or thePerson.diseases[diseaseType].isImmune:
        return
    contactProb = contactProp.contactFrequency * tickLength * thePerson.socialBehaviour
    if random.random() <= contactProb:
        #Contact
        otherPerson = random.choice(personsAtPlace)
        if otherPerson.diseases[diseaseType].isContagious():
            logging.write("contacts", now.now(), diseaseType.getName(), placeName,
                        thePerson.name, thePerson.task.activity.getName(),
                        otherPerson.name, otherPerson.task.activity.getName())
            infectionProb = getInfectionProb(diseaseType, otherPerson, contactProp)
            if random.random() <= infectionProb:
                thePerson.diseases[diseaseType].infect(now)
                logging.write("infections", now.now(), diseaseType.getName(), placeName,
                        thePerson.name, thePerson.task.activity.getName(),
                        otherPerson.name, otherPerson.task.activity.getName())

def getInfectionProb(diseaseType, contagiousPerson, contactProp):
    return contagiousPerson.diseases[diseaseType].contLevel * \
            max(0,1 - 0.5 * random.triangular(0, contactProp.contactDistance*2, contactProp.contactDistance)/contagiousPerson.diseases[diseaseType].contRadius)

