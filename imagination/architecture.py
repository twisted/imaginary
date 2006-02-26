"""
Architectural features such as rooms, doors, and walls.
"""

from zope.interface import Interface, implements
from imagination import simulacrum, actions, containment, errors, event
from imagination.text import english
from imagination.facets import Facet

class IExit(Interface):
    def between(a, b):
        """
        Link a and b together with this edge
        """

class Portal(containment.Container):
    implements(IExit)
    def between(self, a, b):
        a = containment.ILinkable(a)
        b = containment.ILinkable(b)
        self._locs = [a, b]
        a.link(1,self)
        b.link(1,self)

    def getOppositeLocation(self, loc):
        """The name says it all! But the code says very little.
        """
        return self._locs[not self._locs.index(loc)]

    def portableEntered(self, portable, oldLocation):
        loc = self.getOppositeLocation(oldLocation)
        portable.location = loc


class IOpenTarget(Interface):
    def open():
        """Try to open the door! Maybe raise an ActionRefused.
        """
class ICloseTarget(Interface):
    def close():
        """Try to close etc"""

class ISightOnly(Interface):
    """Component for a criterion set to True when a call to collect() is only
    looking for objects that can be seen, not manipulated.  This interface
    represents a boolean.
    """

class Door(Portal):
    """
    I'm a portal that can be opened and closed.
    """
    implements(IOpenTarget, ICloseTarget)

    def __init__(self, original, closed=True, transparent=False):
        Portal.__init__(self, original)
        self.closed = closed
        self.transparent = transparent

    # IOpenTarget

    def open(self, action):
        if self.closed is False:
            raise errors.ActionRefused((self, " is already open!"))
        otherMessage = (action.actor, " opens the ", self)
        event.broadcastEvent(action.actor,
            ("You open the ", self, "."),
            otherMessage)
        event.broadcastToLocation(
            self.getOppositeLocation(containment.ILocatable(action.actor).location),
            otherMessage)
        self.closed = False

    # ICloseTarget

    def close(self, action):
        if self.closed is True:
            raise errors.ActionRefused((self, " is already closed!"))
        otherMessage = (action.actor, " closes the ", self)
        event.broadcastEvent(action.actor,
            ("You close the ", self, "."),
            otherMessage)
        event.broadcastToLocation(
            self.getOppositeLocation(containment.ILocatable(action.actor).location),
            otherMessage)
        self.closed = True

    def iterImplementors(self, interface):
        if self.closed:
            try:
                selfish = interface(self)
            except TypeError: 
                return iter([])
            return iter([selfish])
        else:
            return containment.Container.iterImplementors(self, interface)

    def more(self, asker, interface, criteria):
        superseq = containment.Container.more(self, asker,
                                              interface, criteria)
        if self.closed:
            if self.transparent:
                if ISightOnly(criteria, False):
                    for d, n in superseq:
                        yield d, n
                    return
                else:
                    for d, n in superseq:
                        yield d, TouchRefuser(self, n)
                    return
            else:
                return
        else:
            for n in superseq:
                yield n

    # IEnterTarget

    def preTargetEnter(self, action):
        if self.closed:
            raise errors.ActionRefused((self, " is closed."))

class TouchRefuser:
    implements(simulacrum.ICollector)
    def __init__(self, obstruction, target):
        self.obstruction = obstruction
        self.target = target

    def more(self, *a,**k):
        return []

    def find(self, *a, **kw):
        for t in self.target.find(*a,**kw):
            yield actions.Refusal(
                t, ("You can see ",t, " but ",self.obstruction,
                    " is in the way."))

class Open(actions.TargetAction):
    def doAction(self):
        self.target.open(self)

class Close(actions.TargetAction):
    def doAction(self):
        self.target.close(self)


class Enter(actions.TargetAction):
    def doAction(self):
        loc = containment.ILocatable(self.actor).location
        self.target.portableEntered(containment.ILocatable(self.actor), loc)
        english.IThinker(self.actor).parse("look")

IEnterTarget = IExit


class MovementParser(english.Subparser):
    simpleTargetParsers = {'enter': Enter,
                           'open': Open,
                           'close': Close}

english.registerSubparser(MovementParser())

class OpenCloseActor(Facet):
    implements(IOpenActor, ICloseActor)

class Enterer(Facet):
    implements(IEnterActor)
