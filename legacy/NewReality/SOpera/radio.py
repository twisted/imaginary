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
from Reality import thing, container
from Reality.phrase import Subparser, registerSubparser
from Reality.beyondspike import TargetAction, codeInterfaceForAction

# Twisted imports
from twisted.python.components import Adapter, Interface, registerAdapter

class Tune(TargetAction):
    pass
exec codeInterfaceForAction(Tune)


class Untuneable(Adapter):
    __implements__ = (ITuneTarget,)
    
    def targetActionTune(self, actor):
        actor.hears(self.original, " can not be tuned.")

registerAdapter(Untuneable, thing.Thing, ITuneTarget)

class Radio(space.Located, electronic.Electronic):
    __implements__ = (
        space.Located.__implements__,
        electronic.Electronic.__implements__,
        ITuneTarget,
        ISayActor
    )

    __all = {}
    __count = 0

    LOW, HIGH, INCR = 100, 100000, 10
    frequency = 100

    def __init__(self):
        self.synonyms = self.synonyms + (('#%d' % self.__count),)
        self.__count = self.__count + 1
        self.setFrequency(self.LOW)


    def __setstate__(self, state):
        self.__dict__ = state
        self.setFrequency(self.frequency)


    def tune(self, freq):
        if self.__all.has_key(freq):
            try:
                self.__all[freq].remove(self)
            except ValueError, e:
                pass
        if not self.__all.has_key(freq):
            self.__all[freq] = [self]
        else:
            self.__all[freq].append(self)
        self.frequency = freq

    def action_tune(self, tuner, frequency):
        tuner.broadcastToOne(
            to_subject = ('You fiddle with ', self, '.'),
            to_other = (tuner, ' fiddles with ', self, '.')
        )

        if self.LOW <= x <= self.HIGH and x % self.INCR == 0:
            self.tune(x)
            sentence.subject.hears('You tune ', self, ' to %dkHz.' % x)
        else:
            sentence.subject.hears('Radios can only be tuned in the range of %dkHz through %dkHz in increments of %dkHz.' % (self.LOW, self.HIGH, self.INCR))

    def verb_tune(self, sentence):
        self.verb_tune.__doc__ = """tune <radio> to <frequency>
        
        Changes the tranceiver frequency of the specified radio.  Frequency
        ranges are from %dkHz to %dkHz in %dkHz increments.  All radios on a
        particular frequency can here the transmissions of all other radios on
        that frequency.""" % (self.LOW, self.HIGH, self.INCR)

        try:
            to = sentence.indirectString('to')
            self.action_tune(sentence.subject, int(to))
        except ValueError:
            sentence.subject.hears("%s isn't a valid frequency." % to)

    def receiveComm(self, sender, message):
        self.location.hears('From ', self, ' you hear, "', message, '"')

    def sendComm(self, sender, message):
        for i in self.__all[self.frequency]:
            if i is not self:
                i.receiveComm(sender, message)

    def action_comm(self, sender, message):
        self.sendComm(sender, message)

    def verb_comm_into(self, sentence):
        msg = sentence.directString()
        self.action_comm(sentence.subject, msg)


registerAdapter(electronic.Electronic, Radio, IActivateTarget)
registerAdapter(electronic.Electronic, Radio, IDectivateTarget)

