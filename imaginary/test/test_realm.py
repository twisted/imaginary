from twisted.trial import unittest

from axiom import store

from imaginary import iimaginary, objects
from imaginary.wiring import realm

class RealmTestCase(unittest.TestCase):
    def setUp(self):
        self.store = store.Store()
        self.origin = objects.Thing(store=self.store, name=u"origin")
        objects.Container(store=self.store, capacity=1000).installOn(self.origin)
        self.realm = realm.ImaginaryRealm(store=self.store)
        self.realm.installOn(self.store)


    def testPlayerCreation(self):
        player = self.realm.create(u"testuser", u"testpass")
        self.failUnless(iimaginary.IActor.providedBy(iimaginary.IActor(player, None)))
