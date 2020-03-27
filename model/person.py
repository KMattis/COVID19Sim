class Person:
    def __init__(self, name, age, home, workplace):
        self.name = name
        self.age = age
        self.home = home
        self.workplace = workplace
        self.currentPosition = home
        self.currentDestination = workplace
        self.progress = 0.0

    def setDestination(self, dest):
        self.currentDestination = dest
        self.progress = 0.0
    
    def getXY(self):
        return (self.currentPosition.x + (self.currentDestination.x - self.currentPosition.x) * self.progress,
            self.currentPosition.y + (self.currentDestination.y - self.currentPosition.y) * self.progress)

    def update(self, delta):
        self.progress += delta
        if self.progress >= 1.0:
            self.progress = 1.0
            self.currentPosition = self.currentDestination
