# -*- test-case-name: imaginary.test -*-
import pprint
import re

from twisted.trial import unittest
from twisted.test.proto_helpers import StringTransport

from axiom import store

from imaginary import iimaginary, objects, text, language
from imaginary.wiring import player, realm

E = re.escape

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
            description=u"Location for testing.",
            proper=True)

        locContainer = objects.Container(store=self.store, capacity=1000)
        locContainer.installOn(self.location)

        self.realm = realm.ImaginaryRealm(store=self.store)
        self.player = self.realm.create(u"Test Player", u"password", gender=language.Gender.FEMALE)
        self.playerContainer = iimaginary.IContainer(self.player)
        self.playerWrapper = player.Player(self.player)

        self.playerWrapper.useColors = False
        locContainer.add(self.player)
        self.transport = StringTransport()
        self.playerWrapper.setProtocol(PlayerProtocol(self.transport))

        self.observer = self.realm.create(u"Observer Player", u"password", gender=language.Gender.FEMALE)
        self.observerWrapper = player.Player(self.observer)
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
                m = re.compile(expected.rstrip() + '$').match(got.rstrip())
                if m is None:
                    s1 = pprint.pformat(gotLines)
                    s2 = pprint.pformat(oput)
                    raise unittest.FailTest(
                        "\n%s\ndid not match expected\n%s\n(Line %d)" % (s1, s2, i))
                results[-1].append(m)
            xport.clear()
        return results


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
