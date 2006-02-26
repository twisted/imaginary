"""
All the crazy ideas that we came up with that we want simulacrum to support!

TODO: Actually try running this code.
"""

from twisted.python import components

from imagination import simulacrum, containment, architecture, physical, observation
from imagination.text import english


def wrapper(o, iface, adapter):
    """
    Create a wrapper for some componentized that has some interface overridden.

    XXX probably extend this to support multiple ifaces at a
    time. hmm.  wrap(o)[iface:adapterINST, iface:adapterINST], almost
    the same as templates. That'd be good. Later.
    """
    c = components.Componentized()
    # XXX hrng, this is fragile. What's another approach???
    # Need IComponentized(o)
    c._adapterCache = o.original._adapterCache
    c.setComponent(iface, adapter)
    return c


class ShimmeringPortal(architecture.Portal, containment.Container):
    """
    A portal that obscures the visibility of things behind it.
    """
    __implements__ = architecture.Portal.__implements__ + containment.Container.__implements__

    # XXX mmhhh I *bet* to make this robust I really ought to
    # implement both more and find... but implementing more would
    # suck, I'd have to wrap collectors to wrap their find output, or
    # something
    
    def find(self, asker, interface, criterion):
        stuff = containment.Container.find(self, asker, interface, criterion)
        if interface is not observation.ILookTarget:
            for x in stuff: yield x
            return

        for ltarget in stuff:
            phys = physical.IPhysical(ltarget, None)
            if not phys:
                continue # ??
            if phys.size > 2:
                yield wrapper(ltarget, english.INoun,
                              english.Noun(name=phys.shape, description="A %s shape." % phys.shape))

class HolyBox(containment.Container):#, architecture.Box):
    def __init__(self, original, holesize):
        containment.Container.__init__(self, original)
        self.holesize = holesize


    def find(self, asker, interface, criterion):
        stuff = containment.Container.find(self, asker, interface, criterion)
        if interface is not ITakeTarget:
            for x in stuff: yield x
            return

        for ttarget in stuff:
            phys = physical.IPhysical(ttarget)
            if phys.size > self.holesize:
                yield actions.Refusal(ttarget, (ttarget, " is too big to fit through the hole in the ", self))
            yield ttarget
