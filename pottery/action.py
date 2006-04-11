# -*- test-case-name: pottery.test -*-

import os, random

from zope.interface import Interface

import pyparsing

from twisted.python import util, rebuild, components
from twisted import plugin

import pottery.plugins
from pottery import (ipottery, epottery, iterutils, commands, events,
                     objects, text as T)

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
                    raise epottery.AmbiguousArgument(self, k, v, objs)
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

    actorInterface = ipottery.IActor

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
            return list(player.installedOn.search(self.targetRadius(player), self.targetInterface, v))
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
            return list(player.installedOn.search(self.toolRadius(player), self.toolInterface, v))
        return super(ToolAction, self).resolve(player, k, v)

class LookAround(NoTargetAction):
    commandName = "look"
    expr = pyparsing.Literal("look")

    def do(self, player, line):
        if player.installedOn.location is None:
            player.send("You are floating in an empty, formless void.", "\n")
        else:
            player.send(player.installedOn.location.longFormatTo(player.installedOn), "\n")

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
        if player.installedOn is not target:
            evt = events.Success(
                actor=player.installedOn,
                target=target,
                actorMessage=target.longFormatTo(player.installedOn),
                targetMessage=(player.installedOn, " looks at you."))
            evt.broadcast()
        else:
            evt = events.Success(
                actor=player.installedOn,
                actorMessage=target.longFormatTo(player.installedOn))
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
            actor=player.installedOn,
            actorMessage=("You change ", target, "'s description."),
            otherMessage=(player.installedOn, " changes ", target, "'s description."))
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
            actor=player.installedOn,
            actorMessage=("You change ", target, "'s name."),
            otherMessage=(player.installedOn, " changes ", target, "'s name to ", name, "."))
        evt.broadcast()
        target.name = name



class Open(TargetAction):
    expr = (pyparsing.Literal("open") +
            pyparsing.White() +
            commands.targetString("target"))

    targetInterface = ipottery.IContainer

    def do(self, player, line, target):
        if not target.closed:
            evt = events.ThatDoesntWork(
                actor=player.installedOn,
                target=target.installedOn,
                actorMessage=(target.installedOn, " is already open."))
        else:
            target.closed = False
            evt = events.Success(
                actor=player.installedOn,
                target=target.installedOn,
                actorMessage=("You open ", target.installedOn, "."),
                targetMessage=(player.installedOn, " opens you."),
                otherMessage=(player.installedOn, " opens ", target.installedOn, "."))
        evt.broadcast()



class Close(TargetAction):
    expr = (pyparsing.Literal("close") +
            pyparsing.White() +
            commands.targetString("target"))

    targetInterface = ipottery.IContainer

    def do(self, player, line, target):
        if target.closed:
            evt = events.ThatDoesntWork(
                actor=player.installedOn,
                target=target.installedOn,
                actorMessage=(target.installedOn, " is already closed."))
        else:
            target.closed = True
            evt = events.Success(
                actor=player.installedOn,
                target=target.installedOn,
                actorMessage=("You close ", target.installedOn, "."),
                targetMessage=(player.installedOn, " closes you."),
                otherMessage=(player.installedOn, " closes ", target.installedOn, "."))
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
    return events.Success(
        actor=player,
        target=target,
        tool=container,
        actorMessage=("You take ", target, " from ", container, "."),
        targetMessage=(player, " takes you from ", container, "."),
        toolMessage=(player, " takes ", target, " from you."),
        otherMessage=(player, " takes ", target, " from ", container, "."))


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
            target.moveTo(player.installedOn)
        except epottery.DoesntFit:
            tooHeavy(player.installedOn, target).broadcast()
        else:
            targetTaken(player.installedOn, target, tool).broadcast()



