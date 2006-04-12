from __future__ import nested_scopes

import time

from reality import chronology
# gotta do this here! because the test runner will find
# a delayed call after the first test is run.
chronology.timer.dcall.cancel()

# and not only that, but we're importing it before the other reality
# stuff so we force the other reality stuff to use *our* timer, not
# the automatically instantiated singleton.

chronology.timer = timer = chronology.FakeTimer(test=True)

from twisted.internet import reactor
from twisted.trial import unittest
from twisted.python import components

from reality import errors, things, ambulation, conveyance, emporium, harm, acoustics, conflagration, pyrotechnics, observation
from reality.text import english
from reality.text.common import express

from os.path import join as opj
from quotient import storq



class TestEventReceiver(components.Adapter):
    __implements__ = things.IEventReceiver

    def eventReceived(self, emitter, event):
        self.original.done = 1

class ITestInterface(components.Interface):
    "internet"

ambulation.Exit.classForwardInterface(ITestInterface)

class TestComponent(components.Adapter):
    __implements__ = ITestInterface

class Hello:
    pass

class ImplementorQueryTestCase(unittest.TestCase):
    def setUp(self):
        d = self.mktemp()
        self.store = storq.Store(opj(d, "db"), opj(d, "files"))            

    def tearDown(self):
        self.store.close()
        
    def testSimpleEvent(self):
        s = self.store
        t = s.transact(things.Thing, s, "t")
        bob = s.transact(things.Actor, s, "bob")
        t2 = s.transact(things.Movable, s, "t2")
        s.transact(bob.moveTo, t)
        s.transact(t2.moveTo, t)
        t2.addAdapter(TestEventReceiver, 1)
        t2.done = 0
        bob.emitEvent(Hello())
        self.failUnless(t2.done)

    def testLookFor(self):
        s = self.store
        l = s.transact(things.Thing, s, "z")
        x = s.transact(things.Thing, s, "x")
        y = s.transact(things.Thing, s, "y")
        for t in x, y:
            t.addAdapter(TestComponent, 1)
        bob = s.transact(things.Actor, s, "bob")
        s.transact(bob.moveTo, l)
        s.transact(l.link, x)
        s.transact(l.link, y)
        self.failUnlessEqual( things.IInterfaceForwarder(bob).lookFor("x", ITestInterface, 3),
                              [x.getComponent(ITestInterface)])

    def testExitPropogation(self):
        s = self.store
        a = s.transact(ambulation.Room, s, "A")
        b = s.transact(ambulation.Room, s, "B")
        c = s.transact(ambulation.Room, s, "C")
        e = s.transact(ambulation.Door, s, "door", "east", a, c)
        bob = s.transact(things.Actor, s, "bob")
        sword = s.transact(things.Movable, s, "sword")
        sword.addAdapter(TestComponent, 1)
        sword.addAdapter(conveyance.Portable, 1)
        s.transact(sword.moveTo, c)
        s.transact(bob.moveTo, a)
        pars = english.Parsing(bob).parse
        l = things.IInterfaceForwarder(bob).lookFor("sword", ITestInterface, 3)
        assert l[0] is sword.getComponent(ITestInterface)
        self.assertRaises(errors.ActionRefused, pars, "get sword")
        pars("go east")
        assert bob.location.getItem() == c
        l = things.IInterfaceForwarder(bob).lookFor("sword", ITestInterface)
        pars("take sword")
        assert sword.location.getItem() == bob
        assert l[0] is sword.getComponent(ITestInterface)
        pars("go west")
        assert bob.location.getItem() == a
        pars("drop sword")
        assert sword.location.getItem() == a

    def testSuperBasicPortables(self):
        def _():
            a = things.Movable(self.store, "a")
            b = things.Movable(self.store, "b")
            c = things.Movable(self.store, "c")
            a.moveTo(b)
            self.assertEquals(a.location.getItem(), b)
            a.moveTo(c)
            self.assertEquals(a.location.getItem(), c)
        self.store.transact(_)

    def testBasicPortables(self):
        s = self.store
        foo1 = s.transact(things.Movable, s, "foo")
        foo2 = s.transact(things.Movable, s, "foo")
        foo2.addAdapter(conveyance.Portable, 1)
        r = s.transact(ambulation.Room, s, "R")
        bob = s.transact(things.Actor, s, "bob")
        s.transact(foo1.moveTo, r)
        s.transact(foo2.moveTo, r)
        s.transact(bob.moveTo, r)
        pars = english.Parsing(bob).parse
        pars("take foo")
        assert foo2.location.getItem() == bob
        pars("drop foo")
        assert foo2.location.getItem() == r

    def testBasicWearables(self):
        from reality import raiment
        s = self.store
        foo = s.transact(things.Movable, s, "fedora")
        foo.addAdapter(raiment.Wearable,1).setStyle("hat")
        bob = s.transact(things.Actor, s, "bob")
        r = s.transact(ambulation.Room, s, "R")
        s.transact(foo.moveTo, r)
        s.transact(bob.moveTo, r)
        pars = english.Parsing(bob).parse
        pars("wear fedora")
        assert raiment.IWearTarget(foo).wearer.original is bob
        assert raiment.IWearActor(bob).clothing['crown'][-1].original is foo
        pars("remove fedora")
        assert raiment.IWearTarget(foo).wearer is None

    def testBasicMovement(self):
        s = self.store
        a = s.transact(things.Movable, s, 'a')
        b = s.transact(things.Movable, s, 'b')
        class L:
            __implements__ = things.IMoveListener
            def __init__(self):
                self.arrives = []
                self.leaves = []
                self.moves = []

            def thingArrived(self, emitter, event):
                self.arrives.append((emitter, event))
            
            def thingLeft(self, emitter, event):
                self.leaves.append((emitter, event))
            
            def thingMoved(self, emitter, event):
                self.moves.append((emitter, event))

        r = s.transact(ambulation.Room, s, "r")
        s.transact(a.moveTo, r)
        s.transact(b.moveTo, r)
        l = L()
        b.addComponent(l, 1)
        r2 = s.transact(ambulation.Room, s, "r2")
        s.transact(a.moveTo, r2)
        assert l.leaves[0][0] == a, l.leaves[0][0]
        s.transact(a.moveTo, r)
        assert l.arrives[0][0] == a, l.arrives[0][0]
        s.transact(a.moveTo, r)
        assert l.moves[0][0] == a, l.moves[0][0]
        assert len(l.moves) == len(l.arrives) == len(l.leaves) == 1, str(
            (l.moves, l.arrives, l.leaves))

    def testWarpgateMovement(self):
        ## XXX TODO
        
        ### 'go in' is not how we want to spell this (though that
        ### spelling _should_ continue to work), really it's 'enter
        ### gate'.  however, there is no 'exitKnownAs' function to
        ### override, and it's not entirely clear what the best way to
        ### architect that is (knownAs is a bit of a hack anyway - we
        ### probably don't want X different versions of it, since it
        ### should be indexed most of the time)
        
        from reality import translocation
        s = self.store
        w1 = s.transact(translocation.Warpgate, s, "gate")
        w2 = w1.otherEnd.getItem()
        r1 = s.transact(ambulation.Room, s, "Metal Room")
        r2 = s.transact(ambulation.Room, s, "Plastic Room")
        bob = s.transact(things.Actor, s, "bob")
        s.transact(bob.moveTo, r1)
        s.transact(w1.moveTo, r1)
        s.transact(w2.moveTo, r2)
        pars = english.Parsing(bob).parse
        pars("go in")
        self.failUnlessEqual(bob.location, w2.location)
        self.failUnless(bob.location.getItem(), r2)
        pars("go in")
        self.failUnlessEqual(bob.location, w1.location)
        self.failUnless(bob.location.getItem(), r1)
        

