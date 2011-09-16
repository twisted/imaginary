# -*- test-case-name: examplegame.test.test_tether -*-

"""
A simplistic implementation of tethering, which demonstrates how to prevent
someone from moving around.

This implementation is somewhat limited, as it assumes that tethered objects
can only be located in players' inventories and on the ground.  It also makes
several assumptions about who is actually doing the moving in moveTo; in order
to be really correct, the implementation of movement needs to relay more
information about what is moving and how.
"""

from zope.interface import implements

from axiom.item import Item
from axiom.attributes import reference

from imaginary.iimaginary import IMovementRestriction, IActor
from imaginary.eimaginary import ActionFailure
from imaginary.events import ThatDoesntWork
from imaginary.enhancement import Enhancement
from imaginary.objects import Thing


class Tether(Item, Enhancement):
    """
    I am a force that binds two objects together.

    Right now this force isn't symmetric; the idea is that the thing that we
    are tethered 'to' is immovable for some other reason.  This is why we're in
    the example rather than a real robust piece of game-library functionality
    in imaginary proper.

    The C{thing} that we are installed on is prevented from moving more than a
    certain distance away from the thing it is tethered C{to}.

    This is accomplished by preventing movement of the object's container;
    i.e. if you pick up a ball that is tied to the ground, you can't move until
    you drop it.
    """

    thing = reference(reftype=Thing,
                      whenDeleted=reference.CASCADE,
                      allowNone=False)

    # XXX 'thing' and 'to' should be treated more consistently, or at least the
    # differences between them explained officially.
    to = reference(reftype=Thing,
                   whenDeleted=reference.CASCADE,
                   allowNone=False)

    implements(IMovementRestriction)

    powerupInterfaces = [IMovementRestriction]

    def movementImminent(self, movee, destination):
        """
        The object which is tethered is trying to move somewhere.  If it has an
        IActor, assume that it's a player trying to move on its own, and emit
        an appropriate message.

        Otherwise, assume that it is moving *to* an actor, and install a
        L{MovementBlocker} on that actor.
        """
        # There isn't enough information provided to moveTo just yet; we need
        # to know who is doing the moving.  In the meanwhile, if you have an
        # actor, we'll assume you're a player.
        if IActor(movee, None) is not None:
            raise ActionFailure(
                ThatDoesntWork(
                    actor=self.thing,
                    actorMessage=[u"You can't move, you're tied to ",
                                  self.to,
                                  "."],
                    otherMessage=[self.thing, u' struggles.']))
        MovementBlocker.destroyFor(self.thing.location)
        if self.to != destination:
            MovementBlocker.createFor(destination, tether=self)

        return False


class MovementBlocker(Item, Enhancement):
    """
    A L{MovementBlocker} is an L{Enhancement} which prevents the movement of a
    player holding a tethered object.
    """
    implements(IMovementRestriction)

    powerupInterfaces = [IMovementRestriction]

    thing = reference(
        doc="""
        The L{Thing} whose movement is blocked.
        """, reftype=Thing, allowNone=False,
        whenDeleted=reference.CASCADE)

    tether = reference(
        doc="""
        The L{Tether} ultimely responsible for blocking movement.
        """,
        reftype=Tether, allowNone=False,
        whenDeleted=reference.CASCADE)


    def movementImminent(self, movee, destination):
        """
        The player this blocker is installed on is trying to move.  Assume that
        they are trying to move themselves (via a 'go' action) and prevent it
        by raising an L{ActionFailure} with an appropriate error message for
        the player.
        """
        raise ActionFailure(
            ThatDoesntWork(
                actor=self.thing,
                actorMessage=
                [u"You can't move, you're still holding ",
                 self.tether.thing,u'.'],
                otherMessage=
                [self.thing, u' struggles with ', self.tether.thing,u'.']))
