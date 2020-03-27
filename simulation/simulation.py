from model import grid, place, person
from simulation import time

SIMULATION_SPEED = 0.01

class Simulation:
    def __init__(self, persons):
        self.now = time.Timestamp(time.HOUR * 8)
        self.persons = persons

    def simulate(self, delta):
        self.now.minute += delta * SIMULATION_SPEED
        for thePerson in self.persons:
            thePerson.update(self.now)
