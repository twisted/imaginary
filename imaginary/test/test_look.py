
from twisted.trial import unittest

from axiom import store
from axiom.dependency import installOn

from imaginary import iimaginary, objects, language, action, events
from imaginary.world import ImaginaryWorld
from imaginary.test import commandutils


class TestIntelligence(object):
    def __init__(self):
        self.observedConcepts = []


    def prepare(self, concept):
        return lambda: self.observedConcepts.append(concept)



class LookTestCase(unittest.TestCase):
    def setUp(self):
        self.store = store.Store()

        self.location = objects.Thing(
            store=self.store,
            name=u"Test Location",
            description=u"Location for testing.",
            proper=True)

        locContainer = objects.Container(store=self.store, capacity=1000)
        installOn(locContainer, self.location)

        self.world = ImaginaryWorld(store=self.store)
        self.player = self.world.create(u"Test Player", gender=language.Gender.FEMALE)
        locContainer.add(self.player)
        self.actor = iimaginary.IActor(self.player)
        self.actor.setEphemeralIntelligence(TestIntelligence())


    def testLookAroundEventBroadcasting(self):
        action.LookAround().runEventTransaction(self.actor, u"look", {})
        evts = self.actor.getIntelligence().observedConcepts
        self.assertEquals(len(evts), 1)
        self.failUnless(isinstance(evts[0], events.Success))


    def testLookAtExitNameEventBroadcasting(self):
        target = objects.Thing(
            store=self.store,
            name=u"Visible Location",
            description=u"Description of visible location.",
            proper=True)
        targetContainer = objects.Container(store=self.store, capacity=1000)
        installOn(targetContainer, target)

        objects.Exit.link(self.location, target, u"south")

        action.LookAt().runEventTransaction(self.actor, u"look", {"target": u"south"})
        evts = self.actor.getIntelligence().observedConcepts
        self.assertEquals(len(evts), 1)
        self.failUnless(isinstance(evts[0], events.Success))
        self.assertEquals(
            commandutils.flatten(evts[0].actorMessage.plaintext(self.actor)),
            u"[ Visible Location ]\n( north )\nDescription of visible location.\n")