from reality import actions, ambulation
from reality.text import common, english

class ISwingDanceActor(components.Interface): pass
class IAttackActor(components.Interface): pass
class ISwingDanceTarget(components.Interface): pass
class IAttackTarget(components.Interface): pass

class NullAdapter(components.Adapter):
    __implements__ = ISwingDanceActor, IAttackActor, ISwingDanceTarget, IAttackTarget

class SwingDance(actions.TargetAction):
    def doAction(self):
        things.IThing(self.actor).swung = True
        "You dance wildly!"

# This should _really_ be a ToolAction with a possibly implicit target...
class Attack(actions.TargetAction): 
    def doAction(self):
        things.IThing(self.actor).attacked = True
        "You swing wildly!"

components.registerAdapter(NullAdapter, things.Actor, ISwingDanceActor)
components.registerAdapter(NullAdapter, things.Actor, IAttackActor)


class SubparserBits(english.Subparser):
    def parse_foo(self, player, text):
        return 7

    def parse_swing(self, player, text):
        return [SwingDance(player, text), Attack(player, text)]

english.registerSubparser(SubparserBits())

class ColoredSword(things.Movable):
    def __init__(self, store, color):
        self.name = color + " sword"
        things.Movable.__init__(self, store, self.name)

    def knownAs(self, name, observer):
        return self.name.count(name)

