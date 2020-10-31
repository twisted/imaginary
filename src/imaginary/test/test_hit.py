
from twisted.trial import unittest

from imaginary.test import commandutils
from imaginary.test.commandutils import E

from imaginary import objects, iimaginary

class HitTestCase(commandutils.CommandTestCaseMixin, unittest.TestCase):
    def testHit(self):
        self._test(
            "hit self",
            [E("Hit yourself?  Stupid.")])

        self._test(
            "hit foobar",
            [E("Who's that?")])

        actor = iimaginary.IActor(self.player)
        actor.stamina.current = 0
        self._test(
            "hit Observer Player",
            ["You're too tired!"])

        actor.stamina.current = actor.stamina.max

        x, y = self._test(
            "hit Observer Player",
            ["You hit Observer Player for (\\d+) hitpoints."],
            ["Test Player hits you for (\\d+) hitpoints."])
        self.assertEquals(x[1].groups(), y[0].groups())

        actor.stamina.current = actor.stamina.max

        x, y = self._test(
            "attack Observer Player",
            ["You hit Observer Player for (\\d+) hitpoints."],
            ["Test Player hits you for (\\d+) hitpoints."])
        self.assertEquals(x[1].groups(), y[0].groups())


        monster = objects.Thing(store=self.store, name=u"monster")
        objects.Actor.createFor(monster)
        monster.moveTo(self.location)
        x, y = self._test(
            "hit monster",
            ["You hit the monster for (\\d+) hitpoints."],
            ["Test Player hits a monster."])
        monster.destroy()


    def testInvalidAttacks(self):
        self._test(
            "hit here",
            [E("Who's that?")],
            [])

        obj = objects.Thing(store=self.store, name=u"quiche")
        obj.moveTo(self.location)
        self._test(
            "hit quiche",
            [E("Who's that?")],
            [])
