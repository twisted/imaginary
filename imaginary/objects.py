# -*- test-case-name: imaginary.test.test_garments.FunSimulationStuff.testTooBulky -*-

"""
This module contains the core, basic objects in Imaginary.

L{imaginary.objects} contains the physical simulation (L{Thing}), objects
associated with scoring (L{Points}), and the basic actor interface which allows
the user to perform simple actions (L{Actor}).
"""

from __future__ import division, print_function

import math

from zope.interface import implements, implementer

from twisted.python import reflect, components

from epsilon import structlike
from epsilon.remember import remembered

from axiom import item, attributes

from imaginary import iimaginary, eimaginary, text as T, events, language

from imaginary.enhancement import Enhancement as _Enhancement

from imaginary.language import Description

from imaginary.idea import (
    Idea, Link, Proximity, ProviderOf, AlsoKnownAs, CanSee,
    Vector, DelegatingRetriever)


class Points(item.Item):
    max = attributes.integer(doc="""
    Maximum number of points.
    """, allowNone=False)

    current = attributes.integer(doc="""
    Current number of points.
    """, allowNone=False)

    def __init__(self, **kw):
        if 'max' in kw and 'current' not in kw:
            kw['current'] = kw['max']
        super(Points, self).__init__(**kw)

    def __cmp__(self, other):
        return cmp(self.current, other)

    def __str__(self):
        return '%d/%d' % (self.current, self.max)

    def __repr__(self):
        d = {'class': reflect.qual(self.__class__),
             'current': self.current,
             'max': self.max}
        return '%(class)s(%(max)d, %(current)d)' % d

    def increase(self, amount):
        return self.modify(amount)

    def decrease(self, amount):
        return self.modify(-amount)

    def modify(self, amount):
        self.current = max(min(self.current + amount, self.max), 0)
        return self.current



