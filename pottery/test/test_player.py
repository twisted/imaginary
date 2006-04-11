from zope.interface import implements

from twisted.trial import unittest
from twisted.python.util import unsignedID

from axiom import store

from pottery import objects, events, ipottery
from pottery.wiring import player


class Formattable:
    implements(ipottery.IDescribeable)

    def formatTo(self, what):
        return 'shortFormatTo(%X)' % (unsignedID(what),)


    def longFormatTo(self, what):
        raise NotImplementedError("This isn't tested here.")


class PlayerTest(unittest.TestCase):
    def setUp(self):
        self.store = store.Store()

        self.bob = objects.Object(store=self.store, name=u"bob")
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

    def testFormatting(self):
        obj = objects.Object(store=self.store, name=u"name", description=u"descr")
        self.assertEquals(self.player.format(obj), "name")

        longFormat = self.player.format(obj.longFormatTo(self.player))
        self.assertEquals(
            longFormat,
            "[ name ]\n"
            "descr\n")

    def testShortFormatTo(self):
        self.assertEquals(
            self.player.format('hello'),
            'hello')

        self.assertEquals(
            self.player.format(('hello', 'world')),
            'helloworld')

        self.assertEquals(
            self.player.format((1, 2, 3)),
            '123')

        self.assertEquals(
            self.player.format(('hello', (1, 2, 3), 'world')),
            'hello123world')

        def gen():
            for i in range(3):
                yield i
        self.assertEquals(
            self.player.format(('hello', gen(), 'world')),
            'hello012world')

        self.assertEquals(
            self.player.format(('hello', Formattable())),
            'helloshortFormatTo(' + hex(unsignedID(self.player)).upper()[2:].rstrip('L') + ')')
