"""
Tests for the conversion between abstract objects representing the world or
changes in the world into concrete per-user-interface content.
"""

import attr

from zope.interface import implementer
from zope.interface.verify import verifyClass

from twisted.trial import unittest

from imaginary import language, unc, text as T, iimaginary
from imaginary.test import commandutils

class FakeThing(object):
    def __init__(self, **kw):
        self.__dict__.update(kw)



class NounTestCase(unittest.TestCase):
    def setUp(self):

        self.thing = FakeThing(
            name=u'fake thing',
            description=u"Fake Thing Description",
            gender="!@>",
            proper=False,
            powerupsFor=lambda iface: [],
            )
        self.male = FakeThing(
            name=u"billy",
            gender=language.Gender.MALE,
            )
        self.female = FakeThing(
            name=u"janey",
            gender=language.Gender.FEMALE,
            )
        self.observer = FakeThing()
        self.noun = language.Noun(self.thing)
        self.malenoun = language.Noun(self.male)
        self.femalenoun = language.Noun(self.female)



class SharedTextyTests(commandutils.LanguageMixin):
    def format(self, concept):
        raise NotImplementedError("Implement me")

    def testExpressString(self):
        self.assertEquals(self.format(language.ExpressString(u"foo bar")), u"foo bar")


    def testExpressList(self):
        self.assertEquals(self.format(language.ExpressList([
            language.ExpressString(u"foo"),
            u" ",
            language.ExpressString(u"bar")])),
                          u"foo bar")

    def testItemizedList(self):
        self.assertEquals(self.format(language.ItemizedList([])),
                          u'') # XXX Does this make sense?

        self.assertEquals(self.format(language.ItemizedList([
            u'foo'])),
                          u'foo')
        self.assertEquals(self.format(language.ItemizedList([
            u'foo', u'bar'])),
                          u'foo and bar')
        self.assertEquals(self.format(language.ItemizedList([
            u'foo', u'bar', u'baz'])),
                          u'foo, bar, and baz')


    def testShortName(self):
        self.assertEquals(self.format(self.noun.shortName()), u"fake thing")


    def testNounPhrase(self):
        self.assertEquals(self.format(self.noun.nounPhrase()), u"a fake thing")


    def testProperNounPhrase(self):
        self.thing.proper = True
        self.assertEquals(self.format(self.noun.nounPhrase()), u"fake thing")


    def testDefiniteNounPhrase(self):
        self.assertEquals(self.format(self.noun.definiteNounPhrase()), u"the fake thing")


    def testProperDefiniteNounPhrase(self):
        self.thing.proper = True
        self.assertEquals(self.format(self.noun.definiteNounPhrase()), u"fake thing")


    def testPersonalPronoun(self):
        self.assertEquals(self.format(self.malenoun.heShe()), u"he")
        self.assertEquals(self.format(self.femalenoun.heShe()), u"she")
        self.assertEquals(self.format(self.noun.heShe()), u"it")


    def testObjectivePronoun(self):
        self.assertEquals(self.format(self.malenoun.himHer()), u'him')
        self.assertEquals(self.format(self.femalenoun.himHer()), u'her')
        self.assertEquals(self.format(self.noun.himHer()), u'it')


    def testPossessivePronoun(self):
        self.assertEquals(self.format(self.malenoun.hisHer()), u'his')
        self.assertEquals(self.format(self.femalenoun.hisHer()), u'her')
        self.assertEquals(self.format(self.noun.hisHer()), u'its')



    def testCapitalization(self):
        self.assertEquals(
            self.format(language.ExpressString(u"foo").capitalizeConcept()),
            u"Foo")
        self.assertEquals(
            self.format(language.ExpressList([[[[u"hi"]]]]).capitalizeConcept()),
            u"Hi")
        self.assertEquals(
            self.format(language.ItemizedList([u"foo", u"bar", u"baz"]).capitalizeConcept()),
            u"Foo, bar, and baz")


    def testSentence(self):
        self.assertEquals(
            self.format(language.Sentence([self.noun.nounPhrase(), u" is awesome."])),
            u"A fake thing is awesome.")




def _description(title=None, exits=(), description=None, components=None):
    """

    """
    return language.Description(
        title=title, exits=exits, description=description,
        components=components)



