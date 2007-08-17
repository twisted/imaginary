
"""
Tests for the conversion between abstract objects representing the world or
changes in the world into concrete per-user-interface content.
"""

from twisted.trial import unittest

from epsilon import structlike

from imaginary import language, unc, text as T
from imaginary.test import commandutils

class FakeThing(object):
    def __init__(self, **kw):
        self.__dict__.update(kw)



class FakeDescriptionContributor:
    def __init__(self, description):
        self.descr = description


    def conceptualize(self):
        return language.ExpressString(self.descr)



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




class BasicConceptTestCasePlaintext(NounTestCase, SharedTextyTests):

    def format(self, concept):
        return self.flatten(concept.plaintext(self.observer))


    def testMissingDescription(self):
        self.thing.description = None
        self.assertEquals(self.format(language.DescriptionConcept(self.thing.name, self.thing.description)),
                          u'[ fake thing ]\n')


    def testEmptyDescription(self):
        self.thing.description = u''
        self.assertEquals(self.format(language.DescriptionConcept(self.thing.name, self.thing.description)),
                          u'[ fake thing ]\n')


    def testDescription(self):
        self.assertEquals(self.format(language.DescriptionConcept(self.thing.name, self.thing.description)),
                          u'[ fake thing ]\n'
                          u'Fake Thing Description\n')


    def testExitsDescription(self):
        exits = [StubExit(name=u"north"), StubExit(name=u"west")]
        self.assertEquals(self.format(language.DescriptionConcept(self.thing.name, self.thing.description, exits)),
                          u'[ fake thing ]\n'
                          u'( north west )\n'
                          u'Fake Thing Description\n')


    def testDescriptionContributors(self):
        a = FakeDescriptionContributor(u"first part")
        b = FakeDescriptionContributor(u"last part")
        self.assertEquals(self.format(language.DescriptionConcept(self.thing.name, self.thing.description, others=[a, b])),
                          u'[ fake thing ]\n'
                          u'Fake Thing Description\n' +
                          a.descr + u"\n" +
                          b.descr)


class StubExit(structlike.record("name")):
    pass

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

    def testMissingDescription(self):
        self.thing.description = None
        self._assertECMA48Equality(
            self.format(language.DescriptionConcept(self.thing.name, self.thing.description)),
            self.flatten([T.bold, T.fg.green, u'[ ', [T.fg.normal, "fake thing"], u' ]\n']))


    def testEmptyDescription(self):
        self.thing.description = u''
        self._assertECMA48Equality(
            self.format(language.DescriptionConcept(self.thing.name, self.thing.description)),
            self.flatten([T.bold, T.fg.green, u'[ ', [T.fg.normal, "fake thing"], u' ]\n']))


    def testDescription(self):
        self._assertECMA48Equality(
            self.format(language.DescriptionConcept(self.thing.name, self.thing.description)),
            self.flatten([[T.bold, T.fg.green, u'[ ', [T.fg.normal, "fake thing"], u' ]\n'],
                          T.fg.green, u'Fake Thing Description\n']))


    def testExitsDescription(self):
        exits = [StubExit(name=u"north"), StubExit(name=u"west")]
        self._assertECMA48Equality(
            self.format(language.DescriptionConcept(self.thing.name, self.thing.description, exits)),
            self.flatten([[T.bold, T.fg.green, u'[ ', [T.fg.normal, "fake thing"], u' ]\n'],
                          [T.bold, T.fg.green, u'( ', [T.fg.normal, T.fg.yellow, u'north west'], u' )', u'\n'],
                          T.fg.green, u'Fake Thing Description\n']))


    def testDescriptionContributors(self):
        a = FakeDescriptionContributor(u"first part")
        b = FakeDescriptionContributor(u"last part")
        self._assertECMA48Equality(
            self.format(language.DescriptionConcept(self.thing.name, self.thing.description, others=[a, b])),
            self.flatten([[[T.bold, T.fg.green, u'[ ', [T.fg.normal, "fake thing"], u' ]\n'],
                          T.fg.green, u'Fake Thing Description\n'], a.descr + u"\n" + b.descr]))
