# -*- test-case-name: reality.test_reality -*-

"""
Things that can be carried, picked up, put down, things that can be put in
other things, on other things, beneath other things, next to other things and
behind other things.
"""

from twisted.python import components 

from reality import things
from reality import errors
from reality import actions
from reality.text import english

class Take(actions.ToolAction, things.MovementEvent):

    #def broadcastFormat(self):
    #    """No-op because this is broadcast by moveTo.
    #    """

    def formatToActor(self):
        return "You take ",self.target,"."
    def formatToOther(self):
        return self.actor, " takes ", self.target,"."
    def doAction(self):
        t = self.target.getComponent(things.IThing)
        a = self.actor.getComponent(things.IThing)
        if t.location.getItem() == a:
            raise errors.ActionFailed("You were already holding ",t)
        t.moveTo(a, self)


class DropAll(actions.NoTargetAction, things.MovementEvent):
    def doAction(self):
        for t in self.actor.get_things():
            Drop(self.actor, t.getComponent(IDropTarget))
                
class Drop(actions.TargetAction, things.MovementEvent):
    def formatToActor(self):
        return "You drop ",self.target,"."

    def doAction(self):
        """Place an object currently in this player into the Room which
        contains them.
        """
        t = self.target.getComponent(things.IThing)
        a = self.actor.getComponent(things.IThing)
        loc = a.location.getItem()
        if t.location.getItem() == a:
            t.moveTo(loc)
        else:
            raise errors.ActionFailed("You weren't holding that.")

class Portable(components.Adapter):
    __implements__ = ITakeTarget, IDropTarget
    def __init__(self, original, weight = 1, bulk = 1):
        components.Adapter.__init__(self, original)
        self.weight = weight
        self.bulk = bulk

    def moveTo(self, container, event=None):
        return self.original.moveTo(container, event=None)


class CarryVerbs(english.Subparser):

    def parse_drop(self, player, text):
        # things = player.lookFor(text, IDropTarget)
        actor = player.getComponent(IDropActor)
        if not actor:
            return []
        if not things and text == "all":
            # XXX NOT WORKING
            return DropAll(actor),
        else:
            return [Drop(actor, text)]

    simpleToolParsers = {"take": Take,
                         "get": Take}

class PackMule(components.Adapter):
    __implements__ = ITakeActor, IDropActor, IDropAllActor

english.registerSubparser(CarryVerbs())
components.registerAdapter(PackMule, things.Thing, ITakeActor)
components.registerAdapter(PackMule, things.Thing, IDropActor)
components.registerAdapter(PackMule, things.Thing, IDropAllActor)
