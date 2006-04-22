
from twisted.trial import unittest

from axiom import store

from imaginary.wiring import realm
from imaginary import iimaginary, action

class TestIntelligence(object):
    def __init__(self):
        self.events = []

    def prepare(self, event):
        return lambda: self.events.append(event)


class WhoTestCase(unittest.TestCase):
    def setUp(self):
        self.store = store.Store()
        self.realm = realm.ImaginaryRealm(store=self.store)
        self.player = self.realm.create(u"testplayer", u"testpassword")
        self.actor = iimaginary.IActor(self.player)
        self.intelligence = TestIntelligence()
        self.actor.intelligence = self.intelligence
        self.others = []
        for i in xrange(5):
            self.others.append(self.realm.create(u"player-%d" % (i,), u"testpassword"))
        self.realm.loggedIn(self.player)


    def testWhoExpression(self):
        expr = action.ExpressWho(self.realm)
        crud = ''.join(list(expr.plaintext(self.player)))
        self.assertEquals(len(crud.splitlines()), 3, crud)


    def testOthersAsWell(self):
        for other in self.others:
            self.realm.loggedIn(other)
        expr = action.ExpressWho(self.realm)
        crud = ''.join(list(expr.plaintext(self.player)))
        self.assertEquals(len(crud.splitlines()), 8, crud)
        for player in self.others:
            self.failUnless(player.name in crud)


    def testEventReceived(self):
        action.Who().do(self.actor, "who")
        self.assertEquals(len(self.intelligence.events), 1)
        self.failUnless(isinstance(self.intelligence.events[0], action.ExpressWho))
        self.assertIdentical(self.intelligence.events[0].original, self.realm)
