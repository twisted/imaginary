
"""
Unit tests for Imaginary actions.
"""

from twisted.trial import unittest
from twisted.python import filepath

from imaginary import iimaginary, objects, events
from imaginary.action import Action, TargetAction, Help
from imaginary.test import commandutils
from imaginary.test.commandutils import E

# Regular expression for matching variable parts of the output of certain
# commands.
PTR = "[A-F0-9]{1,8}"
STOREID = "\\d+"

class TransactionalEventBroadcasterTestCase(unittest.TestCase):
    def testAddEvent(self):
        L = []
        teb = events.TransactionalEventBroadcaster()
        teb.addEvent(lambda: L.append('win'))
        teb.addRevertEvent(lambda: L.append('lose'))
        teb.broadcastEvents()
        self.assertEquals(L, ['win'])


    def testAddRevertEvent(self):
        L = []
        teb = events.TransactionalEventBroadcaster()
        teb.addEvent(lambda: L.append('lose'))
        teb.addRevertEvent(lambda: L.append('win'))
        teb.broadcastRevertEvents()
        self.assertEquals(L, ['win'])


    def testBadEvents(self):
        teb = events.TransactionalEventBroadcaster()
        self.assertRaises(ValueError, teb.addEvent, None)
        self.assertRaises(ValueError, teb.addRevertEvent, None)



class TargetActionTests(commandutils.CommandTestCaseMixin, unittest.TestCase):
    """
    Tests for general functionality provided by L{TargetAction} which is not
    specific to any particular action.
    """
    def test_resolveTarget(self):
        """
        L{TargetAction.resolve} finds things by name when passed a C{"target"}
        string.
        """
        self.assertEqual(
            TargetAction().resolve(self.player, "target", u"Observer Player"),
            [self.observer])


    def test_resolveTargetCaseInsensitively(self):
        """
        L{TargetAction.resolve} considers names case-insensitively when
        searching for things.
        """
        self.assertEqual(
            TargetAction().resolve(self.player, "target", u"observer player"),
            [self.observer])