class Thing(item.Item):
    """
    A L{Thing} is a physically located object in the game world.

    While a game object in Imaginary is composed of many different Python
    objects, the L{Thing} is the central object that most game objects will
    share.  It's central for several reasons.

    First, a L{Thing} is connected to the point-of-interest simulation that
    makes up the environment of an Imaginary game.  A L{Thing} has a location,
    and a L{Container} can list the L{Thing}s located within it, which is how
    you can see the objects in your surroundings or a container.

    Each L{Thing} has an associated L{Idea}, which provides the graph that can
    be traversed to find other L{Thing}s to be the target for actions or
    events.

    A L{Thing} is also the object which serves as the persistent nexus of
    powerups that define behavior.  An L{_Enhancement} is a powerup for a
    L{Thing}.  L{Thing}s can be powered up for a number of different interfaces:

        - L{iimaginary.IMovementRestriction}, for preventing the L{Thing} from
          moving around,

        - L{iimaginary.ILinkContributor}, which can provide links from the
          L{Thing}'s L{Idea} to other L{Idea}s,

        - L{iimaginary.ILinkAnnotator}, which can provide annotations on links
          incoming to or outgoing from the L{Thing}'s L{Idea},

        - L{iimaginary.ILocationLinkAnnotator}, which can provide annotations on
          links to or from any L{Thing}'s L{Idea} which is ultimately located
          within the powered-up L{Thing}.

        - L{iimaginary.IDescriptionContributor}, which provide components of
          the L{Thing}'s description when viewed with the L{Look} action.

        - and finally, any interface used as a target for an action or event.

    The way this all fits together is as follows: if you wanted to make a
    shirt, for example, you would make a L{Thing}, give it an appropriate name
    and description, make a new L{Enhancement} class which implements
    L{IMovementRestriction} to prevent the shirt from moving around unless it
    is correctly in the un-worn state, and then power up that L{Enhancement} on
    the L{Thing}.  This particular example is implemented in
    L{imaginary.garments}, but almost any game-logic implementation will follow
    this general pattern.
    """

    implements(iimaginary.IThing, iimaginary.IVisible, iimaginary.INameable,
               iimaginary.ILinkAnnotator, iimaginary.ILinkContributor)

    weight = attributes.integer(doc="""
    Units of weight of this object.
    """, default=1, allowNone=False)

    location = attributes.reference(doc="""
    Direct reference to the location of this object
    """)

    portable = attributes.boolean(doc="""
    Whether this can be picked up, pushed around, relocated, etc
    """, default=True, allowNone=False)

    name = attributes.text(doc="""
    The name of this object.
    """, allowNone=False)

    description = attributes.text(doc="""
    What this object looks like.
    """, default=u"")

    gender = attributes.integer(doc="""
    The grammatical gender of this thing.  One of L{language.Gender.MALE},
    L{language.Gender.FEMALE}, or L{language.Gender.NEUTER}.
    """, default=language.Gender.NEUTER, allowNone=False)

    proper = attributes.boolean(doc="""
    Whether my name is a proper noun.
    """, default=False, allowNone=False)


    def destroy(self):
        if self.location is not None:
            iimaginary.IContainer(self.location).remove(self)
        self.deleteFromStore()


    def links(self):
        """
        Implement L{ILinkContributor.links()} by offering a link to this
        L{Thing}'s C{location} (if it has one).
        """
        # since my link contribution is to go up (out), put this last, since
        # containment (i.e. going down (in)) is a powerup.  we want to explore
        # contained items first.
        for pup in self.powerupsFor(iimaginary.ILinkContributor):
            for link in pup.links():
                # wooo composition
                yield link
        if self.location is not None:
            l = Link(self.idea, self.location.idea)
            # XXX this incorrectly identifies any container with an object in
            # it as 'here', since it doesn't distinguish the observer; however,
            # cycle detection will prevent these links from being considered in
            # any case I can think of.  However, 'here' is ambiguous in the
            # case where you are present inside a container, and that should
            # probably be dealt with.
            l.annotate([AlsoKnownAs('here')])
            yield l


    def allAnnotators(self):
        """
        A generator which yields all L{iimaginary.ILinkAnnotator} providers
        that should affect this L{Thing}'s L{Idea}.  This includes:

            - all L{iimaginary.ILocationLinkAnnotator} powerups on all
              L{Thing}s which contain this L{Thing} (the container it's in, the
              room its container is in, etc)

            - all L{iimaginary.ILinkAnnotator} powerups on this L{Thing}.
        """
        loc = self
        while loc is not None:
            # TODO Test the loc is None case
            if loc is not None:
                for pup in loc.powerupsFor(iimaginary.ILocationLinkAnnotator):
                    yield pup
            loc = loc.location
        for pup in self.powerupsFor(iimaginary.ILinkAnnotator):
            yield pup


    def annotationsFor(self, link, idea):
        """
        Implement L{ILinkAnnotator.annotationsFor} to consult each
        L{ILinkAnnotator} for this L{Thing}, as defined by
        L{Thing.allAnnotators}, and yield each annotation for the given L{Link}
        and L{Idea}.
        """
        for annotator in self.allAnnotators():
            for annotation in annotator.annotationsFor(link, idea):
                yield annotation


    @remembered
    def idea(self):
        """
        An L{Idea} which represents this L{Thing}.
        """
        idea = Idea(self)
        idea.linkers.append(self)
        idea.annotators.append(self)
        return idea


    def findProviders(self, interface, distance):
        """
        Temporary emulation of the old way of doing things so that I can
        surgically replace findProviders.
        """
        return self.idea.obtain(
            Proximity(distance, CanSee(ProviderOf(interface))))


    def obtainOrReportWhyNot(self, retriever):
        """
        Invoke L{Idea.obtain} on C{self.idea} with the given C{retriever}.

        If no results are yielded, then investigate the reasons why no results
        have been yielded, and raise an exception describing one of them.

        Objections may be registered by:

            - an L{iimaginary.IWhyNot} annotation on any link traversed in the
              attempt to discover results, or,

            - an L{iimaginary.IWhyNot} yielded by the given C{retriever}'s
              L{iimaginary.IRetriever.objectionsTo} method.

        @return: a list of objects returned by C{retriever.retrieve}

        @rtype: C{list}

        @raise eimaginary.ActionFailure: if no results are available, and an
            objection has been registered.
        """
        obt = self.idea.obtain(retriever)
        results = list(obt)
        if not results:
            reasons = list(obt.reasonsWhyNot)
            if reasons:
                raise eimaginary.ActionFailure(events.ThatDoesntWork(
                        actor=self,
                        actorMessage=reasons[0].tellMeWhyNot()))
        return results


    def moveTo(self, where, arrivalEventFactory=None):
        """
        Implement L{iimaginary.IThing.moveTo} to change the C{location} of this
        L{Thing} to a new L{Thing}, broadcasting an L{events.DepartureEvent} to
        note this object's departure from its current C{location}.

        Before moving it, invoke each L{IMovementRestriction} powerup on this
        L{Thing} to allow them to prevent this movement.
        """
        whereContainer = iimaginary.IContainer(where, None)
        if (whereContainer is
            iimaginary.IContainer(self.location, None)):
            # Early out if I'm being moved to the same location that I was
            # already in.
            return
        if whereContainer is None:
            whereThing = None
        else:
            whereThing = whereContainer.thing
        if whereThing is not None and whereThing.location is self:
            # XXX should be checked against _all_ locations of whereThing, not
            # just the proximate one.

            # XXX actor= here is wrong, who knows who is moving this thing.
            raise eimaginary.ActionFailure(events.ThatDoesntWork(
                    actor=self,
                    actorMessage=[
                        language.Noun(where.thing).definiteNounPhrase()
                        .capitalizeConcept(),
                        " won't fit inside itself."]))

        oldLocation = self.location
        for restriction in self.powerupsFor(iimaginary.IMovementRestriction):
            restriction.movementImminent(self, where)
        if oldLocation is not None:
            events.DepartureEvent(oldLocation, self).broadcast()
        if where is not None:
            where = iimaginary.IContainer(where)
            if oldLocation is not None and not self.portable:
                raise eimaginary.CannotMove(self, where)
            where.add(self)
            if arrivalEventFactory is not None:
                arrivalEventFactory(self).broadcast()
        if oldLocation is not None:
            iimaginary.IContainer(oldLocation).remove(self)


    def knownTo(self, observer, name):
        """
        Implement L{INameable.knownTo} to compare the name to L{Thing.name} as
        well as few constant values based on the relationship of the observer
        to this L{Thing}, such as 'me', 'self', and 'here'.

        @param observer: an L{IThing} provider.
        """

        mine = self.name.lower()
        name = name.lower()
        if name == mine or name in mine.split():
            return True
        if observer == self:
            if name in ('me', 'self'):
                return True
        return False


    def visualizeWithContents(self, paths):
        """
        Visualize this L{Thing} via L{Description.fromVisualization}.
        """
        return Description.fromVisualization(self, paths)


    def isViewOf(self, thing):
        """
        Implement L{IVisible.isViewOf} to return C{True} if its argument is
        C{self}.  In other words, this L{Thing} is only a view of itself.
        """
        return (thing is self)

