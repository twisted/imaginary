
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
