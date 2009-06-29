
from twisted.trial import unittest
from twisted.internet import task

from axiom import store

from imaginary import iimaginary, events, objects
from imaginary.test import commandutils

from examplegame import mice


class IntelligenceTestCase(unittest.TestCase):
    def setUp(self):
        self.store = store.Store()

        self.location = objects.Thing(store=self.store, name=u"Place")
        self.locationContainer = objects.Container.createFor(self.location, capacity=1000)

        self.alice = objects.Thing(store=self.store, name=u"Alice")
        self.actor = objects.Actor.createFor(self.alice)

        self.alice.moveTo(self.location)

        self.intelligence = commandutils.MockIntelligence(store=self.store)
        self.actor.setEnduringIntelligence(self.intelligence)


    def test_intelligenceReceivesEvent(self):
        """
        Enduring intelligences should receive events.
        """
        evt = events.Success(
            location=self.location,
            otherMessage=u"Hello, how are you?")

        self.actor.send(evt)
        self.assertEquals(self.intelligence.concepts, [evt])


    def test_persistentIntelligence(self):
        """
        Whitebox test that enduring intelligencii are actually persistent.
        """
        # TB <---- THAT MEANS IT'S TRANSLUCENT
        self.assertIdentical(
            self.store.findUnique(
                objects.Actor,
                objects.Actor._enduringIntelligence == self.intelligence),
            self.actor)



class MouseTestCase(unittest.TestCase):
    def setUp(self):
        self.store = store.Store()

        self.clock = objects.Thing(store=self.store, name=u"Clock")
        self.clockContainer = objects.Container.createFor(self.clock, capacity=10)

        self.mouse = mice.createMouse(store=self.store, name=u"Squeaker McSqueakenson")
        self.mouseActor = iimaginary.IActor(self.mouse)
        self.mousehood = self.mouseActor.getIntelligence()
        self.mouse.moveTo(self.clock)

        self.player = objects.Thing(store=self.store, name=u"Mean Old Man")
        self.playerActor = objects.Actor.createFor(self.player)
        self.playerIntelligence = commandutils.MockIntelligence(
            store=self.store)
        self.playerActor.setEnduringIntelligence(self.playerIntelligence)

        self.player.moveTo(self.clock)


    def test_mouseSqueaksAtIntruders(self):
        """
        When a mean old man walks into the mouse's clock, the mouse will squeak
        ruthlessly.
        """
        clock = task.Clock()
        self.mousehood._callLater = clock.callLater
        evt = events.ArrivalEvent(actor=self.player)
        self.mouseActor.send(evt)

        self.assertEquals(len(self.playerIntelligence.concepts), 0)
        clock.advance(0)

        self.assertEquals(len(self.playerIntelligence.concepts), 1)
        event = self.playerIntelligence.concepts[0]
        self.assertEquals(
            commandutils.flatten(event.otherMessage.plaintext(self.player)),
            u"SQUEAK!")


    def test_mouseCanSqueak(self):
        events.runEventTransaction(self.store, self.mousehood.squeak)
        self.assertEquals(len(self.playerIntelligence.concepts), 1)
        event = self.playerIntelligence.concepts[0]
        self.assertEquals(
            commandutils.flatten(event.otherMessage.plaintext(self.player)),
            u"SQUEAK!")


    def test_mouseActivation(self):
        """
        Activating a mouse should set the scheduling mechanism to the
        reactor's.
        """
        from twisted.internet import reactor
        self.assertEquals(self.mousehood._callLater, reactor.callLater)



class MouseReactionTestCase(commandutils.CommandTestCaseMixin,
                            unittest.TestCase):
    def testCreation(self):
        """
        Test that a mouse can be created with the create command.
        """
        self._test(
            "create the mouse named squeaker",
            ['You create squeaker.'],
            ['Test Player creates squeaker.'])

        [mouse] = list(self.playerContainer.getContents())
        self.failUnless(isinstance(iimaginary.IActor(mouse).getIntelligence(), mice.Mouse))


    def testSqueak(self):
        """
        Test that when someone walks into a room with a mouse, the mouse
        squeaks and the person who walked in hears it.
        """
        mouse = mice.createMouse(store=self.store, name=u"squeaker")
        clock = task.Clock()
        intelligence = iimaginary.IActor(mouse).getIntelligence()
        intelligence._callLater = clock.callLater

        elsewhere = objects.Thing(store=self.store, name=u"Mouse Hole")
        objects.Container.createFor(elsewhere, capacity=1000)

        objects.Exit.link(self.location, elsewhere, u"south")

        mouse.moveTo(elsewhere)

        self._test(
            "south",
            [commandutils.E("[ Mouse Hole ]"),
             commandutils.E("( north )"),
             commandutils.E("a squeaker")],
            ['Test Player leaves south.'])

        clock.advance(0)
        self._test(None, ["SQUEAK!"])
