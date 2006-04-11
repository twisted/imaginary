from twisted.trial import unittest

from axiom import store

from pottery import ipottery, objects
from pottery.wiring import realm

class RealmTestCase(unittest.TestCase):
    def setUp(self):
        self.store = store.Store()
        self.origin = objects.Object(store=self.store, name=u"origin")
        objects.Container(store=self.store, capacity=1000).installOn(self.origin)
        self.realm = realm.PotteryRealm(store=self.store)
        self.realm.installOn(self.store)


    def testPlayerCreation(self):
        player = self.realm.create(u"testuser", u"testpass")
        self.failUnless(ipottery.IActor.providedBy(ipottery.IActor(player, None)))
