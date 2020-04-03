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

def simulateContact(personsAtPlace, thePerson, thePlace, tickLength):
	prob = thePlace.char.contactFrequency * tickLength * thePerson.socialBehaviour
	 

def getInfectionProb(infectedPerson, thePlace):
	return infectedPerson.sickness.contLevel*(1-math.tanh(thePlace.char.contactDistance/infectedPerson.sickness.contRadius))




