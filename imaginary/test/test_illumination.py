from twisted.trial import unittest

from axiom import store

from imaginary import iimaginary, objects
from imaginary.manipulation import Manipulator

from imaginary.test import commandutils


class DarknessTestCase(unittest.TestCase):

    def setUp(self):
        self.store = store.Store()
        self.location = objects.Thing(store=self.store, name=u"Dark Room")
        objects.Container.createFor(self.location, capacity=1000)

        objects.LocationLighting.createFor(self.location, candelas=0)

        self.rock = objects.Thing(store=self.store, name=u"Rock")

        self.observer = objects.Thing(store=self.store, name=u"Observer")

        self.rock.moveTo(self.location)
        self.observer.moveTo(self.location)


    def assertDarkRoom(self, visible):
        """
        Assert that the given L{IVisible} provider is a dark room.
        """
        descr = visible.visualize()
        expressed = descr.plaintext(self.observer)
        lines = commandutils.flatten(expressed).splitlines()

        self.assertEquals(
            lines,
            [u"[ Blackness ]",
             u"You cannot see anything because it is very dark."])


    def testDarkenedRoom(self):
        """
        Test that when a 'dark' LocationLighting proxy is on a location,
        only darkness can be seen.
        """
        darkThings = list(self.observer.findProviders(iimaginary.IVisible, 1))
        self.assertDarkRoom(darkThings[0])
        self.assertEquals(len(darkThings), 1)


    def testLookingOut(self):
        """
        Test that when findProviders is called on an observer in a dark
        location, objects in nearby illuminated rooms are returned.
        """
        nearby = objects.Thing(store=self.store, name=u"other room")
        objects.Container.createFor(nearby, capacity=1000)
        ball = objects.Thing(store=self.store, name=u"ball")
        ball.moveTo(nearby)

        objects.Exit.link(self.location, nearby, u"west")

        found = list(self.observer.findProviders(iimaginary.IVisible, 3))
        self.assertDarkRoom(found[0])
        self.assertEquals(found[1:], [nearby, ball])
        self.assertEquals(len(found), 3)


    def testNonVisibilityUnaffected(self):
        """
        Test that the LocationLightning thingy doesn't block out non-IVisible
        stuff.
        """
        self.assertEquals(
            list(self.observer.findProviders(iimaginary.IThing, 3)),
            [self.observer, self.location, self.rock])


    def testLightSourceInLocation(self):
        """
        Test that a light source in a dark room causes things to be visible
        again.
        """
        torch = objects.Thing(store=self.store, name=u"torch")
        objects.LightSource.createFor(torch, candelas=80)
        torch.moveTo(self.location)

        self.assertEquals(
            list(self.observer.findProviders(iimaginary.IVisible, 1)),
            [self.observer, self.location, self.rock, torch])


    def testHeldLightSource(self):
        """
        Test that a torch in an open container lights up a location.
        """
        torch = objects.Thing(store=self.store, name=u"torch")
        objects.LightSource.createFor(torch, candelas=80)

        objects.Container.createFor(self.observer, capacity=1000)

        torch.moveTo(self.observer)

        self.assertEquals(
            list(self.observer.findProviders(iimaginary.IVisible, 1)),
            [self.observer, self.location, torch, self.rock])


    def testOccultedLightSource(self):
        """
        Test that a light source which is obscured somehow does not actually
        illuminate a location.
        """
        torch = objects.Thing(store=self.store, name=u"torch")
        objects.LightSource.createFor(torch, candelas=80)

        c = objects.Container.createFor(self.observer, capacity=1000)

        torch.moveTo(self.observer)
        c.closed = True

        found = list(self.observer.findProviders(iimaginary.IVisible, 1))
        self.assertDarkRoom(found[0])
        self.assertEquals(len(found), 1)



class DarknessCommandTestCase(commandutils.CommandTestCaseMixin, unittest.TestCase):
    def testLookingIntoDarkness(self):
        objects.LocationLighting.createFor(self.location, candelas=0)
        self._test(
            "look",
            [commandutils.E("[ Blackness ]"),
             "You cannot see anything because it is very dark."])


    def testTorch(self):
        objects.LocationLighting.createFor(self.location, candelas=0)
        self._test(
            "create a torch named torch",
            ["You create a torch."],
            ["Test Player creates a torch."])

        self._test(
            "look",
            [commandutils.E("[ Test Location ]"),
             "Location for testing.",
             "Observer Player"])


    def test_changeIlluminationLevel(self):
        """
        An administrator can change the illumination level of a room to a fixed
        number by using the "illuminate" command.
        """
        fade_to_black = "Your environs fade to black due to Ineffable Spooky Magic."
        no_change = "You do it.  Swell."
        dark_to_light = "Your environs are suddenly alight."
        brighten = "Your environs seem slightly brighter."
        endarken = "Your environs seem slightly dimmer."
        theAdmin = Manipulator(store=self.store, thing=self.playerWrapper.actor)
        self.playerWrapper.actor.powerUp(theAdmin)

        self._test(
            "illuminate 0",
            [fade_to_black],
            [fade_to_black])

        ll = self.store.findUnique(
            objects.LocationLighting,
            objects.LocationLighting.thing == self.location)
        self.assertEquals(ll.candelas, 0)

        self._test(
            "illuminate 0",
            [no_change])
        self.assertEquals(ll.candelas, 0)

        self._test(
            "illuminate 100",
            [dark_to_light],
            [dark_to_light])
        self.assertEquals(ll.candelas, 100)

        self._test(
            "illuminate 110",
            [brighten],
            [brighten])
        self.assertEquals(ll.candelas, 110)

        self._test(
            "illuminate 100",
            [endarken],
            [endarken])
        self.assertEquals(ll.candelas, 100)

        self._test(
            "illuminate 0",
            [fade_to_black],
            [fade_to_black])
        self.assertEquals(ll.candelas, 0)


    def test_regularUserCantIlluminate(self):
        """
        A regular, non-administrative user should not be able to illuminate a
        room with the administrative command.
        """
        objects.LocationLighting(thing=self.location,
                                 store=self.location.store,
                                 candelas=100)
        self._test(
            "illuminate 0",
            ["You are insufficiently brilliant to do that directly."])
        self.assertEquals(self.store.findUnique(
                objects.LocationLighting,
                objects.LocationLighting.thing == self.location).candelas, 100)
