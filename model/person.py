import enum
import math
import random

from simulation import time

MINUTES_PER_CELL = 0.5

class Person:
    def __init__(self, name, age, home, workplace):
        self.name = name
        self.age = age
        self.home = home
        self.workplace = workplace
        self.currentPosition = home
        self.currentDestination = home
        self.lastAction = time.Timestamp(0)
        self.nextAction = time.Timestamp(random.randrange(time.HOUR * 8, time.HOUR * 10))

    def setDestination(self, dest, now):
        self.lastAction.set(now.now())
        if dest == self.currentPosition:
            if dest == self.home:
                self.nextAction.set(now.today() + time.DAY + random.randrange(time.HOUR * 8, time.HOUR * 10))
            else:
                self.nextAction.set(now.now() + time.HOUR * 7 + time.MINUTE * 30 + random.randrange(0, time.HOUR))
        else:
            distance = math.sqrt((self.currentPosition.x - dest.x)**2 + (self.currentPosition.y - dest.y)**2)
            self.nextAction.set(now.now() + distance * MINUTES_PER_CELL * random.uniform(0.9, 1.1) * time.MINUTE)

        self.currentDestination = dest
    
    def getXY(self, now: time.Timestamp):
        progress = min(1, (now.now() - self.lastAction.now()) / (self.nextAction.now() - self.lastAction.now()))
        return (self.currentPosition.x + (self.currentDestination.x - self.currentPosition.x) * progress,
            self.currentPosition.y + (self.currentDestination.y - self.currentPosition.y) * progress)

    def update(self, now):
        if now.now() < self.nextAction.now():
            return

        if self.currentPosition == self.currentDestination:
            if self.currentPosition == self.home:
                self.setDestination(self.workplace, now)
            else:
                self.setDestination(self.home, now)
        else:
            self.currentPosition = self.currentDestination
            self.setDestination(self.currentDestination, now)


