from twisted.trial import unittest

from pottery.test import commandutils

class VendingTest(commandutils.CommandTestCaseMixin, unittest.TestCase):
    def testTheyExist(self):
        self._test("create 'vending machine' vendy",
                   ["vendy created."],
                   ["Test Player creates vendy."])


    def testPopulateVendingMachine(self):
        self._test("create 'vending machine' vendy",
                   ["vendy created."],
                   ["Test Player creates vendy."])

        self._test("create quiche quiche",
                   ["quiche created."],
                   ["Test Player creates quiche."])

        self._test("open vendy",
                   ["You open vendy."],
                   ["Test Player opens vendy."])

        self._test("put quiche in vendy",
                   ["You put quiche in vendy."],
                   ["Test Player puts quiche in vendy."])
