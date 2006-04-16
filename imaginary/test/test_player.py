from twisted.trial import unittest

from axiom import store

from imaginary import objects, events
from imaginary.wiring import player



class PlayerTest(unittest.TestCase):
    def setUp(self):
        self.store = store.Store()

        self.bob = objects.Thing(store=self.store, name=u"bob")
        self.actor = objects.Actor(store=self.store)
        self.actor.installOn(self.bob)

        self.player = player.Player(self.bob)
        self.player.useColors = False

        from twisted.test.proto_helpers import StringTransport
        self.transport = StringTransport()
        class Protocol:
            write = self.transport.write
        self.player.setProtocol(Protocol())


    def testSend(self):
        self.player.send(events.Success(actor=self.bob, actorMessage="Hi"))
        self.assertEquals(self.transport.value(), "Hi\n")
