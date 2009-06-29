import weakref

from twisted.internet import task
from twisted.trial import unittest

from axiom import store

from imaginary import iimaginary, objects, events, action

from imaginary.test import commandutils

from examplegame import mice
from examplegame import japanese

class MouseChallengeMixin(object):
    """
    A mixin meant to be used in TestCases which want to assert things
    about mouse challenges.

    The subclass must be sure to provide a C{player} instance
    attribute, which is the L{IThing<iimaginary.IThing>} provider of
    the player which observes the mouse, and a C{mouseName} attribute
    which should be the mouse's name.
    """
    def assertChallenge(self, concept):
        """
        Assert that the given concept is a challenge from the mouse
        named self.mouseName, as observed by self.player.
        """
        said = commandutils.flatten(concept.plaintext(self.player))
        self.failUnless(said.startswith(u"A %s says, '" % (self.mouseName,)), repr(said))
        self.failUnlessIn(said[-3], japanese.hiragana)
        self.failUnless(said.endswith("'\n"), repr(said))



class HiraganaMouseTestCase(MouseChallengeMixin, unittest.TestCase):
    """
    Test that there is a mouse that says hiragana and stuff
    """

    def setUp(self):
        self.store = store.Store()

        self.clock = objects.Thing(store=self.store, name=u"Clock")
        self.clockContainer = objects.Container.createFor(self.clock, capacity=10)

        self.mouseName = u"\N{KATAKANA LETTER PI}\N{KATAKANA LETTER SMALL YU}"
        self.mouse = mice.createHiraganaMouse(
            store=self.store,
            name=self.mouseName)
        self.mouseActor = iimaginary.IActor(self.mouse)
        self.mousehood = self.mouseActor.getIntelligence()
        self.mouse.moveTo(self.clock)

        (self.player,
         self.playerActor,
         self.playerIntelligence) = commandutils.createPlayer(self.store,
                                                              u"Mean Old Man")


        self.player.moveTo(self.clock)

        self.reactorTime = task.Clock()
        self.mousehood._callLater = self.reactorTime.callLater


    def test_mouseCanSqueak(self):
        """
        When explicitly told to challenge with a given romaji syllable, the
        mouse should say a hiragana letter.
        """
        events.runEventTransaction(
            self.store,
            self.mousehood.challenge,
            character=u"\N{HIRAGANA LETTER A}")

        self.assertEquals(len(self.playerIntelligence.concepts), 1)
        event = self.playerIntelligence.concepts[0]
        self.assertEquals(
            commandutils.flatten(event.otherMessage.plaintext(self.player)),
            u"A %s says, '\N{HIRAGANA LETTER A}'" % (self.mouseName,))


    def test_randomHiragana(self):
        """
        When explicitly told to challenge without specifying a syllable, the
        mouse should say a random one.
        """
        events.runEventTransaction(self.store, self.mousehood.challenge)
        self.assertEquals(len(self.playerIntelligence.concepts), 1)
        event = self.playerIntelligence.concepts[0]
        self.assertChallenge(event)


    def test_ji(self):
        """
        Two hiragana characters map to the romaji 'ji'.  Test that we do the
        right thing for them.
        """
        self.mousehood.challenge(character=u"\N{HIRAGANA LETTER DI}")
        self.failUnless(self.mousehood.vetteChallengeResponse(u"ji"))
        self.mousehood.challenge(character=u"\N{HIRAGANA LETTER ZI}")
        self.failUnless(self.mousehood.vetteChallengeResponse(u"ji"))


    def test_zu(self):
        """
        Two hiragana characters map to the romaji 'zu'.  Test that we do the
        right thing for them.
        """
        self.mousehood.challenge(character=u"\N{HIRAGANA LETTER DU}")
        self.failUnless(self.mousehood.vetteChallengeResponse(u"zu"))
        self.mousehood.challenge(character=u"\N{HIRAGANA LETTER ZU}")
        self.failUnless(self.mousehood.vetteChallengeResponse(u"zu"))


    def test_mouseStartsChallengingWhenPlayersArrive(self):
        """
        When a player arrives, the mouse should go into the 'I am
        challenging' state.
        """
        # Whitebox
        self.assertEquals(self.mousehood.challenging, False)

        evt = events.ArrivalEvent(actor=self.player)
        self.mouseActor.send(evt)

        self.assertEquals(self.mousehood.challenging, True)


    def test_mouseSchedulesChallenges(self):
        """
        After telling a mouse to start challenging, it should schedule timed
        events to say challenges.
        """
        self.mousehood.startChallenging()
        self.reactorTime.advance(self.mousehood.challengeInterval)
        concepts = self.playerIntelligence.concepts
        self.assertEquals(len(concepts), 1)
        self.assertChallenge(concepts[0])


    def test_mouseStopsChallengingWhenPlayersLeave(self):
        """
        When the 'last' player leaves, the mouse stops challenging.
        """
        # Whitebox
        self.mousehood.startChallenging()

        evt = events.DepartureEvent(location=self.clock,
                                    actor=self.player)
        self.player.moveTo(None)
        self.mouseActor.send(evt)

        self.assertEquals(self.mousehood.challenging, False)


    def test_mouseStopsSchedulingChallenges(self):
        """
        When a mouse is told to stop challenging, it should cancel any
        challenges it had scheduled.
        """
        self.mousehood.startChallenging()
        self.mousehood.stopChallenging()

        self.reactorTime.advance(self.mousehood.challengeInterval)
        self.assertEquals(self.playerIntelligence.concepts, [])


    def test_stopChallengingWhenNotChallengingFails(self):
        """
        Don't stop challenging when you're not challenging.
        """
        self.assertRaises(mice.ChallengeVacuum, self.mousehood.stopChallenging)


    def test_startChallengingTwiceFails(self):
        """
        Don't start challenging twice.
        """
        self.mousehood.startChallenging()
        self.assertRaises(mice.ChallengeCollision, self.mousehood.startChallenging)


    def test_challengeRecurrence(self):
        """
        After a challenge is issued another one should be issued later.
        """
        self.mousehood.startChallenging()
        self.reactorTime.advance(self.mousehood.challengeInterval)

        self.assertIn(self.mousehood.getCurrentChallenge(), japanese.hiragana)

        self.mousehood._currentChallenge = None # Clear his challenge evilly

        self.reactorTime.advance(self.mousehood.challengeInterval)

        self.assertIn(self.mousehood.getCurrentChallenge(), japanese.hiragana)


    def test_twoMenEnter(self):
        """
        Test that when *TWO* players join, the mouse doesn't schedule too many
        challenges.
        """
        otherPlayer = commandutils.createPlayer(self.store,
                                                u"Polite Young Man")[0]

        # Send an arrival event because setUp doesn't
        firstEvent = events.ArrivalEvent(actor=self.player)

        self.mouseActor.send(firstEvent)
        otherPlayer.moveTo(self.clock, arrivalEventFactory=events.MovementArrivalEvent)

        self.playerIntelligence.concepts = []
        self.reactorTime.advance(self.mousehood.challengeInterval)

        self.assertEquals(len(self.playerIntelligence.concepts), 1)
        self.assertChallenge(self.playerIntelligence.concepts[0])


    def test_twoMenLeave(self):
        """
        Test that when two players are near the mouse, the mouse doesn't
        unschedule its challenge until they both leave.
        """
        otherPlayer = commandutils.createPlayer(self.store,
                                                u"Polite Young Man")[0]
        otherPlayer.moveTo(self.clock)

        self.mousehood.startChallenging()

        firstEvent = events.DepartureEvent(location=self.clock,
                                           actor=self.player)
        secondEvent = events.DepartureEvent(location=self.clock,
                                            actor=otherPlayer)

        otherPlayer.moveTo(None)
        self.mouseActor.send(secondEvent)

        self.playerIntelligence.concepts = []

        self.reactorTime.advance(self.mousehood.challengeInterval)

        self.assertEquals(len(self.playerIntelligence.concepts), 1)
        self.assertChallenge(self.playerIntelligence.concepts[0])

        self.player.moveTo(None)
        self.mouseActor.send(firstEvent)

        self.failIf(self.mousehood.challenging)


    def test_getCurrentChallenge(self):
        """
        Test that we can introspect the current challenge of a mouse.
        """
        self.mousehood.startChallenging()
        self.reactorTime.advance(self.mousehood.challengeInterval)
        self.failUnlessIn(self.mousehood.getCurrentChallenge(), japanese.hiragana)

        self.mousehood.stopChallenging()
        self.assertIdentical(self.mousehood.getCurrentChallenge(), None)


    def test_vetteChallengeResponse(self):
        """
        Test that the correct response to the current challenge is accepted by
        the mouse.
        """
        self.mousehood.startChallenging()
        self.reactorTime.advance(self.mousehood.challengeInterval)

        romaji = japanese.hiragana[self.mousehood.getCurrentChallenge()]
        self.failUnless(self.mousehood.vetteChallengeResponse(romaji))

        for romaji in japanese.hiragana.values():
            if romaji != japanese.hiragana[self.mousehood.getCurrentChallenge()]:
                self.failIf(self.mousehood.vetteChallengeResponse(romaji))


    def test_respondToChallengeCorrectly(self):
        """
        Test that when a correct response is received, the current challenge is
        expired and the mouse salutes you.
        """
        self.mousehood.startChallenging()
        self.reactorTime.advance(self.mousehood.challengeInterval)

        correctResponse = japanese.hiragana[
            self.mousehood.getCurrentChallenge()]

        self.mousehood.responseReceived(self.player, correctResponse)
        self.reactorTime.advance(0)

        self.assertIdentical(self.mousehood.getCurrentChallenge(), None)

        self.assertEquals(len(self.playerIntelligence.concepts), 2)
        c = self.playerIntelligence.concepts[1]
        self.assertEquals(
            commandutils.flatten(c.plaintext(self.player)),
            u"%s salutes you!\n" % (self.mouseName,))


    def test_respondToChallengeInorrectly(self):
        """
        Test that when an incorrect response is received, the current challenge
        is not expired and the mouse bites you.
        """
        self.mousehood.startChallenging()
        self.reactorTime.advance(self.mousehood.challengeInterval)

        correctResponse = japanese.hiragana[
            self.mousehood.getCurrentChallenge()]

        for ch in japanese.hiragana.values():
            if ch != correctResponse:
                self.mousehood.responseReceived(self.player, ch)
                break
        else:
            self.fail("Buggy test")

        self.reactorTime.advance(0)

        self.assertIn(self.mousehood.getCurrentChallenge(),
                      japanese.romajiToHiragana[correctResponse])

        self.assertEquals(len(self.playerIntelligence.concepts), 2)
        c = self.playerIntelligence.concepts[1]
        self.assertEquals(
            commandutils.flatten(c.plaintext(self.player)),
            u"%s bites you!\n" % (self.mouseName,))


    def test_playerSaysCorrectThing(self):
        """
        Test that when someone gives voice to the correct response to a mouse's
        current challenge, the mouse acknowledges this with a salute.
        """
        self.mousehood.startChallenging()
        self.reactorTime.advance(self.mousehood.challengeInterval)
        action.Say().do(
            # http://divmod.org/trac/ticket/2917
            iimaginary.IActor(self.player),
            None,
            japanese.hiragana[self.mousehood.getCurrentChallenge()])

        self.assertIdentical(self.mousehood.getCurrentChallenge(), None)
        self.reactorTime.advance(0)

        self.assertEquals(len(self.playerIntelligence.concepts), 3)
        c = self.playerIntelligence.concepts[2]
        self.assertEquals(
            commandutils.flatten(c.plaintext(self.player)),
            u"%s salutes you!\n" % (self.mouseName,))


    def test_playerSaysIncorrectThing(self):
        """
        Test that when someone gives voice to the correct response to a mouse's
        current challenge, the mouse acknowledges this with a salute.
        """
        self.mousehood.startChallenging()
        self.reactorTime.advance(self.mousehood.challengeInterval)

        action.Say().do(
            # http://divmod.org/trac/ticket/2917
            iimaginary.IActor(self.player), None, u"lolololo pew")

        self.failIfIdentical(self.mousehood.getCurrentChallenge(), None)
        self.reactorTime.advance(0)

        self.assertEquals(len(self.playerIntelligence.concepts), 3)
        c = self.playerIntelligence.concepts[2]
        self.assertEquals(
            commandutils.flatten(c.plaintext(self.player)),
            u"%s bites you!\n" % (self.mouseName,))


    def test_activationUsesReactorScheduling(self):
        """
        Test that the default scheduler of the mouse is the Twisted
        reactor, since that is the scheduler that needs to be used
        with the actual Imaginary server.
        """
        deletions = []
        ref = weakref.ref(self.mousehood, deletions.append)
        # This is a hack to reload the mouse since it gets its
        # _callLater set in setUp.
        del self.mouse
        del self.mouseActor
        del self.mousehood
        self.assertEquals(deletions, [ref])
        mousehood = self.store.findUnique(mice.HiraganaMouse)
        from twisted.internet import reactor
        self.assertEquals(mousehood._callLater, reactor.callLater)



