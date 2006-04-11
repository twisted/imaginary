import itertools

from twisted.internet import defer
from twisted.python import log

from pottery import ipottery, epottery, text as T, commands


class Player(object):
    """UI integration layer for Actors to protocols.
    """
    proto = None
    realm = None

    useColors = True

    def __init__(self, actor):
        self.actor = actor
        self.player = ipottery.IActor(actor)
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
            err.trap(epottery.NoSuchCommand)
            self.proto.write('Bad command or filename\r\n')

        def ebAmbiguity(err):
            err.trap(epottery.AmbiguousArgument)
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


    def format(self, *args):
        L = []
        it = T.flatten(args, currentAttrs=self.termAttrs)
        while True:
            try:
                obj = it.next()
            except StopIteration:
                break
            else:
                if ipottery.IDescribeable.providedBy(obj):
                    it = itertools.chain(
                        T.flatten(obj.formatTo(self),
                                  currentAttrs=self.termAttrs), it)
                else:
                    if self.useColors:
                        L.append(str(obj))
                    else:
                        if (hasattr(obj, 'startswith')
                            and hasattr(obj, 'endswith')
                            and obj.startswith('\x1b[')
                            and obj.endswith('m')):
                            continue
                        L.append(str(obj))

        return ''.join(L)


    def send(self, event):
        if self.proto is not None:
            self.lowLevelSend(event.formatTo(self.actor))


    def lowLevelSend(self, stuff):
        bytes = self.format(stuff)
        self.proto.write(bytes)


    def destroy(self):
        super(Player, self).destroy()
        self.realm.destroy(self)
        self.disconnect()
