
import pprint

from twisted.trial import unittest

from imaginary import text as T
from imaginary import unc

class TestStruct(T._structlike):
    __names__ = ['x', 'y', 'z']
    __defaults__ = [1, 2, 3]

class StructLike(unittest.TestCase):
    def testSimpleInstantiation(self):
        x = TestStruct()
        self.assertEquals(x.x, 1)
        self.assertEquals(x.y, 2)
        self.assertEquals(x.z, 3)

        y = TestStruct('3', '2', '1')
        self.assertEquals(y.x, '3')
        self.assertEquals(y.y, '2')
        self.assertEquals(y.z, '1')

        z = TestStruct(z='z', x='x', y='y')
        self.assertEquals(z.x, 'x')
        self.assertEquals(z.y, 'y')
        self.assertEquals(z.z, 'z')

        a = TestStruct('abc')
        self.assertEquals(a.x, 'abc')
        self.assertEquals(a.y, 2)
        self.assertEquals(a.z, 3)

        b = TestStruct(y='123')
        self.assertEquals(b.x, 1)
        self.assertEquals(b.y, '123')
        self.assertEquals(b.z, 3)

def F(*a, **kw):
    if 'currentAttrs' not in kw:
        # Everything is turned off/normaled by default
        kw['currentAttrs'] = T.AttributeSet()
    return ''.join(list(T.flatten(*a, **kw)))


def NN(**kw):
    nkw = dict.fromkeys(T.AttributeSet.__names__, T.unset)
    nkw.update(kw)
    AS = T.AttributeSet(**nkw)
    x = T.neutral.clone().update(AS)
    return x

def E(*s):
    return '\x1b[' + ';'.join(s) + 'm'

class AttributeSetting(unittest.TestCase):
    AS = T.AttributeSet
    B, U, R, L = '1', '4', '7', '5'

    testData = [
        # From    To               Expected    Name?
        (AS(),    AS(),            '',        'no transition'),
        (AS(),    NN(bold=True),   E(B),      'enable bold'),
        (AS(),    NN(),            '',        'do not care about bold'),
        (AS(),    NN(fg='1'),      E('31'),   'red foreground'),
        (AS(),    NN(bg='2'),      E('42'),   'green background')]

    blink = AS(blink=True)
    testData.extend([
        (blink, NN(blink=True),   '',      'no transition'),
        (blink, NN(),             '',      'do not care'),
        (blink, NN(blink=False),  E('0'),  'turn off blink')])

    bu = AS(blink=True, underline=True)
    testData.extend([
        (bu, bu,                               '',        'no transition'),
        (bu, NN(blink=True),                   '',        'do not care'),
        (bu, NN(blink=True, underline=False),  E('0', L), 'disable underline'),
        (bu, NN(underline=False),              E('0', L), 'disable underline'),
        (bu, NN(blink=False, underline=False), E('0'),   'turn it all off')])

    testData.extend([
        (AS(),               NN(fg='1'),         E('31'),     'set fg red'),
        (AS(),               NN(bg='2'),         E('42'),     'set bg green'),
        (AS(),             NN(fg='3', bg='4'), E('33', '44'), 'set fg and bg'),
        (AS(fg='5'),         NN(fg='9'),         E('0'),      'reset fg'),
        (AS(bg='6'),         NN(bg='9'),         E('0'),      'reset bg'),
        (AS(fg='7', bg='0'), NN(),               '',          'do nothing'),
        (AS(fg='1', bg='2'), NN(fg='9'),         E('0', '42'), 'reset fg'),
        (AS(fg='3', bg='4'), NN(bg='9'),         E('0', '33'), 'reset bg'),
        (AS(fg='5'),         NN(bg='3'),         E('43'),      'enable bg'),
        (AS(bg='7'),         NN(bg='3'),         E('43'),      'switch bg'),
        (AS(fg='2'),         NN(fg='1'),         E('31'),      'switch fg'),
        (AS(fg='6'),         NN(fg='6'),         '',           'request same'),
        ])

    def testMega(self):
        # trial should support this use case.
        failures = []
        for n, (start, finish, output, msg) in enumerate(self.testData):
            got = finish.toVT102(start)

            if got != output:
                failures.append((got, output, str(n) + ': ' + msg))

        if failures:
            failures.insert(0,
                            ('received', 'expected', "what's up"))
            raise unittest.FailTest(pprint.pformat(failures))

