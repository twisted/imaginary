# -*- test-case-name: imaginary -*-


from zope.interface import Interface, Attribute



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

    All L{ILinkContributors} which are powered up on a particular
    L{imaginary.objects.Thing} will be appended to that
    L{imaginary.objects.Thing}'s value.
    """

    def links():
        """
        @return: an iterable of L{imaginary.idea.Link}s.
        """



class IDescriptionContributor(Interface):
    """
    A powerup interface which can add text to the description of an object.

    All IDescriptionContributors which are powered up on a particular Object
    will be given a chance to add to the output of its
    L{contributeDescriptionFrom
    <IDescriptionContributor.contributeDescriptionFrom>} method.
    """

    def contributeDescriptionFrom(paths):
        """
        Contribute a portion of the description of the thing that this
        L{IDescriptionContributor} is powering up, based on the given
        collection of L{imaginary.idea.Path}s which pass through that thing.

        @param paths: paths which pass through the thing that this
            L{IDescriptionContributor} may be powering up, that may be relevant
            to the description that this contributor wants to contribute.  For
            example, if a console has red, green, and blue lights on it, and
            each is a separate path, an L{IDescriptionContributor} describing
            the buttons may examine the paths here to ensure that the buttons
            are all visible and look normal to the player before describing
            them using some custom prose.
        @type paths: L{list} of L{imaginary.idea.Path}

        @return: a concept which presents a description to its observer.
        @rtype: L{IConcept}
        """



class INameable(Interface):
    """
    A provider of L{INameable} is an object which can be identified by an
    imaginary actor by a name.
    """

    def knownTo(observer, name):
        """
        Is this L{INameable} known to the given C{observer} by the given
        C{name}?

        @param name: the name to test for

        @type name: L{unicode}

        @param observer: the thing which is observing this namable.

        @type observer: L{IThing}

        @rtype: L{bool}

        @return: L{True} if C{name} identifies this L{INameable}, L{False}
            otherwise.
        """


class ILitLink(Interface):
    """
    This interface is an annotation interface for L{imaginary.idea.Link}
    objects, for indicating that the link can apply lighting.
    """

    def isItLit(path):
        """
        Is the given C{path} well-lit enough for its target to be visible,
        according to the lighting applied by this link?

        @param path: a path containing the link that this L{ILitLink} is
            annotating.
        @type path: L{imaginary.idea.Path}

        @return: L{True} if the target of the path should be lit, L{False} if
            not.
        @rtype: L{bool}
        """

    def applyLighting(litThing, eventualTarget, requestedInterface):
        """
        Apply a transformation to an object that an
        L{imaginary.idea.Idea.obtain} is requesting, based on the light level
        of this link and its surroundings.

        @param litThing: The L{IThing} to apply lighting to.

        @type litThing: L{IThing}

        @param eventualTarget: The eventual, ultimate target of the path in
            question.

        @type eventualTarget: C{requestedInterface}

        @param requestedInterface: The interface requested by the query that
            resulted in this path; this is the interface which
            C{eventualTarget} should implement.

        @type requestedInterface: L{Interface}

        @return: C{eventualTarget}, or, if this L{ILitLink} knows how to deal
            with lighting specifically for C{requestedInterface}, a modified
            version thereof which still implements C{requestedInterface}.  If
            insufficient lighting results in the player being unable to access
            the desired object at all, C{None} will be returned.

        @rtype: C{NoneType}, or C{requestedInterface}
        """




class IThing(Interface):
    """
    A thing in the world.  It has a location and and might be relocateable.
    """
    location = Attribute("An IThing which contains this IThing")

    proper = Attribute(
        "A boolean indicating the definiteness of this thing's pronoun.")

    name = Attribute(
        "A unicode string, the name of this Thing.")


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



class IMovementRestriction(Interface):
    """
    A L{MovementRestriction} is a powerup that can respond to a L{Thing}'s
    movement before it occurs, and thereby restrict it.

    Powerups of this type are consulted on L{Thing} before movement is allowed
    to complete.
    """

    def movementImminent(movee, destination):
        """
        An object is about to move.  Implementations can raise an exception if
        they wish to to prevent it.

        @param movee: the object that is moving.

        @type movee: L{Thing}

        @param destination: The L{Thing} of the container that C{movee} will be
            moving to.

        @type destination: L{IThing}

        @raise Exception: if the movement is to be prevented.
        """



class IActor(Interface):
    hitpoints = Attribute("L{Points} instance representing hit points")
    experience = Attribute("C{int} representing experience")
    level = Attribute("C{int} representing player's level")
    thing = Attribute("L{IThing} which represents the actor's physical body.")

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



class IExit(Interface):
    """
    An interface representing one direction that a player may move in.  While
    L{IExit} only represents one half of a passageway, it is not necessarily
    one-way; in most cases, a parallel exit will exist on the other side.
    (However, it I{may} be one-way; there is no guarantee that you will be able
    to traverse it backwards, or even indeed that it will take you somewhere at
    all!)
    """

    name = Attribute(
        """
        The name of this exit.  This must be something adaptable to
        L{IConcept}, to display to players.
        """)

    def traverse(thing):
        """
        Attempt to move the given L{IThing} through this L{IExit} to the other
        side.  (Note that this may not necessarily result in actual movement,
        if the exit does something tricky like disorienting you or hurting
        you.)

        @param thing: Something which is passing through this exit.

        @type thing: L{IThing}
        """


    def shouldEvenAttemptTraversalFrom(fromLocation, potentialTraverser):
        """
        Is it plausible for the given thing to attempt a C{traverse} of this
        L{IExit}?

        @param fromLocation: The location from which the traversal might be
            attempted.
        @type fromLocation: L{IThing}

        @param potentialTraverser: The thing which might attempt to traverse
            the exit.
        @type potentialTraverser: L{IThing}

        @return: C{True} if so, C{False} if not.
        """





class IObstruction(Interface):
    """
    An L{IObstruction} is a link annotation indicating that there is a physical
    obstruction preventing solid objects from reaching between the two ends of
    the link.  For example, a closed door might annotate its link to its
    destination with an L{IObstruction}.
    """

    def whyNot():
        """
        @return: a reason why this is obstructed.

        @rtype: L{IWhyNot}
        """



class IContainer(Interface):
    """
    An object which can contain other objects.
    """
    capacity = Attribute(
        """
        The maximum weight this container is capable of holding.
        """)

    closed = Attribute(
        """
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

    def vt102(observer):
        """
        Produce some nicely colored data structures which can later be rendered
        to some VT-102-escape-code compatible octets.

        @param observer: the physical body of the player who is perceiving this
            concept
        @type observer: L{IThing}

        @return: Some text in the format (currently informally) defined by
            L{imaginary.text}.
        @rtype: a L{list} or something, good luck
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



class ILinkAnnotator(Interface):
    """
    An L{ILinkAnnotator} provides annotations for links from one
    L{imaginary.idea.Idea} to another.
    """

    def annotationsFor(link, idea):
        """
        Produce an iterator of annotations to be applied to a link whose source
        or target is the L{Idea} that this L{ILinkAnnotator} has been applied
        to.
        """



class ILocationLinkAnnotator(Interface):
    """
    L{ILocationLinkAnnotator} is a powerup interface to allow powerups for a
    L{Thing} to act as L{ILinkAnnotator}s for every L{Thing} contained within
    it.  This allows area-effect link annotators to be implemented simply,
    without needing to monitor movement.
    """

    def annotationsFor(link, idea):
        """
        Produce an iterator of annotations to be applied to a link whose source
        or target is an L{Idea} of a L{Thing} contained in the L{Thing} that
        this L{ILocationLinkAnnotator} has been applied to.
        """



class IRetriever(Interface):
    """
    An L{IRetriever} examines a L{Path} and retrieves a desirable object from
    it to yield from L{Idea.obtain}, if the L{Path} is suitable.

    Every L{IRetriever} has a different definition of suitability; you should
    examine some of their implementations for more detail.
    """

    def retrieve(path):
        """
        Return the suitable object described by C{path}, or None if the path is
        unsuitable for this retriever's purposes.
        """

    def shouldKeepGoing(path):
        """
        Inspect a L{Path}.  True if it should be searched, False if not.

        @param path: A path to inspect.
        @type path: L{Path}

        @return: L{True} if retrieval should continue to the paths reachable
            beyond C{path}, L{False} otherwise.
        """


    def objectionsTo(path, result):
        """
        @param path: The path to a particular result.
        @type path: L{Path}

        @param result: An object previously returned by C{retrieve} which will
            be retrieved if this method does not return any objections to it.
        @type result: ???

        @return: an iterator of IWhyNot, if you object to this result being
            yielded.
        """



class IContainmentRelationship(Interface):
    """
    Indicate the containment of one idea within another, via a link.

    This is an annotation interface, used to annotate L{iimaginary.idea.Link}s
    to specify that the relationship between linked objects is one of
    containment.  In other words, the presence of an
    L{IContainmentRelationship} annotation on a L{iimaginary.idea.Link}
    indicates that the target of that link is contained by the source of that
    link.
    """

    containedBy = Attribute(
        """
        A reference to the L{IContainer} which contains the target of the link
        that this L{IContainmentRelationship} annotates.
        """)

    contained = Attribute(
        """
        A reference to the L{IThing} being contained.
        """
    )



class IVisible(Interface):
    """
    A thing which can be seen.
    """

    def visualizeWithContents(pathsToContents):
        """
        @return: an L{IConcept} which represents the visible aspects of this
            visible thing, but with the given list of L{imaginary.idea.Path}
            objects pointing at paths which continue on past this L{IVisible}.
        """



    def isViewOf(thing):
        """
        Is this L{IVisible} a view of a given L{Thing}?

        @rtype: L{bool}
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


    def nowWornBy(wearer):
        """
        This article of clothing is now being worn by C{wearer}.

        @param wearer: The wearer of the clothing.

        @type wearer: L{IClothingWearer}
        """


    def noLongerWorn():
        """
        This article of clothing is no longer being worn.
        """



