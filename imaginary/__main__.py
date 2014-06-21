"""
Run a single-player Imaginary world.
"""
from __future__ import unicode_literals

import fcntl
import struct
import tty
import signal

from axiom.store import Store

from twisted.python.log import startLogging

from imaginary.wiring.player import Player
from imaginary.world import ImaginaryWorld
from imaginary.wiring.terminalui import TextServerBase
from twisted.conch.stdio import runWithProtocol

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

    def connectionMade(self):
        super(ConsoleTextServer, self).connectionMade()
        self.player.setProtocol(self)
        height, width = getTerminalSize(self.terminalFD)
        self.terminalSize(width, height)

    def connectionLost(self, reason):
        from twisted.internet import reactor
        reactor.stop()


def main():
    startLogging(file('imaginary-debug.log', 'w'))

    store = Store()
    world = ImaginaryWorld(store=store)
    actor = world.create("player")

    def makeTextServer():
        tsb = ConsoleTextServer(Player(actor), sys.stdout.fileno())
        from twisted.internet import reactor
        def winchAccess(signum, frame):
            reactor.callFromThread(tsb.terminalSize, *getTerminalSize()[::-1])
        signal.signal(signal.SIGWINCH, winchAccess)
        return tsb
    runWithProtocol(makeTextServer)

if __name__ == '__main__':
    main()
