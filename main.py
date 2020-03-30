import time
import configparser

import generation.grid_generator, generation.person_generator
from rendering.renderer import Renderer
from simulation.simulation import Simulation
from profiler.profiler import profilerObj

MINUTES_PER_REAL_SECOND = 100

def getCurrentTimeMillis():
    return round(time.time() * 1000)

with open("logfiles/activity.log", "w") as f:
    pass

config = configparser.ConfigParser()
config.read("config.ini")

theGrid = generation.grid_generator.generate(int(config["default"]["gridSize"]))
persons = generation.person_generator.generate(theGrid, int(config["default"]["numPersons"]))

theRenderer = Renderer(len(persons))
theRenderer.initPlaceBuffer(theGrid)

theSimulation = Simulation(persons, theGrid)

lastUpdate = getCurrentTimeMillis()
running = True

loops = 0

while running:
    profilerObj.startProfiling("covid")
    now = getCurrentTimeMillis()
    deltaTime = now - lastUpdate

    profilerObj.startProfiling("fetchEvents")
    running = theRenderer.fetchEvents(deltaTime)
    profilerObj.stopStartProfiling("render")
    theRenderer.render(persons, deltaTime, theSimulation.now)
    profilerObj.stopStartProfiling("simulation")

    for i in range(int(deltaTime / 1000 * MINUTES_PER_REAL_SECOND)):
        theSimulation.simulate(theGrid)
        lastUpdate = getCurrentTimeMillis()
    profilerObj.stopProfiling()

    profilerObj.stopProfiling() #covid
    loops += 1
    if loops % 100 == 0:
        profilerObj.printPercentages("covid")
        profilerObj.reset()

theRenderer.quit()
