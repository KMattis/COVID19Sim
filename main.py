import time
import configparser

import generation.grid_generator, generation.person_generator
from rendering.renderer import Renderer
from simulation.simulation import Simulation
from profiler.profiler import Profiler

def getCurrentTimeMillis():
    return round(time.time() * 1000)

config = configparser.ConfigParser()
config.read("config.ini")

theGrid = generation.grid_generator.generate(int(config["default"]["gridSize"]))
persons = generation.person_generator.generate(theGrid, int(config["default"]["numPersons"]))

theRenderer = Renderer()
theRenderer.initPlaceBuffer(theGrid)

theSimulation = Simulation(persons)

lastUpdate = getCurrentTimeMillis()
running = True

profiler = Profiler()
loops = 0


while running:
    profiler.startProfiling("covid")
    now = getCurrentTimeMillis()
    deltaTime = now - lastUpdate
    lastUpdate = now



    profiler.startProfiling("fetchEvents")
    running = theRenderer.fetchEvents(deltaTime)
    profiler.stopStartProfiling("render")
    theRenderer.render(persons, deltaTime, theSimulation.now, profiler)
    profiler.stopStartProfiling("simulation")
    theSimulation.simulate(deltaTime)
    profiler.stopProfiling()

    profiler.stopProfiling() #covid
    loops += 1
    if loops % 100 == 0:
        profiler.printPercentages("covid")
        profiler.reset()

theRenderer.quit()
