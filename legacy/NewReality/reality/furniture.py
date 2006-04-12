# -*- test-case-name: reality.test_reality -*-
from twisted.python import components
from reality import actions, things
from reality.text import english

class Sit(actions.TargetAction, things.MovementEvent):
    def doAction(self):
        self.actor.sit(self.target, self)

class SitParser(english.Subparser):
    simpleTargetParsers = {
        "sit": Sit,
        }
english.registerSubparser(SitParser())

# XXX TODO WARNING DANGER !!!
# this blows, big time. If you sit in the chair, you disappear.

class Chair(components.Adapter):
    __implements__ = ISitTarget,

class Sitter(components.Adapter):
    __implements__ = ISitActor

    def sit(self, sittable, event=None):
        self.original.moveTo(things.IThing(sittable), event)

components.registerAdapter(Sitter, things.Actor, ISitActor)
