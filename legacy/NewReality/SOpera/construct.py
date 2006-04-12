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
import random, math

# Sibling imports
import space, utils

def findOrbitalVelocity(primary, secondary):
    """findOrbitalVelocity(primary, secondary) -> float
    
    Determine the average velocity at which secondary will orbit primary
    """
    if max(primary.mass, secondary.mass) / min(primary.mass, secondary.mass) < 1000:
        raise Exception("Won't calculate radius for bodies with mass within 3 orders of magnitude")
    
    G = 6.667e-11
    a, b = secondary.getGravitationalAttraction(primary)
    r = secondary.coordinates.distance(primary)
    m = primary.mass
    v = ((G * m) / r) ** 0.5

def findOrbitalRadius(primary, secondary):
    """findOrbitalRadius(primary, secondary) -> float
    
    Determine the average distance at which secondary will orbit primary
    """
    if max(primary.mass, secondary.mass) / min(primary.mass, secondary.mass) < 1000:
        raise Exception("Won't calculate radius for bodies of mass within 3 orders of magnitude")
    
    G = 6.667e-11
    a, b = secondary.getGravitationalAttraction(primary)
    v = secondary.velocity.magnitude()
    m = primary.mass
    r = (G * m) / (v * 2)
    return r

def findOrbitalMass(primary, secondary):
    """findOrbitalMass(primary, secondary) -> float
    
    Determine the mass with which secondary will orbit primary
    """
    G = 6.667e-11
    m = primary.mass
    r = primary.coordinates.distance(secondary.coordinates)
    v = (secondary.velocity - primary.velocity).magnitude()
    m = (v * v * m * r) / G
    return m

def pickSolarMass():
    return (random.random() + 1) * (10 ** random.gauss(30, 2))

def pickSolarCoordinates():
    p = space.Point(random.random() - 0.5, random.random() - 0.5, random.random() - 0.5)
    return p.unit() * (random.random() * 1e10)

def generateDistances(count):
    # Planetary orbital distances are roughly fibinacci multiples
    d = random.random() * (10 ** random.gauss(9, 1))
    print d
    r = [d]
    for i in utils.fibonacci(count):
        r.append(r[-1] * i * random.gauss(1, 0.05))
        print r[-1]
    return tuple(r)

def pickPlanetaryVelocity(mass):
    # Bigger things should move more slowly
    return (random.random() + 1) * (10 ** random.gauss(5, 1))

def makeSystem(name, types, numPlanets = 5, planetNames = None, reality = ''):
    if planetNames is None:
        planetNames = []
    else:
        planetNames = planetNames[:]
    planetNames.extend(['%s %d' % (name, i + 1) for i in range(len(planetNames), numPlanets)])

    m = space.Point()
    system = space.StellarThing(name + ' System', reality)
    s = space.Star(name, pickSolarMass(), reality)
    s.coordinates = pickSolarCoordinates()
    s.location = system

    r = generateDistances(numPlanets)
    for i in planetNames:
        x = [random.random() * 0.01 - 0.005 for j in range(4)]
        p = random.choice(types)(i, reality)
        p.velocity = space.Point(x[0], pickPlanetaryVelocity(p.mass), x[1])
        p.coordinates = space.Point(x[2], r[0], x[3])
        p.mass = findOrbitalMass(s, p)
        r = r[1:]
        p.location = system
        m = m + (p.velocity / p.mass)
           
    # Counter the momentum of all the planets with solar momentum
    s.velocity = -m / s.mass

    return system
