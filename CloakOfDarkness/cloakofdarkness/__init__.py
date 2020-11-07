
"""
An Imaginary implementation of <http://www.firthworks.com/roger/cloak/>.

Quoting:

* The Foyer of the Opera House[1] is where the game begins[2]. This empty[3]
  room[4] has doors to the south and west, also an unusable exit to the
  north[5]. There is nobody else around[6].

* The Bar[7] lies south[8] of the Foyer, and is initially unlit[9]. Trying to
  do anything other than return northwards results in a warning message about
  disturbing things in the dark[10].

* On the wall of the Cloakroom[11], to the west of the Foyer[12], is fixed a
  small brass hook[13].

* Taking an inventory of possessions reveals that the player is wearing[16] a
  black velvet cloak[14] which, upon examination, is found to be
  light-absorbent[15]. The player can drop the cloak on the floor of the
  Cloakroom or, better, put it on the hook.

* Returning to the Bar without the cloak reveals that the room is now lit. A
  message[16] is scratched in the sawdust on the floor.

* The message reads either "You have won"[17] or "You have lost", depending on how
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
from imaginary.objects import (
    Thing,
    Container,
    Exit,
    LocationLighting,
)
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
    foyer = Thing(
        store=store,
        # [1]
        name="The Foyer of the Opera House",
        # [3], [6]
        description="This is an empty room.  There is nobody else around.",
    )
    # [4]
    Container.createFor(foyer, capacity=1000)

    world = ImaginaryWorld(
        store=store,
        # [2]
        origin=foyer,
    )

    nowhere = Thing(store=store, name="nowhere")
    Container.createFor(nowhere, capacity=1000)
    # [5]
    Exit.link(foyer, nowhere, "north")

    bar = Thing(
        store=store,
        # [7]
        name="The Bar",
    )
    Container.createFor(bar, capacity=1000)
    # [8]
    Exit.link(foyer, bar, "south")
    # [9]
    LocationLighting.createFor(bar, candelas=0)

    # [16]
    message = Thing(
        store=store,
        name="message",
        location=bar,
        description=(
            # [17]
            "Scratched into the sawdust on the floor, the words 'You have won.'"
        ),
    )

    # [11]
    cloakroom = Thing(store=store, name="Cloakroom")
    Container.createFor(cloakroom, capacity=1000)
    # [12]
    Exit.link(foyer, cloakroom, "west")

    # [13]
    hook = Thing(
        store=store,
        name="small brass hook",
        description="It is fixed to the wall.",
        location=cloakroom,
        portable=False,
    )

    protagonist = world.create("Protagonist")
    # [14]
    cloak = createShirt(
        store=store,
        name="black velvet cloak",
        location=protagonist,
        # [15]
        description="It seems to absorb light.",
    )
    # [16]
    wearer = IClothingWearer(protagonist)
    wearer.putOn(IClothing(cloak))

    return world
