import pygame
from pygame.locals import *

DISPLAY_WIDTH = 1000
DISPLAY_HEIGHT = 1000

CELL_SIZE = 21
PLACE_SIZE = 11

class Renderer:
    def __init__(self):
        pygame.display.init()
        self.display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption("COVID-19 Simulation")
        self.colors = { 0: (0, 0, 255), 1: (255, 0, 0), 2: (128, 0, 128), 4: (0, 128, 0) }
    
    def render(self, grid, persons):
        running = True
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                running = False
    
        self.display.fill((255, 255, 255))
    
        for thePlace in grid.internal_grid:
            color = self.colors[thePlace.char.placeType.value]
            pygame.draw.rect(self.display,
                    color, 
                    (CELL_SIZE*thePlace.x, CELL_SIZE*thePlace.y,
                    PLACE_SIZE, PLACE_SIZE))

        for thePerson in persons:
            pygame.draw.rect(self.display,
                    (255, 128, 0),
                    (thePerson.home.x * CELL_SIZE,
                        thePerson.home.y * CELL_SIZE,
                        PLACE_SIZE,
                        PLACE_SIZE),
                    3)
    
        pygame.display.update()
        return running
    
    def quit(self):
        pygame.display.quit()
    