class ISittable(Interface):
    """
    Something you can sit on.
    """

    def seat(sitterThing):
        """
        @param sitterThing: The person sitting down on this sittable surface.

        @type sitterThing: L{imaginary.objects.Thing}
        """



class IWhyNot(Interface):
    """
    This interface is an idea link annotation interface, designed to be applied
    by L{ILinkAnnotator}s, that indicates a reason why a given path cannot
    yield a provider.  This is respected by L{imaginary.idea.ProviderOf}.
    """

    def tellMeWhyNot():
        """
        Return something adaptable to L{IConcept}, that explains why this link
        is unsuitable for producing results.  For example, the string "It's too
        dark in here."
        """



class IDistance(Interface):
    """
    A link annotation that provides a distance.
    """

    distance = Attribute("floating point, distance in meters")



class IElectromagneticMedium(Interface):
    """
    A medium through which electromagnetic radiation may or may not pass; used
    as a link annotation.
    """

    def isOpaque(observer):
        """
        Will this propagate radiation the visible spectrum?

        @param observer: The L{Thing} which has eyeballs which are shooting out
            electromagnetic radiation which could lead to reflected perceptrons
            to let the L{Thing} perceive a target.
        @type observer: L{Thing}

        @note: This interface has a problem.  C{observer} should probably
            provide some kind of C{ISpectrum} interface and the implementation
            of L{IElectromagneticMedium} should consult methods of that to
            determine the frequency that is relevant, etc.  Also, the basic
            perception interface should probably be something else.  Batman
            might use echo-location to perceive his environment (he's a bat,
            right?) so "look at Alice" shouldn't require that he can "see"
            Alice via L{IElectromagneticMedium} - he can "see" her via
            L{ISoundMedium} or whatever.
        """