components.registerAdapter(lambda thing: language.Noun(thing).nounPhrase(),
                           Thing,
                           iimaginary.IConcept)


def _eventuallyContains(containerThing, containeeThing):
    """
    Does a container, or any containers within it (or any containers within any
    of those, etc etc) contain some object?

    @param containeeThing: The L{Thing} which may be contained.

    @param containerThing: The L{Thing} which may have a L{Container} that
    contains C{containeeThing}.

    @return: L{True} if the containee is contained by the container.
    """
    while containeeThing is not None:
        if containeeThing is containerThing:
            return True
        containeeThing = containeeThing.location
    return False




OPPOSITE_DIRECTIONS = {
    u"north": u"south",
    u"west": u"east",
    u"northwest": u"southeast",
    u"northeast": u"southwest"}


def _populateOpposite():
    """
    Populate L{OPPOSITE_DIRECTIONS} with inverse directions.

    (Without leaking any loop locals into the global scope, thank you very
    much.)
    """
    for (k, v) in OPPOSITE_DIRECTIONS.items():
        OPPOSITE_DIRECTIONS[v] = k

_populateOpposite()



DIRECTION_ALIASES = {
    u"n": u"north",
    u"s": u"south",
    u"w": u"west",
    u"e": u"east",
    u"nw": u"northwest",
    u"se": u"southeast",
    u"ne": u"northeast",
    u"sw": u"southwest"}



