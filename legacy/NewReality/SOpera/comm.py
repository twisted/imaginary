# Space Opera - A Multiplayer Science Fiction Game Engine
# Copyright (C) 2002 Jean-Paul Calderone
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	 See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
#

# Reality imports
from Reality.beyondspike import NoTargetAction, TargetAction
from Reality.phrase import registerSubparser, Subparser, Parsing, IParsing
from Reality.thing import Thing

# Twisted imports
from twisted.python.components import Interface, implements, registerAdapter

# Sibling imports
import sopera

class ISayActor(Interface):
    def actorActionSay(self, text):
        pass

class IWhisperActor(Interface):
    def actorActionWhisper(self, target, text):
        pass

class IHollerActor(Interface):
    def actorActionHoller(self, text):
        pass

class Speaker:
    __implements__ = (ISayActor, IWhisperActor, IHollerActor)

    def __init__(self, original):
        self.original = original

    def actorActionSay(self, text):
        subject = 'You say, "', text, '"'
        other = self.original, ' says, "', text, '"'
        self.original.broadcastToOne(
            to_subject = subject,
            to_other = other
        )

    def actorActionWhisper(self, target, text):
        if target is self.original:
            self.original.hears('Talking to yourself again, I see.')
            return

        t = self.original, ' whispers to you, "', text, '"'
        s = 'You whisper to ', target, ', "', text, '"'
        o = self.original, ' whispers to ', target, '.'
        self.original.broadcastToPair(
            target = target,
            to_target = t,
            to_subject = s,
            to_other = o
        )

    def actorActionHoller(self, text):
        pass

registerAdapter(Speaker, sopera.Player, ISayActor)
registerAdapter(Speaker, sopera.Player, IWhisperActor)

class Say(NoTargetAction):
    def __init__(self, actor, speech):
        NoTargetAction.__init__(self, actor)
        self.speech = speech

    def getDispatchList(self):
        return [
            [ISayActor, self.actor, 'actorActionSay', (self.speech,), {}]
        ]

class Whisper(TargetAction):
    def __init__(self, actor, target, speech):
        TargetAction.__init__(self, actor, target)
        self.speech = speech

    def getDispatchList(self):
        return [
            [IWhisperActor, self.actor, 'actorActionWhisper', (self.target, self.speech), {}]
        ]
        
class CommVerbs(Subparser):
    def parse_say(self, player, text):
        return [Say(player, text)]

    def parse_whisper(self, player, text):
        i = text.rfind(' to ')
        if i != -1:
            t = text[i + 4:]
            target = player.locate(t)
            return [Whisper(player, target, text[:i])]

registerSubparser(CommVerbs())
