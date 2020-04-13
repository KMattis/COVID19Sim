import math

from model import transport

def generate(grid, step, numLines, privateSpeed, publicSpeed, frequency):
    stops = []
    connections = []

    #Generate radial public transport lines
    centerX = grid.size // 2
    centerY = grid.size // 2
    stops.append(grid.get(centerX, centerY))
    for i in range(numLines):
        angle = i * 2 * math.pi / numLines
        for i in range(1, grid.size // (2 * step)):
            x = round(centerX + math.cos(angle) * (i * step))
            y = round(centerY + math.sin(angle) * (i * step))
            stops.append(grid.get(x, y))
            if i == 1:
                connections.append((len(stops)-1, 0, 1))
            else:
                connections.append((len(stops)-1, len(stops)-2, 1))

    #Old square grid
    #for x in range(0, grid.size, stepX):
    #    for y in range(0, grid.size, stepY):
    #        place = grid.get(x,y)
    #        stops.append(grid.get(x,y))
    #        if x > 0:
    #            connections.append((len(stops)-1-grid.size//stepY, len(stops)-1, 1))
    #        if y > 0:
    #            connections.append((len(stops)-1, len(stops)-2, 1))
    return transport.TrafficNetwork(stops, connections, grid, frequency, privateSpeed, publicSpeed) 
