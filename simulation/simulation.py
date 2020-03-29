import random

from plotting import logging

from model import grid, place, person, needs
from simulation import time

from profiler.profiler import profilerObj

SIMULATION_SPEED = 0.1
SIMULATION_TICK_LENGTH = 1 * time.MINUTE

class Simulation:
    def __init__(self, persons, grid):
        self.now = time.Timestamp(time.HOUR * 6)
        self.persons = persons
        self.lastUpdate = -1

        for thePerson in self.persons:
            self.plan(thePerson, grid)

    def simulate(self, delta, grid):
        self.now.minute += delta * SIMULATION_SPEED

        if self.now.minute < self.lastUpdate + SIMULATION_TICK_LENGTH:
            return

        deltaInMinutes = self.now.minute - self.lastUpdate

        self.lastUpdate = self.now.minute

        persons_travelling = 0
        persons_at_place = { place.PlaceType.HOME : 0, place.PlaceType.SERVICE : 0, place.PlaceType.NONSERVICE : 0, place.PlaceType.OUTDOOR : 0 }
        for thePerson in self.persons:
            thePerson.needs.update(deltaInMinutes)

            if thePerson.isTraveling():
                persons_travelling += 1
                if self.now.now() > thePerson.travelEnd.now():
                    thePerson.currentPosition = thePerson.currentDestination
            else:
                persons_at_place[thePerson.currentPosition.char.placeType] += 1

            if self.now.now() < thePerson.schedule.items[0].stop:
                continue

            thePerson.needs.needs[thePerson.schedule.items[0].place.char.needType] = 0
            self.plan(thePerson,grid)
            nextGoal = thePerson.schedule.getNext()
            
            thePerson.setDestination(nextGoal.place, self.now)
        
        logging.Logger.write("activity", self.now.minute, persons_travelling, *(persons_at_place.values()))


    #Plan the schedule of a person
    def plan(self, person, grid):
        #Check if work need is > 0.5 && work has open
        if person.needs.needsWork() and person.workplace.hasOpen(self.now): #TODO hasOpen is NOT optimal
            person.schedule.plan(person.workplace,
                    self.now.now(),
                    Simulation.gauss(self.now.now() + person.workplace.char.avgDuration, time.HOUR, self.now.now() + time.HOUR))
        elif person.needs.needsEat():
            #get neares eating place
            park = random.choice(grid.parks)
            person.schedule.plan(park,
                    self.now.now(),
                    Simulation.gauss(self.now.now() + time.HOUR, time.HOUR, self.now.now() + time.HOUR))
        else:
            person.schedule.plan(person.home,
                    self.now.now(),
                    Simulation.gauss(self.now.now() + time.HOUR, time.HOUR, self.now.now() + time.HOUR))

        """
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
        """

    @staticmethod
    def gauss(mu, sigma, _min):
        return max(_min, random.gauss(mu, sigma))
