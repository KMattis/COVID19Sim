import enum
import math
import random

from simulation import time
from model import schedule, need_type, place, disease, person_behaviour

MINUTES_PER_CELL = 0.5

class Person:
    def __init__(self,
            name: str,
            age: int,
            startingPlace: place.Place,
            needTypes: [need_type.NeedType],
            disease: disease.Sickness,
            behaviour: person_behaviour.PersonBehaviour,
            socialBehaviour: float):
        self.name: str = name
        self.age: int = age

        self.currentPosition: place.Place = startingPlace
        self.currentDestination:place.Place = startingPlace

        self.direction: [int] = [0, 0]

        self.travelStart: time.Timestamp = time.Timestamp(-1)
        self.travelEnd: time.Timestamp = time.Timestamp(0)
        self.schedule: schedule.Schedule = schedule.Schedule()

        self.needs = {}
        for needType in needTypes:
            self.needs[needType] = random.uniform(0, 1)
    
        self.disease: disease.Sickness = disease

        self.behaviour: person_behaviour.PersonBehaviour = behaviour
        self.socialBehaviour: float = socialBehaviour

        self.friends = set()
        self.friends0 = set()

    def setDestination(self, dest: place.Place, now: time.Timestamp) -> None:
        self.travelStart.set(now.now())
        distance = math.sqrt((self.currentPosition.x - dest.x)**2 + (self.currentPosition.y - dest.y)**2)
        self.travelEnd.set(round(now.now() + distance * MINUTES_PER_CELL * random.uniform(0.9, 1.1) * time.MINUTE))
        self.currentDestination = dest
        divisor = max(1,(self.travelEnd.now() - self.travelStart.now()))
        self.direction = [(self.currentDestination.x - self.currentPosition.x) / divisor, (self.currentDestination.y - self.currentPosition.y) / divisor]

    def isTravelling(self) -> bool:
        return self.currentDestination != self.currentPosition

    def computeFriends(self):
        self.friends.update(self.friends0)
        for p in self.friends0:
            self.friends.update(p.friends)

def makeFriends(personA, personB):
    personA.friends0.add(personB)
    personB.friends0.add(personA)

