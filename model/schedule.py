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

class Schedule:
    def __init__(self):
        self.task: ScheduleItem = None

    def plan(self, place: place.Place, start: int, stop: int, activity: need_type.NeedType) -> None:
        if self.task is not None and start < self.task.stop:
            raise Exception("Events must be added in ascending order {0},{1},{2}".format(place.char.placeType, start, stop)) 
        self.task = ScheduleItem(place, start, stop, activity)
    
