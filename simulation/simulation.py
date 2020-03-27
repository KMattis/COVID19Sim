from model import grid, place, person

class Simulation:
    def __init__(self, persons):
        self.minute = 0
        self.persons = persons

    def simulate(self, delta):
        self.minute += delta / 1000 * 10
        for thePerson in self.persons:
            thePerson.update(delta / 1000 * 10)
