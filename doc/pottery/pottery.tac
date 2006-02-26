from pottery import objects, wiring
from twisted.application import service

application = service.Application("Pottery Game Server")

wiring.makeService(
    objects.Room("The Place"), 
    {'port': 4022,
     'pubKeyFile': 'pottery_id.pub',
     'privKeyFile': 'pottery_id'},
    {'port': 4023}).setServiceParent(application)
