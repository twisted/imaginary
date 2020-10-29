
"""
Tests for L{imaginary.wiring.player}.
"""

from twisted.trial import unittest

from axiom import store

from imaginary import objects
from imaginary.objects import Container
from imaginary.wiring import player



class PlayerTest(unittest.TestCase):
    def setUp(self):
        self.store = store.Store()

        self.bob = objects.Thing(store=self.store, name=u"bob")
        self.room = objects.Thing(store=self.store, name=u"a place")
        roomContainer = Container.createFor(self.room, capacity=1000)
        self.bob.moveTo(roomContainer)

        self.actor = objects.Actor.createFor(self.bob)

        self.player = player.Player(self.bob)
        self.player.useColors = False

        from twisted.test.proto_helpers import StringTransport
        self.transport = StringTransport()
        class Protocol:
            write = self.transport.write
        self.player.setProtocol(Protocol())


    def testSend(self):
        self.player.send("Hi\n")
        self.assertEquals(self.transport.value(), "Hi\n")
        self.player.send(("Hi", "\n"))
        self.assertEquals(self.transport.value(), "Hi\nHi\n")
        self.player.send(["Hi", "\n"])
        self.assertEquals(self.transport.value(), "Hi\nHi\nHi\n")
        self.player.send(i for i in ("Hi", "\n"))
        self.assertEquals(self.transport.value(), "Hi\nHi\nHi\nHi\n")


    def testDisconnect(self):
        self.player.proto.terminal = None
        self.player.disconnect()
        self.assertIdentical(self.actor.getIntelligence(), None)


    def test_ambiguity(self):
        """
        When the player refers to something ambiguously, the error message
        should enumerate the objects in question.
        """
        for color in [u'red', u'green', u'blue']:
            it = objects.Thing(store=self.store, name=u'%s thing' % (color,))
            it.moveTo(self.room)

        self.player.parse("take thing")

        self.assertEquals(self.transport.value(),
                          "> take thing\n"
                          "Could you be more specific?  When you said 'thing', "
                          "did you mean: a red thing, a green thing, "
                          "or a blue thing?\r\n")
