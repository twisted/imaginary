# -*- test-case-name: imaginary -*-

"""
This module implements a highly abstract graph-traversal system for actions and
events to locate the objects which can respond to them.  The top-level
entry-point to this system is L{Idea.obtain}.

It also implements several basic retrievers related to visibility and physical
reachability.
"""

from zope.interface import implements

from characteristic import with_cmp, with_init, attributes

from epsilon.structlike import record

from imaginary.iimaginary import (
    INameable, ILitLink, IThing, IObstruction, IElectromagneticMedium,
    IDistance, IRetriever, IExit)



@attributes(["source", "target", "annotations"], create_init=False)
class Link(object):
    """
    A L{Link} is a connection between two L{Idea}s in a L{Path}.

    @ivar annotations: The domain-specific simulation annotations that apply to
        this link.
    @type annotations: L{list}
    """

    def __init__(self, source, target):
        """
        @param source: the idea that this L{Link} originated from.
        @type source: L{Idea}

        @param target: the idea that this L{Link} refers to.
        @type target: L{Idea}
        """
        self.source = source
        self.target = target
        self.annotations = []


    def annotate(self, annotations):
        """
        Annotate this link with a list of annotations.
        """
        self.annotations.extend(annotations)


    def of(self, interface):
        """
        Yield all annotations on this link which provide the given interface.
        """
        for annotation in self.annotations:
            provider = interface(annotation, None)
            if provider is not None:
                yield provider



@with_cmp(["links"])
@with_init(["links"])
class Path(object):
    """
    A list of L{Link}s.

    @ivar links: A L{list} of L{Link}s describing a path through the simulation
        graph.  The order is significant.  The target of each link is the
        source of the subsequent link.
    @type links: L{list} of L{Link}s
    """

    def of(self, interface):
        """
        @return: an iterator of providers of interfaces, adapted from each link
            in this path.
        """
        for link in self.links:
            for annotation in link.of(interface):
                yield annotation


    def eachSubPath(self):
        """
        Iterate over each path which is a prefix of this path.

        @return: A generator which yields L{Path} instances.  The first
            instance yielded is a L{Path} with only the first L{Link} of this
            path.  The second instance yielded has the first and second
            L{Link}s of this path.  This pattern continues until a L{Path} with
            the same L{Links} as this L{Path} is yielded.

        """
        for x in range(1, len(self.links) + 1):
            yield Path(links=self.links[:x])


    def eachTargetAs(self, interface):
        """
        @return: an iterable of all non-None results of each L{Link.targetAs}
            method in this L{Path}'s C{links} attribute.
        """
        for link in self.links:
            provider = interface(link.target.delegate, None)
            if provider is not None:
                yield provider


    def targetAs(self, interface):
        """
        Retrieve the target of the last link of this path, its final
        destination, as a given interface.

        @param interface: the interface to retrieve.
        @type interface: L{zope.interface.interfaces.IInterface}

        @return: the last link's target, adapted to the given interface, or
            C{None} if no appropriate adapter or component exists.
        @rtype: C{interface} or C{NoneType}
        """
        return interface(self.links[-1].target.delegate, None)


    def isCyclic(self):
        """
        Determine if this path is cyclic, to avoid descending down infinite
        loops.

        @return: a boolean indicating whether this L{Path} is cyclic or not,
            i.e. whether the L{Idea} its last link points at is the source of
            any of its links.
        """
        if len(self.links) < 2:
            return False
        return (self.links[-1].target in (x.source for x in self.links))


    def to(self, link):
        """
        Create a new path, extending this one by one new link.
        """
        return Path(links=self.links + [link])


    def __repr__(self):
        """
        @return: an expanded pretty-printed representation of this Path,
        suitable for debugging.
        """
        s = 'Path('
        for link in self.links:
            dlgt = link.target.delegate
            src = link.source.delegate
            s += "\n\t"
            s += repr(getattr(src, 'name', src))
            s += " => "
            s += repr(getattr(dlgt, 'name', dlgt))
            s += " "
            s += repr(link.annotations)
        s += ')'
        return s



