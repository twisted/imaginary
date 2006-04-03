
"""Unit tests for Pottery commands.
"""

import re, pprint

from twisted.trial import unittest
from twisted.test.proto_helpers import StringTransport

from pottery import objects, wiring, commands
from pottery.test import commandutils

E = re.escape

class Commands(commandutils.CommandTestCaseMixin, unittest.TestCase):

    def testBadCommand(self):
        self._test(
            "jibber jabber",
            ["Bad command or filename"])

    def testInventory(self):
        # There ain't no stuff
        self._test(
            "inventory",
            ["Inventory:"])

        # Give 'em something and make sure
        # they show up
        self.player.add(objects.Object("foobar"))
        self._test(
            "inventory",
            ["Inventory:",
             "foobar"])

        # Give 'em a couple more things
        self.player.add(objects.Object("barbaz"))
        self.player.add(objects.Object("barbaz"))
        self._test(
            "inventory",
            ["Inventory:",
             "foobar",
             "barbaz",
             "barbaz"])

    def testCommands(self):
        cmds = dict.fromkeys([
                getattr(cls, 'commandName', cls.__name__.lower())
                for cls
                in commands.Command.commands.values()]).keys()
        cmds.sort()
        self._test(
            "commands",
            [' '.join(cmds)])

    def testGet(self):
        # Try to get something that does not exist
        self._test(
            "get foobar",
            ["Nothing like that around here."])

        # Try to get yourself
        self._test(
            "get self",
            ["You cannot take Test Player."])
        self.assertEquals(self.player.location, self.location)

        # Try to get the location
        self._test(
            "get here",
            ["You cannot take Test Location."])
        self.assertEquals(self.location.location, None)

        # Make an object and try to get it
        o = objects.Object("foo")
        self.location.add(o)
        self._test(
            "get foo",
            ["You take foo."],
            ["Test Player takes foo."])
        self.assertEquals(o.location, self.player)

        # Try to get the observer
        self._test(
            "get 'Observer Player'",
            ["Observer Player is too heavy to pick up."],
            ["Test Player tries to pick you up, but fails."])
        self.assertEquals(self.observer.location, self.location)

        # Container stuff
        self._test(
            "get baz from bar",
            ["Nothing like that around here."])

        c = objects.Container("bar")
        self.location.add(c)
        o = objects.Object("baz")
        c.add(o)
        self._test(
            "get baz from bar",
            ["You take baz from bar."],
            ["Test Player takes baz from bar."])
        self.assertEquals(o.location, self.player)

        # Can't get things from a closed container
        o.moveTo(c)
        c.closed = True
        self._test(
            "get baz from bar",
            ["Nothing like that around here."],
            [])
        self.assertEquals(o.location, c)
        self.assertEquals(c.contents, [o])

    def testDrop(self):
        self._test(
            "drop foo",
            ["Nothing like that around here."])

        o = objects.Object("bar")
        self.player.add(o)
        self._test(
            "drop bar",
            ["You drop bar."],
            ["Test Player drops bar."])
        self.assertEquals(o.location, self.location)

    def testLook(self):
        self._test(
            "look",
            [E("[ Test Location ]"),
             E("(  )"),
             "Location for testing.",
             "Observer Player"])

        self._test(
            "look here",
            [E("[ Test Location ]"),
             E("(  )"),
             "Location for testing.",
             "Observer Player"])

        self._test(
            "look me",
            ["Test Player",
             "Test Player is great"])

        self._test(
            "look at me",
            ["Test Player",
             "Test Player is great"])

        self._test(
            "look at Observer Player",
            ["Observer Player",
             "Observer Player is great"],
            ["Test Player looks at you."])

        o = objects.Object("foo")
        self.location.add(o)
        self._test(
            "look at foo",
            ["foo"])

        self._test(
            "look at bar",
            ["You don't see that."])

    def testSay(self):
        self._test(
            "say hello",
            ["You say, 'hello'"],
            ["Test Player says, 'hello'"])

        self._test(
            "'hello",
            ["You say, 'hello'"],
            ["Test Player says, 'hello'"])

        self._test(
            "'hello world! quote -> '",
            ["You say, 'hello world! quote -> ''"],
            ["Test Player says, 'hello world! quote -> ''"])

    def testEmote(self):
        self._test(
            "emote jumps up and down",
            ["Test Player jumps up and down"],
            ["Test Player jumps up and down"])

        self._test(
            ":jumps up and down",
            ["Test Player jumps up and down"],
            ["Test Player jumps up and down"])

    def testSearch(self):
        self._test(
            "search self",
            ["Test Player",
             "Test Player is great.",
             ""])

        self._test(
            "search me",
            ["Test Player",
             "Test Player is great.",
             ""])

        self._test(
            "search here",
            [E("[ Test Location ]"),
             E("(  )"),
             "Location for testing.",
             "Observer Player",
             ""])

        self._test(
            "search 'Test Player'",
            ["Test Player",
             "Test Player is great.",
             ""])

        self._test(
            'search "Observer Player"',
            ["Observer Player",
             "Observer Player is great.",
             ""])

        self._test(
            "search blub",
            [""])

    def testDescribe(self):
        self._test(
            "describe me test description",
            ["You change Test Player's description."],
            ["Test Player changes Test Player's description."])
        self.assertEquals(self.player.description,
                          "test description")

        self._test(
            "describe here description test",
            ["You change Test Location's description."],
            ["Test Player changes Test Location's description."])
        self.assertEquals(self.location.description,
                          "description test")


    def testName(self):
        self._test(
            "name me fooix",
            ["You change Test Player's name."],
            ["Test Player changes Test Player's name to fooix."])
        self.assertEquals(self.player.name,
                          "fooix")

        self._test(
            "name here CRAP of CRAPness",
            ["You change Test Location's name."],
            ["fooix changes Test Location's name to CRAP of CRAPness."])
        self.assertEquals(self.location.name,
                          "CRAP of CRAPness")


    def testHit(self):
        self._test(
            "hit self",
            [E("Hit yourself?  Stupid.")])

        self._test(
            "hit foobar",
            ["Who's that?"])

        self.player.stamina.current = 0
        self._test(
            "hit Observer Player",
            ["You're too tired!"])

        self.player.stamina.current = self.player.stamina.max

        x, y = self._test(
            "hit Observer Player",
            ["You hit Observer Player for (\\d+) hitpoints."],
            ["Test Player hits you for (\\d+) hitpoints."])
        self.assertEquals(x[1].groups(), y[0].groups())

        self.player.stamina.current = self.player.stamina.max

        x, y = self._test(
            "attack Observer Player",
            ["You hit Observer Player for (\\d+) hitpoints."],
            ["Test Player hits you for (\\d+) hitpoints."])
        self.assertEquals(x[1].groups(), y[0].groups())


    def testRestore(self):
        self._test(
            "restore foobar",
            ["Who's that?"])

        self._test(
            "restore here",
            ["Test Location cannot be restored."])

        self.player.hitpoints.decrease(25)
        self.player.stamina.decrease(25)
        self._test(
            "restore self",
            ["You have fully restored yourself."])
        self.assertEquals(self.player.hitpoints.current,
                          self.player.hitpoints.max)
        self.assertEquals(self.player.stamina.current,
                          self.player.stamina.max)

        self.observer.hitpoints.decrease(25)
        self.observer.stamina.decrease(25)
        self._test(
            "restore Observer Player",
            ["You have restored Observer Player to full health."],
            ["Test Player has restored you to full health."])
        self.assertEquals(self.observer.hitpoints.current,
                          self.observer.hitpoints.max)
        self.assertEquals(self.observer.stamina.current,
                          self.observer.stamina.max)

    def testScore(self):
        # XXX This is kind of weak.  How can this test be improved?
        x, y = self._test(
            "score",
            [".*",
             ".*Level: (\\d+) Experience: (\\d+)",
             ".*Hitpoints: (\\d+)/(\\d+)",
             ".*Stamina: (\\d+)/(\\d+)",
             ".*"])
        self.assertEquals(x[0].groups(), ()) # Extra line for the command
        self.assertEquals(x[1].groups(), ())
        self.assertEquals(x[2].groups(), ('0', '0'))
        self.assertEquals(x[3].groups(), ('100', '100'))
        self.assertEquals(x[4].groups(), ('100', '100'))
        self.assertEquals(x[5].groups(), ())

        self.player.level = 3
        self.player.experience = 63
        self.player.hitpoints.current = 32
        self.player.hitpoints.max = 74
        self.player.stamina.current = 12
        self.player.stamina.max = 39
        x, y = self._test(
            "score",
            [".*",
             ".*Level: (\\d+) Experience: (\\d+)",
             ".*Hitpoints: (\\d+)/(\\d+)",
             ".*Stamina: (\\d+)/(\\d+)",
             ".*"])
        self.assertEquals(x[0].groups(), ())
        self.assertEquals(x[1].groups(), ())
        self.assertEquals(x[2].groups(), ('3', '63'))
        self.assertEquals(x[3].groups(), ('32', '74'))
        self.assertEquals(x[4].groups(), ('12', '39'))
        self.assertEquals(x[5].groups(), ())


    def testSpawn(self):
        self._test(
            "spawn foobar",
            ["foobar created."],
            ["Test Player creates foobar."])
        foobar = self.player.find("foobar")
        self.assertEquals(foobar.name, "foobar")
        self.assertEquals(foobar.description, "an undescribed monster")
        self.assertEquals(foobar.location, self.location)

        self._test(
            'spawn "bar foo"',
            ["bar foo created."],
            ["Test Player creates bar foo."])
        barfoo = self.player.find("bar foo")
        self.assertEquals(barfoo.name, "bar foo")
        self.assertEquals(barfoo.description, "an undescribed monster")
        self.assertEquals(barfoo.location, self.location)

        self._test(
            'spawn "described monster" It looks like a monster with a description.',
            ["described monster created."],
            ["Test Player creates described monster."])
        monster = self.player.find("described monster")
        self.assertEquals(monster.name, "described monster")
        self.assertEquals(monster.description, "It looks like a monster with a description.")
        self.assertEquals(monster.location, self.location)

        # XXX Some automatic cleanup maybe?
        for m in foobar, barfoo, monster:
            m.destroy()

    def testDig(self):
        self._test(
            "dig west dark tunnel",
            ["You create an exit."],
            ["Test Player created an exit to the west."])
        room = self.location.exits['west']
        self.assertEquals(room.name, "dark tunnel")
        self.assertEquals(room.description, '')
        self.assertIdentical(room.exits['east'], self.location)

        self._test(
            "dig east bright tunnel",
            ["You create an exit."],
            ["Test Player created an exit to the east."])
        room = self.location.exits['east']
        self.assertEquals(room.name, "bright tunnel")
        self.assertEquals(room.description, '')
        self.assertIdentical(room.exits['west'], self.location)

        self._test(
            "dig west boring tunnel",
            ["There is already an exit in that direction."])

    def testBury(self):
        self._test(
            "bury south",
            ["There isn't an exit in that direction."])
        self.assertEquals(self.location.exits, {})

        room = objects.Room("destination")
        room.exits['north'] = self.location
        self.location.exits['south'] = room

        self._test(
            "bury south",
            ["It's gone."],
            ["Test Player destroyed the exit to the south."])
        self.assertEquals(self.location.exits, {})
        self.assertEquals(room.exits, {})

        self.location.exits['south'] = room
        room.exits['north'] = self.location
        self.observer.moveTo(room)

        self._test(
            "bury south",
            ["It's gone."],
            ["The exit to the north crumbles and disappears."])


    def testGo(self):
        self._test(
            "go west",
            ["You can't go that way."])
        self._test(
            "west",
            ["You can't go that way."])

        room = objects.Room("destination")
        self.location.exits["west"] = room
        room.exits["east"] = self.location

        self._test(
            "west",
            [E("[ destination ]"),
             E("( east )"),
             ""],
            ["Test Player leaves west."])

        self._test(
            "north",
            ["You can't go that way."])
        self._test(
            "go east",
            [E("[ Test Location ]"),
             E("( west )"),
             "Location for testing",
             "Observer Player"],
            ["Test Player arrives from the west."])

    def testScrutinize(self):
        ptr = "0x[0123456789abcdefABCDEF]{8}"
        self._test(
            "scrutinize me",
            [E("('Player',"),
             E(" {'_heartbeatCall': <twisted.internet.base.DelayedCall instance at ") + ptr + E(">,"),
             E("  'contents': [],"),
             E("  'description': '',"),
             E("  'hitpoints': pottery.objects.Points(100, 100),"),
             E("  'location': Room(name='Test Location', location=None),"),
             E("  'name': 'Test Player',"),
             E("  'proto': <pottery.test.commandutils.Protocol instance at ") + ptr + E(">,"),
             E("  'stamina': pottery.objects.Points(100, 100),"),
             E("  'strength': pottery.objects.Points(100, 100),"),
             E("  'termAttrs': AttributeSet(bold=False, underline=False, reverseVideo=False, blink=False, fg=9, bg=9),"),
             E("  'useColors': False})")])

        self._test(
            "scrutinize here",
            [E("('Room',"),
             E(" {'contents': [Player(name='Test Player', location=Room(name='Test Location', location=None)),"),
             E("               Player(name='Observer Player', location=Room(name='Test Location', location=None))],"),
             E("  'description': 'Location for testing.',"),
             E("  'exits': {},"),
             E("  'name': 'Test Location'})")])



    def testOpenClose(self):
        container = objects.Container("container")
        self.location.add(container)
        self._test(
            "close container",
            ["You close container."],
            ["Test Player closes container."])
        self._test(
            "close container",
            ["container is already closed."],
            [])
        self._test(
            "open container",
            ["You open container."],
            ["Test Player opens container."])
        self._test(
            "open container",
            ["container is already open."],
            [])
