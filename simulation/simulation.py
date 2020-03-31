import random

from plotting import logging

from model import grid, place, person, needs, place_characteristics
from simulation import time, math

from profiler.profiler import profilerObj

SIMULATION_TICK_LENGTH = 5 * time.MINUTE

class Simulation:
    def __init__(self, persons, grid):
        self.now = time.Timestamp(time.HOUR * 0)
        self.persons = persons
        self.lastUpdate = -1

        for thePerson in self.persons:
            self.plan(thePerson, grid)

    def simulate(self, grid):
        self.now.minute += SIMULATION_TICK_LENGTH

        self.lastUpdate = self.now.minute

        persons_at_place = { "TRAVEL": 0, place_characteristics.PlaceType.HOME : 0, place_characteristics.PlaceType.WORK : 0, place_characteristics.PlaceType.OUTDOOR : 0, "EAT": 0 }

        place_map = {}
        for thePerson in self.persons:

            if thePerson.isTravelling():
                persons_at_place["TRAVEL"] += 1
                if self.now.now() > thePerson.travelEnd.now():
                    thePerson.currentPosition = thePerson.currentDestination
            else:

                appendPlaceMap(place_map, thePerson)

                if thePerson.currentPosition.char.placeType == place_characteristics.PlaceType.WORK and thePerson.currentPosition != thePerson.workplace:
                    persons_at_place["EAT"] += 1
                else:
                    persons_at_place[thePerson.currentPosition.char.placeType] += 1


            if self.now.now() < thePerson.schedule.task.stop:
                continue

            thePerson.needs.update(self.now)
            thePerson.sickness.update(self.now)
            
            dur = thePerson.schedule.task.getDuration()
            for need in thePerson.schedule.task.place.char.needTypes:
                if need != needs.NeedType.WORK or thePerson.schedule.task.place == thePerson.workplace:
                    if thePerson.needs.needs[need] >= 0.75:
                        thePerson.needs.needs[need] -= dur / time.HOUR * 0.5
 
            self.plan(thePerson,grid)

        for pl in filter(lambda pl: place_map[pl][1] > 0, place_map):
            #Determine infection risk at pl
            #...
            for thePerson in place_map[pl][0]:
                pWorker, pVisitor = pl.getInfectionRisks( )
                #Infect with prob. as calculated above

        logging.write("activity", self.now.minute, *(persons_at_place.values()))

    #Plan the schedule of a person
    def plan(self, person, grid):
        for need in person.needs.getPrioNeeds():
            exists, openPlace, dur = canBeSatisfied(person, grid, need, self.now, person.needs.needs[need])
            if exists:
                person.schedule.plan(openPlace, self.now.now(), self.now.now()+dur)
                person.setDestination(person.schedule.task.place, self.now)
                return                

def appendPlaceMap(place_map, thePerson) -> None: 
    thePlace = thePerson.schedule.task.place
    if not thePlace in place_map:
        place_map[thePlace] = [[thePerson], 1 if thePerson.sickness.isContagious() else 0] 
        return
    if thePerson.sickness.isInfected:
        place_map[thePlace][1] += 1
    place_map[thePerson.schedule.task.place][0].append(thePerson)

def canBeSatisfied(person: person.Person, grid: grid.Grid, need: needs.NeedType, now: time.Timestamp, needval: float) -> (bool, place.Place, int):
    distmap = grid.getDistanceMap()
    if need == needs.NeedType.WORK:
        return person.workplace.isOpen(now), person.workplace, math.truncated_gauss(person.workplace.char.avgDuration / 4, time.HOUR, time.HOUR)
    elif need == needs.NeedType.SLEEP:
        return True, person.home, max(1 * time.HOUR, needval * time.HOUR * 3 * random.uniform(0.9, 1.1))
    elif need == needs.NeedType.OUTDOOR:
        nearparks = distmap.getNearPlaces(person.currentPosition.x, person.currentPosition.y, place_characteristics.SubType.PARK)
        for (pos, _, __) in nearparks:
            x,y = pos
            if grid.get(x,y).isOpen(now):
                return True, grid.get(x,y), math.truncated_gauss(time.HOUR, time.HOUR, time.HOUR)
        return False, None, None
    elif need == needs.NeedType.EAT:
        nearres = distmap.getNearPlaces(person.currentPosition.x, person.currentPosition.y, place_characteristics.SubType.RESTAURANT)
        for (pos, _, __) in nearres:
            x,y = pos
            if grid.get(x,y).isOpen(now):
                return True, grid.get(x,y), math.truncated_gauss(time.HOUR, time.HOUR, time.HOUR)
        return False, None, None
    else:
        raise Exception("Unknown need type")

