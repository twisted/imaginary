# -*- test-case-name: reality.test_reality -*-

from reality import things
from reality import actions

from twisted.python import components

_opposites = [
    ("north", "south"),
    ("in", "out"),
    ("east", "west"),
    ("northeast", "southwest"),
    ("northwest", "southeast"),
    ("up", "down"),
    ("left", "right"),
    ("forward", "backward"),
    ("starboard", "port")
    ]

def opposite(term):
    for a, b in _opposites:
        if term == a:
            return b
        if term == b:
            return a
    raise KeyError(term+" has no opposite")

def isOpposite(term1,term2):
    for a, b in _opposites:
        if term1 == a and term2 == b:
            return 1
        if term2 == a and term1 == b:
            return 1
    return 0


class Exit(things.Thing):
    def __init__(self, store, name, direction, source, destination, twoway=True,
                 reverseName=None):
        things.Thing.__init__(self, store, name)
        self.direction = direction
        self.source = source.referenceTo()
        self.destination = destination.referenceTo()
        self.twoway = twoway
        self.reverseName = reverseName
        # link up the exit
        assert destination.getComponent(IWalkTarget)
        assert source.getComponent(IWalkTarget)
        source.link(self)
        self.link(source)
        if twoway:
            destination.link(self)
            self.link(destination)
        self.forwardedInterfaces = []

    classForwardedInterfaces = []

    def classForwardInterface(self, iface):
        self.classForwardedInterfaces.append(iface)

    classForwardInterface = classmethod(classForwardInterface)

    def forwardedInterface(self, iface):
        self.forwardedInterfaces.append(iface)
        
    def collectImplementors(self, asker, iface, collection, seen, event=None, name=None, intensity=2):
        if not intensity:
            return collection
        seen[self.storeID] = None
        newIntensity = intensity - self.intensityBarrier
        if isinstance(asker, things.Movable):
            subCollection = {}
            self.collectMe(asker, iface, collection, name=name, event=event)
            if asker.location == self.source:
                if iface == IWalkTarget:                    
                    if name == self.direction:
                        dest = self.destination.getItem()
                        collection[self] = dest.getComponent(IWalkTarget)
                else:
                    dest = self.destination.getItem()
                    dest.collectImplementors(asker, iface, subCollection, seen, event=event, name=name, intensity=newIntensity)
            elif (asker.location == self.destination) and self.twoway:
                if iface == IWalkTarget:
                    if name == self.reverseName or isOpposite(name, self.direction):
                        collection[self] = self.source.getItem().getComponent(IWalkTarget)
                else:
                    self.source.getItem().collectImplementors(asker, iface, subCollection, seen, event=event, name=name, intensity=newIntensity)
            if iface in self.classForwardedInterfaces + self.forwardedInterfaces:
                collection.update(subCollection)
            elif name is not None:
                for k, v in subCollection.iteritems():
                    collection[k] = things.Refusal(v,(v," is too far away."))
        else:
            things.Thing.collectImplementors(self, asker, iface, collection, seen, event=event, name=name, intensity=intensity)
        return collection

class IOpened(components.Interface):
    def isOpen(self):
        """Is this thing open?
        """

class Door(Exit):
    def collectImplementors(self, asker, iface, collection, seen, event=None, name=None, intensity=2):
        op = IOpened(self).isOpen()
        if op or asker is self:
            Exit.collectImplementors(self, asker, iface, collection, seen, event=None, name=name, intensity=intensity)
        else:
            self.collectMe(asker, iface, collection, name=name, event=event)
        return collection


class OpenDoor(components.Adapter):
    __implements__ = IOpened
    def isOpen(self):
        return 1

## class Twiddler(components.Adapter):
##     temporaryAdapter = True
##     __implements__ = IOpenActor, ICloseActor

## components.registerAdapter(Twiddler, things.Movable, IOpenActor)
components.registerAdapter(OpenDoor, Door, IOpened)

import actions

class Walk(actions.TargetAction, things.MovementEvent):
    def broadcastFormat(self):
        """No-op since this Walk event is broadcast by moveTo.
        """
    
    def doAction(self):
        self.actor.walkTo(self.target, self)

    def whyCantFind(self, iType, iName):
        return "You can't go %s from here." % iName

class Walker(components.Adapter):
    __implements__ = IWalkActor

    def walkTo(self, target, event=None):
        self.original.moveTo(target.getComponent(things.IThing), event)

components.registerAdapter(Walker, things.Movable, IWalkActor)

class Room(things.Thing):
    # will probably be a Pool, eventually
    __implements__ = things.Thing.__implements__, IWalkTarget
    intensityBarrier = 0

from reality.text import english

class WalkParser(english.Subparser):
    simpleTargetParsers = {
        "go": Walk,
        "walk": Walk
        }


def walkAbbrev(abbrev, direction):
    def parsefun(self, actor, text):
        if not text:
            return [Walk(actor, direction)]
        return []
    setattr(WalkParser, "parse_"+abbrev, parsefun)

for a,d in (("n", "north"),
          ("ne", "northeast"),
          ("e", "east"),
          ("se", "southeast"),
          ("s", "south"),
          ("sw", "southwest"),
          ("w", "west"),
          ("nw", "northwest")):
    walkAbbrev(a, d)

english.registerSubparser(WalkParser())

