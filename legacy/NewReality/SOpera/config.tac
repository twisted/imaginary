# Space Opera - A Multiplayer Science Fiction Game Engine
# Copyright (C) 2002 Jean-Paul Calderone
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	 See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
#
#!python

import os
from twisted.internet import app
from twisted.web import server
from twisted.python import util
from twisted.spread import pb
from Reality import reality, plumbing

a = application = app.Application("reality")
r = reality.fromSourceFile(util.sibpath(__file__, "build_map"), a)

a.listenTCP(pb.portno, pb.BrokerFactory(pb.AuthRoot(a)))
a.listenTCP(8181, server.Site(plumbing.Web(r)))

plumbing.Hose.delimiters.append('\n')
a.listenTCP(4242, plumbing.Spigot(r))
a.persistStyle = None
