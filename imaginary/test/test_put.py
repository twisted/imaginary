
from twisted.trial import unittest

from imaginary.test import commandutils
from imaginary import objects

class PutTestCase(commandutils.CommandTestCaseMixin, unittest.TestCase):
    def setUp(self):
        r = commandutils.CommandTestCaseMixin.setUp(self)
        self.object = objects.Thing(store=self.store, name=u"foo")
        self.object.moveTo(self.player)
        self.container = objects.Thing(store=self.store, name=u"bar")
        self.containerContainer = objects.Container.createFor(self.container, capacity=1)
        self.container.moveTo(self.location)
        return r


    def test_put(self):
        """
        The I{put} action changes the location of a thing from the actor's
        inventory to the specified container.
        """
        self._test(
            "put foo in bar",
            ["You put the foo in the bar."],
            ["Test Player puts a foo in a bar."])
        self.assertIdentical(self.player.location, self.location)
        self.assertIdentical(self.object.location, self.container)
        self.assertIdentical(self.container.location, self.location)
        self.assertEquals(list(self.containerContainer.getContents()), [self.object])


    def testPutHere(self):
        self._test(
            "put here in bar",
            ["A thing cannot contain itself in euclidean space."],
            [])
        self.assertIdentical(self.location.location, None)
        self.assertNotIn(self.location, self.containerContainer.getContents())


    def testPutNonContainer(self):
        self._test(
            "put bar in foo",
            ["That doesn't work."],
            [])
        self.assertIdentical(self.container.location, self.location)


    def testPutRecursive(self):
        self._test(
            "put bar in bar",
            ["A thing cannot contain itself in euclidean space."],
            [])
        self.assertEquals(list(self.containerContainer.getContents()), [])
        self.assertEquals(self.container.location, self.location)


    def testNestedContainment(self):
        another = objects.Thing(store=self.store, name=u"another")
        objects.Container.createFor(another, capacity=1)
        self.containerContainer.add(another)

        self._test(
            "put bar in another",
            ["A thing cannot contain itself in euclidean space."],
            [])
        self.assertIdentical(another.location, self.container)
        self.assertEquals(list(self.containerContainer.getContents()), [another])


    def testIndirectNestedContainment(self):
        innermost = objects.Thing(store=self.store, name=u"innermost")
        innermostContainer = objects.Container.createFor(innermost, capacity=1)
        middle = objects.Thing(store=self.store, name=u"middle")
        middleContainer = objects.Container.createFor(middle, capacity=1)
        middleContainer.add(innermost)
        self.containerContainer.add(middle)

        self._test(
            "put bar in innermost",
            ["A thing cannot contain itself in euclidean space."],
            [])
        self.assertIdentical(self.container.location, self.location)
        self.assertEquals(list(self.containerContainer.getContents()), [middle])
        self.assertIdentical(middle.location, self.container)
        self.assertEquals(list(middleContainer.getContents()), [innermost])
        self.assertIdentical(innermost.location, middle)
        self.assertEquals(list(innermostContainer.getContents()), [])


    def test_putClosedFails(self):
        """
        The I{put} action fails if the specified container is closed.
        """
        self.containerContainer.closed = True
        self._test(
            "put foo in bar",
            ["The bar is closed."])
        self.assertEquals(list(self.containerContainer.getContents()), [])
        self.assertIdentical(self.object.location, self.player)


    def test_putFullFails(self):
        """
        The I{put} action fails if the specified container is full.
        """
        self.containerContainer.capacity = 1
        self.object.weight = 2
        self._test(
            "put foo in bar",
            ["The foo does not fit in the bar."])
        self.assertEquals(list(self.containerContainer.getContents()), [])
        self.assertIdentical(self.object.location, self.player)