class Exit(item.Item):
    """
    An L{Exit} is an oriented pathway between two L{Thing}s which each
    represent a room.
    """

    implements(iimaginary.INameable, iimaginary.IExit)

    fromLocation = attributes.reference(
        doc="""
        Where this exit leads from.
        """, allowNone=False,
        whenDeleted=attributes.reference.CASCADE, reftype=Thing)

    toLocation = attributes.reference(
        doc="""
        Where this exit leads to.
        """, allowNone=False,
        whenDeleted=attributes.reference.CASCADE, reftype=Thing)

    name = attributes.text(doc="""
    What this exit is called/which direction it is in.
    """, allowNone=False)

    sibling = attributes.reference(doc="""
    The reverse exit object, if one exists.
    """)

    distance = attributes.ieee754_double(
        doc="""
        How far, in meters, does a user have to travel to traverse this exit?
        """, allowNone=False, default=1.0)

    def knownTo(self, observer, name):
        """
        Implement L{iimaginary.INameable.knownTo} to identify this L{Exit} as
        its C{name} attribute.
        """
        return name == self.name


    def traverse(self, thing):
        """
        Implement L{iimaginary.IExit} to move the given L{Thing} to this
        L{Exit}'s C{toLocation}.
        """
        if self.sibling is not None:
            arriveDirection = self.sibling.name
        else:
            arriveDirection = OPPOSITE_DIRECTIONS.get(self.name)

        thing.moveTo(
            self.toLocation,
            arrivalEventFactory=lambda player: events.MovementArrivalEvent(
                thing=thing,
                origin=None,
                direction=arriveDirection))


    # XXX This really needs to be renamed now that links are a thing.
    @classmethod
    def link(cls, a, b, forwardName, backwardName=None, distance=1.0):
        """
        Create two L{Exit}s connecting two rooms.

        @param a: The first room.

        @type a: L{Thing}

        @param b: The second room.

        @type b: L{Thing}

        @param forwardName: The name of the link going from C{a} to C{b}.  For
            example, u'east'.

        @type forwardName: L{unicode}

        @param backwardName: the name of the link going from C{b} to C{a}.  For
            example, u'west'.  If not provided or L{None}, this will be
            computed based on L{OPPOSITE_DIRECTIONS}.

        @type backwardName: L{unicode}
        """
        if backwardName is None:
            backwardName = OPPOSITE_DIRECTIONS[forwardName]
        forward = cls(store=a.store, fromLocation=a, toLocation=b,
                 name=forwardName, distance=distance)
        backward = cls(store=b.store, fromLocation=b, toLocation=a,
                  name=backwardName, distance=distance)
        forward.sibling = backward
        backward.sibling = forward


    def destroy(self):
        if self.sibling is not None:
            self.sibling.deleteFromStore()
        self.deleteFromStore()


    @remembered
    def exitIdea(self):
        """
        This property is the L{Idea} representing this L{Exit}; this is a
        fairly simple L{Idea} that will link only to the L{Exit.toLocation}
        pointed to by this L{Exit}, with a distance annotation indicating the
        distance traversed to go through this L{Exit}.
        """
        x = Idea(self)
        x.linkers.append(self)
        return x


    def links(self):
        """
        Generate a link to the location that this exit points at.

        @return: an iterator which yields a single L{Link}, annotated with a
            L{Vector} that indicates a distance of 1.0 (a temporary measure,
            since L{Exit}s don't have distances yet) and a direction of this
            exit's C{name}.
        """
        l = Link(self.exitIdea, self.toLocation.idea)
        l.annotate([Vector(self.distance, self.name),
                    # We annotate this link with ourselves because the 'Named'
                    # retriever will use the last link in the path to determine
                    # if an object has any aliases.  We want this direction
                    # name to be an alias for the room itself as well as the
                    # exit, so we want to annotate the link with an INameable.
                    # This also has an effect of annotating the link with an
                    # IExit, and possibly one day an IItem as well (if such a
                    # thing ever comes to exist), so perhaps we eventually want
                    # a wrapper which elides all references here except
                    # INameable since that's what we want.  proxyForInterface
                    # perhaps?  However, for the moment, the extra annotations
                    # do no harm, so we'll leave them there.
                    self])
        yield l


    def shouldEvenAttemptTraversalFrom(self, where, observer):
        """
        
        """
        return (self.fromLocation is where)

def _exitAsConcept(exit):
    return language.ExpressList(
        [u'the exit to ', language.Noun(exit.toLocation).nounPhrase()])


components.registerAdapter(_exitAsConcept, Exit, iimaginary.IConcept)



class ContainmentRelationship(structlike.record("containedBy contained")):
    """
    Implementation of L{iimaginary.IContainmentRelationship}.  The interface
    specifies no methods or attributes.  See its documentation for more
    information.
    """
    implements(iimaginary.IContainmentRelationship)



