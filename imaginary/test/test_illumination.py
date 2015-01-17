
from zope.interface import implements

from twisted.trial import unittest

from axiom import store, item, attributes

from imaginary.enhancement import Enhancement
from imaginary import iimaginary, objects, idea
from imaginary.language import ExpressString
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
        descr = visible.visualizeWithContents([])
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


    def test_nonVisibilityAffected(self):
        """
        L{LocationLightning} blocks out non-IVisible stuff from
        L{Thing.findProviders} by default.
        """
        self.assertEquals(
            list(self.observer.findProviders(iimaginary.IThing, 3)),
            [])
        # XXX need another test: not blocked out from ...


    def test_nonVisibilityUnaffected(self):
        """
        L{LocationLightning} should not block out non-IVisible stuff from a
        plain L{Idea.obtain} query.
        """
        self.assertEquals(
            list(self.observer.idea.obtain(
                    idea.Proximity(3, idea.ProviderOf(iimaginary.IThing)))),
            [self.observer, self.location, self.rock]
            )


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
            [self.observer, torch, self.location, self.rock])


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
             "Here, you see Observer Player."])


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


class ActionsInDarkRoomTestCase(commandutils.CommandTestCaseMixin,
                                unittest.TestCase):
    """
    Darkness interferes with other commands.
    """

    def setUp(self):
        """
        There's a room which is dark, where the player is trying to do things.
        """
        commandutils.CommandTestCaseMixin.setUp(self)
        self.lighting = objects.LocationLighting.createFor(
            self.location, candelas=0)


    def test_actionWithTargetInDarkRoom(self):
        """
        By default, actions which require objects in a darkened room should
        fail, because it's too dark.
        """
        self.assertCommandOutput(
            "create pants named 'pair of pants'",
            ["You create a pair of pants."],
            ["Test Player creates a pair of pants."])

        # The action is going to try to locate its target.  During the graph
        # traversal it shouldn't find _any_ pants.  Whether or not we find any
        # pants, we want the message to note that it's too dark.  The reason is
        # actually a property of a link (or perhaps a set of links: i.e. the
        # me->me link, the me->chair link, the chair->room link) so the
        # retriever is going to need to keep a list of those (Refusals) as it
        # retrieves each one.
        #
        # resolve calls search
        # search calls findProviders
        # findProviders constructs a thingy, calls obtain()

        self.test_actionWithNoTargetInDarkRoom()


    def test_actionWithTargetInAdjacentDarkRoom(self):
        """
        If a player is standing I{next} to a dark room, they should not be able
        to locate targets in the dark room, but the reporting in this case
        should be normal, not the "It's too dark to see" that would result if
        they were in the dark room themselves.
        """
        self.otherRoom = objects.Thing(store=self.store, name=u'Elsewhere')
        objects.Container.createFor(self.otherRoom, capacity=1000)
        objects.Exit.link(self.location, self.otherRoom, u'west')
        self.player.moveTo(self.otherRoom)
        self.observer.moveTo(self.otherRoom)
        self.assertCommandOutput(
            "wear pants",
            [commandutils.E(u"Who's that?")],
            [])


    def test_actionWithNoTargetInDarkRoom(self):
        """
        By default, actions which require objects in a darkened room should
        fail because it's too dark, even if there is actually no target to be
        picked up.
        """
        self._test(
            "wear pants",
            ["It's too dark to see."], # to dark to see... the pants?  any pants?
            [])


    def test_examiningNonThing(self):
        """
        When examining an L{IVisible} which is not also an L{IThing}, it should
        be dark.
        """
        t = objects.Thing(name=u"magic stone", store=self.store)
        t.powerUp(MagicStone(thing=t, store=self.store))
        t.moveTo(self.location)

        self.assertCommandOutput(
            "look at rune",
            ["It's too dark to see."],
            [])
        self.lighting.candelas = 100
        self.assertCommandOutput(
            "look at rune",
            ["A totally mystical rune."],
            [])



class Rune(object):
    """
    This is an example provider of L{iimaginary.IVisible} which is not an
    L{iimaginary.IThing}.
    """

    implements(iimaginary.IVisible, iimaginary.INameable)

    def visualizeWithContents(self, paths):
        """
        Return an L{ExpressString} with a sample string that can be tested
        against.
        """
        return ExpressString("A totally mystical rune.")


    def knownTo(self, observer, asName):
        """
        Implement L{iimaginary.INameable.knownTo} to respond to the word 'rune'
        and nothing else, so that this object may be found by
        L{imaginary.idea.Idea.obtain}.
        """
        return (asName == "rune")



class MagicStone(item.Item, Enhancement):
    """
    This is a magic stone that has a rune on it which you can examine.
    """

    implements(iimaginary.ILinkContributor)
    powerupInterfaces = [iimaginary.ILinkContributor]
    thing = attributes.reference()

    def links(self):
        """
        Implement L{ILinkContributor} to yield a single link to a L{Rune}.
        """
        runeIdea = idea.Idea(Rune())
        yield idea.Link(self.thing.idea, runeIdea)
