from model import mass_transportation as mt


def generate(grid, step, frequency):
    stops = []
    connections = []
    for x in range(grid.size, step=step):
        for y in range(grid.size, step=step):
            stops.append((x,y))
            if x > 0:
                connections.append(len(stops)-1, len(stops)-1 - grid.size//step, 1)
            if y > 0:
                connections.append(len(stops)-1, len(stops)-2, 1)
    return mt.TrafficNetwork(stops, connections, grid, frequency) 
