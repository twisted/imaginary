# -*- test-case-name: pottery.test.test_vending -*-
from zope.interface import implements

from twisted import plugin

from pottery.ipottery import IObjectType
from pottery import quiche


class _ObjectPluginHelper(object):
    implements(plugin.IPlugin, IObjectType)

    def __init__(self, typeName, typeObject):
        self.type = typeName
        self.typeObject = typeObject

    def getType(self):
        return self.typeObject

quichePlugin = _ObjectPluginHelper('quiche', quiche.Quiche)
vendingPlugin = _ObjectPluginHelper('vending machine', quiche.VendingMachine)
quarterPlugin = _ObjectPluginHelper('quarter', quiche.Quarter)
