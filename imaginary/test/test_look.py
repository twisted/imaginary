"""
Tests for L{imaginary.action.LookAt} and L{imaginary.action.LookAround}.
"""
from __future__ import print_function
from textwrap import dedent

from twisted.trial.unittest import TestCase

from zope.interface import implementer

from characteristic import attributes as has_attributes
from axiom import store, item, attributes

from imaginary import iimaginary, objects, language, action, events
from imaginary.enhancement import Enhancement
from imaginary.world import ImaginaryWorld
from imaginary.test.commandutils import (
    CommandTestCaseMixin, E, createLocation, flatten)


class TestIntelligence(object):
    def __init__(self):
        self.observedConcepts = []


    def prepare(self, concept):
        return lambda: self.observedConcepts.append(concept)



class LookContext(object):
    def __init__(self):
        self.store = store.Store()

        locContainer = createLocation(
            self.store, name=u"Test Location",
            description=u"Location for testing.")
        self.location = locContainer.thing

        self.world = ImaginaryWorld(store=self.store)
        self.player = self.world.create(u"Test Player", gender=language.Gender.FEMALE)
        locContainer.add(self.player)
        self.actor = iimaginary.IActor(self.player)
        self.actor.setEphemeralIntelligence(TestIntelligence())



class LookAroundTranscriptTests(CommandTestCaseMixin, TestCase):
    """
    Transcript-style tests for I{look}.
    """
    def test_emptyLocation(self):
        iimaginary.IContainer(self.location).remove(self.observer)
        self._test(
            u"look",
            [E(u"[ Test Location ]"),
             u"Location for testing.",
             ])


    def test_siblingObject(self):
        self._test(
            "look",
            [E(u"[ Test Location ]"),
             u"Location for testing.",
             u"Here, you see Observer Player."])


    def test_cousinObject(self):
        o = objects.Thing(store=self.store, name=u"foo")
        iimaginary.IContainer(self.observer).add(o)
        self._test(
            "look",
            [E(u"[ Test Location ]"),
             u"Location for testing.",
             u"Here, you see Observer Player."])


    def test_childObject(self):
        o = objects.Thing(store=self.store, name=u"foo")
        self.playerContainer.add(o)
        self._test(
            "look",
            [E(u"[ Test Location ]"),
             u"Location for testing.",
             u"Here, you see Observer Player."])


    def test_equipment(self):
        self.observer.moveTo(None)
        self._test(u"create a shirt named t-shirt", [u"You create a t-shirt."])
        self._test(u"wear t-shirt", [u"You put on the t-shirt."])
        self._test(
            u"look",
            [E(u"[ Test Location ]"),
             E(u"Location for testing.")])



@implementer(iimaginary.ILitLink)
@has_attributes(["bear"])
class BearsHiddenBeyondThisLink(object):
    """
    An annotation for a link implementing L{BearBlindness}.
    """

    def isItLit(self, path):
        """
        Any path that passes through a L{BearsHiddenBeyondThisLink} link and
        terminates in a bear is shrouded in darkness.  The bear lies in wait.
        """
        schroedingerBear = path.targetAs(iimaginary.IThing)
        actualBear = self.bear
        if schroedingerBear == actualBear:
            return False
        else:
            return True


    def whyNotLit(self):
        """
        The reason that a bear is obscured is L{BearsWhyNot}.
        """
        return BearsWhyNot()


    def applyLighting(self, litThing, it, interface):
        """
        L{iimaginary.ILitLink.applyLighting} can modify a target that has had
        lighting applied to it; in the case of this annotation things are
        either completely not lit at all (bears) or fully lit and appear normal
        (everything else) so we just always return the thing itself and don't
        modify it.
        """
        return it



class BearsWhyNot(object):
    """
    A reason you can't see something: it's a bear, and you're blind to bears,
    that's why you can't see it.
    """

    def tellMeWhyNot(self):
        """
        An evocative message that the user probably won't see (since they can't
        in fact see this bear).
        """
        return u"IT'S A BEAR"



