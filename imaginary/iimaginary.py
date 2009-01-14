# -*- test-case-name: imaginary -*-


from zope.interface import Interface, Attribute



class ITelnetService(Interface):
    """
    Really lame tag interface used by the Mantissa offering system to uniquely
    identify a powerup that runs a telnet server.
    """



class ISSHService(Interface):
    """
    Really lame tag interface used by the Mantissa offering system to uniquely
    identify a powerup that runs an ssh server.
    """



class IThingType(Interface):
    """
    Plugin interface for kinds of objects which can be created in the realm.
    """
    type = Attribute("Name of this type of object.")

    def getType():
        """
        Return a two-argument callable which will be invoked with C{name},
        C{description} to create a new instance of this type.  Should return an
        L{IThing} provider.
        """


class ILinkContributor(Interface):
    """
    A powerup interface which can add more connections between objects in the
    world graph.

    All ILinkContributors which are powered up on a particular Thing will be
    given a chance to add to the L{IThing.link} method's return value.
    """

    def links():
        """
        Return a C{dict} mapping names of connections to C{IThings}.
        """


class IDescriptionContributor(Interface):
    """
    A powerup interface which can add text to the description of an object.

    All IDescriptionContributors which are powered up on a particular Object
    will be given a chance to add to the output of its C{conceptualize} method.
    """

    def conceptualize():
        """
        Return an IConcept provider.
        """



class IThing(Interface):
    """
    A thing in the world.  It has a location and and might be relocateable.
    """
    location = Attribute("An IThing which contains this IThing")


    def moveTo(where, arrivalEventFactory=None):
        """
        Change this things location to the new location, if possible.

        @type where: L{IThing} provider.
        @param where: The new location to be moved to.
        
        @type arrivalEventFactory: A callable which takes a single
        argument, the thing being moved, and returns an event.
        @param arrivalEventFactory: Will be called to produce the
        event to be broadcast to the new location upon arrival of this
        thing. If not specified (or None), no event will be broadcast.
        """


    def findProviders(interface, distance):
        """
        Retrieve all game objects which provide C{interface} within C{distance}.

        @return: A generator of providers of C{interface}.
        """


    def proxiedThing(thing, interface, distance):
        """
        Given an L{IThing} provider, return a provider of L{interface} as it is
        accessible from C{self}.  Any necessary proxies will be applied.
        """


    def knownAs(name):
        """
        Return a boolean indicating whether this thing might reasonably be
        called C{name}.

        @type name: C{unicode}
        """



class IActor(Interface):
    hitpoints = Attribute("L{Points} instance representing hit points")
    experience = Attribute("C{int} representing experience")
    level = Attribute("C{int} representing player's level")

    def send(event):
        """Describe something to the actor.

        @type event: L{IConcept} provider
        @param event: Something that will be described to the actor.
        """


    def getIntelligence():
        """
        Return the current intelligence associated with this actor, be it
        ephemeral or enduring.

        @rtype: L{IEventObserver}.
        """


    def setEphemeralIntelligence(intelligence):
        """
        Set the intelligence for this actor to an ephemeral L{IEventObserver}.

        @type intelligence: L{IEventObserver} provider.
        """


    def setEnduringIntelligence(intelligence):
        """
        Set the intelligence for this actor to a persistent L{IEventObserver}.

        @type intelligence: L{IEventObserver} provider.
        """



class IManipulator(Interface):
    """
    An L{IManipulator} provider is an actor who can perform direct
    manipulations of a world's environment (or at least, try to).
    """

    def setIllumination(candelas):
        """
        Attempt to set the ambient illumination this L{IManipulator}'s
        location.

        @param candelas: the desired ambient illumination value of the location
            in candelas.

        @type candelas: L{int}

        @return: The previous ambient light level (in candelas)

        @raise imaginary.eimaginary.ActionFailure: if the action cannot be
            completed (for example, if this L{IManipulator} doesn't have
            permission to change the lighting in its location).
        """



class IEventObserver(Interface):
    def prepare(concept):
        """
        Capture the given concept in a callable which will describe something
        to this observer.

        The callable will be invoked when it is entirely certain that the
        concept is congruent with game reality.  For example, a concept for an
        arrow striking its target might be prepared but the resulting callable
        will not be invoked until the combat game system decides the arrow
        really is striking its target.

        This two-phase process is also used to deal with events occurring
        during transactions.  While the event will be prepared immediately
        during the execution of an action, the callable resulting from the
        preparation will not be invoked until the transaction has completed.
        If the transaction fails with an exception, then the callables will not
        be invoked.

        @type concept: L{IConcept} provider
        @param concept: Something that will be described to the actor.

        @return: a 0-argument callable which will deliver the given concept to
            this observer.
        """



class ITransactionalEventBroadcaster(Interface):
    """
    A thing which mediates the deadly side-effects of event broadcast by
    holding things back until a transaction has been successfully committed or
    is being reverted.
    """
    def addEvent(event):
        """
        Add an event which will be broadcast when the transaction is committed
        successfully.
        """


    def addRevertEvent(event):
        """
        Add an event which will be broadcast when the transaction is reverted.
        """



class IContainer(Interface):
    """
    An object which can contain other objects.
    """
    capacity = Attribute("""
    The maximum weight this container is capable of holding.
    """)

