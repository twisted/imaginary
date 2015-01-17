# -*- test-case-name: imaginary.test -*-

from __future__ import print_function

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
from imaginary.vision import visualizations

from imaginary.idea import (
    CanSee, Proximity, ProviderOf, Named, Traversability,
    Reachable, isKnownTo
)
from imaginary.iimaginary import IThing


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
        """
        Parse an action.
        """
        for eachActionType in self.actions:
            try:
                match = eachActionType.match(player, line)
            except pyparsing.ParseException:
                pass
            else:
                if match is not None:
                    match = dict(match)
                    for k,v in match.items():
                        if isinstance(v, pyparsing.ParseResults):
                            match[k] = v[0]

                    return eachActionType().runEventTransaction(player, line, match)
        return defer.fail(eimaginary.NoSuchCommand(line))



class Action(object):
    """
    An L{Action} represents an intention of a player to do something.
    """
    __metaclass__ = _ActionType
    infrastructure = True

    actorInterface = iimaginary.IActor

    def runEventTransaction(self, player, line, match):
        """
        Take a player, input, and dictionary of parse results, resolve those
        parse results into implementations of appropriate interfaces in the
        game world, and execute the actual Action implementation (contained in
        the 'do' method) in an event transaction.

        This is the top level of action invocation.

        @param player: A L{Thing} representing the actor's body.

        @param line: A unicode string containing the original input

        @param match: A dictionary containing some parse results to pass
            through to this L{Action}'s C{do} method as keyword arguments.

        @raise eimaginary.AmbiguousArgument: if multiple valid targets are
            found for an argument.
        """
        def thunk():
            begin = time.time()
            try:
                actor = self.actorInterface(player)
                for (k, v) in match.items():
                    try:
                        objs = self.resolve(player, k, v)
                    except NotImplementedError:
                        pass
                    else:
                        if len(objs) == 1:
                            match[k] = objs[0]
                        elif len(objs) == 0:
                            self.cantFind(player, actor, k, v)
                        else:
                            raise eimaginary.AmbiguousArgument(self, k, v, objs)
                return self.do(actor, line, **match)
            finally:
                end = time.time()
                log.msg(interface=iaxiom.IStatEvent,
                        stat_actionDuration=end - begin,
                        stat_actionExecuted=1)
        events.runEventTransaction(player.store, thunk)


    def cantFind(self, player, actor, slot, name):
        """
        This hook is invoked when a target cannot be found.

        This will delegate to a method like C{self.cantFind_<slot>(actor,
        name)} if one exists, to determine the error message to show to the
        actor.  It will then raise L{eimaginary.ActionFailure} to stop
        processing of this action.

        @param player: The L{Thing} doing the searching.

        @type player: L{IThing}

        @param actor: The L{IActor} doing the searching.

        @type actor: L{IActor}

        @param slot: The slot in question.

        @type slot: C{str}

        @param name: The name of the object being searched for.

        @type name: C{unicode}

        @raise eimaginary.ActionFailure: always.
        """
        func = getattr(self, "cantFind_"+slot, None)
        if func:
            msg = func(actor, name)
        else:
            msg = "Who's that?"
        raise eimaginary.ActionFailure(
            events.ThatDoesntWork(
                actorMessage=msg,
                actor=player))


    @classmethod
    def match(cls, player, line):
        """
        Parse the given C{line} using this L{Action} type's pyparsing C{expr}
        attribute.  A C{pyparsing.LineEnd} is appended to C{expr} to avoid
        accidentally matching a prefix instead of the whole line.

        @return: a list of 2-tuples of all the results of parsing, or None if
            the expression does not match the given line.

        @param line: a line of user input to be interpreted as an action.

        @see: L{imaginary.pyparsing}
        """
        return (cls.expr + pyparsing.LineEnd()).parseString(line)


    def do(self, player, line, **slots):
        """
        Subclasses override this method to actually perform the action.

        This method is performed in an event transaction, by 'run'.

        NB: The suggested implementation strategy for a 'do' method is to do
        action-specific setup but then delegate the bulk of the actual logic to
        a method on a target/tool interface.  The 'do' method's job is to
        select the appropriate methods to invoke.

        @param player: a provider of this L{Action}'s C{actorInterface}.

        @param line: the input string that created this action.

        @param slots: The results of calling C{self.resolve} on each parsing
        result (described by a setResultsName in C{self.expr}).
        """
        raise NotImplementedError("'do' method not implemented")


    def resolve(self, player, name, value):
        """
        Resolve a given parsed value to a valid action parameter by calling a
        'resolve_<name>' method on this L{Action} with the given C{player} and
        C{value}.

        @param player: the L{Thing} attempting to perform this action.

        @type player: L{Thing}

        @param name: the name of the slot being filled.  For example, 'target'.

        @type name: L{str}

        @param value: a string representing the value that was parsed.  For
            example, if the user typed 'get fish', this would be 'fish'.

        @return: a value which will be passed as the 'name' parameter to this
            L{Action}'s C{do} method.
        """
        resolver = getattr(self, 'resolve_%s' % (name,), None)
        if resolver is None:
            raise NotImplementedError(
                "Don't know how to resolve %r (%r)" % (name, value))
        return resolver(player, value)



