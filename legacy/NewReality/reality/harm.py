# -*- test-case-name: reality.test_reality -*- 
from twisted.python import components 
from reality import things, errors, actions, ambulation, raiment
from reality.text import english


IDamageActor = things.IThing
class Damage(actions.ToolAction):
    def formatToActor(self):
        with = ""
        if self.tool:
            with = " with ", self.tool
        return ("You hit ",self.target) + with + (".",)
    def formatToTarget(self):
        with = ""
        if self.tool:
            with = " with ", self.tool
        return (self.actor," hits you") + with + (".",)         
    def formatToOther(self):
        with = ""
        if self.tool:
            with = " with ", self.tool
        return (self.actor," hits ",self.target) + with + (".",)

    def doAction(self):
        amount = self.tool.getDamageAmount()
        self.target.damage(amount)

class Weapon(components.Adapter):
    __implements__ = IDamageTool,
    
    def getDamageAmount(self):
        return 10

class Damageable(components.Adapter):
    __implements__ = IDamageTarget

    def damage(self, amount):
        self.original.emitEvent("Ow! that hurt. You take %d points of damage."
                                % amount, intensity=1)

class Armor(raiment.Wearable):
    __implements__ = IDamageTarget,  raiment.IWearTarget, raiment.IUnwearTarget
    originalTarget = None
    armorCoefficient = 0.5
    def dress(self, wearer):
        originalTarget = wearer.getComponent(IDamageTarget)
        if originalTarget:            
            self.originalTarget = originalTarget
            wearer.original.setComponent(IDamageTarget, self)

    def undress(self, wearer):
        if self.originalTarget:
            wearer.setComponent(IDamageTarget, self.originalTarget)
            
    def damage(self, amount):
        self.original.emitEvent("Your armor cushions the blow.", intensity=2)
        if self.originalTarget:
            self.originalTarget.damage(amount * self.armorCoefficient)


class DamageableDoor(components.Adapter):
    __implements__ = ambulation.IOpened, IDamageTarget
    strength = 50
    def damage(self, amount):
        self.strength -= amount
        if self.strength <= 0:
            #XXX Indicate WHICH door
            self.original.emitEvent("The door shatters to pieces!")
            self.original.setAdapter(ambulation.IOpened, ambulation.OpenDoor)
            
    def isOpen(self):
        return 0

class HarmParser(english.Subparser):
    simpleToolParsers = {"hit":Damage}

english.registerSubparser(HarmParser())
components.registerAdapter(Damageable, things.Actor, IDamageTarget)