class Containment(object):
    """
    Functionality for containment to be used as a mixin in Powerups.
    """

    implements(iimaginary.IContainer, iimaginary.IDescriptionContributor,
               iimaginary.ILinkContributor)
    powerupInterfaces = (iimaginary.IContainer,
                         iimaginary.ILinkContributor,
                         iimaginary.IDescriptionContributor)

    # Units of weight which can be contained
    capacity = None

    # Boolean indicating whether the container is currently closed or open.
    closed = False

    # IContainer
    def contains(self, other):
        for child in self.getContents():
            if other is child:
                return True
            cchild = iimaginary.IContainer(child, None)
            if cchild is not None and cchild.contains(other):
                return True
        return False


    def getContents(self):
        if self.thing is None:
            return []
        return self.store.query(Thing, Thing.location == self.thing)


    def add(self, obj):
        if self.closed:
            raise eimaginary.Closed(self, obj)
        containedWeight = self.getContents().getColumn("weight").sum()
        if containedWeight + obj.weight > self.capacity:
            raise eimaginary.DoesntFit(self, obj)
        assert self.thing is not None
        obj.location = self.thing


    def remove(self, obj):
        if self.closed:
            raise eimaginary.Closed(self, obj)
        if obj.location is self.thing:
            obj.location = None


    def getExits(self):
        return self.store.query(Exit, Exit.fromLocation == self.thing)


    def getExitNames(self):
        return self.getExits().getColumn("name")


    _marker = object()
    def getExitNamed(self, name, default=_marker):
        result = self.store.findUnique(
            Exit,
            attributes.AND(Exit.fromLocation == self.thing,
                           Exit.name == name),
            default=default)
        if result is self._marker:
            raise KeyError(name)
        return result


    # ILinkContributor
    def links(self):
        """
        Implement L{ILinkContributor} to contribute L{Link}s to all contents of
        this container, as well as all of its exits, and its entrance from its
        location.
        """
        if not self.closed:
            # This is actually wrong; we ought to always return these links,
            # but annotate them with something that indicates a (potentially
            # opaque) physical obstruction.
            for ob in self.getContents():
                content = Link(self.thing.idea, ob.idea)
                content.annotate([ContainmentRelationship(self, ob)])
                yield content
        yield Link(self.thing.idea, self._entranceIdea)
        if self.thing.location is not None:
            yield Link(self.thing.idea, self._exitIdea)
        for exit in self.getExits():
            # TODO: Annotate this link with the *direction* information Change
            # the exit to annotate its outbound link with the *distance*
            # information (which it mostly does already but it mixes in the
            # direction there too)
            yield Link(self.thing.idea, exit.exitIdea)


    @remembered
    def _entranceIdea(self):
        """
        Return an L{Idea} that reflects the implicit entrance from this
        container's location to the interior of the container.
        """
        return Idea(delegate=_ContainerEntrance(self))


    @remembered
    def _exitIdea(self):
        """
        Return an L{Idea} that reflects the implicit exit from this container
        to its location.
        """
        return Idea(delegate=_ContainerExit(self))


    # IDescriptionContributor
    def contributeDescriptionFrom(self, paths):
        """
        Implement L{IDescriptionContributor} to enumerate the contents of this
        containment.

        @return: an L{ExpressSurroundings} with an iterable of all visible
        contents of this container.
        """
        return ExpressContents(self, paths)



def pathIndicatesContainmentIn(path, container):
    """
    Does the given L{Path} indicate containment in the given container?
    """
    containments = list(path.of(iimaginary.IContainmentRelationship))
    if containments:
        # TODO: need direct tests for this, since deduplicate() fixes it by
        # accident; objects in containers all have links to their locations and
        # those links could be interpreted as meaning that everything is
        # located in that object unless you look specifically at the
        # contained-thing as well as the container.
        if (containments[-1].containedBy is container and
            containments[-1].contained is
            path.targetAs(iimaginary.IThing)):
            return True
    return False



class _ContainedBy(DelegatingRetriever):
    """
    An L{iimaginary.IRetriever} which discovers only things present in a given
    container.  Currently used only for discovering the list of things to list
    in a container's description.

    @ivar retriever: a retriever to delegate to.

    @type retriever: L{iimaginary.IRetriever}

    @ivar container: the container to test containment by

    @type container: L{IThing}
    """

    implements(iimaginary.IRetriever)

    def __init__(self, retriever, container):
        DelegatingRetriever.__init__(self, retriever)
        self.container = container


    def resultRetrieved(self, path, result):
        """
        If this L{_ContainedBy}'s container contains the last L{IThing} target
        of the given path, return the result of this L{_ContainedBy}'s
        retriever retrieving from the given C{path}, otherwise C{None}.
        """
        if pathIndicatesContainmentIn(path, self.container):
            return result



@implementer(iimaginary.IExit, iimaginary.INameable)
class _ContainerEntrance(structlike.record('container')):
    """
    A L{_ContainerEntrance} is the implicit entrance to a container from its
    location.  If a container is open, and big enough, it can be entered.

    @ivar container: the container that this L{_ContainerEntrance} points to.

    @type container: L{Containment}
    """

    @property
    def name(self):
        """
        Implement L{iimaginary.IExit.name} to return a descriptive name for the
        inward exit of this specific container.
        """
        return 'into ', language.Noun(self.container.thing).definiteNounPhrase()


    def traverse(self, thing):
        """
        Implement L{iimaginary.IExit.traverse} to move the thing in transit to
        the container specified.
        """
        thing.moveTo(self.container)


    def knownTo(self, observer, name):
        """
        Delegate L{iimaginary.INameable.knownTo} to this
        L{_ContainerEntrance}'s container's thing.
        """
        return self.container.thing.knownTo(observer, name)


    def shouldEvenAttemptTraversalFrom(self, where, observer):
        """
        
        """
        return False


    @property
    def fromLocation(self):
        """
        
        """
        return self.container.thing.location



