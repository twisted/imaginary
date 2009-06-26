
"""
Tests for L{imaginary.world}.
"""

from twisted.trial.unittest import TestCase

from axiom.store import Store

from imaginary.iimaginary import IActor, IContainer, IClothingWearer
from imaginary.world import ImaginaryWorld


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
