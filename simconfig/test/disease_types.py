from simulation import time, simulation

import model.disease_type

class COVID19(model.disease_type.DiseaseType):
    def __init__(self):
        self.health = None

    def initialize(self, needTypes):
        self.health = [need for need in needTypes if need.getName() == "HEALTH"][0]
    
    def update(self, now,  person):
        disease = person.diseases[self]
        
        if not disease.isInfected:
            return

        infTime = time.Timestamp(now.now()-disease.infectionStarted).day()

        if 0 <= infTime < 12:
            disease.contLevel = 0.8
            disease.contRadius = 1
            disease.healthDamage = 50
            person.needs[self.health] += (simulation.SIMULATION_TICK_LENGTH / time.HOUR) * 0.1
        #elif 2 <= infTime < 5:
        #    disease.contLevel = 0.8
        #    disease.contRadius = 1
        #    disease.healthDamage = 20
        #elif 5 <= infTime < 7:
        #    disease.contLevel = 1
        #    disease.contRadius = 1.5
        #    disease.healthDamage = 50
        #elif 7 <= infTime < 10:
        #    disease.contLevel = 0.4
        #    disease.contRadius = 0.5
        #    disease.healthDamage = 20
        elif 12 <= infTime:
            disease.contLevel = 0
            disease.contRadius = 0
            disease.healthDamage = 0
            disease.isInfected = False
            disease.isImmune = True

    def getName(self):
        return "COVID-19"

