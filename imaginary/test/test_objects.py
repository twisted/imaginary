
from zope.interface import Interface

from twisted.trial import unittest
from twisted.python import components

from axiom import store

from imaginary import iimaginary, eimaginary, objects, events
from imaginary.test import commandutils



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




class ObjectTestCase(unittest.TestCase):
    def setUp(self):
        self.store = store.Store()


    def testCreation(self):
        obj = objects.Thing(store=self.store, name=u"test object", description=u"lame description")
        self.assertEquals(obj.name, u"test object")
        self.assertEquals(obj.description, u"lame description")


    def testDestroy(self):
        obj = objects.Thing(store=self.store, name=u"x")
        obj.destroy()

        room = objects.Thing(store=self.store, name=u"test location")
        locContainer = objects.Container.createFor(room, capacity=1000)
        obj = objects.Thing(store=self.store, name=u"y")
        obj.moveTo(room)

        obj.destroy()
        self.assertIdentical(obj.location, None)
        self.assertEquals(list(locContainer.getContents()), [])


    def testMoving(self):
        obj = objects.Thing(store=self.store, name=u"DOG")
        room = objects.Thing(store=self.store, name=u"HOUSE")
        objects.Container.createFor(room, capacity=1000)
        obj.moveTo(room)
        self.assertIdentical(obj.location, room)
        obj.moveTo(room)
        self.assertIdentical(obj.location, room)


    def testNonPortable(self):
        """
        Test that the C{portable} flag is respected and prevents movement
        between locations.
        """
        obj = objects.Thing(store=self.store, name=u"mountain")
        obj.portable = False
        room = objects.Thing(store=self.store, name=u"place")
        objects.Container.createFor(room, capacity=1000)
        obj.moveTo(room)
        elsewhere = objects.Thing(store=self.store, name=u"different place")
        container = objects.Container.createFor(elsewhere, capacity=1000)
        self.assertRaises(eimaginary.CannotMove, obj.moveTo, elsewhere)
        self.assertIdentical(obj.location, room)
        self.assertEquals(list(iimaginary.IContainer(room).getContents()), [obj])
        self.assertEquals(list(container.getContents()), [])



class MovementTestCase(unittest.TestCase):
    def setUp(self):
        self.store = store.Store()
        obj = objects.Thing(store=self.store, name=u"DOG")
        room = objects.Thing(store=self.store, name=u"HOUSE")
        objects.Container.createFor(room, capacity=1000)
        obj.moveTo(room)

        observer = objects.Thing(store=self.store, name=u"OBSERVER")
        actor = objects.Actor.createFor(observer)
        intelligence = commandutils.MockEphemeralIntelligence()
        actor.setEphemeralIntelligence(intelligence)

        self.obj = obj
        self.room = room
        self.observer = observer
        self.intelligence = intelligence
        self.actor = actor


    def testMovementDepartureEvent(self):
        """
        Test that when a Thing is moved out of a location, a departure event is
        broadcast to that location.
        """
        self.observer.moveTo(self.room)
        self.intelligence.events[:] = []

        self.obj.moveTo(None)

        evts = self.intelligence.events
        self.assertEquals(len(evts), 1)
        self.failUnless(
            isinstance(evts[0], events.DepartureEvent))
        self.assertIdentical(evts[0].location, self.room)
        self.assertIdentical(evts[0].actor, self.obj)


    def testMovementArrivalEvent(self):
        """
        Test that when a Thing is moved to a location, an arrival event is
        broadcast to that location.
        """
        destination = objects.Thing(store=self.store, name=u'ELSEWHERE')
        objects.Container.createFor(destination, capacity=1000)

        self.observer.moveTo(destination,
                             arrivalEventFactory=events.MovementArrivalEvent)

        evts = self.intelligence.events
        self.assertEquals(len(evts), 1)
        self.failUnless(isinstance(evts[0], events.MovementArrivalEvent))
        self.assertIdentical(evts[0].thing, self.observer)
        self.assertIdentical(evts[0].location, destination)
        evts[:] = []

        self.obj.moveTo(destination, arrivalEventFactory=events.MovementArrivalEvent)

        evts = self.intelligence.events
        self.assertEquals(len(evts), 1)
        self.failUnless(
            isinstance(evts[0], events.ArrivalEvent))
        self.assertIdentical(evts[0].location, destination)
        self.assertIdentical(evts[0].thing, self.obj)

    # TODO - Test that a guy moving around sees first his own departure event
    # and then his arrival event.

    def test_parameterizedArrivalEvent(self):
        """
        moveTo should take a parameter which allows customization of
        the arrival event that it emits.
        """
        destination = objects.Thing(store=self.store, name=u'ELSEWHERE')
        objects.Container.createFor(destination, capacity=1000)

        class DroppedEvent(events.MovementArrivalEvent):
            def conceptFor(self, observer):
                return "you rock."
        self.observer.moveTo(destination, arrivalEventFactory=DroppedEvent)

        evts = self.intelligence.events
        self.assertEquals(len(evts), 1)
        self.failUnless(isinstance(evts[0], DroppedEvent))
        self.assertIdentical(evts[0].thing, self.observer)
        self.assertIdentical(evts[0].location, destination)

    def test_parameterizedArrivalAsNone(self):
        """
        If the parameter for customizing the arrival event is None, no
        arrival event should be broadcast.
        """
        destination = objects.Thing(store=self.store, name=u'ELSEWHERE')
        objects.Container.createFor(destination, capacity=1000)

        self.observer.moveTo(destination, arrivalEventFactory=None)
        self.assertEquals(self.intelligence.events, [])


    def test_parameterizedArrivalDefaultsNone(self):
        """
        The default should be for moveTo not to broadcast an event.
        """
        destination = objects.Thing(store=self.store, name=u'ELSEWHERE')
        objects.Container.createFor(destination, capacity=1000)

        self.observer.moveTo(destination)
        self.assertEquals(self.intelligence.events, [])



