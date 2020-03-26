import enum

import place

class Person:
    def __init__(self, age, infected = False, immune = False):
        #The person's age
        self.age = age

        #Whether this person is infected with COVID19
        self.infected = infected

        #Whether this person is immune to COVID19
        self.immune = immune

class GroupType(enum.Enum):
    FAMILY  = 0
    FRIENDS = 1

#A group may represent a family, a circle of friends, collegues, etc.
#Groups may schedule meetings, which the members will likely attend
#A group should do one activity regularly. TODO: the place might change?
#i.e. they might meet every day in a restaurant, or every saturday at the football field, etc.
#A family for example will meet every evening until the the next morning, to simulate sleeping
class Group:
    def __init__(self, members: list(Person), meetingPlace: place.Place):
        self.members = members
        self.place = meetingPlace


#TODO: There should also be large scale events like soccer games where many people without connections meet
