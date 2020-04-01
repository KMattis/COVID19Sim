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



