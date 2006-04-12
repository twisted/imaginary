from twisted.trial import unittest

from imaginary import objects, quiche, iimaginary
from imaginary.test import commandutils


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

    def testBuyingQuiche(self):
        self._test("create 'vending machine' vendy",
                   ["vendy created."],
                   ["Test Player creates vendy."])

        self._test("drop vendy",
                   ["You drop vendy."],
                   ["Test Player drops vendy."])

        self._test("create quiche quiche",
                   ["quiche created."],
                   ["Test Player creates quiche."])

        self._test("open vendy",
                   ["You open vendy."],
                   ["Test Player opens vendy."])

        self._test("put quiche in vendy",
                   ["You put quiche in vendy."],
                   ["Test Player puts quiche in vendy."])

        for i in range(5):
            self._test("create quarter quarter%s " % i,
                       ["quarter%s created." % i],
                       ["Test Player creates quarter%s." % i])

        for i in range(4):
            self._test("put quarter%i in vendy" % i,
                       ["You put quarter%s in vendy." % i],
                       ["Test Player puts quarter%s in vendy." % i])

        # XXX - This order is wrong, fix it.
        self._test("put quarter4 in vendy",
                   ["vendy thumps loudly and spits out quiche onto the ground.",
                    "You put quarter4 in vendy."],
                   ["vendy thumps loudly and spits out quiche onto the ground.",
                    "Test Player puts quarter4 in vendy."])

    def testProgrammaticQuichePurchase(self):
        location = objects.Object(store=self.store, name=u"room")
        icloc = objects.Container(store=self.store, capacity=500)
        icloc.installOn(location)

        vm = quiche.createVendingMachine(self.store, u"Vendy", u"VEEEENDYYYYY")
        vm.moveTo(location)

        icvm = iimaginary.IContainer(vm)
        icvm.closed = False
        theQuiche = quiche.createQuiche(self.store, u"quiche")
        icvm.add(theQuiche)
        icvm.closed = True

        for i in range(4):
            quarter = quiche.createCoin(store=self.store, name=u"quarter%s" % (i,))
            icvm.add(quarter)

        quarter = quiche.createCoin(store=self.store, name=u"quarter4")
        icvm.add(quarter)

        self.failUnless(icloc.contains(theQuiche))

