# -*- test-case-name: imaginary.test.test_actions -*-

import time, random, operator
import pprint

from zope.interface import implements

from twisted.python import log, filepath
from twisted.internet import defer

from axiom import iaxiom
from axiom.attributes import AND

import imaginary.plugins
from imaginary import (iimaginary, eimaginary, iterutils, events,
                       objects, text as T, language, pyparsing)
from imaginary.world import ImaginaryWorld

## Hacks because pyparsing doesn't have fantastic unicode support
_quoteRemovingQuotedString = pyparsing.quotedString.copy()
_quoteRemovingQuotedString.setParseAction(pyparsing.removeQuotes)

class UnicodeWord(pyparsing.Token):
    def parseImpl(self, instring, loc, doActions=True):
        maxLoc = len(instring)
        while loc < maxLoc and instring[loc].isspace():
            loc += 1
        start = loc
        while loc < maxLoc and not instring[loc].isspace():
            loc += 1
        end = loc
        return end, instring[start:end]



class _ActionType(type):
    actions = []
    def __new__(cls, name, bases, attrs):
        infrastructure = attrs.pop('infrastructure', False)
        t = super(_ActionType, cls).__new__(cls, name, bases, attrs)
        if not infrastructure:
            cls.actions.append(t)
        return t


    def parse(self, player, line):
        for cls in self.actions:
            try:
                match = cls.match(player, line)
            except pyparsing.ParseException:
                pass
            else:
                if match is not None:
                    match = dict(match)
                    for k,v in match.items():
                        if isinstance(v, pyparsing.ParseResults):
                            match[k] = v[0]

                    return cls().runEventTransaction(player, line, match)
        return defer.fail(eimaginary.NoSuchCommand(line))



class Action(object):
    __metaclass__ = _ActionType
    infrastructure = True


    def runEventTransaction(self, player, line, match):
        """
        Take a player, line, and dictionary of parse results and execute the
        actual Action implementation.

        @param player: A provider of C{self.actorInterface}
        @param line: A unicode string containing the original input
        @param match: A dictionary containing some parse results to pass
        through to the C{run} method.

        """
        events.runEventTransaction(
            player.store, self.run, player, line, **match)


    def match(cls, player, line):
        return cls.expr.parseString(line)
    match = classmethod(match)


    def run(self, player, line, **kw):
        begin = time.time()
        try:
            return self._reallyRun(player, line, kw)
        finally:
            end = time.time()
            log.msg(
                interface=iaxiom.IStatEvent,
                stat_actionDuration=end - begin,
                stat_actionExecuted=1,
                )


    def _reallyRun(self, player, line, kw):
        for (k, v) in kw.items():
            try:
                objs = self.resolve(player, k, v)
            except NotImplementedError:
                pass
            else:
                if len(objs) != 1:
                    raise eimaginary.AmbiguousArgument(self, k, v, objs)
                else:
                    kw[k] = objs[0]
        return self.do(player, line, **kw)


    def resolve(self, player, name, value):
        raise NotImplementedError("Don't know how to resolve %r (%r)" % (name, value))



class NoTargetAction(Action):
    """
    @cvar actorInterface: Interface that the actor must provide.
    """
    infrastructure = True

    actorInterface = iimaginary.IActor

    def match(cls, player, line):
        actor = cls.actorInterface(player, None)
        if actor is not None:
            return super(NoTargetAction, cls).match(player, line)
        return None
    match = classmethod(match)

    def run(self, player, line, **kw):
        return super(NoTargetAction, self).run(self.actorInterface(player), line, **kw)


def targetString(name):
    return (
        _quoteRemovingQuotedString ^
        UnicodeWord()).setResultsName(name)



class TargetAction(NoTargetAction):
    """
    Subclass L{TargetAction} to implement an action that acts on a target, like
    'take foo' or 'eat foo' where 'foo' is the target.

    @cvar targetInterface: the interface which the 'target' parameter to 'do'
        must provide.
    """

    infrastructure = True

    targetInterface = iimaginary.IThing

    def targetRadius(self, player):
        return 2

    def resolve(self, player, k, v):
        if k == "target":
            return list(player.thing.search(self.targetRadius(player), self.targetInterface, v))
        return super(TargetAction, self).resolve(player, k, v)



