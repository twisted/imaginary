
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
        player.moveTo(Container.createFor(place, capacity=1000))

        bauble = Thing(store=st, name=u"bauble")
        bauble.moveTo(player)

        Drop().runEventTransaction(player, None, dict(target=bauble.name))
        self.assertEquals(len([concept for concept
                               in intelligence.concepts
                               if isinstance(concept, ArrivalEvent)]), 1)
