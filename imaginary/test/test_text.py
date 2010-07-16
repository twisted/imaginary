import pprint, string

from twisted.trial import unittest
from twisted.conch.insults import insults, helper

from imaginary.wiring import textserver
from imaginary import text as T
from imaginary import unc

def F(*a, **kw):
    if "currentAttrs" not in kw:
        kw["currentAttrs"] = T.AttributeSet()
    return ''.join(list(T.flatten(a, **kw)))


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

    def testNoColors(self):
        self.assertEquals(
            F([[T.fg.green, "hi", T.bg.yellow, "there", T.bold, "no"], "normal", [T.fg.blue, "blue"], "notblue"],
              useColors=False),
            "hitherenonormalbluenotblue")

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


class AsynchronousIncrementalUTF8DecoderTestCase(unittest.TestCase):
    """
    Test L{imaginary.wiring.textserver.AsynchronousIncrementalUTF8Decoder}
    """
    def setUp(self):
        self.a = textserver.AsynchronousIncrementalUTF8Decoder()


    def testASCII(self):
        for ch in 'hello, world':
            self.a.add(ch)
        self.assertEquals(self.a.get(), u'hello, world')


    def testTwoBytes(self):
        character = u'\N{LATIN CAPITAL LETTER A WITH GRAVE}'
        byte1, byte2 = character.encode('utf-8')
        self.a.add(byte1)
        self.assertEquals(self.a.get(), u'')
        self.a.add(byte2)
        self.assertEquals(self.a.get(), character)


    def testThreeBytes(self):
        character = u'\N{HIRAGANA LETTER A}'
        byte1, byte2, byte3 = character.encode('utf-8')
        self.a.add(byte1)
        self.assertEquals(self.a.get(), u'')
        self.a.add(byte2)
        self.assertEquals(self.a.get(), u'')
        self.a.add(byte3)
        self.assertEquals(self.a.get(), character)


    def testFourBytes(self):
        character = u'\N{BYZANTINE MUSICAL SYMBOL PSILI}'
        byte1, byte2, byte3, byte4 = character.encode('utf-8')
        self.a.add(byte1)
        self.assertEquals(self.a.get(), u'')
        self.a.add(byte2)
        self.assertEquals(self.a.get(), u'')
        self.a.add(byte3)
        self.assertEquals(self.a.get(), u'')
        self.a.add(byte4)
        self.assertEquals(self.a.get(), character)


    def testSeveralCharacters(self):
        char1 = u'\N{LATIN CAPITAL LETTER A WITH GRAVE}'
        byte1, byte2 = char1.encode('utf-8')
        self.a.add(byte1)
        self.assertEquals(self.a.get(), u'')
        self.a.add(byte2)
        self.assertEquals(self.a.get(), char1)

        char2 = u'\N{HIRAGANA LETTER A}'
        byte1, byte2, byte3 = char2.encode('utf-8')
        self.a.add(byte1)
        self.assertEquals(self.a.get(), char1)
        self.a.add(byte2)
        self.assertEquals(self.a.get(), char1)
        self.a.add(byte3)
        self.assertEquals(self.a.get(), char1 + char2)

        char3 = u'\N{BYZANTINE MUSICAL SYMBOL PSILI}'
        byte1, byte2, byte3, byte4 = char3.encode('utf-8')
        self.a.add(byte1)
        self.assertEquals(self.a.get(), char1 + char2)
        self.a.add(byte2)
        self.assertEquals(self.a.get(), char1 + char2)
        self.a.add(byte3)
        self.assertEquals(self.a.get(), char1 + char2)
        self.a.add(byte4)
        self.assertEquals(self.a.get(), char1 + char2 + char3)


    def testReset(self):
        self.a.add('a')
        self.a.reset()
        self.assertEquals(self.a.get(), u'')


    def testNarrowWidth(self):
        self.a.add('a')
        self.assertEquals(self.a.width(), 1)


    def testWideWidth(self):
        map(self.a.add, u'\N{HIRAGANA LETTER A}'.encode('utf-8'))
        self.assertEquals(self.a.width(), 2)


    def testMixedWidth(self):
        self.a.add('a')
        map(self.a.add, u'\N{HIRAGANA LETTER A}'.encode('utf-8'))
        self.assertEquals(self.a.width(), 3)
        map(self.a.add, u'\N{HIRAGANA LETTER A}'.encode('utf-8'))
        self.a.add('a')
        self.assertEquals(self.a.width(), 6)


    def testPop(self):
        self.a.add('a')
        self.assertEquals(self.a.pop(), u'a')
        self.assertEquals(self.a.get(), u'')


    def testPopIncompleteCharacter(self):
        self.a.add(u'\N{LATIN CAPITAL LETTER A WITH GRAVE}'.encode('utf-8')[0])
        self.assertRaises(ValueError, self.a.pop)


    def testPopEmpty(self):
        self.assertRaises(IndexError, self.a.pop)