class PlaintextDescriptionTests(NounTestCase, SharedTextyTests):

    def format(self, concept):
        return self.flatten(concept.plaintext(self.observer))


    def test_missingDescription(self):
        """
        L{Description.plaintext} can be used with with a C{None} description.
        """
        self.assertEqual(
            self.format(
                _description(title=self.thing.name,
                                  description=None)),
            u'[ fake thing ]\n'
        )


    def test_emptyDescription(self):
        """
        L{Description.plaintext} can be used with an empty string description.
        """
        self.assertEqual(
            self.format(
                _description(title=self.thing.name, description=u'')),
            u'[ fake thing ]\n'
        )


    def test_description(self):
        """
        A non-empty description string is included in the result of
        L{Description.plaintext}.
        """
        self.assertEqual(
            self.format(
                _description(title=self.thing.name,
                                  description=self.thing.description)),
            u'[ fake thing ]\n'
            u'Fake Thing Description\n'
        )


    def test_exitsDescription(self):
        """
        A L{Description.plaintext} includes any exits.
        """
        exits = [StubExit(name=u"north"), StubExit(name=u"west")]
        self.assertEqual(
            self.format(
                _description(title=self.thing.name,
                                  description=self.thing.description,
                                  exits=exits)),
            u'[ fake thing ]\n'
            u'( north west )\n'
            u'Fake Thing Description\n'
        )


    def test_components(self):
        """
        A L{Description.plaintext} includes any extra components.
        """
        a = language.ExpressString(u"first part")
        b = language.ExpressString(u"last part")
        self.assertEquals(
            self.format(
                _description(title=self.thing.name,
                                  description=self.thing.description,
                                  components=[a, b])),
            u'[ fake thing ]\n'
            u'Fake Thing Description\n' +
            a.original + u"\n" +
            b.original
        )


@attr.s
@implementer(iimaginary.IExit)
class StubExit(object):
    name = attr.ib()

    def shouldEvenAttemptTraversalFrom(self, where, thing):
        """
        Yes.
        """
        return True


    def traverse(self, thing):
        """
        Don't go anywhere.
        """



verifyClass(iimaginary.IExit, StubExit)

class VT102Tests(NounTestCase, SharedTextyTests):
    def format(self, concept):
        return self.flatten(concept.vt102(self.observer))


    def unparse(self, s):
        print repr(s)
        return list(unc.parser(unc.tokenize(s)))

    def _assertECMA48Equality(self, a, b):
        errorLines = ['%-38s|%38s' % ('received', 'expected')]
        for la, lb in map(None,
                          unc.prettystring(a).splitlines(),
                          unc.prettystring(b).splitlines()):
            errorLines.append('%-38s|%38s' % (la, lb))

        self.assertEquals(a, b, '\nERROR!\n' + '\n'.join(errorLines))

    def test_missingDescription(self):
        """
        L{Description.vt102} can be used with with a C{None} description.
        """
        self.thing.description = None
        self._assertECMA48Equality(
            self.format(_description(title=self.thing.name,
                                     description=self.thing.description)),
            self.flatten([T.bold, T.fg.green, u'[ ', [T.fg.normal, "fake thing"], u' ]\n']))


    def test_emptyDescription(self):
        """
        L{Description.vt102} can be used with an empty string description.
        """
        self.thing.description = u''
        self._assertECMA48Equality(
            self.format(_description(title=self.thing.name,
                                     description=self.thing.description)),
            self.flatten([T.bold, T.fg.green, u'[ ', [T.fg.normal, "fake thing"], u' ]\n']))


    def test_description(self):
        """
        A non-empty description string is included in the result of
        L{Description.vt102}.
        """
        self._assertECMA48Equality(
            self.format(_description(title=self.thing.name,
                                     description=self.thing.description)),
            self.flatten([[T.bold, T.fg.green, u'[ ', [T.fg.normal, "fake thing"], u' ]\n'],
                          T.fg.green, u'Fake Thing Description\n']))


    def test_exitsDescription(self):
        """
        A L{Description.vt102} includes any exits.
        """
        exits = [StubExit(name=u"north"), StubExit(name=u"west")]
        self._assertECMA48Equality(
            self.format(_description(title=self.thing.name,
                                     description=self.thing.description,
                                     exits=exits)),
            self.flatten([[T.bold, T.fg.green, u'[ ', [T.fg.normal, "fake thing"], u' ]\n'],
                          [T.bold, T.fg.green, u'( ', [T.fg.normal, T.fg.yellow, u'north west'], u' )', u'\n'],
                          T.fg.green, u'Fake Thing Description\n']))


    def test_descriptionContributors(self):
        """
        A L{Description.vt102} includes any extra components.
        """
        a = language.ExpressString(u"first part")
        b = language.ExpressString(u"last part")
        self._assertECMA48Equality(
            self.format(_description(title=self.thing.name,
                                     description=self.thing.description,
                                     components=[a, b])),
            self.flatten([[[T.bold, T.fg.green, u'[ ', [T.fg.normal, "fake thing"], u' ]\n'],
                           T.fg.green, u'Fake Thing Description\n'], a.original + u"\n" + b.original]))
