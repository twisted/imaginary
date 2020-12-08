
from __future__ import unicode_literals

from imaginary.world import ImaginaryWorld
from imaginary.objects import Thing, Container, Exit
from imaginary.garments import createShirt, createPants
from imaginary.iimaginary import IClothing, IClothingWearer
from imaginary.manipulation import (
    Manipulator,
)

from examplegame.squeaky import Squeaker


def world(store):
    def room(name, description):
        it = Thing(
            store=store,
            name=name,
            description=description,
            proper=True,
            portable=False,
        )
        Container.createFor(it, capacity=1000)
        return it
    origin = room("The Beginning", "Everything here looks fresh and new.")
    world = ImaginaryWorld(store=store, origin=origin)
    protagonist = world.create("An Example Player")
    # Allow the protagonist to use the mildly privileged "manipulator"
    # actions.
    Manipulator.createFor(protagonist)

    shirt = createShirt(store=store, name="shirt", location=world.origin)
    pants = createPants(store=store, name="pants", location=world.origin)
    middle = room(
        "The Middle",
        "At first glance, this appears to be the center of things.",
    )
    wearer = IClothingWearer(protagonist)
    wearer.putOn(IClothing(shirt))
    wearer.putOn(IClothing(pants))
    Exit.link(world.origin, middle, "north")

    squeakerThing = Thing(name="squeaker", location=middle, store=store)
    Squeaker.createFor(squeakerThing)
    return world
