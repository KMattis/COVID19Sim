import enum
import math
import random

from simulation import time
from model import schedule, needs, place, needs, sickness

MINUTES_PER_CELL = 0.5

class Person:
    def __init__(self, name: str, age: int, home: place.Place, needs: needs.Needs, sickness: sickness.Sickness):
        self.name: str = name
        self.age: int = age

        self.currentPosition: place.Place = home
        self.currentDestination:place.Place = home

        self.direction: [int] = [0, 0]

        self.travelStart: time.Timestamp = time.Timestamp(-1)
        self.travelEnd: time.Timestamp = time.Timestamp(0)
        self.schedule: schedule.Schedule = schedule.Schedule()

        self.needs: needs.Needs = needs
    
        self.sickness: sickness.Sickness = sickness

    def setDestination(self, dest: place.Place, now: time.Timestamp) -> None:
        self.travelStart.set(now.now())
        distance = math.sqrt((self.currentPosition.x - dest.x)**2 + (self.currentPosition.y - dest.y)**2)
        self.travelEnd.set(round(now.now() + distance * MINUTES_PER_CELL * random.uniform(0.9, 1.1) * time.MINUTE))
        self.currentDestination = dest
        divisor = max(1,(self.travelEnd.now() - self.travelStart.now()))
        self.direction = [(self.currentDestination.x - self.currentPosition.x) / divisor, (self.currentDestination.y - self.currentPosition.y) / divisor]
    
    def getXY(self, now: time.Timestamp) -> (int, int):
        if self.isTravelling():        
            progress = min(now.now() - self.travelStart.now(), self.travelEnd.now() - self.travelStart.now())
            return self.currentPosition.x + self.direction[0] * progress, self.currentPosition.y + self.direction[1] * progress
        else:
            return self.currentPosition.x, self.currentPosition.y

    def isTravelling(self) -> bool:
        return self.currentDestination != self.currentPosition
