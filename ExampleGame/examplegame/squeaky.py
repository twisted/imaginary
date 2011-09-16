# -*- test-case-name: examplegame.test.test_squeaky -*-

"""
This module implements an L{ILinkAnnotator} which causes an object to squeak
when it is moved.  It should serve as a simple example for overriding what
happens when an action is executed (in this case, 'take' and 'drop').
"""

from zope.interface import implements

from axiom.item import Item
from axiom.attributes import reference

from imaginary.iimaginary import IMovementRestriction, IConcept
from imaginary.events import Success
from imaginary.enhancement import Enhancement
from imaginary.objects import Thing


class Squeaker(Item, Enhancement):
    """
    This is an L{Enhancement} which, when installed on a L{Thing}, causes that
    L{Thing} to squeak when you pick it up.
    """

    implements(IMovementRestriction)

    powerupInterfaces = [IMovementRestriction]

    thing = reference(allowNone=False,
                      whenDeleted=reference.CASCADE,
                      reftype=Thing)


    def movementImminent(self, movee, destination):
        """
        The object enhanced by this L{Squeaker} is about to move - emit a
        L{Success} event which describes its squeak.
        """
        Success(otherMessage=(IConcept(self.thing).capitalizeConcept(),
                              " emits a faint squeak."),
                location=self.thing.location).broadcast()
