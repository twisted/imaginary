
# Twisted, the Framework of Your Internet
# Copyright (C) 2001 Matthew W. Lefkowitz
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of version 2.1 of the GNU Lesser General Public
# License as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

"""
I am a support module for creating reality servers with mktap.
"""

# System Imports
from cPickle import load
import sys

# Twisted Imports
from reality import plumbing, realities
from twisted.internet import tcp, main
from twisted.web import server
from twisted.python import usage
from twisted.spread import pb

class Options(usage.Options):
    synopsis = ("Usage: mktap reality --map <map.rpl>\n"
                "       mktap reality --plain")
    optParameters = [['map', 'm', None,
                      "The reality map pickle to use."],
                     ['web', 'w', 8080,
                      "The port to start the web interface on."],
                     ['telnet', 't', 4040,
                      "The port to start the telnet interface on."],
                     ['faucet', 'f', 8787,
                      "The port to start the faucet interface on."]]
    optFlags = [['plain', 'p',
                 "Create a Reality with only one room, and one Author "
                 "named 'Author' with password 'changeme'."]]

def updateApplication(app, config):
    rdf = None
    if config.opts['plain'] and config.opts['map']:
        raise usage.error("--plain and --map conflict.")

    if config.opts['plain']:
        import room, player, thing
        rdf = thing._default = realities.Reality('Reality', app)
        rm = room.Room("Starting Point")(
                       description="This is where you start.")
        p = player.Author("Author")(location=rm)
        p.makeIdentity("changeme")
        
    elif config.opts['map']:
        print 'Loading %s...' % config.opts['map']
        sys.stdout.flush()
        rdf = realities._default = load(open(config.opts['map'],'rb'))
        rdf.setApplication(app)
        # Should this be considered 'Legacy'?
        rdf.addPlayersAsIdentities()
        print 'Loaded.'

    #print rdf
    if not rdf:
        raise usage.error("You *need* to specify either --plain or --map.")

    app.addDelayed(rdf)
        
    spigot = plumbing.Spigot(rdf)
    site = server.Site(plumbing.Web(rdf))
    bf = pb.BrokerFactory(pb.AuthRoot(app))
        
    if config.opts['web']:
        app.listenTCP(int(config.opts['web']), site)
    if config.opts['telnet']:
        app.listenTCP(int(config.opts['telnet']), spigot)
    if config.opts['faucet']:
        app.listenTCP(int(config.opts['faucet']), bf)
