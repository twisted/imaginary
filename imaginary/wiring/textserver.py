# -*- test-case-name: imaginary.test.test_text -*-

import sys, unicodedata

from zope.interface import implements

from twisted.cred.portal import IRealm
from twisted.conch.insults import insults
from twisted.python import log, util
from twisted import copyright as tcopyright

from axiom.item import Item
from axiom.dependency import dependsOn

from xmantissa.ixmantissa import ITerminalServerFactory
from xmantissa.terminal import ShellAccount
from xmantissa.sharing import asAccessibleTo, itemFromProxy

from imaginary import copyright as pcopyright
from imaginary import resources
from imaginary.objects import Thing
from imaginary.world import ImaginaryWorld
from imaginary.wiring.player import Player


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



class CharacterSelectionTextServer(TextServerBase):
    """
    L{CharacterSelectionTextServer} presents a simple text menu for selecting
    or creating a character and then enters the selected or created character
    into an Imaginary simulation.

    @ivar motd: Some text which will be displayed at connection setup time.

    @ivar role: The L{Role} which will own any new characters created.

    @ivar world: The L{ImaginaryWorld} which the selected character will be
        entered into.

    @ivar choices: A list of L{Thing}s which represent existing characters
        which may be selected.
    """

    motd = file(util.sibpath(resources.__file__, 'motd')).read() % {
        'pythonVersion': sys.version,
        'twistedVersion': tcopyright.version,
        'imaginaryVersion': pcopyright.version}

    state = 'SELECT'

    def __init__(self, role, world, choices):
        self.role = role
        self.world = world
        self.choices = choices


    def connectionMade(self):
        TextServerBase.connectionMade(self)
        self.terminal.reset()
        self.write(self.motd)
        self.write('Choose a character: \n')
        self.write('  0) Create\n')
        for n, actor in enumerate(self.choices):
            self.write('  %d) %s\n' % (n + 1, actor.name.encode('utf-8')))
        self.write('> ')


    def line_SELECT(self, line):
        which = int(line)
        if which == 0:
            self.write('Name? ')
            return 'USERNAME'
        else:
            return self.play(self.choices[which - 1])


    def play(self, character):
        self.player = Player(character)
        self.player.setProtocol(self)
        self.world.loggedIn(character)
        self._prepareDisplay()
        return 'COMMAND'


    def line_USERNAME(self, line):
        """
        Handle a username supplied in response to a prompt for one when
        creating a new character.

        This will create a user with the name given by C{line}, made available
        to the role indicated by C{self.role}, and entered into play.
        """
        actor = self.world.create(line)
        self.role.shareItem(actor)
        return self.play(actor)



class ImaginaryApp(Item):
    """
    A terminal application which presents an Imaginary game session.
    """
    powerupInterfaces = (ITerminalServerFactory,)
    implements(*powerupInterfaces)

    shell = dependsOn(ShellAccount)

    name = 'imaginary'

    def _charactersForViewer(self, store, role):
        """
        Find the characters the given role is allowed to play.

        This will load any L{Thing}s from C{store} which are shared to C{role}.
        It then unwraps them from their sharing wrapper and returns them (XXX
        there should really be a way for this to work without the unwrapping,
        no?  See #2909. -exarkun).
        """
        characters = []
        things = store.query(Thing)
        actors = asAccessibleTo(role, things)
        characters.extend(map(itemFromProxy, actors))
        return characters


    def buildTerminalProtocol(self, viewer):
        """
        Create and return a L{TextServer} using a L{Player} owned by the store
        this item is in.

        This implementation is certainly wrong.  It probably reflects some
        current limitations of Mantissa.  Primarily, the limitation is
        interaction between different stores, in this case a user store and an
        application store.
        """
        # XXX Get the Imaginary app store.  Eventually this should just be
        # self.store.  See #2908.
        imaginary = IRealm(self.store.parent).accountByAddress(u'Imaginary', None).avatars.open()

        role = viewer.roleIn(imaginary)
        characters = self._charactersForViewer(imaginary, role)

        world = imaginary.findUnique(ImaginaryWorld)
        return CharacterSelectionTextServer(role, world, characters)