class Idea(record("delegate linkers annotators")):
    """
    Consider a person's activities with the world around them as having two
    layers.  One is a physical layer, out in the world, composed of matter and
    energy. The other is a cognitive layer, internal to the person, composed
    of ideas about that matter and energy.

    For example, when a person wants to sit in a wooden chair, they must first
    visually locate the arrangement of wood in question, make the determination
    of that it is a "chair" based on its properties, and then perform the
    appropriate actions to sit upon it.

    However, a person may also interact with symbolic abstractions rather than
    physical objects.  They may read a word, or point at a window on a computer
    screen.  An L{Idea} is a representation of the common unit that can be
    referred to in this way.

    Both physical and cognitive layers are present in Imaginary.  The cognitive
    layer is modeled by L{imaginary.idea}.  The physical layer is modeled by a
    rudimentary point-of-interest simulation in L{imaginary.objects}.  An
    L{imaginary.thing.Thing} is a physical object; an L{Idea} is a node in a
    non-physical graph, related by links that are annotated to describe the
    nature of the relationship between it and other L{Idea}s.

    L{Idea} is the most abstract unit of simulation.  It does not have any
    behavior or simulation semantics of its own; it merely ties together
    different related systems.

    An L{Idea} is composed of a C{delegate}, which is an object that implements
    simulation-defined interfaces; a list of L{ILinkContributor}s, which
    produce L{Link}s to other L{Idea}s, an a set of C{ILinkAnnotator}s, which
    apply annotations (which themselves implement simulation-defined
    link-annotation interfaces) to those links.

    Each L{imaginary.thing.Thing} has a corresponding L{Idea} to represent it
    in the simulation.  The physical simulation defines only a few types of
    links: objects have links to their containers, containers have links to
    their contents, rooms have links to their exits, exits have links to their
    destinations.  Any L{imaginary.thing.Thing} can have a powerup applied to
    it which adds to the list of linkers or annotators for its L{Idea},
    however, which allows users to create arbitrary objects.

    For example, the target of the "look" action must implement
    L{imaginary.iimaginary.IVisible}, but need not be a
    L{iimaginary.objects.Thing}.  A simulation might want to provide a piece of
    graffiti that you could look at, but would not be a physical object, in the
    sense that you couldn't pick it up, weigh it, push it, etc.  Such an object
    could be implemented as a powerup for both
    L{imaginary.iimaginary.IDescriptionContributor}, which would impart some
    short flavor text to the room, and L{imaginary.iimaginary.IVisible}, which
    would be an acceptable target of 'look'.  The
    L{imaginary.iimaginary.IVisible} implementation could even be an in-memory
    object, not stored in the database at all; and there could be different
    implementations for different observers, depending on their level of
    knowledge about the in-world graffiti.

    @ivar delegate: this object is the object which may be adaptable to a set
        of interfaces.  This L{Idea} delegates all adaptation to its delegate.
        In many cases (when referring to a physical object), this will be an
        L{imaginary.thing.Thing}, but not necessarily.

    @ivar linkers: a L{list} of L{ILinkContributor}s which are used to gather
        L{Link}s from this L{Idea} during L{Idea.obtain} traversal.

    @ivar annotators: a L{list} of L{ILinkAnnotator}s which are used to annotate
        L{Link}s gathered from this L{Idea} via the C{linkers} list.
    """

    def __init__(self, delegate):
        super(Idea, self).__init__(delegate, [], [])


    def _allLinks(self):
        """
        Return an iterator of all L{Links} away from this idea.
        """
        for linker in self.linkers:
            for link in linker.links():
                yield link


    def _applyAnnotators(self, linkiter):
        """
        Apply my list of annotators to each link in the given iterable.
        """
        for link in linkiter:
            self._annotateOneLink(link)
            yield link


    def _annotateOneLink(self, link):
        """
        Apply all L{ILinkAnnotator}s in this L{Idea}'s C{annotators} list.
        """
        allAnnotations = []
        for annotator in self.annotators:
            # XXX important to test: annotators shouldn't mutate the links.
            # The annotators show up in a non-deterministic order, so in order
            # to facilitate a consistent view of the link in annotationsFor(),
            # all annotations are applied at the end.
            annotations = list(annotator.annotationsFor(link, self))
            allAnnotations.extend(annotations)
        link.annotate(allAnnotations)


    def obtain(self, retriever):
        """
        Traverse the graph of L{Idea}s, starting with C{self}, looking for
        objects which the given L{IRetriever} can retrieve.

        The graph will be traversed by looking at all the links generated by
        this L{Idea}'s C{linkers}, only continuing down those links for which
        the given L{IRetriever}'s C{shouldKeepGoing} returns L{True}.

        @param retriever: an object which will be passed each L{Path} in turn,
            discovered during traversal of the L{Idea} graph.  If any
            invocation of L{IRetriever.retrieve} on this parameter should
            succeed, that will be yielded as a result from this method.
        @type retriever: L{IRetriever}

        @return: a generator which yields the results of C{retriever.retrieve}
            which are not L{None}.
        """
        return ObtainResult(self, retriever)


    def _doObtain(self, retriever, path, reasonsWhyNot):
        """
        A generator that implements the logic for obtain()
        """
        if path is None:
            # Special case: we only get a self->self link if we are the
            # beginning _and_ the end.
            path = Path(links=[])
            selfLink = Link(source=self, target=self)
            self._annotateOneLink(selfLink)
            finalPath = path.to(selfLink)
        else:
            finalPath = Path(links=path.links[:])
            self._annotateOneLink(finalPath.links[-1])

        result = retriever.retrieve(finalPath)
        objections = set(retriever.objectionsTo(finalPath, result))
        reasonsWhyNot |= objections
        if result is not None:
            if not objections:
                yield result

        for link in self._applyAnnotators(self._allLinks()):
            subpath = path.to(link)
            if subpath.isCyclic():
                continue
            if retriever.shouldKeepGoing(subpath):
                for obtained in link.target._doObtain(retriever, subpath, reasonsWhyNot):
                    yield obtained