def targetString(name):
    return (
        _quoteRemovingQuotedString ^
        UnicodeWord()).setResultsName(name)



class TargetAction(Action):
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

    def resolve_target(self, player, targetName):
        return _getIt(player, targetName,
                      self.targetInterface, self.targetRadius(player))



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

    def resolve_tool(self, player, toolName):
        return _getIt(player, toolName,
                      self.toolInterface, self.toolRadius(player))



def _getIt(player, thingName, iface, radius):
    """
    Retrieve game objects answering to the given name which provide the
    given interface and are within the given distance.

    @param player: The L{Thing} from which to search.

    @param radius: How many steps to traverse (note: this is wrong, it
        will become a real distance-y thing with real game-meaning
        someday).
    @type radius: C{float}

    @param iface: The interface which objects within the required range
        must be adaptable to in order to be returned.

    @param thingName: The name of the stuff.
    @type thingName: C{str}

    @return: An iterable of L{iimaginary.IThing} providers which are found.
    """
    providerOf = ProviderOf(iface)
    canSee = CanSee(providerOf, player)
    named = Named(thingName, canSee, player)
    reachable = Reachable(named)
    proximity = Proximity(radius, reachable)
    return list(player.obtainOrReportWhyNot(proximity))



class LookAround(Action):
    # TODO: replace this with an alias for 'look at here' or similar.
    actionName = "look"
    expr = pyparsing.Literal("look") + pyparsing.StringEnd()

    def do(self, player, line):
        ultimateLocation = player.thing.location
        while ultimateLocation.location is not None:
            ultimateLocation = ultimateLocation.location
        targets = visualizations(player.thing,
                                 lambda viewTarget:
                                 viewTarget.targetAs(IThing) is ultimateLocation)
        if targets:
            target = targets[0]
        else:
            target = u"You are floating in an empty, formless void."
        events.Success(actor=player.thing,
                       actorMessage=target).broadcast()



class LookAt(TargetAction):
    actionName = "look"
    expr = (pyparsing.Literal("look") +
            pyparsing.Optional(pyparsing.White() +
                               pyparsing.Literal("at")) +
            pyparsing.White() +
            pyparsing.restOfLine.setResultsName("target"))

    targetInterface = iimaginary.IVisible

    def resolve_target(self, player, targetName):
        """
        Resolve the target to look at by looking for a named, visible object in
        a proximity of 3 meters from the player.

        @param player: The player doing the looking.

        @type player: L{IThing}

        @param targetName: The name of the object we are looking for.

        @type targetName: C{unicode}

        @return: A list of the results of C{visualizeWithContents}.

        @rtype: C{list} of L{IConcept}

        @raise eimaginary.ActionFailure: with an appropriate message if the
            target cannot be resolved for an identifiable reason.  See
            L{imaginary.objects.Thing.obtainOrReportWhyNot} for a description
            of how such reasons may be identified.
        """
        return visualizations(player,
                              lambda path: isKnownTo(player, path, targetName))


    def cantFind_target(self, player, name):
        return "You don't see that."

    def targetRadius(self, player):
        return 3

    def do(self, player, line, target):
        if player.thing is not target:
            evt = events.Success(
                actor=player.thing,
                # sometimes 'target' is a thing you're looking at, and
                # therefore a DescriptionWithContents, and therefore has a
                # 'target' attribute; other times it's some random
                # ExpressString instance and you are not actually broadcasting
                # *to* anywhere.
                target=getattr(target, "target", None),
                actorMessage=target,
                targetMessage=(player.thing, " looks at you."))
        else:
            evt = events.Success(
                actor=player.thing,
                actorMessage=target)
        evt.broadcast()



class Illuminate(Action):
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



class Equipment(Action):
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

    def cantFind_target(self, player, targetName):
        return "Nothing like that around here."
    cantFind_tool = cantFind_target

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

    def cantFind_target(self, player, targetName):
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

    def cantFind_target(self, player, targetName):
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

    def cantFind_target(self, player, targetName):
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



