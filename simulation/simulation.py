import random

from plotting import logging

from model import place, person, place_characteristics, disease
from simulation import time, math

from profiler.profiler import profilerObj

SIMULATION_TICK_LENGTH = 5 * time.MINUTE

class Simulation:
    def __init__(self, persons):
        self.now = time.Timestamp(time.HOUR * 0)
        self.persons = persons
        self.bobby = persons[0]
        self.lastUpdate = -1

        self.bobby.disease.infect(time.Timestamp(-3 * time.DAY))

        for thePerson in self.persons:
            self.plan(thePerson)

    def simulate(self):
        self.now.minute += SIMULATION_TICK_LENGTH

        self.lastUpdate = self.now.minute

        logging.write("bobby", self.now.now(), self.bobby.task.activity.getName())

        bobby_needs = { "TRAVEL": 1 if self.bobby.isTravelling() else 0 }
        persons_at_place = { "TRAVEL": 0 }
        for needType in self.bobby.needs:
            persons_at_place[needType] = 0
            bobby_needs[needType] = self.bobby.needs[needType]

        logging.write("bobby_needs", self.now.minute, *(bobby_needs.values()))


        place_map = {}
        for thePerson in self.persons:
            if thePerson.isTravelling():
                persons_at_place["TRAVEL"] += 1
                if self.now.now() > thePerson.travelEnd.now():
                    thePerson.currentPosition = thePerson.currentDestination
            else:
                appendPlaceMap(place_map, thePerson)
                persons_at_place[thePerson.task.activity] += 1

            thePerson.disease.update(self.now)

            if self.now.now() < thePerson.task.stop:
                continue

            
            thePerson.behaviour.updateNeeds(thePerson)
            self.plan(thePerson)

        for thePlace in filter(lambda thePlace: place_map[thePlace][1] > 0, place_map):
            for thePerson in place_map[thePlace][0]:
                disease.simulateContact(self.now, place_map[thePlace][0], thePerson, thePlace, SIMULATION_TICK_LENGTH)

        numInfected = sum(1 if p.disease.isInfected else 0 for p in self.persons)
        numContagious = sum(1 if p.disease.isContagious() else 0 for p in self.persons)
        numImmune = sum(1 if p.disease.isImmune else 0 for p in self.persons)
        print(numInfected, numContagious, numImmune)
        logging.write("disease", self.now.minute, numInfected, numContagious, numImmune)
        logging.write("activity", self.now.minute, *(persons_at_place.values()))

    #Plan the schedule of a person
    def plan(self, person):
        for need in person.behaviour.getNeedPrio(person):
            task = need.trySatisfy(person, person.needs[need], self.now)
            if task is not None:
                person.plan(task)
                return

def appendPlaceMap(place_map, thePerson) -> None: 
    thePlace = thePerson.task.place
    if not thePlace in place_map:
        place_map[thePlace] = [[thePerson], 1 if thePerson.disease.isContagious() else 0] 
        return
    if thePerson.disease.isContagious():
        place_map[thePlace][1] += 1
    place_map[thePerson.task.place][0].append(thePerson)

