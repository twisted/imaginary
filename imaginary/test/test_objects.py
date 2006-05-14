
from zope.interface import Interface, implements

from twisted.trial import unittest
from twisted.python import components

from axiom import store, item, attributes

from imaginary import eimaginary, objects, iimaginary

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
        locContainer = objects.Container(store=self.store, capacity=1000)
        locContainer.installOn(room)
        obj = objects.Thing(store=self.store, name=u"y")
        obj.moveTo(room)

        obj.destroy()
        self.assertIdentical(obj.location, None)
        self.assertEquals(list(locContainer.getContents()), [])


    def testMoving(self):
        obj = objects.Thing(store=self.store, name=u"DOG")
        room = objects.Thing(store=self.store, name=u"HOUSE")
        objects.Container(store=self.store, capacity=1000).installOn(room)
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
        objects.Container(store=self.store, capacity=1000).installOn(room)
        obj.moveTo(room)
        elsewhere = objects.Thing(store=self.store, name=u"different place")
        container = objects.Container(store=self.store, capacity=1000)
        container.installOn(elsewhere)
        self.assertRaises(eimaginary.CannotMove, obj.moveTo, elsewhere)
        self.assertIdentical(obj.location, room)
        self.assertEquals(list(iimaginary.IContainer(room).getContents()), [obj])
        self.assertEquals(list(container.getContents()), [])



unexpected = object()
class IFoo(Interface):
    """
    Stupid thing to help tests out.
    """

components.registerAdapter(lambda o: (unexpected, o), objects.Thing, IFoo)


class Proxy(item.Item, item.InstallableMixin):
    implements(iimaginary.IProxy)

    thing = attributes.reference()

    installedOn = objects.installedOn

    provider = attributes.inmemory()

    priority = attributes.integer(default=0)

    proxiedObjects = attributes.inmemory()

    def installOn(self, other):
        super(Proxy, self).installOn(other)
        other.powerUp(self, iimaginary.IProxy, self.priority)


    # IProxy
    def proxy(self, facet, iface):
        getattr(self, 'proxiedObjects', []).append((facet, iface))
        return self.provider



class StubLocationProxy(item.Item, item.InstallableMixin):
    implements(iimaginary.ILocationProxy)

    thing = attributes.reference()
    installedOn = objects.installedOn

    def installOn(self, other):
        super(StubLocationProxy, self).installOn(other)
        other.powerUp(self, iimaginary.ILocationProxy)

    def proxy(self, facet, interface):
        return (facet,)



