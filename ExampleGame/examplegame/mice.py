# -*- test-case-name: examplegame.test.test_mice,examplegame.test.test_japanese -*-

import random

from zope.interface import implements

from axiom import item, attributes

from imaginary import iimaginary, events, objects, action, language
from examplegame import japanese


class Mouse(item.Item):
    """
    A silly mouse which squeaks when actors enter the room it is in.

    @ivar _callLater: The scheduling function to use. Override in unit
    tests only.
    """

    implements(iimaginary.IEventObserver)

    squeakiness = attributes.integer(doc="""
    How likely the mouse is to squeak when intruded upon (0 - 100).

    This mouse is so angry that he will pretty much always squeak.
    """, default=100)

    _callLater = attributes.inmemory()

    def activate(self):
        from twisted.internet import reactor
        self._callLater = reactor.callLater


    def prepare(self, concept):
        """
        An event was received. Squeak if it represents the arrival of a dude.
        """
        if isinstance(concept, events.ArrivalEvent):
            return lambda: self._callLater(0, self.squeak)
        return lambda: None


    def squeak(self):
        actor = self.store.findUnique(
            objects.Actor,
            objects.Actor._enduringIntelligence == self)
        evt = events.Success(
            actor=actor.thing,
            otherMessage=u"SQUEAK!")
        evt.broadcast()



class ChallengeCollision(Exception):
    """
    Raised when a L{HiraganaMouse} is asked to start issuing challenges when it
    is already issuing challenges.
    """



class ChallengeVacuum(Exception):
    """
    Raised when a L{HiraganaMouse} is asked to stop issuing challenges when it
    is already not issuing challenges.
    """



class HiraganaMouse(item.Item):
    """
    A mouse which occasionally challenges those in its location to
    transliterate Hiragana.

    @ivar _callLater: The scheduling function to use. Defaults to the
    reactor's callLater method. This is parameterized for the sake of
    unit tests.
    """

    implements(iimaginary.IEventObserver)

    challenging = attributes.boolean(doc="""
    Whether or not this mouse is currently creating random challenges.
    """, default=False)

    challengeInterval = attributes.integer(doc="""
    Number of seconds between challenges.
    """, default=15, allowNone=False)

    _currentChallenge = attributes.text(doc="""
    The Hiragana character which the mouse has most recently issued as a
    challenge.
    """, default=None)


    _callLater = attributes.inmemory()
    _currentChallengeCall = attributes.inmemory()

    def activate(self):
        from twisted.internet import reactor
        self._callLater = reactor.callLater

    def _actor(self):
        """
        Get the h-mouse's associated actor. PRIVATE. WHY DID I DOCUMENT THIS.
        """
        return self.store.findUnique(
            objects.Actor,
            objects.Actor._enduringIntelligence == self)


    def _numDudes(self):
        """
        Get the number of actors (other than the h-mouse) in the
        h-mouse's location. PRIVATE.
        """
        actor = self._actor()
        numDudes = len([actor
                        for dude
                        in actor.thing.findProviders(iimaginary.IActor, 1)
                        if dude is not actor])
        return numDudes


    def maybeChallenge(self):
        """ 
        Start challenging if there is anyone around to challenge (and
        this h-mouse isn't already challenging).
        """
        if not self.challenging and self._numDudes() >= 1:
            self.startChallenging()


    def prepare(self, concept):
        """
        An event was received. Start or stop challenging as
        appropriate, based on whether there is anyone to challenge.
        """
        if isinstance(concept, events.ArrivalEvent):
            self.maybeChallenge()
        elif isinstance(concept, events.DepartureEvent) and self._numDudes() == 0:
            self.stopChallenging()
        elif isinstance(concept, events.SpeechEvent) and concept.speaker is not self._actor().thing:
            self.responseReceived(concept.speaker, concept.text)
        return lambda: None


    def startChallenging(self):
        """
        Start shouting hiragana in the hope that someone knows what it means.

        @raises ChallengeCollision: If this h-mouse is already challenging.
        """
        if self.challenging:
            raise ChallengeCollision()

        self.challenging = True
        self._scheduleChallenge()


    def _scheduleChallenge(self):
        """
        Schedule a challenge to happen in the number of seconds set in
        the instance attribute 'challengeInterval'.
        """
        self._currentChallengeCall = self._callLater(self.challengeInterval, 
                                                     self._challengeAndRepeat)


    def stopChallenging(self):
        """
        Stop shouting hiragana.
        
        @raises ChallengeVacuum: If this h-mouse is not currently challenging.
        """
        if not self.challenging:
            raise ChallengeVacuum()

        self.challenging = False

        self._currentChallenge = None
        self._currentChallengeCall.cancel()
        self._currentChallengeCall = None


    def _challengeAndRepeat(self):
        """
        Shout a challenge and then schedule another one.
        """
        self.challenge()
        self._scheduleChallenge()


    def getCurrentChallenge(self):
        """
        Return the Hiragana character which is this mouse's current challenge,
        if it has one.

        @rtype: C{unicode} or C{None}
        """
        return self._currentChallenge


    def vetteChallengeResponse(self, romajiResponse):
        """
        Return True if the given response matches the current challenge, False
        otherwise.
        """
        hiragana = japanese.romajiToHiragana.get(romajiResponse.upper(), None)
        return hiragana is not None and self.getCurrentChallenge() in hiragana


    def responseReceived(self, responder, romajiResponse):
        """
        Called when some speech is observed.
        """
        me = self._actor().thing
        if self.vetteChallengeResponse(romajiResponse):
            self._currentChallenge = None
            verb = u"salute"
        else:
            verb = u"bite"
        evt = events.Success(
            actor=me,
            target=responder,
            actorMessage=language.Sentence(["You ", verb, " ", responder, "."]),
            targetMessage=language.Sentence([language.Noun(me).shortName(), " ", verb, "s you!"]),
            otherMessage=language.Sentence([me, " ", verb, "s ", responder, "."]))
        # Fuck the reactor, Fuck scheduling, why does responseReceived
        # need to be concerned with these stupid scheduling details
        # when all it wants to do is respond basically-immediately.
        self._callLater(0, evt.broadcast)


    def challenge(self, character=None):
        """
        Say only a single random hiragana character.
        """
        if character is None:
            character = random.choice(japanese.hiragana.keys())
        self._currentChallenge = character
        actor = self._actor()
        action.Say().do(actor.thing, None, character)



def createMouseCreator(mouseIntelligenceFactory):
    """
    Create a createMouse function, which can be called to create a
    mouse object. Used for the 'Create' command plugin system.
    """
    def createMouse(**kw):
        store = kw['store']
        mouse = objects.Thing(**kw)
        mouseActor = objects.Actor.createFor(mouse)
        mousehood = mouseIntelligenceFactory(store=store)
        mouseActor.setEnduringIntelligence(mousehood)
        return mouse
    return createMouse

createMouse = createMouseCreator(Mouse)
createHiraganaMouse = createMouseCreator(HiraganaMouse)
