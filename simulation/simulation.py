from model import grid, place, person
from simulation import time

SIMULATION_SPEED = 0.01
SIMULATION_TICK_LENGTH = 5 * time.MINUTE

class Simulation:
    def __init__(self, persons):
        self.now = time.Timestamp(time.HOUR * 8)
        self.lastUpdate = time.Timestamp(time.HOUR * 8)
        self.persons = persons

    def simulate(self, delta):
        self.now.minute += delta * SIMULATION_SPEED

        if self.now.now() - self.lastUpdate.now() > SIMULATION_TICK_LENGTH: # We only simulate in SIMULATION_TICK_LENGTH Minute timestamps
            self.lastUpdate.set(self.now.now())
            for thePerson in self.persons:
                thePerson.update(self.now)