class FindProvidersTestCase(unittest.TestCase):
    def setUp(self):
        self.store = store.Store()
        obj = objects.Thing(store=self.store, name=u"generic object")
        room = objects.Thing(store=self.store, name=u"room")
        objects.Container(store=self.store, capacity=1000).installOn(room)
        obj.moveTo(room)
        self.obj = obj
        self.room = room


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


    def testProxyRestrictsResults(self):
        """
        If we put a proxy between the object and the room, and the proxy
        returns None, then no facets should be returned when searching for
        providers of IFoo.
        """
        p = Proxy(store=self.store, provider=None)
        p.installOn(self.obj)

        self.assertEquals(
            list(self.obj.findProviders(IFoo, 1)),
            [])


    def testProxyReturnsAlternate(self):
        """
        Similar to testProxyReturnsAlternate, but using a proxy which returns
        an alternative provider. The provider should be in the result of
        findProviders.
        """
        expected = u"expected"
        p = Proxy(store=self.store, provider=expected)
        p.installOn(self.obj)

        self.assertEquals(
            list(self.obj.findProviders(IFoo, 1)),
            [expected, expected])


    def testProxyNoneWins(self):
        """
        If the first proxy found returns None, and the second proxy found
        returns an object, then nothing should be returned from findProviders.
        """
        expected = u"zoom"
        firstProxy = Proxy(store=self.store, priority=1, provider=None)
        secondProxy = Proxy(store=self.store, priority=2, provider=expected)

        firstProxy.installOn(self.obj)
        secondProxy.installOn(self.obj)

        self.assertEquals(
            list(self.obj.findProviders(IFoo, 1)),
            [])


    def testProxyApplicability(self):
        """
        Test that an observer sees a room through a proxy on the room, but sees
        himself unproxied.
        """
        expected = u"frotz"
        p = Proxy(store=self.store, provider=expected)
        p.proxiedObjects = []
        p.installOn(self.room)

        self.assertEquals(
            list(self.obj.findProviders(IFoo, 1)),
            [(unexpected, self.obj), expected])

        self.assertEquals(
            p.proxiedObjects,
            [((unexpected, self.room), IFoo)])


    # TODO: test similar to testProxyApplicability only obj -> proxy1 -> obj2 -> proxy2 -> obj3.

    def testLocationProxy(self):
        """
        Test that ILocationProxy powerups on a location are asked to proxy for
        all objects within location.

        Also test that an ILocationProxy will get the location on which it is
        powered up passed to its proxy method.

        """
        locationProxy = StubLocationProxy(store=self.store)
        locationProxy.installOn(self.room)

        self.assertEquals(list(self.obj.findProviders(iimaginary.IThing, 1)),
                          [(self.obj,), (self.room,)])


    def testLocationProxyProxiesIndirectContents(self):
        """
        Similar to testLocationProxy, but also ensure that objects which are
        indirectly contained by the location are also proxied.
        """
        locationProxy = StubLocationProxy(store=self.store)
        locationProxy.installOn(self.room)

        objects.Container(store=self.store, capacity=9999).installOn(self.obj)
        rock = objects.Thing(store=self.store, name=u"rock")
        rock.moveTo(self.obj)

        self.assertEquals(
            list(self.obj.findProviders(iimaginary.IThing, 1)),
            [(self.obj,), (rock,), (self.room,)])


    def testLocationProxyOnlyAppliesToContainedObjects(self):
        """
        Test Location Proxy Only Applies To Contained Objects.
        """
        locationProxy = StubLocationProxy(store=self.store)
        locationProxy.installOn(self.room)

        nearby = objects.Thing(store=self.store, name=u"other room")
        objects.Container(store=self.store, capacity=1000).installOn(nearby)
        ball = objects.Thing(store=self.store, name=u"ball")
        ball.moveTo(nearby)

        objects.Exit.link(self.room, nearby, u"west")


        self.assertEquals(list(self.obj.findProviders(iimaginary.IThing, 2)),
                          [(self.obj,), (self.room,), nearby, ball])



    def testRemoteLocationProxies(self):
        """
        Test that location proxies apply to their contents, even when the
        findProviders call is originated from a different location.
        """

        nearby = objects.Thing(store=self.store, name=u"other room")
        objects.Container(store=self.store, capacity=1000).installOn(nearby)
        ball = objects.Thing(store=self.store, name=u"ball")
        ball.moveTo(nearby)


        locationProxy = StubLocationProxy(store=self.store)
        locationProxy.installOn(nearby)

        objects.Exit.link(self.room, nearby, u"west")


        self.assertEquals(list(self.obj.findProviders(iimaginary.IThing, 2)),
                          [self.obj, self.room, (nearby,), (ball,)])



    def testPositiveKnownAs(self):
        self.failUnless(self.obj.knownAs(u"generic object"))


    def testNegativeKnownAs(self):
        self.failIf(self.obj.knownAs(u"specific object"))


    def testNotReallyProxiedSelfThing(self):
        """
        Test that an unwrapped Thing can be found from itself through the
        proxy-resolving method L{IThing.proxiedThing}.
        """
        self.assertIdentical(
            self.obj.proxiedThing(self.obj, iimaginary.IThing, 0),
            self.obj)


    def testNotReallyProxiedOtherThing(self):
        """
        Like testNotReallyProxiedSelfThing, but find an object other than the
        finder.
        """
        self.assertIdentical(
            self.obj.proxiedThing(self.room, iimaginary.IThing, 0),
            self.room)



    def testCannotFindProxiedThing(self):
        """
        Test that L{IThing.proxiedThing} raises the appropriate exception when
        the searched-for thing cannot be found.
        """
        self.assertRaises(
            eimaginary.ThingNotFound,
            self.obj.proxiedThing,
            objects.Thing(store=self.store, name=u"nonexistent"),
            iimaginary.IThing,
            0)


    def testActuallyProxiedSelfThing(self):
        """
        Test that if a proxy gets in the way, it is properly respected by
        L{IThing.proxiedThing}.
        """
        class result(object):
            thing = self.obj

        p = Proxy(store=self.store, provider=result)
        p.installOn(self.obj)

        self.assertIdentical(
            self.obj.proxiedThing(self.obj, iimaginary.IThing, 0),
            result)


    def testActuallyProxiedOtherThing(self):
        """
        Just like testActuallyProxiedSelfThing, but look for a Thing other than
        the finder.
        """
        class result(object):
            thing = self.room

        p = Proxy(store=self.store, provider=result)
        p.installOn(self.obj)

        self.assertIdentical(
            self.obj.proxiedThing(self.room, iimaginary.IThing, 0),
            result)



    def testSearchFindsExits(self):
        """
        Test that search can find an exit.
        """
        room = objects.Thing(store=self.store, name=u"Northerly Room")
        objects.Container(store=self.store, capacity=1000).installOn(room)
        objects.Exit.link(self.room, room, u"north")

        self.assertEquals(
            list(self.obj.search(1, iimaginary.IThing, u"north")),
            [room])


    # Test: me
    # Test: here
    # Test: self
