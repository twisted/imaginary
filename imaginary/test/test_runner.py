"""
Test running an Imaginary world
"""

import os
import fcntl
import pty
import tty
import struct

from twisted.trial.unittest import TestCase
from imaginary.__main__ import getTerminalSize

class WindowSizing(TestCase):
    """
    Tests for getting the size of a terminal window.
    """

    def test_getTerminalSize(self):
        """
        Does getWindowSize get the size of a terminal window?
        """
        leader, follower = pty.openpty()
        self.addCleanup(os.close, leader)
        self.addCleanup(os.close, follower)
        structformat = '4H'
        ws_row, ws_col, ws_xpixel, ws_ypixel = 123, 456, 789, 912
        data = struct.pack(structformat, ws_row, ws_col, ws_xpixel, ws_ypixel)
        fcntl.ioctl(leader, tty.TIOCSWINSZ, data)
        self.assertEqual(getTerminalSize(follower), (ws_row, ws_col))

