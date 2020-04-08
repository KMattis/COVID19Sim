from model import mass_transportation as mt
from model.place_characteristics import PlaceType


def generate(grid, step, frequency):
    stops = []
    connections = []
    for x in range(0, grid.size, step):
        for y in range(0, grid.size, step):
            place = grid.get(x,y)
            if place.char.placeType is not PlaceType.NONE:
                stops.append(grid.get(x,y))
                if x > 0:
                    connections.append((len(stops)-1, len(stops)-1 - grid.size//step, 1))
                if y > 0:
                    connections.append((len(stops)-1, len(stops)-2, 1))
    return mt.TrafficNetwork(stops, connections, grid, frequency, 10) 
