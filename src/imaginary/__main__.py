# -*- test-case-name: imaginary.test.test_runner -*-
"""
Run a single-player Imaginary world.
"""
from __future__ import unicode_literals

import fcntl
import termios
import struct
import tty
import sys
import os
import signal

from axiom.store import Store

from twisted.python.log import startLogging
from twisted.internet.stdio import StandardIO
from twisted.conch.insults.insults import ServerProtocol
from twisted.internet.task import react
from twisted.internet.defer import Deferred

from imaginary.wiring.player import Player
from imaginary.world import ImaginaryWorld
from imaginary.wiring.terminalui import TextServerBase
from imaginary.objects import Actor

def getTerminalSize(terminalFD):
    """
    Get the height and width of the terminal, in characters.

    @param terminalFD: The file descriptor of the terminal to inspect.
    @type terminalFD: L{int}
    """
    winsz = fcntl.ioctl(terminalFD, tty.TIOCGWINSZ, b'12345678')
    winSize = struct.unpack(
        b'4H', winsz
    )
    ws_row, ws_col, ws_xpixel, ws_ypixel = winSize
    return ws_row, ws_col



class ConsoleTextServer(TextServerBase, object):
    """
    A L{ConsoleTextServer} is a terminal-based view onto an Imaginary world,
    from the perspective of a given player.

    As it is designed for a console, it gets terminal size from its protocol,
    and stops the reactor when complete.

    @ivar player: The player which will be given life from the terminal's
        input.
    @type player: L{imaginary.wiring.Player}

    @ivar terminalFD: The file descriptor of the terminal from which to get the
        size of the player.
    @type terminalFD: L{int}

    @ivar done: A L{Deferred} firing when the connection is lost.
    @type done: L{Deferred}
    """
    state = b'COMMAND'

    def __init__(self, player, terminalFD):
        self.player = player
        self.terminalFD = terminalFD
        self.done = Deferred()


    def connectionMade(self):
        """
        The terminal interaction has started; size the displayed terminal
        according to the current size of C{self.terminalFD}.
        """
        super(ConsoleTextServer, self).connectionMade()
        self.player.setProtocol(self)
        height, width = getTerminalSize(self.terminalFD)
        self.terminalSize(width, height)


    def connectionLost(self, reason):
        """
        The connection is complete; fire L{self.done}.
        """
        self.done.callback(None)



def loadWorld(worldName, store):
    """
    Load an imaginary world from a file.

    The specified file should be a Python file defining a global callable named
    C{world}, taking an axiom L{Store} object and returning an
    L{ImaginaryWorld}.  This world (and its attendant L{Store}) should contain
    only a single L{Actor} instance, which will be used for the player
    character.

    @param worldName: The path name to a Python file containing a world.
    @type worldName: L{str}

    @param store: The axiom data store to read the world into.
    @type store: L{Store}
    """
    with open(worldName, "rb") as f:
        codeobj = compile(f.read(), worldName, "exec")
        namespace = {}
        eval(codeobj, namespace, namespace)
        return namespace['world'](store)



def findActorThing(store):
    """
    Discover the L{Thing} associated with the only L{Actor} in the given
    L{Store}.

    @param store: An axiom store to query.
    @type store: L{Store}

    @return: a L{Thing} belonging to an L{Actor}; the L{Actor}'s physical body.
    @rtype: L{Thing}
    """
    return store.findUnique(Actor).thing



def makeOrLoadWorld(reactor, worldName=None):
    store = Store()
    if worldName is None:
        world = ImaginaryWorld(store=store)
        world.create("player")
    else:
        world = loadWorld(worldName, store)
    return store



def makeTextServer(reactor, terminal_fd, player):
    """
    Make an ``ITerminalProtocol`` for running an Imaginary session.

    :param int terminal_fd: The file descriptor of the terminal the server is
        connected to.  This is used to determine the display size so elements
        can be fit to it.  It is not used for other input or output.

    :param Player player: The player operating the session.  This is used to
        interpret input.

    :return: An object providing ``ITerminalProtocol`` which can handle text
        input and generate text output to facilitate an Imaginary session.
    """
    tsb = ConsoleTextServer(player, terminal_fd)
    def winchAccess(signum, frame):
        reactor.callFromThread(
            tsb.terminalSize,
            *getTerminalSize(terminal_fd)[::-1]
        )
    signal.signal(signal.SIGWINCH, winchAccess)
    return tsb



def runTextServer(reactor, terminal_fd, *argv):
    """
    Run a text-based Imaginary session.

    :param terminal_fd: See ``makeTextServer``.

    :param *: Additional positional arguments to use to initialize the
        Imaginary world.
    """
    store = makeOrLoadWorld(reactor, *argv)
    actor = findActorThing(store)
    textServer = makeTextServer(reactor, terminal_fd, Player(actor))
    StandardIO(ServerProtocol(lambda: textServer))
    return textServer.done


CLEAR_SCREEN = b"\r\x1bc\r"

def withSavedTerminalSettings(fd, blockingCall):
    """
    Save and restore terminal settings for the given file descriptor.

    @param fd: The file descriptor, a PTY, to preserve terminal settings for.
    @type fd: L{int}

    @param blockingCall: A 0-argument callable that might modify C{fd}'s
        terminal settings.
    @type blockingCall: L{callable}

    @return: The result of L{blockingCall}.
    """
    oldSettings = termios.tcgetattr(fd)
    tty.setraw(fd)
    try:
        return blockingCall()
    finally:
        termios.tcsetattr(fd, termios.TCSANOW, oldSettings)
        os.write(fd, CLEAR_SCREEN)



def ifmain(thunk):
    """
    If the current module is being run as C{__main__}, then run the decorated
    function with C{sys.argv[1:]}.  Otherwise, return it.

    @param thunk: A function taking C{argv} to run if it's defined in
        C{__main__}.
    @type thunk: L{callable}
    """
    if __name__ == '__main__':
        thunk(sys.argv[1:])
    return thunk



@ifmain
def main(argv):
    """
    Start logging to a temporary file and then run the main loop.
    """
    startLogging(file('imaginary-debug.log', 'w'))
    terminal_fd = sys.__stdin__.fileno()
    withSavedTerminalSettings(
        terminal_fd,
        lambda: react(runTextServer, terminal_fd, argv),
    )
