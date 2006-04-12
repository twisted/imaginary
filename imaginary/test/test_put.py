
from twisted.trial import unittest

from imaginary.test import commandutils
from imaginary import iimaginary, action, objects

class PutTestCase(commandutils.CommandTestCaseMixin, unittest.TestCase):
    def setUp(self):
        r = commandutils.CommandTestCaseMixin.setUp(self)
        self.object = objects.Object(store=self.store, name=u"foo")
        self.object.moveTo(self.player)
        self.container = objects.Object(store=self.store, name=u"bar")
        self.containerContainer = objects.Container(store=self.store, capacity=1)
        self.containerContainer.installOn(self.container)
        self.container.moveTo(self.location)
        return r

    def testPut(self):
        self._test(
            "put foo in bar",
            ["You put foo in bar."],
            ["Test Player puts foo in bar."])
        self.assertIdentical(self.player.location, self.location)
        self.assertIdentical(self.object.location, self.container)
        self.assertIdentical(self.container.location, self.location)
        self.assertEquals(list(self.containerContainer.getContents()), [self.object])


    def testPutSelf(self):
        self._test(
            "put self in bar",
            ["That doesn't work."],
            [])
        self.assertIdentical(self.player.location, self.location)
        self.assertIn(self.player, iimaginary.IContainer(self.location).getContents())


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
        another = objects.Object(store=self.store, name=u"another")
        objects.Container(store=self.store, capacity=1).installOn(another)
        self.containerContainer.add(another)

        self._test(
            "put bar in another",
            ["A thing cannot contain itself in euclidean space."],
            [])
        self.assertIdentical(another.location, self.container)
        self.assertEquals(list(self.containerContainer.getContents()), [another])


    def testIndirectNestedContainment(self):
        innermost = objects.Object(store=self.store, name=u"innermost")
        innermostContainer = objects.Container(store=self.store, capacity=1)
        innermostContainer.installOn(innermost)
        middle = objects.Object(store=self.store, name=u"middle")
        middleContainer = objects.Container(store=self.store, capacity=1)
        middleContainer.installOn(middle)
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


    def testPutClosed(self):
        self.containerContainer.closed = True
        self._test(
            "put foo in bar",
            ["bar is closed."])
        self.assertEquals(list(self.containerContainer.getContents()), [])
        self.assertIdentical(self.object.location, self.player)
