
from twisted.trial.unittest import TestCase

from imaginary.language import express, ItemizedList


# probably belongs in a test-processing module.

class TestItemizedList(TestCase):

    def testListing(self):
        self.assertEquals(
            u'1, 2, 3 and 4',
            express(ItemizedList([u'1', u'2', u'3', u'4']), None))


class ConceptExpression(TestCase):

    def testBasicTypes(self):
        def mary(observer):
            if observer is mary:
                return u'you '
            else:
                return u'mary '

        def takes(observer):
            if observer is mary:
                return u'take '
            else:
                return u'takes '

        def bob(observer):
            self.fail("Bob is just an observer, nobody should talk to bob")

        THE_IDEA = [mary, takes, u'the apple']

        self.assertEquals(
            express(THE_IDEA,
                    mary),
            u'you take the apple')

        self.assertEquals(
            express(THE_IDEA,
                    bob),
            u'mary takes the apple')
