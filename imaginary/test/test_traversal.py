
from twisted.trial import unittest

from axiom.store import Store

from imaginary.places import Thing
from imaginary.iimaginary import IVisible

class BasicVisibility(unittest.TestCase):
    # Ordering actually is important.
    # The rule is:

    # Me first
    # in before out
    # out before over
    # over until distance

    def testOneRoom(self):

        s = Store()

        room = Thing(store=s)

        table = Thing(store=s,
                      location=room)

        guy = Thing(store=s,
                    location=room)

        bauble = Thing(store=s,
                       location=guy)

        book = Thing(store=s,
                     location=table)

        self.assertEquals(list(guy.findProviders(IVisible)),
                          [guy, bauble, room, table, book])

    def testTwoRooms(self):
        s = Store()

        here = Thing(store=s, baseName=u'here')

        there = Thing(store=s, baseName=u'there')

        here.createTwoWayExit(u'north', there)

        me = Thing(store=s, location=here, baseName=u'me')

        self.assertEquals(list(me.findProviders(IVisible)),
                          [me, here, there])

    def testThreeRooms(self):
        s = Store()

        here = Thing(store=s)
        there = Thing(store=s)
        everywhere = Thing(store=s)

        here.createTwoWayExit(u'north', there)
        there.createTwoWayExit(u'north', everywhere)

        garbage = Thing(store=s, location=everywhere)
        me = Thing(store=s, location=here)

        self.assertEquals(list(me.findProviders(IVisible)),
                          [me, here, there])
