import enum



class PlaceType(enum.Enum):
    WORK    = 0
    HOME    = 1
    LEISURE = 2
    HEALTH  = 3

class Place:
    def __init__(self, placeType: PlaceType):
        self.type = placeType
        
    