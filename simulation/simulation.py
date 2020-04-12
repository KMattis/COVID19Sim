from simulation import random

from plotting import logging

from model import place, person, place_characteristics, disease, transport
from simulation import time, math

from profiler.profiler import profilerObj

SIMULATION_TICK_LENGTH = 1* time.MINUTE

class Simulation:
    def __init__(self, persons, grid, diseaseTypes, trafficNetwork, travelDatas):
        self.now = time.Timestamp(time.HOUR * 0)
        self.persons = persons
        self.bobby = persons[0]
        self.grid = grid
        self.lastUpdate = -1
        self.travel = transport.Travel(persons, trafficNetwork)
        self.travelDatas = travelDatas
        

        self.diseaseTypes = diseaseTypes

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

        place_map = {}
        travel_map = {}
        travelData_none = transport.TravelData(-1,-1, self.grid.get(0,0), self.grid.get(0,0), 0, False)
        for i in range(len(self.travelDatas)):
            self.travelDatas[i] = transport.TravelData(-1,-1, self.persons[i].currentPosition, self.grid.get(0,0), 0, False)
        transport.TravelData
        travelData_none.isInvalid = True
        
        for (i, thePerson) in enumerate(self.persons):
            if self.now.now() >= thePerson.task.stop:
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
                self.appendTravelMap(travel_map, thePerson, travelData)
                self.travelDatas[i] = travelData
            else: 
                thePerson.currentPosition = thePerson.currentDestination
                self.appendPlaceMap(place_map, thePerson)
                persons_per_need[thePerson.task.activity] += 1
                persons_at_place[thePerson.task.place.char.subType] += 1
           # thePerson.travelData = travelData 
            
            for diseaseType in self.diseaseTypes:
                diseaseType.update(self.now, thePerson)

        for diseaseType in self.diseaseTypes:
            #Simulate the diseaseType
            for thePlace in filter(lambda thePlace: place_map[thePlace][1][diseaseType] > 0, place_map):
                for thePerson in place_map[thePlace][0]:
                    disease.simulateContact(self.now, diseaseType, place_map[thePlace][0], thePerson, thePlace.char.contactProperties, thePlace.char.subType.name, SIMULATION_TICK_LENGTH)
            for con in filter(lambda con: travel_map[con][1][diseaseType] > 0, travel_map):
                cp = disease.ContactProperties(0.5, 90)
                for thePerson in travel_map[con][0]:
                    disease.simulateContact(self.now, diseaseType, travel_map[con][0], thePerson, cp, "PUBLIC_TRANSPORT", SIMULATION_TICK_LENGTH) 

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

    def appendPlaceMap(self, place_map, thePerson) -> None: 
        thePlace = thePerson.task.place
        if not thePlace in place_map:
            contagiousDict = {}
            for diseaseType in self.diseaseTypes:
                contagiousDict[diseaseType] = 1 if thePerson.diseases[diseaseType].isContagious() else 0
            place_map[thePlace] = [[thePerson], contagiousDict] 
        else:
            for diseaseType in self.diseaseTypes:
                if thePerson.diseases[diseaseType].isContagious():
                    place_map[thePlace][1][diseaseType] += 1
            place_map[thePlace][0].append(thePerson)

    def appendTravelMap(self, travel_map, thePerson, travelData):
        con = (travelData.origin, travelData.destination)
        if not con in travel_map:
            contagiousDict = {}
            for diseaseType in self.diseaseTypes:
                contagiousDict[diseaseType] = 1 if thePerson.diseases[diseaseType].isContagious() else 0
            travel_map[con] = [[thePerson], contagiousDict] 
        else:
            for diseaseType in self.diseaseTypes:
                if thePerson.diseases[diseaseType].isContagious():
                    travel_map[con][1][diseaseType] += 1
            travel_map[con][0].append(thePerson)
            
        



