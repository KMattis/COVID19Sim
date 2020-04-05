import networkx as nx

class TrafficNetwork:
    def __init__(self, stops, connections, grid, frequency):
        self.stops = stops #List of grid coordinates
        self.connections = connections #List of tuples (index, index1, weight)
        self.frequency = frequency
        self.G = nx.Graph() #Works on indices
        self.createGraph()
        self.shortestConnections = {}
        self.distMap = []
        self.createDistMap(grid)
        
    def createGraph(self):
        self.G.clear()
        self.G.add_nodes_from(list(range(len(self.stops))))
        self.G.add_weighted_edges_from(self.connections)
      
    def calculateShortestPaths(self):
        for stop in self.stops:
            self.shortestConnections[stop] = self.G.all_shortest_paths(G, source=stop, weight='weight')
    
    def findNearestStop(self, x, y):
        curDist = (None, -1);
        for stop in enumerate(self.stops):
            dist = (stop[1][0] - x) ** 2 + (stop[1][1] -y) **2
            if dist < curDist[1] or curDist[1] == -1:
                curDist = (stop[0], dist)
        return curDist
        
    def createDistMap(self, grid):
        for x in range(grid.size):
            for y in range(grid.size):
               self.distMap[x + y*grid.size] = self.findNearestStop(x,y) 

    def getNearestStop(self, x, y):
        return self.distMap[x+ y * grid.size] 
                
class Travel:
    def __init__(self):
        pass
