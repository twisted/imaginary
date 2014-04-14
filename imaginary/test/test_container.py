# -*- test-case-name: imaginary.test -*-

from zope.interface.verify import verifyObject

from twisted.trial import unittest

from axiom import store

from imaginary import iimaginary, eimaginary, objects
from imaginary.test.commandutils import (
    CommandTestCaseMixin, E, createLocation, flatten)
from imaginary.language import ExpressList

class ContainerTestCase(unittest.TestCase):
    def setUp(self):
        self.store = store.Store()
        self.containmentCore = objects.Thing(store=self.store, name=u"container")
        self.container = objects.Container.createFor(self.containmentCore, capacity=1)
        self.object = objects.Thing(store=self.store, name=u"object")


    def testAdd(self):
        """
        Test that successfully adding an object to a container properly adjusts
        the world graph - in particular, the contents list of the container and
        the location of the object.
        """
        self.container.add(self.object)
        self.assertEquals(list(self.container.getContents()), [self.object])
        self.assertIdentical(self.object.location, self.containmentCore)


    def testRemove(self):
        """
        Test that successfully removing an object from a container properly
        adjusts the world graph - in particular, the contents list of the
        container and the location of the object.
        """
        self.testAdd()
        self.container.remove(self.object)
        self.assertEquals(list(self.container.getContents()), [])
        self.assertIdentical(self.object.location, None)


    def testOverflowing(self):
        """
        Test the capacity feature of the container implementation as it
        interacts with the weight feature of the object implementation.
        """
        self.container.capacity = 1
        self.object.weight = 2
        self.assertRaises(eimaginary.DoesntFit, self.container.add, self.object)
        self.assertEquals(list(self.container.getContents()), [])
        self.assertIdentical(self.object.location, None)


    def testClosed(self):
        """
        Test the closed feature of the container implementation.
        """
        self.container.closed = True
        self.assertRaises(eimaginary.Closed, self.container.add, self.object)
        self.assertEquals(list(self.container.getContents()), [])
        self.assertIdentical(self.object.location, None)

        self.container.closed = False
        self.container.add(self.object)
        self.container.closed = True

        self.assertRaises(eimaginary.Closed, self.container.remove, self.object)
        self.assertEquals(list(self.container.getContents()), [self.object])
        self.assertIdentical(self.object.location, self.containmentCore)



