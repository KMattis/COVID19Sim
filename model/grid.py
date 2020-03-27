import model.place

class Grid:
    def __init__(self, size):
        self.size = size
        self.internal_grid = [[None for _ in range(size)] for _ in range(size)]

    def addPlace(self, thePlace):
        if self.internal_grid[thePlace.x][thePlace.y] is not None:
            raise Exception("There is already a place at this point")
        self.internal_grid[thePlace.x][thePlace.y] = thePlace

    def render(self):
        switch = { 0: "\033[34m", 1: "\033[33m", 2: "\033[32m", 4: "\033[31m" }

        for i in range(self.size):
            for j in range(self.size):
                t = self.internal_grid[i][j].char.placeType.value
                print(switch[t], t, "\033[0m", end="", sep="")
            print()