components.registerAdapter(NullAdapter, ColoredSword, ISwingDanceTarget)
components.registerAdapter(NullAdapter, ColoredSword, IAttackTarget)

class PhraseParserTestCase(unittest.TestCase):
    def setUp(self):
        d = self.mktemp()
        self.store = storq.Store(opj(d, "db"), opj(d, "files"))            

    def tearDown(self):
        self.store.close()

    def testBits(self):
        bits = SubparserBits().getParserBits()
        d = dict(bits)
        assert 'foo' in d
        assert d['foo'](None, None) == 7

    def testAmbiguity(self):
        s = self.store
        bob = s.transact(things.Actor, s, "Bob")
        red = s.transact(ColoredSword, s, "Red")
        #blue = s.transact(ColoredSword, s, "Blue")

        room = s.transact(ambulation.Room, s, "Room!")
        for x in bob, red:#, blue:
            s.transact(x.moveTo, room)

        p = common.IThinker(bob)
        p.parse("swing sword")
        self.assertEquals(len(p.potentialActions), 2)
        p.parse("1")
        p.parse("swing sword")
        self.assertEquals(len(p.potentialActions), 2)
        p.parse("2")
        assert bob.swung
        assert bob.attacked

class FormatterTestCase(unittest.TestCase):
    def setUp(self):
        d = self.mktemp()
        self.store = storq.Store(opj(d, "db"), opj(d, "files"))            

    def tearDown(self):
        self.store.close()

    def testExpressUtil(self):
        s = self.store
        self.failUnlessEqual(express(("1", "2", "3"), None),
                             "123")
        self.failUnless(express(errors.Nonsense(), None))
        self.failUnless(express(s.transact(things.Thing, s, "bob"), None))

    def testNounDescription(self):
        s = self.store
        bob = s.transact(things.Actor, s, 'bob')
        obj = s.transact(things.Movable, s, 'hey')
        c = obj.addAdapter(conveyance.Portable, 1)
        desc = common.IDescribeable(obj)
        desc.describe(c, "hello", 1)
        self.assertEquals(desc.explainTo(bob), "hello")

