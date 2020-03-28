import random

from model import grid, place, person
from simulation import time

SIMULATION_SPEED = 0.01
SIMULATION_TICK_LENGTH = 5 * time.MINUTE

class Simulation:
    def __init__(self, persons):
        self.now = time.Timestamp(time.HOUR * 6)
        self.persons = persons

        for thePerson in self.persons:
            self.plan(thePerson)

    def simulate(self, delta):
        self.now.minute += delta * SIMULATION_SPEED

        for thePerson in self.persons:
            if thePerson.isTraveling() and self.now.now() > thePerson.travelEnd.now():
                thePerson.currentPosition = thePerson.currentDestination

            if self.now.now() < thePerson.schedule.items[0].stop:
                continue

            nextGoal = thePerson.schedule.getNext()
            if thePerson.schedule.needsPlanning():
                self.plan(thePerson)
            thePerson.setDestination(nextGoal.place, self.now)

    #Plan the schedule of a person
    def plan(self, person):
        t = person.schedule.getLastScheduledTime()
        if t == -1:
            nextDayToPlan = self.now.today()
        else:
            nextDayToPlan = time.Timestamp(t + time.DAY).today()

        start = Simulation.gauss(nextDayToPlan + random.choice(person.workplace.char.avgArrival),
                time.HOUR, self.now.now() + 1)
        person.schedule.plan(person.workplace,
            start,
            Simulation.gauss(start + person.workplace.char.avgDuration, time.HOUR, start + time.HOUR))

    def gauss(mu, sigma, _min):
        return max(_min, random.gauss(mu, sigma))
