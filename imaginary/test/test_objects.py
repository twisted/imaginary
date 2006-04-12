
from twisted.trial import unittest

from axiom import store, item, attributes

from imaginary import eimaginary, objects, iterutils, text as T, iimaginary

class PointsTestCase(unittest.TestCase):
    def setUp(self):
        self.store = store.Store()

    def testInitialiation(self):
        p = objects.Points(store=self.store, max=100)
        self.assertEquals(p.current, p.max)
        self.assertEquals(p.max, 100)


    def testMutation(self):
        p = objects.Points(store=self.store, max=100)
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
        p = objects.Points(store=self.store, max=100)
        self.assertEquals(str(p), '100/100')
        self.assertEquals(repr(p), 'imaginary.objects.Points(100, 100)')

        p.decrease(10)
        self.assertEquals(str(p), '90/100')
        self.assertEquals(repr(p), 'imaginary.objects.Points(100, 90)')

        p.decrease(90)
        self.assertEquals(str(p), '0/100')
        self.assertEquals(repr(p), 'imaginary.objects.Points(100, 0)')



class Describeable(item.Item):
    long = attributes.text(default=u"Yo LONG")
    short = attributes.text(default=u"yo")

    def longFormatTo(self, other):
        return self.long


    def formatTo(self, other):
        return self.short



class ObjectTestCase(unittest.TestCase):
    def setUp(self):
        self.store = store.Store()

    def testCreation(self):
        obj = objects.Object(store=self.store, name=u"test object", description=u"lame description")
        self.assertEquals(obj.name, u"test object")
        self.assertEquals(obj.description, u"lame description")


    def testDestroy(self):
        obj = objects.Object(store=self.store, name=u"x")
        obj.destroy()

        room = objects.Object(store=self.store, name=u"test location")
        objects.Container(store=self.store, capacity=1000).installOn(room)
        obj = objects.Object(store=self.store, name=u"y")
        obj.moveTo(room)

        obj.destroy()
        self.assertEquals(obj.location, None)
        self.failIf(room.find("y") is not None)



    def testFind(self):
        obj = objects.Object(store=self.store, name=u"z")
        room = objects.Object(store=self.store, name=u"location")
        objects.Container(store=self.store, capacity=1000).installOn(room)
        obj.moveTo(room)

        self.assertIdentical(obj.find("z"), obj)
        self.assertIdentical(obj.find("me"), obj)
        self.assertIdentical(obj.find("self"), obj)
        self.assertIdentical(obj.find("here"), room)

        self.assertIdentical(obj.find("zoop"), None)



    def testMoving(self):
        obj = objects.Object(store=self.store, name=u"DOG")
        room = objects.Object(store=self.store, name=u"HOUSE")
        objects.Container(store=self.store, capacity=1000).installOn(room)
        obj.moveTo(room)
        self.assertIdentical(obj.location, room)
        obj.moveTo(room)
        self.assertIdentical(obj.location, room)



    def testNonPortable(self):
        """
        Test that the C{portable} flag is respected and prevents movement between locations.
        """
        obj = objects.Object(store=self.store, name=u"mountain")
        obj.portable = False
        room = objects.Object(store=self.store, name=u"place")
        objects.Container(store=self.store, capacity=1000).installOn(room)
        obj.moveTo(room)
        elsewhere = objects.Object(store=self.store, name=u"different place")
        container = objects.Container(store=self.store, capacity=1000)
        container.installOn(elsewhere)
        self.assertRaises(eimaginary.CannotMove, obj.moveTo, elsewhere)
        self.assertIdentical(obj.location, room)
        self.assertEquals(list(iimaginary.IContainer(room).getContents()), [obj])
        self.assertEquals(list(container.getContents()), [])


    def testObjectProvidesIDescribeable(self):
        obj = objects.Object(store=self.store, name=u"mountain")
        self.assertTrue(iimaginary.IDescribeable.providedBy(iimaginary.IDescribeable(obj)))

    def testDescriptionOverridableByPowerup(self):
        obj = objects.Object(store=self.store, name=u"mountain")
        obj.powerUp(Describeable(store=self.store), iimaginary.IDescribeable)

        out = iimaginary.IDescribeable(obj).longFormatTo("hello")
        self.assertEquals(out, "Yo LONG")

