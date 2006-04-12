# -*- test-case-name: reality.test_reality -*-

"""
UNTESTED!! THIS CODE IS JUST IDEAS, IT DOES NOT WORK YET
"""


import actions
import phrase
from twisted.python import components

class IPressTarget(components.Interface):
    def pressed(self):
        """The gadget has been pressed.

        @returns: a formattable tuple which will be appended both to the
        message the actor sees and the message everyone else sees.
        """

    def buttonName(self, observer):
        """The name of this thing as a button.

        Many structures that can be manipulated as `buttons' are actually
        something else with a single large button on them.  For example: a
        water fountain with a button on it to make the water flow, a trigger on
        a gun, the switch on a lantern, (or the button on a phaser), the front
        of a dispenser.  This allows you to format a different name for your
        object, e.g. \"the lantern's switch\", rather than having every
        potentially pressable object be a full constellation of different,
        discrete Things.

        @returns: formattable object (string, tuple, etc).
        """

class Press(actions.TargetAction):
    """This is a basic action which can be used for pressable/pressable buttons
    and levers.
    """
    def __init__(self, *a,**k):
        actions.TargetAction.__init__(self,*a,**k)
        self.actorMessage = ("You press ",self.target.buttonName,". ")
        self.otherMessage = (self.actor," presses ",self.target.buttonName,". ")
        
    def doAction(self):
        message = self.target.pressed(self)
        self.actorMessage += message,
        self.otherMessage += message,


class Pull(actions.TargetAction):
    """This is a basic action which can be used for pressable/pressable buttons
    and levers.
    """
    def __init__(self, *a,**k):
        actions.TargetAction.__init__(self,*a,**k)
        self.actorMessage = ("You pull on ",self.target,". ")
        self.otherMessage = (self.actor," pulls on ",self.target,". ")

    def doAction(self):
        message = self.target.pressed(self)
        self.actorMessage += message,
        self.otherMessage += message,

class Activate(actions.TargetAction):
    """This is a basic action that can be used for switches that can be turned
    on and off.
    """
    def __init__(self, *a,**k):
        actions.TargetAction.__init__(self,*a,**k)
        self.actorMessage = ("You turn on ",self.target,". ")
        self.otherMessage = (self.actor," turns on ",self.target,". ")

    def doAction(self):
        message = self.target.activated(self)
        self.actorMessage += message,
        self.otherMessage += message,


class Deactivate(actions.TargetAction):
    """This is a basic action that can be used for switches that can be turned
    on and off.
    """
    def __init__(self, *a,**k):
        actions.TargetAction.__init__(self,*a,**k)
        self.actorMessage = ("You turn off ",self.target,". ")
        self.otherMessage = (self.actor," turns off ",self.target,". ")

    def doAction(self):
        message = self.target.activated(self)
        self.actorMessage += message,
        self.otherMessage += message,


class Toggle(components.Adapter):
    __implements__ = IPressTarget, IPullTarget, IActivateTarget, IDeactivateTarget

    pressable = True
    pullable = True
    switchable = True

    def pressed(self, action):
        return "Nothing happens"
    def pulled(self, action):
        return "Nothing happens"
    def activated(self, action):
        return "Nothing happens"

class ButtonsSubparser(phrase.Subparser):
    simpleTargetParsers = {"push": Press,
                           "press": Press,
                           "hit": Press,
                           "pull": Pull}
