import enum
import math
import random

MINUTES_PER_CELL = 0.5

class Person:
    def __init__(self, name, age, home, workplace):
        self.name = name
        self.age = age
        self.home = home
        self.workplace = workplace
        self.currentPosition = home
        self.currentDestination = home
        self.lastAction = -60
        self.nextAction = random.randrange(0, 120)

    def setDestination(self, dest, now):
        self.lastAction = now
        today = (now // (24 * 60)) * 24 * 60
        if dest == self.currentPosition:
            if dest == self.home:
                self.nextAction = today + 24 * 60 + random.randrange(0, 120)
            else:
                self.nextAction = now + 7 * 60 + random.randrange(0, 60)
        else:
            distance = math.sqrt((self.currentPosition.x - dest.x)**2 + (self.currentPosition.y - dest.y)**2)
            self.nextAction = now + distance * MINUTES_PER_CELL * random.uniform(0.9, 1.1)

        self.currentDestination = dest
    
    def getXY(self, now):
        progress = (now - self.lastAction) / (self.nextAction - self.lastAction)
        return (self.currentPosition.x + (self.currentDestination.x - self.currentPosition.x) * progress,
            self.currentPosition.y + (self.currentDestination.y - self.currentPosition.y) * progress)

    def update(self, now):
        if now < self.nextAction:
            return

        if self.currentPosition == self.currentDestination:
            if self.currentPosition == self.home:
                self.setDestination(self.workplace, now)
            else:
                self.setDestination(self.home, now)
        else:
            self.currentPosition = self.currentDestination
            self.setDestination(self.currentDestination, now)


