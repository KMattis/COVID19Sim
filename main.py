import time as pytime
import configparser
import argparse

from multiprocessing import Process, Manager, Value

import importlib.util
import inspect

import generation.grid_generator, generation.person_generator, generation.need_parser
from rendering.renderer import Renderer
from simulation.simulation import Simulation
from simulation import time
from profiler.profiler import profilerObj
from plotting import logging

MINUTES_PER_REAL_SECOND = 1000

killSimulationLoop = False

def readArguments():
    #Setup argparse
    argparser: argparse.ArgumentParser = argparse.ArgumentParser()
    argparser.add_argument("--no-render", dest="noRender", action='store_const', const=True)
    argparser.add_argument("--config-file", dest="configFile", type=str, default="simconfig/config.ini")
    argparser.add_argument("--need-types-file", dest="needTypesFile", type=str, default="simconfig/need_types.py")
    argparser.add_argument("--num-days", dest="numDays", type=int, default=0)
    return argparser.parse_args()

def getCurrentTimeMillis():
    return round(pytime.time() * 1000)

def registerLoggingCategories():
    logging.registerCategory("activity")
    logging.registerCategory("bobby")
    logging.registerCategory("output")
    logging.registerCategory("bobby_needs")

def loadPersonScripts(config):
    personScriptName = config["default"]["personScript"]
    spec = importlib.util.spec_from_file_location("person_script", personScriptName)
    personScriptModule = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(personScriptModule)
    members = dict((name, func) for name, func in inspect.getmembers(personScriptModule))
    return members["initialize"], members["getNeedPrio"], members["updateNeeds"]

def main():
    args = readArguments()
    registerLoggingCategories()

    lastUpdate = getCurrentTimeMillis()
    running = True
    loops = 0

    logging.write("output", "starting main loop")
    ########
    queue = Manager().Queue()
    killSim = Value('i', 0)
    simProcess = Process(target=simLoop, args=(queue, killSim,))
    simProcess.start()

    initialData = queue.get(block=True)
    if not args.noRender:
        numPersons = initialData[0]
        gridSize = initialData[1]
        gridData = initialData[2]
        theRenderer = Renderer(numPersons)
        theRenderer.initPlaceBuffer(gridSize, gridData)

    simData = queue.get(block=True)
    simPersons = simData[1]
    simNow = simData[0]
    nowOb = time.Timestamp(simNow)
    ########

    while running:
        now = getCurrentTimeMillis()
        deltaTime = now - lastUpdate

        if not args.noRender:
            running = theRenderer.fetchEvents(deltaTime)
            if not queue.empty():
                simData = queue.get(block=False)
                simPersons = simData[1]
                simNow = simData[0]
            theRenderer.render(simPersons, deltaTime, simNow) 
        nowOb = time.Timestamp(simNow)
        
        loops += 1
        if loops % 100 == 0:
            print("Simulation time: {0}:{1}:{2}".format(nowOb.day(), nowOb.hourOfDay(), nowOb.minuteOfHour()))

        if args.numDays > 0 and nowOb.day() >= args.numDays:
            running = False

    logging.write("output", "shutting down")
    if not args.noRender:
        theRenderer.quit()
    killSim.value = 1
    while(not queue.empty()):
        queue.get(block=False)
    simProcess.join() 
    
def simLoop(connection, killMe):
    #SETUP
    args = readArguments()

    registerLoggingCategories()


    config = configparser.ConfigParser()
    config.read(args.configFile)

    logging.write("output", "generating")
    needTypes = generation.need_parser.readNeedTypes(args.needTypesFile)
    theGrid = generation.grid_generator.generate(int(config["default"]["gridSize"]), needTypes)
    persons = generation.person_generator.generate(theGrid, int(config["default"]["numPersons"]), needTypes)

    for needType in needTypes:
        needType.initialize(persons, theGrid)
        logging.write("output", needType.getName())

    initializePersonScript, getNeedPrio, updateNeeds = loadPersonScripts(config)

    #We need to send the grid data to the renderer.
    connection.put([len(persons), theGrid.size, [p.char.placeType.value for p in theGrid.internal_grid]])

    initializePersonScript(needTypes)
    theSimulation = Simulation(persons, getNeedPrio, updateNeeds)

    #MAIN LOOP
    lastUpdate = getCurrentTimeMillis()
    while killMe.value == 0:
        now = getCurrentTimeMillis()
        deltaTime = now - lastUpdate
        theSimulation.simulate()
        if deltaTime/1000 > 1/5 and connection.empty():
            connection.put([theSimulation.now.now(), [p.getXY(theSimulation.now) for p in theSimulation.persons]])

if __name__ == "__main__":
    main()
