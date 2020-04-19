import enum

from simulation import time

from model import place_characteristics

class Place:
    def __init__(self, x: int, y: int, name: str, characteristics: place_characteristics.PlaceCharacteristics, index: int):
        self.x: int = x
        self.y: int = y
        self.name: str = name
        self.index = index
        self.char: place_characteristics.PlaceCharacteristics = characteristics

    def isOpen(self, timestamp: time.Timestamp) -> bool:
        return timestamp.dayOfWeek() in self.char.openDays and self.char.openHours[0] <= timestamp.hourOfDay()*time.HOUR < self.char.openHours[0] + self.char.openHours[1]