class ToolAction(TargetAction):
    """
    Subclass L{ToolAction} to implement an action that acts on a target by
    using a tool, like 'unlock door with key', where 'door' is the target and
    'key' is the tool.

    @cvar toolInterface: the L{zope.interface.Interface} which the 'tool'
        parameter to 'do' must provide.
    """
    infrastructure = True

    toolInterface = iimaginary.IThing

    def toolRadius(self, player):
        return 2

    def resolve(self, player, k, v):
        if k == "tool":
            return list(player.thing.search(
                    self.toolRadius(player), self.toolInterface, v))
        return super(ToolAction, self).resolve(player, k, v)



class LookAround(NoTargetAction):
    actionName = "look"
    expr = pyparsing.Literal("look") + pyparsing.StringEnd()

    def do(self, player, line):
        for visible in player.thing.findProviders(iimaginary.IVisible, 1):
            if player.thing.location is visible.thing:
                concept = visible.visualize()
                break
        else:
            concept = u"You are floating in an empty, formless void."
        events.Success(actor=player.thing,
                       actorMessage=concept).broadcast()



class LookAt(TargetAction):
    actionName = "look"
    expr = (pyparsing.Literal("look") +
            pyparsing.Optional(pyparsing.White() +
                               pyparsing.Literal("at")) +
            pyparsing.White() +
            pyparsing.restOfLine.setResultsName("target"))

    targetInterface = iimaginary.IVisible

    def targetNotAvailable(self, player, exc):
        return "You don't see that."

    def targetRadius(self, player):
        return 3

    def do(self, player, line, target):
        if player.thing is not target:
            evt = events.Success(
                actor=player.thing,
                target=target,
                actorMessage=target.visualize(),
                targetMessage=(player.thing, " looks at you."))
        else:
            evt = events.Success(
                actor=player.thing,
                actorMessage=target.visualize())
        evt.broadcast()



class Illuminate(NoTargetAction):
    """
    Change the ambient light level at the location of the actor.  Since this is
    an administrative action that directly manipulates the environment, the
    actor must be a L{iimaginary.IManipulator}.

    The argument taken by this action is an integer which specifies the light
    level in U{candelas<http://en.wikipedia.org/wiki/Candela>}.
    """

    actorInterface = iimaginary.IManipulator

    expr = (pyparsing.Literal("illuminate") +
            pyparsing.White() +
            pyparsing.Word("0123456789").setResultsName("candelas"))


    def do(self, player, line, candelas):
        """
        Attempt to change the illumination of the player's surroundings.

        @param player: a manipulator that can change the illumination of its
            room.
        @type player: L{IManipulator}

        @param line: the text being parsed
        @type line: L{str}

        @param candelas: the number of candelas to change the ambient
            illumination to.
        @type candelas: L{str}
        """
        candelas = int(candelas)
        oldCandelas = player.setIllumination(candelas)
        otherMessage = None
        if oldCandelas == candelas:
            actorMessage = u"You do it.  Swell."
        elif candelas == 0:
            actorMessage = (
                u"Your environs fade to black due to Ineffable Spooky Magic.")
            otherMessage = actorMessage
        elif oldCandelas == 0:
            actorMessage = u"Your environs are suddenly alight."
            otherMessage = actorMessage
        elif candelas < oldCandelas:
            actorMessage = u"Your environs seem slightly dimmer."
            otherMessage = actorMessage
        elif candelas > oldCandelas:
            actorMessage = u"Your environs seem slightly brighter."
            otherMessage = actorMessage
        events.Success(actor=player.thing,
                       actorMessage=actorMessage,
                       otherMessage=otherMessage).broadcast()



class Describe(TargetAction):
    expr = (pyparsing.Literal("describe") +
            pyparsing.White() +
            targetString("target") +
            pyparsing.White() +
            pyparsing.restOfLine.setResultsName("description"))

    def targetRadius(self, player):
        return 3

    def do(self, player, line, target, description):
        target.description = description
        evt = events.Success(
            actor=player.thing,
            actorMessage=("You change ", target, "'s description."),
            otherMessage=(player.thing, " changes ", target, "'s description."))
        evt.broadcast()


