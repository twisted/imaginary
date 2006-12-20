# -*- test-case-name: imaginary.test -*-
"""

Physical model of point-of-interest based geography.  This is where both indoor
(rooms) and outdoor (areas) places are defined.

"""

from zope.interface import providedBy, implements

from axiom import item, attributes

from imaginary.iimaginary import IThingPowerUp, IDescriptor, IVisible



DIRECTIONS = {
    u'north': 'south'
}


def _rev():
    for thisdir, thatdir in DIRECTIONS.items():
        DIRECTIONS[thatdir] = thisdir


_rev()


class Thing(item.Item):
    """
    I am a physical thing in the word.
    """
    implements(IVisible)

    # dynamic / mutable stuff
    location = attributes.reference()

    # template / constant stuff
    weight = attributes.integer()
    heft = attributes.integer()

    # constant, but language-dependent (???)

    # (if we are to actually write a multilingual game, this will have to be
    # upgraded.)

    baseName = attributes.text()

    gender = attributes.integer()

    def moveTo(self, newLocation):
        """
        Move to a new location.
        """
        self.location = newLocation

    def createTwoWayExit(self, direction, otherRoom, distance=100,
                         otherDirection=None):
        if otherDirection is None:
            otherDirection = DIRECTIONS.get(otherDirection, u'back')
        e1 = self.store.findOrCreate(Exit,
                                     direction=direction,
                                     origin=self,
                                     distance=distance,
                                     destination=otherRoom)
        e2 = self.store.findOrCreate(Exit,
                                     direction=otherDirection,
                                     origin=otherRoom,
                                     distance=distance,
                                     destination=self)
        e1.reverse = e2
        e2.reverse = e1

    def fullyConceptualize(self):
        """
        Yield a sequence of all concepts represented by this Thing.
        """
        for descriptor in self.powerupsFor(IDescriptor):
            yield descriptor.conceptualize()

    def findProviders(self, iface, distance=100, seen=None):
        """
        Find objects contextually appropriate to this Thing which provide the
        given interface.
        """
        # XXX TODO: determine if I want to proxy; determine if I'm allowable
        # for this interface; look up powerups (???)
        if seen is None:
            seen = set()
        if self in seen:
            return
        seen.add(self)
        adapted = iface(self, None)
        if adapted is not None:
            yield adapted
        for containedThing in self.store.query(Thing, Thing.location == self):
            for containedImpl in containedThing.findProviders(iface, distance, seen):
                yield containedImpl
        loc = self.location
        if loc is not None:
            for throughLocationImpl in loc.findProviders(iface, distance, seen):
                yield throughLocationImpl

        # all exits starting here (don't query reverse on purpose)

        for ex in self.store.query(Exit, Exit.origin == self):
            throughExitDistance = distance - ex.distance
            if throughExitDistance < 0:
                continue
            for throughExitProvider in ex.destination.findProviders(
                iface,
                distance=throughExitDistance,
                seen=seen):
                # filter this one?
                # let the exit filter this one?
                yield throughExitProvider

class Exit(item.Item):
    # implements(IExit)

    origin = attributes.reference(reftype=Thing, allowNone=False)
    destination = attributes.reference(reftype=Thing, allowNone=False)

    direction = attributes.text()

    opposite = attributes.reference() # ref to other Exit
    distance = attributes.integer(allowNone=False) # units for this ?

    reverse = attributes.reference() # is this two-way




class BehaviorMixin:
    """
    I am a mixin for behavior data.
    """

    behaviorPriority = 0

    def installBehavior(self, onThing):
        self.thing = onThing
        for iface in providedBy(self):
            if iface.extends(IThingPowerUp):
                onThing.powerUp(self, iface, self.behaviorPriority)

class Description(item.Item, BehaviorMixin):
    implements(IDescriptor)

    behaviorPriority = item.POWERUP_BEFORE

    thing = attributes.reference()

    description = attributes.text()

    def conceptualize(self, observer):
        return self.description


