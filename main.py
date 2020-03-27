import time


import generation.grid_generator, generation.person_generator
from rendering.renderer import Renderer

def getCurrentTimeMillis():
    return round(time.time() * 1000)

theGrid = generation.grid_generator.generate(200)
persons = generation.person_generator.generate(theGrid, 10000)

theRenderer = Renderer()

lastUpdate = getCurrentTimeMillis()
running = True

loops = 0

while running:
    now = getCurrentTimeMillis()
    deltaTime = now - lastUpdate
    lastUpdate = now

    running = theRenderer.render(theGrid, persons, deltaTime)

    for thePerson in persons:
        thePerson.update(deltaTime / 5000)

    if deltaTime > 0 and loops % 10 == 0:
        print("FPS:", 1000 / deltaTime)

    loops += 1

theRenderer.quit()