class Name(TargetAction):
    expr = (pyparsing.Literal("name") +
            pyparsing.White() +
            targetString("target") +
            pyparsing.White() +
            pyparsing.restOfLine.setResultsName("name"))

    def targetRadius(self, player):
        return 3

    def do(self, player, line, target, name):
        evt = events.Success(
            actor=player.thing,
            actorMessage=("You change ", target, "'s name."),
            otherMessage=language.Sentence([player.thing, " changes ", target, "'s name to ", name, "."]))
        evt.broadcast()
        target.name = name



class Open(TargetAction):
    expr = (pyparsing.Literal("open") +
            pyparsing.White() +
            targetString("target"))

    targetInterface = iimaginary.IContainer

    def do(self, player, line, target):
        dnf = language.Noun(target.thing).definiteNounPhrase()
        if not target.closed:
            raise eimaginary.ActionFailure(events.ThatDoesntWork(
                actor=player.thing,
                target=target.thing,
                actorMessage=language.Sentence([dnf, " is already open."])))

        target.closed = False
        evt = events.Success(
            actor=player.thing,
            target=target.thing,
            actorMessage=("You open ", dnf, "."),
            targetMessage=language.Sentence([player.thing, " opens you."]),
            otherMessage=language.Sentence([player.thing, " opens ", target.thing, "."]))
        evt.broadcast()



class Close(TargetAction):
    expr = (pyparsing.Literal("close") +
            pyparsing.White() +
            targetString("target"))

    targetInterface = iimaginary.IContainer

    def do(self, player, line, target):
        dnf = language.Noun(target.thing).definiteNounPhrase()
        if target.closed:
            raise eimaginary.ActionFailure(events.ThatDoesntWork(
                actor=player.thing,
                target=target.thing,
                actorMessage=language.Sentence([dnf, " is already closed."])))

        target.closed = True
        evt = events.Success(
            actor=player.thing,
            target=target.thing,
            actorMessage=("You close ", dnf, "."),
            targetMessage=language.Sentence([player.thing, " closes you."]),
            otherMessage=language.Sentence([player.thing, " closes ", target.thing, "."]))
        evt.broadcast()



def tooHeavy(player, target):
    return eimaginary.ActionFailure(events.ThatDoesntWork(
        actor=player, target=target,
        actorMessage=(target, " is too heavy to pick up."),
        otherMessage=(player, " struggles to lift ", target, ", but fails."),
        targetMessage=(player, " tries to pick you up, but fails.")))



def targetTaken(player, target, container=None):
    if container is None:
        return events.Success(
            actor=player, target=target,
            actorMessage=("You take ", target, "."),
            targetMessage=(player, " takes you."),
            otherMessage=(player, " takes ", target, "."))
    idop = language.Noun(container).definiteNounPhrase()
    return events.Success(
        actor=player,
        target=target,
        tool=container,
        actorMessage=("You take ", target, " from ", idop, "."),
        targetMessage=(player, " takes you from ", idop, "."),
        toolMessage=(player, " takes ", target, " from you."),
        otherMessage=(player, " takes ", target, " from ", idop, "."))



class Remove(TargetAction):
    expr = ((pyparsing.Literal("remove") |
             pyparsing.Literal("take off")) +
            pyparsing.White() +
            targetString("target"))

    targetInterface = iimaginary.IClothing
    actorInterface = iimaginary.IClothingWearer

    def do(self, player, line, target):
        from imaginary import garments
        try:
            player.takeOff(target)
        except garments.InaccessibleGarment, e:
            raise eimaginary.ActionFailure(events.ThatDoesntWork(
                actor=player.thing,
                target=target.thing,
                actorMessage=(u"You cannot take off ",
                              language.Noun(target.thing).definiteNounPhrase(),
                              u" because you are wearing ",
                              e.obscuringGarment.thing, u"."),
                otherMessage=language.Sentence([
                    player.thing,
                    u" gets a dumb look on ",
                    language.Noun(player.thing).hisHer(),
                    u" face."])))

        evt = events.Success(
            actor=player.thing,
            target=target.thing,
            actorMessage=(u"You take off ",
                          language.Noun(target.thing).definiteNounPhrase(),
                          u"."),
            otherMessage=language.Sentence([
                player.thing, u" takes off ", target.thing, u"."]))
        evt.broadcast()



