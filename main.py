import time
import configparser

import generation.grid_generator, generation.person_generator
from rendering.renderer import Renderer
from simulation.simulation import Simulation

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

while running:
    now = getCurrentTimeMillis()
    deltaTime = now - lastUpdate
    lastUpdate = now

    running = theRenderer.fetchEvents(deltaTime)

    theRenderer.render(persons, deltaTime, theSimulation.now)
    theSimulation.simulate(deltaTime)

theRenderer.quit()
