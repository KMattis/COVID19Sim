import time

def getCurrentTimeMillis():
    return round(time.time() * 1000)

def keyToList(key: str):
    return key.split(".", -1)

def listToKey(list):
    return ".".join(list)

class Profiler:
    def __init__(self):
        self.startTimes = {}
        self.totalTimes = {}
        self.currentKey = []

    def reset(self):
        self.startTimes.clear()
        self.totalTimes.clear()


    def startProfiling(self, k):
        self.currentKey = self.currentKey + [k]

        self.startTimes[listToKey(self.currentKey)] = getCurrentTimeMillis()
        if listToKey(self.currentKey) not in self.totalTimes:
            self.totalTimes[listToKey(self.currentKey)] = 0

    def stopProfiling(self):
        self.totalTimes[listToKey(self.currentKey)] += getCurrentTimeMillis() - self.startTimes[listToKey(self.currentKey)]
        self.currentKey = self.currentKey[:-1]
    
    def stopStartProfiling(self, k):
        self.stopProfiling()
        self.startProfiling(k)

    def printPercentages(self, baseKey):
        print("Profiling results:")
        print("-"*30)
        self.printPercentages0([baseKey])
        print("-"*30)

    def printPercentages0(self, key):
        relevantKeys = []
        for _k in self.totalTimes:
            k = keyToList(_k)
            if len(k) == len(key) + 1 and key == k[:len(key)]:
                relevantKeys.append(k)

        if len(relevantKeys) == 0:
            return

        totalTime = self.totalTimes[listToKey(key)]

        sumPercentage = 0
        indent = " "*(len(key)-1)*4
        for k in relevantKeys:
            percentage = round(100 * self.totalTimes[listToKey(k)] / totalTime)
            sumPercentage += percentage
            print(indent + listToKey(k) + ": " + str(percentage) + "%")
            self.printPercentages0(k)
        print(indent + listToKey(key) + ".other: " + str(100 - sumPercentage) + "%")