class Wear(TargetAction):
    expr = (pyparsing.Literal("wear") +
            pyparsing.White() +
            targetString("target"))

    targetInterface = iimaginary.IClothing
    actorInterface = iimaginary.IClothingWearer

    def do(self, player, line, target):
        from imaginary import garments
        try:
            player.putOn(target)
        except garments.TooBulky, e:
            raise eimaginary.ActionFailure(events.ThatDoesntWork(
                actor=player.thing,
                target=target.thing,
                actorMessage=language.Sentence([
                    language.Noun(e.wornGarment.thing).definiteNounPhrase(),
                    u" you are already wearing is too bulky for you to do"
                    u" that."]),
                otherMessage=language.Sentence([
                    player.thing,
                    u" wrestles with basic personal problems."])))

        evt = events.Success(
            actor=player.thing,
            target=target.thing,
            actorMessage=(u"You put on ",
                          language.Noun(target.thing).definiteNounPhrase(),
                          "."),
            otherMessage=language.Sentence([
                player.thing, " puts on ", target.thing, "."]))
        evt.broadcast()



class Equipment(NoTargetAction):
    expr = pyparsing.Literal("equipment")

    actorInterface = iimaginary.IClothingWearer

    def do(self, player, line):
        from imaginary import garments
        equipment = list(player.store.query(
            objects.Thing,
            AND(
                garments.Garment.thing == objects.Thing.storeID,
                garments.Garment.wearer == player),
            sort=objects.Thing.name.ascending))
        if equipment:
            evt = events.Success(
                actor=player.thing,
                actorMessage=[
                    u"You are wearing ",
                    language.ItemizedList(equipment),
                    u"."])
        else:
            evt = events.Success(
                actor=player.thing,
                actorMessage=language.ExpressString(
                    u"You aren't wearing any equipment."))
        evt.broadcast()



class TakeFrom(ToolAction):
    actionName = "take"

    expr = ((pyparsing.Literal("get") ^ pyparsing.Literal("take")) +
            pyparsing.White() +
            targetString("target") +
            pyparsing.Optional(pyparsing.White() +
                               pyparsing.Literal("from")) +
            pyparsing.White() +
            targetString("tool"))

    def targetNotAvailable(self, player, exc):
        return "Nothing like that around here."
    toolNotAvailable = targetNotAvailable

    def do(self, player, line, target, tool):
        # XXX Make sure target is in tool
        targetTaken(player.thing, target, tool).broadcast()
        try:
            target.moveTo(player.thing)
        except eimaginary.DoesntFit:
            raise tooHeavy(player.thing, target)



class PutIn(ToolAction):

    toolInterface = iimaginary.IThing
    targetInterface = iimaginary.IContainer

    def targetNotAvailable(self, player, exc):
        return "That doesn't work."

    expr = (pyparsing.Literal("put") +
            pyparsing.White() +
            targetString("tool") +
            pyparsing.Optional(pyparsing.White() +
                               pyparsing.Literal("in")) +
            pyparsing.White() +
            targetString("target"))

    def do(self, player, line, tool, target):
        ctool = iimaginary.IContainer(tool, None)
        targetObject = target.thing
        if ctool is not None and (ctool.contains(targetObject) or ctool is target):
            raise eimaginary.ActionFailure(
                events.ThatDoesntWork(
                    actor=player.thing,
                    target=targetObject,
                    tool=tool,
                    actorMessage="A thing cannot contain itself in euclidean space."))

        dnf = language.Noun(targetObject).definiteNounPhrase()
        evt = events.Success(
            actor=player.thing,
            target=targetObject,
            tool=tool,
            actorMessage=("You put ",
                          language.Noun(tool).definiteNounPhrase(),
                          " in ", dnf, "."),
            targetMessage=language.Sentence([player.thing, " puts ", " tool in you."]),
            toolMessage=language.Sentence([player.thing, " puts you in ", targetObject, "."]),
            otherMessage=language.Sentence([player.thing, " puts ", tool, " in ", targetObject, "."]))
        evt.broadcast()

        try:
            tool.moveTo(target)
        except eimaginary.DoesntFit:
            # <allexpro> dash: put me in a tent and give it to moshez!
            raise eimaginary.ActionFailure(
                events.ThatDoesntWork(
                    actor=player.thing,
                    target=targetObject,
                    tool=tool,
                    actorMessage=language.Sentence([
                            language.Noun(tool).definiteNounPhrase(),
                            u" does not fit in ", dnf, u"."])))
        except eimaginary.Closed:
            raise eimaginary.ActionFailure(
                events.ThatDoesntWork(
                    actor=player.thing,
                    target=targetObject,
                    tool=tool,
                    actorMessage=language.Sentence([dnf, " is closed."])))



