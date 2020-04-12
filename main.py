import time as pytime
import configparser
import argparse

from multiprocessing import Process, Manager, Value, Array
from generation import transport_generator, traffic_parser

import importlib.util
import inspect

from generation import grid_generator, person_generator, script_loader
from simulation.simulation import Simulation
from simulation import time
from plotting import logging
from simulation import random
from model import transport


def readArguments():
    #Setup argparse
    argparser: argparse.ArgumentParser = argparse.ArgumentParser()
    argparser.add_argument("--no-render", dest="noRender", action='store_const', const=True)
    argparser.add_argument("--config-file", dest="modelsConfigFile", type=str, default="simconfig/models.ini")
    argparser.add_argument("--model", dest="model", type=str, default="realistic")
    argparser.add_argument("--num-days", dest="numDays", type=int, default=0)
    argparser.add_argument("--seed",dest="seedValue",type=int,default=None)
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
    nownow = Value('i', 0, lock=False)
    travelDatas = Array(transport.TravelData, 10000, lock=False)
    simProcess = Process(target=simLoop, args=(queue, killSim, nownow, travelDatas, ))
    simProcess.start()

    random.setSeed(args.seedValue)
    #Initialize the renderer
    initialData = queue.get(block=True)
    numPersons = initialData[0]
    gridSize = initialData[1]
    gridData = initialData[2]
    theRenderer = Renderer(numPersons)
    theRenderer.initPlaceBuffer(gridSize, gridData)
    
    #Get the first simulation datum
    #simData = queue.get(block=True)
    simPersons = list(map(lambda td: (td.startTime,
                            td.endTime,
                            td.destination_x,
                            td.destination_y,
                            td.origin_x, td.origin_y) 
                            if td.startTime <= nownow.value <= td.endTime
                            else (-1, -1, 0, 0, td.origin_x, td.origin_y),
                            travelDatas))

    nowOb = time.Timestamp(nownow.value)
    ########

    while running:
        now = getCurrentTimeMillis()
        deltaTime = now - lastUpdate

        running = theRenderer.fetchEvents(deltaTime)
        simPersons = list(map(lambda td: (td.startTime,
                            td.endTime,
                            td.destination_x,
                            td.destination_y,
                            td.origin_x, td.origin_y) 
                            if td.startTime <= nownow.value <= td.endTime
                            else (-1, -1, 0, 0, td.origin_x, td.origin_y),
                            travelDatas))
        
        theRenderer.render(simPersons, deltaTime, nownow.value)
        nowOb = time.Timestamp(nownow.value)
        
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
    
def simLoop(connection, killMe, nownow, travelDatas):
    #SETUP
    registerLoggingCategories()
    args = readArguments()
    random.setSeed(args.seedValue)
    modelData = loadModelData(args)
    theSimulation = setupSimulation(modelData, travelDatas)

    #We need to send the grid data to the renderer.
    connection.put([len(theSimulation.persons), theSimulation.grid.size, [p.char.placeType.value for p in theSimulation.grid.internal_grid]])

    #MAIN LOOP
    last100 = getCurrentTimeMillis()
    i = 0
    while killMe.value == 0:
        theSimulation.simulate()
        nownow.value = theSimulation.now.now()
        i += 1
        if i % 100 == 0:
            print("100 simulation steps took " + str(getCurrentTimeMillis() - last100) + "ms")
            last100 = getCurrentTimeMillis()

def loadModelData(args):
    modelDataParser = configparser.ConfigParser()
    modelDataParser.read(args.modelsConfigFile)
    return modelDataParser[args.model]

def setupSimulation(model_data, travelDatas):
    needTypes = script_loader.readObjectsFromScript(model_data["need_types"], "need_types")
    needTypesDict = {}
    for needType in needTypes:
        needTypesDict[needType.getName()] = needType
    diseaseTypes  = script_loader.readObjectsFromScript(model_data["disease_types"], "disease_types")
    theGrid = grid_generator.generate(model_data)
    persons = person_generator.generate(model_data, needTypesDict, diseaseTypes)
    privateSpeed, publicSpeed, distStationsX, distStationsY, freq = traffic_parser.readTrafficData(model_data["transport"])


    for needType in needTypes:
        needType.initialize(needTypesDict, persons, theGrid)
        logging.write("output", needType.getName())

    for diseaseType in diseaseTypes:
        diseaseType.initialize(needTypesDict)
        logging.registerCategory("disease." + diseaseType.getName())

    return Simulation(persons, theGrid, diseaseTypes, transport_generator.generate(theGrid, distStationsX, distStationsY, privateSpeed, publicSpeed, freq), travelDatas)

def mainNoRender(args):
    #Startup code
    registerLoggingCategories()
    random.setSeed(args.seedValue)
    modelData = loadModelData(args)
    theSimulation = setupSimulation(modelData, )

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
