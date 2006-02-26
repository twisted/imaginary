# -*- test-case-name: imagination.test -*-

from zope.interface import Interface, Attribute, implements

from imagination.simulacrum import ICollector, ICallableCriterion, always
from imagination import actions, errors, facets
from imagination.text import english
from imagination.event import broadcastEvent

__metaclass__ = type

class ILocatable(Interface):
    location = Attribute("Where this thing is")

class ILinkable(Interface):
    def link(distance, collector):
        pass

    def unlink(distance, collector):
        pass

    def grab(implementor):
        pass

    def ungrab(implementor):
        pass

class AtomMobility(facets.Facet):
    """Implement ILocatable for non-containers
    """
    implements(ILocatable)

    _location = None

    def location():
        def get(self):
            return self._location
        def set(self, value):
            self._moveTo(value)
        return get, set
    location = property(*location())

    def contents():
        def get(self):
            link = ILinkable(self)
            # DON'T use a query like lookFor, this is a straight manipulation
            # to accompany _outWithTheOld and _inWithTheNew
            for imp in link.implementors:
                loc = ILocatable(imp, None)
                if loc is not None and ILinkable(loc.location) is ILinkable(self):
                    yield loc.original
        return get,

    contents = property(*contents())

    def __init__(self, original, location = None, mobile = True):
        facets.Facet.__init__(self, original)
        self.mobile = mobile
        if location is not None:
            self.location = location

    def _outWithTheOld(self, cself, cnew):
        cloc = ILinkable(self.location)
        cloc.ungrab(cself)
        cself.ungrab(cloc)

    def _inWithTheNew(self, cself, cnew):
        self._location = cnew
        if cnew is not None:
            cnew.grab(cself)
            cself.grab(cnew)

    def _moveTo(self, newLocation):
        if not self.mobile and newLocation is not None:
            raise errors.ActionRefused(self, " is immobile!")
        cnew = None
        if newLocation is not None:
            cnew = ILinkable(newLocation)
        cself = ILinkable(self)
        if self.location is not None:
            self._outWithTheOld(cself, cnew)
        self._inWithTheNew(cself, cnew)

class ContainerMobility(AtomMobility):
    """Implement ILocatable for containers
    """


    def _outWithTheOld(self, cself, cnew):
        AtomMobility._outWithTheOld(self, cself, cnew)
        cloc = ILinkable(self.location)
        cself.unlink(0, cloc)

    def _inWithTheNew(self, cself, cnew):
        AtomMobility._inWithTheNew(self, cself, cnew)
        if cnew is not None:
            cself.link(0, cnew)


class Atom(facets.Facet):
    implements(ICollector, ILinkable)

    def __init__(self, original):
        facets.Facet.__init__(self, original)
        self.implementors = []
        self.collectors = []

    def iterImplementors(self, interface):
        """Yield a sequence of objects implementing interface.
        """
        selfish = interface(self, None)
        if selfish is not None:
            yield selfish
        for i in self.implementors:
            o = interface(i, None)
            if o is not None:
                yield o

    def find(self, asker, interface, criterion):
        valid = ICallableCriterion(criterion, always)
        for implementor in self.iterImplementors(interface):
            if valid(implementor):
                yield implementor

    def more(self, asker, interface, criterion):
        return self.collectors

    def link(self, distance, other):
        """Make a collector reachable from this object at the given distance.
        """
        ILinkable(other).collectors.append((distance, self))

    def unlink(self, distance, other):
        """Make a collector at exactly the given distance unreachable from this object.
        """
        ILinkable(other).collectors.remove((distance, self))

    def grab(self, other):
        """Add an implementor to this collector.
        """
        self.implementors.append(other)

    def ungrab(self, other):
        """Remove an implement from this collector.
        """
        self.implementors.remove(other)

class Container(Atom):
    def link(self, distance, other):
        Atom.link(self, distance, other)
        self.collectors.append((distance, ILinkable(other)))

    def unlink(self, distance, other):
        Atom.unlink(self, distance, other)
        self.collectors.remove((distance, ILinkable(other)))

class Take(actions.TargetAction):

    def getPotentialThings(self, iName, iType):
        for t in actions.TargetAction.getPotentialThings(self, iName, iType):
            if not isinstance(t, actions.Refusal) and (
                ILocatable(t).location is ILinkable(self.actor)):
                yield actions.Refusal(t, ("You already have ", t, "."))
            else:
                yield t

    def doAction(self):
        if ILocatable(self.target).location == ILinkable(self.actor):
            raise errors.ActionFailed("You were already holding ", self.target)
        if ILinkable(self.target) == ILinkable(self.actor):
            raise errors.ActionFailed("You try and you try, "
                                      "but you can't seem to get any leverage.")
        if ILocatable(self.actor).location == ILinkable(self.target):
            raise errors.ActionFailed("Your attempt to warp the fabric of space fails.")
        ILocatable(self.target).location = self.actor
        broadcastEvent(self.actor,
                       ("You pick up ", self.target, "."),
                       (self.actor, " picks up ", self.target, "."))

ITakeTarget = ILocatable

class Put(actions.ToolAction):
    ON = 'on'
    IN = 'in'
    UNDER = BENEATH = 'under'
    NEXT_TO = 'next to'

    PREPOSITIONS = [ON, IN, UNDER, NEXT_TO]

    def __init__(self, player, preposition, *a, **kw):
        actions.ToolAction.__init__(self, player, *a, **kw)
        self.preposition = preposition

    def doAction(self):
        ILocatable(self.tool).location = self.target

IPutTarget = ILinkable
IPutTool = ILocatable

class Drop(actions.TargetAction):
    def getPotentialThings(self, iName, iType):
        for t in actions.TargetAction.getPotentialThings(self, iName, iType):
            if ILocatable(t).location is ILinkable(self.actor):
                yield t
            else:
                yield actions.Refusal(t, ("You're not carrying ", t, "."))

    def doAction(self):
        ILocatable(self.target).location = ILocatable(self.actor).location
        broadcastEvent(self.actor,
                       ("You drop ", self.target, "."),
                       (self.actor, " drops ", self.target, "."))

IDropTarget = ILinkable

class ContainmentParser(english.Subparser):
    simpleTargetParsers = {'take': Take,
                           'get': Take,
                           'drop': Drop}

    def parse_put(self, player, text):
        for prep in Put.PREPOSITIONS:
            delim = ' ' + prep + ' '
            if delim in text:
                toolName, targetName = english.rsplit1(text, delim)
                return [Put(player, prep, targetName, toolName)]
        return []

english.registerSubparser(ContainmentParser())

class Owner(facets.Facet):
    """
    Implementor of actor for verbs which involve the ability to carry or
    physically assert ownership over objects.
    """
    implements(ITakeActor,
               IPutActor,
               IDropActor)

