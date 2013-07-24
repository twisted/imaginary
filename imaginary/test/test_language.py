
from twisted.trial.unittest import TestCase

from imaginary.objects import Thing
from imaginary.language import Gender, ConceptTemplate, ExpressList
from imaginary.test.commandutils import flatten

class ConceptTemplateTests(TestCase):
    """
    Tests for L{imaginary.language.ConceptTemplate}.
    """
    def setUp(self):
        self.thing = Thing(name=u"alice", gender=Gender.FEMALE)


    def expandToText(self, template, values):
        """
        Expand the given L{ConceptTemplate} with the given values and flatten
        the result into a L{unicode} string.
        """
        return flatten(ExpressList(template.expand(values)).plaintext(None))


    def test_unexpandedLiteral(self):
        """
        A template string containing no substitution markers expands to itself.
        """
        self.assertEqual(
            u"hello world",
            self.expandToText(ConceptTemplate(u"hello world"), {}))


    def test_expandedName(self):
        """
        I{field:name} can be used to substitute the name of the value given by
        C{"field"}.
        """
        template = ConceptTemplate(u"{a:name}")
        self.assertEqual(
            u"alice",
            self.expandToText(template, dict(a=self.thing)))


    def test_expandedPronoun(self):
        """
        I{field:pronoun} can be used to substitute the personal pronoun of the
        value given by C{"field"}.
        """
        template = ConceptTemplate(u"{b:pronoun}")
        self.assertEqual(
            u"she",
            self.expandToText(template, dict(b=self.thing)))


    def test_intermixed(self):
        """
        Literals and subsitution markers may be combined in a single template.
        """
        template = ConceptTemplate(u"{c:pronoun} wins.")
        self.assertEqual(
            u"she wins.",
            self.expandToText(template, dict(c=self.thing)))


    def test_multiples(self):
        """
        Multiple substitution markers may be used in a single template.
        """
        another = Thing(name=u"bob", gender=Gender.FEMALE)
        template = ConceptTemplate(u"{a:name} hits {b:name}.")
        self.assertEqual(
            u"alice hits bob.",
            self.expandToText(template, dict(a=self.thing, b=another)))


    def test_adjacent(self):
        """
        Adjacent substitution markers are expanded without introducing
        extraneous intervening characters.
        """
        another = Thing(name=u"bob", gender=Gender.FEMALE)
        template = ConceptTemplate(u"{a:name}{b:name}")
        self.assertEqual(
            u"alicebob",
            self.expandToText(template, dict(a=self.thing, b=another)))


    def test_missingTarget(self):
        """
        A missing target is expanded to a warning about a bad template.
        """
        template = ConceptTemplate(u"{c} wins.")
        self.assertEqual(
            u"<missing target 'c' for expansion> wins.",
            self.expandToText(template, dict()))


    def test_missingTargetWithSpecifier(self):
        """
        A missing target is expanded to a warning about a bad template.
        """
        template = ConceptTemplate(u"{c:pronoun} wins.")
        self.assertEqual(
            u"<missing target 'c' for 'pronoun' expansion> wins.",
            self.expandToText(template, dict()))


    def test_unsupportedSpecifier(self):
        """
        A specifier not supported on the identified target is expanded to a
        warning about a bad template.
        """
        template = ConceptTemplate(u"{c:glorbex} wins.")
        self.assertEqual(
            u"<'glorbex' unsupported by target 'c'> wins.",
            self.expandToText(template, dict(c=self.thing)))
