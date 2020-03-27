import enum

class PlaceType(enum.Enum):
    NONE = -1
    HOME = 0
    SERVICE = 1
    NONSERVICE = 2
    MASSEVENT = 3
    OUTDOOR = 4
    HEALTHCARE = 5

class Place:
    def __init__(self, x, y, name, characteristics):
        self.x = x
        self.y = y
        self.name = name
        self.char = characteristics

class PlaceCharacteristics:
    def __init__(self, placeType):
        self.placeType = placeType
