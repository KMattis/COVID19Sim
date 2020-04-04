from model import place, need_type

class ScheduleItem:
    def __init__(self, place: place.Place, start: int, stop: int, activity: need_type.NeedType):
        self.place = place
        self.start = start
        self.stop = stop
        self.activity = activity

    def getDuration(self) -> int:
        return self.stop - self.start

    def __str__(self) -> str:
        return str(self.place.char.placeType) + ": " + str(self.start) + "-" + str(self.stop)
