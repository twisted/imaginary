

from zope.interface import Interface, implements, directlyProvides

from twisted.trial import unittest

from axiom import item, attributes

from imaginary.test import commandutils
from imaginary import iimaginary, plugins, creation
from imaginary.creation import createCreator


class IFoo(Interface):
    pass



class Foo(item.Item):
    implements(IFoo)
    powerupInterfaces = (IFoo,)

    foo = attributes.text()



createFoo = createCreator((Foo, {'foo': u'bar'}))


class FooPlugin(object):
    directlyProvides(iimaginary.IThingType)

    type = 'foo'

    def getType(cls):
        return createFoo
    getType = classmethod(getType)



class CreateTest(commandutils.CommandTestCaseMixin, unittest.TestCase):
    def _getPlugins(self, iface, package):
        self.assertIdentical(iface, iimaginary.IThingType)
        self.assertIdentical(package, plugins)
        return [FooPlugin]


    def setUp(self):
        self.old_getPlugins = creation.getPlugins
        creation.getPlugins = self._getPlugins
        return commandutils.CommandTestCaseMixin.setUp(self)


    def tearDown(self):
        creation.getPlugins = self.old_getPlugins
        return commandutils.CommandTestCaseMixin.tearDown(self)


    def testCreate(self):
        self._test(
            "create foo bar",
            ["Bar created."],
            ["Test Player creates bar."])
        foobar = self.find(u"bar")
        self.assertEquals(foobar.name, "bar")
        self.assertEquals(foobar.description, "an undescribed object")
        self.assertEquals(foobar.location, self.player)
        foo = IFoo(foobar)
        self.failUnless(isinstance(foo, Foo))
        self.assertEquals(foo.foo, u"bar")

        self._test(
            "create foo 'bar foo'",
            ["Bar foo created."],
            ["Test Player creates bar foo."])
        barfoo = self.find(u"bar foo")
        self.assertEquals(barfoo.name, "bar foo")
        self.assertEquals(barfoo.description, 'an undescribed object')
        self.assertEquals(barfoo.location, self.player)

        self._test(
            "create foo 'described thing' This is the things description.",
            ["Described thing created."],
            ["Test Player creates described thing."])
        thing = self.find(u"described thing")
        self.assertEquals(thing.name, "described thing")
        self.assertEquals(thing.description, "This is the things description.")
        self.assertEquals(thing.location, self.player)
