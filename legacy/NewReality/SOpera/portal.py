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

# Twisted imports
from twisted.python.components import Interface

# Reality imports
from Reality import thing
from Reality.beyondspike import TargetAction, codeInterfaceForAction
from Reality.phrase import registerAdapter, registerSubparser, Subparser


class IEnterTarget(Interface):
    """Interface for things that can be entered."""
    def targetActionEnter(self, actor):
        """The actor is trying to enter the target."""


class Enter(TargetAction):
    pass
exec codeInterfaceForAction(Enter)

class Unenterable:
    __implements__ = (IEnterTarget,)
    temporaryAdapter = 1
    
    def __init__(self, target):
        self.target = target

    def targetActionEnter(self, actor):
        actor.hears("You cannot enter ", self.target, ".");

registerAdapter(Unenterable, thing.Thing, IEnterTarget)

class Portal:
    """
    A thing which can be entered and which will transport
    the actor to a destination that may or may not be
    adjacent to their stating position in Euclidean Space.
    This is one way.
    """

    __implements__ = (IEnterTarget,)
    
    destination = None

    def __init__(self, destination):
        self.destination = destination

    def targetActionEnter(self, actor):
        self.action_enter(actor)

    def action_enter(self, actor):
        actor.broadcastToOne(
            to_subject = ("You enter ", self, "."),
            to_other = (actor, " enters ", self, ".")
        )
        actor.location = self.destination
        actor.broadcastToOne(
            to_subject = (),
            to_other = (actor, " arrives  ", self, ".")
        )

class PortalParser(Subparser):
    simpleTargetParsers = {'enter': Enter}

registerSubparser(PortalParser())
