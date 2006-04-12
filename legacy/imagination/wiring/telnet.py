# -*- test-case-name: imagination.test.test_wiring -*-

from twisted.protocols import telnet
from twisted.internet import protocol
from twisted.internet import defer
from twisted.internet import reactor
from twisted.python import log
from twisted.cred import credentials
from twisted.cred import checkers
from twisted.cred.error import UnauthorizedLogin
from twisted.python import components

from imagination.text import english
from imagination import simulacrum, errors, iimagination, containment

DEBUG = 0
WONTECHO = ''.join((telnet.IAC, telnet.WONT, telnet.ECHO))
WILLECHO = ''.join((telnet.IAC, telnet.WILL, telnet.ECHO))

class NoSelection(Exception):
    pass

class ImaginationTextServer(telnet.Telnet):
    mode = "Username"

    __implements__ = iimagination.IUI,

    needsPrompt = True

    def send(self, text):
        self.write(text)

    def block(self, deferred):
        self.mode = "Blocked"
        deferred.addBoth(self._unblock)
        return deferred

    def _unblock(self, resultOrFailure):
        self.mode = None
        return resultOrFailure

    def telnet_Blocked(self, line):
        self.send("Please wait...\r\n")

    def connectMessage(self):
        """A message welcoming you to the server.

        This should return a string which will be displayed to every user
        when they initially connect.
        """
        return ""

    def connectionMade(self):
        self.send(self.connectMessage())
        self.send("Username: ")

    def telnet_Username(self, username):
        self.avatar = self.factory.actorTemplate[
            iimagination.IUI: lambda x: self].fill(
            english.INoun, name=username).new()
        self.userLoggedIn()
        return "Command"

    def welcomeMessage(self):
        return ''.join((
            "\r\nTR: connected to ",
            english.INoun(self.avatar).name,
            '\r\n'
        ))

    def userLoggedIn(self):
        self.send(self.welcomeMessage())
        self.telnet_Command("look")

    def telnet_Command(self, cmd):
        self.needsPrompt = True
        d = defer.maybeDeferred(english.IThinker(self.avatar).parse, cmd)
        d.addErrback(self._ebParsed)
        d.addCallback(self._cbParsed)

    def _ebParsed(self, failure):
        if failure.check(errors.RealityException):
            self.send(english.express(failure.value, self.avatar) + '\r\n')
        else:
            self.send("Internal parse error: %s\r\n" % (failure.value,))
            return failure

    def _cbParsed(self, result):
        self.send(self.commandPrompt())
        self.needsPrompt = False

    def commandPrompt(self):
        return english.express(self.avatar, self.avatar) + '> '

    # IUI implementation
    def presentEvent(self, eventInterface, event):
        s = english.express(event, self.avatar) + "\r\n"
        if not self.needsPrompt:
            s = "\r\n" + s
        self.send(s)

    choiceDeferred = choiceItems = None

    def presentMenu(self, items, typename=None):
        if self.choiceDeferred is not None:
            self.choiceDeferred.errback(NoSelection())
        self.choiceDeferred = None

        lines = []
        if typename is not None:
            lines.append("Which %s do you mean?" % (typename,))
        for i in items:
            lines.append("%d. %s" % (len(lines), english.express(i, self.avatar)))
        lines.append('Choose: ')
        self.send('\r\n'.join(lines))
        self.mode = "Choosing"
        self.choiceDeferred = defer.Deferred().addErrback(self._ebChoice)
        self.choiceItems = items
        return self.choiceDeferred

    def _ebChoice(self, failure):
        if not failure.check(NoSelection):
            self.send("Internal menu error: %s\r\n" % (failure.value,))
        return failure

    def telnet_Choosing(self, text):
        try:
            val = int(text)
        except ValueError:
            self.mode = "Command"
            return self.telnet_Command(text)
        else:
            if val < 1 or val > len(self.choiceItems):
                self.send("Try again: ")
            else:
                self.mode = "Command"
                d, self.choiceDeferred = self.choiceDeferred, None
                d.callback(val - 1)


class TextFactory(protocol.ServerFactory):
    def __init__(self, actorTemplate):
        self.actorTemplate = actorTemplate

    protocol = ImaginationTextServer
