
"""
Tests for L{imaginary.world}.
"""

from twisted.trial.unittest import TestCase
from twisted.test.proto_helpers import StringTransport

from axiom.store import Store

from imaginary.iimaginary import IActor, IContainer, IClothingWearer
from imaginary.wiring.player import Player
from imaginary.world import ImaginaryWorld
from imaginary.test.commandutils import PlayerProtocol


class ImaginaryWorldTests(TestCase):
    """
    Tests for L{ImaginaryWorld} which is responsible for adding new characters
    to the simulation and keeping track of active characters.
    """
    def test_create(self):
        """
        L{ImaginaryWorld.create} returns a L{Thing} which is adaptable to
        L{IActor}, L{IContainer}, and L{IClothingWearer} and which is contained
        by the world's C{origin} L{Thing}.
        """
        name = u"foo"
        store = Store()
        world = ImaginaryWorld(store=store)
        character = world.create(name)
        self.assertEqual(character.name, name)
        self.assertTrue(IContainer(world.origin).contains(character))
        self.assertNotIdentical(IActor(character, None), None)
        self.assertNotIdentical(IContainer(character, None), None)
        self.assertNotIdentical(IClothingWearer(character, None), None)


    def test_creationEvent(self):
        """
        When a new L{Thing} is created via L{ImaginaryWorld.create}, its
        addition to L{ImaginaryWorld.origin} is broadcast to that location.
        """
        store = Store()
        world = ImaginaryWorld(store=store)
        observer = world.create(u"observer")

        # There really needs to be a way to get into the event dispatch
        # system.  It's so hard right now that I'm not even going to try,
        # instead I'll look at some strings that get written to a transport.
        observingPlayer = Player(observer)
        transport = StringTransport()
        observingPlayer.setProtocol(PlayerProtocol(transport))

        # Make another thing for the observer to watch the creation of.
        world.create(u"foo")

        self.assertEquals(transport.value(), "Foo arrives.\n")
