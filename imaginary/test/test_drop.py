
from twisted.trial.unittest import TestCase

from axiom.store import Store

from imaginary.test.commandutils import createPlayer
from imaginary.objects import Thing, Container
from imaginary.action import Drop
from imaginary.events import ArrivalEvent


class DropTestCase(TestCase):
    def test_arrivalEvent(self):
        """
        Test that when a thing is dropped, an ArrivalEvent instance is
        broadcast to the room it is dropped into.
        """
        st = Store()

        player, actor, intelligence = createPlayer(st, u"Foo")
        place = Thing(store=st, name=u"soko")
        Container(store=st, capacity=1000).installOn(place)
        player.moveTo(place)

        bauble = Thing(store=st, name=u"bauble")
        bauble.moveTo(player)

        Drop().do(player, None, bauble)
        self.assertEquals(len(intelligence.concepts), 1)
        self.failUnless(isinstance(intelligence.concepts[0], ArrivalEvent))
