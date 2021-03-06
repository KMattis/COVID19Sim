from simulation import random
from model import need_type, place_characteristics, schedule
from simulation import time, math

class Sleep(need_type.NeedType):
    def __init__(self):
        self.homes = {}

    def initialize(self, needTypes, persons, grid):
        homes = [thePlace for thePlace in grid.internal_grid
            if thePlace is not None
            and thePlace.char.placeType is place_characteristics.PlaceType.HOME]
        
        for person in persons:
            self.homes[person] = random.choice(homes)
            person.currentPosition = self.homes[person]
            person.currentDestination = self.homes[person]
            
    def trySatisfy(self, person, needValue, now):
        return schedule.ScheduleItem(self.homes[person], now.now(), now.now() + random.uniform(2 * time.HOUR, 4 * time.HOUR), self)

    def getName(self):
        return "SLEEP"

class Work(need_type.NeedType):
    def __init__(self):
        self.workplaces = {}

    def initialize(self, needTypes, persons, grid):
        workplaces = [thePlace for thePlace in grid.internal_grid
            if thePlace is not None
            and (thePlace.char.placeType is place_characteristics.PlaceType.WORK
                or thePlace.char.placeType is place_characteristics.PlaceType.HEALTHCARE)]
        
        for person in persons:
            self.workplaces[person] = random.choice(workplaces)
        
    def trySatisfy(self, person, needValue, now):
        workplace = self.workplaces[person]
        if workplace.isOpen(now):
            return schedule.ScheduleItem(workplace, now.now(), now.now() + random.uniform(2 * time.HOUR, 4 * time.HOUR), self)
        else:
            return None

    def getName(self):
        return "WORK"

class Eat(need_type.NeedType):
    def __init__(self):
        self.grid = None

    def initialize(self, needTypes, persons, grid):
        self.grid = grid

    def trySatisfy(self, person, needValue, now):
        distmap = self.grid.getDistanceMap()
        nearres = distmap.getNearPlaces(person.currentPosition.x, person.currentPosition.y, place_characteristics.SubType.RESTAURANT)
        for (pos, _, __) in nearres:
            x,y = pos
            if self.grid.get(x,y).isOpen(now):
                return schedule.ScheduleItem(self.grid.get(x,y), now.now(), now.now() + random.uniform(time.MINUTE * 10, time.MINUTE * 30), self)
        return None

    def getName(self):
        return "EAT"

class Outdoor(need_type.NeedType):
    def __init__(self):
        self.grid = None

    def initialize(self, needTypes, persons, grid):
        self.grid = grid

    def trySatisfy(self, person, needValue, now):
        distmap = self.grid.getDistanceMap()
        nearparks = distmap.getNearPlaces(person.currentPosition.x, person.currentPosition.y, place_characteristics.SubType.PARK)
        for (pos, _, __) in nearparks:
            x,y = pos
            if self.grid.get(x,y).isOpen(now):
                return schedule.ScheduleItem(self.grid.get(x,y), now.now(), now.now() + random.uniform(time.HOUR, 2 * time.HOUR), self)
        return None
    
    def getName(self):
        return "OUTDOOR"

class Social(need_type.NeedType):
    def __init__(self):
        self.sleep = None
        self.gatherings = {}
        self.massEvents = None

    def initialize(self, needTypes, persons, grid):
        self.sleep = needTypes["SLEEP"]
        self.massEvents = [p for p in grid.internal_grid if p.char.placeType == place_characteristics.PlaceType.MASSEVENT]

    def trySatisfy(self, person, needValue, now):
        if person in self.gatherings and self.gatherings[person].stop < now.now() - 30*time.MINUTE:
            return self.gatherings[person]
            
        startTime = now.now()
        duration = random.uniform(time.HOUR, 3 * time.HOUR)
        endTime = startTime + duration

        possiblePlaces = [self.sleep.homes[person]] + [p for p in self.massEvents if p.isOpen(now)]
        date = schedule.ScheduleItem(random.choice(possiblePlaces), startTime, endTime, self)

        for p in person.friends:
            self.gatherings[p] = date

        return date
    
    def getName(self):
        return "SOCIAL"

class Health(need_type.NeedType):
    def __init__(self):
        self.grid = None

    def initialize(self, needTypes, persons, grid):
        self.grid = grid

    def trySatisfy(self, person, needValue, now):
        distmap = self.grid.getDistanceMap()
        nearHospitals = distmap.getNearPlaces(person.currentPosition.x, person.currentPosition.y, place_characteristics.SubType.HOSPITAL)
        for (pos, _, __) in nearHospitals:
            x,y = pos
            if self.grid.get(x,y).isOpen(now):
                return schedule.ScheduleItem(self.grid.get(x,y), now.now(), now.now() + random.uniform(time.HOUR, 2 * time.HOUR), self)
        return None
    
    def getName(self):
        return "HEALTH"

