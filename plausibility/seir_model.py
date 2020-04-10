

def calculateSEIRParameters():
    numContacts = fileLen("logfiles/contacts.log")
    numInfections = fileLen("logfiles/infections.log")
    incubationPeriod = 1 * 24
    infectiousPeriod = 3 * 24
    alpha = calculateAlpha(incubationPeriod)
    beta = calculateBeta(numInfections, numContacts)
    gamma = calulcateGamma(infectiousPeriod)
    print("Alpha", alpha, "Beta", beta, "Gamma", gamma)


def fileLen(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def calculateAlpha(incubationPeriod):
    return 1 / incubationPeriod

def calculateBeta(numInfections, numContacts):
    return numInfections / numContacts

def calulcateGamma(infectiousPeriod):
    return 1 / infectiousPeriod

if __name__ == "__main__":
    calculateSEIRParameters()