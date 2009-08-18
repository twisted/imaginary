# -*- test-case-name: imaginary.test.test_illumination -*-

"""
This module implements a highly abstract graph-traversal system for actions and
events to locate the objects which can respond to them.  The top-level
entry-point to this system is L{Idea.obtain}.
"""

from itertools import chain

from zope.interface import implements
from epsilon.structlike import record

from imaginary.iimaginary import (
    INameable, ILitLink, IThing, IObstruction, IElectromagneticMedium,
    IDistance, IRetriever, IExit)



class Link(record("source target")):
    """
    A L{Link} is a connection between two L{Idea}s in a L{Path}.

    @ivar source: the idea that this L{Link} originated from.

    @type source: L{Idea}

    @ivar target: the idea that this L{Link} refers to.

    @type target: L{Idea}
    """

    def __init__(self, *a, **k):
        super(Link, self).__init__(*a, **k)
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



class Path(record('links')):
    """
    A list of L{Link}s.
    """

    def of(self, interface):
        """
        @return: an iterator of providers of interfaces, adapted from each link
            in this path.
        """
        for link in self.links:
            for annotation in link.of(interface):
                yield annotation


    def _eachSubPath(self):
        """
        For a L{Path} containing N links, yield N paths.  For example, if you
        have a L{Path} like::

            (a->b) (b->c) (c->d)

        this will yield the paths::

            (a->b)
            (a->b) (b->c)
            (a->b) (b->c) (c->d)
        """
        for x in range(len(self.links)):
            op = Path(self.links[:x+1])
            yield op


    def eachTargetAs(self, interface):
        """
        @return: an iterable of all non-None results of each L{Link.targetAs}
            method in this L{Path}'s C{links} attribute.
        """
        for path in self._eachSubPath():
            provider = path.targetAs(interface)
            if provider is not None:
                yield provider


    def targetAs(self, interface):
        """
        @return: the last link's target.
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
        return Path(self.links + [link])


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
            s += "=>"
            s += repr(getattr(dlgt, 'name', dlgt))
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
    their contents, rooms have links to their exits, exits have links to thier
    destinations.  Any L{imaginary.thing.Thing} can have a powerup applied to
    it which adds to the list of linkers or annotators for its L{Idea},
    however, which allows users to create arbitrary objects.

    For example, the target of the "look" action must implement
    L{imaginary.iimaginary.IVisible}, but need not be a
    L{iimaginary.objects.Thing}.  A simulation might want to provide a piece of
    graffiti that you could look at, but would not be a physical object, in the
    sense that you couldn't pick it up, weigh it, push it, etc.  Such an object
    could be implemented as a powerup for both
    L{imaginary.iimaginary.IDescriptionContributor} (to some short flavor test
    to the room) and L{imaginary.iimaginary.IVisible} which would be an
    acceptable target of 'look'.  The L{imaginary.iimaginary.IVisible}
    implementation could even be an in-memory object, not stored in the
    database at all; and there could be different implementations for different
    observers, depending on their level of knowledge about the in-world
    graffiti.

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
            allAnnotations.extend(annotator.annotationsFor(link, self))
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
            path = Path([])
            selfLink = Link(self, self)
            self._annotateOneLink(selfLink)
            finalPath = path.to(selfLink)
        else:
            finalPath = Path(path.links[:])
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



class _Delegator(object):
    """
    A delegating retriever, so that retrievers can be easily composed.
    """

    implements(IRetriever)

    def __init__(self, retriever):
        """
        Create a delegator with a retriever to delegate to.
        """
        self.retriever = retriever


    def _moreObjectionsTo(self, path, result):
        """
        
        """
        return []


    def objectionsTo(self, path, result):
        """
        Delegate to _moreObjectionsTo.
        """
        for objection in self.retriever.objectionsTo(path, result):
            yield objection
        for objection in self._moreObjectionsTo(path, result):
            yield objection


    def _shouldStillKeepGoing(self, path):
        """
        
        """
        return True


    def shouldKeepGoing(self, path):
        """
        
        """
        return (self.retriever.shouldKeepGoing(path) and
                self._shouldStillKeepGoing(path))


    def _reallyRetrieve(self, path, subResult):
        """
        
        """
        return subResult


    def retrieve(self, path):
        """
        
        """
        subResult = self.retriever.retrieve(path)
        if subResult is None:
            return None
        return self._reallyRetrieve(path, subResult)



class Proximity(_Delegator):
    """
    L{Proximity} is a retriever which will continue traversing any path which
    is shorter than its proscribed distance, but not any longer.
    """

    implements(IRetriever)

    def __init__(self, distance, retriever):
        """
        
        """
        _Delegator.__init__(self, retriever)
        self.distance = distance


    def _shouldStillKeepGoing(self, path):
        """
        Implement L{IRetriever.shouldKeepGoing} to stop for paths whose sum of
        L{IDistance} annotations is greater than L{Proximity.distance}.
        """
        dist = sum(vector.distance for vector in path.of(IDistance))
        ok = (self.distance >= dist)
        return ok



class Reachable(_Delegator):
    """
    L{Reachable} is a navivator which will object to any path with an
    L{IObstruction} annotation on it.
    """

    implements(IRetriever)

    def _moreObjectionsTo(self, path, result):
        """
        Yield an objection from each L{IObstruction.whyNot} method annotating
        the given path.
        """
        if result is not None:
            for obstruction in path.of(IObstruction):
                yield obstruction.whyNot()



class Traversability(_Delegator):
    """
    A path is only traversible if it terminates in *one* exit.  Once you've
    gotten to an exit, you have to stop, because the player needs to go through
    that exit to get to the next one.
    """

    def _shouldStillKeepGoing(self, path):
        """
        Stop at the first exit that you find.
        """
        for index, target in enumerate(path.eachTargetAs(IExit)):
            if index > 0:
                return False
        return True



class Opacity(record("opaque")):
    """
    A link annotation that implements L{IElectromagneticMedium} to return a
    simple observer-independent flag.

    Note: a better implementation would take into account wavelengths of
    ambient light, and the observer's vision.
    """

    implements(IElectromagneticMedium)

    def opaqueTo(self, observer):
        """
        Is this medium opaque to the given observer?  Actually, ignore the
        observer and always return this L{Opacity}'s C{opaque} flag.
        """
        return self.opaque



class Vector(record('distance direction')):
    """
    A L{Vector} is a link annotation which remembers a distance and a
    direction; for example, a link through a 'north' exit between rooms will
    have a direction of 'north' and a distance specified by that
    L{imaginary.objects.Exit} (defaulting to 1 meter).
    """

    implements(IDistance)


# Application

class ProviderOf(record("interface")):
    """
    L{ProviderOf} is a retriever which will retrieve the facet which provides
    its C{interface}, if any exists at the terminus of the path.
    """

    implements(IRetriever)

    def __init__(self, *args, **kw):
        """
        Initialize a L{ProviderOf} retriever, starting with an empty list of
        reasons why it hasn't found anything.
        """
        super(ProviderOf, self).__init__(*args, **kw)


    def retrieve(self, path):
        """
        Retrieve the target of the path, as it provides the interface specified
        by this L{ProviderOf}.
        """
        return path.targetAs(self.interface)

    def objectionsTo(self, path, result):
        """
        
        """
        return []

    def shouldKeepGoing(self, path):
        """
        
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



