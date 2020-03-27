from rendering import camera

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.arrays import ArrayDatatype as ADT

import ctypes

import numpy

import pygame
from pygame.locals import *

DISPLAY_WIDTH = 1100
DISPLAY_HEIGHT = 1100

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
        self.colors = { -1: (255,255,255), 0: (0, 0, 255), 1: (255, 0, 0), 2: (128, 0, 128), 4: (0, 0.5, 0) }

        self.placesVertexBuffer = None
 
    def initPlaceBuffer(self, grid):
        vertexBufferData = []

        for x in range(0, grid.size):
            for y in range(0, grid.size):
                thePlace = grid.get(x,y)
                color = self.colors[thePlace.char.placeType.value]
                dl = [CELL_SIZE*x, CELL_SIZE*y]
                dr = [CELL_SIZE*x + PLACE_SIZE, CELL_SIZE*y]
                tl = [CELL_SIZE*x, CELL_SIZE*y + PLACE_SIZE]
                tr = [CELL_SIZE*x + PLACE_SIZE, CELL_SIZE*y + PLACE_SIZE]

                vertices = [dl, tl, tr, dl, tr, dr]

                for vertex in vertices:
                    vertexBufferData.append(float(vertex[0]))
                    vertexBufferData.append(float(vertex[1]))
                    vertexBufferData.append(float(color[0]))
                    vertexBufferData.append(float(color[1]))
                    vertexBufferData.append(float(color[2]))

        vertexBufferData = numpy.array(vertexBufferData, dtype=numpy.float32)

        self.placesVertexBuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.placesVertexBuffer)
        glBufferData(GL_ARRAY_BUFFER, ADT.arrayByteCount(vertexBufferData), ADT.voidDataPointer(vertexBufferData), GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def render(self, grid, persons, deltaTime, now):
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

        #Draw the places
        glBindBuffer(GL_ARRAY_BUFFER, self.placesVertexBuffer)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)

        glVertexPointer(2, GL_FLOAT, 5*4, None)
        glColorPointer(3, GL_FLOAT, 5*4, ctypes.c_void_p(8))
        glDrawArrays(GL_TRIANGLES, 0, grid.size * grid.size * 6)

        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)

        glBindBuffer(GL_ARRAY_BUFFER, 0)


        for thePerson in persons:
            x,y = thePerson.getXY(now)
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
    
