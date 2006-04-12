# -*- test-case-name: reality.test_reality -*- 
from twisted.python import components 

from reality import things, actions
from reality.text import english

IPlayWindInstrumentActor = things.IThing
class PlayWindInstrument(actions.TargetAction):
    def formatToActor(self):
        return ("You play ",self.target.instrumentSound(),
                " upon ",self.target,".")
    def formatToOthers(self):
        return (self.actor, " plays ",self.target.instrumentSound(),
                " upon ",self.target, ".")
    def doAction(self):
        self.target.playInstrument()

class MusicParser(english.Subparser):
    def parse_blow(self, player, text):
        actor = player.getComponent(IPlayWindInstrumentActor)
        if actor is None:
            return []
        return [PlayWindInstrument(actor, text)]

english.registerSubparser(MusicParser())

class Whistle(components.Adapter):
    __implements__ = IPlayWindInstrumentTarget

    def instrumentSound(self):
        return "a shrill blast"
    
    def playInstrument(self):
        "This whistle is boring and doesn't do anything but make noise"
