from reality import things, actions, wiring,\
     harm, ambulation, emporium, conveyance, observation
from reality.text import common, english
## Set up simulation
shop = ambulation.Room("SwordMart")
shop.getComponent(common.IDescribeable).describe("__main__", "A weapons shop. ")
room = ambulation.Room("Non-Shop")
room.getComponent(common.IDescribeable).describe("__main__", "Not a shop.")
exit = emporium.ShopDoor("Security Door", "north", shop, room)
exit.addAdapter(ambulation.OpenDoor, True)
trapdoor = ambulation.Door("Secret Trapdoor", "down", shop, room, twoway=0)
trapdoor.addAdapter(ambulation.OpenDoor, True)
shopkeeper = things.Actor("Asidonhopo")

vendor = shopkeeper.addAdapter(emporium.Vendor, True)
bob = things.Actor("bob")
bob.gender = things.MALE
customer = bob.addAdapter(emporium.Customer, True)
bauble = things.Movable("long sword")
bauble2 = things.Movable("short sword")
bauble2.addAdapter(conveyance.Portable, True)
bauble.addAdapter(conveyance.Portable, True)

[t.moveTo(shop) for t in (shopkeeper, bob, bauble, bauble2)]

vendor.stock(bauble, 100)
vendor.stock(bauble2, 50)
vendor.balance = 0
customer.balance = 100

## Start network server
bobServer = wiring.TextFactory(bob)

from twisted.internet import app
application = app.Application("reality")
application.listenTCP(8888, bobServer)
if __name__ == '__main__':
    application.run()

'''
"go north"
"go south"
"get bauble"
"go north" -- refused
"go down" -- lose bauble
"go south" -- back to shop
"get bauble"
"buy bauble"
'''
