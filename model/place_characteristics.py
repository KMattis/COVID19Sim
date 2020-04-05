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
    HOSPITAL = 4

class PlaceCharacteristics:
    def __init__(self,
            placeType: PlaceType,
            openDays: [int],
            openHours:[int],
            subType: SubType,
            frequency: int,
            contactFrequency: float,
            contactDistance: float):
        
        self.openHours: [int] = openHours
        self.openDays: [int] = openDays
        self.placeType: PlaceType = placeType
        self.subType: SubType = subType
        self.frequency: int = frequency
        self.contactFrequency: float = contactFrequency
        self.contactDistance: float = contactDistance

NONE_CHAR = PlaceCharacteristics(PlaceType.NONE, 0, 0, SubType.NONE, 0, 0, 0)