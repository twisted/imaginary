# -*- test-case-name: imaginary.test -*-

import os, random, operator
import pprint

from zope.interface import implements

import pyparsing

from twisted.python import util
from twisted import plugin

from axiom import attributes

import imaginary.plugins
from imaginary.wiring import realm
from imaginary import (iimaginary, eimaginary, iterutils, commands, events,
                       objects, text as T, language)

class Action(commands.Command):
    infrastructure = True

    def run(self, player, line, **kw):
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

def getPlugins(iface, package):
    """Get plugins. See L{twisted.plugin.getPlugins}.

    I only exist so that I can be monkeypatched. :-S
    """
    return plugin.getPlugins(iface, package)


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


class TargetAction(NoTargetAction):
    """
    @cvar targetInterface
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
    @cvar toolInterface
    """
    infrastructure = True

    toolInterface = iimaginary.IThing

    def toolRadius(self, player):
        return 2

    def resolve(self, player, k, v):
        if k == "tool":
            return list(player.thing.search(self.toolRadius(player), self.toolInterface, v))
        return super(ToolAction, self).resolve(player, k, v)



class LookAround(NoTargetAction):
    commandName = "look"
    expr = pyparsing.Literal("look") + pyparsing.StringEnd()

    def do(self, player, line):
        if player.thing.location is None:
            concept = u"You are floating in an empty, formless void."
        else:
            concept = language.Noun(player.thing.location).description()
        events.Success(actor=player.thing,
                       actorMessage=concept).broadcast()



class LookAt(TargetAction):
    commandName = "look"
    expr = (pyparsing.Literal("look") +
            pyparsing.Optional(pyparsing.White() +
                               pyparsing.Literal("at")) +
            pyparsing.White() +
            pyparsing.restOfLine.setResultsName("target"))

    def targetNotAvailable(self, player, exc):
        return "You don't see that."

    def targetRadius(self, player):
        return 3

    def do(self, player, line, target):
        if player.thing is not target:
            evt = events.Success(
                actor=player.thing,
                target=target,
                actorMessage=language.Noun(target).description(),
                targetMessage=(player.thing, " looks at you."))
        else:
            evt = events.Success(
                actor=player.thing,
                actorMessage=language.Noun(target).description())
        evt.broadcast()

class Describe(TargetAction):
    expr = (pyparsing.Literal("describe") +
            pyparsing.White() +
            commands.targetString("target") +
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
            commands.targetString("target") +
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
            commands.targetString("target"))

    targetInterface = iimaginary.IContainer

    def do(self, player, line, target):
        dnf = language.Noun(target.thing).definiteNounPhrase()
        if not target.closed:
            evt = events.ThatDoesntWork(
                actor=player.thing,
                target=target.thing,
                actorMessage=language.Sentence([dnf, " is already open."]))
        else:
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
            commands.targetString("target"))

    targetInterface = iimaginary.IContainer

    def do(self, player, line, target):
        dnf = language.Noun(target.thing).definiteNounPhrase()
        if target.closed:
            evt = events.ThatDoesntWork(
                actor=player.thing,
                target=target.thing,
                actorMessage=language.Sentence([dnf, " is already closed."]))
        else:
            target.closed = True
            evt = events.Success(
                actor=player.thing,
                target=target.thing,
                actorMessage=("You close ", dnf, "."),
                targetMessage=language.Sentence([player.thing, " closes you."]),
                otherMessage=language.Sentence([player.thing, " closes ", target.thing, "."]))
        evt.broadcast()



def tooHeavy(player, target):
    return events.ThatDoesntWork(
        actor=player, target=target,
        actorMessage=(target, " is too heavy to pick up."),
        otherMessage=(player, " struggles to lift ", target, ", but fails."),
        targetMessage=(player, " tries to pick you up, but fails."))

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
            commands.targetString("target"))

    targetInterface = iimaginary.IClothing
    actorInterface = iimaginary.IClothingWearer

    def do(self, player, line, target):
        from imaginary import garments
        try:
            player.takeOff(target)
        except garments.InaccessibleGarment, e:
            evt = events.ThatDoesntWork(
                actor=player.thing,
                target=target.thing,
                actorMessage=(u"You cannot take off ",
                              target.thing,
                              u" because you are wearing ",
                              e.obscuringGarment.thing, u"."),
                otherMessage=language.Sentence([
                    player.thing,
                    u" gets a dumb look on ",
                    language.Noun(player.thing).hisHer(),
                    u" face."]))
        else:
            evt = events.Success(
                actor=player.thing,
                target=target.thing,
                actorMessage=(u"You take off ", target.thing, u"."),
                otherMessage=language.Sentence([
                    player.thing, u" takes off ", target.thing, u"."]))
        evt.broadcast()



