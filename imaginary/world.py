# -*- test-case-name: imaginary.test.test_world -*-

"""
@see L{ImaginaryWorld}
"""

from axiom.item import Item
from axiom.attributes import inmemory, reference

from imaginary.iimaginary import IContainer
from imaginary.objects import Thing, Container, Actor
from imaginary.events import MovementArrivalEvent


class ImaginaryWorld(Item):
    """
    An instance of L{ImaginaryWorld} is a handle onto an Imaginary simulation.
    All connected users are tracked on this item, and new characters are
    created via the L{create} method.
    """
    origin = reference(
        doc="""
        The L{Thing} where all new characters will be placed.  It will be
        created in the first call to L{create} if it is not provided.
        """, reftype=Thing)

    connected = inmemory(
        doc="""
        A C{list} of L{Thing} instances which correspond to the users currently
        connected.
        """)


    def activate(self):
        self.connected = []


    def create(self, name, **kw):
        """
        Make a new character L{Thing} with the given name and return it.

        @type name: C{unicode}
        @rtype: L{Thing}
        """
        if self.origin is None:
            self.origin = Thing(store=self.store, name=u"The Place")
            Container.createFor(self.origin, capacity=1000)

        character = Thing(store=self.store, weight=100,
                          name=name, proper=True, **kw)
        Container.createFor(character, capacity=10)
        Actor.createFor(character)

        # Unfortunately, world -> garments -> creation -> action ->
        # world. See #2906. -exarkun
        from imaginary.garments import Wearer
        Wearer.createFor(character)

        character.moveTo(
            self.origin,
            lambda player: MovementArrivalEvent(
                thing=player, origin=None, direction=None))
        return character


    def loggedIn(self, character):
        """
        Indicate that a character is now participating in the simulation.
        """
        self.connected.append(character)


    def loggedOut(self, character):
        """
        Indicate that a character is no longer participating in the simulation.
        """
        self.connected.remove(character)
