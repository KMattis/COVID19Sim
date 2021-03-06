MINUTE = 1
HOUR = 60 * MINUTE
DAY = 24 * HOUR
WEEK = 7 * DAY

class Timestamp:
    def __init__(self, minute):
        self.minute = minute

    def set(self, minute):
        self.minute = minute

    def now(self):
        return self.minute

    def minuteOfHour(self):
        return (self.minute // MINUTE) % (HOUR/MINUTE)

    def hourOfDay(self):
        return (self.minute // HOUR) % (DAY/HOUR)

    def day(self):
        return self.minute // DAY

    def today(self):
        return self.day() * DAY

    def dayOfWeek(self):
        return self.day() % (WEEK // DAY)