class Colorization(unittest.TestCase):
    def testTrivialStringOnly(self):
        self.assertEquals(
            F('hello world'),
            'hello world')

        self.assertEquals(
            F('hello', ' ', 'world'),
            'hello world')

        self.assertEquals(
            F(''),
            '')

    def testTrivialStringAndList(self):
        self.assertEquals(
            F(['hello world']),
            'hello world')

        self.assertEquals(
            F(['hello', ' ', 'world']),
            'hello world')

        self.assertEquals(
            F(['hello', [' ', ['world']]]),
            'hello world')

        self.assertEquals(
            F(['hello', [' '], 'world']),
            'hello world')

        self.assertEquals(
            F([[['hello'], ' '], 'world']),
            'hello world')

    def testTrivialStringWithAttributes(self):
        self.assertEquals(
            F('hello world', currentAttrs=T.fg.normal),
            'hello world')

    def testForegroundColorization(self):
        for code, sym in [(30, T.fg.black),
                          (31, T.fg.red),
                          (32, T.fg.green),
                          (33, T.fg.yellow),
                          (34, T.fg.blue),
                          (35, T.fg.magenta),
                          (36, T.fg.cyan),
                          (37, T.fg.white)]:
            self.assertEquals(
                F(sym, 'hello world'),
                '\x1b[%dmhello world\x1b[0m' % (code,))

    def testBackgroundColorization(self):
        for code, sym in [(40, T.bg.black),
                          (41, T.bg.red),
                          (42, T.bg.green),
                          (43, T.bg.yellow),
                          (44, T.bg.blue),
                          (45, T.bg.magenta),
                          (46, T.bg.cyan),
                          (47, T.bg.white)]:
            self.assertEquals(
                F(sym, 'hello world'),
                '\x1b[%dmhello world\x1b[0m' % (code,))

    def testExtraAttributes(self):
        for code, sym in [(1, T.bold),
                          (5, T.blink),
                          (7, T.reverseVideo),
                          (4, T.underline)]:
            self.assertEquals(
                F(sym, 'hello world'),
                '\x1b[%dmhello world\x1b[0m' % (code,))

        self.assertEquals(F(T.fg.normal, 'hello world'), 'hello world')
        self.assertEquals(F(T.bg.normal, 'hello world'), 'hello world')

    def testSmallerNestedCharacterState(self):
        a = F([T.fg.red, 'red', [T.reverseVideo, '!red']])
        b = '\x1b[31mred\x1b[7m!red\x1b[0m'

        self.assertEquals(a, b)

    def _assertECMA48Equality(self, a, b):
        errorLines = ['received\t\texpected']
        for la, lb in zip(unc.prettystring(a).splitlines(),
                          unc.prettystring(b).splitlines()):
            errorLines.append(la + '\t\t' + lb)

        self.assertEquals(a, b, '\nERROR!\n' + '\n'.join(errorLines))

    def testNestedCharacterState(self):
        a = F([T.fg.red, 'hello'],
              [T.bg.green, 'world',
              [T.bg.normal, 'more worlds']],
              [T.blink, 'blinky'],
              [T.fg.red, T.bg.blue, 'multicolor',
               [T.reverseVideo, 'colormulti']])
        b = ('\x1b[31mhello'
             '\x1b[0;42mworld'
             '\x1b[0mmore worlds'
             '\x1b[5mblinky'
             '\x1b[0;31;44mmulticolor'
             '\x1b[7mcolormulti\x1b[0m')
        self._assertECMA48Equality(a, b)

        self._assertECMA48Equality(
            F([T.fg.red, [T.bg.green, [T.blink, 'hello'], ' '], 'world']),
            '\x1b[5;31;42mhello\x1b[0;31;42m \x1b[0;31mworld\x1b[0m')
        
        self._assertECMA48Equality(
            F([T.fg.cyan,
               T.bg.magenta,
               'Hello ',
               [T.fg.normal, 'world'],
               '.']),
            '\x1b[36;45mHello \x1b[0;45mworld\x1b[36m.\x1b[0m')