class HiraganaMouseCommandTestCase(commandutils.CommandTestCaseMixin, unittest.TestCase):
    """
    H-mouse tests which use the command system.
    """

    mouseName = u"\N{KATAKANA LETTER PI}\N{KATAKANA LETTER SMALL YU}"
    hiraganaCharacterPattern = u"'[" + u''.join(japanese.hiragana.keys()) + u"]'"
    speechPattern = mouseName + u" says, " + hiraganaCharacterPattern

    def test_oneManEnters(self):
        """
        Test that when a fellow jaunts into a venue inhabited by a mouse of the
        Nipponese persuasion, a hiragana allocution follows.
        """
        clock = task.Clock()

        closet = objects.Thing(store=self.store, name=u"Closet")
        closetContainer = objects.Container.createFor(closet, capacity=500)

        mouse = mice.createHiraganaMouse(
            store=self.store,
            name=self.mouseName,
            proper=True)
        mouseActor = iimaginary.IActor(mouse)
        mousehood = mouseActor.getIntelligence()
        mousehood._callLater = clock.callLater
        mouse.moveTo(closet)

        objects.Exit.link(self.location, closet, u"north")

        self._test(
            "north",
            [commandutils.E("[ Closet ]"),
             commandutils.E("( south )"),
             commandutils.E(self.mouseName)],
            ["Test Player leaves north."])

        clock.advance(mousehood.challengeInterval)

        self._test(None, [self.speechPattern])


    def test_creation(self):
        """
        Test the creation of a hiragana-speaking mouse using the thing creation
        plugin system.
        """
        self._test(
            u"create the 'hiragana mouse' named " + self.mouseName,
            [commandutils.E(u"You create " + self.mouseName + u".")],
            [commandutils.E(u"Test Player creates %s." % (self.mouseName,))])

        for thing in self.location.findProviders(iimaginary.IThing, 0):
            if thing.name == self.mouseName:
                break
        else:
            self.fail("Could not find the mouse!  Test bug.")

        clock = task.Clock()
        jimhood = iimaginary.IActor(thing).getIntelligence()
        jimhood._callLater = clock.callLater

        self._test(
            u"drop " + self.mouseName,
            [commandutils.E(u"You drop %s." % (self.mouseName,))],
            [commandutils.E(u"Test Player drops %s." % (self.mouseName,))])

        clock.advance(jimhood.challengeInterval)

        self._test(
            None,
            [self.speechPattern],
            [self.speechPattern])
