from twisted.trial import unittest

from axiom import store

from pottery import ipottery, objects

def hate(l):
    if not isinstance(l, (tuple, list)):
        yield l
    else:
        for x in l:
            for crap in hate(x):
                yield crap


class ActorTest(unittest.TestCase):
    def setUp(self):
        self.store = store.Store()

    def testPoweringUp(self):
        o = objects.Object(store=self.store, name=u"wannabe")
        self.assertEquals(ipottery.IActor(o, "hah"), "hah")
        a = objects.Actor(store=self.store)
        a.installOn(o)
        self.assertEquals(ipottery.IActor(o, None), a)

    def testLongFormat(self):
        o = objects.Object(store=self.store, name=u"wannabe")
        objects.Actor(store=self.store).installOn(o)
        self.failUnless("great" in hate(o.longFormatTo(None)))

    def testHitPoints(self):
        o = objects.Object(store=self.store, name=u"hitty")
        a = objects.Actor(store=self.store)
        a.installOn(o)
        self.assertEquals(a.hitpoints, 100)

    def testExperience(self):
        o = objects.Object(store=self.store, name=u"hitty")
        a = objects.Actor(store=self.store)
        a.installOn(o)
        self.assertEquals(a.experience, 0)
        a.gainExperience(1100)
        self.assertEquals(a.experience, 1100)
        self.assertEquals(a.level, 10)

