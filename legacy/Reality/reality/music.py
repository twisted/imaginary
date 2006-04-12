# -*- test-case-name: reality.test_reality -*-

# Twisted Imports
from twisted.python.components import Interface, implements

# Reality Imports
from reality.actions import NoTargetAction, TargetAction, ToolAction
from reality.phrase import registerSubparser, Subparser, Parsing, IParsing
from reality.thing import Thing

# TODO: implement songs (action targets for playInstrument)

class PlayInstrument(ToolAction):
    allowNoneInterfaceTypes = ["Target"]
    def doAction(self):
        self.tool.playInstrument(self)

class IWindInstrument(IPlayInstrumentTool):
    pass

class MusicParser(Subparser):
    def parse_blow(self, player, text):
        """Handles these cases:

        'blow whistle'
        'blow horn'
        """
        return [PlayInstrument(player, None, target) for target in 
                player.lookAroundFor(text, IWindInstrument)]

    simpleToolParsers = {"play": PlayInstrument}

registerSubparser(MusicParser())

class Flute(Thing):
    __implements__ = IWindInstrument, Thing.__implements__
    def playInstrument(self, action):
        action.actor.hears( 'POKEY I AM PLAYING THE FLUTE AND IT IS FUN' )
