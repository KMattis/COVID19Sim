import enum
import random

from simulation import time, simulation, math
from model import place


class NeedType(enum.Flag):
    NONE = enum.auto()
    EAT = enum.auto()
    SLEEP = enum.auto()
    WORK = enum.auto()
    OUTDOOR = enum.auto()

class Needs:
    def __init__(self, dEat, dSleep, dWork, dOutdoor):
        self.needs = { NeedType.EAT: 0, NeedType.SLEEP: random.uniform(0.6, 0.8), NeedType.WORK: 0, NeedType.OUTDOOR: 0 }
        self.deltas = { NeedType.EAT: dEat * random.uniform(0.9, 1.1),
                NeedType.SLEEP: dSleep * random.uniform(0.9, 1.1),
                NeedType.WORK: dWork * random.uniform(0.9, 1.1),
                NeedType.OUTDOOR: dOutdoor*random.uniform(0.9, 1.1) }
        self.lastNeedUpdate = 0

    def update(self, now):
        delta = now.now() - self.lastNeedUpdate
        self.needs[NeedType.EAT] = min(1, self.needs[NeedType.EAT] + self.deltas[NeedType.EAT] * delta)
        self.needs[NeedType.SLEEP] = min(1, self.needs[NeedType.SLEEP] + self.deltas[NeedType.SLEEP] * delta)
        self.needs[NeedType.WORK] = min(1, self.needs[NeedType.WORK] + self.deltas[NeedType.WORK] * delta)
        self.needs[NeedType.OUTDOOR] = min(1, self.needs[NeedType.OUTDOOR] + self.deltas[NeedType.OUTDOOR] * delta)
        self.lastNeedUpdate = now.now()

    def getPrioNeeds(self):
        sortedNeeds = sorted([k for k in self.needs.keys() if self.needs[k] >= 0.5], key=lambda k: self.needs[k], reverse=True)
        sortedNeeds.append(NeedType.SLEEP)
        return sortedNeeds

def canBeSatisfied(person, grid, need, now, needval):
    distmap = grid.getDistanceMap()
    if need == NeedType.WORK:
        return person.workplace.isOpen(now), person.workplace, math.truncated_gauss(person.workplace.char.avgDuration / 4, time.HOUR, time.HOUR)
    elif need == NeedType.SLEEP:
        return True, person.home, max(1 * time.HOUR, needval * time.HOUR * 3 * random.uniform(0.9, 1.1))
    elif need == NeedType.OUTDOOR:
        nearparks = distmap.getNearPlaces(person.currentPosition.x, person.currentPosition.y, place.SubType.PARK)
        for (pos, _, __) in nearparks:
            x,y = pos
            if grid.get(x,y).isOpen(now):
                return True, grid.get(x,y), math.truncated_gauss(time.HOUR, time.HOUR, time.HOUR)
        return False, None, None
    elif need == NeedType.EAT:
        nearres = distmap.getNearPlaces(person.currentPosition.x, person.currentPosition.y, place.SubType.RESTAURANT)
        for (pos, _, __) in nearres:
            x,y = pos
            if grid.get(x,y).isOpen(now):
                return True, grid.get(x,y), math.truncated_gauss(time.HOUR, time.HOUR, time.HOUR)
        return False, None, None
    else:
        raise Exception("Unknown need type")

