import random

from plotting import logging

from model import place, person, place_characteristics
from simulation import time, math

from profiler.profiler import profilerObj

from simconfig import need_priority

SIMULATION_TICK_LENGTH = 5 * time.MINUTE

class Simulation:
    def __init__(self, persons, getNeedPrio, updateNeeds):
        self.now = time.Timestamp(time.HOUR * 0)
        self.persons = persons
        self.lastUpdate = -1
        self.getNeedPrio = getNeedPrio
        self.updateNeeds = updateNeeds

        for thePerson in self.persons:
            self.plan(thePerson)

    def simulate(self):
        self.now.minute += SIMULATION_TICK_LENGTH

        self.lastUpdate = self.now.minute

        logging.write("bobby", self.now.now(), self.persons[0].schedule.task.activity.getName())

        persons_at_place = { "TRAVEL": 0 }
        for needType in self.persons[0].needs:
            persons_at_place[needType] = 0

        place_map = {}
        for thePerson in self.persons:
            if thePerson.isTravelling():
                persons_at_place["TRAVEL"] += 1
                if self.now.now() > thePerson.travelEnd.now():
                    thePerson.currentPosition = thePerson.currentDestination
            else:
                appendPlaceMap(place_map, thePerson)
                persons_at_place[thePerson.schedule.task.activity] += 1


            if self.now.now() < thePerson.schedule.task.stop:
                continue

            thePerson.sickness.update(self.now)
            
            self.updateNeeds(thePerson)
            self.plan(thePerson)

        for pl in filter(lambda pl: place_map[pl][1] > 0, place_map):
            #Determine infection risk at pl
            #...
            for thePerson in place_map[pl][0]:
                pWorker, pVisitor = pl.getInfectionRisks( )
                #Infect with prob. as calculated above

        logging.write("activity", self.now.minute, *(persons_at_place.values()))

    #Plan the schedule of a person
    def plan(self, person):
        for need in self.getNeedPrio(person):
            exists, openPlace, dur = need.trySatisfy(person, person.needs[need], self.now)
            if exists:
                person.schedule.plan(openPlace, self.now.now(), self.now.now()+dur, need)
                person.setDestination(person.schedule.task.place, self.now)
                return

def appendPlaceMap(place_map, thePerson) -> None: 
    thePlace = thePerson.schedule.task.place
    if not thePlace in place_map:
        place_map[thePlace] = [[thePerson], 1 if thePerson.sickness.isContagious() else 0] 
        return
    if thePerson.sickness.isInfected:
        place_map[thePlace][1] += 1
    place_map[thePerson.schedule.task.place][0].append(thePerson)