interfaces = [iimaginary.ILinkAnnotator]
@implementer(*interfaces)
class BearBlindness(item.Item, Enhancement):
    """
    An enhancement for an actor which causes that actor to become unable to see
    bears.

    (This could be installed on something other than an actor, which would
    cause all bears on the other side of whatever link it was to become
    invisible to all.)
    """
    powerupInterfaces = interfaces

    thing = attributes.reference(
        """
        This is a reference to a Thing which is blind to bears.
        """
    )

    bear = attributes.reference(
        """
        This is a reference to a Thing which is the one and only bear in the
        universe, which you cannot see.

        THERE CAN ONLY BE ONE.
        """
    )

    def annotationsFor(self, link, idea):
        """
        Yield an annotation for all links which causes bears on the opposite
        side of you to be invisible to you.
        """
        yield BearsHiddenBeyondThisLink(bear=self.bear)



class LookAtTranscriptTests(CommandTestCaseMixin, TestCase):
    def test_bearBlindness(self):
        """
        If I cast a spell on you which makes you unable to see bears, you
        should not see a bear in the room with you when you look at the room
        around you.
        """
        bear = objects.Thing(store=self.store,
                             name=u"Bear",
                             location=self.location)
        BearBlindness(store=self.store,
                      thing=self.player,
                      bear=bear).applyEnhancement()
        self._test(
            "look here",
            [E("[ Test Location ]"),
             E("Location for testing."),
             "Here, you see Observer Player."])



    def test_exits(self):
        objects.Exit.link(self.location, self.location, u"north")
        self._test(
            "look here",
            [E("[ Test Location ]"),
             E("( north south )"),
             E("Location for testing."),
             "Here, you see Observer Player."])


    def test_lookMe(self):
        self._test(
            "look me",
            [E("[ Test Player ]"),
             "Test Player is great.",
             "She is naked."])


    def test_lookAtMe(self):
        self._test(
            "look at me",
            [E("[ Test Player ]"),
             "Test Player is great.",
             "She is naked."])


    def test_lookAtAnother(self):
        self._test(
            "look at Observer Player",
            [E("[ Observer Player ]"),
             "Observer Player is great.",
             "She is naked."],
            ["Test Player looks at you."])


    def test_lookAtThing(self):
        o = objects.Thing(store=self.store, name=u"foo")
        iimaginary.IContainer(self.location).add(o)
        self._test(
            "look at foo",
            [E("[ foo ]")])


    def test_lookAtMissing(self):
        self._test(
            "look at bar",
            ["You don't see that."])



class LookAroundTests(TestCase):
    """
    Tests for L{imaginary.action.LookAround}.
    """
    def setUp(self):
        self.context = LookContext()


    def test_eventBroadcasting(self):
        """
        The L{LookAround} action broadcasts an L{events.Success} to the actor.
        """
        action.LookAround().runEventTransaction(
            self.context.player, u"look", {})
        [event] = self.context.actor.getIntelligence().observedConcepts
        self.assertIsInstance(event, events.Success)



class LookAtTests(TestCase):
    """
    Tests for L{imaginary.action.LookAt}.
    """
    def setUp(self):
        self.context = LookContext()


    def test_exitNameEventBroadcasting(self):
        target = objects.Thing(
            store=self.context.store,
            name=u"Visible Location",
            description=u"Description of visible location.",
            proper=True)
        objects.Container.createFor(target, capacity=1000)
        objects.Exit.link(self.context.location, target, u"south")

        action.LookAt().runEventTransaction(
            self.context.player, u"look", {"target": u"south"})
        evts = self.context.actor.getIntelligence().observedConcepts
        self.assertEqual(1, len(evts))
        self.assertIsInstance(evts[0], events.Success)
        self.assertEqual(
            dedent(u"""
            [ Visible Location ]
            ( north )
            Description of visible location.
            """).lstrip(),
            flatten(evts[0].actorMessage.plaintext(self.context.actor.thing)))



