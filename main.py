import time
import configparser
import argparse

import generation.grid_generator, generation.person_generator, generation.need_parser
from rendering.renderer import Renderer
from simulation.simulation import Simulation
from profiler.profiler import profilerObj
from plotting import logging


#Setup argparse
argparser: argparse.ArgumentParser = argparse.ArgumentParser()
argparser.add_argument("--no-render", dest="noRender", action='store_const', const=True)
args = argparser.parse_args()

MINUTES_PER_REAL_SECOND = 100

def getCurrentTimeMillis():
    return round(time.time() * 1000)

logging.registerCategory("activity")
logging.registerCategory("output")

config = configparser.ConfigParser()
config.read("simconfig/config.ini")

logging.write("output", "generating")
needTypes = generation.need_parser.readNeedTypes("simconfig/need_types.py")
theGrid = generation.grid_generator.generate(int(config["default"]["gridSize"]), needTypes)
persons = generation.person_generator.generate(theGrid, int(config["default"]["numPersons"]), needTypes)

for needType in needTypes:
    needType.initialize(persons, theGrid)

if not args.noRender:
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

    if not args.noRender:
        profilerObj.startProfiling("fetchEvents")
        running = theRenderer.fetchEvents(deltaTime)
        profilerObj.stopStartProfiling("render")
        theRenderer.render(persons, deltaTime, theSimulation.now)
        profilerObj.stopProfiling()
            
    profilerObj.startProfiling("simulation")

    for i in range(max(1, int(deltaTime / 1000 * MINUTES_PER_REAL_SECOND))):
        theSimulation.simulate(theGrid)
        lastUpdate = getCurrentTimeMillis()
    profilerObj.stopProfiling()

    profilerObj.stopProfiling() #covid
    loops += 1
    if loops % 100 == 0:
        now = theSimulation.now
        print("Simulation time: {0}:{1}:{2}".format(now.day(), now.hourOfDay(), now.minuteOfHour()))
        profilerObj.printPercentages("covid")
        profilerObj.reset()

logging.write("output", "shutting down")

if not args.noRender:
    theRenderer.quit()
