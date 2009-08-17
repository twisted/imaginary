
from twisted.trial.unittest import TestCase

from imaginary.test.commandutils import CommandTestCaseMixin

from imaginary.objects import Thing, Container

from examplegame.squeaky import Squeaker

class SqueakTest(CommandTestCaseMixin, TestCase):
    """
    Squeak Test.
    """

    def setUp(self):
        """
        Set Up.
        """
        CommandTestCaseMixin.setUp(self)
        self.squeaker = Thing(store=self.store, name=u"squeaker")
        self.squeaker.moveTo(self.location)
        self.squeakification = Squeaker.createFor(self.squeaker)


    def test_itSqueaks(self):
        """
        Picking up a squeaky thing makes it emit a squeak.
        """
        self.assertCommandOutput(
            "take squeaker",
            ["You take a squeaker.",
             "A squeaker emits a faint squeak."],
            ["Test Player takes a squeaker.",
             "A squeaker emits a faint squeak."])


    def test_squeakyContainer(self):
        """
        If a container is squeaky, that shouldn't interfere with its function
        as a container.  (i.e. let's make sure that links keep working even
        though we're using an annotator here.)
        """
        cont = Container.createFor(self.squeaker)

        mcguffin = Thing(store=self.store, name=u"mcguffin")
        mcguffin.moveTo(cont)

        self.assertCommandOutput(
            "take mcguffin from squeaker",
            ["You take a mcguffin from the squeaker."],
            ["Test Player takes a mcguffin from the squeaker."])
