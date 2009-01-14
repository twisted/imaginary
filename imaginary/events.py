# -*- test-case-name: imaginary.test -*-

from zope.interface import implements

from twisted.python import context

from imaginary import iimaginary, language, eimaginary


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
        """
        Determine which objects should receive this event and return a callable
        object which will deliver it to them.

        Note that this occurs during event propagation, and you probably don't
        need to call it directly.

        @see: L{iimaginary.IEventObserver.prepare} and
            L{TransactionalEventBroadcaster} for a more thorough description of
            how this method is used to interact with transactions.

        @return: a 0-arg callable object which, when called, will call the
            results of all L{IEventObserver}s which were contained within this
            L{Event}'s location when this method, L{Event.reify}, was called.
        """
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



class TransactionalEventBroadcaster(object):
    """
    Collect a bunch of output events as a transaction is being executed, then
    distribute them when it has completed.

    Events can be added normally or as revert events.  Normal events are
    broadcast after the transaction is successfully committed.  Revert events
    are broadcast if the transaction failed somehow and was been reverted.
    """
    implements(iimaginary.ITransactionalEventBroadcaster)

    def __init__(self):
        self._events = []
        self._revertEvents = []


    def addEvent(self, event):
        """
        Add a normal event.

        @param event: A no-argument callable to be invoked when this
        transaction has been committed.
        """
        if not callable(event):
            raise ValueError("Events must be callable", event)
        self._events.append(event)


    def addRevertEvent(self, event):
        """
        Add a revert event.

        @param event: A no-argument callable to be invoked when this
        transaction has been reverted.
        """
        if not callable(event):
            raise ValueError("Events must be callable", event)
        self._revertEvents.append(event)


    def broadcastEvents(self):
        """
        Send all normal events.
        """
        events = self._events
        self._events = self._revertEvents = None
        map(apply, events)


    def broadcastRevertEvents(self):
        """
        Send all revert events.
        """
        events = self._revertEvents
        self._events = self._revertEvents = None
        map(apply, events)



def runEventTransaction(store, func, *args, **kwargs):
    """
    This takes responsibility for setting up the transactional event
    broadcasting junk, handling action errors, and broadcasting commit or
    revert events.
    """
    broadcaster = TransactionalEventBroadcaster()
    def runHelper():
        # Set up event context for the duration of the action
        # run.  Additionally, handle raised ActionFailures by
        # adding their events to the revert event list and
        # re-raising them so they will revert the transaction.
        try:
            return context.call(
                {iimaginary.ITransactionalEventBroadcaster: broadcaster},
                func, *args, **kwargs)
        except eimaginary.ActionFailure, e:
            broadcaster.addRevertEvent(e.event.reify())
            raise
    try:
        result = store.transact(runHelper)
    except eimaginary.ActionFailure, e:
        broadcaster.broadcastRevertEvents()
        return None
    else:
        broadcaster.broadcastEvents()
        return result



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
    An event representing the arrival of an object.
    """



class MovementArrivalEvent(ArrivalEvent):
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



class DepartureEvent(Success):
    """
    An event representing the departure of an object at a location to a
    destination.
    """
    def __init__(self, location, actor, **kw):
        """
        @type location: L{iimaginary.IThing} provider.
        @param location: The location that the actor is leaving.
        @type actor: L{iimaginary.IThing} provider.
        @param actor: The actor that is leaving.
        """
        super(DepartureEvent, self).__init__(location, actor, **kw)


class SpeechEvent(Success):
    """
    An event representing something somebody said.

    @ivar speaker: The Thing which spoke.
    @ivar text: The text which was spoken.
    """
    def __init__(self, speaker, text):
        """
        @type speaker: L{iimaginary.IThing} provider.
        @param speaker: The actor emitting this speech.
        @type text: C{unicode}
        @param text: The text that the actor said.
        """
        self.speaker = speaker
        self.text = text
        Success.__init__(
            self,
            location=speaker.location,
            actor=speaker,
            actorMessage=["You say, '", text, "'"],
            otherMessage=language.Sentence([speaker, " says, '", text, "'"]))