class _ContainerExit(structlike.record('container')):
    """
    A L{_ContainerExit} is the exit from a container, or specifically, a
    L{Containment}; an exit by which actors may move to the container's
    container.

    @ivar container: the container that this L{_ContainerExit} points out from.

    @type container: L{Containment}
    """

    implements(iimaginary.IExit, iimaginary.INameable)

    @property
    def name(self):
        """
        Implement L{iimaginary.IExit.name} to return a descriptive name for the
        outward exit of this specific container.
        """
        return 'out of ', language.Noun(self.container.thing).definiteNounPhrase()


    def traverse(self, thing):
        """
        Implement L{iimaginary.IExit.traverse} to move the thing in transit to
        the container specified.
        """
        thing.moveTo(self.container.thing.location)


    def knownTo(self, observer, name):
        """
        This L{_ContainerExit} is known to observers inside it as 'out'
        (i.e. 'go out', 'look out'), but otherwise it has no known description.
        """
        return (observer.location == self.container.thing) and (name == 'out')


    def shouldEvenAttemptTraversalFrom(self, where, observer):
        """
        
        """
        return False


    @property
    def fromLocation(self):
        """
        
        """
        return self.container.thing



class ExpressSurroundings(language.ItemizedList):
    def concepts(self, observer):
        return [iimaginary.IConcept(o)
                for o in super(ExpressSurroundings, self).concepts(observer)
                if o is not observer]



class Container(item.Item, Containment, _Enhancement):
    """
    A generic L{_Enhancement} that implements containment.
    """

    # TODO: Add `hasExits` flag - somewhere - maybe not as persistent state?
    # If it is false then don't generate any exit links (mainly into and out of
    # since those are currently automatic and pervasive).  Set it to false on
    # players.  Players aren't really containers.  It's just a hack to make
    # inventories easy.  Implement a better inventory system later - holding
    # things, putting things in your pockets, etc.

    contentsTemplate = attributes.text(
        doc="""
        Define how the contents of this container are presented to observers.
        Certain substrings will be given special treatment.

        @see: L{imaginary.language.ConceptTemplate}
        """,
        allowNone=True, default=None)

    capacity = attributes.integer(
        doc="""
        Units of weight which can be contained.
        """, allowNone=False, default=1)

    closed = attributes.boolean(
        doc="""
        Indicates whether the container is currently closed or open.
        """, allowNone=False, default=False)

    thing = attributes.reference(
        doc="""
        The object this container powers up.
        """)


    def __str__(self):
        return '<Container %r>' % (self.thing.name,)
    __repr__ = __str__



class ExpressContents(language.Sentence):
    """
    A concept representing the things contained by another thing - excluding
    the observer of the concept.
    """
    _CONDITION = CanSee(ProviderOf(iimaginary.IThing))

    def __init__(self, original, paths):
        """
        
        """
        super(ExpressContents, self).__init__(original)
        self.paths = paths


    def _contentConcepts(self, observer):
        """
        Get concepts for the contents of the thing wrapped by this concept.

        @param observer: The L{objects.Thing} which will observe these
            concepts.

        @return: A L{list} of the contents of C{self.original}, excluding
            C{observer}.
        """
        container = self.original
        seer = CanSee(ProviderOf(iimaginary.IThing))
        for path in self.paths:
            target = path.targetAs(iimaginary.IThing)
            if target is None:
                continue
            if pathIndicatesContainmentIn(path, container):
                if seer.shouldStillKeepGoing(path):
                    yield target


    @property
    def template(self):
        """
        This is the template string which is used to construct the overall
        concept, indicating what the container is and what its contents are.
        """
        template = self.original.contentsTemplate
        if template is None:
            template = u"{subject:pronoun} contains {contents}."
        return template


    def _expand(self, template, observer, concepts):
        """
        Expand the given template using the wrapped container's L{Thing} as the
        subject.

        C{u"contents"} is also available for substitution with the contents of
        the container.

        @return: An iterator of concepts derived from the given template.
        """
        return language.ConceptTemplate(template).expand(dict(
                subject=self.original.thing,
                contents=language.ItemizedList(concepts)))


    def concepts(self, observer):
        """
        Return a L{list} of L{IConcept} providers which express the contents of
        the wrapped container.
        """
        concepts = list(self._contentConcepts(observer))
        if concepts:
            return list(self._expand(self.template, observer, concepts))
        return []



class ExpressCondition(language.BaseExpress):
    implements(iimaginary.IConcept)

    def vt102(self, observer):
        return [
            [T.bold, T.fg.yellow, language.Noun(
                    self.original.thing).shortName().plaintext(observer)],
            u" is ",
            [T.bold, T.fg.red, self.original._condition(), u"."]]