class ExpressContentsTests(unittest.TestCase):
    """
    Tests for L{ExpressContents}.
    """
    def setUp(self):
        self.store = store.Store()
        self.box = objects.Thing(store=self.store, name=u"box")
        self.container = objects.Container.createFor(self.box, capacity=123)
        self.concept = objects.ExpressContents(self.container)
        self.observer = objects.Thing(store=self.store, name=u"observer")


    def addContents(self, names):
        """
        Add a new L{Thing} to C{self.container} for each element of C{names}.

        @param names: An iterable of L{unicode} giving the names of the things
            to create and add.
        """
        things = []
        for name in names:
            thing = objects.Thing(store=self.store, name=name, proper=True)
            thing.moveTo(self.container)
            things.append(thing)
        return things


    def test_interface(self):
        """
        An instance of L{ExpressContents} provides L{IConcept}.
        """
        self.assertTrue(verifyObject(iimaginary.IConcept, self.concept))


    def test_contentConceptsEmpty(self):
        """
        L{ExpressContents._contentConcepts} returns an empty L{list} if the
        L{Container} the L{ExpressContents} instance is initialized with has no
        contents.
        """
        contents = self.concept._contentConcepts(self.observer)
        self.assertEqual([], contents)


    def test_contentConcepts(self):
        """
        L{ExpressContents._contentConcepts} returns a L{list} of L{IConcept}
        providers representing the things contained by the L{Container} the
        L{ExpressContents} instance is initialized with.
        """
        [something] = self.addContents([u"something"])

        contents = self.concept._contentConcepts(self.observer)
        self.assertEqual([something], contents)


    def test_contentConceptsExcludesObserver(self):
        """
        The L{list} returned by L{ExpressContents._contentConcepts} does not
        include the observer, even if the observer is contained by the
        L{Container} the L{ExpressContents} instance is initialized with.
        """
        [something] = self.addContents([u"something"])
        self.observer.moveTo(self.container)

        concepts = self.concept._contentConcepts(self.observer)
        self.assertEqual([something], concepts)


    def test_contentConceptsExcludesUnseen(self):
        """
        If the L{Container} used to initialize L{ExpressContents} cannot be
        seen by the observer passed to L{ExpressContents._contentConcepts}, it
        is not included in the returned L{list}.
        """
        objects.LocationLighting.createFor(self.box, candelas=0)
        [something] = self.addContents([u"something"])

        concepts = self.concept._contentConcepts(self.observer)
        self.assertEqual([], concepts)


    def test_template(self):
        """
        L{ExpressContents.template} evaluates to the value of the
        C{contentsTemplate} attribute of the L{Container} used to initialize
        the L{ExpressContents} instance.
        """
        template = u"{pronoun} is carrying {contents}."
        self.container.contentsTemplate = template
        self.assertEqual(template, self.concept.template)


    def test_defaultTemplate(self):
        """
        If the wrapped L{Container}'s C{contentsTemplate} is C{None},
        L{ExpressContents.template} evaluates to a string giving a simple,
        generic English-language template.
        """
        self.container.contentsTemplate = None
        self.assertEqual(
            u"{subject:pronoun} contains {contents}.", self.concept.template)


    def test_expandSubject(self):
        """
        L{ExpressContents.expand} expands a concept template string using
        the wrapped L{Container}'s L{Thing} as I{subject}.
        """
        self.assertEqual(
            [self.box.name],
            list(self.concept._expand(u"{subject:name}", self.observer, [])))


    def conceptAsText(self, concept, observer):
        """
        Express C{concept} to C{observer} and flatten the result into a
        L{unicode} string.

        @return: The text result expressing the concept.
        """
        return flatten(
            ExpressList(concept.concepts(observer)).plaintext(observer))


    def test_expandContents(self):
        """
        L{ExpressContents.expand} expands a concept template string using the
        contents of the L{Thing} as I{contents}.
        """
        self.addContents([u"something", u"something else"])

        contents = self.concept._expand(
            u"{contents}", self.observer,
            self.concept._contentConcepts(self.concept)
        )
        self.assertEqual(
            u"something and something else",
            self.conceptAsText(ExpressList(contents), self.observer))


    def test_concepts(self):
        """
        L{ExpressContents.concepts} returns a L{list} expressing the contents
        of the wrapped container to the given observer.
        """
        self.addContents([u"red fish", u"blue fish"])
        self.assertEqual(
            u"it contains red fish and blue fish.",
            self.conceptAsText(self.concept, self.observer))


    def test_emptyConcepts(self):
        """
        If the wrapped container is empty, L{ExpressContents.concepts} returns
        an empty list.
        """
        self.assertEqual(
            u"", self.conceptAsText(self.concept, self.observer))



class IngressAndEgressTestCase(CommandTestCaseMixin, unittest.TestCase):
    """
    I should be able to enter and exit containers that are sufficiently big.
    """

    def setUp(self):
        """
        Create a container, C{self.box} that is large enough to stand in.
        """
        CommandTestCaseMixin.setUp(self)
        self.container = createLocation(self.store, u"box", None)
        self.box = self.container.thing
        self.box.proper = False
        self.box.moveTo(self.location)


    def test_enterBox(self):
        """
        I should be able to enter the box.
        """
        self.assertCommandOutput(
            'enter box',
            [E('[ Test Location ]'),
             'Location for testing.',
             'Here, you see Observer Player and a box.'],
            ['Test Player leaves into the box.'])


    def test_exitBox(self):
        """
        I should be able to exit the box.
        """
        self.player.moveTo(self.container)
        self.assertCommandOutput(
            'exit out',
            [E('[ Test Location ]'),
             'Location for testing.',
             'Here, you see Observer Player and a box.'],
            ['Test Player leaves out of the box.'])
        self.assertEquals(self.player.location,
                          self.location)


    def test_enterWhileHoldingBox(self):
        """
        When I'm holding a container, I shouldn't be able to enter it.
        """
        self.container.thing.moveTo(self.player)
        self.assertCommandOutput('enter box',
                                 ["The box won't fit inside itself."],
                                 [])

