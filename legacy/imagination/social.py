from zope.interface import implements
from imagination.simulacrum import IHearer
from imagination.event import broadcastEvent
from imagination.actions import NoTargetAction
from imagination.text import english
from imagination.facets import Facet

class Say(NoTargetAction):
    def __init__(self, actor, speech):
        NoTargetAction.__init__(self, actor)
        self.speech = speech

    def doAction(self):
        broadcastEvent(self.actor,
                       ('You say, "', self.speech, '"'),
                       (self.actor, ' says, "', self.speech, '"'),
                       iface=IHearer)

class SocialParser(english.Subparser):

    def parse_say(self, player, text):
        return [Say(player, text)]

english.registerSubparser(SocialParser())

class Speaker(Facet):
    implements(ISayActor)
