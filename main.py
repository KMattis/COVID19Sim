import time
import configparser

import generation.grid_generator, generation.person_generator
from rendering.renderer import Renderer
from simulation.simulation import Simulation
from profiler.profiler import profilerObj
from plotting import logging

MINUTES_PER_REAL_SECOND = 100

def getCurrentTimeMillis():
    return round(time.time() * 1000)

logging.registerCategory("activity")
logging.registerCategory("output")

config = configparser.ConfigParser()
config.read("simconfig/config.ini")

logging.write("output", "generating the grid")
theGrid = generation.grid_generator.generate(int(config["default"]["gridSize"]))

logging.write("output", "generating the persons")
persons = generation.person_generator.generate(theGrid, int(config["default"]["numPersons"]))

theRenderer = Renderer(len(persons))
theRenderer.initPlaceBuffer(theGrid)

theSimulation = Simulation(persons, theGrid)

lastUpdate = getCurrentTimeMillis()
running = True

loops = 0

logging.write("output", "starting main loop")
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

logging.write("output", "shutting down")
theRenderer.quit()
