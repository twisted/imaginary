# -*- test-case-name: reality.test_reality -*-
from twisted.protocols import telnet
from twisted.internet.protocol import ServerFactory
from twisted.internet import defer

from reality.text.common import INoun, IThinker, express, IDescribeable
from reality.things import EventReceiver, IEventReceiver, IMoveListener, Refusal
from reality import errors

import traceback

DEBUG = 0
WONTECHO = ''.join((telnet.IAC, telnet.WONT, telnet.ECHO))
WILLECHO = ''.join((telnet.IAC, telnet.WILL, telnet.ECHO))

class TextServer(telnet.Telnet):
    mode = "Command"
    __implements__ = IEventReceiver, IMoveListener

    avatar = None

    def connectMessage(self):
        """A message welcoming you to the server.
        
        This should return a string which will be displayed to every user
        when they initially connect.
        """
        return ""

    def welcomeMessage(self):
        """A message welcoming you back into the game.
        
        This should return a string which will be displayed after a user
        has successfully logged on.
        """
        return ''.join((
            WONTECHO,
            "\r\nTR: connected to ",
            INoun(self.avatar).name,
            '\r\n'
        ))

    def telnet_Command(self, cmd):
        try:
            r = IThinker(self.avatar).parse(cmd)
        except Refusal, ref:
            print "refusal!"
            self.write(express(ref.whyNot, self.avatar) + '\r\n')
        except errors.RealityException, re:
            print "RealityException!"
            traceback.print_exc()
            self.write(express(re, self.avatar) + '\r\n')
        else:
            if r is not None:
                print r
        self.write(self.commandPrompt())
        return 'Command'

    def connectionMade(self):
        self.write(self.connectMessage())
        if self.avatar:
            self.loginSequence()

    def loginSequence(self):
        self.write(self.welcomeMessage())
        IThinker(self.avatar).parse("look")
        self.write(self.commandPrompt())

    def setAvatar(self, a):
        self.avatar = a
        a.setComponent(IEventReceiver, self)
        a.setComponent(IMoveListener, self)

    def commandPrompt(self):
        return express(self.avatar, self.avatar) + ': '

    def eventReceived(self, emitter, evt):
        if DEBUG:
            self.write('[' + str(emitter) + '] ')
        self.write("\r\n" + express(evt, self.avatar) + "\r\n")

    def thingArrived(self, emitter, event):
        pass

    def thingLeft(self, emitter, event):
        pass

    def thingMoved(self, emitter, event):
        if emitter is self.avatar:
            IThinker(self.avatar).parse("look")

class TextFactory(ServerFactory):
    protocol = TextServer

    def __init__(self, person):
        self.person = person

    def buildProtocol(self, addr):
        p = ServerFactory.buildProtocol(self, addr)
        p.setAvatar(self.person)
        return p
