# -*- test-case-name: examplegame.test.test_vending -*-

from imaginary.creation import CreationPluginHelper
from examplegame.quiche import createQuiche, createCoin, createVendingMachine

quichePlugin = CreationPluginHelper('quiche', createQuiche)
vendingPlugin = CreationPluginHelper('vending machine', createVendingMachine)
quarterPlugin = CreationPluginHelper('quarter', createCoin)

