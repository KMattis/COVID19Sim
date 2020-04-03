from simulation import time

def defaultUpdate(sickness, now):
    infTime = time.Timestamp(now.now()-sickness.infectionStarted).day()
    if 3 <= infTime < 12:
        sickness.contLevel = 0.5
        sickness.contRadius = 1
        sickness.healthDamage = 50
    #elif 2 <= infTime < 5:
    #    sickness.contLevel = 0.8
    #    sickness.contRadius = 1
    #    sickness.healthDamage = 20
    #elif 5 <= infTime < 7:
    #    sickness.contLevel = 1
    #    sickness.contRadius = 1.5
    #    sickness.healthDamage = 50
    #elif 7 <= infTime < 10:
    #    sickness.contLevel = 0.4
    #    sickness.contRadius = 0.5
    #    sickness.healthDamage = 20
    elif 12 <= infTime:
        sickness.contLevel = 0
        sickness.contRadius = 0
        sickness.healthDamage = 0
        sickness.isInfected = False
        sickness.isImmune = True

