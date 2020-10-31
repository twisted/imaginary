# -*- test-case-name: imaginary.test.test_enhancement -*-

"""
This module contains objects for application code to use to implement behaviors
that attach to objects in a simulation.
"""

class Enhancement(object):
    """
    An L{Enhancement} is an object attached to a L{imaginary.objects.Thing}
    that provides some additional functionality.

    This class is a mixin; it expects to be mixed in to an L{Item} subclass,
    since it passes itself as an argument to L{Item.powerUp}.

    Note that an L{Enhancement} embodies the behavior, but not the physical
    attributes, of the object in question.

    For example, let's say you wanted to implement a cell phone in Imaginary.
    You would make an L{Enhancement} called C{CellPhone} which had various
    attributes, for example C{phoneNumber}.  Then you would do C{phoneBody =
    Thing(...)} to create a physical 'phone' object in a world.  Next, you
    would do C{cellPhone = CellPhone.createFor(phoneBody, ...)}, which would
    create a C{CellPhone} object that endowed your physical 'phone' with the
    properties of being an actual phone, like having a phone number, ringing
    when dialed, etc.

    Note that it is not enough to simply create your C{CellPhone}, as it will
    not have a physical body, and therefore not exist in the world.

    @ivar thing: a L{imaginary.objects.Thing} powered up with this
         L{Enhancement}.  All subclasses which mix in L{Item} should declare
         this as an L{attributes.reference} attribute.  Unless your
         L{Enhancement} subclass is specifically designed to exist
         independently of its L{Thing}, or to accept other types for this
         attribute, it should also be declared as C{(allowNone=False,
         reftype=Thing, whenDeleted=CASCADE)}.
    """

    def installed(self):
        """
        Override the C{installed()} hook that C{axiom.dependency} provides.
        When L{Enhancement} was called C{ThingMixin}, the suggested mechanism
        to install simulation components was to use the dependency system,
        which was wrong, c.f. U{http://divmod.org/trac/ticket/2558}.

        @raise RuntimeError: to indicate that you shouldn't use this
            functionality.
        """
        raise RuntimeError("Use Enhancement.createFor, not installOn(), "
                           "to apply an Enhancement to a Thing.")


    def applyEnhancement(self):
        """
        Apply this L{Enhancement} to its C{thing} attribute, by powering it up.
        """
        self.thing.powerUp(self)


    def removeEnhancement(self):
        """
        Remove this L{Enhancement} from its C{thing} attribute, by powering it
        down.
        """
        self.thing.powerDown(self)


    @classmethod
    def createFor(cls, thing, **kw):
        """
        Create an L{Enhancement} of this type for the given
        L{imaginary.objects.Thing}, in the given L{imaginary.objects.Thing}'s
        store.
        """
        self = cls(store=thing.store, thing=thing, **kw)
        self.applyEnhancement()
        return self


    @classmethod
    def destroyFor(cls, thing):
        """
        Destroy the L{Enhancement}s of the given subclass associated with the
        given L{Thing}, if one exists.

        @param thing: A L{Thing} which may be the value of the C{thing}
            attribute of an instance of the given L{Enhancement} subclass.

        @type thing: L{Thing}
        """
        it = thing.store.findUnique(cls, cls.thing == thing, default=None)
        if it is not None:
            it.removeEnhancement()
            it.deleteFromStore()
