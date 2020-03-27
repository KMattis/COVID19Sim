import model.place

class Grid:
    def __init__(self, size):
        self.size = size
        self.internal_grid = [None for _ in range(size * size)]

    def get(self, x, y):
        return self.internal_grid[x + self.size * y]

    def set(self, x, y, place):
        self.internal_grid[x + self.size * y] = place

    def addPlace(self, thePlace):
        if self.get(thePlace.x,thePlace.y) is not None:
            raise Exception("There is already a place at this point")
        self.set(thePlace.x, thePlace.y, thePlace)

    def render(self):
        switch = { 0: "\033[34m", 1: "\033[33m", 2: "\033[32m", 4: "\033[31m" }

        for i in range(self.size):
            for j in range(self.size):
                t = self.get(i, j).char.placeType.value
                print(switch[t], "\u2588", "\033[0m", end="", sep="")
            print()
