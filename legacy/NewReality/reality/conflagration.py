# -*- test-case-name: reality.test_reality -*-
from twisted.python import components 

from reality import things, actions
from reality.text import english

IExtinguishActor = things.IThing
class Extinguish(actions.TargetAction):

    def formatToActor(self):
        return "You blow out ",self.target,"."

    def formatToOther(self):
        return self.actor," blows out ",self.target,"."

    def doAction(self):
        self.target.unlight()
        
class FireParser(english.Subparser):
    simpleTargetParsers = {"blow": Extinguish}

english.registerSubparser(FireParser())

class Candle(components.Adapter):
    __implements__ = IExtinguishTarget
    lit = 0
    def light(self):
        self.lit = 1                
        n = self.getComponent(english.INoun)
        #n.changeName(n.name + " (providing light)")
        n.describe(self, "It is lit.")
        
    def unlight(self):
        self.lit = 0
        n = self.getComponent(english.INoun)
        #n.changeName(n.name[:-18])
        n.describe(self, '')
