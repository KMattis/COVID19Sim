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
        self.camera = camera.Camera(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)
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
    
        
        startX = max(0, self.camera.x // CELL_SIZE - 1)
        startY = max(0, self.camera.y // CELL_SIZE - 1)
        endX = min(grid.size, (self.camera.x + self.camera.screenWidth) // CELL_SIZE + 1)
        endY = min(grid.size, (self.camera.y + self.camera.screenHeight) // CELL_SIZE + 1)

        for x in range(startX, endX):
            for y in range(startY, endY):
                thePlace = grid.get(x,y)
                color = self.colors[thePlace.char.placeType.value]
                self.drawRect(
                        CELL_SIZE*thePlace.x, 
                        CELL_SIZE*thePlace.y,
                        PLACE_SIZE, 
                        PLACE_SIZE,
                        color,
                        0)

        for thePerson in persons:
            x,y = thePerson.getXY()
            # self.drawRectChecked(
            #         x * CELL_SIZE,
            #         y * CELL_SIZE,
            #         PLACE_SIZE,
            #         PLACE_SIZE,
            #         (255, 128, 0),
            #         3)
    
        pygame.display.update()
        return running
    
    def quit(self):
        pygame.display.quit()

    def drawRect(self, x, y, width, height, color, thickness):
        pygame.draw.rect(self.display, color,
            (self.camera.getRelXPos(x), self.camera.getRelYPos(y), width, height),
            thickness)

    def drawRectChecked(self, x, y, width, height, color, thickness):
        if self.camera.onScreen(x, y, width, height):
            pygame.draw.rect(self.display, color,
                (self.camera.getRelXPos(x), self.camera.getRelYPos(y), width, height),
                thickness)
    
