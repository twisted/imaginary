from twisted.python import components 
from reality import things, actions, ambulation, acoustics, pyrotechnics, conflagration, harm, wiring, observation
from reality.text import english


room = ambulation.Room("Room")
room2 = ambulation.Room("Room 2")
door = ambulation.Door("door","north",room,room2)
door.addAdapter(harm.DamageableDoor, True)
bob = things.Actor("bob")
rocket = things.Movable("rocket")
rocket.addAdapter(pyrotechnics.Rocket, True)
candle = things.Movable("candle")
candle.addAdapter(conflagration.Candle, True).light()
whistle = things.Movable("whistle")
whistle.addAdapter(acoustics.Whistle, True)
whistle.moveTo(room)
candle.moveTo(room)
bob.moveTo(room)
rocket.moveTo(room)

network = wiring.TextFactory(bob)
from twisted.internet import app
application = app.Application("reality")
application.listenTCP(8888, network)
if __name__ == '__main__':
    import sys
    from twisted.python import log
    log.startLogging(sys.stdout, 0)
    application.run()
