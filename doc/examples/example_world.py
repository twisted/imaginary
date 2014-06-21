
from __future__ import unicode_literals

from imaginary.world import ImaginaryWorld
from imaginary.objects import Thing, Container, Exit
from imaginary.garments import createShirt, createPants
from imaginary.iimaginary import IClothing, IClothingWearer

from examplegame.squeaky import Squeaker


def world(store):
    def room(name):
        it = Thing(store=store, name=name)
        Container.createFor(it, capacity=1000)
        return it
    world = ImaginaryWorld(store=store,
                           origin=room("The Beginning"))
    protagonist = world.create("An Example Player")
    shirt = createShirt(store=store, name="shirt", location=world.origin)
    pants = createPants(store=store, name="pants", location=world.origin)
    middle = room("The Middle")
    wearer = IClothingWearer(protagonist)
    wearer.putOn(IClothing(shirt))
    wearer.putOn(IClothing(pants))
    Exit.link(world.origin, middle, "north")

    squeakerThing = Thing(name="squeaker", location=middle, store=store)
    Squeaker.createFor(squeakerThing)
    return world
