
from zope.interface import implements

from twisted.trial import unittest

from axiom import store, item, attributes

from imaginary import iimaginary, events, objects, commands, npc
from imaginary.test import commandutils


class MockIntelligence(item.Item):
    implements(iimaginary.IEventObserver)

    anAttribute = attributes.integer()
    concepts = attributes.inmemory()

    def activate(self):
        self.concepts = []


    def prepare(self, concept):
        return lambda: self.concepts.append(concept)


class IntelligenceTestCase(unittest.TestCase):
    def setUp(self):
        self.store = store.Store()

        self.location = objects.Thing(store=self.store, name=u"Place")
        self.locationContainer = objects.Container(store=self.store, capacity=1000)
        self.locationContainer.installOn(self.location)

        self.alice = objects.Thing(store=self.store, name=u"Alice")
        self.actor = objects.Actor(store=self.store)
        self.actor.installOn(self.alice)

        self.alice.moveTo(self.location)

        self.intelligence = MockIntelligence(store=self.store)
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
        self.clockContainer = objects.Container(store=self.store, capacity=10)
        self.clockContainer.installOn(self.clock)

        self.mouse = npc.createMouse(store=self.store, name=u"Squeaker McSqueakenson")
        self.mouseActor = iimaginary.IActor(self.mouse)
        self.mousehood = self.mouseActor.getIntelligence()
        self.mouse.moveTo(self.clock)

        self.player = objects.Thing(store=self.store, name=u"Mean Old Man")
        self.playerActor = objects.Actor(store=self.store)
        self.playerActor.installOn(self.player)
        self.playerIntelligence = MockIntelligence(store=self.store)
        self.playerActor.setEnduringIntelligence(self.playerIntelligence)

        self.player.moveTo(self.clock)


    def test_mouseSqueaksAtIntruders(self):
        """
        When a mean old man walks into the mouse's clock, the mouse will squeak
        ruthlessly.
        """
        evt = events.ArrivalEvent(thing=self.player, origin=None)
        self.mouseActor.send(evt)

        self.assertEquals(len(self.playerIntelligence.concepts), 1)
        event = self.playerIntelligence.concepts[0]
        self.assertEquals(
            commandutils.flatten(event.otherMessage.plaintext(self.player)),
            u"SQUEAK!")


    def test_mouseCanSqueak(self):
        commands.runEventTransaction(self.store, self.mousehood.squeak)
        self.assertEquals(len(self.playerIntelligence.concepts), 1)
        event = self.playerIntelligence.concepts[0]
        self.assertEquals(
            commandutils.flatten(event.otherMessage.plaintext(self.player)),
            u"SQUEAK!")



class MouseReactionTestCase(commandutils.CommandTestCaseMixin, unittest.TestCase):
    def testCreation(self):
        """
        Test that a mouse can be created with the create command.
        """
        self._test(
            "create mouse squeaker",
            ['Squeaker created.'],
            ['Test Player creates squeaker.'])

        [mouse] = list(self.playerContainer.getContents())
        self.failUnless(isinstance(iimaginary.IActor(mouse).getIntelligence(), npc.Mouse))


    def testSqueak(self):
        """
        Test that when someone walks into a room with a mouse, the mouse
        squeaks and the person who walked in hears it.
        """

        mouse = npc.createMouse(store=self.store, name=u"squeaker")

        elsewhere = objects.Thing(store=self.store, name=u"Mouse Hole")
        objects.Container(store=self.store, capacity=1000).installOn(elsewhere)

        objects.Exit.link(self.location, elsewhere, u"south")

        mouse.moveTo(elsewhere)

        self._test(
            "south",
            [commandutils.E("[ Mouse Hole ]"),
             commandutils.E("( north )"),
             commandutils.E("a squeaker"),
             commandutils.E("SQUEAK!")],
            ['Test Player leaves south.'])
