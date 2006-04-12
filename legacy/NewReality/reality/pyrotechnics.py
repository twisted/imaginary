# -*- test-case-name: reality.test_reality -*-
from twisted.python import components 
from reality import things, actions, harm
from reality.text import english

IBlowUpActor = things.IThing
IBlowUpTarget = harm.IDamageTarget
class BlowUp(actions.ToolAction):
    allowNoneInterfaceTypes = ['Place']
    def formatToActor(self):
        return "You fire ",self.tool,"  at ",self.target,"."
    
    def formatToOther(self):
        return self.actor," fires ",self.tool," at ",self.target,"."
    def doAction(self):
        self.tool.armed = 1
        #self.tool.original.moveTo(self.target.original.location)
        #XXX the above breaks when targeted at doors
        d = harm.Damage(self.actor, self.target, self.tool)
        d.target = self.target
        d.actor = self.actor
        d.tool = self.tool
        d.performAction()

class ExplosivesParser(english.Subparser):
    simpleToolParsers = {"blow": BlowUp}

english.registerSubparser(ExplosivesParser())

class Rocket(components.Adapter):
    __implements__ = IBlowUpTool, harm.IDamageTool
    armed = 0 

    def getDamageAmount(self):
        if self.armed:
            self.detonate()
            return 100        
        else:
            self.original.emitEvent("Thump!")
            return 1

    def detonate(self):
        self.original.emitEvent("*BOOM*!!")
        self.original.unlink(self.original.location)
        self.original.location.getItem().unlink(self.original)
