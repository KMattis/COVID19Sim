from simulation import time

def defaultContProb(disease, dist, exposureTime):
    if (disease.contRadius > dist):
        return 0
    dDist = disease.contRadius - dist
    if dDist >= disease.contRadius:
        return exposureTime*disease.contagiousLev
    return 2*exposureTime*disease.contagiousLev