_directionNames = objects.OPPOSITE_DIRECTIONS.keys()
_directionNames.extend(objects.DIRECTION_ALIASES.keys())

DIRECTION_LITERAL = reduce(
    operator.xor, [
        pyparsing.Literal(d)
        for d in _directionNames]).setResultsName("direction")



def expandDirection(direction):
    """
    Expand direction aliases into the names of the directions they refer to.
    """
    return objects.DIRECTION_ALIASES.get(direction, direction)



class Dig(Action):
    expr = (pyparsing.Literal("dig") +
            pyparsing.White() +
            DIRECTION_LITERAL +
            pyparsing.White() +
            pyparsing.restOfLine.setResultsName("name"))

    def do(self, player, line, direction, name):
        direction = expandDirection(direction)
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



class Bury(Action):
    expr = (pyparsing.Literal("bury") +
            pyparsing.White() +
            DIRECTION_LITERAL)

    def do(self, player, line, direction):
        direction = expandDirection(direction)
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



class Go(Action):
    expr = (
        (pyparsing.Literal("go") + pyparsing.White() +
         targetString("direction")) |
        (pyparsing.Literal("enter") + pyparsing.White() +
         targetString("direction")) |
        (pyparsing.Literal("exit") + pyparsing.White() +
         targetString("direction")) |
        DIRECTION_LITERAL)

    actorInterface = iimaginary.IThing

    def resolve_direction(self, player, directionName):
        """
        Identify a direction by having the player search for L{IExit}
        providers that they can see and reach.
        """
        directionName = expandDirection(directionName)
        return player.obtainOrReportWhyNot(
            Proximity(
                3.0,
                Traversability(
                    Named(directionName,
                          CanSee(ProviderOf(iimaginary.IExit)), player))))


    def cantFind_direction(self, actor, directionName):
        """
        Explain to the user that they can't go in a direction that they can't
        locate.
        """
        return u"You can't go that way."


    def do(self, player, line, direction):
        location = player.location

        evt = events.Success(
            location=location,
            actor=player,
            otherMessage=(player, " leaves ", direction.name, "."))
        evt.broadcast()

        try:
            direction.traverse(player)
        except eimaginary.DoesntFit:
            raise eimaginary.ActionFailure(events.ThatDoesntWork(
                actor=player,
                actorMessage=language.ExpressString(
                        u"There's no room for you there.")))

        # This is subtly incorrect: see http://divmod.org/trac/ticket/2917
        lookAroundActor = iimaginary.IActor(player)
        LookAround().do(lookAroundActor, "look")



class Restore(TargetAction):
    expr = (pyparsing.Literal("restore") +
            pyparsing.White() +
            pyparsing.restOfLine.setResultsName("target"))

    targetInterface = iimaginary.IActor

    def cantFind_target(self, player, targetName):
        # XXX Hoist this up to TargetAction and apply it generally.
        things = _getIt(
            player.thing,
            targetName,
            iimaginary.IThing,
            self.targetRadius(player))
        for thing in things:
            return (language.Noun(thing).nounPhrase().plaintext(player),
                    " cannot be restored.")
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



class Say(Action):
    expr = (((pyparsing.Literal("say") + pyparsing.White()) ^
             pyparsing.Literal("'")) +
            pyparsing.restOfLine.setResultsName("text"))

    def do(self, player, line, text):
        evt = events.SpeechEvent(speaker=player.thing, text=text)
        evt.broadcast()



class Emote(Action):
    expr = (((pyparsing.Literal("emote") + pyparsing.White()) ^
             pyparsing.Literal(":")) +
            pyparsing.restOfLine.setResultsName("text"))

    def do(self, player, line, text):
        evt = events.Success(actor=player.thing,
                             actorMessage=[player.thing, " ", text],
                             otherMessage=[player.thing, " ", text])
        evt.broadcast()



class Actions(Action):
    expr = pyparsing.Literal("actions")

    def do(self, player, line):
        cmds = dict.fromkeys(
            getattr(cmd, 'actionName', cmd.__name__.lower())
            for cmd
            in self.__class__.actions).keys()
        cmds.sort()
        player.send((iterutils.interlace(" ", cmds), "\n"))



class Commands(Action):
    """
    The I{commands} action provides a pointer to inexperienced players that
    they should be thinking in terms of I{actions} instead.

    This has no world side-effects; it just provides some user-interface
    information to the player.
    """
    expr = pyparsing.Literal("commands")

    def do(self, player, line):
        player.send("Try 'actions' instead.")



class Score(Action):
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



class Who(Action):
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



class Inventory(Action):
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



class Help(Action):
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
