from model import transport
from model.place_characteristics import PlaceType


def generate(grid, stepX, stepY, privateSpeed, publicSpeed, frequency):
    stops = []
    connections = []
    for x in range(0, grid.size, stepX):
        for y in range(0, grid.size, stepY):
            place = grid.get(x,y)
            stops.append(grid.get(x,y))
            if x > 0:
                connections.append((len(stops)-1-grid.size//stepY, len(stops)-1, 1))
            if y > 0:
                connections.append((len(stops)-1, len(stops)-2, 1))
    return transport.TrafficNetwork(stops, connections, grid, frequency, privateSpeed, publicSpeed) 
