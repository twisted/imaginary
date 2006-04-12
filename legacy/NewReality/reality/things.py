# -*- test-case-name: reality.test_reality -*-
NAME = 0
TARGET = 1

from twisted.python import components, log, context
from twisted.internet import defer

from reality.text import common

from quotient import storq

class IInterfaceForwarder(components.Interface):
    def collectImplementors(self, asker, iface, collection=None, seen=None, event=None, name='', intensity=2):
        """Return a dictionary mapping InterfaceForwarders to their implementors of iface.

        @type asker: C{Thing}
        @param asker: The object which initiated this collection.
        
        @type iface: C{Interface}
        @param iface: The interface objects collected must implemented.
        
        @type collection: C{dict}
        @param collection: The objects collected so far.

        @type seen: C{dict}
        @param seen: The objects already considered for inclusion in C{collection}.

        @param event: The event this collection is in response to.
        
        @type name: C{str}
        @param name: The name objects to collect should answer to, if applicable.
        
        @type intensity: C{int}
        @param intensity: The effort to expend in the search for implementors of C{iface}.
        
        @rtype: C{dict}
        @return: A dictionary mapping instances implementing IInterfaceForwarder to objects
        implementing C{iface}.
        """

    def lookFor(self, name, iface, intensity=None):
        """Look for all implementors of the given interface

        @type name: C{str} or C{NoneType}
        @param name: The name of the thing to look for
        
        @type iface: C{components.Interface}
        @param iface: The interface the target must implement
        
        @type intensity: C{int}
        @param intensity: The effort to expend in this search

        @rtype: C{list} of implementors of C{iface}
        @return: The objects found with the given name
        """

class IInterfaceFilter(components.Interface):
    def filterImplementors(self, asker, iface, implementors):
        """
        """

class IThing(components.Interface):
    def emitEvent(self, event, iface=None):
        """Emit the given event.
        """

NEUTER = 0
MALE = 1
FEMALE = 2

class Thing(storq.Item, components.Componentized):
    """I am the abstract superclass of all observable objects in a Twisted
    Reality world.
    """

##     persistenceForgets = ['store']
##     contextRemembers = [('store','store')]

    unique = 0
    gender = NEUTER
    __implements__ = IThing, IInterfaceForwarder
    
    def __init__(self, store, name='@', gender=None):
        components.Componentized.__init__(self)
        storq.Item.__init__(self, store)
        common.INoun(self).changeName(name) # get default language implementor
        self._links = []
        self._implementorFilters = []
        if gender is not None:
            self.gender = gender

    def knownAs(self, name, observer):
        return common.INoun(self).knownAs(name, observer)

    def __repr__(self):
        noun = self.getComponent(common.INoun)
        name = noun is None and self.__class__.__name__ or noun.name
        return ''.join(('<', name, '>'))

    def link(self, other):
        self.touch()
        self._links.append(other.referenceTo())
        
    def unlink(self, other):
        self.touch()
        if isinstance(other, storq.ItemReference):
            thing = other
        else:
            thing = other.referenceTo()
            
        self._links.remove(thing)
        
    def allLinks(self):
        return self._links

    intensityBarrier = 1

    def collectMe(self, asker, iface, collection, name=None, event=None):
        if (name is None) or self.knownAs(name, asker):
            comp = self.getComponent(iface)
            if comp is not None:
                collection[self] = comp
            elif name is not None:
                collection[self] = Refusal(self, ("You can't do that with ",
                                                  self,"."))

    def collectImplementors(self, asker, iface, collection, seen, event=None, name=None, intensity=3):
        if not intensity:
            return collection
        seen[self.storeID] = None
        self.collectMe(asker, iface, collection, name=name, event=event)
        newIntensity = intensity - self.intensityBarrier
        for link in self.allLinks():
            if not seen.has_key(link.storeID):
                thing = link.getItem()
                thing.collectImplementors(asker, iface, collection=collection, seen=seen, name=name, intensity=newIntensity)
        return collection

    def lookFor(self, name, iface, intensity=2):
        """Look for all implementors of 
        """
        
        l = self.store.transact(self.collectImplementors, self, iface, {}, {}, name=name,intensity=intensity).values()
        for filt in self._implementorFilters:
            l = filt.filterImplementors(self, iface, l)
        return l

    def findListeners(self, event, iface=None, intensity=3):
        if iface is None:
            iface = IEventReceiver
        listeners = self.collectImplementors(self, iface, {}, {}, event=event, intensity=intensity).values()
        return listeners

    def emitEvent(self, event, iface=None, listeners=None, intensity=3):
        if listeners is not None:
            assert len(listeners) != 0
        for listener in listeners or self.findListeners(event, iface, intensity=intensity):
            try:
                listener.eventReceived(self, event)
            except:
                log.deferr()

    def searchContents(self, name, interface):
        """
        This code is awful. However, desperate
        times call for desperate measures.
        """
        return [x for x in IInterfaceForwarder(self).lookFor(name, interface)
                if not isinstance(x, Refusal)
                if IThing(x).location.getItem() == self]
    
    def getOutermostRoom(self):
        "desperate times, etc"
        obj = self
        while getattr(obj,'location',None):
            obj = obj.location.getItem()
        return obj


