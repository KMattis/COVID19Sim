import time


import generation.grid_generator, generation.person_generator
from rendering.renderer import Renderer
from simulation.simulation import Simulation

def getCurrentTimeMillis():
    return round(time.time() * 1000)

theGrid = generation.grid_generator.generate(100)
persons = generation.person_generator.generate(theGrid, 10000)

theRenderer = Renderer()
theRenderer.initPlaceBuffer(theGrid)

theSimulation = Simulation(persons)

lastUpdate = getCurrentTimeMillis()
running = True

loops = 0

while running:
    now = getCurrentTimeMillis()
    deltaTime = now - lastUpdate
    lastUpdate = now

    running = theRenderer.render(theGrid, persons, deltaTime, theSimulation.minute)
    theSimulation.simulate(deltaTime)

    if deltaTime > 0 and loops % 10 == 0:
        # print("FPS:", 1000 / deltaTime)
        m = int(theSimulation.minute)
        print(m // (24 * 60),  (m // 60) % 24, m % 60, sep=":")
    

    loops += 1

theRenderer.quit()
