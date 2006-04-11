
"""Unit tests for Pottery commands.
"""

from twisted.trial import unittest

from pottery import ipottery, objects, commands
from pottery.test import commandutils
from pottery.test.commandutils import E

PTR = "[A-F0-9]{1,8}"

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

        playerContainer = ipottery.IContainer(self.player)

        # Give 'em something and make sure
        # they show up
        playerContainer.add(objects.Object(store=self.store, name=u"foobar"))
        self._test(
            "inventory",
            ["Inventory:",
             "foobar"])

        # Give 'em a couple more things
        playerContainer.add(objects.Object(store=self.store, name=u"barbaz"))
        playerContainer.add(objects.Object(store=self.store, name=u"barbaz"))
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
        o = objects.Object(store=self.store, name=u"foo")
        ipottery.IContainer(self.location).add(o)
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

        c = objects.Object(store=self.store, name=u"bar")
        cContainer = objects.Container(store=self.store, capacity=1)
        cContainer.installOn(c)

        ipottery.IContainer(self.location).add(c)
        o = objects.Object(store=self.store, name=u"baz")
        cContainer.add(o)
        self._test(
            "get baz from bar",
            ["You take baz from bar."],
            ["Test Player takes baz from bar."])
        self.assertEquals(o.location, self.player)

        # Can't get things from a closed container
        o.moveTo(c)
        cContainer.closed = True
        self._test(
            "get baz from bar",
            ["Nothing like that around here."],
            [])
        self.assertEquals(o.location, c)
        self.assertEquals(list(cContainer.getContents()), [o])

    def testDrop(self):
        self._test(
            "drop foo",
            ["Nothing like that around here."])

        o = objects.Object(store=self.store, name=u"bar")
        ipottery.IContainer(self.player).add(o)
        self._test(
            "drop bar",
            ["You drop bar."],
            ["Test Player drops bar."])
        self.assertEquals(o.location, self.location)

    def testLook(self):
        self._test(
            "look",
            [E("[ Test Location ]"),
             "Location for testing.",
             "Observer Player"])

        self._test(
            "look here",
            [E("[ Test Location ]"),
             "Location for testing.",
             "Observer Player"])

        objects.Exit.link(self.location, self.location, u"north")
        self._test(
            "look here",
            [E("[ Test Location ]"),
             E("( north south )"),
             "Location for testing.",
             "Observer Player"])

        self._test(
            "look me",
            [E("[ Test Player ]"),
             "Test Player is great"])

        self._test(
            "look at me",
            [E("[ Test Player ]"),
             "Test Player is great"])

        self._test(
            "look at Observer Player",
            [E("[ Observer Player ]"),
             "Observer Player is great"],
            ["Test Player looks at you."])


        o = objects.Object(store=self.store, name=u"foo")
        ipottery.IContainer(self.location).add(o)
        self._test(
            "look at foo",
            [E("[ foo ]")])

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
            [E("[ Test Player ]"),
             "Test Player is great.",
             ""])

        self._test(
            "search me",
            [E("[ Test Player ]"),
             "Test Player is great.",
             ""])

        self._test(
            "search here",
            [E("[ Test Location ]"),
             "Location for testing.",
             "Observer Player",
             ""])

        self._test(
            "search 'Test Player'",
            [E("[ Test Player ]"),
             "Test Player is great.",
             ""])

        self._test(
            'search "Observer Player"',
            [E("[ Observer Player ]"),
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


    def testRestore(self):
        self._test(
            "restore foobar",
            ["Who's that?"])

        self._test(
            "restore here",
            ["Test Location cannot be restored."])

        actor = ipottery.IActor(self.player)
        actor.hitpoints.decrease(25)
        actor.stamina.decrease(25)
        self._test(
            "restore self",
            ["You have fully restored yourself."])
        self.assertEquals(actor.hitpoints.current,
                          actor.hitpoints.max)
        self.assertEquals(actor.stamina.current,
                          actor.stamina.max)

        oactor = ipottery.IActor(self.observer)
        oactor.hitpoints.decrease(25)
        oactor.stamina.decrease(25)
        self._test(
            "restore Observer Player",
            ["You have restored Observer Player to full health."],
            ["Test Player has restored you to full health."])
        self.assertEquals(oactor.hitpoints.current,
                          oactor.hitpoints.max)
        self.assertEquals(oactor.stamina.current,
                          oactor.stamina.max)

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

        actor = ipottery.IActor(self.player)
        actor.level = 3
        actor.experience = 63
        actor.hitpoints.current = 32
        actor.hitpoints.max = 74
        actor.stamina.current = 12
        actor.stamina.max = 39
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
        room = self.location.getExitNamed(u'west').toLocation
        self.assertEquals(room.name, u"dark tunnel")
        self.assertEquals(room.description, u'')
        self.assertIdentical(room.getExitNamed(u'east').toLocation,
                             self.location)

        self._test(
            "dig east bright tunnel",
            ["You create an exit."],
            ["Test Player created an exit to the east."])
        room = self.location.getExitNamed(u'east').toLocation
        self.assertEquals(room.name, u"bright tunnel")
        self.assertEquals(room.description, u'')
        self.assertIdentical(room.getExitNamed(u'west').toLocation, self.location)

        self._test(
            "dig west boring tunnel",
            ["There is already an exit in that direction."])

    def testBury(self):
        self._test(
            "bury south",
            ["There isn't an exit in that direction."])
        self.assertEquals(list(self.location.getExits()), [])

        room = objects.Object(store=self.store, name=u"destination")
        objects.Container(store=self.store, capacity=1000).installOn(room)
        objects.Exit.link(room, self.location, u'north')

        self._test(
            "bury south",
            ["It's gone."],
            ["Test Player destroyed the exit to destination."])
        self.assertEquals(list(self.location.getExits()), [])
        self.assertEquals(list(room.getExits()), [])

        objects.Exit.link(self.location, room, u'south')
        self.observer.moveTo(room)

        self._test(
            "bury south",
            ["It's gone."],
            # XXX - This is wrong, but I cannot fix it now.  "The" should be
            # capitalized.
            ["the exit to Test Location crumbles and disappears."])
        self.assertEquals(list(self.location.getExits()), [])
        self.assertEquals(list(room.getExits()), [])


    def testGo(self):
        self._test(
            "go west",
            ["You can't go that way."])
        self._test(
            "west",
            ["You can't go that way."])

        room = objects.Object(store=self.store, name=u"destination")
        objects.Container(store=self.store, capacity=1000).installOn(room)
        objects.Exit.link(self.location, room, u"west")

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
        STOREID = "\\d+"
        self._test(
            "scrutinize me",
            [E("('Object',"),
             E(" {'contents': [],"),
             E("  'description': u'',"),
             E("  'location': Object(description=u'Location for testing.', "
               "location=None, name=u'Test Location', portable=True, weight=1, "
               "storeID=1)@0x") + "[A-F0-9]{1,8}" + E(","),
             E("  'name': u'Test Player',"),
             E("  'portable': True,"),
             E("  'weight': 100})"),
             ])

        self._test(
            "scrutinize here",
            [E("('Object',"),
             E(" {'contents': [Object(description=u'', location=reference(") + STOREID + E("), name=u'Test Player', portable=True, weight=100, storeID=6)@0x") + PTR + E(","),
             E("               Object(description=u'', location=reference(") + STOREID + E("), name=u'Observer Player', portable=True, weight=100, storeID=18)@0x") + PTR + E("],"),
             E("  'description': u'Location for testing.',"),
             E("  'location': None,"),
             E("  'name': u'Test Location',"),
             E("  'portable': True,"),
             E("  'weight': 1})")])



    def testOpenClose(self):
        container = objects.Object(store=self.store, name=u"container")
        objects.Container(store=self.store, capacity=1).installOn(container)
        ipottery.IContainer(self.location).add(container)
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
