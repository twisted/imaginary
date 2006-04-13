
from zope.interface import Interface, Attribute


class ITelnetService(Interface):
    """
    Really lame tag interface used by the Mantissa offering system to uniquely
    identify a powerup that runs a telnet server.
    """


class IDescribeable(Interface):
    """
    A thing which can be described to those with the power of observation.
    """
    def formatTo(whom):
        """
        Return a brief description of this object, as observed by the
        given observer.
        """


    def longFormatTo(whom):
        """
        Return a longer description of this object, as observed by the
        given observer.
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
    will be given a chance to add to the output of its C{longFormatTo} method.
    """

    def longFormatTo(other):
        """
        @see IDescribeable
        """



class IThing(IDescribeable):
    """
    A thing in the world.  In addition to the behavior described by
    L{IDescribeable}, this has a location and and might be relocateable.
    """
    location = Attribute("An IThing which contains this IThing")

    def canSee(observer):
        """
        Return a boolean indicating whether the given observer can see
        this object.
        """


    def moveTo(where):
        """
        Change this things location to the new location, if possible.
        """



class IActor(Interface):
    hitpoints = Attribute("L{Points} instance representing hit points")
    experience = Attribute("C{int} representing experience")
    level = Attribute("C{int} representing player's level")

    def send(event):
        """Describe something to the actor.

        @type event: L{IDescribeable} provider
        @param event: Something that will be described to the actor.
        """


class IEventObserver(Interface):
    def send(event):
        """Describe something to the actor.

        @type event: L{IDescribeable} provider
        @param event: Something that will be described to the actor.
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

class IClothing(IThingPowerUp):
    """
    """

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


class IConcept(Interface):
    """
    This represents a concept which can be expressed in english.

    Many adapters to IConcept exist for simple types: for example, a string or
    unicode object, when expressed, is assumed to be in the target language
    (english, in the case of this interface) and the string itself is returned.

    Sequences (lists and tuples) are adapted to IConcept by adapting each
    element to IConcept in turn, and concatenating the result of expressing
    each one.

    Functions and methods are adapted to IConcept by assuming that they are
    one-argument callables which take the observer they are being expressed to
    as an argument.

    Note: functions adapted in this manner will _not_ have their return values
    inspected as adaptable to IConcept; they must simply return unicode objects
    as expressTo is documented to.  This will not be changed: the potential for
    infinitely recursive invocations is too great.

    Some code which provides simple examples of how this interface may be
    applied can be found in imaginary.test.test_english.TestConcept.

    XXX TODO: expressTo should eventually return structured information for
    more detailed rendering (item links in chat text, for example).
    """

    def expressTo(observer):
        """
        Return a short (<4k) unicode object representing the description of this
        concept in english.

        Never implement or call this method yourself.  See the interface
        documentation for more information.

        @param observer: the IThing provider who is asking to learn about this
        concept, or None.  This comes from the argument to 'express'.
        """

class IVisible(Interface):
    """
    A thing which can be seen.

    XXX TODO: perhaps this should deal with name vs. description?  also, unique
    IDs for referring to things?
    """

    def fullyConceptualize(self):
        """
        Return an iterable of all concepts describing what this visible object
        looks like.
        """
