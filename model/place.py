import enum

from simulation import time

class PlaceType(enum.Enum):
    NONE = -1
    HOME = 0
    WORK = 1
    MASSEVENT = 2
    OUTDOOR = 3
    HEALTHCARE = 4

class SubType(enum.Enum):
    NONE = -1
    RESTAURANT = 0
    PARK = 1
    OFFICE = 2
    HOME = 3
     

class Place:
    def __init__(self, x, y, name, characteristics):
        self.x = x
        self.y = y
        self.name = name
        self.char = characteristics

    def isOpen(self, timestamp):
        return self.char.openHours[0] <= timestamp.hourOfDay()*time.HOUR < self.char.openHours[0] + self.char.openHours[1]
