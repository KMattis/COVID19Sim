from rendering import camera
from rendering import text
from rendering.vbo import VertexBufferObject

from profiler.profiler import profilerObj

from OpenGL.GL import *
from OpenGL.arrays import ArrayDatatype as ADT

import ctypes

import numpy

import pygame
import pygame.time
from pygame.locals import *

DISPLAY_WIDTH = 1100
DISPLAY_HEIGHT = 1100

PLACE_SIZE = 0.6

MOVEMENT_PER_SECOND = 50

class Renderer:
    def __init__(self, numPersons):
        pygame.display.init()
        pygame.init()
        self.display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT),
                pygame.OPENGL | pygame.DOUBLEBUF)
        glClearColor(255,255,255,255)
        pygame.display.set_caption("COVID-19 Simulation")
        self.camera = camera.Camera(20, 20, DISPLAY_WIDTH, DISPLAY_HEIGHT)
        self.colors = { -1: (255,255,255), 0: (0, 0, 255), 1: (255, 0, 0), 2: (128, 0, 128), 3: (0, 0.5, 0) }

        self.vbo = None
        self.time_text = text.Text('', position=(-0.88, 0.95), font_size=80, font_color=(0,0,0,1))
        self.fps_text = text.Text('', position=(-0.88, 0.9), font_size=80, font_color=(0,0,0,1))
        self.clock = pygame.time.Clock()
        self.personVertices = numpy.empty(numPersons * 2, dtype=numpy.float32)

 
    def initPlaceBuffer(self, grid):
        vertexBufferData = []

        for x in range(0, grid.size):
            for y in range(0, grid.size):
                thePlace = grid.get(x,y)
                color = self.colors[thePlace.char.placeType.value]
                dl = [x, y]
                dr = [x + PLACE_SIZE, y]
                tl = [x, y + PLACE_SIZE]
                tr = [x + PLACE_SIZE, y + PLACE_SIZE]

                vertices = [dl, tl, tr, dl, tr, dr]

                for vertex in vertices:
                    vertexBufferData.append(float(vertex[0]))
                    vertexBufferData.append(float(vertex[1]))
                    vertexBufferData.append(float(color[0]))
                    vertexBufferData.append(float(color[1]))
                    vertexBufferData.append(float(color[2]))

        self.vbo = VertexBufferObject(vertexBufferData)

    def fetchEvents(self, deltaTime):
        running = True
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.camera.zoom(0.85)
                elif event.button == 5:
                    self.camera.zoom(1.15)
            elif event.type == QUIT:
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

        return running

    def render(self, persons, deltaTime, now):
        self.camera.setupProjectionMatrix()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        profilerObj.startProfiling("places")
        #Draw the places
        self.vbo.bind()
        glVertexPointer(2, GL_FLOAT, 5*4, None)
        glColorPointer(3, GL_FLOAT, 5*4, ctypes.c_void_p(8))
        self.vbo.draw()
        VertexBufferObject.unbind()
        profilerObj.stopStartProfiling("persons")
        #Draw the persons
        self.drawPersons(persons, now)
        profilerObj.stopStartProfiling("text")
        #Draw text
        self.camera.setupAbsoluteMatrix()
        self.drawTime(now)
        profilerObj.stopProfiling()

        glFlush()
        pygame.display.flip()
        self.clock.tick()
    
    def quit(self):
        pygame.display.quit()

    def drawPersons(self, persons, now):
        #persons cannot be drawn via vbo because there positions change
        #we draw them directly as arrays

        placeSizeHalfed = PLACE_SIZE / 2
        profilerObj.startProfiling("arrayCreation")
        for i in range(len(persons)):
            x, y = persons[i].getXY(now)
            self.personVertices[2 * i] = x + placeSizeHalfed
            self.personVertices[2 * i + 1] = y + placeSizeHalfed

        profilerObj.stopStartProfiling("drawing")
        glColor3f(0,0,0)
        glPointSize(PLACE_SIZE * 10)

        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(2, GL_FLOAT, 0, self.personVertices)
        glDrawArrays(GL_POINTS, 0, len(persons))
        glDisableClientState(GL_VERTEX_ARRAY)
        profilerObj.stopProfiling()

    def drawTime(self, now):
        shader = text.get_default_shader()

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.fps_text.set_text('FPS: {0}'.format(round(self.clock.get_fps())))
        self.time_text.set_text('{0}:{1}:{2}'.format(round(now.day()), round(now.hourOfDay()), round(now.minuteOfHour())))

        self.fps_text.draw(shader)
        self.time_text.draw(shader)

        glDisable(GL_BLEND)