class Take(TargetAction):
    expr = ((pyparsing.Literal("get") ^ pyparsing.Literal("take")) +
            pyparsing.White() +
            targetString("target"))

    def targetNotAvailable(self, player, exc):
        return u"Nothing like that around here."

    def targetRadius(self, player):
        return 1

    def do(self, player, line, target):
        if target in (player.thing, player.thing.location) or target.location is player.thing:
            raise eimaginary.ActionFailure(events.ThatDoesntMakeSense(
                actor=player.thing,
                actorMessage=("You cannot take ", target, ".")))

        targetTaken(player.thing, target).broadcast()
        try:
            target.moveTo(player.thing)
        except eimaginary.DoesntFit:
            raise tooHeavy(player.thing, target)



def insufficientSpace(player):
    return eimaginary.ActionFailure(events.ThatDoesntWork(
        actor=player,
        actorMessage="There's not enough space for that."))



class Drop(TargetAction):
    expr = (pyparsing.Literal("drop") +
            pyparsing.White() +
            targetString("target"))

    def targetNotAvailable(self, player, exc):
        return "Nothing like that around here."

    def targetRadius(self, player):
        return 1

    def do(self, player, line, target):
        if target.location is not player.thing:
            raise eimaginary.ActionFailure(
                events.ThatDoesntMakeSense(
                    actor=player.thing,
                    actorMessage="You can't drop that."))

        try:
            target.moveTo(
                player.thing.location,
                arrivalEventFactory=lambda target: events.ArrivalEvent(
                    actor=player.thing,
                    actorMessage=("You drop ",
                                  language.Noun(target).definiteNounPhrase(),
                                  "."),
                    target=target,
                    targetMessage=(player.thing, " drops you."),
                    otherMessage=(player.thing, " drops ", target, ".")))
        except eimaginary.DoesntFit:
            raise insufficientSpace(player.thing)



DIRECTION_LITERAL = reduce(
    operator.xor, [
        pyparsing.Literal(d)
        for d
        in objects.OPPOSITE_DIRECTIONS]).setResultsName("direction")



class Dig(NoTargetAction):
    expr = (pyparsing.Literal("dig") +
            pyparsing.White() +
            DIRECTION_LITERAL +
            pyparsing.White() +
            pyparsing.restOfLine.setResultsName("name"))

    def do(self, player, line, direction, name):
        if iimaginary.IContainer(player.thing.location).getExitNamed(direction, None) is not None:
            raise eimaginary.ActionFailure(events.ThatDoesntMakeSense(
                actor=player.thing,
                actorMessage="There is already an exit in that direction."))

        room = objects.Thing(store=player.store, name=name)
        objects.Container.createFor(room, capacity=1000)
        objects.Exit.link(player.thing.location, room, direction)

        evt = events.Success(
            actor=player.thing,
            actorMessage="You create an exit.",
            otherMessage=language.Sentence([player.thing, " created an exit to the ", direction, "."]))
        evt.broadcast()

        # XXX Right now there can't possibly be anyone in the
        # destination room, but someday there could be.  When there
        # could be, broadcast this to them too.



