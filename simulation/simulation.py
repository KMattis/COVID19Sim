from simulation import random

from plotting import logging

from model import place, person, place_characteristics, disease, transport
from simulation import time, math

from profiler.profiler import profilerObj

SIMULATION_TICK_LENGTH = 5* time.MINUTE

class PlaceMapObject:
    def __init__(self, diseaseTypes):
        self.updated = -1
        self.persons = []
        self.diseases = {dt: 0 for dt in diseaseTypes}

class TravelMapObject:
    def __init__(self, diseaseTypes):
        self.updated = -1
        self.persons = []
        self.diseases = {dt: 0 for dt in diseaseTypes}


class Simulation:
    def __init__(self, persons, grid, diseaseTypes, trafficNetwork, travelDatas):
        self.now = time.Timestamp(time.HOUR * 0)
        self.persons = persons
        self.grid = grid
        self.i = 0
        self.placeMap = [PlaceMapObject(diseaseTypes) for _ in range(len(self.grid.internal_grid))]
        self.gridSize = len(self.grid.internal_grid)
        self.bobby = persons[0]
        self.lastUpdate = -1
        self.travel = transport.Travel(persons, trafficNetwork)
        self.travelDatas = travelDatas
        for i in range(len(self.travelDatas)):
            self.travelDatas[i] = transport.TravelData(-1,-1, self.persons[i].currentPosition, self.grid.get(0,0), 0, False)

        self.diseaseTypes = diseaseTypes

        self.travelMap = {}
        for con in trafficNetwork.connections:
            self.travelMap[(trafficNetwork.stops[con[0]].index, trafficNetwork.stops[con[1]].index) ] = PlaceMapObject(diseaseTypes)
            self.travelMap[(trafficNetwork.stops[con[1]].index, trafficNetwork.stops[con[0]].index) ] = PlaceMapObject(diseaseTypes)

        for disease in self.bobby.diseases.values():
            disease.infect(time.Timestamp(-3 * time.DAY))

        for thePerson in self.persons:
            self.plan(thePerson)

    def simulate(self):
        self.now.minute += SIMULATION_TICK_LENGTH
        nownow = self.now.now()

        self.lastUpdate = self.now.minute

        logging.write("bobby", self.now.now(), self.bobby.task.activity.getName())

        bobby_needs = {"TRAVEL_PUBLIC": 0, "TRAVEL_PRIVATE": 0}
        if self.travel.isTravelling(self.bobby, self.now.now()):
            if self.travel.travellers[self.bobby][0].isPublic:
                bobby_needs["TRAVEL_PUBLIC"] = 1
            else:
                bobby_needs["TRAVEL_PRIVATE"] = 1

        persons_at_place = { "TRAVEL_PRIVATE": 0, "TRAVEL_PUBLIC": 0 }
        persons_per_need = { "TRAVEL_PRIVATE": 0, "TRAVEL_PUBLIC": 0 }

        for needType in self.bobby.needs:
            persons_per_need[needType] = 0
            bobby_needs[needType] = self.bobby.needs[needType]

        for subType in place_characteristics.SubType:
            persons_at_place[subType] = 0

        logging.write("bobby_needs", self.now.minute, *(bobby_needs.values()))

        travel_map = {}
        
        for (i, thePerson) in enumerate(self.persons):
            if nownow >= thePerson.task.stop:
                self.plan(thePerson)
                thePerson.behaviour.updateNeeds(thePerson)

            travelData = self.travel.updatePerson(thePerson, nownow)
            if travelData is not None:
                if not travelData.isPublic:
                    persons_per_need["TRAVEL_PRIVATE"] += 1
                    persons_at_place["TRAVEL_PRIVATE"] += 1
                else:
                    persons_per_need["TRAVEL_PUBLIC"] += 1
                    persons_at_place["TRAVEL_PUBLIC"] += 1
                thePerson.currentDestination = travelData.destination
                if travelData.isPublic:
                    self.appendTravelMap(thePerson, travelData, nownow)
                self.travelDatas[i] = travelData
            else: 
                thePerson.currentPosition = thePerson.currentDestination
                self.appendPlaceMap(thePerson, nownow)
                persons_per_need[thePerson.task.activity] += 1
                persons_at_place[thePerson.task.place.char.subType] += 1
            
            for diseaseType in self.diseaseTypes:
                diseaseType.update(self.now, thePerson)

        for diseaseType in self.diseaseTypes:
            #Simulate the diseaseType
            self.simulatePlaceContacts(diseaseType, nownow)
            self.simulateTravelContacts(diseaseType, nownow)
            #Log the diseaseType
            numInfected = sum(1 if p.diseases[diseaseType].isInfected else 0 for p in self.persons)
            numContagious = sum(1 if p.diseases[diseaseType].isContagious() else 0 for p in self.persons)
            numImmune = sum(1 if p.diseases[diseaseType].isImmune else 0 for p in self.persons)
            print(diseaseType.getName(), numInfected, numContagious, numImmune)
            logging.write("disease." + diseaseType.getName(), self.now.minute, numInfected, numContagious, numImmune)
        logging.write("activity", self.now.minute, *(persons_per_need.values()))
        logging.write("places", self.now.minute, *(persons_at_place.values()))

    #Plan the schedule of a person
    def plan(self, person):
        for need in person.behaviour.getNeedPrio(person):
            task = need.trySatisfy(person, person.needs[need], self.now)
            if task is not None:
                person.task = task
                self.travel.setDestination(person, task.place, task.start+1, self.now.now())
                return

    def simulateTravelContacts(self, diseaseType, nownow):
        for ind in filter(lambda ind: self.travelMap[ind].diseases[diseaseType] > 0 and self.travelMap[ind].updated == nownow, self.travelMap):
            mo = self.travelMap[ind]
            cp = disease.ContactProperties(0.5, 90)
            for thePerson in mo.persons:
                disease.simulateContact(self.now, diseaseType, mo.persons, thePerson, cp, "PUBLIC_TRANSPORT", SIMULATION_TICK_LENGTH) 

    def simulatePlaceContacts(self, diseaseType, nownow):
        for thePlace in filter(lambda thePlace: self.placeMap[thePlace.index].diseases[diseaseType] > 0 and self.placeMap[thePlace.index].updated == nownow, self.grid.internal_grid):
            for thePerson in self.placeMap[thePlace.index].persons:
                disease.simulateContact(self.now, diseaseType, self.placeMap[thePlace.index].persons, thePerson, thePlace.char.contactProperties, thePlace.char.subType.name, SIMULATION_TICK_LENGTH)

    def appendPlaceMap(self, thePerson, nownow) -> None: 
        thePlace = thePerson.task.place
        if self.placeMap[thePlace.index].updated < nownow:
            for diseaseType in self.diseaseTypes:
                self.placeMap[thePlace.index].diseases[diseaseType] = 1 if thePerson.diseases[diseaseType].isContagious() else 0
            self.placeMap[thePlace.index].persons.clear()
            self.placeMap[thePlace.index].updated = nownow
        else:
            for diseaseType in self.diseaseTypes:
                if thePerson.diseases[diseaseType].isContagious():
                    self.placeMap[thePlace.index].diseases[diseaseType] += 1
        self.placeMap[thePlace.index].persons.append(thePerson)

    def appendTravelMap(self, thePerson, travelData, nownow):
        ind = (travelData.origin.index, travelData.destination.index)
        if self.travelMap[ind].updated < nownow:
            for diseaseType in self.diseaseTypes:
                self.travelMap[ind].diseases[diseaseType] = 1 if thePerson.diseases[diseaseType].isContagious() else 0
            self.travelMap[ind].persons.clear()
            self.travelMap[ind].updated = nownow
        else:
            for diseaseType in self.diseaseTypes:
                if thePerson.diseases[diseaseType].isContagious():
                    self.travelMap[ind].diseases[diseaseType] += 1
        self.travelMap[ind].persons.append(thePerson)
 
        