class Wear(TargetAction):
    expr = (pyparsing.Literal("wear") +
            pyparsing.White() +
            commands.targetString("target"))

    targetInterface = iimaginary.IClothing
    actorInterface = iimaginary.IClothingWearer

    def do(self, player, line, target):
        from imaginary import garments
        try:
            player.putOn(target)
        except garments.TooBulky, e:
            evt = events.ThatDoesntWork(
                actor=player.thing,
                target=target.thing,
                actorMessage=language.Sentence([
                    language.Noun(e.wornGarment.thing).definiteNounPhrase(),
                    u" you are already wearing is too bulky for you to do"
                    u" that."]),
                otherMessage=language.Sentence([
                    player.thing,
                    u" wrestles with basic personal problems."]))
        else:
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
            attributes.AND(
                garments.Garment.thing == objects.Thing.storeID,
                garments.Garment.wearer == player),
            sort=objects.Thing.name.ascending).getColumn("name"))
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
    commandName = "take"

    expr = ((pyparsing.Literal("get") ^ pyparsing.Literal("take")) +
            pyparsing.White() +
            commands.targetString("target") +
            pyparsing.Optional(pyparsing.White() +
                               pyparsing.Literal("from")) +
            pyparsing.White() +
            commands.targetString("tool"))

    def targetNotAvailable(self, player, exc):
        return "Nothing like that around here."
    toolNotAvailable = targetNotAvailable

    def do(self, player, line, target, tool):
        # XXX Make sure target is in tool
        try:
            target.moveTo(player.thing)
        except eimaginary.DoesntFit:
            tooHeavy(player.thing, target).broadcast()
        else:
            targetTaken(player.thing, target, tool).broadcast()



class PutIn(ToolAction):

    toolInterface = iimaginary.IThing
    targetInterface = iimaginary.IContainer

    def targetNotAvailable(self, player, exc):
        return "That doesn't work."

    expr = (pyparsing.Literal("put") +
            pyparsing.White() +
            commands.targetString("tool") +
            pyparsing.Optional(pyparsing.White() +
                               pyparsing.Literal("in")) +
            pyparsing.White() +
            commands.targetString("target"))

    def do(self, player, line, tool, target):
        ctool = iimaginary.IContainer(tool, None)
        targetObject = target.thing
        if ctool is not None and (ctool.contains(targetObject) or ctool is target):
            evt = events.ThatDoesntWork(actor=player.thing, target=targetObject, tool=tool,
                                        actorMessage="A thing cannot contain itself in euclidean space.")
        else:
            dnf = language.Noun(targetObject).definiteNounPhrase()
            try:
                tool.moveTo(target)
            except eimaginary.DoesntFit:
                # <allexpro> dash: put me in a tent and give it to moshez!
                evt = events.ThatDoesntWork(actor=player.thing, target=targetObject, tool=tool)
            except eimaginary.Closed:
                evt = events.ThatDoesntWork(actor=player.thing,
                                            target=targetObject,
                                            tool=tool,
                                            actorMessage=language.Sentence([dnf, " is closed."]))
            else:
                evt = events.Success(
                    actor=player.thing,
                    target=targetObject,
                    tool=tool,
                    actorMessage=("You put ", tool, " in ", dnf, "."),
                    targetMessage=language.Sentence([player.thing, " puts ", " tool in you."]),
                    toolMessage=language.Sentence([player.thing, " puts you in ", targetObject, "."]),
                    otherMessage=language.Sentence([player.thing, " puts ", tool, " in ", targetObject, "."]))
        evt.broadcast()



class Take(TargetAction):
    expr = ((pyparsing.Literal("get") ^ pyparsing.Literal("take")) +
            pyparsing.White() +
            commands.targetString("target"))

    def targetNotAvailable(self, player, exc):
        return u"Nothing like that around here."

    def targetRadius(self, player):
        return 1

    def do(self, player, line, target):
        if target in (player.thing, player.thing.location) or target.location is player.thing:
            evt = events.ThatDoesntMakeSense(
                actor=player.thing,
                actorMessage=("You cannot take ", target, "."))
            evt.broadcast()
            return

        try:
            target.moveTo(player.thing)
        except eimaginary.DoesntFit:
            tooHeavy(player.thing, target).broadcast()
        else:
            targetTaken(player.thing, target).broadcast()



