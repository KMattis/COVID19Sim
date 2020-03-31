import enum
import random

from typing import Dict

from simulation import time, math
from model import place_characteristics, need_type

class Needs:
    def __init__(self, needTypes: [need_type.NeedType]):
        self.needs: Dict[need_type.NeedType, float] = {}
        self.deltas: Dict[need_type.NeedType, float] = {}
        for needType in needTypes:
            self.needs[needType] = random.uniform(0, 1)
            self.deltas[needType] = needType.getDelta() * random.uniform(0.9, 1.1)
        self.lastNeedUpdate: int = 0

    def update(self, now: time.Timestamp) -> None:
        delta = now.now() - self.lastNeedUpdate
        self.lastNeedUpdate = now.now()

        for needType in self.needs:
            self.needs[needType] = min(1, self.needs[needType] + self.deltas[needType] * delta)

    def getPrioNeeds(self) -> [need_type.NeedType]:
        sortedNeeds = sorted([k for k in self.needs.keys()], key=lambda k: self.needs[k], reverse=True)
        #sortedNeeds.append(NeedType.SLEEP)
        return sortedNeeds
