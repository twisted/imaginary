# -*- test-case-name: pottery.test -*-
import pprint
import re

from twisted.trial import unittest
from twisted.test.proto_helpers import StringTransport

from pottery import objects, wiring


class CommandTestCaseMixin:
    def setUp(self):
        self.location = objects.Room("Test Location",
                                     "Location for testing.")

        self.player = objects.Player("Test Player")
        self.player.useColors = False
        self.location.add(self.player)
        self.transport = StringTransport()
        class Protocol:
            write = self.transport.write
        self.player.setProtocol(Protocol())

        self.observer = objects.Player("Observer Player")
        self.location.add(self.observer)
        self.otransport = StringTransport()
        class Protocol:
            write = self.otransport.write
        self.observer.setProtocol(Protocol())


    def tearDown(self):
        for p in self.player, self.observer:
            try:
                p.destroy()
            except AttributeError:
                pass

    def _test(self, command, output, observed=()):
        wiring.parse(self.transport, self.player, command)

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
