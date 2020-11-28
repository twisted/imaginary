
from twisted.trial import unittest

from imaginary import objects, iimaginary
from imaginary.test import commandutils

from examplegame import quiche


class VendingTest(commandutils.CommandTestCaseMixin, unittest.TestCase):
    def _create(self):
        """
        Create the vending machine.
        """
        self._test("create the 'vending machine' named vendy A vending machine.",
                   ["You create vendy."],
                   ["Test Player creates vendy."],
        )


    def _drop(self):
        self._test(
            "drop vendy",
            ["You drop vendy."],
            ["Test Player drops vendy."],
        )


    def _open(self):
        """
        Open the vending machine.
        """
        self._test("open vendy",
                   ["You open vendy."],
                   ["Test Player opens vendy."],
        )


    def _close(self):
        """
        Close the vending machine.
        """
        self._test("close vendy",
                   ["You close vendy."],
                   ["Test Player closes vendy."],
        )


    def _create_quiche(self):
        self._test("create a quiche named quiche",
                   ["You create a quiche."],
                   ["Test Player creates a quiche."])


    def _put_quiche(self):
        self._test("put quiche in vendy",
                   ["You put the quiche in vendy."],
                   ["Test Player puts a quiche in vendy."])



    def testTheyExist(self):
        self._create()


    def testPopulateVendingMachine(self):
        self._create()
        self._open()
        self._create_quiche()
        self._put_quiche()


    def testClosedDescription(self):
        """
        The contents of a vending machine are not visible when the vending machine
        is closed.
        """
        self._create()
        self._open()
        self._create_quiche()
        self._put_quiche()
        self._close()
        self._test(
            "look at vendy",
            [commandutils.E("[ vendy ]"),
             "A vending machine.",
             "",
            ],
            [],
        )

    def closedEmptyDescription(self):
        """
        The fact that a vending machine is empty is not visible when the vending
        machine is closed.
        """
        self._create()
        self._test(
            "look at vendy",
            [commandutils.E("[ vendy ]"),
             "A vending machine.",
             "",
            ],
            [],
        )


    def testOpenDescription(self):
        """
        When the vending machine is open its contents are visible.
        """
        self._create()
        self._drop()
        self._open()
        self._create_quiche()
        self._put_quiche()
        self._test(
            "look at vendy",
            [commandutils.E("[ vendy ]"),
             "A vending machine.",
             "It contains a quiche.",
             "",
            ],
            [],
        )


    def testOpenEmptyDescription(self):
        """
        When the vending machine is open the fact that it is empty is visible.
        """
        self._create()
        self._drop()
        self._open()
        self._test(
            "look at vendy",
            [commandutils.E("[ vendy ]"),
             "A vending machine.",
             "",
            ],
            [],
        )


    def _create_quarter(self, name):
        self._test(
            "create the quarter named %s" % (name,),
            ["You create %s." % (name,)],
            ["Test Player creates %s." % (name,)],
        )


    def _put_quarter(self, name):
        self._test("put %s in vendy" % (name,),
                   ["You put %s in vendy." % (name,)],
                   ["Test Player puts %s in vendy." % (name,)])


    def testBuyingQuiche(self):
        self._create()
        self._drop()
        self._create_quiche()
        self._open()
        self._put_quiche()

        for i in range(5):
            self._create_quarter("quarter%i" % (i,))

        for i in range(4):
            self._put_quarter("quarter%i" % (i,))

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
