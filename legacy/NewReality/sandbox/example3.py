from reality import things, actions, wiring,\
     harm, ambulation, emporium, conveyance, observation
from reality.text.common import IDescribeable

## Set up simulation
room = ambulation.Room("room")
bob = things.Actor("Bob")
rodney = things.Actor("rodneY")

sword = things.Movable("sword")
sword.addAdapter(harm.Weapon, True)
sword.addAdapter(conveyance.Portable, True)
armor = things.Movable("armor")
armor.addAdapter(harm.Armor,True)
armor.addAdapter(conveyance.Portable, True)
for o in rodney, bob, sword, armor:
    o.moveTo(room)

## Start network server
bobServer = wiring.TextFactory(bob)
rodneyServer = wiring.TextFactory(rodney)

from twisted.internet import app
application = app.Application("reality")
application.listenTCP(8888, bobServer)
application.listenTCP(8889, rodneyServer)
if __name__ == '__main__':
    application.run()

'''
bob: "hit rodney with sword"
rodney: "wear armor"
bob: "hit rodney with sword"
'''
