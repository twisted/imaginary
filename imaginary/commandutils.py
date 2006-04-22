# -*- test-case-name: imaginary.test -*-
import pprint
import re

from twisted.trial import unittest
from twisted.test.proto_helpers import StringTransport

from axiom import store

from imaginary import objects
from imaginary.wiring import player


E = re.escape

def _makePlayer(store, name):
    obj = objects.Thing(store=store, name=name)
    obj.weight = 100
    actor = objects.Actor(store=store)
    actor.installOn(obj)
    playerContainer = objects.Container(store=store, capacity=90)
    playerContainer.installOn(obj)
    return obj, player.Player(obj)


class PlayerProtocol(object):
    def __init__(self, transport):
        self.transport = transport

    def write(self, crap):
        self.transport.write(crap)


class CommandTestCaseMixin:
    def setUp(self):
        self.store = store.Store()

        self.location = objects.Thing(
            store=self.store,
            name=u"Test Location",
            description=u"Location for testing.")

        locContainer = objects.Container(store=self.store, capacity=1000)
        locContainer.installOn(self.location)

        self.player, self.playerWrapper = _makePlayer(self.store, u"Test Player")

        self.playerWrapper.useColors = False
        locContainer.add(self.player)
        self.transport = StringTransport()
        self.playerWrapper.setProtocol(PlayerProtocol(self.transport))

        self.observer, self.observerWrapper = _makePlayer(self.store, u"Observer Player")
        locContainer.add(self.observer)
        self.otransport = StringTransport()
        self.observerWrapper.setProtocol(PlayerProtocol(self.otransport))

    def tearDown(self):
        for p in self.player, self.observer:
            try:
                p.destroy()
            except AttributeError:
                pass

    def _test(self, command, output, observed=()):
        # Deprecate this or something
        command = unicode(command, 'ascii')

        self.playerWrapper.parse(command)

        output.insert(0, "> " + command)

        results = []
        for xport, oput in ((self.transport, output),
                            (self.otransport, observed)):
            results.append([])
            gotLines = xport.value().splitlines()
            for i, (got, expected) in enumerate(map(None, gotLines, oput)):
                got = got or ''
                expected = expected or '$^'
                m = re.compile(expected.rstrip()).match(got.rstrip())
                if m is None:
                    s1 = pprint.pformat(gotLines)
                    s2 = pprint.pformat(oput)
                    raise unittest.FailTest(
                        "\n%s\ndid not match expected\n%s\n(Line %d)" % (s1, s2, i))
                results[-1].append(m)
            xport.clear()
        return results