def insufficientSpace(player):
    return events.ThatDoesntWork(
        actor=player,
        actorMessage="There's not enough space for that.")



def creationSuccess(player, creation):
    return events.Success(
        actor=player,
        target=creation,
        actorMessage=language.Sentence([creation, " created."]),
        targetMessage=language.Sentence([player, " creates you."]),
        otherMessage=language.Sentence([player, " creates ", creation, "."]))



class Spawn(NoTargetAction):
    expr = (pyparsing.Literal("spawn") +
            pyparsing.White() +
            commands.targetString("name") +
            pyparsing.Optional(pyparsing.White() +
                               pyparsing.restOfLine.setResultsName("description")))

    def do(self, player, line, name, description=u'an undescribed monster'):
        mob = objects.Thing(store=player.store, name=name, description=description)
        objects.Actor(store=player.store).installOn(mob)
        try:
            mob.moveTo(player.thing.location)
        except eimaginary.DoesntFit:
            mob.destroy()
            insufficientSpace(player.thing).broadcast()
        else:
            creationSuccess(player.thing, mob).broadcast()



class Create(NoTargetAction):
    expr = (pyparsing.Literal("create") +
            pyparsing.White() +
            commands.targetString("typeName") +
            pyparsing.White() +
            commands.targetString("name") +
            pyparsing.Optional(pyparsing.White() +
                               pyparsing.restOfLine.setResultsName("description")))

    def do(self, player, line, typeName, name, description=None):
        if not description:
            description = u'an undescribed object'
        for plug in getPlugins(iimaginary.IThingType, imaginary.plugins):
            if plug.type == typeName:
                o = plug.getType()(store=player.store, name=name,
                                   description=description, proper=True)
                break
        else:
            raise ValueError("Can't find " + typeName)
        try:
            o.moveTo(player.thing)
        except eimaginary.DoesntFit:
            o.destroy()
            insufficientSpace(player.thing).broadcast()
        else:
            creationSuccess(player.thing, o).broadcast()



class Drop(TargetAction):
    expr = (pyparsing.Literal("drop") +
            pyparsing.White() +
            commands.targetString("target"))

    def targetNotAvailable(self, player, exc):
        return "Nothing like that around here."

    def targetRadius(self, player):
        return 1

    def do(self, player, line, target):
        if target.location is not player.thing:
            evt = events.ThatDoesntMakeSense(
                actor=player.thing,
                actorMessage="You can't drop that.")
            evt.broadcast()
        else:
            try:
                target.moveTo(player.thing.location)
            except eimaginary.DoesntFit:
                insufficientSpace(player.thing).broadcast()
            else:
                evt = events.Success(
                    actor=player.thing,
                    actorMessage=("You drop ", target, "."),
                    target=target,
                    targetMessage=(player.thing, " drops you."),
                    otherMessage=(player.thing, " drops ", target, "."))
                evt.broadcast()



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
        if player.thing.location.getExitNamed(direction, None) is not None:
            evt = events.ThatDoesntMakeSense(
                actor=player.thing,
                actorMessage="There is already an exit in that direction.")
            evt.broadcast()
        else:
            room = objects.Thing(store=player.store, name=name)
            objects.Container(store=player.store, capacity=1000).installOn(room)
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
        for exit in player.thing.location.getExits():
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

        evt = events.ThatDoesntMakeSense(
            actor=player.thing,
            actorMessage="There isn't an exit in that direction.")
        evt.broadcast()



