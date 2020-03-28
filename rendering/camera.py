from OpenGL.GL import *

class Camera:
    def __init__(self, x, y, screenWidth, screenHeight):
        self.x = x
        self.y = y
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.zoomFactor = 0.05
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def zoom(self, factor):
        self.zoomFactor *= factor

    def setupProjectionMatrix(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(self.x - self.zoomFactor * self.screenWidth / 2,  self.x + self.zoomFactor * self.screenWidth / 2,
                self.y - self.zoomFactor * self.screenHeight / 2, self.y + self.zoomFactor * self.screenHeight / 2,
                -1, 1)
        glMatrixMode(GL_MODELVIEW)

    def setupAbsoluteMatrix(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.screenWidth,
                0, self.screenHeight,
                -1, 1)
        glMatrixMode(GL_MODELVIEW)

#    def onScreen(self, x, y, width, height):
#        return x + width >= self.x and y + height >= self.y and x <= self.x + self.screenWidth and y <= self.y + self.screenHeight
