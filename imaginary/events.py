# -*- test-case-name: imaginary.test -*-

from zope.interface import implements

from twisted.python import context

from imaginary import iimaginary, language


class Event(language.BaseExpress):
    implements(iimaginary.IConcept)

    actorMessage = targetMessage = toolMessage = otherMessage = None

    def __init__(self,
                 location=None, actor=None, target=None, tool=None,
                 actorMessage=None, targetMessage=None, toolMessage=None,
                 otherMessage=None):

        if location is None and actor is not None:
            location = actor.location

        self.location = location
        self.actor = actor
        self.target = target
        self.tool = tool
        if actorMessage is not None:
            self.actorMessage = iimaginary.IConcept(actorMessage)
        if targetMessage is not None:
            self.targetMessage = iimaginary.IConcept(targetMessage)
        if toolMessage is not None:
            self.toolMessage = iimaginary.IConcept(toolMessage)
        if otherMessage is not None:
            self.otherMessage = iimaginary.IConcept(otherMessage)


    def conceptFor(self, observer):
        # This can't be a dict because then the ordering when actor is target
        # or target is tool or etc is non-deterministic.
        if observer is self.actor:
            msg = self.actorMessage
        elif observer is self.target:
            msg = self.targetMessage
        elif observer is self.tool:
            msg = self.toolMessage
        else:
            msg = self.otherMessage
        return msg


    def reify(self):
        L = []
        for ob in iimaginary.IContainer(self.location).getContents():
            observer = iimaginary.IEventObserver(ob, None)
            if observer:
                sender = observer.prepare(self)
                if not callable(sender):
                    raise TypeError("Senders must be callable", sender)
                L.append(sender)
        return lambda: map(apply, L)


    def vt102(self, observer):
        c = self.conceptFor(observer)
        if c is not None:
            return [c.vt102(observer), '\n']
        return u''



class ThatDoesntMakeSense(Event):
    """
    An action was attempted which is logically impossible.
    """
    def __init__(self, actorMessage="That doesn't make sense.", **kw):
        super(ThatDoesntMakeSense, self).__init__(actorMessage=actorMessage, **kw)


class ThatDoesntWork(Event):
    """
    An action was attempted which is phyically impossible.
    """
    def __init__(self, actorMessage="That doesn't work.", **kw):
        super(ThatDoesntWork, self).__init__(actorMessage=actorMessage, **kw)


class Success(Event):
    """
    You do it.  Swell.
    """

    def broadcast(self):
        """
        Don't really broadcast.  Add this event to the events which will be
        sent when the action (or whatever) execution transaction is committed
        successfully.
        """
        broadcaster = context.get(iimaginary.ITransactionalEventBroadcaster)
        if broadcaster is not None:
            broadcaster.addEvent(self.reify())
        else:
            self.reify()()



class ArrivalEvent(Success):
    """
    An event representing the arrival of an object at a location from an
    origin.
    """
    def __init__(self, thing, origin=None, direction=None):
        self.thing = thing
        self.origin = origin
        self.direction = direction
        self.location = self.thing.location


    def conceptFor(self, observer):
        if observer is self.thing:
            return None
        if self.origin is not None:
            msg = [" arrives from ", self.origin, "."]
        elif self.direction is not None:
            msg = [" arrives from the ", self.direction, "."]
        else:
            msg = [" arrives."]
        msg.insert(0, self.thing)
        return language.Sentence(msg)
