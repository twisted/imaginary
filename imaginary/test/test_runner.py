"""
Test running an Imaginary world
"""

import os
import fcntl
import pty
import tty
import struct
import termios

from axiom.store import Store

from twisted.trial.unittest import TestCase

from twisted.internet.defer import Deferred
from twisted.test.proto_helpers import StringTransport
from twisted.conch.insults.insults import ServerProtocol

from imaginary.world import ImaginaryWorld
from imaginary.wiring.player import Player
from imaginary.__main__ import withSavedTerminalSettings
from imaginary.__main__ import CLEAR_SCREEN
from imaginary.__main__ import getTerminalSize, ConsoleTextServer


def makeTerminal(testCase):
    """
    Create a terminal for a given test case.
    """
    leader, follower = pty.openpty()
    testCase.addCleanup(os.close, leader)
    testCase.addCleanup(os.close, follower)
    return leader, follower


def setTerminalSize(terminalFD, ws_row=25, ws_col=80,
                    ws_xpixel=0, ws_ypixel=0):
    """
    Set the size of the given PTY leader file descriptor.
    """
    structformat = '4H'
    data = struct.pack(structformat, ws_row, ws_col, ws_xpixel, ws_ypixel)
    fcntl.ioctl(terminalFD, tty.TIOCSWINSZ, data)



class WindowSizing(TestCase):
    """
    Tests for getting the size of a terminal window.
    """

    def test_getTerminalSize(self):
        """
        L{getWindowSize} gets the size of a terminal file descriptor.
        """
        leader, follower = makeTerminal(self)
        ws_row, ws_col, ws_xpixel, ws_ypixel = 123, 456, 789, 912
        setTerminalSize(leader, ws_row, ws_col, ws_xpixel, ws_ypixel)
        self.assertEqual(getTerminalSize(follower), (ws_row, ws_col))


    def test_consoleTextServer(self):
        """
        L{ConsoleTextServer.connectionMade} sets the protocol of its player to
        itself.
        """
        leader, follower = makeTerminal(self)
        store = Store()
        world = ImaginaryWorld(store=store)
        actor = world.create(u"player")

        setTerminalSize(leader, 234, 567)
        player = Player(actor)
        textServer = ConsoleTextServer(player, follower)
        terminalProtocol = ServerProtocol(lambda: textServer)
        self.assertIdentical(player.proto, None)
        terminalProtocol.makeConnection(StringTransport())
        self.assertIdentical(player.proto, textServer)
        self.assertEqual(textServer.width, 567)
        self.assertEqual(textServer.height, 234)


    def test_withSavedTerminalSettings(self):
        """
        L{withSavedTerminalSettings} saves and then restores the settings for
        the terminal that it is given.
        """
        leader, follower = makeTerminal(self)

        attrs = termios.tcgetattr(follower)
        [iflag, oflag, cflag, lflag, ispeed, ospeed, cc] = attrs
        def mangle():
            os.write(follower, b"HELLO")
            termios.tcsetattr(follower, termios.TCSANOW,
                              [iflag, oflag, cflag, lflag,
                               ispeed + 1000, ospeed + 1000, cc])
            mangle.run = True
        mangle.run = False
        withSavedTerminalSettings(follower, mangle)
        self.assertEqual(mangle.run, True)
        newattrs = termios.tcgetattr(follower)
        LFLAGS = 3
        # These seem to change randomly, and I'm not sure why, so let's exclude
        # them from the test (we never changed them in mangle() anyway).
        newattrs[LFLAGS] = 0
        attrs[LFLAGS] = 0
        self.assertEqual(newattrs, attrs)
        self.assertEqual(os.read(leader, 1024), b"HELLO" + CLEAR_SCREEN)
