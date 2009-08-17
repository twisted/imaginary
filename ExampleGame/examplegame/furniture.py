# -*- test-case-name: examplegame.test.test_furniture -*-

"""

    Furniture is the mass noun for the movable objects which may support the
    human body (seating furniture and beds), provide storage, or hold objects
    on horizontal surfaces above the ground.

        -- Wikipedia, http://en.wikipedia.org/wiki/Furniture

L{imaginary.furniture} contains L{Action}s which allow players to interact with
household objects such as chairs and tables, and L{Enhancement}s which allow
L{Thing}s to behave as same.

This has the same implementation weakness as L{examplegame.tether}, in that it
needs to make some assumptions about who is moving what in its restrictions of
movement; it should be moved into imaginary proper when that can be properly
addressed.  It's also a bit too draconian in terms of preventing the player
from moving for any reason just because they're seated.  However, it's a
workable approximation for some uses, and thus useful as an example.
"""

from zope.interface import implements

from axiom.item import Item
from axiom.attributes import reference

from imaginary.iimaginary import ISittable, IContainer, IMovementRestriction
from imaginary.eimaginary import ActionFailure
from imaginary.events import ThatDoesntWork
from imaginary.language import Noun
from imaginary.action import Action, TargetAction
from imaginary.events import Success
from imaginary.enhancement import Enhancement
from imaginary.objects import Container
from imaginary.pyparsing import Literal, Optional, restOfLine

class Sit(TargetAction):
    """
    An action allowing a player to sit down in a chair.
    """
    expr = (Literal("sit") + Optional(Literal("on")) +
            restOfLine.setResultsName("target"))

    targetInterface = ISittable

    def do(self, player, line, target):
        """
        Do the action; sit down.
        """
        target.seat(player)

        actorMessage=["You sit in ",
                      Noun(target.thing).definiteNounPhrase(),"."]
        otherMessage=[player.thing, " sits in ",
                      Noun(target.thing).definiteNounPhrase(),"."]
        Success(actor=player.thing, location=player.thing.location,
                actorMessage=actorMessage,
                otherMessage=otherMessage).broadcast()


class Stand(Action):
    """
    Stand up from a sitting position.
    """
    expr = (Literal("stand") + Optional(Literal("up")))

    def do(self, player, line):
        """
        Do the action; stand up.
        """
        # XXX This is wrong.  I should be issuing an obtain() query to find
        # something that qualifies as "my location" or "the thing I'm already
        # sitting in".
        chair = ISittable(player.thing.location, None)
        if chair is None:
            raise ActionFailure(ThatDoesntWork(
                    actor=player.thing,
                    actorMessage=["You're already standing."]))
        chair.unseat(player)
        Success(actor=player.thing, location=player.thing.location,
                actorMessage=["You stand up."],
                otherMessage=[player.thing, " stands up."]).broadcast()



class Chair(Enhancement, Item):
    """
    A chair is a thing you can sit in.
    """

    implements(ISittable, IMovementRestriction)

    powerupInterfaces = [ISittable]

    thing = reference()
    container = reference()


    def movementImminent(self, movee, destination):
        """
        A player tried to move while they were seated.  Prevent them from doing
        so, noting that they must stand first.

        (Assume the player was trying to move themselves, although there's no
        way to know currently.)
        """
        raise ActionFailure(ThatDoesntWork(
                actor=movee,
                actorMessage=u"You can't do that while sitting down."))


    def applyEnhancement(self):
        """
        Apply this enhancement to this L{Chair}'s thing, creating a
        L{Container} to hold the seated player, if necessary.
        """
        super(Chair, self).applyEnhancement()
        container = IContainer(self.thing, None)
        if container is None:
            container = Container.createFor(self.thing, capacity=300)
        self.container = container


    def seat(self, player):
        """
        The player sat down on this chair; place them into it and prevent them
        from moving elsewhere until they stand up.
        """
        player.thing.moveTo(self.container)
        player.thing.powerUp(self, IMovementRestriction)


    def unseat(self, player):
        """
        The player stood up; remove them from this chair.
        """
        player.thing.powerDown(self, IMovementRestriction)
        player.thing.moveTo(self.container.thing.location)