## <allexpro> dash: put me in a tent and give it to moshez!
class PutIn(ToolAction):
    toolInterface = ipottery.IObject
    targetInterface = ipottery.IContainer

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
        ctool = ipottery.IContainer(tool, None)
        targetObject = target.installedOn
        if ctool is not None and (ctool.contains(targetObject) or ctool is target):
            evt = events.ThatDoesntWork(actor=player.installedOn, target=targetObject, tool=tool,
                                        actorMessage="A thing cannot contain itself in euclidean space.")
        else:
            try:
                tool.moveTo(target)
            except epottery.DoesntFit:
                evt = events.ThatDoesntWork(actor=player.installedOn, target=targetObject, tool=tool)
            except epottery.Closed:
                evt = events.ThatDoesntWork(actor=player.installedOn, target=targetObject, tool=tool, actorMessage=(targetObject, " is closed."))
            else:
                evt = events.Success(
                    actor=player.installedOn, target=targetObject, tool=tool,
                    actorMessage=("You put ", tool, " in ", targetObject, "."),
                    targetMessage=(player.installedOn, " puts ", " tool in you."),
                    toolMessage=(player.installedOn, " puts you in ", targetObject, "."),
                    otherMessage=(player.installedOn, " puts ", tool, " in ", targetObject, "."))
        evt.broadcast()


class Take(TargetAction):
    expr = ((pyparsing.Literal("get") ^ pyparsing.Literal("take")) +
            pyparsing.White() +
            commands.targetString("target"))

    def targetNotAvailable(self, player, exc):
        return "Nothing like that around here."

    def targetRadius(self, player):
        return 1

    def do(self, player, line, target):
        if target in (player.installedOn, player.installedOn.location) or target.location is player.installedOn:
            evt = events.ThatDoesntMakeSense(
                actor=player.installedOn,
                actorMessage=("You cannot take ", target, "."))
            evt.broadcast()
            return

        try:
            target.moveTo(player.installedOn)
        except epottery.DoesntFit:
            tooHeavy(player.installedOn, target).broadcast()
        else:
            targetTaken(player.installedOn, target).broadcast()


