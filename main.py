import time as pytime
import configparser
import argparse

from multiprocessing import Process, Manager, Value

import importlib.util
import inspect

import generation.grid_generator, generation.person_generator, generation.script_loader
from rendering.renderer import Renderer
from simulation.simulation import Simulation
from simulation import time
from profiler.profiler import profilerObj
from plotting import logging

MINUTES_PER_REAL_SECOND = 1000
MAX_RENDER_PER_SEC = 5

killSimulationLoop = False

def readArguments():
    #Setup argparse
    argparser: argparse.ArgumentParser = argparse.ArgumentParser()
    argparser.add_argument("--no-render", dest="noRender", action='store_const', const=True)
    argparser.add_argument("--config-file", dest="modelsConfigFile", type=str, default="simconfig/models.ini")
    argparser.add_argument("--model", dest="model", type=str, default="realistic")
    argparser.add_argument("--num-days", dest="numDays", type=int, default=0)
    return argparser.parse_args()

def getCurrentTimeMillis():
    return round(pytime.time() * 1000)

def registerLoggingCategories():
    logging.registerCategory("activity")
    logging.registerCategory("places")
    logging.registerCategory("bobby")
    logging.registerCategory("output")
    logging.registerCategory("bobby_needs")
    logging.registerCategory("infections")

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
        else:
            simData = queue.get(block=True)
            simNow = simData[0]
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

    model_data_parser = configparser.ConfigParser()
    model_data_parser.read(args.modelsConfigFile)
    model_data = model_data_parser[args.model]

    logging.write("output", "generating")
    needTypes = generation.script_loader.readObjectsFromScript(model_data["need_types"], "need_types")
    needTypesDict = {}
    for needType in needTypes:
        needTypesDict[needType.getName()] = needType
    diseaseTypes  = generation.script_loader.readObjectsFromScript(model_data["disease_types"], "disease_types")
    theGrid = generation.grid_generator.generate(model_data, needTypes)
    persons = generation.person_generator.generate(theGrid, model_data, needTypesDict, diseaseTypes)

    for needType in needTypes:
        needType.initialize(needTypesDict, persons, theGrid)
        logging.write("output", needType.getName())

    for diseaseType in diseaseTypes:
        diseaseType.initialize(needTypesDict)
        logging.registerCategory("disease." + diseaseType.getName())

    #We need to send the grid data to the renderer.
    connection.put([len(persons), theGrid.size, [p.char.placeType.value for p in theGrid.internal_grid]])

    theSimulation = Simulation(persons, diseaseTypes)

    #MAIN LOOP
    lastUpdate = getCurrentTimeMillis()
    last100 = getCurrentTimeMillis()
    i = 1
    while killMe.value == 0:
        now = getCurrentTimeMillis()
        deltaTime = now - lastUpdate
        theSimulation.simulate()
        if deltaTime > 1000/MAX_RENDER_PER_SEC and connection.empty():
            personData = list(map(lambda p: ((p.currentPosition.x, p.currentPosition.y), p.direction, p.travelStart.now(), p.travelEnd.now()) if p.isTravelling() else ((p.currentPosition.x, p.currentPosition.y), (0,0), 0, 0), theSimulation.persons))
            connection.put([theSimulation.now.now(), personData])
            lastUpdate = now
        if i % 100 == 0:
            print("100 simulation steps took " + str(getCurrentTimeMillis() - last100) + "ms")
            last100 = getCurrentTimeMillis()
        i += 1

if __name__ == "__main__":
    main()