#     lid = Attribute("""
#     A reference to an L{IThing} which serves as this containers lid, or
#     C{None} if there is no lid.
#     """)

    closed = Attribute("""
    A boolean indicating whether this container is closed.
    """)

    def add(object):
        """
        Place the given object into this container.

        @type object: L{IThing}
        @param object: The world object to be added to this container.  Its
        C{location} attribute will be updated if it is successfully added.

        @raise DoesntFit: If there is no room for C{object} in this container.
        @raise Closed: If this container is not currently open.
        """


    def remove(object):
        """
        Remove the given object from this container.

        @type object: L{IThing}

        @param object: The world object which is currently in this container
        which is to be removed.  If it is successfully removed, its C{location}
        attribute will be set to C{None}.

        @raise ValueError: If C{object} is not within this container.
        @raise Closed: If this container is not currently open.
        """


    def contains(other):
        """
        @returns: True if other is in me. And by 'in', I mean 'IN'!  (And
        by 'IN' he means to any arbitrarily deeply nested distance)
        """


    def getContents():
        """
        @returns: An iterable of the direct contents of this container.
        """


    def getExits():
        """
        @return: an L{axiom.store.ItemQuery} of the exits leading out of this
        container.
        """


    def getExitNames():
        """
        @return: an L{axiom.store.AttributeQuery} of the names of the exits
        leading out of this container.
        """


    def getExitNamed(name, default=None):
        """
        @return: The L{imaginary.objects.Exit} with the given name, or default
        if none is found.

        @raise KeyError: When an exit with the given name is not found and no
        default was passed.
        """



class IConcept(Interface):
    """
    This represents a concept which can be expressed in English.
    """

    def plaintext(observer):
        """
        @param observer: the IThing provider who is asking to learn about this
        concept, or None.  This comes from the argument to 'express'.
        """


    def capitalizeConcept():
        """
        Make this concept CAPITALISERD!

        Oh man this is retarded.

        XXX fix it or something pleeeeeeeaaaaaaaaaasssssssssseeeeeeeeee
        deletedeletedletedletledeltetledleltellxceltedlelt
        """



class IProxy(Interface):
    """
        | > look
        | [ Nuclear Reactor Core ]
        | High-energy particles are wizzing around here at a fantastic rate.  You can
        | feel the molecules in your body splitting apart as neutrons bombard the
        | nuclei of their constituent atoms.  In a few moments you will be dead.
        | There is a radiation suit on the floor.
        | > take radiation suit
        | You take the radiation suit.
        | Your internal organs hurt a lot.
        | > wear radiation suit
        | You wear the radiation suit.
        | You start to feel better.

    That is to say, a factory for objects which take the place of elements in
    the result of L{IThing.findProviders} for the purpose of altering their
    behavior in some manner due to a particular property of the path in the
    game object graph through which the original element would have been found.

    Another example to consider is that of a pair of sunglasses worn by a
    player: these might power up that player for IProxy so as to be able to
    proxy IVisible in such a way as to reduce glaring light.
    """
    # XXX: Perhaps add 'distance' here, so Fog can be implemented as an
    # IVisibility proxy which reduces the distance a observer can see.
    def proxy(iface, facet):
        """
        Proxy C{facet} which provides C{iface}.

        @param facet: A candidate for inclusion in the set of objects returned
        by findProviders.

        @return: Either a provider of C{iface} or C{None}. If C{None} is
        returned, then the object will not be returned from findProviders.
        """



class ILocationProxy(Interface):
    """
    Similar to L{IProxy}, except the pathway between the observer and the
    target is not considered: instead, all targets are wrapped by all
    ILocationProxy providers on their location.
    """

    def proxy(iface, facet):
        """
        Proxy C{facet} which provides C{iface}.

        @param facet: A candidate B{contained by the location on which this is
        a powerup} for inclusion in the set of objects returned by
        findProviders.

        @return: Either a provider of C{iface} or C{None}. If C{None} is
        returned, then the object will not be returned from findProviders.
        """



class IVisible(Interface):
    """
    A thing which can be seen.
    """
    def visualize():
        """
        Return an IConcept which represents the visible aspects of this
        visible thing.
        """



class ILightSource(Interface):
    """
    Powerup interface for things which emit photons in measurable quantities.
    """
    candelas = Attribute("""
    The luminous intensity in candelas.

    See U{http://en.wikipedia.org/wiki/Candela}.
    """)



####### Below here is new, experimental stuff, which doesn't really work yet.


class IThingPowerUp(Interface):
    """
    Utility super-interface of all interfaces which are designed to be used as
    arguments to powerUp for Thing.

    Objects which provide this interface must also provide IItem, obviously, as
    only Items can be Powerups.
    """


class IClothingWearer(IThingPowerUp):
    """
    A person who can wear clothing.
    """

    def putOn(garment):
        """
        Put on an article of clothing.

        @param garment: An article of clothing.
        @type garment: L{IClothing} provider

        @raise: L{TooBulky}, if the new article of clothing will not fit
        because this wearer is already wearing a bulkier article of clothing in
        that slot.
        """


    def takeOff(garment):
        """
        Remove an article of clothing.

        @param garment: An article of clothing that this wearer is wearing.

        @raise: L{InaccessibleGarment}: if the article of clothing is either
        not being worn, or is being worn beneath another article of clothing
        which must be removed first.
        """



class IClothing(IThingPowerUp):
    """
    A piece of clothing which can be worn by an L{IClothingWearer}.
    """

    garmentSlots = Attribute(
        """
        A list of unicode strings that describe the parts of the body where
        this article of clothing can be worn, taken from the list of constants
        in L{imaginary.garments.GARMENT_SLOTS}.
        """)

    bulk = Attribute(
        """
        An integer, 1 or greater, abstractly describing how thick this garment
        is.  A bulkier garment cannot be worn over a less bulky one.
        """)



class IDescriptor(IThingPowerUp):
    """
    I provide a portion of a Thing's description.

    Install IDescribable powerUps on Thing to influence how it will be shown to
    the user.
    """

    def conceptualize():
        """
        Return an object adaptable to the IConcept for the language of an
        observer.
        """



