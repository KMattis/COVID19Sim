import time
import configparser
import argparse

import importlib.util
import inspect

import generation.grid_generator, generation.person_generator, generation.need_parser
from rendering.renderer import Renderer
from simulation.simulation import Simulation
from profiler.profiler import profilerObj
from plotting import logging


#Setup argparse
argparser: argparse.ArgumentParser = argparse.ArgumentParser()
argparser.add_argument("--no-render", dest="noRender", action='store_const', const=True)
argparser.add_argument("--config-file", dest="configFile", type=str, default="simconfig/config.ini")
argparser.add_argument("--need-types-file", dest="needTypesFile", type=str, default="simconfig/need_types.py")
args = argparser.parse_args()

MINUTES_PER_REAL_SECOND = 100

def getCurrentTimeMillis():
    return round(time.time() * 1000)

logging.registerCategory("activity")
logging.registerCategory("bobby")
logging.registerCategory("output")

config = configparser.ConfigParser()
config.read(args.configFile)

logging.write("output", "generating")
needTypes = generation.need_parser.readNeedTypes(args.needTypesFile)
theGrid = generation.grid_generator.generate(int(config["default"]["gridSize"]), needTypes)
persons = generation.person_generator.generate(theGrid, int(config["default"]["numPersons"]), needTypes)

for needType in needTypes:
    needType.initialize(persons, theGrid)

personScriptName = config["default"]["personScript"]
spec = importlib.util.spec_from_file_location("person_script", personScriptName)
personScriptModule = importlib.util.module_from_spec(spec)
spec.loader.exec_module(personScriptModule)
members = dict((name, func) for name, func in inspect.getmembers(personScriptModule))
initializePersonScript = members["initialize"]
getNeedPrio = members["getNeedPrio"]
updateNeeds = members["updateNeeds"]

if not args.noRender:
    theRenderer = Renderer(len(persons))
    theRenderer.initPlaceBuffer(theGrid)

initializePersonScript(needTypes)
theSimulation = Simulation(persons, getNeedPrio, updateNeeds)

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
        theSimulation.simulate()
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
