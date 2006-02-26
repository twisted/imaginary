
import os, random

from zope.interface import Interface

import pyparsing

from twisted.python import util, reflect, rebuild

import pottery
from pottery import ipottery, epottery, iterutils, commands, events, objects, text as T
from pottery.predicates import atLeastOne, isNot, And

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
                    raise epottery.AmbiguousArgument(k, objs)
                else:
                    kw[k] = objs[0]
        return self.do(player, line, **kw)

    def resolve(self, player, name, value):
        raise NotImplementedError("Don't know how to resolve %r (%r)" % (name, value))


class NoTargetAction(Action):
    """
    @cvar actorInterface
    """
    infrastructure = True

    actorInterface = ipottery.IPlayer

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

    targetInterface = ipottery.IObject

    def targetRadius(self, player):
        return 2

    def resolve(self, player, k, v):
        if k == "target":
            return list(player.search(self.targetRadius(player), self.targetInterface, v))
        return super(TargetAction, self).resolve(player, k, v)


class ToolAction(TargetAction):
    """
    @cvar toolInterface
    """
    infrastructure = True

    toolInterface = ipottery.IObject

    def toolRadius(self, player):
        return 2

    def resolve(self, player, k, v):
        if k == "tool":
            return list(player.search(self.toolRadius(player), self.toolInterface, v))
        return super(ToolAction, self).resolve(player, k, v)

class LookAround(NoTargetAction):
    commandName = "look"
    expr = pyparsing.Literal("look")

    def do(self, player, line):
        if player.location is None:
            player.send("You are floating in an empty, formless void.", "\n")
        else:
            player.send(player.location.longFormatTo(player), "\n")

class LookAt(TargetAction):
    commandName = "look"
    expr = (pyparsing.Literal("look") +
            pyparsing.Optional(pyparsing.White() +
                               pyparsing.Literal("at")) +
            pyparsing.White() +
            pyparsing.restOfLine.setResultsName("target"))

    def targetRadius(self, player):
        return 3

    def do(self, player, line, target):
        if player is not target:
            evt = events.Success(
                actor=player,
                target=target,
                actorMessage=target.longFormatTo(player),
                targetMessage=(player, " looks at you."))
            evt.broadcast()
        else:
            evt = events.Success(
                actor=player,
                actorMessage=target.longFormatTo(player))
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
            actor=player,
            actorMessage=("You change ", target, "'s description."),
            otherMessage=(player, " changes ", target, "'s description."))
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
            actor=player,
            actorMessage=("You change ", target, "'s name."),
            otherMessage=(player, " changes ", target, "'s name to ", name, "."))
        evt.broadcast()
        target.name = name

def tooHeavy(player, target):
    return events.ThatDoesntWork(
        actor=player, target=target,
        actorMessage=(target, " is too heavy to pick up."),
        otherMessage=(player, " struggles to lift ", target, ", but fails."),
        targetMessage=(player, " tries to pick you up, but fails."))

def targetTaken(player, target):
    return events.Success(
        actor=player, target=target,
        actorMessage=("You take ", target, "."),
        targetMessage=(player, " takes you."),
        otherMessage=(player, " takes ", target, "."))


class TakeFrom(ToolAction):
    commandName = "take"

    expr = ((pyparsing.Literal("get") ^ pyparsing.Literal("take")) +
            pyparsing.White() +
            commands.targetString("target") +
            pyparsing.Optional(pyparsing.White() +
                               pyparsing.Literal("from")) +
            pyparsing.White() +
            commands.targetString("tool"))

    def do(self, player, line, target, tool):
        try:
            target.moveTo(player)
        except epottery.DoesntFit:
            tooHeavy(player, target).broadcast()
        else:
            targetTaken(player, target).broadcast()


class Take(TargetAction):
    expr = ((pyparsing.Literal("get") ^ pyparsing.Literal("take")) +
            pyparsing.White() +
            commands.targetString("target"))

    def targetRadius(self, player):
        return 1

    def do(self, player, line, target):
        if target in (player, player.location) or target.location is player:
            evt = events.ThatDoesntMakeSense(
                actor=player,
                actorMessage=("You cannot take ", target, "."))
            evt.broadcast()
            return

        try:
            target.moveTo(player)
        except epottery.DoesntFit:
            tooHeavy(player, target).broadcast()
        else:
            targetTaken(player, target).broadcast()


