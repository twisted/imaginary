# -*- test-case-name: imaginary.test.test_text -*-

from twisted.conch.insults import insults
from twisted.python import log

import unicodedata

_widths = {'W': 2, 'N': 1, 'F': 2, 'H': 1, 'Na': 1, 'A': 1}
def width(ch):
    """
    Compute the display width of the given character.

    Useful for cursor-repositioning tasks, however this is not entirely
    reliable since different terminal emulators have different behavior in
    this area.

    @see: U{http://unicode.org/reports/tr11/}

    @return: The width in 1/2 ems of the given single-length unicode string.
    @rtype: C{int}
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



class TextServerBase(insults.TerminalProtocol):
    """
    L{TextServerBase} presents a simple two-region interface for controlling a
    character.  The majority of the screen is used to present output and one
    line at the bottom of the screen is used to collect input.

    @ivar state: The input handling state this L{CharacterSelectionTextServer}
        is in currently.  See the C{line_}-prefixed methods.

    @ivar width: The width in columns of the client.
    @type width: L{int}
    @ivar height: The height in rows of the client.
    @type height: L{int}

    @ivar player: C{None} until a character actually enters play using this
        connection, then a L{Player} wrapped around that character.
    """
    state = 'IGNORE'

    width = 80
    height = 24

    player = None

    def connectionMade(self):
        self.decoder = AsynchronousIncrementalUTF8Decoder()
        self.commandHistory = ['']
        self.historyPosition = None


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

        if self.state == 'COMMAND':
            self._prepareDisplay()


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
                self._eraseOneInputCharacter(width(ch))
        elif isinstance(keyID, str) and keyID >= ' ':
            self._echoInput(keyID)
            self.decoder.add(keyID)


    def connectionLost(self, reason):
        insults.TerminalProtocol.connectionLost(self, reason)
        if self.player is not None:
            self.player.disconnect()
            self.player = None


    # Other stuff
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


    def line_COMMAND(self, line):
        if line.strip().lower() == 'quit':
            self.player.disconnect()
        else:
            self.player.parse(line)
            self.commandHistory.append(line)



