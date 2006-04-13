# -*- test-case-name: imaginary.test.test_vending -*-
from zope.interface import implements

from twisted import plugin

from imaginary.iimaginary import IThingType
from imaginary import quiche


class _ObjectPluginHelper(object):
    implements(plugin.IPlugin, IThingType)

    def __init__(self, typeName, typeObject):
        self.type = typeName
        self.typeObject = typeObject

    def getType(self):
        return self.typeObject

quichePlugin = _ObjectPluginHelper('quiche', quiche.createQuiche)
vendingPlugin = _ObjectPluginHelper('vending machine', quiche.createVendingMachine)
quarterPlugin = _ObjectPluginHelper('quarter', quiche.createCoin)

