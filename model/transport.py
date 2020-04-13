import ctypes
import math
import networkx as nx
from simulation import time
from model import disease

class TrafficNetwork:
    def __init__(self, stops, connections, grid, frequency, privateTransportSpeed, publicTransportSpeed):
        self.stops = stops #List of grid coordinates
        self.connections = connections #List of tuples (index, index1, weight)
        self.frequency = frequency
        self.privateTransportSpeed = privateTransportSpeed
        self.publicTransportSpeed = publicTransportSpeed
        self.grid_size = grid.size
        self.G = nx.Graph() #Works on indices
        self.createGraph()
        self.stopDists = {}
        self.shortestConnections = {}
        self.calculateStopDistances()
        self.calculateShortestPaths()
        self.distMap = [None] * grid.size**2
        self.createDistMap()
        
    def createGraph(self):
        self.G.clear()
        self.G.add_nodes_from(list(range(len(self.stops))))
        self.G.add_weighted_edges_from(self.connections)

    #TODO: Wastes space
    def calculateStopDistances(self):
        for stop0 in enumerate(self.stops):
            self.stopDists[stop0[0]] = {}
            for stop1 in enumerate(self.stops):
                dist = math.sqrt((stop0[1].x-stop1[1].x)**2 + (stop0[1].y-stop1[1].y)**2)
                timeDist = dist//self.publicTransportSpeed
                self.stopDists[stop0[0]][stop1[0]] = (dist, timeDist)
      
    def calculateShortestPaths(self):
        shortestConnections = nx.shortest_path(self.G, weight='weight')
        for con0 in shortestConnections:
            self.shortestConnections[con0] = {}
            for con1 in shortestConnections[con0]: 
                lastStop = self.stops[shortestConnections[con0][con1][0]]
                #TODO Use stop distsances which have already been calculated
                dist = 0
                timeDist = 0
                for i in range(1, len(shortestConnections[con0][con1])):
                    thisStop = self.stops[shortestConnections[con0][con1][i]]
                    dist += math.sqrt((thisStop.x - lastStop.x)**2 + (thisStop.y - lastStop.y)**2)
                    timeDist += dist//self.publicTransportSpeed
                    lastStop = thisStop
                self.shortestConnections[con0][con1] = MTRoute(shortestConnections[con0][con1], dist, timeDist)
    
    def findNearestStop(self, x, y):
        curDist = (None, -1);
        for stop in enumerate(self.stops):
            dist = math.sqrt((stop[1].x - x) ** 2 + (stop[1].y -y) **2)
            if dist < curDist[1] or curDist[1] == -1:
                timeDist = dist //self.publicTransportSpeed
                curDist = (stop[0], dist, timeDist)
        return curDist
        
    def createDistMap(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
               self.distMap[x + y*self.grid_size] = self.findNearestStop(x,y) 

    def getNearestStop(self, x, y):
        return self.distMap[x+ y * self.grid_size]
    
    def getDistStops(self, index0, index1):
        return self.shortestConnections[index0][index1] 

class MTRoute:
    def __init__(self, stopIndices, dist, timeDist):
        self.stopIndices = stopIndices
        self.dist = dist
        self.timeDist = timeDist


class TravelData(ctypes.Structure):
    _fields_ = [('startTime', ctypes.c_int32), ('endTime', ctypes.c_int32), ('origin_x', ctypes.c_int32), ('origin_y', ctypes.c_int32), ('destination_x', ctypes.c_int32), ('destination_y', ctypes.c_int32), ('distance', ctypes.c_float), ('isPublic', ctypes.c_bool), ('isInvalid', ctypes.c_bool)] 
    def __init__(self, startTime, endTime, origin, destination, distance, isPublic):
        self.startTime = int(startTime)
        self.endTime = int(endTime)
        self.origin = origin
        self.destination = destination 
        self.distance = distance
        self.isPublic = isPublic
        
        self.isInvalid = False
        self.origin_x = origin.x
        self.origin_y = origin.y
        self.destination_x = destination.x
        self.destination_y = destination.y
        

    def __str__(self):
        return str(self.startTime) + " " + str(self.endTime) + " " + str(self.destination.x) + " " + str(self.destination.y) + " " + str(self.distance) + " " + str(self.isPublic)

                
#Holds all travelling persons, sets their positions, and calculates infection risks
class Travel:
    def __init__(self, persons, trafficNetwork):
        self.travellers = {person: [] for person in persons}
        #person: List[TravelData]
        self.trafficNetwork = trafficNetwork
        self.infectionMap = [({connection: [] for connection in trafficNetwork.connections})]
        
 
    #TODO: Include some average waiting time
    def findRoute(self, person, destination):
        distDirect = math.sqrt((person.currentPosition.x - destination.x) ** 2) + math.sqrt((person.currentPosition.y - destination.y)**2)
        startStation = self.trafficNetwork.getNearestStop(person.currentPosition.x, person.currentPosition.y)
        endStation = self.trafficNetwork.getNearestStop(destination.x, destination.y)
        publicRoute = self.trafficNetwork.getDistStops(startStation[0], endStation[0])
        distPublic = publicRoute.dist + startStation[2] + endStation[2]
        if (len(publicRoute.stopIndices) < 2):
            return None
        return (startStation, publicRoute, endStation) if distPublic <= person.behaviour.getPublicTransportAffinity()*distDirect//self.trafficNetwork.privateTransportSpeed else None
    
    #TODO: Cache travels (save travel datas once calculated)
    #TODO: Long routes should one TravelData!
    def setDestination (self, person, destination, start, nownow):
        route = self.findRoute(person, destination)
        if route is not None: #Public travel
            fr = self.trafficNetwork.frequency
            startTime = start
            endTime = start+route[0][2]
            destinations = []
            if route[0][1] > 0:
                destinations = [TravelData(startTime, endTime, person.currentPosition, self.trafficNetwork.stops[route[0][0]], route[0][1], False)]
            lastStop = self.trafficNetwork.stops[route[0][0]]
            lastStopIndex = route[0][0]
            for stopIndex in route[1].stopIndices:
                startTime = endTime + self.trafficNetwork.frequency - endTime % self.trafficNetwork.frequency
                endTime = startTime + self.trafficNetwork.stopDists[lastStopIndex][stopIndex][1]
                destinations.append(TravelData(startTime, endTime, lastStop, self.trafficNetwork.stops[stopIndex], self.trafficNetwork.stopDists[lastStopIndex][stopIndex][0], True))
                lastStop = self.trafficNetwork.stops[stopIndex] 
                lastStopIndex = stopIndex
            if route[2][1] > 0:
                destinations.append(TravelData(endTime, endTime+route[2][2], lastStop, self.trafficNetwork.stops[route[2][0]], route[2][1], False))
            self.travellers[person] += destinations
        else:
            dist = math.sqrt((person.currentPosition.x - destination.x)**2 + (person.currentPosition.y - destination.y) **2)
            if dist > 0:
                self.travellers[person] += [TravelData(start, start+(dist//self.trafficNetwork.privateTransportSpeed), person.currentPosition, destination, dist, False)]

    def isMoving(self, person, nownow):
        return len(self.travellers[person]) > 0 and  self.travellers[person][0].startTime <= nownow <= self.travellers[person][0].endTime
        
    def isTravelling(self, person, nownow):
        if len(self.travellers[person]) > 0 and self.travellers[person][0].isPublic:
            curTravel = self.travellers[person][0]
            return curTravel.startTime <= nownow+self.trafficNetwork.frequency and nownow <= curTravel.endTime
        return len(self.travellers[person]) > 0 and  self.travellers[person][0].startTime <= nownow <= self.travellers[person][0].endTime

    def updatePerson(self, person, nownow):
        i = 0
        for td in self.travellers[person]:
            if td.endTime < nownow:
                i += 1
                continue
            self.travellers[person] = self.travellers[person][i:]
            if td.startTime > nownow and not (td.isPublic and td.startTime < nownow + self.trafficNetwork.frequency):
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
        



