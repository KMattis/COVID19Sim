import random
import time

def setseed(seed_value=None):
    global seedvalue
    if seed_value is None:
        seedvalue=time.time()
    else:
        seedvalue=seed_value
    random.seed(seedvalue)
    return 0



def randomint(a, b):
    return random.randint(a, b)

def randomchoices(a, b):
    return random.choices(a, b)

def randomrandom():
    return random.random()

def randomrange(a, b):
    return random.randrange(a, b)

def randomchoice(a):
    return random.choice(a)

def randomtriangular(a, b, c):
    random.triangular(a, b, c)
    
def randomuniform(a, b):
    return random.uniform(a, b)

def randomgauss(a, b):
    return random.gauss(a, b)