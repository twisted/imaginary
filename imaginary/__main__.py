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

def getTerminalSize(terminalFD):
    """
    Get the height and width of the terminal, in characters.
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
    """
    state = b'COMMAND'

    def __init__(self, player, terminalFD):
        self.player = player
        self.terminalFD = terminalFD
        self.done = Deferred()

    def connectionMade(self):
        super(ConsoleTextServer, self).connectionMade()
        self.player.setProtocol(self)
        height, width = getTerminalSize(self.terminalFD)
        self.terminalSize(width, height)

    def connectionLost(self, reason):
        self.done.callback(None)



def makeTextServer(reactor):
    store = Store()
    world = ImaginaryWorld(store=store)
    actor = world.create("player")

    tsb = ConsoleTextServer(Player(actor), sys.__stdin__.fileno())
    def winchAccess(signum, frame):
        reactor.callFromThread(tsb.terminalSize, *getTerminalSize()[::-1])
    signal.signal(signal.SIGWINCH, winchAccess)
    return tsb



def runTextServer(reactor):
    """
    Run a L{ConsoleTextServer}.
    """
    textServer = makeTextServer(reactor)
    StandardIO(ServerProtocol(lambda: textServer))
    return textServer.done


CLEAR_SCREEN = b"\r\x1bc\r"

def withSavedTerminalSettings(fd, blockingCall):
    """
    Save and restore terminal settings for the given file descriptor.
    """
    oldSettings = termios.tcgetattr(fd)
    tty.setraw(fd)
    try:
        blockingCall()
    finally:
        termios.tcsetattr(fd, termios.TCSANOW, oldSettings)
        os.write(fd, CLEAR_SCREEN)



def ifmain(thunk):
    if __name__ == '__main__':
        thunk(sys.argv[1:])
    return thunk



@ifmain
def main(argv):
    startLogging(file('imaginary-debug.log', 'w'))
    withSavedTerminalSettings(sys.__stdin__.fileno(),
                              lambda: react(runTextServer, argv))

