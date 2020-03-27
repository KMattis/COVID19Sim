import enum

import random

class Person:
    def __init__(self, name, age, home, workplace):
        self.name = name
        self.age = age
        self.home = home
        self.workplace = workplace
        self.currentPosition = home
        self.currentDestination = home
        self.progress = 1.0
        self.timeLeft = random.randrange(0, 2000)

    def setDestination(self, dest):
        self.currentDestination = dest
        self.progress = 0.0
    
    def getXY(self):
        return (self.currentPosition.x + (self.currentDestination.x - self.currentPosition.x) * self.progress,
            self.currentPosition.y + (self.currentDestination.y - self.currentPosition.y) * self.progress)

    def update(self, delta):
        if self.currentPosition != self.currentDestination:
            self.progress += delta / 5000
            if self.progress >= 1.0:
                self.progress = 1.0
                self.currentPosition = self.currentDestination
        else:
            self.timeLeft -= delta
            if self.timeLeft < 0:
                if self.currentPosition == self.workplace:
                    self.setDestination(self.home)
                    self.timeLeft = random.randrange(14000, 16000)
                elif self.currentPosition == self.home:
                    self.setDestination(self.workplace)
                    self.timeLeft = random.randrange(7000, 9000)
