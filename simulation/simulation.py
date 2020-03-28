import random

from model import grid, place, person
from simulation import time

SIMULATION_SPEED = 0.01
SIMULATION_TICK_LENGTH = 5 * time.MINUTE

class Simulation:
    def __init__(self, persons):
        self.now = time.Timestamp(time.HOUR * 8)
        self.lastUpdate = time.Timestamp(time.HOUR * 8)
        self.persons = persons

        for thePerson in self.persons:
            self.plan(thePerson)


    def simulate(self, delta):
        self.now.minute += delta * SIMULATION_SPEED

        if self.now.now() - self.lastUpdate.now() > SIMULATION_TICK_LENGTH: # We only simulate in SIMULATION_TICK_LENGTH Minute timestamps
            self.lastUpdate.set(self.now.now())
            for thePerson in self.persons:
                if thePerson.isTraveling():
                    if self.now.now() > thePerson.travelEnd.now():
                        thePerson.currentPosition = thePerson.currentDestination

                if self.now.now() < thePerson.schedule.items[0].stop:
                    continue

                nextGoal = thePerson.schedule.getNext()
                if thePerson.schedule.needsPlanning():
                    self.plan(thePerson)
                thePerson.setDestination(nextGoal.place, self.now)

    #Plan the schedule of a person
    def plan(self, person):
        lastScheduledTime = time.Timestamp(person.schedule.getLastScheduledTime())

        if lastScheduledTime.now() == 0:
            beginDay = lastScheduledTime.today()
        else:
            beginDay = lastScheduledTime.today() + 1 * time.DAY

        #Plan work for 2 more days
        for i in range(2):
            nextDay = beginDay + i * time.DAY

            person.schedule.plan(person.workplace, 
                nextDay + person.workplace.char.avgArrival + random.randrange(-time.HOUR, +time.HOUR),
                nextDay + person.workplace.char.avgDuration + random.randrange(-time.HOUR, +time.HOUR))