def insufficientSpace(player):
    return events.ThatDoesntWork(
        actor=actor,
        actorMessage="There's not enough space for that.")

def creationSuccess(player, creation):
    return events.Success(
        actor=player,
        target=creation,
        actorMessage=(creation, " created."),
        targetMessage=(player, " creates you."),
        otherMessage=(player, " creates ", creation, "."))

class Spawn(NoTargetAction):
    expr = (pyparsing.Literal("spawn") +
            pyparsing.White() +
            commands.targetString("name") +
            pyparsing.Optional(pyparsing.White() +
                               pyparsing.restOfLine.setResultsName("description")))

    def do(self, player, line, name, description='an undescribed monster'):
        mob = objects.Mob(name, description)
        try:
            mob.moveTo(player.location)
        except epottery.DoesntFit:
            mob.destroy()
            insufficientSpace(player).broadcast()
        else:
            creationSuccess(player, mob).broadcast()

class Create(NoTargetAction):
    expr = (pyparsing.Literal("create") +
            pyparsing.White() +
            commands.targetString("name") +
            pyparsing.Optional(pyparsing.White() +
                               pyparsing.restOfLine.setResultsName("description")))

    def do(self, player, line, name, description='an undescribed object'):
        o = objects.Object(name, description)
        try:
            o.moveTo(player)
        except epottery.DoesntFit:
            o.destroy()
            insufficientSpace(player).broadcast()
        else:
            creationSuccess(player, o).broadcast()

class Drop(TargetAction):
    expr = (pyparsing.Literal("drop") +
            pyparsing.White() +
            commands.targetString("target"))

    def targetRadius(self, player):
        return 1

    def do(self, player, line, target):
        if target.location is not player:
            evt = events.ThatDoesntMakeSense(
                actor=player,
                actorMessage="You can't drop that.")
            evt.broadcast()
        else:
            try:
                target.moveTo(player.location)
            except epottery.DoesntFit:
                insufficientSpace(player).broadcast()
            else:
                evt = events.Success(
                    actor=player,
                    actorMessage=("You drop ", target, "."),
                    target=target,
                    targetMessage=(player, " drops you."),
                    otherMessage=(player, " drops ", target, "."))
                evt.broadcast()


class Dig(NoTargetAction):
    expr = (pyparsing.Literal("dig") +
            pyparsing.White() +
            (pyparsing.Literal("north") ^
             pyparsing.Literal("south") ^
             pyparsing.Literal("west") ^
             pyparsing.Literal("east")).setResultsName("direction") +
            pyparsing.White() +
            pyparsing.restOfLine.setResultsName("name"))

    def do(self, player, line, direction, name):
        if direction in player.location.exits:
            evt = events.ThatDoesntMakeSense(
                actor=player,
                actorMessage="There is already an exit in that direction.")
            evt.broadcast()
        else:
            room = objects.Room(name)
            player.location.exits[direction] = room
            room.exits[commands.OPPOSITE_DIRECTIONS[direction]] = player.location

            evt = events.Success(
                actor=player,
                actorMessage="You create an exit.",
                otherMessage=(player, " created an exit to the ", direction, "."))
            evt.broadcast()

            # XXX Right now there can't possibly be anyone in the
            # destination room, but someday there could be.  When there
            # could be, broadcast this to them too.


class Bury(NoTargetAction):
    expr = (pyparsing.Literal("bury") +
            pyparsing.White() +
            (pyparsing.Literal("north") ^
             pyparsing.Literal("south") ^
             pyparsing.Literal("west") ^
             pyparsing.Literal("east")).setResultsName("direction"))

    def do(self, player, line, direction):
        if direction not in player.location.exits:
            evt = events.ThatDoesntMakeSense(
                actor=player,
                actorMessage="There isn't an exit in that direction.")
            evt.broadcast()
        else:
            room = player.location.exits.pop(direction)
            try:
                room.exits.pop(commands.OPPOSITE_DIRECTIONS[direction])
            except KeyError:
                pass
            else:
                evt = events.Success(
                    location=room,
                    otherMessage=(
                        "The exit to the ",
                        commands.OPPOSITE_DIRECTIONS[direction], " ",
                        "crumbles and disappears."))
                evt.broadcast()

            evt = events.Success(
                actor=player,
                actorMessage="It's gone.",
                otherMessage=(player, " destroyed the exit to the ", direction, "."))
            evt.broadcast()

