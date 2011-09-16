
"""
This module contains tests for the examplegame.furniture module.
"""

from twisted.trial.unittest import TestCase

from imaginary.test.commandutils import CommandTestCaseMixin, E

from imaginary.objects import Thing, Container, Exit
from examplegame.furniture import Chair

class SitAndStandTests(CommandTestCaseMixin, TestCase):
    """
    Tests for the 'sit' and 'stand' actions.
    """

    def setUp(self):
        """
        Create a room, with a dude in it, and a chair he can sit in.
        """
        CommandTestCaseMixin.setUp(self)
        self.chairThing = Thing(store=self.store, name=u"chair")
        self.chairThing.moveTo(self.location)
        self.chair = Chair.createFor(self.chairThing)


    def test_sitDown(self):
        """
        Sitting in a chair should move your location to that chair.
        """
        self.assertCommandOutput(
            "sit chair",
            ["You sit in the chair."],
            ["Test Player sits in the chair."])
        self.assertEquals(self.player.location, self.chair.thing)


    def test_standWhenStanding(self):
        """
        You can't stand up - you're already standing up.
        """
        self.assertCommandOutput(
            "stand up",
            ["You're already standing."])


    def test_standWhenSitting(self):
        """
        If a player stands up when sitting in a chair, they should be seen to
        stand up, and they should be placed back into the room where the chair
        is located.
        """
        self.test_sitDown()
        self.assertCommandOutput(
            "stand up",
            ["You stand up."],
            ["Test Player stands up."])
        self.assertEquals(self.player.location, self.location)


    def test_takeWhenSitting(self):
        """
        When a player is seated, they should still be able to take objects on
        the floor around them.
        """
        self.test_sitDown()
        self.ball = Thing(store=self.store, name=u'ball')
        self.ball.moveTo(self.location)
        self.assertCommandOutput(
            "take ball",
            ["You take a ball."],
            ["Test Player takes a ball."])


    def test_moveWhenSitting(self):
        """
        A player who is sitting shouldn't be able to move without standing up
        first.
        """
        self.test_sitDown()
        otherRoom = Thing(store=self.store, name=u'elsewhere')
        Container.createFor(otherRoom, capacity=1000)
        Exit.link(self.location, otherRoom, u'north')
        self.assertCommandOutput(
            "go north",
            ["You can't do that while sitting down."])
        self.assertCommandOutput(
            "go south",
            ["You can't go that way."])


    def test_lookWhenSitting(self):
        """
        Looking around when sitting should display the description of the room.
        """
        self.test_sitDown()
        self.assertCommandOutput(
            "look",
            # I'd like to add ', in the chair' to this test, but there's
            # currently no way to modify the name of the object being looked
            # at.
            [E("[ Test Location ]"),
             "Location for testing.",
             "Observer Player and a chair"])


