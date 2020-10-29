
"""
An Imaginary implementation of <http://www.firthworks.com/roger/cloak/>.
"""

from __future__ import unicode_literals

from zope.interface import implementer

from axiom.item import Item
from axiom.attributes import reference

from imaginary.world import ImaginaryWorld
from imaginary.events import Success
from imaginary.objects import Thing, Container, Exit
from imaginary.garments import createShirt
from imaginary.iimaginary import IClothing, IClothingWearer, IWhyNot, ILitLink, IMovementRestriction
from imaginary.enhancement import Enhancement


# XXX Make this an ILinkAnnotator instead (additionally?)
@implementer(IWhyNot, ILitLink)
class CloakOfDarkness(Item, Enhancement):
    thing = reference()
    message = reference()

    powerupInterfaces = [ILitLink]

    def tellMeWhyNot(self):
        return "You are overcome by the impression of disturbing things in the dark."

    def isItLit(self, path):
        return True


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

    message = Thing(store=store, name="message", location=foyer)

    protagonist = world.create("Protagonist")
    cloak = createShirt(store=store, name="cloak", location=protagonist)
    CloakOfDarkness.createFor(cloak, message=message)
    wearer = IClothingWearer(protagonist)
    wearer.putOn(IClothing(cloak))

    bar = Thing(store=store, name="Bar")
    Container.createFor(bar, capacity=1000)
    Exit.link(foyer, bar, "south")

    cloakroom = Thing(store=store, name="Cloakroom")
    Container.createFor(cloakroom, capacity=1000)
    hook = Thing(store=store, name="hook", location=cloakroom, portable=False)
    Exit.link(foyer, cloakroom, "west")

    return world
