import math, random

from simconfig import sickness_updates, sickness_probs

class Sickness:
    def __init__(self, updateName, contProbName, isInfected=False, contagiousLev=0, contagiousRadius=0, infectionStarted=-1, healthDamage=0, nownow=0, isImmune=False):
        self.contLevel = contagiousLev #In ~ prop/minute *100; specifics depend on contPropFunction
        self.contRadius = contagiousRadius #In meters
        self.infectionStarted = infectionStarted #0=no infection
        #damage done to infected person 0-100 (100 =dead)Maybe switch to continous damage "to" the person class?
        self.healthDamage = healthDamage
        self.updateFunction = getattr(sickness_updates, updateName)
        self.contProbFunction = getattr(sickness_probs, contProbName) 
        self.lastUpdate = nownow
        self.isInfected = isInfected
        self.isImmune = isImmune

    def update(self, now):
        if self.isInfected:
            self.updateFunction(self, now) 
            self.lastUpdate = now.now()
        self.lastUpdate = now.now()

    #exposureTime in minutes
    def contProbName(self, dist, exposureTime):
        return self.contProbFunction(self, dist, exposureTime)

    def isContagious(self):
        return self.isInfected and self.contRadius > 0

    def infect(self, now):
        if not self.isImmune and not self.isInfected:
            self.isInfected = True
            self.infectionStarted = now.now()

def simulateContact(now, personsAtPlace, thePerson, thePlace, tickLength):
    if thePerson.sickness.isInfected or thePerson.sickness.isImmune:
        return
    contactProb = thePlace.char.contactFrequency * tickLength * thePerson.socialBehaviour
    if random.random() <= contactProb:
        #Contact
        otherPerson = random.choice(personsAtPlace)
        if otherPerson.sickness.isContagious():
            infectionProb = getInfectionProb(otherPerson, thePlace)
            if random.random() <= infectionProb:
                thePerson.sickness.infect(now)

def getInfectionProb(contagiousPerson, thePlace):
    return contagiousPerson.sickness.contLevel*max(0, 1 - 0.5 * random.triangular(0, thePlace.char.contactDistance*2, thePlace.char.contactDistance)/contagiousPerson.sickness.contRadius)




