# -*- test-case-name: imaginary.test -*-
import pprint
from re import compile, escape as E
E                               # export for other modules

from zope.interface import implements

from twisted.trial import unittest
from twisted.test.proto_helpers import StringTransport

from axiom import store, item, attributes

from imaginary import iimaginary, objects, text, language
from imaginary.wiring import player
from imaginary.world import ImaginaryWorld

class PlayerProtocol(object):
    def __init__(self, transport):
        self.transport = transport

    def write(self, crap):
        self.transport.write(crap)


class CommandTestCaseMixin:
    """
    A mixin for TestCase classes which provides support for testing Imaginary
    environments via command-line transcripts.
    """

    def setUp(self):
        """
        Set up a store with a location, a player and an observer.
        """
        self.store = store.Store()

        self.location = objects.Thing(
            store=self.store,
            name=u"Test Location",
            description=u"Location for testing.",
            proper=True)

        locContainer = objects.Container.createFor(self.location, capacity=1000)

        self.world = ImaginaryWorld(store=self.store, origin=self.location)
        self.player = self.world.create(
            u"Test Player", gender=language.Gender.FEMALE)
        self.playerContainer = iimaginary.IContainer(self.player)
        self.playerWrapper = player.Player(self.player)

        self.playerWrapper.useColors = False
        locContainer.add(self.player)
        self.transport = StringTransport()
        self.playerWrapper.setProtocol(PlayerProtocol(self.transport))

        self.observer = self.world.create(
            u"Observer Player", gender=language.Gender.FEMALE)
        self.observerWrapper = player.Player(self.observer)
        locContainer.add(self.observer)
        self.otransport = StringTransport()
        self.observerWrapper.setProtocol(PlayerProtocol(self.otransport))

        # Clear the transport, since we don't care about the observer
        # arrival event.
        self.transport.clear()


    def tearDown(self):
        """
        Disconnect the player and observer from their respective transports.
        """
        for p in self.player, self.observer:
            try:
                p.destroy()
            except AttributeError:
                pass


    def watchCommand(self, command):
        """
        Make C{self.player} run the given command and return the output both
        she and C{self.observer} receive.

        @param command: The textual command to run.
        @type command: C{unicode}
        @return: The player's output and the third-party observer's output.
        @rtype: Two-tuple of C{unicode}
        """
        self.playerWrapper.parse(command)
        return (
            self.transport.value().decode('utf-8'),
            self.otransport.value().decode('utf-8'))


    def assertCommandOutput(self, command, output, observed=()):
        """
        Verify that when C{command} is executed by this
        L{CommandTestCaseMixin.playerWrapper}, C{output} is produced (to the
        actor) and C{observed} is produced (to the observer).

        @param command: The string for L{CommandTestCaseMixin.playerWrapper} to
            execute.
        @type command: L{str}

        @param output: The expected output of C{command} for
            L{CommandTestCaseMixin.player} to observe.
        @type output: iterable of L{str}

        @param observed: The expected output that
            L{CommandTestCaseMixin.observer} will observe.
        @type observed: iterable of L{str}
        """
        if command is not None:
            # Deprecate this or something
            if not isinstance(command, unicode):
                command = unicode(command, 'ascii')
            self.playerWrapper.parse(command)
            output.insert(0, "> " + command)

        results = []
        for perspective, xport, oput in ([
                ('actor' ,self.transport, output),
                ('observer', self.otransport, observed)]):
            results.append([])
            gotLines = xport.value().decode('utf-8').splitlines()
            for i, (got, expected) in enumerate(map(None, gotLines, oput)):
                got = got or ''
                expected = expected or '$^'
                m = compile(expected.rstrip() + '$').match(got.rstrip())
                if m is None:
                    s1 = pprint.pformat(gotLines)
                    s2 = pprint.pformat(oput)
                    raise unittest.FailTest(
                        "\n%s %s\ndid not match expected\n%s\n(Line %d)" % (
                            repr(perspective), s1, s2, i))
                results[-1].append(m)
            xport.clear()
        return results

    # Old alias.
    _test = assertCommandOutput


    def find(self, name):
        return [
            th
            for th in self.player.findProviders(iimaginary.IThing, 1)
            if th.name == name][0]



def flatten(expr):
    """
    Test utility method to turn a list of strings character attribute
    declarations and similar lists into a single string with all character
    attribute information removed.
    """
    return u''.join(list(text.flatten(expr, currentAttrs=text.AttributeSet())))



class LanguageMixin(object):
    def flatten(self, expr):
        return flatten(expr)



class MockIntelligence(item.Item):
    """
    A persistent intelligence which accumulates observed events in a
    list for later retrieval and assertion. This should be
    instantiated and passed to
    L{iimaginary.IActor.setEnduringIntelligence}.

    XXX: This should probably be unnecessary at some point. It is used
    with code which assumes a persistent intelligence is involved.
    """
    implements(iimaginary.IEventObserver)

    anAttribute = attributes.integer()
    concepts = attributes.inmemory()

    def activate(self):
        self.concepts = []


    def prepare(self, concept):
        return lambda: self.concepts.append(concept)



class MockEphemeralIntelligence(object):
    """
    Like L{MockIntelligence}, but it should be used with
    L{iimaginary.IActor.setEphemeralIntelligence}.
    """
    implements(iimaginary.IEventObserver)

    def __init__(self):
        self.events = []


    def prepare(self, event):
        return lambda: self.events.append(event)



def createPlayer(store, name):
    """
    Create a mock player with a mock intelligence with the given
    name. The intelligence is a L{MockIntelligence} which can have its
    concepts introspected.

    @type store: L{axiom.store.Store}.
    @type name: C{unicode}.
    @param name: The name of the newly-created player.
    @return: A three-tuple of (playerThing, playerActor, playerIntelligence).
    """
    player = objects.Thing(store=store, name=name)
    objects.Container.createFor(player, capacity=100)
    playerActor = objects.Actor.createFor(player)
    playerIntelligence = MockIntelligence(store=store)
    playerActor.setEnduringIntelligence(playerIntelligence)
    return player, playerActor, playerIntelligence

__all__ = ['E', 'CommandTestCaseMixin', 'createPlayer', 'MockIntelligence',
           'PlayerProtocol']