class Go(NoTargetAction):
    expr = (pyparsing.Optional(pyparsing.Literal("go") +
                               pyparsing.White()) +
            (pyparsing.Literal("north") ^
             pyparsing.Literal("south") ^
             pyparsing.Literal("west") ^
             pyparsing.Literal("east")).setResultsName("direction"))

    def do(self, player, line, direction):
        try:
            dest = player.location.exits[direction]
        except KeyError:
            evt = events.ThatDoesntWork(
                actor=player,
                actorMessage="You can't go that way.")
            evt.broadcast()
        else:
            location = player.location
            try:
                player.moveTo(dest)
            except epottery.DoesntFit:
                player.send("There's no room for you there.")
                return

            evt = events.Success(
                location=location,
                actor=player,
                otherMessage=(player, " leaves ", direction, "."))
            evt.broadcast()

            evt = events.Success(
                location=dest,
                actor=player,
                otherMessage=(player, " arrives from the ", commands.OPPOSITE_DIRECTIONS[direction], "."))
            evt.broadcast()

            LookAround().do(player, "look") # XXX A convention for
                                            # programmatically invoked
                                            # commands?  None as the
                                            # line?

# class Eat(Command):
#     expr = (pyparsing.Literal("eat") +
#             pyparsing.White() +
#             pyparsing.restOfLine.setResultsName("item"))

#     def run(self, player, line, item):
#         if item == 'flaming death':
#             player.send("Bye!")
#             Quit().run(player, line)
#             return
#         player.send("Yeuch.")

class Restore(TargetAction):
    expr = (pyparsing.Literal("restore") +
            pyparsing.White() +
            pyparsing.restOfLine.setResultsName("target"))

    def targetRadius(self, player):
        return 3

    def do(self, player, line, target):
        if not hasattr(target, 'hitpoints'):
            evt = events.ThatDoesntMakeSense(
                actor=player,
                actorMessage=(target, " cannot be restored."))
            evt.broadcast()
        else:
            target.hitpoints.current = target.hitpoints.max
            target.stamina.current = target.stamina.max

            if player is target:
                evt = events.Success(
                    actor=player,
                    actorMessage="You have fully restored yourself.")
                evt.broadcast()
            else:
                evt = events.Success(
                    actor=player,
                    actorMessage=("You have restored ", target, " to full health."),
                    target=target,
                    targetMessage=(player, " has restored you to full health."),
                    otherMessage=(player, " has restored ", target, " to full health."))
                evt.broadcast()


class Hit(TargetAction):
    expr = ((pyparsing.Literal("hit") ^
             pyparsing.Literal("attack") ^
             pyparsing.Literal("kill")) +
            pyparsing.White() +
            pyparsing.restOfLine.setResultsName("target"))

    def targetRadius(self, player):
        return 3

    def do(self, player, line, target):
        if target is player:
            player.send("Hit yourself?  Stupid.")
        else:
            cost = random.randrange(1, 5)
            if player.stamina < cost:
                player.send("You're too tired!")
            else:
                damage = random.randrange(1, 5)
                player.stamina.decrease(cost)
                thp = target.hitpoints.decrease(damage)
                target.send(player, " hits you for ", damage, " hitpoints.")
                player.send("You hit ", target, " for ", damage, " hitpoints.")

                if thp <= 0:
                    xp = target.experience / 2 + 1
                    player.gainExperience(xp)
                    player.send("\n",
                                target, " is dead!", "\n",
                                "You gain ", xp, " experience!")
                    target.send("You are dead!")
                    target.destroy()
                    player.location.broadcastIf(
                        isNot(player, target),
                        player, " has killed ", target, ".")

