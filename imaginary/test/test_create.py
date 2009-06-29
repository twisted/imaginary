

from zope.interface import Interface, implements, directlyProvides
from zope.interface.verify import verifyObject

from twisted.trial import unittest

from axiom import store, item, attributes

from imaginary import iimaginary, plugins, creation
from imaginary.creation import createCreator
from imaginary.plugins import imaginary_basic
from imaginary.enhancement import Enhancement

from imaginary.test import commandutils



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
            "create a thing named foo",
            ["You create a foo."],
            ["Test Player creates a foo."])
        [foo] = self.playerContainer.getContents()
        self.assertEqual(foo.name, u"foo")
        self.assertFalse(foo.proper)



class IFruit(Interface):
    pass



class Fruit(item.Item, Enhancement):
    implements(IFruit)
    powerupInterfaces = (IFruit,)

    fresh = attributes.boolean(default=False)
    thing = attributes.reference(allowNone=False)



class FruitPlugin(object):
    directlyProvides(iimaginary.IThingType)

    type = 'fruit'

    def getType(cls):
        return createCreator((Fruit, {'fresh': True}))
    getType = classmethod(getType)



class CreateTest(commandutils.CommandTestCaseMixin, unittest.TestCase):
    """
    Tests for the I{create} action.
    """
    def _getPlugins(self, iface, package):
        self.assertIdentical(iface, iimaginary.IThingType)
        self.assertIdentical(package, plugins)
        return [FruitPlugin]


    def setUp(self):
        self.old_getPlugins = creation.getPlugins
        creation.getPlugins = self._getPlugins
        return commandutils.CommandTestCaseMixin.setUp(self)


    def tearDown(self):
        creation.getPlugins = self.old_getPlugins
        return commandutils.CommandTestCaseMixin.tearDown(self)


    def test_createAThing(self):
        """
        The I{create a} form of the I{create} action makes a new L{Thing} using
        the plugin which matches the type name specified and marks its name as
        a common noun.
        """
        self._test(
            "create a fruit named apple",
            ["You create an apple."],
            ["Test Player creates an apple."])
        apple = self.find(u"apple")
        self.assertEquals(apple.name, "apple")
        self.assertFalse(apple.proper)
        self.assertEquals(apple.description, "an undescribed object")
        self.assertEquals(apple.location, self.player)
        fruit = IFruit(apple)
        self.assertTrue(isinstance(fruit, Fruit))
        self.assertTrue(fruit.fresh)


    def test_createAnThing(self):
        """
        The I{create an} form of the I{create} action makes a new L{Thing}
        using the plugin which matches the type name specified and marks its
        name as a common noun.
        """
        self._test(
            "create an fruit named pear",
            ["You create a pear."],
            ["Test Player creates a pear."])
        pear = self.find(u"pear")
        self.assertEquals(pear.name, "pear")
        self.assertFalse(pear.proper)
        self.assertEquals(pear.description, "an undescribed object")
        self.assertEquals(pear.location, self.player)
        fruit = IFruit(pear)
        self.assertTrue(isinstance(fruit, Fruit))
        self.assertTrue(fruit.fresh)


    def test_createImpliedCommonNounThing(self):
        """
        The I{create} form of the I{create} action implies a common noun name
        and behaves the same way as the I{create a} and I{create an} forms.
        """
        self._test(
            "create fruit named 'bunch of grapes'",
            ["You create a bunch of grapes."],
            ["Test Player creates a bunch of grapes."])
        pear = self.find(u"bunch of grapes")
        self.assertEquals(pear.name, "bunch of grapes")
        self.assertFalse(pear.proper)
        self.assertEquals(pear.description, "an undescribed object")
        self.assertEquals(pear.location, self.player)
        fruit = IFruit(pear)
        self.assertTrue(isinstance(fruit, Fruit))
        self.assertTrue(fruit.fresh)


    def test_createTheThing(self):
        """
        The I{create the} form of the I{create} action makes a new L{Thing}
        using the plugin which matches the type name specified and marks its
        name as a proper noun.
        """
        self._test(
            "create the fruit named 'The Golden Apple'",
            ["You create The Golden Apple."],
            ["Test Player creates The Golden Apple."])
        apple = self.find(u"The Golden Apple")
        self.assertEqual(apple.name, "The Golden Apple")
        self.assertTrue(apple.proper)
        self.assertEqual(apple.description, "an undescribed object")
        self.assertEqual(apple.location, self.player)
        fruit = IFruit(apple)
        self.assertTrue(isinstance(fruit, Fruit))
        self.assertTrue(fruit.fresh)


    def test_createMultiwordWithDescription(self):
        """
        The I{create} command creates a thing of the type specified by its
        first argument, with the name specified by its second argument, and
        with a description specified by the remainder of the input line.
        """
        self._test(
            "create a fruit named 'described fruit' This is the fruit's description.",
            ["You create a described fruit."],
            ["Test Player creates a described fruit."])
        [thing] = self.playerContainer.getContents()
        self.assertEquals(thing.name, "described fruit")
        self.assertEquals(thing.description, "This is the fruit's description.")
        self.assertEquals(thing.location, self.player)



class ListCreatablesTests(commandutils.CommandTestCaseMixin, unittest.TestCase):
    """
    Tests for C{list creatables}.
    """

    def _getPlugins(self, interface, package):
        """
        A stub implementation of L{creation.getPlugins} meant to replace it
        temporarily during tests.

        @param interface: Must be IThingType.
        @param package: Must be L{imaginary.plugins}.
        @return: A list of two instances of L{FruitPlugin}.
        """
        self.assertIdentical(interface, iimaginary.IThingType)
        self.assertIdentical(package, plugins)
        foo = FruitPlugin()
        bar = FruitPlugin()
        foo.type = "foo"
        # Include some non-ascii to make sure it supports non-ascii.
        bar.type = u"bar\N{HIRAGANA LETTER A}"
        return [foo, bar]


    def setUp(self):
        """
        Monkeypatch L{creation.getPlugins} with L{_getPlugins}.
        """
        self.oldGetPlugins = creation.getPlugins
        creation.getPlugins = self._getPlugins
        return commandutils.CommandTestCaseMixin.setUp(self)


    def tearDown(self):
        """
        Unmonkeypatch L{creation.getPlugins}.
        """
        creation.getPlugins = self.oldGetPlugins
        return commandutils.CommandTestCaseMixin.tearDown(self)


    def test_listThingTypes(self):
        """
        L{listThingTypes} returns a list of strings in alphabetical order
        describing types which can be created.
        """
        self.assertEqual(creation.listThingTypes(),
                         [u"bar\N{HIRAGANA LETTER A}", u"foo"])


    def test_listThingTypesCommand(self):
        """
        I{list thing types} displays the names of all types which can be
        created.
        """
        self._test(
            "list thing types",
            [u"bar\N{HIRAGANA LETTER A}", u"foo"],
            [])


    def test_helpListThingTypes(self):
        """
        I{help list thing types} gives usage information for the I{list thing
        types} action.
        """
        actorOutput, otherOutput = self.watchCommand("help list thing types")
        self.assertIn("Show a list of names of things which can be created",
                      actorOutput)
        self.assertEquals(otherOutput, "")


    def test_helpList(self):
        """
        The I{list} help text refers to I{list thing types}.
        """
        actorOutput, otherOutput = self.watchCommand("help list")
        self.assertIn("thing types", actorOutput)
        self.assertEqual(otherOutput, u"")
