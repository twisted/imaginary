# -*- test-case-name: imaginary.test.test_vending -*-

from twisted import plugin

from imaginary import action
from imaginary import quiche


quichePlugin = action.ObjectPluginHelper('quiche', quiche.createQuiche)
vendingPlugin = action.ObjectPluginHelper('vending machine', quiche.createVendingMachine)
quarterPlugin = action.ObjectPluginHelper('quarter', quiche.createCoin)

