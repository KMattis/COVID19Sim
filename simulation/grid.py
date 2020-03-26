
import place

class Grid:
    def __init__(self, size):
        self.internal_grid = [[None for _ in range(size)] for _ in range(size)]

    def addPlaceAt(self, x, y, p):
        if self.internal_grid[x][y] is not None:
            raise Exception("There is already a place at this point")
        self.internal_grid[x][y] = p