from model import grid, place, person

class Simulation:
    def __init__(self, persons):
        self.minute = 0
        self.persons = persons

    def simulate(self, delta):
        self.minute += delta
        for thePerson in self.persons:
            thePerson.update(delta)
