
from twisted.trial import unittest

from pottery import epottery
from pottery import objects
from pottery import iterutils
from pottery import text as T

class PointsTestCase(unittest.TestCase):
    def testInitialiation(self):
        p = objects.Points(100)
        self.assertEquals(p.current, p.max)
        self.assertEquals(p.max, 100)


    def testMutation(self):
        p = objects.Points(100)
        p.increase(10)
        self.assertEquals(p.current, 100)

        p.decrease(10)
        self.assertEquals(p.current, 90)

        p.increase(20)
        self.assertEquals(p.current, 100)

        p.decrease(110)
        self.assertEquals(p.current, 0)

        p.decrease(10)
        self.assertEquals(p.current, 0)

        p.modify(10)
        self.assertEquals(p.current, 10)

        p.modify(-10)
        self.assertEquals(p.current, 0)


    def testRepresentation(self):
        p = objects.Points(100)
        self.assertEquals(str(p), '100/100')
        self.assertEquals(repr(p), 'pottery.objects.Points(100, 100)')

        p.decrease(10)
        self.assertEquals(str(p), '90/100')
        self.assertEquals(repr(p), 'pottery.objects.Points(100, 90)')

        p.decrease(90)
        self.assertEquals(str(p), '0/100')
        self.assertEquals(repr(p), 'pottery.objects.Points(100, 0)')



class ObjectTestCase(unittest.TestCase):
    def testCreation(self):
        obj = objects.Object("test object", "lame description")
        self.assertEquals(obj.name, "test object")
        self.assertEquals(obj.description, "lame description")


    def testDestroy(self):
        obj = objects.Object("x")
        obj.destroy()

        room = objects.Room("test location")
        obj = objects.Object("y")
        obj.moveTo(room)

        obj.destroy()
        self.assertEquals(obj.location, None)
        self.failIf(room.find("y") is not None)



    def testFind(self):
        obj = objects.Object("z")
        room = objects.Room("location")
        obj.moveTo(room)

        self.assertIdentical(obj.find("z"), obj)
        self.assertIdentical(obj.find("me"), obj)
        self.assertIdentical(obj.find("self"), obj)
        self.assertIdentical(obj.find("here"), room)

        self.assertIdentical(obj.find("zoop"), None)



    def testFormatting(self):
        pc = objects.Actor("test actor")
        pc.useColors = False
        try:
            obj = objects.Object("name", "descr")
            self.assertEquals(pc.format(obj), "name")

            longFormat = pc.format(obj.longFormatTo(pc))
            self.assertEquals(
                longFormat,
                "name\n"
                "descr\n")
        finally:
            pc.destroy()



    def testMoving(self):
        obj = objects.Object("DOG")
        room = objects.Room("HOUSE")
        obj.moveTo(room)
        self.assertIdentical(obj.location, room)
        obj.moveTo(room)
        self.assertIdentical(obj.location, room)



    def testNonPortable(self):
        """
        Test that the C{portable} flag is respected and prevents movement between locations.
        """
        obj = objects.Object("mountain")
        obj.portable = False
        room = objects.Room("place")
        obj.moveTo(room)
        elsewhere = objects.Room("different place")
        self.assertRaises(epottery.CannotMove, obj.moveTo, elsewhere)
        self.assertIdentical(obj.location, room)
        self.assertEquals(room.contents, [obj])
        self.assertEquals(elsewhere.contents, [])
