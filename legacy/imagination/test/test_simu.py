
from twisted.trial import unittest

from imagination import simulacrum
from imagination.simulacrum import ICollector, collect, always
from imagination.containment import Container, ILocatable, ILinkable
from imagination.architecture import IExit
from imagination.templates import basic
from imagination.facets import Facet

from zope.interface import Interface

class IRoach(Interface):
    pass
class Roachable(Facet):
    pass

class IKey(Interface):
    pass
class Keyable(Facet):
    pass

Roach = basic.Thing[
    IRoach: Roachable,
    ]

Key = basic.Thing[
    IKey: Keyable,
    ]

from imagination.text.english import INoun

class CockroachTesta1(unittest.TestCase):
    """
    A demonstration of the infamous brass cockroach, reprising its role as the
    world's most obscure and infuriating containment test.
    """

    def setUp(self):
        me = basic.Actor.fill(INoun, name="bob").new()
        me = basic.Actor.fill(INoun, name='bob').new()
        ball = basic.Thing.fill(INoun, name='bouncy ball').new()

        key = Key.fill(INoun, name='gold key').new()
        roach = Roach.new()
        roach2 = Roach.new()
        room1 = basic.Room.new()
        room2 = basic.Room.new()
        room3 = basic.Room.new()

        door1 = basic.Door.fill(IExit, closed=False).new()
        door2 = basic.Door.fill(IExit, closed=False).new()
        # print door1.closed, door2.closed
        table = basic.Thing.new()
        book = basic.Book.new()

        ICollector(me).grab(key)
        ICollector(me).link(0, room1)
        ICollector(room1).grab(ball)

        IExit(door1).between(room1, room2)
        IExit(door2).between(room2, room3)

        ICollector(room3).grab(roach2)

        ICollector(table).link(0, book)
        # ICollector(book).grab(roach)
        ILocatable(roach).location = ILocatable(book)
        ICollector(room2).link(0, table)

        O = room1
        for x in range(100):
            N = basic.Room.new()
            ICollector(O).link(1, N)
            O = N

        self.me = me
        self.roach = roach
        self.key = key
        self.ball = ball
        self.book = book

    def testRightRoach(self):
        roaches = list(collect(ICollector(self.me), IRoach, always, 2))
        keys = list(collect(ICollector(self.me), IKey, always))
        self.assertEquals(roaches, [(2, IRoach(self.roach))])
        self.assertEquals(keys, [(0, IKey(self.key))])

    def testFindSibling(self):
        balls = simulacrum.lookFor(ICollector(self.me), 'ball', ICollector)
        self.assertIn(ICollector(self.ball), [x[1] for x in balls])

    def testContents(self):
        self.assertEquals(list(ILocatable(self.book).contents), [self.roach])