class ECommerceTestCase(unittest.TestCase):
    def setUp(self):
        d = self.mktemp()
        self.store = storq.Store(opj(d, "db"), opj(d, "files"))            

    def tearDown(self):
        self.store.close()

    def testBuy(self):
        s = self.store
        shop = s.transact(ambulation.Room, s, "Shop")
        shopkeeper = s.transact(things.Actor, s, "Asidonhopo")
        bob = s.transact(things.Actor, s, "bob")
        bauble = s.transact(things.Movable, s, "bauble")
        [s.transact(t.moveTo, shop) for t in (shopkeeper, bob, bauble)]
        
        customer = bob.addAdapter(emporium.Customer,  1)
        vendor = shopkeeper.addAdapter(emporium.Vendor, 1)
        bauble.addAdapter(conveyance.Portable, 1)
        
        vendor.stock(bauble, 100)

        assert bauble.getComponent(emporium.IMerchandise)
        vendor.balance = 0
        customer.balance = 100
        pars = english.Parsing(bob).parse
        pars("get bauble")
        pars("buy bauble")
        vendor.balance == 100
        assert customer.balance == 0
        assert bauble.getComponent(emporium.IMerchandise) == None

    def testDoorSecurity(self):
        s = self.store
        shop = s.transact(ambulation.Room, s, "Shop")
        room = s.transact(ambulation.Room, s, "Non-Shop")
        exit = s.transact(emporium.ShopDoor, s, "Security Door", "north", shop, room)
        exit.addAdapter(ambulation.OpenDoor, 1)
        shopkeeper = s.transact(things.Actor, s, "Asidonhopo")
        bob = s.transact(things.Actor, s, "bob")
        bauble = s.transact(things.Movable, s, "bauble")
        [s.transact(t.moveTo, shop) for t in (shopkeeper, bob, bauble)]

        
        customer = bob.addAdapter(emporium.Customer, 1)
        vendor = shopkeeper.addAdapter(emporium.Vendor, 1)
        bauble.addAdapter(conveyance.Portable, 1)
        
        vendor.stock(bauble, 100)
        pars = english.Parsing(bob).parse
        pars("go north")
        assert bob.location.getItem() == room
        pars("go south")
        assert bob.location.getItem() == shop
        pars("get bauble")
        self.assertEquals(bauble.location.getItem(), bob)
        self.failUnlessRaises(errors.ActionRefused,pars, "go north")

    def testObjectSecurity(self):
        s = self.store
        shop = s.transact(ambulation.Room, s, "Shop")
        room = s.transact(ambulation.Room, s, "Non-Shop")
        exit = s.transact(ambulation.Door, s, "Secret Trapdoor", "north", shop, room)
        exit.addAdapter(ambulation.OpenDoor, 1)
        shopkeeper = s.transact(things.Actor, s, "Asidonhopo")
        bob = s.transact(things.Actor, s, "bob")
        bauble = s.transact(things.Movable, s, "bauble")
        bauble.addAdapter(conveyance.Portable, 1)
        [s.transact(t.moveTo, shop) for t in (shopkeeper, bob, bauble)]
        
        customer = bob.addAdapter(emporium.Customer, 1)
        vendor = shopkeeper.addAdapter(emporium.Vendor, 1)
        bauble.addAdapter(conveyance.Portable, 1)
        
        vendor.stock(bauble, 100)
        pars = english.Parsing(bob).parse
        pars("get bauble")
        pars("go north")
        assert bauble.location.getItem() == shop

class CombatTestCase(unittest.TestCase):

    def setUp(self):
        d = self.mktemp()
        s = self.store = storq.Store(opj(d, "db"), opj(d, "files"))            
        room = s.transact(ambulation.Room, s, "Room")
        bob = s.transact(things.Actor, s, "bob")
        rodney = s.transact(things.Actor, s, "rodney")
        sword = s.transact(things.Movable, s, "sword")
        sword.addAdapter(harm.Weapon, 1)
        armor = s.transact(things.Movable, s, "chainmail")
        armor.addAdapter(harm.Armor,1)
        s.transact(bob.moveTo, room)
        s.transact(rodney.moveTo, room)
        s.transact(sword.moveTo, bob)
        s.transact(armor.moveTo, rodney)
        self.bob = bob
        self.rodney = rodney
        
    def tearDown(self):
        self.store.close()

    def testSimpleDamage(self):
        english.Parsing(self.bob).parse("hit rodney with sword")

    def testArmoredDamage(self):
        english.Parsing(self.rodney).parse("wear chainmail")
        english.Parsing(self.bob).parse("hit rodney with sword")
        
class AnotherTestCase(unittest.TestCase):
    def setUp(self):
        d = self.mktemp()
        self.store = storq.Store(opj(d, "db"), opj(d, "files"))            

    def tearDown(self):
        self.store.close()

    def testMusic(self):
        s = self.store
        room = s.transact(ambulation.Room, s, "Room")
        bob = s.transact(things.Actor, s, "bob")
        whistle = s.transact(things.Movable, s, "whistle")
        whistle.addAdapter(acoustics.Whistle, True)
        s.transact(bob.moveTo, room)
        s.transact(whistle.moveTo, room)
        english.Parsing(bob).parse("blow whistle")
        
    def testCandle(self):
        s = self.store
        room = s.transact(ambulation.Room, s, "Room")
        bob = s.transact(things.Actor, s, "bob")
        candle = s.transact(things.Movable, s, "candle")
        candle.addAdapter(conflagration.Candle, True).light()
        s.transact(candle.moveTo, room)
        s.transact(bob.moveTo, room)
        english.Parsing(bob).parse("blow candle")
        
    def testRocket(self):
        s = self.store
        room = s.transact(ambulation.Room, s, "Room")
        room2 = s.transact(ambulation.Room, s, "Room 2")
        door = s.transact(ambulation.Door, s, "door","north",room,room2)
        door.addAdapter(harm.DamageableDoor, True)
        bob = s.transact(things.Actor, s, "bob")
        rocket = s.transact(things.Movable, s, "rocket")
        rocket.addAdapter(pyrotechnics.Rocket, True)
        s.transact(bob.moveTo, room)
        s.transact(rocket.moveTo, room)
        #Since we didn't implement "open" yet...        
        english.Parsing(bob).parse("blow door with rocket")
        english.Parsing(bob).parse("go north")



