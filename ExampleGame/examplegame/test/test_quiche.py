from twisted.trial import unittest

from imaginary import objects, iimaginary
from imaginary.test import commandutils

from examplegame import quiche


class VendingTest(commandutils.CommandTestCaseMixin, unittest.TestCase):
    def testTheyExist(self):
        self._test("create the 'vending machine' named vendy",
                   ["You create vendy."],
                   ["Test Player creates vendy."])


    def testPopulateVendingMachine(self):
        self._test("create the 'vending machine' named vendy",
                   ["You create vendy."],
                   ["Test Player creates vendy."])

        self._test("create a quiche named quiche",
                   ["You create a quiche."],
                   ["Test Player creates a quiche."])

        self._test("open vendy",
                   ["You open vendy."],
                   ["Test Player opens vendy."])

        self._test("put quiche in vendy",
                   ["You put the quiche in vendy."],
                   ["Test Player puts a quiche in vendy."])


    def testBuyingQuiche(self):
        self._test("create the 'vending machine' named vendy",
                   ["You create vendy."],
                   ["Test Player creates vendy."])

        self._test("drop vendy",
                   ["You drop vendy."],
                   ["Test Player drops vendy."])

        self._test("create a quiche named quiche",
                   ["You create a quiche."],
                   ["Test Player creates a quiche."])

        self._test("open vendy",
                   ["You open vendy."],
                   ["Test Player opens vendy."])

        self._test("put quiche in vendy",
                   ["You put the quiche in vendy."],
                   ["Test Player puts a quiche in vendy."])

        for i in range(5):
            self._test("create the quarter named quarter%s " % i,
                       ["You create quarter%s." % i],
                       ["Test Player creates quarter%s." % i])

        for i in range(4):
            self._test("put quarter%i in vendy" % i,
                       ["You put quarter%s in vendy." % i],
                       ["Test Player puts quarter%s in vendy." % i])

        self._test("put quarter4 in vendy",
                   ["You put quarter4 in vendy.",
                   "Vendy thumps loudly and spits out a quiche onto the ground."],
                   ["Test Player puts quarter4 in vendy.",
                    "Vendy thumps loudly and spits out a quiche onto the ground."])


    def testProgrammaticQuichePurchase(self):
        location = objects.Thing(store=self.store, name=u"room")
        icloc = objects.Container.createFor(location, capacity=500)

        vm = quiche.createVendingMachine(store=self.store, name=u"Vendy", description=u"VEEEENDYYYYY")
        vm.moveTo(location)

        icvm = iimaginary.IContainer(vm)
        icvm.closed = False
        theQuiche = quiche.createQuiche(store=self.store, name=u"quiche")
        icvm.add(theQuiche)
        icvm.closed = True

        for i in range(4):
            quarter = quiche.createCoin(store=self.store, name=u"quarter%s" % (i,))
            icvm.add(quarter)

        quarter = quiche.createCoin(store=self.store, name=u"quarter4")
        icvm.add(quarter)

        self.failUnless(icloc.contains(theQuiche))

