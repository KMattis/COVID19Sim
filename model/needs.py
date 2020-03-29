import enum
import random

from simulation import time, simulation
from model import place

EAT_NEED_PER_MINUTE = 0.1 / time.HOUR
SLEEP_NEED_PER_MINUTE = 0.2 / time.HOUR
WORK_NEED_PER_MINUTE = 0.1  / time.HOUR
OUTDOOR_NEED_PER_MINUTE = 0.01  / time.HOUR

class NeedType(enum.Flag):
    NONE = enum.auto()
    EAT = enum.auto()
    SLEEP = enum.auto()
    WORK = enum.auto()
    OUTDOOR = enum.auto()

class Needs:
    def __init__(self, dEat = EAT_NEED_PER_MINUTE, dSleep = SLEEP_NEED_PER_MINUTE, dWork = WORK_NEED_PER_MINUTE, dOutdoor = OUTDOOR_NEED_PER_MINUTE):
        self.needs = { NeedType.EAT: 0, NeedType.SLEEP: random.uniform(0.6, 0.8), NeedType.WORK: 0, NeedType.OUTDOOR: 0 }
        self.deltas = { NeedType.EAT: dEat * random.uniform(0.9, 1.1),
                NeedType.SLEEP: dSleep * random.uniform(0.9, 1.1),
                NeedType.WORK: dWork * random.uniform(0.9, 1.1),
                NeedType.OUTDOOR: dOutdoor*random.uniform(0.9, 1.1) }

    def update(self, delta):
        self.needs[NeedType.EAT] = min(1, self.needs[NeedType.EAT] + self.deltas[NeedType.EAT] * delta)
        self.needs[NeedType.SLEEP] = min(1, self.needs[NeedType.SLEEP] + self.deltas[NeedType.SLEEP] * delta)
        self.needs[NeedType.WORK] = min(1, self.needs[NeedType.WORK] + self.deltas[NeedType.WORK] * delta)
        self.needs[NeedType.OUTDOOR] = min(1, self.needs[NeedType.OUTDOOR] + self.deltas[NeedType.OUTDOOR] * delta)

    def needsWork(self):
        return self.needs[NeedType.WORK] > 0.5
        
    def needsSleep(self):
        return self.needs[NeedType.SLEEP] > 0.5

    def needsEat(self):
        return self.needs[NeedType.EAT] > 0.5

    def needsOutdoor(self):
        return self.needs[NeedType.OUTDOOR] > 0.5

    def getPrioNeeds(self):
        return sorted(self.needs.keys(), key=lambda k: self.needs[k], reverse=True)

def canBeSatisfied(person, grid, need, now, needval):
    distmap = grid.getDistanceMap()
    if need == NeedType.WORK:
        return person.workplace.hasOpen(now), person.workplace, simulation.Simulation.gauss(person.workplace.char.avgDuration, time.HOUR, time.HOUR)
    elif need == NeedType.SLEEP:
        return True, person.home, needval * time.HOUR * 8 * random.uniform(0.9, 1.1)
    elif need == NeedType.OUTDOOR:
        nearparks = distmap.getNearPlaces(person.currentPosition.x, person.currentPosition.y, place.SubType.PARK)
        nearparks = list(filter(lambda p: grid.get(p[0][0], p[0][1]).hasOpen(now), nearparks))
        parkIndex = 0 if len(nearparks) == 0 else random.randrange(0, len(nearparks))
        return len(nearparks) > 0, None if len(nearparks) == 0 else grid.get(nearparks[parkIndex][0][0], nearparks[parkIndex][0][1]), simulation.Simulation.gauss(time.HOUR, time.HOUR, time.HOUR)#TODO
    elif need == NeedType.EAT:
        nearres = distmap.getNearPlaces(person.currentPosition.x, person.currentPosition.y, place.SubType.RESTAURANT)
        nearres = list(filter(lambda p: grid.get(p[0][0], p[0][1]).hasOpen(now), nearres))
        resIndex = 0 if len(nearres) == 0 else random.randrange(0, len(nearres))
        return len(nearres) > 0, None if len(nearres) == 0 else grid.get(nearres[resIndex][0][0], nearres[resIndex][0][1]), simulation.Simulation.gauss(time.HOUR, time.HOUR, time.HOUR) #TODO
    else:
        raise Exception("Unknown need type")

