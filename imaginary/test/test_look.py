"""
Tests for L{imaginary.action.LookAt} and L{imaginary.action.LookAround}.
"""
from twisted.trial.unittest import TestCase

from axiom import store

from imaginary import iimaginary, objects, language, action, events
from imaginary.world import ImaginaryWorld
from imaginary.test.commandutils import (
    CommandTestCaseMixin, E, createLocation, flatten)


class TestIntelligence(object):
    def __init__(self):
        self.observedConcepts = []


    def prepare(self, concept):
        return lambda: self.observedConcepts.append(concept)



class LookContext(object):
    def __init__(self):
        self.store = store.Store()

        locContainer = createLocation(
            self.store, name=u"Test Location",
            description=u"Location for testing.")
        self.location = locContainer.thing

        self.world = ImaginaryWorld(store=self.store)
        self.player = self.world.create(u"Test Player", gender=language.Gender.FEMALE)
        locContainer.add(self.player)
        self.actor = iimaginary.IActor(self.player)
        self.actor.setEphemeralIntelligence(TestIntelligence())



class LookAroundTranscriptTests(CommandTestCaseMixin, TestCase):
    """
    Transcript-style tests for I{look}.
    """
    def test_emptyLocation(self):
        iimaginary.IContainer(self.location).remove(self.observer)
        self._test(
            u"look",
            [E(u"[ Test Location ]"),
             u"Location for testing.",
             ])


    def test_siblingObject(self):
        self._test(
            "look",
            [E(u"[ Test Location ]"),
             u"Location for testing.",
             u"Here, you see Observer Player."])


    def test_cousinObject(self):
        o = objects.Thing(store=self.store, name=u"foo")
        iimaginary.IContainer(self.observer).add(o)
        self._test(
            "look",
            [E(u"[ Test Location ]"),
             u"Location for testing.",
             u"Here, you see Observer Player."])


    def test_childObject(self):
        o = objects.Thing(store=self.store, name=u"foo")
        self.playerContainer.add(o)
        self._test(
            "look",
            [E(u"[ Test Location ]"),
             u"Location for testing.",
             u"Here, you see Observer Player."])


    def test_equipment(self):
        self.observer.moveTo(None)
        self._test(u"create a shirt named t-shirt", [u"You create a t-shirt."])
        self._test(u"wear t-shirt", [u"You put on the t-shirt."])
        self._test(
            u"look",
            [E(u"[ Test Location ]"),
             E(u"Location for testing.")])



class LookAtTranscriptTests(CommandTestCaseMixin, TestCase):
    def test_exits(self):
        objects.Exit.link(self.location, self.location, u"north")
        self._test(
            "look here",
            [E("[ Test Location ]"),
             E("( north south )"),
             "Location for testing.",
             "Here, you see Observer Player."])


    def test_lookMe(self):
        self._test(
            "look me",
            [E("[ Test Player ]"),
             "Test Player is great.",
             "She is naked."])


    def test_lookAtMe(self):
        self._test(
            "look at me",
            [E("[ Test Player ]"),
             "Test Player is great.",
             "She is naked."])


    def test_lookAtAnother(self):
        self._test(
            "look at Observer Player",
            [E("[ Observer Player ]"),
             "Observer Player is great.",
             "She is naked."],
            ["Test Player looks at you."])


    def test_lookAtThing(self):
        o = objects.Thing(store=self.store, name=u"foo")
        iimaginary.IContainer(self.location).add(o)
        self._test(
            "look at foo",
            [E("[ foo ]")])


    def test_lookAtMissing(self):
        self._test(
            "look at bar",
            ["You don't see that."])



class LookAroundTests(TestCase):
    """
    Tests for L{imaginary.action.LookAround}.
    """
    def setUp(self):
        self.context = LookContext()


    def test_eventBroadcasting(self):
        """
        The L{LookAround} action broadcasts an L{events.Success} to the actor.
        """
        action.LookAround().runEventTransaction(
            self.context.player, u"look", {})
        [event] = self.context.actor.getIntelligence().observedConcepts
        self.assertIsInstance(event, events.Success)



class LookAtTests(TestCase):
    """
    Tests for L{imaginary.action.LookAt}.
    """
    def setUp(self):
        self.context = LookContext()


    def test_exitNameEventBroadcasting(self):
        target = objects.Thing(
            store=self.context.store,
            name=u"Visible Location",
            description=u"Description of visible location.",
            proper=True)
        objects.Container.createFor(target, capacity=1000)
        objects.Exit.link(self.context.location, target, u"south")

        action.LookAt().runEventTransaction(
            self.context.player, u"look", {"target": u"south"})
        evts = self.context.actor.getIntelligence().observedConcepts
        self.assertEqual(1, len(evts))
        self.assertIsInstance(evts[0], events.Success)
        self.assertEqual(
            u"[ Visible Location ]\n( north )\nDescription of visible location.\n",
            flatten(evts[0].actorMessage.plaintext(self.context.actor)))



class LookAroundTests(TestCase):
    pass

