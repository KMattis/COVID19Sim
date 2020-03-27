import time


import generation.grid_generator, generation.person_generator
from rendering.renderer import Renderer

theGrid = generation.grid_generator.generate(100)
persons = generation.person_generator.generate(theGrid, 100)

theRenderer = Renderer()

lastUpdate = time.Time()
running = True
while running:
    running = theRenderer.render(theGrid, persons)



theRenderer.quit()