class Go(NoTargetAction):
    expr = (pyparsing.Optional(pyparsing.Literal("go") + pyparsing.White()) +
            DIRECTION_LITERAL)

    def do(self, player, line, direction):
        try:
            exit = player.thing.location.getExitNamed(direction)
        except KeyError:
            evt = events.ThatDoesntWork(
                actor=player.thing,
                actorMessage="You can't go that way.")
            evt.broadcast()
        else:
            dest = exit.toLocation
            location = player.thing.location
            try:
                player.thing.moveTo(dest)
            except eimaginary.DoesntFit:
                player.send("There's no room for you there.")
                return

            evt = events.Success(
                location=location,
                actor=player.thing,
                otherMessage=(player.thing, " leaves ", direction, "."))
            evt.broadcast()

            if exit.sibling is not None:
                arriveDirection = exit.sibling.name
            else:
                arriveDirection = object.OPPOSITE_DIRECTIONS[exit.name]

            evt = events.Success(
                location=dest,
                actor=player.thing,
                otherMessage=(player.thing, " arrives from the ", arriveDirection, "."))
            evt.broadcast()

            LookAround().do(player, "look") # XXX A convention for
                                            # programmatically invoked
                                            # commands?  None as the
                                            # line?

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
            toBroadcast.append(events.ThatDoesntMakeSense("Hit yourself?  Stupid.", actor=player.thing))
        else:
            cost = random.randrange(1, 5)
            if player.stamina < cost:
                toBroadcast.append(events.ThatDoesntWork("You're too tired!", actor=player.thing))
            else:
                damage = random.randrange(1, 5)
                player.stamina.decrease(cost)
                thp = target.hitpoints.decrease(damage)
                toBroadcast.append(events.Success(
                    actor=player.thing,
                    target=target.thing,
                    targetMessage=language.Sentence([player.thing, " hits you for ", damage, " hitpoints."]),
                    actorMessage=language.Sentence(["You hit ", language.Noun(target.thing).definiteNounPhrase(), " for ", damage, " hitpoints."]),
                    otherMessage=language.Sentence([player.thing, " hits ", target.thing, "."])))
                if thp <= 0:
                    xp = target.experience / 2 + 1
                    player.gainExperience(xp) # I LOVE IT
                    targetIsDead = [target.thing, " is dead!", "\n"]
                    toBroadcast.append(events.Success(
                        actor=player.thing, target=target.thing,
                        actorMessage=["\n", targetIsDead, "You gain ", xp, " experience"],
                        targetMessage=["You are dead!"],
                        otherMessage=targetIsDead))
                    target.thing.destroy()
        for event in toBroadcast:
            event.broadcast()



class Say(NoTargetAction):
    expr = (((pyparsing.Literal("say") + pyparsing.White()) ^
             pyparsing.Literal("'")) +
            pyparsing.restOfLine.setResultsName("text"))

    def do(self, player, line, text):
        evt = events.Success(actor=player.thing,
                             actorMessage=["You say, '", text, "'"],
                             otherMessage=[player.thing, " says, '", text, "'"])
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

# class Rebuild(NoTargetAction):
#     expr = pyparsing.Literal("rebuild")

#     def do(self, player, line):
#         rebuilt = []
#         for k, v in sys.modules.items():
#             if k.startswith('imaginary.') and v is not None:
#                 rebuilt.append(k)
#                 rebuild.rebuild(v)
#         iimaginary.IActor(player).send("Rebuilt ", ', '.join(rebuilt), ".")

class Commands(NoTargetAction):
    expr = pyparsing.Literal("commands")

    def do(self, player, line):
        cmds = dict.fromkeys(
            getattr(cmd, 'commandName', cmd.__name__.lower())
            for cmd
            in self.__class__.commands).keys()
        cmds.sort()
        player.send((iterutils.interlace(" ", cmds), "\n"))



class Search(NoTargetAction):
    expr = (pyparsing.Literal("search") +
            commands.targetString("name"))

    def do(self, player, line, name):
        srch = player.thing.search(2, iimaginary.IThing, name)
        evt = events.Success(
            actor=player.thing,
            actorMessage=language.ExpressList(
                list(iterutils.interlace('\n',
                                         (language.Noun(o).description()
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
        player.send(ExpressWho(player.store.findUnique(realm.ImaginaryRealm)))



class Scrutinize(TargetAction):
    expr = (pyparsing.Literal("scrutinize") +
            pyparsing.White() +
            commands.targetString("target"))

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

        exits = list(target.getExits())
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



class Help(NoTargetAction):
    expr = (pyparsing.Literal("help") +
            pyparsing.White() +
            commands.targetString("topic"))

    def do(self, player, line, topic):
        topic = topic.lower().strip()
        helpName = os.path.join(util.sibpath(imaginary.__file__, 'resources'), 'help', topic)
        try:
            helpFile = file(helpName, 'r')
        except (OSError, IOError):
            player.send("No help available on ", topic, ".", "\n")
        else:
            player.send(helpFile.read(), '\n')
