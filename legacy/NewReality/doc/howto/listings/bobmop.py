
from twisted.python import components
from reality.actions import TargetAction
from reality.things import Actor

class BobsFunkyDance(TargetAction):
    def formatToActor(self):
        return "You get down with ",self.target

    def formatToOther(self):
        return self.actor, "gets down with ",self.target

class BobsFunkyDancer(components.Adapter):
    """An adapter which represents the ability to dance with a mop.
    """

    __implements__ = IBobsFunkyDanceActor

components.registerAdapter(BobsFunkyDancer, Actor, IBobsFunkyDanceActor)

class BobsFunkyMop(components.Adapter):
    """An adapter which makes an object into a danceable mop.
    """

    __implements__ = IBobsFunkyDanceTarget

