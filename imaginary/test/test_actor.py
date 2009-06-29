from twisted.trial import unittest

from axiom import store

from imaginary import iimaginary, objects

from imaginary.test import commandutils


class ActorTest(unittest.TestCase, commandutils.LanguageMixin):
    def setUp(self):
        self.store = store.Store()

    def testPoweringUp(self):
        o = objects.Thing(store=self.store, name=u"wannabe")
        self.assertEquals(iimaginary.IActor(o, "hah"), "hah")
        a = objects.Actor.createFor(o)
        self.assertEquals(iimaginary.IActor(o, None), a)

    def testCondition(self):
        o = objects.Thing(store=self.store, name=u"wannabe")
        actor = objects.Actor.createFor(o)
        self.failUnless("great" in self.flatten(actor.conceptualize().plaintext(o)))

    def testHitPoints(self):
        o = objects.Thing(store=self.store, name=u"hitty")
        a = objects.Actor.createFor(o)
        self.assertEquals(a.hitpoints, 100)

    def testExperience(self):
        o = objects.Thing(store=self.store, name=u"hitty")
        a = objects.Actor.createFor(o)
        self.assertEquals(a.experience, 0)
        a.gainExperience(1100)
        self.assertEquals(a.experience, 1100)
        self.assertEquals(a.level, 10)

