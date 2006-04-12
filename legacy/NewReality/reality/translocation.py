# -*- test-case-name: reality.test_reality -*- 
from reality import ambulation, things
class _nothing: pass
class Warpgate(ambulation.Exit, things.Movable):
    """
    I am an object that represents an exit-like connection between
    two Movables. This connection may be traversed by Things when
    certain conditions are met, such as being charged to a certain
    level.
    """

    
    __implements__ = things.Movable.__implements__, ambulation.Exit.__implements__, things.IInterfaceForwarder

    otherEnd = None
    twoway = False
    reverseName = None # never used for anything since we can't be two-way
    direction = 'in'
    source = None
    destination = None

    def __init__(self, store, name, otherEnd=_nothing):
        
        # we don't want to set up links, and we have a farly specific
        # set of requirements for 'destination' and 'source' (mostly
        # that they're maintained by Movable) so we don't bother
        # initializing Exit
        things.Movable.__init__(self, store, name)
        # ambulation.Exit.__init__(self, name, direction, source, destination, twoway=False)
        if otherEnd is _nothing:
            otherEnd = Warpgate(store, name+"(reverse)", self)
        self.otherEnd = otherEnd.referenceTo()
        self.forwardedInterfaces = [] #this probably wants to be a property
        
    def moveTo(self, newLocation, event=None):
        oldLocation = self.location and self.location.getItem()
        things.Movable.moveTo(self, newLocation, event)
        if self.location.getItem() is not oldLocation:
            self.source = self.location
            oei = self.otherEnd.getItem()
            oei.touch()
            oei.destination = self.location


    def collectImplementors(self, *args, **kw):
        if self.destination:
            return ambulation.Exit.collectImplementors(self, *args, **kw)
        else:
            return things.Movable.collectImplementors(self, *args, **kw)