class ObtainResult(record("idea retriever")):
    """
    The result of L{Idea.obtain}, this provides an iterable of results.

    @ivar reasonsWhyNot: If this iterator has already been exhausted, this will
        be a C{set} of L{IWhyNot} objects explaining possible reasons why there
        were no results.  For example, if the room where the player attempted
        to obtain targets is dark, this may contain an L{IWhyNot} provider.
        However, until this iterator has been exhausted, it will be C{None}.
    @type reasonsWhyNot: C{set} of L{IWhyNot}, or C{NoneType}

    @ivar idea: the L{Idea} that L{Idea.obtain} was invoked on.
    @type idea: L{Idea}

    @ivar retriever: The L{IRetriever} that L{Idea.obtain} was invoked with.
    @type retriever: L{IRetriever}
    """

    reasonsWhyNot = None

    def __iter__(self):
        """
        A generator which yields each result of the query, then sets
        C{reasonsWhyNot}.
        """
        reasonsWhyNot = set()
        for result in self.idea._doObtain(self.retriever, None, reasonsWhyNot):
            yield result
        self.reasonsWhyNot = reasonsWhyNot



class DelegatingRetriever(object):
    """
    A delegating retriever, so that retrievers can be easily composed.

    See the various methods marked for overriding.

    @ivar retriever: A retriever to delegate most operations to.
    @type retriever: L{IRetriever}
    """

    implements(IRetriever)

    def __init__(self, retriever):
        """
        Create a delegator with a retriever to delegate to.
        """
        self.retriever = retriever


    def moreObjectionsTo(self, path, result):
        """
        Override in subclasses to yield objections to add to this
        L{DelegatingRetriever}'s C{retriever}'s C{objectionsTo}.

        By default, offer no additional objections.
        """
        return []


    def objectionsTo(self, path, result):
        """
        Concatenate C{self.moreObjectionsTo} with C{self.moreObjectionsTo}.
        """
        for objection in self.retriever.objectionsTo(path, result):
            yield objection
        for objection in self.moreObjectionsTo(path, result):
            yield objection


    def shouldStillKeepGoing(self, path):
        """
        Override in subclasses to halt traversal via a C{False} return value for
        C{shouldKeepGoing} if this L{DelegatingRetriever}'s C{retriever}'s
        C{shouldKeepGoing} returns C{True}.

        By default, return C{True} to keep going.
        """
        return True


    def shouldKeepGoing(self, path):
        """
        If this L{DelegatingRetriever}'s C{retriever}'s C{shouldKeepGoing}
        returns C{False} for the given path, return C{False} and stop
        traversing.  Otherwise, delegate to C{shouldStillKeepGoing}.
        """
        return (self.retriever.shouldKeepGoing(path) and
                self.shouldStillKeepGoing(path))


    def resultRetrieved(self, path, retrievedResult):
        """
        A result was retrieved.  Post-process it if desired.

        Override this in subclasses to modify (non-None) results returned from
        this L{DelegatingRetriever}'s C{retriever}'s C{retrieve} method.

        By default, simply return the result retrieved.
        """
        return retrievedResult


    def retrieve(self, path):
        """
        Delegate to this L{DelegatingRetriever}'s C{retriever}'s C{retrieve}
        method, then post-process it with C{resultRetrieved}.
        """
        subResult = self.retriever.retrieve(path)
        if subResult is None:
            return None
        return self.resultRetrieved(path, subResult)



