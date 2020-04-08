import random as r
import time

def setSeed(seed_value=None):
    if seed_value is None:
        seedValue=time.time()
    else:
        seedValue=seed_value
    r.seed(seedValue)
    return 0



def randint(a, b):
    return r.randint(a, b)

def choices(a, b):
    return r.choices(a, b)

def random():
    return r.random()

def randrange(a, b):
    return r.randrange(a, b)

def choice(a):
    return r.choice(a)

def triangular(a, b, c):
    return r.triangular(a, b, c)
    
def uniform(a, b):
    return r.uniform(a, b)

def gauss(a, b):
    return r.gauss(a, b)