class Bury(NoTargetAction):
    expr = (pyparsing.Literal("bury") +
            pyparsing.White() +
            DIRECTION_LITERAL)

    def do(self, player, line, direction):
        for exit in iimaginary.IContainer(player.thing.location).getExits():
            if exit.name == direction:
                if exit.sibling is not None:
                    evt = events.Success(
                        location=exit.toLocation,
                        otherMessage=language.Sentence([
                            exit.sibling, " crumbles and disappears."]))
                    evt.broadcast()

                evt = events.Success(
                    actor=player.thing,
                    actorMessage="It's gone.",
                    otherMessage=language.Sentence([
                        language.Noun(player.thing).nounPhrase(),
                        " destroyed ", exit, "."]))
                evt.broadcast()
                exit.destroy()
                return

        raise eimaginary.ActionFailure(events.ThatDoesntMakeSense(
            actor=player.thing,
            actorMessage="There isn't an exit in that direction."))



class Go(NoTargetAction):
    expr = (pyparsing.Optional(pyparsing.Literal("go") + pyparsing.White()) +
            DIRECTION_LITERAL)

    def do(self, player, line, direction):
        try:
            exit = iimaginary.IContainer(player.thing.location).getExitNamed(direction)
        except KeyError:
            raise eimaginary.ActionFailure(events.ThatDoesntWork(
                actor=player.thing,
                actorMessage=u"You can't go that way."))

        dest = exit.toLocation
        location = player.thing.location

        evt = events.Success(
            location=location,
            actor=player.thing,
            otherMessage=(player.thing, " leaves ", direction, "."))
        evt.broadcast()

        if exit.sibling is not None:
            arriveDirection = exit.sibling.name
        else:
            arriveDirection = object.OPPOSITE_DIRECTIONS[exit.name]

        try:
            player.thing.moveTo(
                dest,
                arrivalEventFactory=lambda player: events.MovementArrivalEvent(
                    thing=player,
                    origin=None,
                    direction=arriveDirection))
        except eimaginary.DoesntFit:
            raise eimaginary.ActionFailure(events.ThatDoesntWork(
                actor=player.thing,
                actorMessage=language.ExpressString(u"There's no room for you there.")))

        # XXX A convention for programmatically invoked actions?
        # None as the line?
        LookAround().do(player, "look")



class Restore(TargetAction):
    expr = (pyparsing.Literal("restore") +
            pyparsing.White() +
            pyparsing.restOfLine.setResultsName("target"))

    targetInterface = iimaginary.IActor

    def targetNotAvailable(self, player, exc):
        for thing in player.search(self.targetRadius(player), iimaginary.IThing, exc.partValue):
            return (language.Noun(thing).nounPhrase().plaintext(player), " cannot be restored.")
        return "Who's that?"

    def targetRadius(self, player):
        return 3


    def do(self, player, line, target):
        target.hitpoints.current = target.hitpoints.max
        target.stamina.current = target.stamina.max

        if player is target:
            evt = events.Success(
                actor=player.thing,
                actorMessage="You have fully restored yourself.")
            evt.broadcast()
        else:
            evt = events.Success(
                actor=player.thing,
                actorMessage=("You have restored ", target.thing, " to full health."),
                target=target.thing,
                targetMessage=(player.thing, " has restored you to full health."),
                otherMessage=(player.thing, " has restored ", target.thing, " to full health."))
            evt.broadcast()



class Hit(TargetAction):
    expr = ((pyparsing.Literal("hit") ^
             pyparsing.Literal("attack") ^
             pyparsing.Literal("kill")) +
            pyparsing.White() +
            pyparsing.restOfLine.setResultsName("target"))

    targetInterface = iimaginary.IActor

    def targetRadius(self, player):
        return 3

    def do(self, player, line, target):
        toBroadcast = []
        if target is player:
            raise eimaginary.ActionFailure(
                events.ThatDoesntMakeSense(u"Hit yourself?  Stupid.",
                                           actor=player.thing))

        cost = random.randrange(1, 5)
        if player.stamina < cost:
            raise eimaginary.ActionFailure(
                events.ThatDoesntWork(u"You're too tired!",
                                      actor=player.thing))

        damage = random.randrange(1, 5)
        player.stamina.decrease(cost)
        thp = target.hitpoints.decrease(damage)
        events.Success(
            actor=player.thing,
            target=target.thing,
            targetMessage=language.Sentence([player.thing, " hits you for ", damage, " hitpoints."]),
            actorMessage=language.Sentence(["You hit ", language.Noun(target.thing).definiteNounPhrase(), " for ", damage, " hitpoints."]),
            otherMessage=language.Sentence([player.thing, " hits ", target.thing, "."])).broadcast()

        if thp <= 0:
            xp = target.experience / 2 + 1
            player.gainExperience(xp) # I LOVE IT
            targetIsDead = [target.thing, " is dead!", "\n"]
            events.Success(
                actor=player.thing, target=target.thing,
                actorMessage=["\n", targetIsDead, "You gain ", xp, " experience"],
                targetMessage=["You are dead!"],
                otherMessage=targetIsDead).broadcast()
            target.thing.destroy()