class Proximity(DelegatingRetriever):
    """
    L{Proximity} is a retriever which will continue traversing any path which
    is shorter than its proscribed distance, but not any longer.

    @ivar distance: the distance, in meters, to query for.

    @type distance: L{float}
    """

    def __init__(self, distance, retriever):
        DelegatingRetriever.__init__(self, retriever)
        self.distance = distance


    def shouldStillKeepGoing(self, path):
        """
        Implement L{IRetriever.shouldKeepGoing} to stop for paths whose sum of
        L{IDistance} annotations is greater than L{Proximity.distance}.
        """
        dist = sum(vector.distance for vector in path.of(IDistance))
        ok = (self.distance >= dist)
        return ok



class Reachable(DelegatingRetriever):
    """
    L{Reachable} is a navivator which will object to any path with an
    L{IObstruction} annotation on it.
    """

    def moreObjectionsTo(self, path, result):
        """
        Yield an objection from each L{IObstruction.whyNot} method annotating
        the given path.
        """
        if result is not None:
            for obstruction in path.of(IObstruction):
                yield obstruction.whyNot()



class Traversability(DelegatingRetriever):
    """
    A path is only traversible if it terminates in *one* exit.  Once you've
    gotten to an exit, you have to stop, because the player needs to go through
    that exit to get to the next one.
    """

    def shouldStillKeepGoing(self, path):
        """
        Stop at the first exit that you find.
        """
        for index, target in enumerate(path.eachTargetAs(IExit)):
            if index > 0:
                return False
        return True



class Vector(record('distance direction')):
    """
    A L{Vector} is a link annotation which remembers a distance and a
    direction; for example, a link through a 'north' exit between rooms will
    have a direction of 'north' and a distance specified by that
    L{imaginary.objects.Exit} (defaulting to 1 meter).
    """

    implements(IDistance)



class ProviderOf(record("interface")):
    """
    L{ProviderOf} is a retriever which will retrieve the facet which provides
    its C{interface}, if any exists at the terminus of the path.

    @ivar interface: The interface which defines the type of values returned by
        the C{retrieve} method.
    @type interface: L{zope.interface.interfaces.IInterface}
    """

    implements(IRetriever)

    def retrieve(self, path):
        """
        Retrieve the target of the path, as it provides the interface specified
        by this L{ProviderOf}.

        @return: the target of the path, adapted to this retriever's interface,
            as defined by L{Path.targetAs}.

        @rtype: L{ProviderOf.interface}
        """
        return path.targetAs(self.interface)


    def objectionsTo(self, path, result):
        """
        Implement L{IRetriever.objectionsTo} to yield no objections.
        """
        return []


    def shouldKeepGoing(self, path):
        """
        Implement L{IRetriever.shouldKeepGoing} to always return C{True}.
        """
        return True