unexpected = object()
class IFoo(Interface):
    """
    Stupid thing to help tests out.
    """

components.registerAdapter(lambda o: (unexpected, o), objects.Thing, IFoo)



class FindProvidersTestCase(unittest.TestCase):
    def setUp(self):
        self.store = store.Store()
        self.retained = []
        obj = objects.Thing(store=self.store, name=u"generic object")
        room = objects.Thing(store=self.store, name=u"room")
        objects.Container.createFor(room, capacity=1000)
        obj.moveTo(room)
        self.obj = obj
        self.room = room


    def tearDown(self):
        """
        Allow the items retained with L{FindProvidersTestCase.retain} to be
        garbage collected.
        """
        del self.retained


    def retain(self, o):
        """
        Keep the given object in memory until the end of the test, so that its
        'inmemory' attributes won't be garbage collected.
        """
        self.retained.append(o)


    def testFindObjects(self):
        """
        Assert that searching for the most basic object interface, L{IObject},
        returns the only two objects available in our test object graph: both
        the location upon which the search was issued and the object which it
        contains.
        """
        self.assertEquals(
            list(self.room.findProviders(iimaginary.IThing, 1)),
            [self.room, self.obj])


    def testFindContainers(self):
        """
        Very much like testFindObjects, but searching for L{IContainer}, which
        only the location provides, and so only the location should be
        returned.
        """
        self.assertEquals(
            list(self.room.findProviders(iimaginary.IContainer, 1)),
            [iimaginary.IContainer(self.room)])


    def testFindNothing(self):
        """
        Again, similar to testFindObjects, but search for an interface that
        nothing provides, and assert that nothing is found.
        """
        class IUnprovidable(Interface):
            """
            Test-only interface that nothing provides.
            """

        self.assertEquals(
            list(self.room.findProviders(IUnprovidable, 1)),
            [])


    def testFindOutward(self):
        """
        Conduct a search for all objects on our test graph, but start the
        search on the contained object rather than the container and assert
        that the same results come back, though in a different order: the
        searched upon Thing always comes first.
        """
        self.assertEquals(
            list(self.obj.findProviders(iimaginary.IThing, 1)),
            [self.obj, self.room])


    def testFindContainersOutward(self):
        """
        Combination of testFindOutward and testFindContainers.
        """
        self.assertEquals(
            list(self.obj.findProviders(iimaginary.IContainer, 1)),
            [iimaginary.IContainer(self.room)])



    def testFindingArbitraryInterface(self):
        """
        Demonstration of the Thing -> IFoo adapter registered earlier in this
        module.  If this test fails then some other tests are probably buggy
        too, even if they pass.

        Thing must be adaptable to IFoo or the tests which assert that certain
        Things are B{not} present in result sets may incorrectly pass.
        """
        self.assertEquals(
            list(self.obj.findProviders(IFoo, 1)),
            [(unexpected, self.obj), (unexpected, self.room)])


    def test_exactlyKnownAs(self):
        """
        L{Thing.knownTo} returns C{True} when called with exactly the things
        own name.
        """
        self.assertTrue(self.obj.knownTo(self.obj, self.obj.name))


    def test_caseInsensitivelyKnownAs(self):
        """
        L{Thing.knownTo} returns C{True} when called with a string which
        differs from its name only in case.
        """
        self.assertTrue(self.obj.knownTo(self.obj, self.obj.name.upper()))
        self.assertTrue(self.obj.knownTo(self.obj, self.obj.name.title()))


    def test_wholeWordSubstringKnownAs(self):
        """
        L{Thing.knownTo} returns C{True} when called with a string which
        appears in the thing's name delimited by spaces.
        """
        self.obj.name = u"one two three"
        self.assertTrue(self.obj.knownTo(self.obj, u"one"))
        self.assertTrue(self.obj.knownTo(self.obj, u"two"))
        self.assertTrue(self.obj.knownTo(self.obj, u"three"))


    def test_notKnownAs(self):
        """
        L{Thing.knownTo} returns C{False} when called with a string which
        doesn't satisfy one of the above positive cases.
        """
        self.assertFalse(self.obj.knownTo(self.obj, u"gunk" + self.obj.name))
        self.obj.name = u"one two three"
        self.assertFalse(self.obj.knownTo(self.obj, u"ne tw"))

    # XXX Test being able to find "me", "here", "self", exits (by direction
    # name?)
