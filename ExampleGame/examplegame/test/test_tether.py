
from twisted.trial.unittest import TestCase

from imaginary.test.commandutils import CommandTestCaseMixin, E

from imaginary.objects import Thing, Container, Exit
from imaginary.garments import Garment

from examplegame.furniture import Chair
from examplegame.tether import Tether

class TetherTest(CommandTestCaseMixin, TestCase):
    """
    A test for tethering an item to its location, such that a player who picks
    it up can't leave until they drop it.
    """

    def setUp(self):
        """
        Tether a ball to the room.
        """
        CommandTestCaseMixin.setUp(self)
        self.ball = Thing(store=self.store, name=u'ball')
        self.ball.moveTo(self.location)
        self.tether = Tether.createFor(self.ball, to=self.location)
        self.otherPlace = Thing(store=self.store, name=u'elsewhere')
        Container.createFor(self.otherPlace, capacity=1000)
        Exit.link(self.location, self.otherPlace, u'north')


    def test_takeAndLeave(self):
        """
        You can't leave the room if you're holding the ball that's tied to it.
        """
        self.assertCommandOutput(
            "take ball",
            ["You take a ball."],
            ["Test Player takes a ball."])
        self.assertCommandOutput(
            "go north",
            ["You can't move, you're still holding a ball."],
            ["Test Player struggles with a ball."])
        self.assertCommandOutput(
            "drop ball",
            ["You drop the ball."],
            ["Test Player drops a ball."])
        self.assertCommandOutput(
            "go north",
            [E("[ elsewhere ]"),
             E("( south )"),
             ""],
            ["Test Player leaves north."])


    def test_allTiedUp(self):
        """
        If you're tied to a chair, you can't leave.
        """
        chairThing = Thing(store=self.store, name=u'chair')
        chairThing.moveTo(self.location)
        chair = Chair.createFor(chairThing)
        self.assertCommandOutput("sit chair",
                                 ["You sit in the chair."],
                                 ["Test Player sits in the chair."])
        Tether.createFor(self.player, to=chairThing)
        self.assertCommandOutput(
            "stand up",
            ["You can't move, you're tied to a chair."],
            ["Test Player struggles."])


    def test_tetheredClothing(self):
        """
        Clothing that is tethered will also prevent movement if you wear it.

        This isn't just simply a test for clothing; it's an example of
        integrating with a foreign system which doesn't know about tethering,
        but can move objects itself.

        Tethering should I{not} have any custom logic related to clothing to
        make this test pass; if it does get custom clothing code for some
        reason, more tests should be added to deal with other systems that do
        not take tethering into account (and vice versa).
        """
        Garment.createFor(self.ball, garmentDescription=u"A lovely ball.",
                          garmentSlots=[u"head"])
        self.assertCommandOutput(
            "wear ball",
            ["You put on the ball."],
            ["Test Player puts on a ball."])
        self.assertCommandOutput(
            "go north",
            ["You can't move, you're still holding a ball."],
            ["Test Player struggles with a ball."])


