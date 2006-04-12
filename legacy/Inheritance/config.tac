#!python

import os
from twisted.internet import main
from twisted.web import server
from twisted.python import util
from twisted.spread import pb
from Reality import reality, plumbing

a = application = main.Application("reality")
r = reality.fromSourceFile(util.sibpath(__file__, "build_map"), a)

a.listenOn(pb.portno, pb.BrokerFactory(pb.AuthRoot(a)))
a.listenOn(8080, server.Site(plumbing.Web(r)))
a.listenOn(4040, plumbing.Spigot(r))
