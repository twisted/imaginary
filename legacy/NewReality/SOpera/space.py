# Space Opera - A Multiplayer Science Fiction Game Engine
# Copyright (C) 2002 Jean-Paul Calderone
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	 See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
#

# System imports
import math, time, operator

# Reality imports
from Reality import thing, room, player

# Twisted imports
from twisted.internet import reactor

class Point:
    """
    Point(x, y, z) -> 3-dimensional euclidean point
    """

    EPSILON = 1e-12

    def __init__(self, x = 0.0, y = 0.0, z = 0.0):
        self.x, self.y, self.z = x, y, z

    def __eq__(self, other):
        if isinstance(other, Point):
            return (abs(self.x - other.x) < self.EPSILON and
                    abs(self.y - other.y) < self.EPSILON and
                    abs(self.z - other.z) < self.EPSILON)
        return 0
 
    def __len__(self):
        return 3

    def __neg__(self):
        return Point(-self.x, -self.y, -self.z)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)
    __radd__ = __add__

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if isinstance(other, Point):
            a = self.toPolar()
            b = other.toPolar()
            return Point.fromPolar(a[0] * b[0], a[1] + b[1], a[2] + b[2])
        else:
            return Point(self.x * other, self.y * other, self.z * other)
    __rmul__ = __mul__
    
    def __div__(self, other):
        if isinstance(other, Point):
            a = self.toPolar()
            b = other.toPolar()
            return Point.fromPolar(a[0] / b[0], a[1] - b[1], a[2] - b[2])
        else:
            return Point(self.x / other, self.y / other, self.z / other)

    def __str__(self):
        return '(%s, %s, %s)' % (self.x, self.y, self.z)
    
    def __repr__(self):
        return 'Point%s' % str(self)

    def unit(self):
        """unit(self) -> Point
        
        create and return the unit vector in the same direction as self
        """
        return self / self.magnitude()

    def magnitude(self):
        """magnitude(self) -> float
        
        return the distance from the origin to this point
        """
        return (self.x * self.x + self.y * self.y + self.z * self.z) ** 0.5

    def magnitude2(self):
        """magnitude2(self) -> float
        
        return the distance squared from the origin to this point
        """
        return (self.x * self.x + self.y * self.y + self.z * self.z)

    def distance(self, other):
        """distance(self) -> float
        
        return the distance from this point to the other point
        """
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2) ** 0.5

    def distance2(self, other):
        """distance2(self) -> float
        
        return the distance squared from this point to the other point
        """
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)

    def toPolar(self):
        """toPolar(self) -> 3-tuple
        
        return the spherical polar form of this point in a 3-tuple:
        (magnitude, latitude, longitude)
        """
        distance = (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5
        longitude = math.atan2(self.y, self.x)
        latitude = math.atan2((self.x ** 2 + self.y ** 2) ** 0.5, self.z)
        return distance, latitude, longitude

    def fromPolar(magnitude, latitude, longitude):
        """Point.fromPolar(magnitude, latitude, longitude) -> Point instance
        
        Create and return a Point from the given spherical polar parameters
        """
        longitude = longitude % (math.pi * 2)
        latitude = latitude % (math.pi * 2)
        x = math.cos(longitude) * math.sin(latitude) * magnitude
        y = math.sin(longitude) * math.sin(latitude) * magnitude
        z = math.cos(latitude) * magnitude
        return Point(x, y, z)
    fromPolar = staticmethod(fromPolar)

class AccelerationUnit:
    def __init__(self, amount):
        self.startTime, self.endTime, self.amount = None, None, amount

    def __str__(self):
        return str(self.amount) + ' for (%4.2f, %4.2f]' % (self.startTime, self.endTime)

    def start(self, when):
        self.startTime = when

    def end(self, when):
        self.endTime = when
        self.durTime = self.endTime - self.startTime
        self.dV = self.durTime * self.durTime * self.amount * 0.5

    def duration(self):
        return self.durTime

    def deltaV(self):
        return self.durTime * self.durTime * self.amount * 0.5

def calculateGravitationalAcceleration(things):
    """
    Calculate and sum the acceleration due to gravity of each Located
    in the sequence on each of the other Locateds in the sequence.  Each
    element of the returned list therefor contains a Point representing the total
    gravitational acceleration for the Thing with the same index in the parameter
    sequence.
    """
    l = len(things)
    accels = [Point()] * l
    for i in range(l):
        for j in range(i + 1, l):
            a = things[i].getGravitationalAttraction(things[j])
            accels[i] = accels[i] + a[0]
            accels[j] = accels[j] + a[1]
    return accels

def calculateTotalEnergy(things):
    """
    Calculate the total kinetic and gravitational potential energy
    of the sequence of things.
    """
    G = 6.667e-11

    k = 0
    for t in things:
        k = k + t.velocity.magnitude2() * (t.mass or 0)
    k = k / 2.0

    g = 0
    for t in things:
        Gt = G * t.mass
        for u in things:
            if u is not t:
                g = g + (Gt * u.mass) / t.coordinates.distance(u.coordinates)
    return k + g

class Located:
    # All values in meters, seconds, kilograms, or some combination thereof
    coordinates, velocity, acceleration = Point(), Point(), Point()
    mass = None
    _accel = None

    __implements__ = ()

    def init(self, t):
        self._accel = [AccelerationUnit(Point())]
        self._accel[0].start(t)

    def positionUpdated(self):
        """positionUpdated(self) -> None
        
        Called whenever self.update() finishes.
        """
        pass

    def update(self, perpetuate = 0):
        """update(self, perpetuate = 0) -> None
        
        Update velocity and coordinates based on all the acceleration changes
        that have occurred since the last call to this method.  If perpetuate
        is not zero, cause this method to be invoked after perpetuate seconds
        with the same arguments.
        """
        t = self.getTime()
        if self._accel is None:
            self.init(t)

        self._accel[-1].end(t)
        for i in self._accel:
            self.velocity = self.velocity + i.deltaV()
            self.coordinates = self.coordinates + self.velocity * i.duration()
        del self._accel[:-1]
        self._accel[0].startTime = self._accel[0].endTime
        
        self.positionUpdated()
        if perpetuate != 0:
            reactor.callLater(perpetuate, self.update, perpetuate)


    def getGravitationalAttraction(self, other):
        """getGravitationalAttraction(otherLocated) -> 2-tuple
        
        Calculate the acceleration due to gravity on the two Locateds
        due to each other.  The first element of the returned sequenced is
        a Point instance with direction towards otherLocated from self and
        magnitude equal to |acceleration due to gravity|.  The second element
        has the same magnitude and points in the opposite direction.
        """
        G = 6.667e-11
        F = (G * self.mass * other.mass) / (self.coordinates.distance2(other.coordinates))
        d1 = (other.coordinates - self.coordinates).unit() * F / self.mass
        d2 = (self.coordinates - other.coordinates).unit() * F / other.mass
        return d1, d2


    def getTime(self):
        return time.time()


    def addAcceleration(self):
        t = self.getTime()
        self._accel is None and self.init(t)
        self._accel[-1].end(t)
        self._accel.append(AccelerationUnit(self.acceleration))
        self._accel[-1].start(t)


    def __setattr__(self, attr, value):
        # To properly track the position and velocity, all the values
        # of acceleration between updates must be recorded, as well as
        # when the change occurred.
        self.__dict__[attr] = value
        if attr == 'acceleration' and self.acceleration is not None:
            self.addAcceleration()


class System(thing.Thing, Located):
    """
    A collection of Located Things, floating around in space.
    """
    def __init__(self, name, coordinates, velocity, reality = ''):
        thing.Thing.__init__(self, name, reality)
        self.coordinates = coordinates
        self.velocity = velocity


class Star(thing.Thing, Located):
    """
    The sun is a mass of incandescent gas, a gigantic nuclear furnace where
    hydrogen is built into helium at a temperature of millions of degrees.
    """
    def __init__(self, name, mass, reality = ''):
        thing.Thing.__init__(self, name, reality)
        self.mass = mass
        self.coordinates = self.velocity = Point()


class World(thing.Thing, Located):
    """
    A collection of locations, floating around in space.
    """
    def __init__(self, name, system, coordinates = None, velocity = None, reality = ''):
        thing.Thing.__init__(self, name, reality)
        self.location = system
        self.coordinates = coordinates
        self.velocity = velocity


try:
    import psyco
    psyco.bind(Located.update)
    psyco.bind(calculateGravitationalAcceleration)
except ImportError:
    pass
