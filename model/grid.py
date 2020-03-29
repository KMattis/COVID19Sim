import model.place

class Grid:
    def __init__(self, size):
        self.size = size
        self.internal_grid = [None for _ in range(size * size)]
        self.parks = []
        self.distanceMap = DistanceMap(self.internal_grid, size, size//5, 10)

    def get(self, x, y):
        return self.internal_grid[x + self.size * y]

    def set(self, x, y, place):
        self.internal_grid[x + self.size * y] = place
        if place.char.placeType == model.place.PlaceType.OUTDOOR:
            self.parks.append(place)

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
    
    def getDistanceMap(self):
        return self.distanceMap

class DistanceMap:
    def __init__(self, internal_grid, size, blockSize, maxDistance):
        self.size = size
        self.internal_grid = internal_grid
        self.blockSize = blockSize
        if size % blockSize != 0:
            raise("Size must be divisible blockSize") 
        self.noBlocks = size // blockSize
        self.blocks = [None for _ in range(self.noBlocks**2)]
        self.maxDistance = maxDistance

    def getBlock(self, x, y):
        return self.blocks[x//self.blockSize + y//self.blockSize * self.noBlocks]

    def getBlockCoord(self, x, y):
        return x//self.blockSize, y//self.blockSize 

    def getCenter(self, blockX, blockY):
        return blockX*self.blockSize+self.blockSize//2, blockY*self.blockSize+self.blockSize//2 
    
    def calcDistancesFromBlock(self, blockX, blockY):
        blockDict = {}
        cx, cy = self.getCenter(blockX, blockY)
        for dx in range(-self.maxDistance, self.maxDistance):
            for dy in range(-self.maxDistance, self.maxDistance):
                x = dx+cx
                y = dy+cy 
                if x + y * self.size >= self.size**2 or x + y * self.size < 0:
                    continue
                currentPoint = self.internal_grid[x + y * self.size]
                blockDict.setdefault(currentPoint.char.subType, []).append([[x,y], dx**2+dy**2, 1 if (dx**2+dy**2) == 0 else 1/(dx**2+dy**2) ])
        for types in blockDict:
            blockDict[types].sort(key=lambda ls: ls[1])
        self.blocks[blockX + self.noBlocks*blockY] = blockDict

    def calcDistances(self):
       for blockX in range(self.noBlocks):
            for blockY in range(self.noBlocks): 
                self.calcDistancesFromBlock(blockX, blockY)

    def getNearPlaces(self, x, y, placeType):
       return self.getBlock(x,y)[placeType]

