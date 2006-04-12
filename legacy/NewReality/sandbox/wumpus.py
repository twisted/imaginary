from twisted.python import components 
from reality import things, actions, ambulation, harm, wiring, observation 
from reality.text import english
from reality.text.common import IDescribeable
import random

## Hazards
class IHazard(components.Interface): pass

class Pit(components.Adapter):
    __implements__ = things.IMoveListener, IHazard
    hazardText = "You feel a draft nearby."
    def thingLeft(*args): pass
    def thingMoved(*args): pass

    def thingArrived(self, emitter, event):
        if isinstance(emitter, things.Player):
            emitter.emitEvent("Uh-oh! You fell in a pit and broke every bone in your body!",intensity=1)
            emitter.die()

class Bats(components.Adapter):
    __implements__ = things.IMoveListener, IHazard

    hazardText = "You hear the rustle of bat wings."
    def thingLeft(*args): pass
    def thingMoved(*args): pass

    def thingArrived(self, emitter, event):
        if isinstance(emitter, things.Player):
            emitter.emitEvent("The bats swoop down upon you"
                             " and haul you off to another part of the cave!",
                             intensity=1)
            
            r = random.choice(rooms)            
            emitter.moveTo(r)

class Wumpus(components.Adapter):
    __implements__ = things.IMoveListener, IHazard, harm.IDamageTarget
    hazardText = "A foul stench fills the air here."
    def thingLeft(*args): pass
    def thingMoved(*args): pass

    def thingArrived(self, emitter, event):
        if isinstance(emitter, things.Player):
            emitter.emitEvent("*ROAR* *chomp* *snurfle* *chomp*! The Wumpus gobbles you up before you can say Jack Robinson!")
            emitter.die()
            
class HazardListener(things.Thing):
    __implements__ = things.IMoveListener,

    def __init__(self, player):
        things.Thing.__init__(self,"")
        self.player = player
        player.link(self)

    def thingArrived(*args): pass
    def thingLeft(*args): pass
    def thingMoved(self,player,event):
        if player is not self.player:
            return
        hazards = player.lookFor(None,IHazard,3)
        if hazards:
            #Some thing or things in the next room. Warn the player.
             for h in hazards:
                player.emitEvent(h.hazardText,intensity=1)

ambulation.Exit.classForwardInterface(IHazard)

## Rooms

rooms = a,b,c,d,e,f,g,h = [ambulation.Room("Room " + n) for n in "ABCDEFGH"]
# room A
ambulation.Exit("tunnel","b",a,b,twoway=True,reverseName="a")
ambulation.Exit("tunnel","d",a,d,twoway=True,reverseName="a")
ambulation.Exit("tunnel","e",a,e,twoway=True,reverseName="a")

#room B
ambulation.Exit("tunnel","c",b,c,twoway=True,reverseName="b")
ambulation.Exit("tunnel","f",b,f,twoway=True,reverseName="b")

#room C
ambulation.Exit("tunnel","d",c,d,twoway=True,reverseName="c")
ambulation.Exit("tunnel","g",c,g,twoway=True,reverseName="c")

#room D
ambulation.Exit("tunnel","h",d,h,twoway=True,reverseName="d")

#room E
ambulation.Exit("tunnel","h",e,h,twoway=True,reverseName="e")
ambulation.Exit("tunnel","f",e,f,twoway=True,reverseName="e")

#room F
ambulation.Exit("tunnel","g",f,g,twoway=True,reverseName="f")

#room G
ambulation.Exit("tunnel","h",g,h,twoway=True,reverseName="g")

#room H - done

#limbo

limbo = ambulation.Room("Limbo")
limbo.getComponent(IDescribeable).describe("__main__", "Purple mists swirl around you.")
ambulation.Exit("exit","out",limbo,a,twoway=False)

## pits

rs = rooms[1:]
random.shuffle(rs)
for r in rs[:2]:
    print "Pit in", r.getComponent(english.INoun).shortName(None)
    p = things.Movable("pit")    
    p.addAdapter(Pit,1)
    p.moveTo(r)

## bats
random.shuffle(rs)

for r in rs[:2]:
    print "Bats in ",r.getComponent(english.INoun).shortName(None)
    b = things.Movable("bats")
    b.addAdapter(Bats,1)
    b.addAdapter(english.CollectiveNoun,1)
    b.getComponent(english.INoun).changeName("bats") #this line should not be necessary
    b.moveTo(r)


    
## startup
for r in rooms:
    r.getComponent(IDescribeable).describe("__main__","Just a boring cave.")
bob = things.Player("bob")
bob.home = limbo
HazardListener(bob)
bob.moveTo(limbo)
network = wiring.TextFactory(bob)
from twisted.internet import app
application = app.Application("reality")
application.listenTCP(8888, network)

from twisted.manhole import telnet
tn = telnet.ShellFactory()
tn.namespace['bob'] = bob
application.listenTCP(8890, tn)

if __name__ == '__main__':
    import sys
    from twisted.python import log
    log.startLogging(sys.stdout, 0)
    application.run()