class Named(_Delegator):
    """
    A retriever which wraps another retriever, but yields only results known to
    a particular observer by a particular name.
    """

    implements(IRetriever)

    def __init__(self, name, retriever, observer):
        """
        
        """
        _Delegator.__init__(self, retriever)
        self.name = name
        self.observer = observer


    def _reallyRetrieve(self, path, subResult):
        """
        Invoke C{retrieve} on the L{IRetriever} which we wrap, but only return
        it if the L{INameable} target of the given path is known as this
        L{Named}'s C{name}.
        """
        named = path.targetAs(INameable)
        allAliases = list(path.links[-1].of(INameable))
        if named is not None:
            allAliases += [named]
        for alias in allAliases:
            if alias.knownTo(self.observer, self.name):
                return subResult
        return None



class CanSee(_Delegator):
    """
    Wrap a L{ProviderOf}, yielding the results that it would yield, but
    applying lighting to the ultimate target based on the last L{IThing} the
    path.
    """

    implements(IRetriever)

    def __init__(self, retriever, observer=None):
        """
        
        """
        _Delegator.__init__(self, retriever)
        self.observer = observer


    def _reallyRetrieve(self, path, subResult):
        """
        Implement L{IRetriever.retrieve} to apply the last L{ILitLink}'s
        lighting to the ultimate resulting object.
        """
        litlinks = list(path.of(ILitLink))
        if not litlinks:
            return subResult
        # XXX what if there aren't any IThings on the path?
        litThing = list(path.eachTargetAs(IThing))[-1]
        # you need to be able to look from a light room to a dark room, so only
        # apply the most "recent" lighting properties.
        return litlinks[-1].applyLighting(
            litThing,
            subResult,
            # XXX this property is violating encapsulation a bit: see above in
            # Named.interface.
            self.retriever.interface)


    def _shouldStillKeepGoing(self, path):
        """
        Implement L{IRetriever.shouldKeepGoing} to not keep going on links that
        are opaque to the observer.
        """
        for opacity in path.of(IElectromagneticMedium):
            if opacity.opaqueTo(self.observer):
                return False
        return True


    def _moreObjectionsTo(self, path, result):
        """
        Implement L{IRetriever.objectionsTo} to object to paths which have
        L{ILitLink} annotations which are not lit.
        """
        for lighting in path.of(ILitLink):
            if not lighting.isItLit(path, result):
                tmwn = lighting.whyNotLit()
                yield tmwn



