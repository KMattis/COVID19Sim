class ScheduleItem:
    def __init__(self, place, start, stop):
        self.place = place
        self.start = start
        self.stop = stop

    def intersectsWith(self, item):
        return self.start <= item.start < self.stop or item.start <= self.start < item.stop

    def getDuration(self):
        return self.stop - self.start

    def __str__(self):
        return str(self.place.char.placeType) + ": " + str(self.start) + "-" + str(self.stop)

class Schedule:
    def __init__(self, home):
        self.task = None
        self.home = home

    def plan(self, place, start, stop):
        if self.task is not None and start < self.task.stop:
            raise Exception("Events must be added in ascending order {0},{1},{2}".format(place.char.placeType, start, stop)) 
        self.task = ScheduleItem(place, start, stop)
    