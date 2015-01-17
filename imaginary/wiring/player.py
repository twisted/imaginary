# -*- test-case-name: imaginary.test.test_player -*-

from zope.interface import implements

from twisted.internet import defer
from twisted.python import log

from imaginary import iimaginary, eimaginary, text as T

from imaginary.text import flatten
from imaginary.action import Action


class Player(object):
    """
    UI integration layer for Actors to protocols.
    """
    implements(iimaginary.IEventObserver)

    proto = None

    useColors = True

    def __init__(self, actor):
        self.actor = actor
        self.player = iimaginary.IActor(actor)
        self.player.setEphemeralIntelligence(self)


    def setProtocol(self, proto):
        if self.proto is not None:
            self.send("Your body has been usurped!\n")
            self.disconnect()
        self.proto = proto
        self.termAttrs = T.AttributeSet()


    def parse(self, line):
        def cbParse(result):
            pass

        def ebParse(err):
            err.trap(eimaginary.NoSuchCommand)
            self.proto.write('Bad command or filename\r\n')

        def ebAmbiguity(err):
            err.trap(eimaginary.AmbiguousArgument)
            exc = err.value
            msg = "Could you be more specific?  When you said '" + exc.partValue + "', did you mean: "
            def format(potentialTarget):
                concept = iimaginary.IConcept(potentialTarget)
                vt102 = concept.vt102(self.player)
                flattened = list(flatten(vt102, useColors=False))
                return "".join(flattened)
            for obj in exc.objects[:-1]:
                msg += format(obj)
                msg += ", "
            msg += "or "
            msg += format(exc.objects[-1])
            msg += "?"
            self.send((msg, "\r\n"))

        def ebUnexpected(err):
            log.err(err)
            self.proto.write('\r\nerror\r\n')

        self.send(('> ', line, '\n'))
        d = defer.maybeDeferred(Action.parse, self.actor, line)
        d.addCallbacks(cbParse, ebParse)
        d.addErrback(ebAmbiguity)
        d.addErrback(ebUnexpected)
        return d


    def disconnect(self):
        if self.proto and self.proto.terminal:
            self.proto.player = None
            self.proto.terminal.loseConnection()
        if self.player.getIntelligence() is self:
            self.player.setEphemeralIntelligence(None)


    def prepare(self, concept):
        """
        Implement L{iimaginary.IEventObserver.prepare} to format an L{IConcept}
        into a VT102-format byte string, capturing whatever encapsulated world
        state as it exists right now.

        @return: a 0-argument callable that will actually send the
            VT102-formatted string to this L{Player}'s protocol, if it still
            has one when it is called.
        """
        stuff = concept.vt102(self.actor)
        def send():
            if self.proto is not None:
                self.send(stuff)
        return send


    def send(self, stuff):
        """
        Write a flattenable structure to my transport/protocol thingy.
        """
        #FIXME: Encoding should be done *inside* flatten, not here.
        flatterStuff = T.flatten(stuff, useColors=self.useColors,
                                 currentAttrs=self.termAttrs)
        txt = u''.join(list(flatterStuff))
        bytes = txt.encode('utf-8')
        self.proto.write(bytes)
