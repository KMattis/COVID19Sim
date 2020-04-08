import enum
import math


from typing import Dict

from simulation import random
from simulation import time
from model import schedule, need_type, place, disease_type, disease, person_behaviour

MINUTES_PER_CELL = 0.5

class Person:
    def __init__(self,
            name: str,
            age: int,
            startingPlace: place.Place,
            needTypes: [need_type.NeedType],
            diseaseTypes: [disease_type.DiseaseType],
            behaviour: person_behaviour.PersonBehaviour,
            socialBehaviour: float):
        self.name: str = name
        self.age: int = age

        self.travelData = None

        self.currentPosition: place.Place = startingPlace
        self.currentDestination:place.Place = startingPlace

        self.task: schedule.ScheduleItem = None

        self.needs: Dict[need_type.NeedType, float] = {}
        for needType in needTypes:
            self.needs[needType] = random.uniform(0, 1)
    
        self.diseases: Dict[disease_type.DiseaseType, disease.Disease] = {}
        for diseaseType in diseaseTypes:
            self.diseases[diseaseType] = disease.Disease(diseaseType)   

        self.behaviour: person_behaviour.PersonBehaviour = behaviour
        self.socialBehaviour: float = socialBehaviour

        self.friends = set()
        self.friends0 = set()

    def computeFriends(self):
        self.friends.update(self.friends0)
        for p in self.friends0:
            self.friends.update(p.friends)

def makeFriends(personA, personB):
    personA.friends0.add(personB)
    personB.friends0.add(personA)