#divunal stuffs
from reality import charge

class ChargeTestCase(unittest.TestCase):
    def setUp(self):
        d = self.mktemp()
        self.store = storq.Store(opj(d, "db"), opj(d, "files"))            

    def tearDown(self):
        self.store.close()

    def testSockets(self):
        s = self.store
        bob = s.transact(things.Actor, s, "bob")
        bob.addAdapter(charge.Battery, ignoreClass=True) #his finger!
        batt = charge.IChargeSource(bob)
        radio = s.transact(things.Thing, s, "Radio")
        radio.addAdapter(charge.Radio, ignoreClass=True)
        sink = charge.IChargeSink(radio)
        batt.sinkTo(radio)
        self.failUnlessRaises(charge.AlreadyConnected, batt.sinkTo, radio)

        batt.unsink(radio)
        self.assertEqual(bool(batt.sink), False)

    def testChargeTransfer(self):
        s = self.store
        batt = s.transact(things.Thing, s, "battery")
        charger = s.transact(things.Thing, s, "charger")
        radio = s.transact(things.Thing, s, "radio")

        batt.addAdapter(charge.Battery, ignoreClass=True)
        charger.addAdapter(charge.BatteryCharger, ignoreClass=True)
        radio.addAdapter(charge.Radio, ignoreClass=True)
       
        b = charge.IChargeSink(batt)
        bsource = charge.IChargeSource(batt)
        r = charge.IChargeSink(radio)
        c = charge.IChargeSource(charger)

        bsource.updateCharge(newCharge=0) # simulate running out of charge
        self.failUnlessRaises(charge.NotEnoughCharge, bsource.sinkTo, r)
        bsource.unsink(r)

        b.setMaximumCapacity(150)
        c.sinkTo(b)
        for x in range(30): #it should take this long to fill up
            timer.runUntilCurrent()
        self.assertEqual(b.updateCharge(), 150)



class ChronologyTestCase(unittest.TestCase):
    def testTickery(self):
        a = []

        def hoorj():
            a.append("woot")

        timer.callLater(1, hoorj)
        timer.callLater(1.2, hoorj)
        timer.callLater(1.5, hoorj)
        timer.callLater(2, hoorj)
        timer.runUntilCurrent()
        self.assertEquals(len(a), 3)
        timer.runUntilCurrent()
        self.assertEquals(len(a), 4)

    def testCallZero(self):
        """
        Test that timer.callLater(0, timer.time) results in that
        timer.time call returning the same value as a synchronous
        timer.time(). The only way this could fail is if the reactor
        takes more than a second to iterate.
        """
        a = [timer.time()]
        def foo():
            a.append(timer.time())
            reactor.stop()
        timer.callLater(0, foo)
        reactor.run()
        self.assertEquals(*a)

    def testTimeFixing(self):
        t = chronology.Timer(test=True)
        a=[]
        t.callLater(1, a.append, None)
        t.callLater(2, a.append, None)

        time.sleep(2.5)
        t.runUntilCurrent()
        self.assertEquals(len(a), 2)

from reality import furniture

class FurnitureTestCase(unittest.TestCase):
    def setUp(self):
        d = self.mktemp()
        self.store = storq.Store(opj(d, "db"), opj(d, "files"))            

    def tearDown(self):
        self.store.close()

    def testSit(self):
        s = self.store
        chair = s.transact(things.Movable, s, "chair")
        chair.addAdapter(furniture.Chair, ignoreClass=1)
        room = s.transact(ambulation.Room, s, "room")
        bob = s.transact(things.Actor, s, "bobby")
        for x in (chair, bob):
            s.transact(x.moveTo, room)

        pars = english.Parsing(bob).parse
        pars('sit chair')
        self.failUnlessEqual(bob.location.getItem(), chair)
