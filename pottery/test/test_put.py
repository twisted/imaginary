
from twisted.trial import unittest

from pottery.test import commandutils
from pottery import ipottery, action, objects

class PutTestCase(commandutils.CommandTestCaseMixin, unittest.TestCase):
    def setUp(self):
        r = commandutils.CommandTestCaseMixin.setUp(self)
        self.object = objects.Object("foo")
        self.object.moveTo(self.player)
        self.container = objects.Container("bar")
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
        self.assertEquals(self.container.contents, [self.object])


    def testPutSelf(self):
        self._test(
            "put self in bar",
            ["That doesn't work."],
            [])
        self.assertIdentical(self.player.location, self.location)
        self.assertIn(self.player, self.location.contents)


    def testPutHere(self):
        self._test(
            "put here in bar",
            ["A thing cannot contain itself in euclidean space."],
            [])
        self.assertIdentical(self.location.location, None)
        self.assertNotIn(self.location, self.container.contents)


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
        self.assertEquals(self.container.contents, [])
        self.assertEquals(self.container.location, self.location)


    def testNestedContainment(self):
        another = objects.Container("another")
        self.container.add(another)

        self._test(
            "put bar in another",
            ["A thing cannot contain itself in euclidean space."],
            [])
        self.assertIdentical(another.location, self.container)
        self.assertEquals(self.container.contents, [another])


    def testIndirectNestedContainment(self):
        innermost = objects.Container("innermost")
        middle = objects.Container("middle")
        middle.add(innermost)
        self.container.add(middle)

        self._test(
            "put bar in innermost",
            ["A thing cannot contain itself in euclidean space."],
            [])
        self.assertIdentical(self.container.location, self.location)
        self.assertEquals(self.container.contents, [middle])
        self.assertIdentical(middle.location, self.container)
        self.assertEquals(middle.contents, [innermost])
        self.assertIdentical(innermost.location, middle)
        self.assertEquals(innermost.contents, [])


    def testPutClosed(self):
        self.container.closed = True
        self._test(
            "put foo in bar",
            ["bar is closed."])
        self.assertEquals(self.container.contents, [])
        self.assertIdentical(self.object.location, self.player)
