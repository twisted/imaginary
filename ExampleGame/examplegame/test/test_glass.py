
"""
Tests for L{examplegame.glass}
"""

from twisted.trial.unittest import TestCase

from imaginary.test.commandutils import CommandTestCaseMixin, E

from imaginary.objects import Thing, Container

from examplegame.glass import GlassBox

class GlassBoxTests(CommandTestCaseMixin, TestCase):
    """
    Tests for L{GlassBox}
    """

    def setUp(self):
        """
        Create a room with a L{GlassBox} in it, which itself contains a ball.
        """
        CommandTestCaseMixin.setUp(self)
        self.box = Thing(store=self.store, name=u'box',
                         description=u'The system under test.')
        self.ball = Thing(store=self.store, name=u'ball',
                          description=u'an interesting object')
        self.container = Container.createFor(self.box)
        GlassBox.createFor(self.box)
        self.ball.moveTo(self.box)
        self.box.moveTo(self.location)
        self.container.closed = True


    def test_lookThrough(self):
        """
        You can see items within a glass box by looking at them directly.
        """
        self.assertCommandOutput(
            "look at ball",
            [E("[ ball ]"),
             "an interesting object"])


    def test_lookAt(self):
        """
        You can see the contents within a glass box by looking at the box.
        """
        self.assertCommandOutput(
            "look at box",
            [E("[ box ]"),
             "The system under test.",
             "It contains a ball."])


    def test_take(self):
        """
        You can't take items within a glass box.
        """
        self.assertCommandOutput(
            "get ball",
            ["You can't reach through the glass box."])


    def test_openTake(self):
        """
        Taking items from a glass box should work if it's open.
        """
        self.container.closed = False
        self.assertCommandOutput(
            "get ball",
            ["You take a ball."],
            ["Test Player takes a ball."])


    def test_put(self):
        """
        You can't put items into a glass box.
        """
        self.container.closed = False
        self.ball.moveTo(self.location)
        self.container.closed = True
        self.assertCommandOutput(
            "put ball in box",
            ["The box is closed."])


    def test_whyNot(self):
        """
        A regression test; there was a bug where glass boxes would interfere
        with normal target-acquisition error reporting.
        """
        self.assertCommandOutput(
            "get foobar",
            ["Nothing like that around here."])
