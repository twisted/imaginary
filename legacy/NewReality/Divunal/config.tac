#!python

import os
from twisted.internet import app
from twisted.web import server
from twisted.python import util
from twisted.spread import pb
from twisted.reality import reality, plumbing

a = application = app.Application("reality")
r = reality.fromSourceFile(util.sibpath(__file__, "build_map"), a)

a.listenTCP(pb.portno, pb.BrokerFactory(pb.AuthRoot(a)))
a.listenTCP(8080, server.Site(plumbing.Web(r)))
a.listenTCP(4040, plumbing.Spigot(r))

r.loop(r['cloud scene balcony'].fling)
