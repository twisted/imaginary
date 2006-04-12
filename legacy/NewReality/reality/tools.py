"Building worlds is hard work. Keep these close to hand."

import time
from twisted.python import components
from twisted.web import server
from reality.web import webwiring
from twisted.manhole import telnet
from twisted.internet import app
from reality.text import common
from reality.things import Thing
from reality.wiring import TextFactory
class IConstructorNotes(components.Interface):
    "Various notes for builders."


class ConstructorNotes(components.Adapter):
    todo = None

components.registerAdapter(ConstructorNotes, Thing, IConstructorNotes)

def addTodo(obj, todoItem):
    c = obj.getComponent(IConstructorNotes)
    if c.todo is None:
        c.todo = []
    c.todo.append(' '.join((time.asctime(),todoItem)))

def describe(thing, desc):
    common.IDescribeable(thing).describe('__main__',desc)
    #Do I really need to say anything about why this is wrong and bad?
    common.IDescribeable(thing).describe('html',desc)

def simpleTRServer(*players,**kwargs):
    application = app.Application("reality")
    wiringPort = 8888
    for p in players:
        application.listenTCP(wiringPort,TextFactory(p))

        wiringPort +=1
        
    if kwargs.get('web'):
        from twisted.web.woven.flashconduit import FlashConduitFactory
        webwiringPort = 8088
        flashPort = 4321
        for p in players:
            site =  server.Site(webwiring.RealityPage(p))
            application.listenTCP(webwiringPort, site)
            #probably wrong
            application.listenTCP(flashPort, FlashConduitFactory(site))
            webwiringPort +=1
            flashPort +=1

    if kwargs.get('debug'):
        tn = telnet.ShellFactory()
        application.listenTCP(8887, tn)
        for p in players:        
            tn.namespace[common.INoun(p).name] = p
    return application
