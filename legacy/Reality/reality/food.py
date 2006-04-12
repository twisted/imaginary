# -*- test-case-name: reality.test_reality -*-

from actions import ToolAction
from phrase import registerSubparser, Subparser
from reality.thing import Thing
from reality import error
from twisted.python.components import Interface, implements, registerAdapter, Adapter

class Eat(ToolAction):
    def doAction(self):
        self.target.destroy()

class Inedible(Adapter):
    __implements__ = IEatTarget
    temporaryAdapter = 1
    def preTargetEat(self, action):
        error.Failure(self.original, " is clearly not edible.")

class EatingVerbs(Subparser):
    simpleToolParsers = {"eat": Eat}

registerAdapter(Inedible, Thing, IEatTarget)
registerSubparser(EatingVerbs())
