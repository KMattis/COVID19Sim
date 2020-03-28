from rendering import camera
from rendering import text
from rendering.vbo import VertexBufferObject


from OpenGL.GL import *
from OpenGL.arrays import ArrayDatatype as ADT

import ctypes

import numpy

import pygame
import pygame.time
from pygame.locals import *

DISPLAY_WIDTH = 1100
DISPLAY_HEIGHT = 1100

CELL_SIZE = 21
PLACE_SIZE = 11

MOVEMENT_PER_SECOND = 200

class Renderer:
    def __init__(self):
        pygame.display.init()
        pygame.init()
        self.display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT),
                pygame.OPENGL | pygame.DOUBLEBUF)
        glClearColor(255,255,255,255)
        pygame.display.set_caption("COVID-19 Simulation")
        self.camera = camera.Camera(DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2, DISPLAY_WIDTH, DISPLAY_HEIGHT)
        self.colors = { -1: (255,255,255), 0: (0, 0, 255), 1: (255, 0, 0), 2: (128, 0, 128), 4: (0, 0.5, 0) }

        self.vbo = None
        self.time_text = text.Text('', position=(-0.88, 0.95), font_size=80, font_color=(0,0,0,1))
        self.fps_text = text.Text('', position=(-0.88, 0.9), font_size=80, font_color=(0,0,0,1))
        self.clock = pygame.time.Clock()

 
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

    def render(self, persons, deltaTime, now, profiler):
        self.camera.setupProjectionMatrix()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        profiler.startProfiling("places")
        #Draw the places
        self.vbo.bind()
        glVertexPointer(2, GL_FLOAT, 5*4, None)
        glColorPointer(3, GL_FLOAT, 5*4, ctypes.c_void_p(8))
        self.vbo.draw()
        VertexBufferObject.unbind()
        profiler.stopStartProfiling("persons")
        #Draw the persons
        self.drawPersons(persons, now)
        profiler.stopStartProfiling("text")
        #Draw text
        self.camera.setupAbsoluteMatrix()
        self.drawTime(now)
        profiler.stopProfiling()

        glFlush()
        pygame.display.flip()
        self.clock.tick()
    
    def quit(self):
        pygame.display.quit()

    def drawPersons(self, persons, now):
        #persons cannot be drawn via vbo because there positions change
        #we draw them directly as arrays

        f = lambda p: [p[0] * CELL_SIZE + PLACE_SIZE // 2, p[1] * CELL_SIZE + PLACE_SIZE // 2] 
        vertices = [f(thePerson.getXY(now)) for thePerson in persons]

        buffer = numpy.array(vertices, dtype=numpy.float32)

        glColor3f(0,0,0)
        glPointSize(PLACE_SIZE * 0.65)

        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointerf(buffer)
        glDrawArrays(GL_POINTS, 0, len(persons))
        glDisableClientState(GL_VERTEX_ARRAY)

    def drawTime(self, now):
        shader = text.get_default_shader()

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.fps_text.set_text('FPS: {0}'.format(round(self.clock.get_fps())))
        self.time_text.set_text('{0}:{1}:{2}'.format(round(now.day()), round(now.hourOfDay()), round(now.minuteOfHour())))

        self.fps_text.draw(shader)
        self.time_text.draw(shader)

        glDisable(GL_BLEND)