
from twisted.trial import unittest

from imaginary import iterutils


class UtilTestCase(unittest.TestCase):
    def testInterlace(self):
        self.assertEquals(
            list(iterutils.interlace('x', ())),
            [])

        self.assertEquals(
            list(iterutils.interlace('x', [1])),
            [1])

        self.assertEquals(
            list(iterutils.interlace('x', [1, 2])),
            [1, 'x', 2])

        self.assertEquals(
            list(iterutils.interlace('x', [1, 2, 3])),
            [1, 'x', 2, 'x', 3])