class Say(NoTargetAction):
    expr = (((pyparsing.Literal("say") + pyparsing.White()) ^
             pyparsing.Literal("'")) +
            pyparsing.restOfLine.setResultsName("text"))

    def do(self, player, line, text):
        player.send("You say, '" + text + "'\n")
        player.location.broadcastIf(
            And(isNot(player),
                atLeastOne('canSee', player)),
            player, " says, '", text, "'\n")

class Emote(NoTargetAction):
    expr = (((pyparsing.Literal("emote") + pyparsing.White()) ^
             pyparsing.Literal(":")) +
            pyparsing.restOfLine.setResultsName("text"))

    def do(self, player, line, text):
        player.send(player.name, " ", text, '\n')
        player.location.broadcastIf(
            And(isNot(player),
                atLeastOne('canSee', player)),
            player, " ", text, '\n')

# class Rebuild(NoTargetAction):
#     expr = pyparsing.Literal("rebuild")

#     def do(self, player, line):
#         rebuilt = []
#         for k, v in sys.modules.items():
#             if k.startswith('pottery.') and v is not None:
#                 rebuilt.append(k)
#                 rebuild.rebuild(v)
#         player.send("Rebuilt ", ', '.join(rebuilt), ".")

class Commands(NoTargetAction):
    expr = pyparsing.Literal("commands")

    def do(self, player, line):
        cmds = dict.fromkeys(
            getattr(cmd, 'commandName', cmd.__name__.lower())
            for cmd
            in self.__class__.commands.itervalues()).keys()
        cmds.sort()
        player.send((iterutils.interlace(" ", cmds), "\n"))

class Search(NoTargetAction):
    expr = (pyparsing.Literal("search") +
            commands.targetString("name"))

    def do(self, player, line, name):
        for thing in player.search(2, ipottery.IObject, name):
            player.send((thing.longFormatTo(player), '\n'))

class Score(NoTargetAction):
    expr = pyparsing.Literal("score")

    def do(self, player, line):
        player.send('/', '-' * 76, '\\', '\n',
                    '|', 'Level: ', player.level, ' Experience: ', player.experience, '\n',
                    '|', 'Hitpoints: ', player.hitpoints, '\n',
                    '|', 'Stamina: ', player.stamina, '\n',
                    '\\', '-' * 76, '/', '\n')

class Who(NoTargetAction):
    expr = pyparsing.Literal("who")

    header = ("/============ Currently Playing ===========\\")
    entry = ("| %(playerName)-40s |")
    footer = ("\\================ Total %(playerCount)03d ===============/")

    def do(self, player, line):
        connectedPlayers = player.realm.connected

        player.send(self.header + '\n')
        for p in connectedPlayers:
            player.send(self.entry % {'playerName': p.formatTo(player)} + '\n')
        player.send(self.footer % {'playerCount': len(connectedPlayers)} + '\n')

import pprint
class Scrutinize(TargetAction):
    expr = (pyparsing.Literal("scrutinize") +
            pyparsing.White() +
            commands.targetString("target"))

    def targetRadius(self, player):
        return 3

    def do(self, player, line, target):
        s = pprint.pformat((target.__class__.__name__, vars(target)))
        player.send(s, '\n')

class Inventory(NoTargetAction):
    expr = pyparsing.Literal("inventory")

    def do(self, player, line):
        player.send(
            [T.fg.yellow, "Inventory:\n"],
            [T.fg.green, [(o, '\n') for o in player.contents]])

class Quit(NoTargetAction):
    actorInterface = ipottery.IPlayer
    expr = pyparsing.Literal("quit")

    def do(self, player, line):
        player.proto.terminal.loseConnection()

class Help(NoTargetAction):
    expr = (pyparsing.Literal("help") +
            pyparsing.White() +
            commands.targetString("topic"))

    def do(self, player, line, topic):
        topic = topic.lower().strip()
        helpName = os.path.join(util.sibpath(pottery.__file__, 'resources'), 'help', topic)
        try:
            helpFile = file(helpName, 'r')
        except (OSError, IOError):
            player.send("No help available on ", topic, ".", "\n")
        else:
            player.send(helpFile.read(), '\n')
