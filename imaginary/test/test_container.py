# -*- test-case-name: imaginary.test -*-

from twisted.trial import unittest

from axiom import store

from imaginary import eimaginary, objects
from imaginary.test.commandutils import CommandTestCaseMixin, E

class ContainerTestCase(unittest.TestCase):
    def setUp(self):
        self.store = store.Store()
        self.containmentCore = objects.Thing(store=self.store, name=u"container")
        self.container = objects.Container.createFor(self.containmentCore, capacity=1)
        self.object = objects.Thing(store=self.store, name=u"object")


    def testAdd(self):
        """
        Test that successfully adding an object to a container properly adjusts
        the world graph - in particular, the contents list of the container and
        the location of the object.
        """
        self.container.add(self.object)
        self.assertEquals(list(self.container.getContents()), [self.object])
        self.assertIdentical(self.object.location, self.containmentCore)


    def testRemove(self):
        """
        Test that successfully removing an object from a container properly
        adjusts the world graph - in particular, the contents list of the
        container and the location of the object.
        """
        self.testAdd()
        self.container.remove(self.object)
        self.assertEquals(list(self.container.getContents()), [])
        self.assertIdentical(self.object.location, None)


    def testOverflowing(self):
        """
        Test the capacity feature of the container implementation as it
        interacts with the weight feature of the object implementation.
        """
        self.container.capacity = 1
        self.object.weight = 2
        self.assertRaises(eimaginary.DoesntFit, self.container.add, self.object)
        self.assertEquals(list(self.container.getContents()), [])
        self.assertIdentical(self.object.location, None)


    def testClosed(self):
        """
        Test the closed feature of the container implementation.
        """
        self.container.closed = True
        self.assertRaises(eimaginary.Closed, self.container.add, self.object)
        self.assertEquals(list(self.container.getContents()), [])
        self.assertIdentical(self.object.location, None)

        self.container.closed = False
        self.container.add(self.object)
        self.container.closed = True

        self.assertRaises(eimaginary.Closed, self.container.remove, self.object)
        self.assertEquals(list(self.container.getContents()), [self.object])
        self.assertIdentical(self.object.location, self.containmentCore)



class IngressAndEgressTestCase(CommandTestCaseMixin, unittest.TestCase):
    """
    I should be able to enter and exit containers that are sufficiently big.
    """

    def setUp(self):
        """
        Create a container, C{self.box} that is large enough to stand in.
        """
        CommandTestCaseMixin.setUp(self)
        self.box = objects.Thing(store=self.store, name=u'box')
        self.container = objects.Container.createFor(self.box, capacity=1000)
        self.box.moveTo(self.location)


    def test_enterBox(self):
        """
        I should be able to enter the box.
        """
        self.assertCommandOutput(
            'enter box',
            [E('[ Test Location ]'),
             'Location for testing.',
             'Here, you see Observer Player and a box.'],
            ['Test Player leaves into the box.'])


    def test_exitBox(self):
        """
        I should be able to exit the box.
        """
        self.player.moveTo(self.container)
        self.assertCommandOutput(
            'exit out',
            [E('[ Test Location ]'),
             'Location for testing.',
             'Here, you see Observer Player and a box.'],
            ['Test Player leaves out of the box.'])
        self.assertEquals(self.player.location,
                          self.location)


    def test_enterWhileHoldingBox(self):
        """
        When I'm holding a container, I shouldn't be able to enter it.
        """
        self.container.thing.moveTo(self.player)
        self.assertCommandOutput('enter box',
                                 ["The box won't fit inside itself."],
                                 [])

