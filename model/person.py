import enum
import math
import random

from simulation import time
from model import schedule, need_type, place, sickness, person_behaviour

MINUTES_PER_CELL = 0.5

class Person:
    def __init__(self,
            name: str,
            age: int,
            startingPlace: place.Place,
            needTypes: [need_type.NeedType],
            sickness: sickness.Sickness,
            behaviour: person_behaviour.PersonBehaviour,
            socialBehaviour: float):
        self.name: str = name
        self.age: int = age

        self.currentPosition: place.Place = startingPlace
        self.currentDestination:place.Place = startingPlace

        self.direction: [int] = [0, 0]

        self.travelStart: time.Timestamp = time.Timestamp(-1)
        self.travelEnd: time.Timestamp = time.Timestamp(0)
        self.task: schedule.ScheduleItem = None

        self.needs = {}
        for needType in needTypes:
            self.needs[needType] = random.uniform(0, 1)
    
        self.sickness: sickness.Sickness = sickness

        self.behaviour: person_behaviour.PersonBehaviour = behaviour
        self.socialBehaviour: float = socialBehaviour

        self.friends = set()
        self.friends0 = set()

    def setDestination(self, dest: place.Place, start: int) -> None:
        self.travelStart.set(start)
        distance = math.sqrt((self.currentPosition.x - dest.x)**2 + (self.currentPosition.y - dest.y)**2)
        self.travelEnd.set(round(start + distance * MINUTES_PER_CELL * random.uniform(0.9, 1.1) * time.MINUTE))
        self.currentDestination = dest
        divisor = max(1,(self.travelEnd.now() - self.travelStart.now()))
        self.direction = [(self.currentDestination.x - self.currentPosition.x) / divisor, (self.currentDestination.y - self.currentPosition.y) / divisor]

    def plan(self, task: schedule.ScheduleItem) -> None:
        if self.task is not None and task.start < self.task.stop:
            raise Exception("Events must be added in ascending order {0},{1},{2}".format(task.place.char.placeType, task.start, task.stop)) 
        self.task = task
        self.setDestination(task.place, task.start)

    def isTravelling(self) -> bool:
        return self.currentDestination != self.currentPosition

    def computeFriends(self):
        self.friends.update(self.friends0)
        for p in self.friends0:
            self.friends.update(p.friends)

def makeFriends(personA, personB):
    personA.friends0.add(personB)
    personB.friends0.add(personA)

