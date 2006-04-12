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
from Reality.beyondspike import TargetAction, codeInterfaceForAction
from Reality.simple import IEatTarget
from Reality.phrase import  Subparser

# Twisted imports
from twisted.python.components import Interface, registerAdapter

class IActivateTarget(Interface):
    """Interface for things that can be activated/deactivated."""
    def targetActionActivate(self, actor):
        """The actor has tried to activate the target."""
    def targetActionDeactivate(self, actor):
        """The actor has tried to activate the target."""


class Activate(TargetAction):
    pass
exec codeInterfaceForAction(Activate)

class Deactivate(TargetAction):
    pass
exec codeInterfaceForAction(Deactivate)


class Unactivateable:
    __implements__ = (IActivateTarget,)
    def __init__(self, target):
        self.target = target

    def targetActionActivate(self, actor):
        actor.hears(self.target, " can not be activated.")

    def targetActionDeactivate(self, actor):
        actor.hears(self.target, " can not be deactivated.")

registerAdapter(Unactivateable, thing.Thing, IActivateTarget)

class ActivationParser(Subparser):
    simpleTargetParsers = {'activate': Activate, 'deactivate': Deactivate}


class Electronic:
    __state = 0
    __broken = 0

    alreadyOnPhrase = None
    alreadyOffPhrase = None
    
    brokenPhrase = None
    onPhrase = None
    offPhrase = None
    
    __implements__ = (thing.Thing.__implements__, IActivateTarget)

    def __init__(self, name, reality = ''):
        self.alreadyOnPhrase = self, ' is already on.'
        self.alreadyOffPhrase = self, ' is already off.'
        self.onPhrase = self, ' hums as it powers up.'
        self.offPhrase = self, ' grows silent as it powers down.'
        self.brokenPhrase = self, ' appears to be broken.'

    def turnOn(self):
        if self.__state == 1:
            raise error.Failure(self.alreadyOnPhrase)
        self.broadcast(self.onPhrase)
        self.__state = 1
    
    def action_activate(self, actor):
        actor.broadcastToOne(
            to_subject = ('You fiddle with ', self, '.'),
            to_other = (actor, ' fiddles with ', self, '.')
        )

        if self.__broken:
            raise error.Failure(self.brokenPhrase)
        else:
            self.turnOn()

    def targetActionActivate(self, actor):
        self.action_activate(actor)

    def turnOff(self):
        if self.__state == 0:
            raise error.Failure(self.alreadyOffPhrase)
        self.broadcast(self.offPhrase)
        self.__state = 0

    def action_deactivate(self, actor):
        actor.broadcastToOne(
            to_subject = ('You fiddle with ', self, '.'),
            to_other = (actor, ' fiddles with ', self, '.')
        )
            
        if self.__broken:
            raise error.Failure(self.brokenPhrase)
        else:
            self.turnOff()

    def targetActionDeactivate(self, actor):
        self.action_deactivate(actor)
