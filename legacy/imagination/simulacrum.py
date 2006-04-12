# -*- test-case-name: imagination.test.test_simu -*-

"""

From Webster's Revised Unabridged Dictionary (1913) [web1913]:

  Simulacrum \Sim`u*la\"crum\, n.; pl. {Simulacra}. [L. See
     {Simulate}.]
     A likeness; a semblance; a mock appearance; a sham; -- now
     usually in a derogatory sense.

           Beneath it nothing but a great simulacrum. --Thackeray.

"""

__metaclass__ = type
from zope import interface
from twisted.python import log
from imagination.text.english import INoun
from imagination.facets import Facet, registerAdapter
from imagination import iimagination

class ICollector(interface.Interface):
    def find(asker, interface, criteria):
        """Return implementation objects that meet the criteria's criteria.

        Only objects which implement the given interface are returned.
        Only objects for which the IImplementorCriterion predicate
        returns True are returned.

        Implementation objects which are considered for return are
        dependent on the implementation of this interface.
        """

    def more(asker, interface, criteria):
        """Return collector objects reachable from this object.

        Only collectors which may 'find' (see above) implementors of
        the given interface are returned.  Note: not collectors which
        *will* find implementors of this interface, merely those which
        can be searched in the context of the criterion passed in.

        If the criteria provide an ICollectorCriterion, then only collectors
        for which it returns True are returned.

        Collector objects which are considered for return are
        dependent on the implementation of this interface.

        An iterable of two-tuples of (distance, collector) is returned.
        """


class ICallableCriterion(interface.Interface):
    """I am the simplest type of criterion; one which can be called on each
    possible implementor to determine whether it is correct or not.
    """
    def __call__(implementor):
        """
        Return True if the implementor meets your criterion, otherwise False.
        """

import types

def _null(o):
    return o

registerAdapter(_null, types.FunctionType, ICallableCriterion)
registerAdapter(_null, types.MethodType, ICallableCriterion)

def _evermore(start, asker, interface, criterion, radius):
    seen = {}
    toQuery = [(0, start)]
    while toQuery:
        distance, collector = toQuery.pop()
        if seen.has_key(id(collector)) or distance > radius:
            continue
        else:
            seen[id(collector)] = collector
            yield distance, collector
        for subdist, subcoll in collector.more(asker, interface, criterion):
            toQuery.append((distance + subdist, subcoll))

def _collect(asker, start, interface, criterion, radius=2):
    """returns an iterable of 'distance', 'implementor' for each 'implementor'
    of 'interface' found in the given distance 'radius'.

    radius is measured in 'number of graph jumps'.  for real distances,
    implement a smart container that understands a distance-implementing
    criterion.
    """
    seen = {}
    for distance, collector in _evermore(start, asker, interface, criterion, radius):
        for implementor in collector.find(asker, interface, criterion):
            if id(implementor) not in seen:
                yield distance, implementor
                seen[id(implementor)] = True

class IKnownAs(interface.Interface):
    name = interface.Attribute("The name to look for.")
    collector = interface.Attribute("The collector to evaluate names for")

class KnownAs(object):
    """I am a criterion that evaluates to true when an object's name as
    described to a particular collector matches mine.
    """

    interface.implements(ICallableCriterion, IKnownAs)

    def __init__(self, name, collector):
        self.name = name
        self.collector = collector

    def __call__(self, impl):
        if INoun(impl).knownAs(self.name, self.collector):
            return True
        return False

def always(obj):
    """One-argument callable that always returns true.  A very basic callable
    criterion.
    """
    return True

def lookFor(collector, name, iface, radius=2):
    """Return implementation objects reachable from the given collector.

    Only objects which are known as the given name by the given collector
    are returned.  Only objects which implement the given interface are
    returned.  Only implementation objects returned from the L{find} method
    of collectors within the given radius are returned.
    """
    return collect(collector, iface,
                   KnownAs(name, collector),
                   radius)


def collect(self, interface, criterion, radius=2):
    """Return implementation objects reachable from this object.

    Only objects which implement the given interface are returned.
    Only objects for which the given criterion predicate (XXX - it
    will not be a predicate forever) returns True are returned.

    Implementation objects returned from the L{find} method of
    collector objects within the given radius are considered for return.

    An iterable of two-tuples of (distance, implementation) is returned.
    """
    return _collect(ICollector(self), ICollector(self), interface, criterion, radius)


class ISeer(interface.Interface):
    def see(event):
        "see something"

class IHearer(interface.Interface):
    def hear(event):
        """Do you hear that, Mr Anderson? It is the sound of
        inevitabilty. It is the sound of your death.
        """

class Sensibility(Facet):
    """
    Default component for sensing events that we don't really give a crap about.
    """
    interface.implements(ISeer, IHearer)

    def see(self, event):
        iimagination.IUI(self.original).presentEvent(ISeer, event)

    def hear(self, event):
        iimagination.IUI(self.original).presentEvent(IHearer, event)
