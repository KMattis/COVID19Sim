import abc

class DiseaseType(abc.ABC):

    @abc.abstractmethod
    def initialize(self, needTypes):
        pass

    @abc.abstractmethod
    def update(self, now, person):
        pass

    @abc.abstractmethod
    def getName(self):
        pass

