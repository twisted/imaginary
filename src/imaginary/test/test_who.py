
from twisted.trial import unittest

from axiom import store

from imaginary import iimaginary, action
from imaginary.test import commandutils
from imaginary.world import ImaginaryWorld


class WhoTestCase(unittest.TestCase):
    """
    Tests for L{ExpressWho} and the I{who} command.
    """
    def setUp(self):
        """
        Create a store and an Imaginary world and populate it with a number
        of players, one of which is equipped to record the events it
        receives.
        """
        self.store = store.Store()
        self.world = ImaginaryWorld(store=self.store)
        self.others = []
        for i in xrange(5):
            self.others.append(self.world.create(u"player-%d" % (i,)))
        self.player = self.world.create(u"testplayer")
        self.actor = iimaginary.IActor(self.player)
        self.intelligence = commandutils.MockEphemeralIntelligence()
        self.actor.setEphemeralIntelligence(self.intelligence)
        self.world.loggedIn(self.player)


    def testWhoExpression(self):
        expr = action.ExpressWho(self.world)
        crud = ''.join(list(expr.plaintext(self.player)))
        self.assertEquals(len(crud.splitlines()), 3, crud)


    def testOthersAsWell(self):
        for other in self.others:
            self.world.loggedIn(other)
        expr = action.ExpressWho(self.world)
        crud = ''.join(list(expr.plaintext(self.player)))
        self.assertEquals(len(crud.splitlines()), 8, crud)
        for player in self.others:
            self.failUnless(player.name in crud)


    def testEventReceived(self):
        action.Who().do(self.actor, "who")
        self.assertEquals(len(self.intelligence.events), 1)
        self.failUnless(isinstance(self.intelligence.events[0], action.ExpressWho))
        self.assertIdentical(self.intelligence.events[0].original, self.world)
