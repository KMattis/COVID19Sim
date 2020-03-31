class ScheduleItem:
    def __init__(self, place, start, stop):
        self.place = place
        self.start = start
        self.stop = stop

    def intersectsWith(self, item):
        return self.start <= item.start < self.stop or item.start <= self.start < item.stop

    def __str__(self):
        return str(self.place.char.placeType) + ": " + str(self.start) + "-" + str(self.stop)

class Schedule:
    def __init__(self, home):
        self.items = []
        self.home = home
    
    def getNext(self):
        self.items = self.items[1:]

        if len(self.items) > 0: 
            return self.items[0]
        else:
            return None

    def plan(self, place, start, stop):
        if len(self.items) > 0:
            if start < self.items[-1].stop:
                raise Exception("Events must be added in ascending order {0},{1},{2}".format(place.char.placeType, start, stop)) 
        self.items.append(ScheduleItem(place, start, stop))

    def getLastScheduledItem(self):
        if len(self.items) > 0:
            return self.items[-1]
        else:
            return None
