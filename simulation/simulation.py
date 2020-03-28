import random

from plotting import logging

from model import grid, place, person
from simulation import time

from profiler.profiler import profilerObj

SIMULATION_SPEED = 0.01
SIMULATION_TICK_LENGTH = 1 * time.MINUTE

class Simulation:
    def __init__(self, persons):
        self.now = time.Timestamp(time.HOUR * 6)
        self.persons = persons
        self.lastUpdate = -1

        for thePerson in self.persons:
            self.plan(thePerson)

    def simulate(self, delta):
        self.now.minute += delta * SIMULATION_SPEED

        if self.now.minute < self.lastUpdate + SIMULATION_TICK_LENGTH:
            return

        self.lastUpdate = self.now.minute

        persons_travelling = 0
        for thePerson in self.persons:
            if thePerson.isTraveling():
                persons_travelling += 1
                if self.now.now() > thePerson.travelEnd.now():
                    thePerson.currentPosition = thePerson.currentDestination

            if self.now.now() < thePerson.schedule.items[0].stop:
                continue

            nextGoal = thePerson.schedule.getNext()
            
            if thePerson.schedule.needsPlanning():
                self.plan(thePerson)

            thePerson.setDestination(nextGoal.place, self.now)
        
        logging.Logger.write("travelling", self.now.minute, persons_travelling)

    #Plan the schedule of a person
    def plan(self, person):
        lastItem = person.schedule.getLastScheduledItem()
        if lastItem == None:
            nextDayToPlan = self.now.today()
            t = -1
        else:
            nextDayToPlan = time.Timestamp(lastItem.start + time.DAY).today()
            t = lastItem.stop
        
        start = max(t+1, nextDayToPlan + random.choice(person.workplace.char.avgArrival) + Simulation.gauss(0,
                time.HOUR, -2 *time.HOUR))
        person.schedule.plan(person.workplace,
            start,
            Simulation.gauss(start + person.workplace.char.avgDuration, time.HOUR, start + time.HOUR))

    @staticmethod
    def gauss(mu, sigma, _min):
        return max(_min, random.gauss(mu, sigma))
