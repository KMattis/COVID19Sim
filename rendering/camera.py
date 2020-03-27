class Camera:
    def __init__(self, x, y, screenWidth, screenHeight):
        self.x = x
        self.y = y
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
    
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

    def onScreen(self, x, y, width, height):
        return x + width >= self.x and y + height >= self.y and x <= self.x + self.screenWidth and y <= self.y + self.screenHeight
