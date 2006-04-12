
# Twisted, the Framework of Your Internet
# Copyright (C) 2001 Matthew W. Lefkowitz
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of version 2.1 of the GNU Lesser General Public
# License as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

"""
Test cases for Reality.
"""

# use twisted-hack pyunit stuff to be picked up by runtests
from pyunit.unittest import TestCase

from reality import error
from reality import realities
from reality import thing
from reality import player
from reality import room
from reality import clothing

from reality.actions import NoTargetAction, TargetAction, ToolAction
from reality.phrase import registerSubparser, Subparser, Parsing, IParsing
from twisted.python.components import Interface, implements, Adapter



class SubparserBits(Subparser):
    def parse_foo(self, player, text):
        return 7


class PhraseParserTestCase(TestCase):
    def testBits(self):
        bits = SubparserBits().getParserBits()
        assert bits[0][0] == 'foo', bits[0]
        assert bits[0][1](None, None) == 7



import food, music
class Cake(thing.Thing):
    __implements__ = food.IEatTarget,
    eatenBy = None
    def actionTargetEat(self, action):
        self.eatenBy = action.actor

class RealityActionsTestCase(TestCase):
    def testSomeSimpleStuff(self):
        import music
        import explosives
        flute = music.Flute("flute")
        p = player.Player("bob")
        r = room.Room("where")
        p.location = r
        flute.location = p
        p.focus = r
        p.getComponent(IParsing).parse('blow flute')

    def testAutomatedParsing(self):
        flute = music.Flute("flute")
        p = player.Player("bob")
        r = room.Room("where")
        p.location = r
        flute.location = p
        p.focus = p
        poundCake = Cake("pound cake")
        chocolateCake = Cake("chocolate cake")
        poundCake.addSynonym("cake")
        chocolateCake.addSynonym("cake")
        p.getComponent(IParsing).parse("eat flute")
        assert chocolateCake.eatenBy == None
        assert poundCake.eatenBy == None
        


class ContainmentTestCase(TestCase):
    def setUp(self):
        r = self.reality = realities.Reality()
        self.ball = thing.Thing("ball", r)
        self.box = thing.Thing("box", r)
        self.table = thing.Thing("table", r)
        self.slab = thing.Thing("slab", r)
        self.bob = player.Player("bob", r)
        self.room = room.Room("room", r)
        self.area = room.Room("area", r)

    def tearDown(self):
        for x in 'ball', 'table', 'slab', 'bob', 'room':
            getattr(self, x).destroy()
            delattr(self, x)


    def testBasicContainment(self):
        self.ball.location = self.room
        assert self.room.find('ball') is self.ball
        assert self.ball.location is self.room,\
               "Ball was located " + str(self.ball.location)
        assert self.ball.place is self.room,\
               "Ball was placed " + str(self.ball.place)
        del self.ball.location
        try:
            self.room.find('ball')
        except error.CantFind: pass
        else:
            assert 0, "This should have failed!"
        assert self.ball.location is None, "location attribute didn't go None"
        assert self.ball.place is None, "place didn't go None"


    def testComponentContainment(self):
        self.ball.location = self.table
        self.ball.component = 1
        self.table.location = self.room
        assert self.ball.location is self.table
        assert self.ball.place is self.table
        assert self.table.find('ball') is self.ball
        self.failUnlessRaises(error.Failure, self.ball.move, destination=self.room, actor=self.bob)
        self.ball.component = 0
        self.ball.location = self.room
        assert self.room.find('ball') is self.ball
        try:
            self.table.find("ball")
        except:
            pass
        else:
            assert 0, "reference cruft left on 'table'."


    def testMultiContainment(self):
        self.table.grab(self.ball)
        self.room.grab(self.ball)
        assert self.room.find('ball') is self.ball
        assert self.table.find('ball') is self.ball
        assert self.ball.location is None
        self.table.toss(self.ball)
        self.room.toss(self.ball)
        self.ball.location = self.slab
        assert self.slab.find('ball') is self.ball
        for x in (self.room, self.table):
            self.failUnlessRaises(error.CantFind, x.find, 'ball')

    def testSurfaceContainment(self):
        self.table.surface = 1
        self.ball.location = self.table
        self.table.location = self.room
        assert self.ball.location is self.table,\
               "location is "+repr(self.ball.location)
        assert self.ball.place is self.room, (
            "place is "+repr(self.ball.place)+ ", locations is " +
            repr(self.ball.locations))
        del self.table.location
        del self.ball.location

        ## Mixing it up a little bit -- applying the surface bit at
        ## the end instead of the beginning.
        self.ball.location = self.table
        self.table.location = self.room
        self.table.surface = 1
        assert self.ball.location is self.table,\
               "location is "+repr(self.ball.location)
        assert self.ball.place is self.room,\
               "place is "+repr(self.ball.place)

        self.table.surface = 0

    def testMultiSurfaceContainment(self):
        ## adding yet more complexity -- 2 levels deep.
        self.table.location = self.room
        self.ball.location = self.slab
        self.slab.location = self.table
        self.slab.surface = 1
        self.table.surface = 1
        assert self.ball.location is self.slab,\
               "location is "+repr(self.ball.location)
        assert self.ball.place is self.room,\
               "place is "+repr(self.ball.place)
        assert self.room.find('ball') is self.ball,\
               "couldn't find ball"
        self.table.surface = 0
        try:
            self.room.find('ball')
            assert 0, "shouldn't be able to find ball."
        except error.CantFind:
            pass
        self.box.surface = 1
        self.ball.location = self.box
        self.box.location = self.slab

    def testPathologicalContainment(self):
        self.table.location = self.room
        self.box.location = self.table
        self.box.surface = 1
        self.table.surface = 1
        # since everything's made a surface and all events are propogated,
        # performance is factorial here, so this `large' number doesn't have to
        # be very large :)
        # in practice, this number should never be bigger than 4.
        largeNumber = 15
        things = []
        for i in range(largeNumber):
            thng = thing.Thing("thing"+str(i))
            thng.surface = 1
            things.append(thng)

        things[0].location = self.box

        for i in range(len(things)):
            thng = things[i]
            if i:
                thng.location = things[i-1]
        assert things[largeNumber-1] == self.room.find('thing' + str(largeNumber-1)),\
               "thing not found"

        for thng in things:
            thng.destroy()

