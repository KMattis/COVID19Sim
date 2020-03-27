from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.arrays import ArrayDatatype as ADT

import numpy

class VertexBufferObject:

    def __init__(self, vertices):
        vertexBufferData = numpy.array(vertices, dtype=numpy.float32)
        self.num_vertices = len(vertices)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, ADT.arrayByteCount(vertexBufferData), ADT.voidDataPointer(vertexBufferData), GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
    
    def bind(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)

    def draw(self):
        glDrawArrays(GL_TRIANGLES, 0, self.num_vertices)

    @staticmethod
    def unbind():        
        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
