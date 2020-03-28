import time
import configparser

import generation.grid_generator, generation.person_generator
from rendering.renderer import Renderer
from simulation.simulation import Simulation
from profiler.profiler import profilerObj

def getCurrentTimeMillis():
    return round(time.time() * 1000)

config = configparser.ConfigParser()
config.read("config.ini")

theGrid = generation.grid_generator.generate(int(config["default"]["gridSize"]))
persons = generation.person_generator.generate(theGrid, int(config["default"]["numPersons"]))

theRenderer = Renderer(len(persons))
theRenderer.initPlaceBuffer(theGrid)

theSimulation = Simulation(persons)

lastUpdate = getCurrentTimeMillis()
running = True

loops = 0


while running:
    profilerObj.startProfiling("covid")
    now = getCurrentTimeMillis()
    deltaTime = now - lastUpdate
    lastUpdate = now



    profilerObj.startProfiling("fetchEvents")
    running = theRenderer.fetchEvents(deltaTime)
    profilerObj.stopStartProfiling("render")
    theRenderer.render(persons, deltaTime, theSimulation.now)
    profilerObj.stopStartProfiling("simulation")
    theSimulation.simulate(deltaTime)
    profilerObj.stopProfiling()

    profilerObj.stopProfiling() #covid
    loops += 1
    if loops % 100 == 0:
        profilerObj.printPercentages("covid")
        profilerObj.reset()

theRenderer.quit()
