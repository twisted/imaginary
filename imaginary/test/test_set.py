
"""
Tests for the set action implemented by L{imaginary.actions.Set}.
"""

from twisted.trial.unittest import TestCase

from imaginary.iimaginary import IContainer
from imaginary.objects import Thing
from imaginary.language import Gender
from imaginary.test.commandutils import CommandTestCaseMixin


class SetTests(CommandTestCaseMixin, TestCase):
    """
    Tests for the set action which allows model-level state to be directly
    manipulated.
    """
    def test_unrecognizedAttribute(self):
        """
        The set action reports a failure when invoked with an attribute it
        cannot change.
        """
        self._test(
            "set monkey of me to stuff",
            ["You cannot set that."])


    def test_maleGender(self):
        """
        The set action can change the value the gender attribute of a thing to
        L{Gender.MALE}.
        """
        self._test(
            "set gender of me to male",
            ["You set your gender to male."])
        self.assertEqual(self.player.gender, Gender.MALE)


    def test_femaleGender(self):
        """
        The set action can change the value the gender attribute of a thing to
        L{Gender.FEMALE}.
        """
        self._test(
            "set gender of me to female",
            ["You set your gender to female."])
        self.assertEqual(self.player.gender, Gender.FEMALE)


    def test_neuterGender(self):
        """
        The set action can change the value the gender attribute of a thing to
        L{Gender.NEUTER}.
        """
        self._test(
            "set gender of me to neuter",
            ["You set your gender to neuter."])
        self.assertEqual(self.player.gender, Gender.NEUTER)


    def test_unrecognizedGender(self):
        """
        The set action reports a failure with usage information if invoked with
        a string which is not a gender.
        """
        self.player.gender = Gender.FEMALE
        self._test(
            "set gender of me to monkey",
            ["Only male, female, and neuter are valid genders.  You "
             "remain female."])
        self.assertEqual(self.player.gender, Gender.FEMALE)


    def test_secondPartyGender(self):
        """
        The set action can change the value of the gender attribute of a thing
        other than the player issuing the action.
        """
        self._test(
            'set gender of "Observer Player" to male',
            ["You set his gender to male."],
            ["Test Player set your gender to male."])


    def test_properNoun(self):
        """
        The set action can change the value of the proper attribute of a thing
        to True.
        """
        something = Thing(store=self.store, name=u"something", proper=False)
        IContainer(self.location).add(something)
        self._test(
            'set proper of something to true',
            ['You make the name of "something" a proper noun.'])
        self.assertTrue(something.proper)


    def test_commonNoun(self):
        """
        The set action can change the value of the proper attribute of a thing
        to False.
        """
        something = Thing(store=self.store, name=u"something", proper=True)
        IContainer(self.location).add(something)
        self._test(
            'set proper of something to false',
            ['You make the name of "something" a common noun.'])
        self.assertFalse(something.proper)


    def test_unrecognizedNounType(self):
        """
        The set action reports a failure with usage information if invoked with
        a string which cannot be interpreted as a boolean value.
        """
        something = Thing(store=self.store, name=u"something", proper=True)
        IContainer(self.location).add(something)
        self._test(
            'set proper of something to blarg',
            ['Only true and false are valid settings for proper.'])
        self.assertTrue(something.proper)

