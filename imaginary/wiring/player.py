import itertools

from twisted.internet import defer
from twisted.python import log

from imaginary import iimaginary, eimaginary, text as T, commands


class Player(object):
    """UI integration layer for Actors to protocols.
    """
    proto = None
    realm = None

    useColors = True

    def __init__(self, actor):
        self.actor = actor
        self.player = iimaginary.IActor(actor)
        self.player.intelligence = self


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
            if len(exc.objects) == 0:
                func = getattr(err.value.action, err.value.part + "NotAvailable", None)
                if func:
                    msg = func(self.actor, exc)
                else:
                    msg = "Who's that?"
            else:
                msg = "Could you be more specific?"
            self.lowLevelSend((msg, "\r\n"))

        def ebUnexpected(err):
            log.err(err)
            self.proto.write('\r\nerror\r\n')

        self.lowLevelSend(('> ', line, '\n'))
        d = defer.maybeDeferred(commands.Command.parse, self.actor, line)
        d.addCallbacks(cbParse, ebParse)
        d.addErrback(ebAmbiguity)
        d.addErrback(ebUnexpected)
        return d


    def disconnect(self):
        if self.proto and self.proto.terminal:
            self.proto.player = None
            self.proto.terminal.loseConnection()
        if self.player.intelligence is self:
            self.player.intelligence = None


    def send(self, event):
        if self.proto is not None:
            self.lowLevelSend(event.vt102(self.actor))


    def lowLevelSend(self, stuff):
        #FIXME: Encoding should be done *inside* flatten, not here.
        flatterStuff = T.flatten(stuff, useColors=self.useColors, currentAttrs=self.termAttrs)
        txt = u''.join(list(flatterStuff))
        bytes = txt.encode('utf-8')
        self.proto.write(bytes)


    def destroy(self):
        super(Player, self).destroy()
        self.realm.destroy(self)
        self.disconnect()