class Say(NoTargetAction):
    expr = (((pyparsing.Literal("say") + pyparsing.White()) ^
             pyparsing.Literal("'")) +
            pyparsing.restOfLine.setResultsName("text"))

    def do(self, player, line, text):
        evt = events.SpeechEvent(speaker=player.thing, text=text)
        evt.broadcast()



class Emote(NoTargetAction):
    expr = (((pyparsing.Literal("emote") + pyparsing.White()) ^
             pyparsing.Literal(":")) +
            pyparsing.restOfLine.setResultsName("text"))

    def do(self, player, line, text):
        evt = events.Success(actor=player.thing,
                             actorMessage=[player.thing, " ", text],
                             otherMessage=[player.thing, " ", text])
        evt.broadcast()



class Actions(NoTargetAction):
    expr = pyparsing.Literal("actions")

    def do(self, player, line):
        cmds = dict.fromkeys(
            getattr(cmd, 'actionName', cmd.__name__.lower())
            for cmd
            in self.__class__.actions).keys()
        cmds.sort()
        player.send((iterutils.interlace(" ", cmds), "\n"))



class Search(NoTargetAction):
    expr = (pyparsing.Literal("search") +
            targetString("name"))

    def do(self, player, line, name):
        srch = player.thing.search(2, iimaginary.IVisible, name)
        evt = events.Success(
            actor=player.thing,
            actorMessage=language.ExpressList(
                list(iterutils.interlace('\n',
                                         (o.visualize()
                                          for o
                                          in srch)))))
        evt.broadcast()



class Score(NoTargetAction):
    expr = pyparsing.Literal("score")

    scoreFormat = (
        '/----------------------------------------------------------------------------\\\n'
        '| Level: %20d Experience: %10d\n'
        '| Hitpoints: %16s\n'
        '| Stamina: %18s\n'
        '\\----------------------------------------------------------------------------/\n')

    def do(self, player, line):
        events.Success(
            actor=player.thing,
            actorMessage=self.scoreFormat % (player.level, player.experience, player.hitpoints, player.stamina)).broadcast()



class ExpressWho(language.BaseExpress):
    header = (u"/============ Currently Playing ===========\\")
    footer = (u"\\================ Total %(playerCount)03d ===============/")

    def vt102(self, observer):
        players = self.original.connected

        return [[T.bold, self.header], u'\n',
                [[language.Noun(p).shortName().vt102(observer), u'\n']
                 for p in players],
                [T.bold, self.footer % {'playerCount': len(players)}], u'\n']



class Who(NoTargetAction):
    expr = pyparsing.Literal("who")

    def do(self, player, line):
        player.send(ExpressWho(player.store.findUnique(ImaginaryWorld)))



class Scrutinize(TargetAction):
    """
    Show detailed information about the model structure of a game object.
    """
    expr = (pyparsing.Literal("scrutinize") +
            pyparsing.White() +
            targetString("target"))

    def targetRadius(self, player):
        return 3

    def do(self, player, line, target):
        v = dict((k, getattr(target, k))
                  for (k, ign)
                  in target.getSchema()
                  if hasattr(target, k))

        targetContainer = iimaginary.IContainer(target, None)
        if targetContainer is not None:
            v['contents'] = list(targetContainer.getContents())
            exits = list(targetContainer.getExits())
            if exits:
                v['exits'] = exits
        s = pprint.pformat((target.__class__.__name__, v))
        # XXX FIXME Send a real Concept
        player.send(s, '\n')



class ExpressInventory(language.BaseExpress):
    implements(iimaginary.IConcept)

    def __init__(self, original):
        self.original = original

    def vt102(self, observer):
        return [[T.fg.yellow, "Inventory:\n"],
                [T.fg.green,
                 [(language.Noun(o).shortName().vt102(observer), '\n')
                  for o
                  in iimaginary.IContainer(self.original).getContents()]]]



