import enum

from simulation import time

EAT_NEED_PER_MINUTE = 0.2 / time.HOUR
SLEEP_NEED_PER_MINUTE = 0.1 / time.HOUR
WORK_NEED_PER_MINUTE = 0.1  / time.HOUR

class NeedType(enum.Flag):
    NONE = enum.auto()
    EAT = enum.auto()
    SLEEP = enum.auto()
    WORK = enum.auto()

class Needs:
    def __init__(self, dEat = EAT_NEED_PER_MINUTE, dSleep = SLEEP_NEED_PER_MINUTE, dWork = WORK_NEED_PER_MINUTE):
        self.needs = { NeedType.EAT: 0, NeedType.SLEEP: 0, NeedType.WORK: 0 }
        self.deltas = { NeedType.EAT: dEat, NeedType.SLEEP: dSleep, NeedType.WORK: dWork }

    def update(self, delta):
        self.needs[NeedType.EAT] = min(1, self.needs[NeedType.EAT] + self.deltas[NeedType.EAT] * delta)
        self.needs[NeedType.SLEEP] = min(1, self.needs[NeedType.SLEEP] + self.deltas[NeedType.SLEEP] * delta)
        self.needs[NeedType.WORK] = min(1, self.needs[NeedType.WORK] + self.deltas[NeedType.WORK] * delta)