class Actable(object):
    implements(iimaginary.IActor, iimaginary.IEventObserver)

    powerupInterfaces = (iimaginary.IActor, iimaginary.IEventObserver,
                         iimaginary.IDescriptionContributor)

    # Yay, experience!
    experience = 0
    level = 0

    CONDITIONS = (
        'dead',
        'dying',
        'incapacitated',
        'mortally wounded',
        'injured',
        'bleeding',
        'shaken up',
        'fine',
        'chipper',
        'great')


    # IDescriptionContributor
    def contributeDescriptionFrom(self, paths):
        return ExpressCondition(self)


    def _condition(self):
        if self.hitpoints.current == 0:
            return self.CONDITIONS[0]
        ratio = self.hitpoints.current / self.hitpoints.max
        idx = int(ratio * (len(self.CONDITIONS) - 2))
        return self.CONDITIONS[idx + 1]


    # IActor
    def send(self, *event):
        if len(event) != 1 or isinstance(event[0], (str, tuple)):
            event = events.Success(
                actor=self.thing,
                actorMessage=event)
        else:
            event = event[0]
        self.prepare(event)()


    # IEventObserver
    def prepare(self, concept):
        """
        Implement L{iimaginary.IEventObserver.prepare} to prepare C{concept}
        with this L{Actable}'s C{intelligence}, if it has one; otherwise,
        return a callable that does nothing.
        """
        intelligence = self.getIntelligence()
        if intelligence is not None:
            return intelligence.prepare(concept)
        return lambda: None


    def gainExperience(self, amount):
        experience = self.experience + amount
        level = int(math.log(experience) / math.log(2))
        evt = None
        if level > self.level:
            evt = events.Success(
                actor=self.thing,
                actorMessage=("You gain ", level - self.level, " levels!\n"))
        elif level < self.level:
            evt = events.Success(
                actor=self.thing,
                actorMessage=("You lose ", self.level - level, " levels!\n"))
        self.level = level
        self.experience = experience
        if evt is not None:
            self.send(evt)



class Actor(item.Item, Actable, _Enhancement):
    hitpoints = attributes.reference(doc="""
    """)
    stamina = attributes.reference(doc="""
    """)
    strength = attributes.reference(doc="""
    """)

    _ephemeralIntelligence = attributes.inmemory(doc="""
    Maybe the L{IEventObserver} associated with this actor, generally a
    L{wiring.player.Player} instance.
    """)

    _enduringIntelligence = attributes.reference(doc="""
    Maybe the persistent L{IEventObserver} associated with this actor.
    Generally used with NPCs.
    """)

    thing = attributes.reference(doc="""
    The L{IThing} that this is installed on.
    """)

    level = attributes.integer(doc="""
    Don't you hate level-based games?  They're so stupid.
    """, default=0, allowNone=False)

    experience = attributes.integer(doc="""
    XP!  Come on, you know what this is.
    """, default=0, allowNone=False)


    def __init__(self, **kw):
        super(Actor, self).__init__(**kw)
        if self.hitpoints is None:
            self.hitpoints = Points(store=self.store, max=100)
        if self.stamina is None:
            self.stamina = Points(store=self.store, max=100)
        if self.strength is None:
            self.strength = Points(store=self.store, max=100)


    def activate(self):
        self._ephemeralIntelligence = None


    def setEphemeralIntelligence(self, intelligence):
        """
        Set the ephemeral intelligence, generally one representing a PC's user
        interface.
        """
        if self._enduringIntelligence:
            raise ValueError("Tried setting an ephemeral intelligence %r when "
                             "an enduring intelligence %r already existed"
                             % (intelligence, self._enduringIntelligence))
        self._ephemeralIntelligence = intelligence


    def setEnduringIntelligence(self, intelligence):
        """
        Set the enduring intelligence, generally one representing an NPC's AI.
        """
        if self._ephemeralIntelligence:
            raise ValueError("Tried setting an enduring intelligence %r when "
                             "an ephemeral intelligence %r already existed"
                             % (intelligence, self._ephemeralIntelligence))
        self._enduringIntelligence = intelligence


    def getIntelligence(self):
        """
        Get the current intelligence, be it ephemeral or enduring.
        """
        if self._ephemeralIntelligence is not None:
            return self._ephemeralIntelligence
        return self._enduringIntelligence



