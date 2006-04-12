
# import stuff
from reality import wiring, things, ambulation, conveyance, raiment
from reality import harm, observation, pyrotechnics, acoustics
from reality.text.common import IDescribeable
from quotient import storq

# "This is the thing that troubles me, for I cannot forget Carcosa,
# where black stars hang in the heavens, where the shadows of men's
# thoughts lengthen in the afternoon..."

s = storq.Store("nettest-data", "nettest-files")

def _1():
    room = ambulation.Room(s, "room1")
    room.getComponent(IDescribeable).describe("__main__", "This is a basic test room. This room description is really quite long. In fact, I plan on writing a book in this room description rivalling War and Peace. However, I probably will not finish it tonight. I will probably work on it for several years, writing my book-length room description into this single string, without putting any line endings in it ever.")
    otherRoom = ambulation.Room(s, "room2")
    person = things.Actor(s, "bob")
    bauble = things.Movable(s, "bauble")
    bauble2 = things.Movable(s, "bauble")
    shirt = things.Movable(s, "shirt")
    shirt.getComponent(IDescribeable).describe("__main__", "It is a shirt!")
    shirt.getComponent(IDescribeable).describe("html", "It is a <em>shirt!</em>")
    rodney = things.Actor(s, "rodney")
    sword = things.Movable(s, "sword")
    sword.addAdapter(harm.Weapon, 1)
    armor = things.Movable(s, "chainmail")
    armor.addAdapter(harm.Armor,1).setStyle("tunic")
    sword.moveTo(person)
    armor.moveTo(rodney)

    # *chomp* *chomp*
    globals().update(locals())

s.transact(_1)

# a cave

def _2():
    cave = s.transact(ambulation.Room, s, "dark cave")
    ambulation.Exit(s, "cave", "east", otherRoom, cave)
    cave.getComponent(IDescribeable).describe("__main__", "It is a cave.")
    ambulation.Exit(s, "tunnel", "southwest", cave, room)
    

    billy =things.Actor(s, "billy")
    billy.moveTo(cave)

    rocket =things.Movable(s, "rocket")
    rocket.addAdapter(pyrotechnics.Rocket, True)
    
    whistle =things.Movable(s, "whistle")
    whistle.addAdapter(acoustics.Whistle, True)
    
    shirt.addAdapter(raiment.Wearable, 1).setStyle('shirt')
    
    d =ambulation.Door(s, "door", "north", room, otherRoom)
    d.addAdapter(harm.DamageableDoor, True)
    
    otherRoom.getComponent(IDescribeable).describe("__main__", "This is another basic test room.")
    
    globals().update(locals())

s.transact(_2)

# some charge stuff

def _3():
    from reality import charge
    
    battery =things.Movable(s, "battery")
    battery.addAdapter(charge.Battery, ignoreClass=True)
    
    charger =things.Movable(s, "charger")
    charger.addAdapter(charge.BatteryCharger, ignoreClass=True)

    radio =things.Movable(s, "radio")
    radio.addAdapter(charge.Radio, ignoreClass=True)
    
    globals().update(locals())

s.transact(_3)

# furniture
def _4():
    from reality import furniture

    print 'making chair'
    chair =things.Movable(s, "chair")
    print 'made chair'
    chair.addAdapter(furniture.Chair, ignoreClass=True)
    print 'added adapter'

    # move everything around!

    for o in rocket, whistle, bauble, bauble2, shirt, battery, charger, radio, chair:
        print 'portabilizing', o
        o.addAdapter(conveyance.Portable, ignoreClass=True)

    for o in bauble, rodney, bauble2, person, shirt, rocket, whistle, battery, charger, radio, chair:
        print "moving", o
        o.moveTo(room)


s.transact(_4)

# connect to the network
network = wiring.TextFactory(person)
network2 = wiring.TextFactory(rodney)
from twisted.internet import app
application = app.Application("reality")
application.listenTCP(8888, network)
application.listenTCP(8889, network2)

# let us debug, shall we yes!
from twisted.manhole import telnet
tn = telnet.ShellFactory()
tn.namespace['bob'] = person
application.listenTCP(8890, tn)

# hook up web shit
from twisted.web import server
from reality.web import webwiring
root = webwiring.RealityPage(person)
site = server.Site(root)
application.listenTCP(8088, site)
from twisted.web.woven.flashconduit import FlashConduitFactory
application.listenTCP(4321, FlashConduitFactory(site))

if __name__ == '__main__':
    import sys
    from twisted.python import log
    log.startLogging(sys.stdout, 0)
    application.run()