def insufficientSpace(player):
    return events.ThatDoesntWork(
        actor=player,
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

    def do(self, player, line, name, description=u'an undescribed monster'):
        mob = objects.Object(store=player.store, name=name, description=description)
        objects.Actor(store=player.store).installOn(mob)
        try:
            mob.moveTo(player.installedOn.location)
        except epottery.DoesntFit:
            mob.destroy()
            insufficientSpace(player.installedOn).broadcast()
        else:
            creationSuccess(player.installedOn, mob).broadcast()

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
        for plug in getPlugins(ipottery.IObjectType, pottery.plugins):
            if plug.type == typeName:
                o = plug.getType()(store=player.store, name=name, description=description)
                break
        else:
            raise ValueError("Can't find " + typeName)
        try:
            o.moveTo(player.installedOn)
        except epottery.DoesntFit:
            o.destroy()
            insufficientSpace(player.installedOn).broadcast()
        else:
            creationSuccess(player.installedOn, o).broadcast()

class Drop(TargetAction):
    expr = (pyparsing.Literal("drop") +
            pyparsing.White() +
            commands.targetString("target"))

    def targetNotAvailable(self, player, exc):
        return "Nothing like that around here."

    def targetRadius(self, player):
        return 1

    def do(self, player, line, target):
        if target.location is not player.installedOn:
            evt = events.ThatDoesntMakeSense(
                actor=player.installedOn,
                actorMessage="You can't drop that.")
            evt.broadcast()
        else:
            try:
                target.moveTo(player.installedOn.location)
            except epottery.DoesntFit:
                insufficientSpace(player.installedOn).broadcast()
            else:
                evt = events.Success(
                    actor=player.installedOn,
                    actorMessage=("You drop ", target, "."),
                    target=target,
                    targetMessage=(player.installedOn, " drops you."),
                    otherMessage=(player.installedOn, " drops ", target, "."))
                evt.broadcast()


class Dig(NoTargetAction):
    expr = (pyparsing.Literal("dig") +
            pyparsing.White() +
            (pyparsing.Literal(u"north") ^
             pyparsing.Literal(u"south") ^
             pyparsing.Literal(u"west") ^
             pyparsing.Literal(u"east")).setResultsName("direction") +
            pyparsing.White() +
            pyparsing.restOfLine.setResultsName("name"))

    def do(self, player, line, direction, name):
        if player.installedOn.location.getExitNamed(direction, None) is not None:
            evt = events.ThatDoesntMakeSense(
                actor=player.installedOn,
                actorMessage="There is already an exit in that direction.")
            evt.broadcast()
        else:
            room = objects.Object(store=player.store, name=name)
            objects.Container(store=player.store, capacity=1000).installOn(room)
            objects.Exit.link(player.installedOn.location, room, direction)

            evt = events.Success(
                actor=player.installedOn,
                actorMessage="You create an exit.",
                otherMessage=(player.installedOn, " created an exit to the ", direction, "."))
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
        for exit in player.installedOn.location.getExits():
            if exit.name == direction:
                if exit.sibling is not None:
                    evt = events.Success(
                        location=exit.toLocation,
                        otherMessage=(exit.sibling,
                                      " crumbles and disappears."))
                    evt.broadcast()

                evt = events.Success(
                    actor=player.installedOn,
                    actorMessage="It's gone.",
                    otherMessage=(player.installedOn, " destroyed ", exit, "."))
                evt.broadcast()
                exit.destroy()
                return

        evt = events.ThatDoesntMakeSense(
            actor=player.installedOn,
            actorMessage="There isn't an exit in that direction.")
        evt.broadcast()


class Go(NoTargetAction):
    expr = (pyparsing.Optional(pyparsing.Literal("go") +
                               pyparsing.White()) +
            (pyparsing.Literal(u"north") ^
             pyparsing.Literal(u"south") ^
             pyparsing.Literal(u"west") ^
             pyparsing.Literal(u"east")).setResultsName("direction"))

    def do(self, player, line, direction):
        try:
            exit = player.installedOn.location.getExitNamed(direction)
        except KeyError:
            evt = events.ThatDoesntWork(
                actor=player.installedOn,
                actorMessage="You can't go that way.")
            evt.broadcast()
        else:
            dest = exit.toLocation
            location = player.installedOn.location
            try:
                player.installedOn.moveTo(dest)
            except epottery.DoesntFit:
                player.send("There's no room for you there.")
                return

            evt = events.Success(
                location=location,
                actor=player.installedOn,
                otherMessage=(player.installedOn, " leaves ", direction, "."))
            evt.broadcast()

            if exit.sibling is not None:
                arriveDirection = exit.sibling.name
            else:
                arriveDirection = object.OPPOSITE_DIRECTIONS[exit.name]

            evt = events.Success(
                location=dest,
                actor=player.installedOn,
                otherMessage=(player.installedOn, " arrives from the ", arriveDirection, "."))
            evt.broadcast()

            LookAround().do(player, "look") # XXX A convention for
                                            # programmatically invoked
                                            # commands?  None as the
                                            # line?

class Restore(TargetAction):
    expr = (pyparsing.Literal("restore") +
            pyparsing.White() +
            pyparsing.restOfLine.setResultsName("target"))

    targetInterface = ipottery.IActor

    def targetNotAvailable(self, player, exc):
        for thing in player.search(self.targetRadius(player), ipottery.IObject, exc.partValue):
            return (thing, " cannot be restored.")
        return "Who's that?"

    def targetRadius(self, player):
        return 3


    def do(self, player, line, target):
        target.hitpoints.current = target.hitpoints.max
        target.stamina.current = target.stamina.max

        if player is target:
            evt = events.Success(
                actor=player.installedOn,
                actorMessage="You have fully restored yourself.")
            evt.broadcast()
        else:
            evt = events.Success(
                actor=player.installedOn,
                actorMessage=("You have restored ", target.installedOn, " to full health."),
                target=target.installedOn,
                targetMessage=(player.installedOn, " has restored you to full health."),
                otherMessage=(player.installedOn, " has restored ", target.installedOn, " to full health."))
            evt.broadcast()


class Hit(TargetAction):
    expr = ((pyparsing.Literal("hit") ^
             pyparsing.Literal("attack") ^
             pyparsing.Literal("kill")) +
            pyparsing.White() +
            pyparsing.restOfLine.setResultsName("target"))

    targetInterface = ipottery.IActor

    def targetRadius(self, player):
        return 3

    def do(self, player, line, target):
        toBroadcast = []
        if target is player:
            toBroadcast.append(events.ThatDoesntMakeSense("Hit yourself?  Stupid.", actor=player.installedOn))
        else:
            cost = random.randrange(1, 5)
            if player.stamina < cost:
                toBroadcast.append(events.ThatDoesntWork("You're too tired!", actor=player.installedOn))
            else:
                damage = random.randrange(1, 5)
                player.stamina.decrease(cost)
                thp = target.hitpoints.decrease(damage)
                toBroadcast.append(events.Success(targetMessage=[player.installedOn, " hits you for ", damage, " hitpoints."],
                                                  actorMessage=["You hit ", target.installedOn, " for ", damage, " hitpoints."],
                                                  otherMessage=[player.installedOn, " hits ", target.installedOn, "."],
                                                  actor=player.installedOn, target=target.installedOn))
                if thp <= 0:
                    xp = target.experience / 2 + 1
                    player.gainExperience(xp) # I LOVE IT
                    targetIsDead = [target.installedOn, " is dead!", "\n"]
                    toBroadcast.append(events.Success(
                        actor=player.installedOn, target=target.installedOn,
                        actorMessage=["\n", targetIsDead, "You gain ", xp, " experience"],
                        targetMessage=["You are dead!"],
                        otherMessage=targetIsDead))
                    target.installedOn.destroy()
        for event in toBroadcast:
            event.broadcast()


class Say(NoTargetAction):
    expr = (((pyparsing.Literal("say") + pyparsing.White()) ^
             pyparsing.Literal("'")) +
            pyparsing.restOfLine.setResultsName("text"))

    def do(self, player, line, text):
        evt = events.Success(actor=player.installedOn,
                             actorMessage=["You say, '", text, "'"],
                             otherMessage=[player.installedOn, " says, '", text, "'"])
        evt.broadcast()

class Emote(NoTargetAction):
    expr = (((pyparsing.Literal("emote") + pyparsing.White()) ^
             pyparsing.Literal(":")) +
            pyparsing.restOfLine.setResultsName("text"))

    def do(self, player, line, text):
        evt = events.Success(actor=player.installedOn,
                             actorMessage=[player.installedOn, " ", text],
                             otherMessage=[player.installedOn, " ", text])
        evt.broadcast()

# class Rebuild(NoTargetAction):
#     expr = pyparsing.Literal("rebuild")

#     def do(self, player, line):
#         rebuilt = []
#         for k, v in sys.modules.items():
#             if k.startswith('pottery.') and v is not None:
#                 rebuilt.append(k)
#                 rebuild.rebuild(v)
#         ipottery.IActor(player).send("Rebuilt ", ', '.join(rebuilt), ".")

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
        for thing in player.installedOn.search(2, ipottery.IObject, name):
            player.send((thing.longFormatTo(player.installedOn), '\n'))

class Score(NoTargetAction):
    expr = pyparsing.Literal("score")

    def do(self, player, line):
        player.send(
            '/', '-' * 76, '\\', '\n',
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
            player.send(self.entry % {'playerName': p.formatTo(player.installedOn)} + '\n')
        player.send(self.footer % {'playerCount': len(connectedPlayers)} + '\n')

import pprint
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

        targetContainer = ipottery.IContainer(target, None)
        if targetContainer is not None:
            v['contents'] = list(targetContainer.getContents())

        exits = list(target.getExits())
        if exits:
            v['exits'] = exits
        s = pprint.pformat((target.__class__.__name__, v))
        player.send(s, '\n')

class Inventory(NoTargetAction):
    expr = pyparsing.Literal("inventory")

    def do(self, player, line):
        player.send(
            [T.fg.yellow, "Inventory:\n"],
            [T.fg.green, [(o, '\n') for o in ipottery.IContainer(player.installedOn).getContents()]])


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
