
"""
An Imaginary implementation of <http://www.firthworks.com/roger/cloak/>.

Quoting:

* The Foyer of the Opera House is where the game begins. This empty room has
  doors to the south and west, also an unusable exit to the north. There is
  nobody else around.

* The Bar lies south of the Foyer, and is initially unlit. Trying to do
  anything other than return northwards results in a warning message about
  disturbing things in the dark.

* On the wall of the Cloakroom, to the west of the Foyer, is fixed a small
  brass hook.

* Taking an inventory of possessions reveals that the player is wearing a
  black velvet cloak which, upon examination, is found to be
  light-absorbent. The player can drop the cloak on the floor of the Cloakroom
  or, better, put it on the hook.

* Returning to the Bar without the cloak reveals that the room is now lit. A
  message is scratched in the sawdust on the floor.

* The message reads either "You have won" or "You have lost", depending on how
  much it was disturbed by the player while the room was dark.

* The act of reading the message ends the game.
"""

from __future__ import (
    unicode_literals,
    print_function,
)

from zope.interface import implementer

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
)
from imaginary.enhancement import Enhancement


def world(store):
    foyer = Thing(store=store, name="Foyer")
    Container.createFor(foyer, capacity=1000)

    world = ImaginaryWorld(
        store=store,
        origin=foyer,
    )

    nowhere = Thing(store=store, name="nowhere")
    Container.createFor(nowhere, capacity=1000)
    Exit.link(foyer, nowhere, "north")

    message = Thing(store=store, name="message", location=foyer)

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

    return world
