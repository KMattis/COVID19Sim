import networkx as nx
import math
from simulation import time

class TrafficNetwork:
    def __init__(self, stops, connections, grid, frequency, distStations):
        self.stops = stops #List of grid coordinates
        self.connections = connections #List of tuples (index, index1, weight)
        self.frequency = frequency
        self.grid_size = grid.size
        self.G = nx.Graph() #Works on indices
        self.createGraph()
        self.shortestConnections = {}
        self.calculateShortestPaths()
        self.distMap = [None] * grid.size**2
        self.createDistMap()
        self.distStations = distStations
        
    def createGraph(self):
        self.G.clear()
        self.G.add_nodes_from(list(range(len(self.stops))))
        self.G.add_weighted_edges_from(self.connections)
      
    #TODO weights?
    def calculateShortestPaths(self):
        self.shortestConnections = nx.shortest_path(self.G,weight='weight')
    
    def findNearestStop(self, x, y):
        curDist = (None, -1);
        for stop in enumerate(self.stops):
            dist = math.sqrt((stop[1].x - x) ** 2 + (stop[1].y -y) **2)
            if dist < curDist[1] or curDist[1] == -1:
                curDist = (stop[0], dist)
        return curDist
        
    def createDistMap(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
               self.distMap[x + y*self.grid_size] = self.findNearestStop(x,y) 

    def getNearestStop(self, x, y):
        return self.distMap[x+ y * self.grid_size]
    
    def getDistStops(self, index0, index1):
        return self.shortestConnections[index0][index1] 

    def getLenRoute(self, route):
        return len(route)*self.distStations

class TravelData:
    def __init__(self, startTime, endTime, destination, distance, isPublic):
        self.startTime = startTime
        self.endTime = endTime
        self.destination = destination 
        self.distance = distance
        self.isPublic = isPublic

    def __str__(self):
        return str(self.startTime) + " " + str(self.endTime) + " " + str(self.destination.x) + " " + str(self.destination.y) + " " + str(self.distance) + " " + str(self.isPublic)

                
#Holds all travelling persons, sets their positions, and calculates infection risks
class Travel:
    def __init__(self, persons, trafficNetwork, walkingSpeed, pubSpeed):
        self.travellers = {person: [] for person in persons}
        #person: List[TravelData]
        self.trafficNetwork = trafficNetwork
        self.walkingSpeed = walkingSpeed
        self.pubSpeed = pubSpeed
        self.infectionMap = [({connection: [] for connection in trafficNetwork.connections})]
        self.timeBetweenStops = self.trafficNetwork.distStations//self.pubSpeed
        
 
    #TODO: Give persons a factor which influences this decision
    def findRoute(self, person, destination):
        distDirect = math.sqrt((person.currentPosition.x - destination.x) ** 2) + math.sqrt((person.currentPosition.y - destination.y)**2)
        startStation = self.trafficNetwork.getNearestStop(person.currentPosition.x, person.currentPosition.y)
        endStation = self.trafficNetwork.getNearestStop(destination.x, destination.y)
        publicRoute = self.trafficNetwork.getDistStops(startStation[0], endStation[0])  
        distPublic = self.trafficNetwork.getLenRoute(publicRoute)//self.pubSpeed + startStation[1] + endStation[1]
        return (startStation, publicRoute, endStation) if distPublic < distDirect else None
    
    def setDestination (self, person, destination, start, nownow):
        route = self.findRoute(person, destination)
        if route is not None: #Public travel
            fr = self.trafficNetwork.frequency
            tbs = self.timeBetweenStops
            startTime = start
            endTime = start+route[0][1]//self.walkingSpeed
            destinations = []
            if route[0][1] > 0:
                destinations = [TravelData(startTime, endTime, self.trafficNetwork.stops[route[0][0]], route[0][1], False)]
            for stopIndex in route[1]:
                startTime = endTime
                endTime = startTime + tbs
                destinations.append(TravelData(startTime, endTime, self.trafficNetwork.stops[stopIndex], tbs, True))
            if route[2][1] > 0:
                destinations.append(TravelData(endTime, endTime+route[2][1]//self.walkingSpeed, self.trafficNetwork.stops[route[2][0]], route[2][1], False))
            self.travellers[person] += destinations
        else:
            dist = math.sqrt((person.currentPosition.x - destination.x)**2 + (person.currentPosition.y - destination.y) **2)
            if dist > 0:
                self.travellers[person] += [TravelData(start, start+(dist//self.walkingSpeed), destination, dist, False)]
        
    def isTravelling(self, person, nownow):
        return len(self.travellers[person]) > 0 and  self.travellers[person][0].startTime <= nownow <= self.travellers[person][0].endTime

    def updatePerson(self, person, nownow):
        i = 0
        for td in self.travellers[person]:
            if td.endTime < nownow:
                i += 1
                continue
            self.travellers[person] = self.travellers[person][i:]
            if td.startTime > nownow: 
                break
            #We now have the current travelData  
            #Remove old travel data
            if len(self.travellers[person]) == 0: 
                break
            travelData = self.travellers[person][0] 
            return travelData  
        #Current travel is not active
        if i == len(self.travellers[person]):
            self.travellers[person] = []
        return None
        



