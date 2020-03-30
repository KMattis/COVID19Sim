from simulation import time

def defaultContProb(sickness, dist, exposureTime):
    if (sickness.contRadius > dist):
        return 0
    dDist = sickness.contRadius - dist
    if dDist >= sickness.contRadius:
        return exposureTime*sickness.contagiousLev
    return 2*exposureTime*sickness.contagiousLev
