import random

from model import need_type, place_characteristics
from simulation import time, math

class Sleep(need_type.NeedType):
    def __init__(self):
        self.homes = {}

    def initialize(self, persons, grid):
        homes = [thePlace for thePlace in grid.internal_grid
            if thePlace is not None
            and thePlace.char.placeType is place_characteristics.PlaceType.HOME]
        
        for person in persons:
            self.homes[person] = random.choice(homes)
        
    def trySatisfy(self, person, needValue, now):
        return True, self.homes[person], random.uniform(time.HOUR, 2 * time.HOUR)

    def getName(self):
        return "SLEEP"

    def getDelta(self):
        return 10 / time.DAY 

class Work(need_type.NeedType):
    def __init__(self):
        self.workplaces = {}

    def initialize(self, persons, grid):
        workplaces = [thePlace for thePlace in grid.internal_grid
            if thePlace is not None
            and thePlace.char.placeType is place_characteristics.PlaceType.WORK]
        
        for person in persons:
            self.workplaces[person] = random.choice(workplaces)
        
    def trySatisfy(self, person, needValue, now):
        workplace = self.workplaces[person]
        return workplace.isOpen(now), workplace, random.uniform(time.HOUR, 2 * time.HOUR)

    def getName(self):
        return "WORK"

    def getDelta(self):
        return 10 / time.DAY 

class Eat(need_type.NeedType):
    def __init__(self):
        self.grid = None

    def initialize(self, persons, grid):
        self.grid = grid

    def trySatisfy(self, person, needValue, now):
        distmap = self.grid.getDistanceMap()
        nearres = distmap.getNearPlaces(person.currentPosition.x, person.currentPosition.y, place_characteristics.SubType.RESTAURANT)
        for (pos, _, __) in nearres:
            x,y = pos
            if self.grid.get(x,y).isOpen(now):
                return True, self.grid.get(x,y), random.uniform(time.MINUTE * 10, time.MINUTE * 30)
        return False, None, None

    def getName(self):
        return "EAT"

    def getDelta(self):
        return 2 / time.DAY 

class Outdoor(need_type.NeedType):
    def __init__(self):
        self.grid = None

    def initialize(self, persons, grid):
        self.grid = grid

    def trySatisfy(self, person, needValue, now):
        distmap = self.grid.getDistanceMap()
        nearparks = distmap.getNearPlaces(person.currentPosition.x, person.currentPosition.y, place_characteristics.SubType.PARK)
        for (pos, _, __) in nearparks:
            x,y = pos
            if self.grid.get(x,y).isOpen(now):
                return True, self.grid.get(x,y), random.uniform(time.HOUR, 2 * time.HOUR)
        return False, None, None
    
    def getName(self):
        return "OUTDOOR"
    
    def getDelta(self):
        return 0.5 / time.DAY 