class AlsoKnownAs(record('name')):
    """
    L{AlsoKnownAs} is an annotation that indicates that the link it annotates
    is known as a particular name.

    @ivar name: The name that this L{AlsoKnownAs}'s link's target is also known
        as.
    @type name: C{unicode}
    """

    implements(INameable)

    def knownTo(self, observer, name):
        """
        An L{AlsoKnownAs} is known to all observers as its C{name} attribute.
        """
        return (self.name == name)



class Named(DelegatingRetriever):
    """
    A retriever which wraps another retriever, but yields only results known to
    a particular observer by a particular name.

    @ivar name: the name to search for.

    @ivar observer: the observer who should identify the target by the name
        this L{Named} is searching for.
    @type observer: L{Thing}
    """

    def __init__(self, name, retriever, observer):
        DelegatingRetriever.__init__(self, retriever)
        self.name = name
        self.observer = observer


    def resultRetrieved(self, path, subResult):
        """
        Invoke C{retrieve} on the L{IRetriever} which we wrap, but only return
        it if the L{INameable} target of the given path is known as this
        L{Named}'s C{name}.
        """
        if isKnownTo(self.observer, path, self.name):
            return subResult
        else:
            return None



def isKnownTo(observer, path, name):
    """
    Is the given path's target known to the given observer by the given name
    (as retrieved via the given path?)

    For example: a room may be known as the name 'north' but only if you're
    standing south of it, so the path via which you retrieved it (starting to
    the south) is relevant.
    """
    named = path.targetAs(INameable)
    # TODO: don't look at the last link only.  There should be a specific
    # "alias" annotation which knows how to alias a specific target; we should
    # give it targetAs(something) so the alias itself can compare.
    # (Introducing additional links into traversal should never break things.)
    allAliases = list(path.links[-1].of(INameable))
    if named is not None:
        allAliases += [named]
    for alias in allAliases:
        if alias.knownTo(observer, name):
            return True
    return False



class CanSee(DelegatingRetriever):
    """
    Wrap a L{ProviderOf}, yielding the results that it would yield, but
    applying lighting to the ultimate target based on the last L{IThing} the
    path.

    @ivar retriever: The lowest-level retriever being wrapped.

    @type retriever: L{ProviderOf} (Note: it might be a good idea to add an
        'interface' attribute to L{IRetriever} so this no longer depends on a
        more specific type than other L{DelegatingRetriever}s, to make the
        order of composition more flexible.)
    """
    def __init__(self, retriever, observer=None):
        """
        @param observer: The L{Thing} which is trying to see things.
        """
        DelegatingRetriever.__init__(self, retriever)
        self.observer = observer


    def resultRetrieved(self, path, subResult):
        """
        Post-process retrieved results by determining if lighting applies to
        them.
        """
        litlinks = list(path.of(ILitLink))
        if not litlinks:
            return subResult
        # XXX what if there aren't any IThings on the path?
        litThing = list(path.eachTargetAs(IThing))[-1]
        # you need to be able to look from a light room to a dark room, so only
        # apply the most "recent" lighting properties.
        return litlinks[-1].applyLighting(
            litThing, subResult, self.retriever.interface)


    def shouldStillKeepGoing(self, path):
        """
        Don't keep going through links that are opaque to the observer.
        """
        for opacity in path.of(IElectromagneticMedium):
            if opacity.isOpaque(self.observer):
                return False
        return True


    def moreObjectionsTo(self, path, result):
        """
        Object to paths which have L{ILitLink} annotations which are not lit.
        """
        for lighting in path.of(ILitLink):
            if not lighting.isItLit(path):
                tmwn = lighting.whyNotLit()
                yield tmwn
