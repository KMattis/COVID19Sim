class Camera:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def setPos(self, x, y):
        self.x = x
        self.y = y

    def getRelXPos(self, absX):
        return absX - self.x

    def getRelYPos(self, absY):
        return absY - self.y