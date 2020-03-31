from typing import Dict

from model import place, place_characteristics

class DistanceMap:
    def __init__(self, internal_grid: [place.Place], size: int, blockSize: int, maxDistance: int):
        self.size: int = size
        self.internal_grid: [place.Place] = internal_grid
        self.blockSize: int = blockSize
        if size % blockSize != 0:
            raise("Size must be divisible blockSize") 
        self.noBlocks: int = size // blockSize
        self.blocks: [Dict] = [None for _ in range(self.noBlocks**2)]
        self.maxDistance: int = maxDistance

    def getBlock(self, x: int, y: int) -> Dict:
        return self.blocks[x//self.blockSize + y//self.blockSize * self.noBlocks]

    def getBlockCoord(self, x: int, y: int) -> (int, int):
        return x//self.blockSize, y//self.blockSize 

    def getCenter(self, blockX: int, blockY: int) -> (int, int):
        return blockX*self.blockSize+self.blockSize//2, blockY*self.blockSize+self.blockSize//2 
    
    def calcDistancesFromBlock(self, blockX: int, blockY: int) -> None:
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

    def calcDistances(self) -> None:
       for blockX in range(self.noBlocks):
            for blockY in range(self.noBlocks): 
                self.calcDistancesFromBlock(blockX, blockY)

    def getNearPlaces(self, x: int, y: int, placeType: place_characteristics.PlaceType):
       return self.getBlock(x,y)[placeType]

class Grid:
    def __init__(self, size: int):
        self.size: int = size
        self.internal_grid: [place.Place] = [None for _ in range(size * size)]
        self.distanceMap: DistanceMap = DistanceMap(self.internal_grid, size, size//5, 20)

    def get(self, x: int, y: int) -> place.Place:
        return self.internal_grid[x + self.size * y]

    def set(self, x: int, y: int, thePlace: place.Place):
        self.internal_grid[x + self.size * y] = thePlace

    def addPlace(self, thePlace: place.Place) -> None:
        if self.get(thePlace.x,thePlace.y) is not None:
            raise Exception("There is already a place at this point")
        self.set(thePlace.x, thePlace.y, thePlace)
    
    def getDistanceMap(self) -> DistanceMap:
        return self.distanceMap
