import enum
import random

from simulation import time

EAT_NEED_PER_MINUTE = 0.1 / time.HOUR
SLEEP_NEED_PER_MINUTE = 0.2 / time.HOUR
WORK_NEED_PER_MINUTE = 0.1  / time.HOUR

class NeedType(enum.Flag):
    NONE = enum.auto()
    EAT = enum.auto()
    SLEEP = enum.auto()
    WORK = enum.auto()

class Needs:
    def __init__(self, dEat = EAT_NEED_PER_MINUTE, dSleep = SLEEP_NEED_PER_MINUTE, dWork = WORK_NEED_PER_MINUTE):
        self.needs = { NeedType.EAT: 0, NeedType.SLEEP: random.uniform(0.6, 0.8), NeedType.WORK: 0 }
        self.deltas = { NeedType.EAT: dEat * random.uniform(0.9, 1.1),
                NeedType.SLEEP: dSleep * random.uniform(0.9, 1.1),
                NeedType.WORK: dWork * random.uniform(0.9, 1.1) }

    def update(self, delta):
        self.needs[NeedType.EAT] = min(1, self.needs[NeedType.EAT] + self.deltas[NeedType.EAT] * delta)
        self.needs[NeedType.SLEEP] = min(1, self.needs[NeedType.SLEEP] + self.deltas[NeedType.SLEEP] * delta)
        self.needs[NeedType.WORK] = min(1, self.needs[NeedType.WORK] + self.deltas[NeedType.WORK] * delta)

    def needsWork(self):
        return self.needs[NeedType.WORK] > 0.5
        
    def needsSleep(self):
        return self.needs[NeedType.SLEEP] > 0.5

    def needsEat(self):
        return self.needs[NeedType.EAT] > 0.5
