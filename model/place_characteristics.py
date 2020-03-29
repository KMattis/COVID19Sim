class PlaceCharacteristics:
    def __init__(self, placeType, avgArrival, avgDuration, openDays, openHours, needTypes, subType, frequency):
        self.openHours = openHours
        self.openDays = openDays
        self.avgArrival = avgArrival
        self.avgDuration = avgDuration
        self.placeType = placeType
        self.needTypes = needTypes
        self.subType = subType
        self.frequency = frequency
