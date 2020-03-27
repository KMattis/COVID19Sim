from rendering import camera

import pygame
from pygame.locals import *

DISPLAY_WIDTH = 1000
DISPLAY_HEIGHT = 1000

CELL_SIZE = 21
PLACE_SIZE = 11

MOVEMENT_PER_SECOND = 200

class Renderer:
    def __init__(self):
        pygame.display.init()
        self.display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption("COVID-19 Simulation")
        self.camera = camera.Camera(0, 0)
        self.colors = { 0: (0, 0, 255), 1: (255, 0, 0), 2: (128, 0, 128), 4: (0, 128, 0) }
    
    def render(self, grid, persons, deltaTime):
        running = True
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == pygame.QUIT:
                running = False

        keys=pygame.key.get_pressed()
        if keys[K_LEFT] or keys[K_a]:
            self.camera.move(-(deltaTime / 1000) * MOVEMENT_PER_SECOND, 0)
        if keys[K_RIGHT] or keys[K_d]:
            self.camera.move(+(deltaTime / 1000) * MOVEMENT_PER_SECOND, 0)
        if keys[K_UP] or keys[K_w]:
            self.camera.move(0, -(deltaTime / 1000) * MOVEMENT_PER_SECOND)
        if keys[K_DOWN] or keys[K_s]:
            self.camera.move(0, +(deltaTime / 1000) * MOVEMENT_PER_SECOND)
    
        self.display.fill((255, 255, 255))
    
        for thePlace in grid.internal_grid:
            color = self.colors[thePlace.char.placeType.value]
            pygame.draw.rect(self.display,
                    color, 
                    (self.camera.getRelXPos(CELL_SIZE*thePlace.x), 
                        self.camera.getRelYPos(CELL_SIZE*thePlace.y),
                        PLACE_SIZE, 
                        PLACE_SIZE))

        for thePerson in persons:
            x,y = thePerson.getXY()
            pygame.draw.rect(self.display,
                    (255, 128, 0),
                    (self.camera.getRelXPos(x * CELL_SIZE),
                        self.camera.getRelYPos(y * CELL_SIZE),
                        PLACE_SIZE,
                        PLACE_SIZE),
                    3)
    
        pygame.display.update()
        return running
    
    def quit(self):
        pygame.display.quit()
    
