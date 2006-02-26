
from twisted.trial import unittest
from twisted.python.util import unsignedID

from pottery import iterutils, objects

class formattable:
    def formatTo(self, what):
        return 'shortFormatTo(%X)' % (unsignedID(what),)

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

    def testShortFormatTo(self):
        o = objects.Actor('dummy')
        try:
            self.assertEquals(
                o.format('hello'),
                'hello')

            self.assertEquals(
                o.format(('hello', 'world')),
                'helloworld')

            self.assertEquals(
                o.format((1, 2, 3)),
                '123')

            self.assertEquals(
                o.format(('hello', (1, 2, 3), 'world')),
                'hello123world')

            def gen():
                for i in range(3):
                    yield i
            self.assertEquals(
                o.format(('hello', gen(), 'world')),
                'hello012world')

            self.assertEquals(
                o.format(('hello', formattable())),
                'helloshortFormatTo(' + hex(unsignedID(o)).upper()[2:].rstrip('L') + ')')
        finally:
            o.destroy()
