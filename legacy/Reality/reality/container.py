# -*- test-case-name: reality.test_reality -*-

# Twisted, the Framework of Your Internet
# Copyright (C) 2001 Matthew W. Lefkowitz
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of version 2.1 of the GNU Lesser General Public
# License as published by the Free Software Foundation.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import new

import thing, error
from player import ITakeTarget, ITakeActor, Take
from phrase import registerSubparser, Subparser, Parsing, IParsing
from twisted.python.components import Interface, registerAdapter, implements, Adapter
from twisted.python import log
from twisted.persisted.styles import Versioned

import actions

class IOpenTarget(actions.TargetAction):
    def open(self):
        """You guessed it.
        """

class ICloseTarget(actions.TargetAction):
    def close(self):
        """That's right.
        """

class IPutTarget(Interface):
    def receivePut(self, obj, how):
        """Accept a target.

        @param obj: the object being moved
        @param how: a string of the preposition of where it is being moved
                    ('in', 'on', etc.)
        """

class Open(actions.TargetAction):
    def doAction(self):
        """
        Open an object.
        """
        self.target.open()
        self.actorMessage = "You opened ", self.target,"."
        self.otherMessage = self.actor," opened ", self.target,"."

class Close(actions.TargetAction):
    def doAction(self):
        """
        Close an object.
        """
        self.target.close()
        self.actorMessage = "You closed ", self.target,"."
        self.otherMessage = self.actor," closed ", self.target,"."

# Probably not such a good idea...
# actions.unify(Open, Close)

class Put(actions.TargetAction):
    def __init__(self, actor, item, container, preposition):
        actions.TargetAction.__init__(self, actor, container)
        self.item = item
        self.preposition = preposition
        self.actorMessage = "You put ",self.item," ",self.preposition," ",self.target,"."
        self.otherMessage = self.actor,' puts ',self.item,' ',self.preposition,' ',self.target,'.'

    def preAction(self):
        sub = self.actor.getComponent(thing.IThing)
        it = self.item.getComponent(thing.IThing)
        if it.location != sub:
            ta = Take(sub.getComponent(ITakeActor),
                      self.item, None)
            ta.actorMessage = ("[taking ",it," first: ")+ta.actorMessage+(']',)
            ta.performAction()
        actions.TargetAction.preAction(self)

    def doAction(self):
        sub = self.actor.getComponent(thing.IThing)
        it = self.item.getComponent(thing.IThing)
        targ = self.target.getComponent(thing.IThing)
        prep = self.preposition
        if it is targ:
            print self.item
            print self.target
            raise error.Already("Some would say it's already there. Anyway, you cant do that.")
        self.target.receivePut(it, self.preposition)

class NonContainer(Adapter):
    __implements__ = IPutTarget,
    temporaryAdapter = True
    def preTargetPut(self, action):
        error.Failure(self.original, " is not something you can put stuff in or on.")

class ContainerVerbs(Subparser):
    def parse_put(self, player, text):
        # TODO: support for tools
        args = text.split()
        for prep in 'in', 'on':
            try:
                i = args.index(prep)
                break
            except ValueError:
                pass
        else:
            raise error.Nonsense
        stuff = player.lookAroundFor(' '.join(args[:i]), ITakeTarget)
        containers = player.lookAroundFor(' '.join(args[i+1:]), IPutTarget)
        actions = []
        for thingy in stuff:
            for container in containers:
                actions.append(Put(player, thingy, container, prep))
        return actions

    simpleTargetParsers = {'open': Open,
                           'close': Close}

class _Contents(thing.Thing):
    "Bookkeeping class for the contents of boxes."
    surface = 0
    def containedPhrase(self, observer, other):
        "calls back up one level."
        return self.location.containedPhrase(observer, other)

class ContainerAdapter(Adapter):
    __implements__ = IPutTarget
    def receivePut(self, it, how):
        it.location = self.original


class OpenableContainer(ContainerAdapter):
    """Boxy, but good.
    """
    __implements__ = IOpenTarget, ICloseTarget, IPutTarget

    def __init__(self, original):
        ContainerAdapter.__init__(self, original)
        t = self.getComponent(thing.IThing)
        self.closedDesc = "It's closed."
        self.openDesc = "It's open."
        t.description = {'open/close': self.closedDesc}
        t.hollow = 1
        self.isOpen = 0
        self.contents = _Contents("$"+t.name + "'s contents")
        self.contents.location = t
        self.contents.component = 1

    def receivePut(self, it, how):
        it.location = self.contents

    def open(self):
        if self.isOpen:
            error.Already("It's already open.")
        self.isOpen = 1
        self.contents.surface = 1
        self.description = {'open/close': self.openDesc}

    def close(self):
        if not self.isOpen:
            error.Already("It's already closed.")
        self.isOpen = 0
        self.contents.surface = 0
        self.description = {'open/close': self.closedDesc}

## Backwards compatibility classes

def _cgs(self):
    """container getstate"""
    return Versioned.__getstate__(self, thing.Thing.__getstate__(self))

class Container(thing.Thing, Versioned):
    """
    Obsoleted convenience class from the Bad Old Days of subclassing, setting a
    few defaults for objects intended to be containers.
    """
    hollow = 1
    persistenceVersion = 3

    def __init__(self, name, reality=''):
        thing.Thing.__init__(self, name, reality)

    def __call__(self, **kw):
        thing.Thing.__call__(self,**kw)
        self.upgradeToVersion2()
        self.upgradeToVersion3()

    def upgradeToVersion3(self):
        self.__class__ = thing.Thing
    
    def upgradeToVersion2(self):
        self.addAdapter(ContainerAdapter, 1)

    __getstate__ = _cgs


class Box(thing.Thing, Versioned):
    """Obsoleted Box class from the Bad Old Days of subclassing.
    """
    persistenceVersion = 3

    def upgradeToVersion3(self):
        self.__class__ = thing.Thing

    def upgradeToVersion2(self):
        ba = OpenableContainer(self)
        for att, defl in [["isOpen", 1],
                          ["contents", None],
                          ["openDesc", (self, "is open")],
                          ["closedDesc", (self, "is closed")]]:
            if self.__dict__.has_key(att):
                setattr(ba, att, getattr(self, att))
                delattr(self, att)
        ba.original = self
        self.addComponent(ba, 1)

    __getstate__ = _cgs

# Adapter registration
registerAdapter(NonContainer, thing.Thing, IPutTarget)
registerSubparser(ContainerVerbs())
