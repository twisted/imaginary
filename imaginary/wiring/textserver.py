
import sys, string

from twisted.conch.insults import insults
from twisted.python import log, util
from twisted import copyright as tcopyright

from imaginary import copyright as pcopyright
from imaginary import eimaginary, resources
from imaginary.wiring import player

class TextServer(insults.TerminalProtocol):
    state = 'USERNAME'

    width = 80
    height = 24

    player = None
    logout = None

    motd = file(util.sibpath(resources.__file__, 'motd')).read() % {
        'pythonVersion': sys.version,
        'twistedVersion': tcopyright.version,
        'imaginaryVersion': pcopyright.version}

    def statefulDispatch(self, prefix, *a, **kw):
        oldState = self.state
        newState = getattr(self, prefix + oldState)(*a, **kw)
        if newState is not None:
            if self.state == oldState:
                self.state = newState
            else:
                log.msg("Warning: state changed and new state returned")

    # ITerminalProtocol
    def terminalSize(self, width, height):
        self.width = width
        self.height = height

        print 'now', self.width, self.height

        if self.state == 'COMMAND':
            self._prepareDisplay()

    def connectionMade(self):
        self.write(self.motd + '\n')
        self.write('Username: ')
        self.lineBuffer = []
        self.commandHistory = ['']
        self.historyPosition = None

    def _prepareDisplay(self):
        self.terminal.reset()
        self.terminal.eraseDisplay()
        self.terminal.setScrollRegion(1, self.height - 2)
        self.terminal.cursorPosition(0, self.height - 2)
        self.terminal.write('-' * (self.width - 1))
        self.terminal.cursorPosition(0, 0)
        self._clearInput()

    def _echoInput(self, ch):
        if self.state == 'COMMAND':
            self.terminal.saveCursor()
            self.terminal.cursorPosition(len(self.lineBuffer), self.height - 1)
            self.terminal.write(ch)
            self.terminal.restoreCursor()
        else:
            self.terminal.write(ch)

    def _eraseOneInputCharacter(self):
        if self.state == 'COMMAND':
            self.terminal.saveCursor()
            self.terminal.cursorPosition(len(self.lineBuffer), self.height - 1)
            self.terminal.write(' ')
            self.terminal.restoreCursor()
        else:
            self.terminal.write('\b \b')

    def _clearInput(self):
        if self.state == 'COMMAND':
            self.terminal.saveCursor()
            self.terminal.cursorPosition(0, self.height - 1)
            self.terminal.eraseLine()
            self.terminal.restoreCursor()
        else:
            self.write('\n')

    def keystrokeReceived(self, keyID, modifier):
        if keyID == '\r' or keyID == '\n':
            self._clearInput()
            line = ''.join(self.lineBuffer)
            self.lineBuffer = []
            self.lineReceived(line)
        elif keyID == self.terminal.BACKSPACE or keyID == '\b':
            if self.lineBuffer:
                self.lineBuffer.pop()
                if self._echo:
                    self._eraseOneInputCharacter()
        elif keyID in list(string.printable):
            if self._echo:
                self._echoInput(keyID)
            self.lineBuffer.append(keyID)
        else:
            print 'Wacky unhandled stuff:', repr(keyID), modifier

    def connectionLost(self, reason):
        insults.TerminalProtocol.connectionLost(self, reason)
        if self.player is not None:
            self.player.disconnect()
            self.player = None
        if self.logout is not None:
            self.logout()
            self.logout = None


    # Other stuff
    _echo = True
    def echoOn(self):
        self._echo = True

    def echoOff(self):
        self._echo = False

    def write(self, bytes):
        self.terminal.write(bytes)

    def lineReceived(self, line):
        self.statefulDispatch('line_', unicode(line, 'ascii'))

    def line_IGNORE(self, line):
        self.write("Your input %r was ignored.\n" % (line,))

    def line_USERNAME(self, username):
        self.username = username
        self.echoOff()
        self.write('Password: ')
        return 'PASSWORD'

    def line_PASSWORD(self, password):
        username = self.username
        del self.username
        self.echoOn()
        self.write('\n')
        self.factory.login(username, password
            ).addCallback(self._cbLogin
            ).addErrback(self._ebBadPassword
            ).addErrback(self._ebNoSuchUser, username
            ).addErrback(log.err
            )
        return 'IGNORE'

    def _cbLogin(self, (iface, avatar, logout)):
        self.player = player.Player(avatar.thing)
        self.logout = logout
        self.player.setProtocol(self)
        self.state = 'COMMAND'

        self._prepareDisplay()

    def _ebBadPassword(self, failure):
        failure.trap(eimaginary.BadPassword)
        self.write('Bad password\nUsername: ')
        self.state = 'USERNAME'

    def _ebNoSuchUser(self, failure, username):
        failure.trap(eimaginary.NoSuchUser)
        self.username = username
        self.write("No such user.  Create? ")
        self.state = 'MAYBE_CREATE'

    def line_MAYBE_CREATE(self, line):
        if line.lower() in ('y', 'yes'):
            self.echoOff()
            self.write('Enter a new password: ')
            return 'NEW_PASSWORD'
        else:
            self.write('Username: ')
            return 'USERNAME'

    def line_NEW_PASSWORD(self, password):
        username = self.username
        del self.username
        self.echoOn()
        actor = self.factory.create(username, password)
        self.player = player.Player(actor)
        self.factory.loggedIn(actor)
        self.player.setProtocol(self)
        self._prepareDisplay()
        return 'COMMAND'

    def line_COMMAND(self, line):
        if line.strip().lower() == 'quit':
            self.player.lowLevelSend("Bye!")
            self.player.disconnect()
        else:
            self.player.parse(line)
            self.commandHistory.append(line)