class UTF8TerminalBuffer(helper.TerminalBuffer):
    # An unfortunate hack'n'paste of
    # helper.TerminalBuffer.insertAtCursor
    def insertAtCursor(self, b):
        if b == '\r':
            self.x = 0
        elif b == '\n' or self.x >= self.width:
            self.x = 0
            self._scrollDown()
        # The following conditional has been changed from the original.
        if (b > '\x7f' or b in string.printable) and b not in '\r\n':
            ch = (b, self._currentCharacterAttributes())
            if self.modes.get(insults.modes.IRM):
                self.lines[self.y][self.x:self.x] = [ch]
                self.lines[self.y].pop()
            else:
                self.lines[self.y][self.x] = ch
            self.x += 1



class TextServerTestCase(unittest.TestCase):
    """
    Tests for L{imaginary.wiring.textserver}
    """

    def setUp(self):
        self.terminal = UTF8TerminalBuffer()
        self.terminal.connectionMade()
        self.protocol = textserver.TextServerBase()
        self.protocol.makeConnection(self.terminal)
        self.terminal.reset()


    def testUTF8Input(self):
        character = u'\N{HIRAGANA LETTER A}'
        for ch in character.encode('utf-8'):
            self.protocol.keystrokeReceived(ch, None)
        self.assertEquals(str(self.terminal).strip(),
                          character.encode('utf-8'))


    def testNonPrintableInput(self):
        lines = []
        self.protocol.lineReceived = lines.append

        bytes = range(0, 127)
        for special in [8, 10, 13]:
            bytes.remove(special)
        bytes = ''.join(map(chr, bytes)) + 'WOO'

        expected = ''.join([byte for byte in bytes
                            if byte >= ' ' and byte != '\x7f'])
        expected = expected.decode('ascii')

        for byte in bytes:
            self.protocol.keystrokeReceived(byte, None)
        self.protocol.keystrokeReceived('\n', None)
        self.assertEquals(lines, [expected])


    def _backspaceTest(self, character, width):
        """
        Verify that a character is erased properly by a backspace.

        @param character: The character to receive, echo, and then have
            deleted.
        @type character: C{unicode}

        @param width: How many columns the given character is expected to be
            when rendered.  This is how many backspaces are expected to be
            required to erase it.
        @type width: C{int}
        """
        lines = []
        self.protocol.lineReceived = lines.append

        # The terminal emulator we use doesn't know enough unicode for this
        # test to work out right.  So we'll fake it ourselves here.
        written = []
        self.terminal.write = written.append

        self.protocol.keystrokeReceived('a', None)
        self.protocol.keystrokeReceived(character.encode('utf-8'), None)
        self.protocol.keystrokeReceived(self.terminal.BACKSPACE, None)

        self.assertEquals(
            ''.join(written),
            'a' + character.encode('utf-8') +
            '\b' * width + ' ' * width + '\b' * width)


    def test_eraseNarrowWithBackspace(self):
        """
        If a backspace keystroke is received when the cursor is positioned
        directly after a character with an I{east asian width} of I{narrow},
        the character is removed from the input buffer and the character is
        erased from the client display with a C{'\b \b'} sequence.
        """
        self._backspaceTest(u'x', 1)


    def test_eraseWideWithBackspace(self):
        """
        If a backspace keystroke is received when the cursor is positioned
        directly after a character with an I{east asian width} of I{wide}, the
        character is removed from the input buffer and the character is
        erased from the client display with a C{'\b\b  \b\b'} sequence.
        """
        self._backspaceTest(u'\u1100', 2)


    def test_eraseFullwidthWithBackspace(self):
        """
        If a backspace keystroke is received when the cursor is positioned
        directly after a character with an I{east asian width} of
        I{fullwidth}, character is removed from the input buffer and the
        character is erased from the client display with a C{'\b\b  \b\b'}
        sequence.
        """
        self._backspaceTest(u'\u3000', 2)


    def test_eraseHalfwidthWithBackspace(self):
        """
        If a backspace keystroke is received when the cursor is positioned
        directly after a character with an I{east asian width} of
        I{halfwidth}, character is removed from the input buffer and the
        character is erased from the client display with a C{'\b \b'}
        sequence.
        """
        self._backspaceTest(u'\u20a9', 1)


    def test_eraseNeutralWithBackspace(self):
        """
        If a backspace keystroke is received when the cursor is positioned
        directly after a character with an I{east asian width} of
        I{neutral}, character is removed from the input buffer and the
        character is erased from the client display with a C{'\b \b'}
        sequence.
        """
        self._backspaceTest(u'\xa0', 1)


    def test_eraseAmbiguousWithBackspace(self):
        """
        If a backspace keystroke is received when the cursor is positioned
        directly after a character with an I{east asian width} of
        I{neutral}, character is removed from the input buffer and the
        character is erased from the client display with a C{'\b \b'}
        sequence.
        """
        self._backspaceTest(u'\xa1', 1)