class Actions(commandutils.CommandTestCaseMixin, unittest.TestCase):

    def testBadCommand(self):
        self._test(
            "jibber jabber",
            ["Bad command or filename"])

    def testInventory(self):
        # There ain't no stuff
        self._test(
            "inventory",
            ["Inventory:"])

        playerContainer = iimaginary.IContainer(self.player)

        # Give 'em something and make sure
        # they show up
        playerContainer.add(objects.Thing(store=self.store, name=u"foobar"))
        self._test(
            "inventory",
            ["Inventory:",
             "foobar"])

        # Give 'em a couple more things
        playerContainer.add(objects.Thing(store=self.store, name=u"barbaz"))
        playerContainer.add(objects.Thing(store=self.store, name=u"barbaz"))
        self._test(
            "inventory",
            ["Inventory:",
             "foobar",
             "barbaz",
             "barbaz"])

    def testActions(self):
        cmds = dict.fromkeys([
                getattr(cls, 'actionName', cls.__name__.lower())
                for cls
                in Action.actions]).keys()
        cmds.sort()
        self._test(
            "actions",
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
        o = objects.Thing(store=self.store, name=u"foo")
        iimaginary.IContainer(self.location).add(o)
        self._test(
            "get foo",
            ["You take a foo."],
            ["Test Player takes a foo."])
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

        c = objects.Thing(store=self.store, name=u"bar")
        cContainer = objects.Container.createFor(c, capacity=1)

        iimaginary.IContainer(self.location).add(c)
        o = objects.Thing(store=self.store, name=u"baz")
        cContainer.add(o)
        self._test(
            "get baz from bar",
            ["You take a baz from the bar."],
            ["Test Player takes a baz from the bar."])
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

        o = objects.Thing(store=self.store, name=u"bar")
        iimaginary.IContainer(self.player).add(o)
        self._test(
            "drop bar",
            ["You drop the bar."],
            ["Test Player drops a bar."])
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
             "Test Player is great.",
             "She is naked."])

        self._test(
            "look at me",
            [E("[ Test Player ]"),
             "Test Player is great.",
             "She is naked."])

        self._test(
            "look at Observer Player",
            [E("[ Observer Player ]"),
             "Observer Player is great.",
             "She is naked."],
            ["Test Player looks at you."])


        o = objects.Thing(store=self.store, name=u"foo")
        iimaginary.IContainer(self.location).add(o)
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
             "She is naked.",
             ""])

        self._test(
            "search me",
            [E("[ Test Player ]"),
             "Test Player is great.",
             "She is naked.",
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
             "She is naked.",
             ""])

        self._test(
            'search "Observer Player"',
            [E("[ Observer Player ]"),
             "Observer Player is great.",
             "She is naked.",
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
            ["Fooix changes Test Location's name to CRAP of CRAPness."])
        self.assertEquals(self.location.name,
                          "CRAP of CRAPness")


    def testRestore(self):
        self._test(
            "restore foobar",
            [E("Who's that?")])

        self._test(
            "restore here",
            ["Test Location cannot be restored."])

        actor = iimaginary.IActor(self.player)
        actor.hitpoints.decrease(25)
        actor.stamina.decrease(25)
        self._test(
            "restore self",
            ["You have fully restored yourself."])
        self.assertEquals(actor.hitpoints.current,
                          actor.hitpoints.max)
        self.assertEquals(actor.stamina.current,
                          actor.stamina.max)

        oactor = iimaginary.IActor(self.observer)
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
             ".*Level: +(\\d+) Experience: +(\\d+)",
             ".*Hitpoints: +(\\d+)/(\\d+)",
             ".*Stamina: +(\\d+)/(\\d+)",
             ".*"])
        self.assertEquals(x[0].groups(), ()) # Extra line for the command
        self.assertEquals(x[1].groups(), ())
        self.assertEquals(x[2].groups(), ('0', '0'))
        self.assertEquals(x[3].groups(), ('100', '100'))
        self.assertEquals(x[4].groups(), ('100', '100'))
        self.assertEquals(x[5].groups(), ())

        actor = iimaginary.IActor(self.player)
        actor.level = 3
        actor.experience = 63
        actor.hitpoints.current = 32
        actor.hitpoints.max = 74
        actor.stamina.current = 12
        actor.stamina.max = 39
        x, y = self._test(
            "score",
            [".*",
             ".*Level: +(\\d+) Experience: +(\\d+)",
             ".*Hitpoints: +(\\d+)/(\\d+)",
             ".*Stamina: +(\\d+)/(\\d+)",
             ".*"])
        self.assertEquals(x[0].groups(), ())
        self.assertEquals(x[1].groups(), ())
        self.assertEquals(x[2].groups(), ('3', '63'))
        self.assertEquals(x[3].groups(), ('32', '74'))
        self.assertEquals(x[4].groups(), ('12', '39'))
        self.assertEquals(x[5].groups(), ())


    def testDig(self):
        self._test(
            "dig west dark tunnel",
            ["You create an exit."],
            ["Test Player created an exit to the west."])
        room = iimaginary.IContainer(self.location).getExitNamed(u'west').toLocation
        self.assertEquals(room.name, u"dark tunnel")
        self.assertEquals(room.description, u'')
        self.assertIdentical(iimaginary.IContainer(room).getExitNamed(u'east').toLocation,
                             self.location)

        self._test(
            "dig east bright tunnel",
            ["You create an exit."],
            ["Test Player created an exit to the east."])
        room = iimaginary.IContainer(self.location).getExitNamed(u'east').toLocation
        self.assertEquals(room.name, u"bright tunnel")
        self.assertEquals(room.description, u'')
        self.assertIdentical(iimaginary.IContainer(room).getExitNamed(u'west').toLocation, self.location)

        self._test(
            "dig west boring tunnel",
            ["There is already an exit in that direction."])

    def testBury(self):
        self._test(
            "bury south",
            ["There isn't an exit in that direction."])
        self.assertEquals(list(iimaginary.IContainer(self.location).getExits()), [])

        room = objects.Thing(store=self.store, name=u"destination", proper=True)
        objects.Container.createFor(room, capacity=1000)
        objects.Exit.link(room, self.location, u'north')

        self._test(
            "bury south",
            ["It's gone."],
            ["Test Player destroyed the exit to destination."])

        self.assertEquals(
            list(iimaginary.IContainer(self.location).getExits()),
            [])

        self.assertEquals(
            list(iimaginary.IContainer(room).getExits()),
            [])

        objects.Exit.link(self.location, room, u'south')
        self.observer.moveTo(room)

        self._test(
            "bury south",
            ["It's gone."],
            ["The exit to Test Location crumbles and disappears."])
        self.assertEquals(
            list(iimaginary.IContainer(self.location).getExits()),
            [])
        self.assertEquals(
            list(iimaginary.IContainer(room).getExits()),
            [])


    def testGo(self):
        self._test(
            "go west",
            ["You can't go that way."])
        self._test(
            "west",
            ["You can't go that way."])

        room = objects.Thing(store=self.store, name=u"destination")
        objects.Container.createFor(room, capacity=1000)
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
             "Location for testing.",
             "Observer Player"],
            ["Test Player arrives from the west."])


    def testDirectionalMovement(self):
        # A couple tweaks to state to make the test simpler
        self.observer.location = None
        self.location.description = None

        oldRoom = self.location
        allDirections = ["northwest", "north", "northeast", "east",
                         "west", "southwest", "south", "southeast"]
        for d in allDirections[:len(allDirections) / 2]:
            room = objects.Thing(store=self.store, name=u"destination")
            objects.Container.createFor(room, capacity=1000)
            objects.Exit.link(oldRoom, room, unicode(d, 'ascii'))
            oldRoom = room

        for d, rd in zip(allDirections, reversed(allDirections)):
            self._test(
                d,
                [E("[ ") + ".*" + E(" ]"), # Not testing room description
                 E("( ") + ".*" + E(" )"), # Just do enough to make sure it was not an error.
                 ""])


    def test_scrutinize(self):
        """
        The scrutinize action takes a thing as a target and displays a lot of
        details about its internal state and construction.
        """
        self._test(
            "scrutinize me",
            [E("('Thing',"),
             E(" {'contents': [],"),
             E("  'description': u'',"),
             E("  'gender': 2,"),
             E("  'location': Thing(description=u'Location for testing.', "
               "gender=3, location=None, name=u'Test Location', portable=True, "
               "proper=True, weight=1, storeID=") + STOREID + E(")@0x") + PTR
               + E(","),
             E("  'name': u'Test Player',"),
             E("  'portable': True,"),
             E("  'proper': True,"),
             E("  'weight': 100})"),
             ])

        self._test(
            "scrutinize here",
            [E("('Thing',"),
             E(" {'contents': [Thing(description=u'', gender=2, location="
               "reference(") +
             STOREID + E("), name=u'Test Player', portable=True, proper="
                         "True, weight=100, storeID=") +
             STOREID + E(")@0x") + PTR + E(","),
             E("               Thing(description=u'', gender=2, location="
               "reference(") +
             STOREID + E("), name=u'Observer Player', portable=True, "
                         "proper=True, weight=100, storeID=") +
             STOREID + E(")@0x") + PTR + E("],"),
             E("  'description': u'Location for testing.',"),
             E("  'gender': 3,"),
             E("  'location': None,"),
             E("  'name': u'Test Location',"),
             E("  'portable': True,"),
             E("  'proper': True,"),
             E("  'weight': 1})")])


    def test_scrutinizeNonContainer(self):
        """
        The scrutinize action produces results for a thing which is not a
        container.
        """
        o = objects.Thing(store=self.store, name=u"foo")
        iimaginary.IContainer(self.location).add(o)
        self._test(
            "scrutinize foo",
            [E(u"('Thing',"),
             E(u" {'description': u'',"),
             E(u"  'gender': 3,"),
             E(u"  'location': Thing(description=u'Location for testing.', "
               "gender=3, location=None, name=u'Test Location', portable="
               "True, proper=True, weight=1, storeID=") +
             STOREID + E(")@0x") + PTR + E(","),
             E(u"  'name': u'foo',"),
             E(u"  'portable': True,"),
             E(u"  'proper': False,"),
             E(u"  'weight': 1})")])


    def testOpenClose(self):
        container = objects.Thing(store=self.store, name=u"container")
        objects.Container.createFor(container, capacity=1)
        iimaginary.IContainer(self.location).add(container)
        self._test(
            "close container",
            ["You close the container."],
            ["Test Player closes a container."])
        self._test(
            "close container",
            ["The container is already closed."],
            [])
        self._test(
            "open container",
            ["You open the container."],
            ["Test Player opens a container."])
        self._test(
            "open container",
            ["The container is already open."],
            [])



    def test_invalidHelp(self):
        """
        The help action tells the player that there is no help for topics for
        which there is no help.
        """
        self._test(
            # Hope you don't make a command with this name.
            "help abcxyz123",
            ["No help available on abcxyz123."],
            [])
        self._test(
            "help /etc/passwd",
            ["No help available on /etc/passwd."],
            [])


    def test_help(self):
        """
        The help action displays information from files in the resource
        directory.
        """
        resources = filepath.FilePath(__file__).parent().sibling("resources")
        self._test(
            "help help",
            resources.child("help").child("help").getContent().splitlines(),
            [])


    def test_helpMultiword(self):
        """
        The help action supports arguments with spaces in them.
        """
        fakeHelp = filepath.FilePath(self.mktemp())
        fakeHelp.makedirs()
        fakeHelp.child("foo bar").setContent("baz")
        original = Help.helpContentPath
        try:
            Help.helpContentPath = fakeHelp
            self._test("help foo bar", ["baz"], [])
        finally:
            Help.helpContentPath = original
