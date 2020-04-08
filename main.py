import time as pytime
import configparser
import argparse

from multiprocessing import Process, Manager, Value

import importlib.util
import inspect

from generation import grid_generator, person_generator, script_loader
from simulation.simulation import Simulation
from simulation import time
from plotting import logging

MINUTES_PER_REAL_SECOND = 1000
MAX_RENDER_PER_SEC = 5

def readArguments():
    #Setup argparse
    argparser: argparse.ArgumentParser = argparse.ArgumentParser()
    argparser.add_argument("--no-render", dest="noRender", action='store_const', const=True)
    argparser.add_argument("--config-file", dest="modelsConfigFile", type=str, default="simconfig/models.ini")
    argparser.add_argument("--model", dest="model", type=str, default="realistic")
    argparser.add_argument("--num-days", dest="numDays", type=int, default=0)
    return argparser.parse_args()

#TODO: Move somewhere else?
def getCurrentTimeMillis():
    return round(pytime.time() * 1000)

def registerLoggingCategories():
    logging.registerCategory("activity")
    logging.registerCategory("places")
    logging.registerCategory("bobby")
    logging.registerCategory("output")
    logging.registerCategory("bobby_needs")
    logging.registerCategory("infections")

def mainRender(args):
    #Import this module only in render mode, as it needs pygame and PyOpenGL
    from rendering.renderer import Renderer

    lastUpdate = getCurrentTimeMillis()
    running = True
    loops = 0

    ########
    queue = Manager().Queue()
    killSim = Value('i', 0)
    simProcess = Process(target=simLoop, args=(queue, killSim,))
    simProcess.start()

    #Initialize the renderer
    initialData = queue.get(block=True)
    numPersons = initialData[0]
    gridSize = initialData[1]
    gridData = initialData[2]
    theRenderer = Renderer(numPersons)
    theRenderer.initPlaceBuffer(gridSize, gridData)

    #Get the first simulation datum
    simData = queue.get(block=True)
    simPersons = simData[1]
    simNow = simData[0]
    nowOb = time.Timestamp(simNow)
    ########

    while running:
        now = getCurrentTimeMillis()
        deltaTime = now - lastUpdate

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

    theRenderer.quit()
    killSim.value = 1
    while(not queue.empty()):
        queue.get(block=False)
    simProcess.join() 
    
def simLoop(connection, killMe):
    #SETUP
    registerLoggingCategories()
    args = readArguments()
    modelData = loadModelData(args)
    theSimulation = setupSimulation(modelData)

    #We need to send the grid data to the renderer.
    connection.put([len(theSimulation.persons), theSimulation.grid.size, [p.char.placeType.value for p in theSimulation.grid.internal_grid]])

    #MAIN LOOP
    lastUpdate = getCurrentTimeMillis()
    last100 = getCurrentTimeMillis()
    i = 0
    while killMe.value == 0:
        now = getCurrentTimeMillis()
        deltaTime = now - lastUpdate
        theSimulation.simulate()
        if deltaTime > 1000/MAX_RENDER_PER_SEC and connection.empty():
            personData = list(map(lambda p: ((p.currentPosition.x, p.currentPosition.y), p.direction, p.travelStart.now(), p.travelEnd.now()) if p.isTravelling() else ((p.currentPosition.x, p.currentPosition.y), (0,0), 0, 0), theSimulation.persons))
            connection.put([theSimulation.now.now(), personData])
            lastUpdate = now
        i += 1
        if i % 100 == 0:
            print("100 simulation steps took " + str(getCurrentTimeMillis() - last100) + "ms")
            last100 = getCurrentTimeMillis()

def loadModelData(args):
    modelDataParser = configparser.ConfigParser()
    modelDataParser.read(args.modelsConfigFile)
    return modelDataParser[args.model]

def setupSimulation(model_data):
    needTypes = script_loader.readObjectsFromScript(model_data["need_types"], "need_types")
    diseaseTypes  = script_loader.readObjectsFromScript(model_data["disease_types"], "disease_types")
    theGrid = grid_generator.generate(model_data)
    persons = person_generator.generate(model_data, needTypes, diseaseTypes)

    for needType in needTypes:
        needType.initialize(needTypes, persons, theGrid)
        logging.write("output", needType.getName())

    for diseaseType in diseaseTypes:
        diseaseType.initialize(needTypes)
        logging.registerCategory("disease." + diseaseType.getName())

    return Simulation(persons, theGrid, diseaseTypes)

def mainNoRender(args):
    #Startup code
    registerLoggingCategories()
    modelData = loadModelData(args)
    theSimulation = setupSimulation(modelData)

    #main loop
    running = True
    last100 = getCurrentTimeMillis()
    i = 0
    while running:
        theSimulation.simulate()
        i += 1
        if i % 100 == 0:
            print("100 simulation steps took " + str(getCurrentTimeMillis() - last100) + "ms")
            last100 = getCurrentTimeMillis()
        if args.numDays > 0 and theSimulation.now.day() >= args.numDays:
            running = False

if __name__ == "__main__":
    args = readArguments()
    if args.noRender:
        mainNoRender(args)
    else:
        mainRender(args)
