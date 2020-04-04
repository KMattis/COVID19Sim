from simulation import time

def defaultUpdate(disease, now):
    infTime = time.Timestamp(now.now()-disease.infectionStarted).day()
    if 3 <= infTime < 12:
        disease.contLevel = 0.5
        disease.contRadius = 1
        disease.healthDamage = 50
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

