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

# reality imports
from reality import thing, container
from actions import TargetAction
from reality.simple import IEatTarget
from reality.phrase import Subparser, registerSubparser

# Twisted imports
from twisted.python.components import Interface, registerAdapter, Adapter

class Activate(TargetAction):
    def __init__(self, *args):
        TargetAction.__init__(self,*args)
        self.actorMessage = ('You fiddle with ', self.target, '.')
        self.otherMessage = (actor, ' fiddles with ', self, '.')
    def doAction(self):
        if self.__broken:
            raise error.Failure(self.brokenPhrase)
        else:
            self.turnOn()


class Deactivate(TargetAction):
    pass

class Unactivateable:
    __implements__ = (IActivateTarget, IDeactivateTarget)
    temporaryAdapter = True
    def __init__(self, target):
        self.target = target

    def targetActionActivate(self, actor):
        actor.hears(self.target, " can not be activated.")

    def targetActionDeactivate(self, actor):
        actor.hears(self.target, " can not be deactivated.")

registerAdapter(Unactivateable, thing.Thing, IActivateTarget)
registerAdapter(Unactivateable, thing.Thing, IDeactivateTarget)

class Electronic(Adapter):
    """
    Something that can be turned on or off, activated, or become broken.
    """

    # Whether this is on or off
    __state = 0

    # Whether this thing still works or not
    __broken = 0

    # What the user is shown when they try to activate this if it
    # is already activated.
    alreadyOnPhrase = None

    # As above, but for the deactivated state.
    alreadyOffPhrase = None

    # What the user is shown if they try to activate/deactivate
    # but the thing is broken.
    brokenPhrase = None

    # What the user is shown when the thing is successfully
    # activated/deactivated
    onPhrase = None
    offPhrase = None

    __implements__ = (IActivateTarget, IDeactivateTarget)

    def __init__(self, original):
        Adapter.__init__(self, original)
        self.alreadyOnPhrase = self, ' is already on.'
        self.alreadyOffPhrase = self, ' is already off.'
        self.onPhrase = self, ' hums as it powers up.'
        self.offPhrase = self, ' grows silent as it powers down.'
        self.brokenPhrase = self, ' appears to be broken.'


    def turnOn(self):
        """
        Invoked when this thing is successfully activated.
        """
        if self.__state == 1:
            raise error.Failure(self.alreadyOnPhrase)
        self.broadcast(self.onPhrase)
        self.__state = 1




    def turnOff(self):
        """
        Invoked when this thing is successfully deactivated.
        """
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

class ActivationParser(Subparser):
    simpleTargetParsers = {'activate': Activate, 'deactivate': Deactivate}

registerSubparser(ActivationParser())
