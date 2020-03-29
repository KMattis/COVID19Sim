import random

from plotting import logging

from model import grid, place, person, needs
from simulation import time

from profiler.profiler import profilerObj

SIMULATION_TICK_LENGTH = 5 * time.MINUTE

class Simulation:
    def __init__(self, persons, grid):
        self.now = time.Timestamp(time.HOUR * 0)
        self.persons = persons
        self.lastUpdate = -1

        for thePerson in self.persons:
            self.plan(thePerson, grid)

    def simulate(self, grid):
        self.now.minute += 1

        if self.now.minute < self.lastUpdate + SIMULATION_TICK_LENGTH:
            return

        deltaInMinutes = SIMULATION_TICK_LENGTH

        self.lastUpdate = self.now.minute

        persons_travelling = 0
        persons_at_place = { place.PlaceType.HOME : 0, place.PlaceType.WORK : 0, place.PlaceType.OUTDOOR : 0, "EAT": 0 }

        profilerObj.startProfiling("stats+travelling")
        for thePerson in self.persons:
            if thePerson.isTraveling():
                persons_travelling += 1
                if self.now.now() > thePerson.travelEnd.now():
                    thePerson.currentPosition = thePerson.currentDestination
            else:
                if thePerson.currentPosition.char.placeType == place.PlaceType.WORK and thePerson.currentPosition != thePerson.workplace:
                    persons_at_place["EAT"] += 1
                else:
                    persons_at_place[thePerson.currentPosition.char.placeType] += 1

        profilerObj.stopStartProfiling("plan")
        for thePerson in self.persons:
            if self.now.now() < thePerson.schedule.items[0].stop:
                continue

            thePerson.needs.update(self.now)
            dur = thePerson.schedule.items[0].stop - thePerson.schedule.items[0].start
            for need in thePerson.schedule.items[0].place.char.needTypes:
                if need != needs.NeedType.WORK or thePerson.schedule.items[0].place == thePerson.workplace:
                    if thePerson.needs.needs[need] >= 0.75:
                        thePerson.needs.needs[need] -= dur / time.HOUR * 0.5
            
            self.plan(thePerson,grid)
            nextGoal = thePerson.schedule.getNext()
            
            thePerson.setDestination(nextGoal.place, self.now)

        profilerObj.stopProfiling()
        
        logging.Logger.write("activity", self.now.minute, persons_travelling, *(persons_at_place.values()))

    #Plan the schedule of a person
    def plan(self, person, grid):
        for need in person.needs.getPrioNeeds():
            exists, openPlace, dur = needs.canBeSatisfied(person, grid, need, self.now, person.needs.needs[need])
            if exists:
                person.schedule.plan(openPlace, self.now.now(), self.now.now()+dur)
                return                


    @staticmethod
    def gauss(mu, sigma, _min):
        return max(_min, random.gauss(mu, sigma))
