

from zope.interface import Interface, implements, directlyProvides
from zope.interface.verify import verifyObject

from twisted.trial import unittest

from axiom import store, item, attributes

from imaginary.test import commandutils
from imaginary import iimaginary, plugins, creation
from imaginary.creation import createCreator
from imaginary.plugins import imaginary_basic



class ThingPlugin(commandutils.CommandTestCaseMixin, unittest.TestCase):
    """
    Tests for L{imaginary_basic.thingPlugin}, a plugin for creating simple
    things with no special behavior.
    """
    def test_createThing(self):
        """
        L{plugins.thingPlugin} creates a L{Thing} with no additional behavior.
        """
        st = store.Store()
        thing = imaginary_basic.thingPlugin.getType()(store=st, name=u"foo")
        self.assertTrue(verifyObject(iimaginary.IThing, thing))
        self.assertIdentical(thing.store, st)
        self.assertEqual(thing.name, u"foo")


    def test_createThingCommand(self):
        """
        Things can be created with the I{create} command.
        """
        self._test(
            "create thing foo",
            ["A foo created."],
            ["Test Player creates a foo."])
        [foo] = self.playerContainer.getContents()
        self.assertEqual(foo.name, u"foo")
        self.assertFalse(foo.proper)



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


    def test_create(self):
        """
        The I{create} command creates a thing of the type specified by its
        first argument and with the name specified by its second argument.
        """
        self._test(
            "create foo bar",
            ["A bar created."],
            ["Test Player creates a bar."])
        [foobar] = self.playerContainer.getContents()
        self.assertEquals(foobar.name, "bar")
        self.assertEquals(foobar.description, "an undescribed object")
        self.assertEquals(foobar.location, self.player)
        self.assertFalse(foobar.proper)
        foo = IFoo(foobar)
        self.failUnless(isinstance(foo, Foo))
        self.assertEquals(foo.foo, u"bar")


    def test_createMultiword(self):
        """
        The I{create} command creates a thing of the type specified by its
        first argument and with the name specified by the contents of a second
        quoted argument.
        """
        self._test(
            "create foo 'bar foo'",
            ["A bar foo created."],
            ["Test Player creates a bar foo."])
        [barfoo] = self.playerContainer.getContents()
        self.assertEquals(barfoo.name, "bar foo")
        self.assertEquals(barfoo.description, 'an undescribed object')
        self.assertEquals(barfoo.location, self.player)


    def test_createMultiwordWithDescription(self):
        """
        The I{create} command creates a thing of the type specified by its
        first argument, with the name specified by its second argument, and
        with a description specified by the remainder of the input line.
        """
        self._test(
            "create foo 'described thing' This is the thing's description.",
            ["A described thing created."],
            ["Test Player creates a described thing."])
        [thing] = self.playerContainer.getContents()
        self.assertEquals(thing.name, "described thing")
        self.assertEquals(thing.description, "This is the thing's description.")
        self.assertEquals(thing.location, self.player)