class Refusal:
    """
    When I ask for implementors of an interface, I can get one of three
    answers:
    
      - Yes, I implement that - an implementor of the interface.
      - No, I don't implement that - no result.
      - I might implement that, but in any event you can't access it for the
        following reason...

    The first two are obvious: collect / don't collect in collectImplementors.
    However, when one wants to refuse an interface in the general case, an
    interface that the system in question may not even know about, this is the
    object that should be returned.

    This allows us to to implement the following sequence, without having
    portability intimately aware of INeebleTarget ::

        > LOOK
        [ Contrived Example ]
        There is a glass box here.  It is closed.
          The glass box contains:
            - a gurfle
            - a smoodle
        > NEEB GURFLE
        You can't neeble that: The gurfle is in a closed box.
    """
    __implements__ = ()

    def __init__(self, implementor, whyNot):
        """Create a Refusal.

        I take an implementor and a reason why that implementor is not
        appropriate.  The implementor, in addition to having a 
        
        """
        self.implementor = implementor
        self.whyNot = whyNot


class IEventReceiver(components.Interface):
    def eventReceived(self, emitter, event):
        """An event was received.
        """

class EventReceiver(components.Adapter):
    __implements__ = IEventReceiver
    def eventReceived(self, emitter, event):
        raise NotImplementedError(self.__class__.__name__ + '.eventReceived')

class IMoveListener(IEventReceiver):
    """A listener for movement events.
    """

    def thingArrived(self, emitter, event):
        pass

    def thingLeft(self, emitter, event):
        pass

    def thingMoved(self, emitter, event):
        pass

class MovementEvent:
    """An event indicating that something moved.
    
    I have 3 attributes:

        - thing (the thing that moved)
        - oldLocation (the location I am moving from)
        - newLocation (the location I am moving to)
    """
    def setupMovement(self, thing, oldLocation, newLocation):
        """Set the three significant attributes.
        
        This is done in this apparently wacky way so that I may be used as a
        mix-in class for action types that involve moving an object.
        """
        self.thing = thing
        self.oldLocation = oldLocation
        self.newLocation = newLocation

class Movable(Thing):
    location = None

    def moveTo(self, newLocation, event=None):
        """Movable
        @type newLocation: L{reality.things.Thing}
        @type event: L{reality.things.MovementEvent}
        """
        if event is None:
            event = MovementEvent()
        event.setupMovement(self, self.location and self.location.getItem(), newLocation)
        leaveList = self.findListeners(event, IMoveListener)
        if self.location is not None:
            self.unlink(self.location)
            self.location.getItem().unlink(self)
        self.location = newLocation.referenceTo()
        newLocation.link(self)
        self.link(newLocation)
        arriveList = self.findListeners(event, IMoveListener)
        moveList = []
        for o in leaveList:
            if isinstance(o, Refusal):
                continue
            if o in arriveList:
                try:
                    o.thingMoved(self, event)
                except:
                    log.deferr()
                arriveList.remove(o)
            else:
                try:
                    o.thingLeft(self, event)
                except:
                    log.deferr()
        for o in arriveList:
            if isinstance(o, Refusal):
                continue
            try:
                o.thingArrived(self, event)
            except:
                log.deferr()


    def destroy(self):
        """
        Forcibly remove an object from its location.
        """
        #XXX: Move to limbo
        self.location.unlink(self)
        self.unlink(self.location)
        self.location = None

class Actor(Movable):
    """All the world's a stage.
    """

class Player(Actor):
    home = None
    def die(self):
        self.emitEvent("You die...",intensity=1)
        if self.home:
            self.moveTo(self.home)
