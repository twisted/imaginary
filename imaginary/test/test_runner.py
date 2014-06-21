"""
Test running an Imaginary world
"""

import os
import fcntl
import pty
import tty
import struct

from axiom.store import Store

from twisted.trial.unittest import TestCase
from twisted.test.proto_helpers import StringTransport
from twisted.conch.insults.insults import ServerProtocol

from imaginary.world import ImaginaryWorld
from imaginary.wiring.player import Player
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
