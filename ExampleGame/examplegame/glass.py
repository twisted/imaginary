# -*- test-case-name: examplegame.test.test_glass -*-
"""
This example implements a transparent container that you can see, but not
reach, the contents of.
"""
from zope.interface import implements

from axiom.item import Item
from axiom.attributes import reference

from imaginary.iimaginary import (
    ILinkContributor, IWhyNot, IObstruction, IContainer)
from imaginary.enhancement import Enhancement
from imaginary.objects import ContainmentRelationship
from imaginary.idea import Link

class _CantReachThroughGlassBox(object):
    """
    This object provides an explanation for why the user cannot access a target
    that is inside a L{imaginary.objects.Thing} enhanced with a L{GlassBox}.
    """
    implements(IWhyNot)

    def tellMeWhyNot(self):
        """
        Return a simple message explaining that the user can't reach through
        the glass box.
        """
        return "You can't reach through the glass box."



class _ObstructedByGlass(object):
    """
    This is an annotation on a link between two objects which represents a
    physical obstruction between them.  It is used to annotate between a
    L{GlassBox} and its contents, so you can see them without reaching them.
    """
    implements(IObstruction)

    def whyNot(self):
        """
        @return: an object which explains why you can't reach through the glass
        box.
        """
        return _CantReachThroughGlassBox()



class GlassBox(Item, Enhancement):
    """
    L{GlassBox} is an L{Enhancement} which modifies a container such that it is
    contained.
    """

    powerupInterfaces = (ILinkContributor,)

    thing = reference()

    def links(self):
        """
        If the container attached to this L{GlassBox}'s C{thing} is closed,
        yield its list of contents with each link annotated with
        L{_ObstructedByGlass}, indicating that the object cannot be reached.
        """
        container = IContainer(self.thing)
        if container.closed:
            for content in container.getContents():
                link = Link(self.thing.idea, content.idea)
                link.annotate([_ObstructedByGlass(),
                               ContainmentRelationship(container,
                                                       content)])
                yield link
