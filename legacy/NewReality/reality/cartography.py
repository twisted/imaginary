import random

class Area:
    def __init__(self):
        self.compass = Compass()
        self.externalExits = {}

    def addExternalExit(self, name, externalExit):
        self.externalExit[name] = externalExit

class Compass:
    points = ('north', 'northeast', 'east', 'southeast', 'south', 'southwest', 'west', 'northwest')

    def spin(self, numPoints=None):
        if numPoints is None:
            numPoints = random.randint(1,7)
        front = self.points[:numPoints]
        back = self.points[numPoints:]
        self.points = back + front
    
    def __getitem__(self, key):
        k = key.lower()
        name = self.points[list(Compass.points).index(k)]
        if key.isupper():
            return name.upper()
        elif key[0].isupper():
            return name.capitalize()
        else:
            return name

