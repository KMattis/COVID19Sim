from rendering import camera

from OpenGL.GL import *
from OpenGL.GLU import *

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
        self.display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT),
                pygame.OPENGL | pygame.DOUBLEBUF)
        glClearColor(255,255,255,255)
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
            self.camera.move(0, +(deltaTime / 1000) * MOVEMENT_PER_SECOND)
        if keys[K_DOWN] or keys[K_s]:
            self.camera.move(0, -(deltaTime / 1000) * MOVEMENT_PER_SECOND)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(self.camera.x, self.camera.x + self.camera.screenWidth,
                self.camera.y, self.camera.y + self.camera.screenHeight,
                -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        startX = int(max(0, self.camera.x // CELL_SIZE - 1))
        startY = int(max(0, self.camera.y // CELL_SIZE - 1))
        endX = int(min(grid.size, (self.camera.x + self.camera.screenWidth) // CELL_SIZE + 1))
        endY = int(min(grid.size, (self.camera.y + self.camera.screenHeight) // CELL_SIZE + 1))

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
            self.drawRectChecked(
                    x * CELL_SIZE,
                    y * CELL_SIZE,
                    PLACE_SIZE // 2,
                    PLACE_SIZE // 2,
                    (0, 0, 0),
                    3)
    
        glFlush()
        pygame.display.flip()
        return running
    
    def quit(self):
        pygame.display.quit()

    def drawRect(self, x, y, width, height, color, thickness):
        r,g,b = color
        glColor3f(r / 255, g / 255, b / 255)
        glRectf(x, y, x + width, y + height)

    def drawRectChecked(self, x, y, width, height, color, thickness):
        if self.camera.onScreen(x, y, width, height):
            self.drawRect(x, y, width, height, color, thickness)
    
