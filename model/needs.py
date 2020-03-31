import enum
import random

from typing import Dict

from simulation import time, math
from model import place_characteristics


class NeedType(enum.Flag):
    NONE = enum.auto()
    EAT = enum.auto()
    SLEEP = enum.auto()
    WORK = enum.auto()
    OUTDOOR = enum.auto()

class Needs:
    def __init__(self, dEat: float, dSleep: float, dWork: float, dOutdoor: float):
        self.needs: Dict[NeedType, float] = { NeedType.EAT: 0, NeedType.SLEEP: random.uniform(0.6, 0.8), NeedType.WORK: 0, NeedType.OUTDOOR: 0 }
        self.deltas: Dict[NeedType, float] = { NeedType.EAT: dEat * random.uniform(0.9, 1.1),
                NeedType.SLEEP: dSleep * random.uniform(0.9, 1.1),
                NeedType.WORK: dWork * random.uniform(0.9, 1.1),
                NeedType.OUTDOOR: dOutdoor*random.uniform(0.9, 1.1) }
        self.lastNeedUpdate: int = 0

    def update(self, now: time.Timestamp) -> None:
        delta = now.now() - self.lastNeedUpdate
        self.needs[NeedType.EAT] = min(1, self.needs[NeedType.EAT] + self.deltas[NeedType.EAT] * delta)
        self.needs[NeedType.SLEEP] = min(1, self.needs[NeedType.SLEEP] + self.deltas[NeedType.SLEEP] * delta)
        self.needs[NeedType.WORK] = min(1, self.needs[NeedType.WORK] + self.deltas[NeedType.WORK] * delta)
        self.needs[NeedType.OUTDOOR] = min(1, self.needs[NeedType.OUTDOOR] + self.deltas[NeedType.OUTDOOR] * delta)
        self.lastNeedUpdate = now.now()

    def getPrioNeeds(self) -> [NeedType]:
        sortedNeeds = sorted([k for k in self.needs.keys() if self.needs[k] >= 0.5], key=lambda k: self.needs[k], reverse=True)
        sortedNeeds.append(NeedType.SLEEP)
        return sortedNeeds
