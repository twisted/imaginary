# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.
# -*- test-case-name: imaginary.test.test_language -*-

"""
Tests for L{imaginary.language}.
"""

from twisted.trial.unittest import SynchronousTestCase as TestCase

from imaginary.objects import Thing
from imaginary.language import Gender, ConceptTemplate, ExpressList, Noun
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

        @param template: a L{ConceptTemplate} with some markup in it

        @param values: the values to interpolate into C{template}

        @return: the text resulting from rendering the given template
        @rtype: L{unicode}
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



def textNounForm(nounFormMethod):
    """
    Create a function for rendering the given noun-form method on L{Noun} to
    text.

    @param nounFormMethod: the name of the noun-form method in question
    @type nounFormMethod: native L{str}

    @return: a function that takes a L{Thing} and returns some text
    @rtype: function(L{Thing}) -> L{unicode}
    """
    def function(thing):
        return flatten(getattr(Noun(thing), nounFormMethod)().plaintext(None))
    return function

heShe = textNounForm("heShe")
himHer = textNounForm("himHer")
hisHer = textNounForm("hisHer")
hisHers = textNounForm("hisHers")

def fourForms(function):
    """
    Generate four noun declensions for the given L{textNounForm} function.

    @rtype: four noun declensions in the order female, male, indeterminate, and
        neuter/impersonal gender.

    @rtype: a 4-L{tuple} of L{unicode}
    """
    alice = Thing(name=u"alice", gender=Gender.FEMALE)
    bob = Thing(name=u"bob", gender=Gender.MALE)
    pat = Thing(name=u"pat", gender=Gender.INDETERMINATE)
    killbot9000 = Thing(name=u"killbot", gender=Gender.NEUTER)
    return tuple(map(function, [alice, bob, killbot9000, pat]))



class DeclensionTests(TestCase):
    """
    Tests for the declension of various noun forms.
    """

    def test_subjectivePronoun(self):
        """
        L{Noun.heShe} returns a gender-appropriate subjective personal pronoun.
        """
        self.assertEqual(fourForms(heShe), (u"she", u"he", u"it", u"they"))


    def test_objectivePronoun(self):
        """
        L{Noun.himHer} returns a gender-appropriate objective pronoun.
        """
        self.assertEqual(fourForms(himHer), (u"her", u"him", u"it", u"them"))


    def test_possessiveAdjective(self):
        """
        L{Noun.hisHer} returns a gender-appropriate possessive adjective.
        """
        self.assertEqual(fourForms(hisHer), (u"her", u"his", u"its", u"their"))


    def test_hisHers(self):
        """
        L{Noun.hisHers} returns a gender-appropriate substantival possessive
        pronoun.
        """
        self.assertEqual(fourForms(hisHers),
                         (u"hers", u"his", u"its", u"theirs"))