class ClothingTestCase(TestCase):
    def testWearAndUnwear(self):
        p = player.Player("bob")
        parseMethod = p.getComponent(IParsing)._parseInternal
        p.focus = p
        t = clothing.Shirt("shirt")
        t.location = p
        parseMethod("wear shirt")
        # assert t.component
        wearer = p.getComponent(clothing.IWearActor)
        unwearer = p.getComponent(clothing.IUnwearActor)
        assert wearer is unwearer
        tt = t.getComponent(clothing.IWearTarget)
        for slot in tt.clothingSlots:
            self.failUnlessEqual(wearer.getClothing(slot),tt)
        parseMethod("remove shirt")
        for slot in tt.clothingSlots:
            self.failIfEqual(wearer.getClothing(slot),tt)

class TestIntel(player.Intelligence):
    """
    Add hooks here for debugging unit tests.
    """

    def seeName(self, name):
        pass
    def seeItem(self, thing,name):
        pass
    def dontSeeItem(self, thing):
        pass
    def seeNoItems(self):
        pass
    def seeExit(self, direction, exit):
        pass
    def dontSeeExit(self, direction):
        pass
    def seeNoExits(self):
        pass
    def seeDescription(self, key, description):
        pass
    def dontSeeDescription(self, key):
        pass
    def seeNoDescriptions(self):
        pass
    def seeEvent(self, string):
        # print repr(string)
        pass
    def request(self, question,default,c):
        cancel()
    def disconnect(self):
        pass
                        
class ContainerVerbsTestCase(TestCase):

    def reportHearing(self, *args):
        print args
    def setUp(self):
        self.bob = player.Player("bob")
        # self.bob.hears = self.reportHearing
        self.room = room.Room("the place")
        self.room2 = room.Room("the other place")
        self.room.connectExit("north", self.room2)
        self.bob.focus = self.room
        import container
        self.box = thing.Thing("box")
        self.box.addAdapter(container.OpenableContainer, 1)
        self.boxie = thing.Thing("boxie")
        self.boxie.addAdapter(container.OpenableContainer, 1)
        self.boxie.addAdapter(player.Portable, 1)
        self.foo = thing.Thing("foo")
        self.notfoo = thing.Thing("baz") 
        self.notfoo.addSynonym("foo")   # it looks like a foo 
        self.foo.addAdapter(player.Portable, 1)
        # but it isn't portable...
        self.bar = thing.Thing("bar")
        self.bar.location = self.bob
        self.bar.addAdapter(player.Portable, 1)
        self.parseMethod = self.bob.getComponent(IParsing)._parseInternal
        for o in self.bob, self.foo, self.notfoo, self.box, self.boxie:
            o.location = self.room
        self.bob.intelligence = TestIntel()

    def testWalkNorth(self):
        self.parseMethod("go north")
        assert self.bob.location is self.room2, str((self.bob.location, self.room2))
    def testPickItUp(self):
        self.parseMethod("take foo")
        assert self.foo.location is self.bob, str(self.foo.location)
    def testPutItDown(self):
        self.parseMethod("drop bar")
        assert self.bar.location is self.room, str(self.bar.location)
    def testPutItPutItPutItPutEtc(self):
        try:
            self.parseMethod("put box in box")
        except error.RealityException:
            pass
    def testPutItIn(self):
        self.parseMethod("put bar in boxie")
        self.parseMethod("put boxie in box")
        
    def tearDown(self):
        del self.bob.intelligence
        for o in self.bob, self.room, self.foo, self.bar:
            o.destroy()

from twisted.popsicle import mailsicle, freezer
import thingsicle

class PopsicleTestCase(TestCase):

    def testMailsicle(self):
        mst = mailsicle.Mailsicle("MAILSICLE_TEST")
        cvtc = ContainerVerbsTestCase("reportHearing")
        cvtc.setUp()
        freezer.register(cvtc.bob, mst)
        freezer.clean()
        cvtc.tearDown()