class Inventory(NoTargetAction):
    expr = pyparsing.Literal("inventory")

    def do(self, player, line):
        events.Success(actor=player.thing,
                       actorMessage=ExpressInventory(player.thing)).broadcast()



class Set(TargetAction):
    """
    Direct model-level state manipulation command.
    """
    expr = (
        pyparsing.Literal("set") + pyparsing.White() +
        targetString("attribute") + pyparsing.White() +
        pyparsing.Literal("of") + pyparsing.White() +
        targetString("target") + pyparsing.White() +
        pyparsing.Literal("to") + pyparsing.White() +
        targetString("value"))

    def do(self, player, line, attribute, target, value):
        """
        Dispatch handling to an attribute-specific method.

        @type attribute: C{unicode}
        @param attribute: The model-level attribute of which to manipulate
            the value.  Handling of each attribute will be dispatched to a
            C{set_}-prefixed method for that attribute based on this value.

        @type target: L{Thing}
        @param target: The model object to manipulate.

        @type value: C{unicode}
        @param value: The new value for the specified attribute.
        """
        try:
            method = getattr(self, "set_" + attribute.upper())
        except AttributeError:
            raise eimaginary.ActionFailure(
                events.ThatDoesntMakeSense(
                    actor=player.thing,
                    actorMessage="You cannot set that."))
        else:
            method(player, line, target, value)


    def set_GENDER(self, player, line, target, value):
        """
        Attempt to change the gender of a thing.

        @param target: The thing to change the gender of.
        @param value: A string naming a gender on L{language.Gender}.
        """
        try:
            target.gender = getattr(language.Gender, value.upper())
        except AttributeError:
            gender = {language.Gender.MALE: "male",
                      language.Gender.FEMALE: "female",
                      language.Gender.NEUTER: "neuter"}.get(target.gender)
            raise eimaginary.ActionFailure(events.ThatDoesntMakeSense(
                    actor=player.thing,
                    actorMessage=("Only male, female, and neuter are valid "
                                  "genders.  You remain ", gender, ".")))
        else:
            if player.thing is target:
                # XXX Why can't I do something with Noun to collapse these
                # cases?
                event = events.Success(
                    actor=player.thing,
                    actorMessage=(u"You set your gender to ", value, "."))
            else:
                event = events.Success(
                    actor=player.thing,
                    target=target,
                    actorMessage=("You set ", language.Noun(target).hisHer(),
                                  " gender to ", value, "."),
                    targetMessage=(player.thing, " set your gender to ",
                                   value, "."))
            event.broadcast()


    def set_PROPER(self, player, line, target, value):
        """
        Attempt to change the name of a thing from a proper noun to a common
        noun or the other way around.

        @param target: The thing to change.
        @param value: The string C{"true"} or C{"false"}.
        """
        if value == "true":
            target.proper = True
            phrase = '" a proper noun.'
        elif value == "false":
            target.proper = False
            phrase = '" a common noun.'
        else:
            raise eimaginary.ActionFailure(
                events.ThatDoesntMakeSense(
                    actor=player.thing,
                    actorMessage=("Only true and false are valid settings "
                                  "for proper.")))
        events.Success(
            actor=player.thing,
            actorMessage=('You make the name of "',
                          language.Noun(target).shortName(),
                          phrase)).broadcast()



class Help(NoTargetAction):
    """
    A command for looking up help files.

    @cvar helpContentPath: The path in which to search for files.
    @type helpContentPath: L{filepath.FilePath}
    """
    expr = (pyparsing.Literal("help") +
            pyparsing.White() +
            pyparsing.restOfLine.setResultsName("topic"))

    helpContentPath = filepath.FilePath(imaginary.__file__).sibling(
        "resources").child("help")

    def do(self, player, line, topic):
        topic = topic.lower().strip()
        try:
            helpFile = self.helpContentPath.child(topic).open()
        except (OSError, IOError, filepath.InsecurePath):
            player.send("No help available on ", topic, ".", "\n")
        else:
            player.send(helpFile.read(), '\n')
