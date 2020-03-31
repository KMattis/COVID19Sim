import enum

from model import need_type

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

class PlaceCharacteristics:
    def __init__(self, placeType: PlaceType, avgArrival: [int], avgDuration: int, openDays: [int], openHours:[int], needTypes: [need_type.NeedType], subType: SubType, frequency: int):
        self.openHours: [int] = openHours
        self.openDays: [int] = openDays
        self.avgArrival: [int] = avgArrival
        self.avgDuration: int = avgDuration
        self.placeType: PlaceType = placeType
        self.needTypes: [need_type.NeedType] = needTypes
        self.subType: SubType = subType
        self.frequency: int = frequency
