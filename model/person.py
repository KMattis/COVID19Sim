import enum
import math
import random

from simulation import time
from model import schedule

MINUTES_PER_CELL = 0.5

class Person:
    def __init__(self, name, age, home, workplace):
        self.name = name
        self.age = age
        self.home = home
        self.workplace = workplace
        self.currentPosition = home
        self.currentDestination = home
        self.direction = [0, 0]
        self.travelStart = time.Timestamp(0)
        self.travelEnd = time.Timestamp(random.randrange(time.HOUR * 8, time.HOUR * 10))
        self.schedule = schedule.Schedule(home)

    def setDestination(self, dest, now):
        self.travelStart.set(now.now())
        distance = math.sqrt((self.currentPosition.x - dest.x)**2 + (self.currentPosition.y - dest.y)**2)
        self.travelEnd.set(now.now() + distance * MINUTES_PER_CELL * random.uniform(0.9, 1.1) * time.MINUTE)
        self.currentDestination = dest
        self.direction = [self.currentDestination.x - self.currentPosition.x, self.currentDestination.y - self.currentPosition.y]
    
    def getXY(self, now: time.Timestamp):
        if self.isTraveling():        
            progress = min(1, (now.now() - self.travelStart.now()) / (self.travelEnd.now() - self.travelStart.now()))
            return self.currentPosition.x + self.direction[0] * progress, self.currentPosition.y + self.direction[1] * progress
        else:
            return self.currentPosition.x, self.currentPosition.y

    def isTraveling(self):
        return self.currentDestination != self.currentPosition