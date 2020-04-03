import abc

from simulation import time

class NeedType(abc.ABC):

    @abc.abstractmethod
    def initialize(self, needTypes, persons, grid):
        pass

    @abc.abstractmethod
    def trySatisfy(self, person, needValue, now):
        pass

    @abc.abstractmethod
    def getName(self):
        pass