class LocationLighting(item.Item, _Enhancement):
    """
    A L{LocationLighting} is an enhancement for a location which allows the
    location's description and behavior to depend on its lighting.  While
    L{LocationLighting} includes its own ambient lighting number, it is not
    really a light source, it's just a location which is I{affected by} light
    sources; for lighting, you should use L{LightSource}.

    By default, in Imaginary, rooms are considered by to be lit to an
    acceptable level that actors can see and interact with both the room and
    everything in it without worrying about light.  By contrast, any room that
    can be dark needs to have a L{LocationLighting} installed.  A room affected
    by a L{LocationLighting} which is lit will behave like a normal room, but a
    room affected by a L{LocationLighting} with no available light sources will
    prevent players from performing actions which require targets that need to
    be seen, and seeing the room's description.
    """

    implements(iimaginary.ILocationLinkAnnotator)
    powerupInterfaces = (iimaginary.ILocationLinkAnnotator,)

    candelas = attributes.integer(
        doc="""
        The ambient luminous intensity in candelas.

        See U{http://en.wikipedia.org/wiki/Candela}.
        """, default=100, allowNone=False)

    thing = attributes.reference(
        doc="""
        The location being affected by lighting.
        """,
        reftype=Thing,
        allowNone=False,
        whenDeleted=attributes.reference.CASCADE)

    def getCandelas(self):
        """
        Sum the candelas of all light sources within a limited distance from
        the location this is installed on and return the result.
        """
        sum = self.candelas
        for candle in self.thing.idea.obtain(
            Proximity(1, ProviderOf(iimaginary.ILightSource))):
            sum += candle.candelas
        return sum


    def annotationsFor(self, link, idea):
        """
        Yield a L{_PossiblyDark} annotation for all links pointing to objects
        located in the C{thing} attribute of this L{LocationLighting}.
        """
        if link.target is idea:
            yield _PossiblyDark(self)



class _DarkLocationProxy(structlike.record('thing')):
    """
    An L{IVisible} implementation for darkened locations.
    """

    implements(iimaginary.IVisible)

    def visualizeWithContents(self, paths):
        """
        Return a L{language.Description} that tells the player they can't see.
        """
        return language.Description(
            title=u"Blackness",
            exits=None,
            description=u"You cannot see anything because it is very dark.",
            components=None
        )



    def isViewOf(self, thing):
        """
        Implement L{IVisible.isViewOf} to delegate to this
        L{_DarkLocationProxy}'s L{Thing}'s L{IVisible.isViewOf}.

        In other words, this L{_DarkLocationProxy} C{isViewOf} its C{thing}.
        """
        return self.thing.isViewOf(thing)



class LightSource(item.Item, _Enhancement):
    """
    A simple implementation of L{ILightSource} which provides a fixed number of
    candelas of luminous intensity, assumed to be emitted uniformly in all
    directions.
    """

    implements(iimaginary.ILightSource)
    powerupInterfaces = (iimaginary.ILightSource,)

    candelas = attributes.integer(
        doc="""
        The luminous intensity in candelas.

        See U{http://en.wikipedia.org/wiki/Candela}.
        """, default=1, allowNone=False)

    thing = attributes.reference(
        doc="""
        The physical body emitting the light.
        """,
        reftype=Thing,
        allowNone=False,
        whenDeleted=attributes.reference.CASCADE)



class _PossiblyDark(structlike.record("lighting")):
    """
    A L{_PossiblyDark} is a link annotation which specifies that the target of
    the link may be affected by lighting.

    @ivar lighting: the lighting for a particular location.

    @type lighting: L{LocationLighting}
    """

    implements(iimaginary.IWhyNot, iimaginary.ILitLink)

    def tellMeWhyNot(self):
        """
        Return a helpful message explaining why something may not be accessible
        due to poor lighting.
        """
        return "It's too dark to see."


    def isItLit(self, path, result):
        """
        Determine if the given result, viewed via the given path, appears to be
        lit.

        @return: L{True} if the result should be lit, L{False} if it is dark.

        @rtype: C{bool}
        """
        # XXX wrong, we need to examine this exactly the same way applyLighting
        # does.  CanSee and Visibility *are* the same object now so it is
        # possible to do.
        if self.lighting.getCandelas():
            return True
        litThing = list(path.eachTargetAs(iimaginary.IThing))[-1]
        if _eventuallyContains(self.lighting.thing, litThing):
            val = litThing is self.lighting.thing
            return val
        else:
            return True


    def whyNotLit(self):
        """
        Return an L{iimaginary.IWhyNot} provider explaining why the target of
        this link is not lit.  (Return 'self', since L{_PossiblyDark} is an
        L{iimaginary.IWhyNot} provider itself.)
        """
        return self


    def applyLighting(self, litThing, eventualTarget, requestedInterface):
        """
        Implement L{iimaginary.ILitLink.applyLighting} to return a
        L{_DarkLocationProxy} for the room lit by this
        L{_PossiblyDark.lighting}, C{None} for any items in that room, or
        C{eventualTarget} if the target is in a different place.
        """
        if self.lighting.getCandelas():
            return eventualTarget
        elif (eventualTarget is self.lighting.thing and
              requestedInterface is iimaginary.IVisible):
            return _DarkLocationProxy(self.lighting.thing)
        elif _eventuallyContains(self.lighting.thing, litThing):
            return None
        else:
            return eventualTarget
