import abc

from simulation import time

class PersonBehaviour(abc.ABC):
    @abc.abstractmethod
    def initialize(self, needTypes):
        pass

    @abc.abstractmethod
    def getNeedPrio(self, thePerson):
        pass

    @abc.abstractmethod
    def updateNeeds(self, thePerson):
        pass

    @abc.abstractmethod
    def getFrequency(self):
        pass

    @abc.abstractmethod
    def getPublicTransportAffinity(self):
        pass
