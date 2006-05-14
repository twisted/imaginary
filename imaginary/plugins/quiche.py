# -*- test-case-name: imaginary.test.test_vending -*-
from zope.interface import implements

from twisted import plugin

from imaginary.iimaginary import IThingType
from imaginary import action
from imaginary import quiche


quichePlugin = action.ObjectPluginHelper('quiche', quiche.createQuiche)
vendingPlugin = action.ObjectPluginHelper('vending machine', quiche.createVendingMachine)
quarterPlugin = action.ObjectPluginHelper('quarter', quiche.createCoin)

