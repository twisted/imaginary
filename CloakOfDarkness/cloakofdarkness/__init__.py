
"""
An Imaginary implementation of <http://www.firthworks.com/roger/cloak/>.
"""

from __future__ import unicode_literals

from zope.interface import implementer

import attr

from axiom.item import Item
from axiom.attributes import reference

from imaginary.world import ImaginaryWorld
from imaginary.events import Success
from imaginary.objects import Thing, Container, Exit
from imaginary.garments import createShirt
from imaginary.iimaginary import (
    IClothing,
    IClothingWearer,
    IWhyNot,
    ILitLink,
    IMovementRestriction,
    ILinkAnnotator,
)
from imaginary.enhancement import Enhancement


@implementer(ILinkAnnotator)
class CloakOfDarkness(Item, Enhancement):
    """
    A cloak of darkness cloaks an item in darkness as long as the cloak is
    worn.  Notably, the thing cloaked in darkness is independent of who wears
    the cloak.
    """
    powerupInterfaces = [ILinkAnnotator]

    # The target of the cloak of darkness.
    thing = reference()

    # The cloak itself.
    cloak = reference()

    def annotationsFor(self, link, idea):
        if link.target.delegate == self.thing:
            # The link is pointing towards the item we are intended to
            # conceal.

            # XXX wearer not on IClothing but needed
            if IClothing(self.cloak).wearer is not None:
                # The cloak is worn!  The effect is active.
                yield Darkness()


@implementer(ILitLink)
class Darkness(object):
    def isItLit(self, path):
        return False

    def applyLighting(self, litThing, eventualTarget, requestedInterface):
        return None

    # XXX whyNotLit not on ILitLink but used
    def whyNotLit(self):
        return None


@implementer(IMovementRestriction)
class ImpassableExit(Item, Enhancement):
    thing = reference()
    target = reference()

    powerupInterfaces = [IMovementRestriction]

    def movementImminent(self, movee, destination):
        return None


def world(store):
    foyer = Thing(store=store, name="Foyer")
    Container.createFor(foyer, capacity=1000)

    nowhere = Thing(store=store, name="nowhere")
    Container.createFor(nowhere, capacity=1000)
    Exit.link(foyer, nowhere, "north")
    ImpassableExit.createFor(foyer, target=nowhere)

    world = ImaginaryWorld(
        store=store,
        origin=foyer,
    )

    protagonist = world.create("Protagonist")
    cloak = createShirt(store=store, name="cloak", location=protagonist)
    wearer = IClothingWearer(protagonist)
    wearer.putOn(IClothing(cloak))

    bar = Thing(store=store, name="Bar")
    Container.createFor(bar, capacity=1000)
    Exit.link(foyer, bar, "south")

    cloakroom = Thing(store=store, name="Cloakroom")
    Container.createFor(cloakroom, capacity=1000)
    hook = Thing(store=store, name="hook", location=cloakroom, portable=False)
    Exit.link(foyer, cloakroom, "west")

    message = Thing(store=store, name="message", location=foyer)
    CloakOfDarkness.createFor(message, cloak=cloak)
    return world
