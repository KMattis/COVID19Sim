from simconfig import sickness_updates, sickness_probs

class Sickness:
    def __init__(self, updateName, contProbName, isInfected=False, contagiousLev=0, contagiousRadius=0, infectionStarted=0, healthDamage=0, nownow=0):
        self.contLevel = contagiousLev #In ~ prop/minute *100; specifics depend on contPropFunction
        self.contRadius = contagiousRadius #In meters
        self.infectionStarted = infectionStarted #0=no infection
        #damage done to infected person 0-100 (100 =dead)Maybe switch to continous damage "to" the person class?
        self.healthDamage = healthDamage
        self.updateFunction = getattr(sickness_updates, updateName)
        self.contProbFunction = getattr(sickness_probs, contProbName) 
        self.lastUpdate = nownow
        self.isInfected = isInfected

    def update(self, now):
        if self.infectionStarted > 0 and self.isInfected:
            self.updateFunction(self, now) 
            self.lastUpdate = now.now()
        self.lastUpdate = now.now()

    #exposureTime in minutes
    def contPropName(self, dist, exposureTime):
        return self.contProbFunction(self, dist, exposureTime)

