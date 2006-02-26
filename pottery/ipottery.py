
from zope.interface import Interface, Attribute

class IObject(Interface):
    """
    A thing in the world.  This has a location and a name.  It can
    also be described to those with the power of observation.
    """
    location = Attribute("An IObject which contains this IObject")

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

    def canSee(observer):
        """
        Return a boolean indicating whether the given observer can see
        this object.
        """

    def moveTo(where):
        """
        Change this things location to the new location, if possible.
        """


class IPlayer(Interface):
    pass

