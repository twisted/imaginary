# -*- test-case-name: imaginary.test.test_text -*-


import sys, string, unicodedata

from twisted.conch.insults import insults
from twisted.python import log, util
from twisted import copyright as tcopyright

from imaginary import copyright as pcopyright
from imaginary import eimaginary, resources
from imaginary.wiring import player


_widths = {'W': 2, 'Na': 1}
def width(ch):
    """
    Return the width in EMs of the given single-length unicode string.

    XXX TODO: Currently only supports Narrow and Wide (ie, no support for
    half-width, full-width, neutral, or ambiguous).
    """
    widthSpecifier = unicodedata.east_asian_width(ch)
    try:
        return _widths[widthSpecifier]
    except KeyError:
        raise KeyError("%r has a width that is not supported: %s" 
                       % (ch, widthSpecifier))


class AsynchronousIncrementalUTF8Decoder(object):
    """
    An incremental UTF-8 decoder which can have bytes pushed onto it
    and unicode pulled out of it. This is especially useful for
    asynchronous network connectinos where a peer may be receiving
    bytes individually and wants to process them as unicode as they
    come in.

    Specifically, it is better than L{encodings.utf_8.StreamReader}
    since it doesn't block while waiting for the completion of a
    character.
    """
    def __init__(self):
        self._buf = []


    def add(self, byte):
        """
        Push a byte onto the unicode string; if the byte contains or
        completes a full utf-8-encoded character, that new character
        will be included in the result of L{get}.
        """
        try:
            character = byte.decode('utf-8')
        except UnicodeDecodeError:
            if self._buf and isinstance(self._buf[-1], str):
                try:
                    character = (self._buf[-1] + byte).decode('utf-8')
                except UnicodeDecodeError:
                    self._buf[-1] = self._buf[-1] + byte
                else:
                    self._buf[-1] = character
            else:
                self._buf.append(byte)
        else:
            self._buf.append(character)


    def get(self):
        """
        Return the accumulated unicode string; If there are presently
        any trailing bytes that don't make up a full character, they
        will not affect the result.
        """
        if self._buf and isinstance(self._buf[-1], str):
            buf = self._buf[:-1]
        else:
            buf = self._buf
        return u''.join(buf)


    def reset(self):
        """
        Clear the current data.
        """
        self._buf = []


    def width(self):
        """
        Return the width in EMs of the current buffer.

        XXX TODO: Currently only supports Narrow and Wide (ie, no support for
        half-width, full-width, neutral, or ambiguous).
        """
        return sum(width(ch)
                   for ch in self._buf
                   if not isinstance(ch, str))


    def pop(self):
        """
        Pop and return the last unicode character off of the current string.

        @raises ValueError: If there is an incomplete character
        waiting to be finished with more bytes.
        @raises IndexError: If there was no data added yet.
        """
        if isinstance(self._buf[-1], str):
            raise ValueError
        return self._buf.pop()



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
        self.decoder = AsynchronousIncrementalUTF8Decoder()
        self.write(self.motd + '\n')
        self.write('Username: ')
        self.commandHistory = ['']
        self.historyPosition = None


    def _prepareDisplay(self):
        self.terminal.reset()
        self.terminal.eraseDisplay()
        self.terminal.setScrollRegion(1, self.height - 2)
        self.terminal.cursorPosition(0, self.height - 2)
        self.terminal.write('-' * (self.width - 1))
        self._positionCursorForInput()


    def _positionCursorForInput(self):
        self.terminal.cursorPosition(self.decoder.width(), self.height - 1)


    def _positionCursorForOutput(self):
        self.terminal.cursorPosition(0, self.height - 3)


    def _echoInput(self, ch):
        self.terminal.write(ch)


    def _eraseOneInputCharacter(self, width):
        self.terminal.write('\b' * width + ' ' * width + '\b' * width)


    def _clearInput(self):
        self.terminal.eraseLine()
        self._positionCursorForOutput()


    def keystrokeReceived(self, keyID, modifier):
        if keyID == '\r' or keyID == '\n':
            line = self.decoder.get()
            self.decoder.reset()
            if self.state == 'COMMAND':
                self._clearInput()
            else:
                self.terminal.nextLine()
            self.lineReceived(line)
        elif keyID == self.terminal.BACKSPACE or keyID == '\b':
            if self.decoder.width():
                ch = self.decoder.pop()
                if self._echo:
                    self._eraseOneInputCharacter(width(ch))
        elif isinstance(keyID, str) and keyID >= ' ':
            if self._echo:
                self._echoInput(keyID)
            self.decoder.add(keyID)


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
        if self.state == 'COMMAND':
            self._positionCursorForOutput()
        self.terminal.write(bytes)
        if self.state == 'COMMAND':
            self._positionCursorForInput()


    def lineReceived(self, line):
        self.statefulDispatch('line_', line)


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
            self.player.disconnect()
        else:
            self.player.parse(line)
            self.commandHistory.append(line)
