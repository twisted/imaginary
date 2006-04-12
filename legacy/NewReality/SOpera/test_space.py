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
import unittest, time

# Reality imports
from Reality import thing

# Sibling imports
import space, construct

INCR = 1

class TimedLocated(space.Located):
    t = 0
    i = 1
    
    def __init__(self, initial = 0, increment = 1):
        self.t, self.i = initial, increment

    def getTime(self):
        return self.t

    def advanceTime(self):
        self.t = self.t + self.i

class StellarThing(thing.Thing, TimedLocated):
    pass

space.StellarThing = StellarThing


class PointTestCase(unittest.TestCase):
    def testEquality(self):
        assert space.Point(1, 1, 1) == space.Point(1, 1, 1)
        assert space.Point(1.0, 1.0, 1.0) == space.Point(1.0, 1.0, 1.0)
        assert space.Point(10, 0, 0) != space.Point(-10, 0, 0)
    
    def testLength(self):
        assert len(space.Point(1, 2, 3)) == 3

    def testNegation(self):
        assert space.Point(2, 5, -3) == -space.Point(-2, -5, 3)
    
    def testAddition(self):
        assert space.Point(1, -1, 0) == (space.Point(0, 0, 0) + space.Point(1, -1, 0))

    def testSubtraction(self):
        assert space.Point(1, -1, 0) == (space.Point(2, 0, 1) - space.Point(1, 1, 1))

    def testMultiplication(self):
        assert space.Point(1, 2, 3) * 5 == space.Point(5, 10, 15)
    
    def testDivision(self):
        assert space.Point(5, 10, 15) / 5 == space.Point(1, 2, 3)

    def testMagnitude(self):
        assert space.Point(1, 2, 3).magnitude() == (14 ** 0.5)

    def testDistance(self):
        assert space.Point(5, 0, 0).distance(space.Point(0, 5, 0)) == (50 ** 0.5)
    
    def testPolar(self):
        p = space.Point(11, 24, 101)
        assert space.Point.fromPolar(*p.toPolar()) == p


class AccelerationTestCase(unittest.TestCase):
    def testAcceleration(self):
        x = TimedLocated(0, 1)

        x.acceleration = space.Point(10, 0, 0)
        x.advanceTime()
        
        x.acceleration = space.Point(-10, 10, 0)
        x.advanceTime()
        
        x.acceleration = space.Point(0, -10, 10)
        x.advanceTime()
        
        x.acceleration = space.Point(0, 0, -10)
        x.advanceTime()
        
        x.acceleration = space.Point(1, 1, 1)
        x.advanceTime()
        
        x.acceleration = space.Point(0, 0, 0)
        x.advanceTime()

        x.advanceTime()
        x.advanceTime()
        x.advanceTime()
        x.update()

        assert x.acceleration == space.Point(0, 0, 0)
        assert x.velocity == space.Point(0.5, 0.5, 0.5)
        assert x.coordinates == space.Point(7.5, 7.5, 7.5)

class GravityTestCase(unittest.TestCase):
    def testGravitation(self):
        Moo().testGravitation()

class Moo:
    def testGravitation(self):
        s = construct.makeSystem('Sol', [space.World], 5)
        things = filter(lambda x: isinstance(x, TimedLocated), s.get_things())
        e = space.calculateTotalEnergy(things)
        for i in xrange(0, 60 * 60 * 24 * 365, INCR):
            A = space.calculateGravitationalAcceleration(things)
            for a, o in zip(A, things):
                o.acceleration = a
                o.advanceTime()
                o.update()


            if i % (60 * 60 * 24) == 0:
                print 'd =', (i / (60 * 60 * 24))
                for j in things:
                    print j.name
                    print """Coords:       %-50s Distance from Sun: %s
Velocity:     %-50s Speed:             %s
Acceleration: %-50s Magnitude:         %s
""" % (j.coordinates, j.coordinates.magnitude(), j.velocity, j.velocity.magnitude(), j.acceleration, j.acceleration.magnitude())
                e, le = space.calculateTotalEnergy(things), e
                print "Percent energy change (J):", (e - le) / le


testCases = [PointTestCase, AccelerationTestCase, GravityTestCase]

if __name__ == '__main__':
    unittest.main()
