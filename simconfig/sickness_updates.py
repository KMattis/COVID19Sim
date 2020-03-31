from simulation import time

def defaultUpdate(sickness, now):
    infTime = time.Timestamp(now.now()-sickness.infectionStarted).day()
    sickness.isInfected = True
    if 0 < infTime < 2:
        sickness.contLevel = 40
        sickness.contRadius = 0.5
        sickness.healthDamage = 0
    elif 2 <= infTime < 5:
        sickness.contLevel = 80
        sickness.contRadius = 1
        sickness.healthDamage = 20
    elif 5 <= infTime < 7:
        sickness.contLevel = 100
        sickness.contRadius = 1
        sickness.healthDamage = 50
    elif 7 <= infTime < 10:
        sickness.contLevel = 40
        sickness.contRadius = 0.5
        sickness.healthDamage = 20
    else:
        sickness.contLevel = 0
        sickness.contRadius = 0
        sickness.healthDamage = 0
        sickness.isInfected = False

