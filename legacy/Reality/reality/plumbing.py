
# Twisted, the Framework of Your Internet
# Copyright (C) 2001-2002 Matthew W. Lefkowitz
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

"""Plumbing classes (pump, pipeline) to put Twisted Reality on the net.
"""

import md5
import string
from cStringIO import StringIO

from reality import player
from twisted.protocols import telnet, http
from twisted.python import log
from twisted.internet import tcp, protocol
from twisted.web import resource, html, widgets, guard
from twisted import copyright

# New-style Imports
from twisted.cred.util import Unauthorized

portno  = 8889
tportno = 8888

class Telnet(telnet.Telnet):
    """
    A telnet protocol extended to support the extra (non-standard)
    command COMPRESS2.
    """
    
    COMPRESS2 = chr(86)

    compressor = None
    compressionEnabled = 0

    def connectionMade(self):
        """
        Try to enable compression and call parent's connectionMade() method
        """
        self.transport.write(telnet.IAC + telnet.WILL + self.COMPRESS2)
        telnet.Telnet.connectionMade(self)


    def iac_DO(self, feature):
        if feature == self.COMPRESS2:
            self.transport.write(telnet.IAC + telnet.SB + self.COMPRESS2 + telnet.IAC + telnet.SE)
            self.compressionEnabled = 1
            self.compressor = zlib.compressobj()

    def write(self, data):
        """
        Write the data to our transport, compressing it first if the
        compression negotiation was successful.
        """
        if self.compressionEnabled:
            data = self.compressor.compress(data) + self.compressor.flush(zlib.Z_SYNC_FLUSH)
        telnet.Telnet.write(self, data)


try:
    import zlib
    _HoseParent = Telnet
except ImportError:
    _HoseParent = telnet.Telnet

class Hose(_HoseParent):
    """A telnet protocol implementation for TR.
    """
    mode = "User"

    def welcomeMessage(self):
        """A message welcoming you to TR.
        """
        return "\r\nTwisted Reality %s\r\n" % copyright.version


    def loginPrompt(self):
        """A login prompt that asks for your character name.
        """
        return "character: "


    def telnet_Password(self, password):
        """Checks authentication against the reality; returns a boolean indicating success.
        """

        self.write(telnet.IAC+ telnet.WONT+ telnet.ECHO+".....\r\n")
        req = self.factory.reality.application.authorizer.getIdentityRequest(self.username)
        self.pw = password
        req.addCallbacks(self.loggedIn, self.notLoggedIn)
        req.arm()
        # kludge; this really ought to be called later, but since the arm()
        # call actually calls self.loggedIn, then the return value of this
        # function will be used to assign to self.mode... ugh.
        if self.mode == 'Command':
            return 'Command'
        return "Pending"

    def loggedIn(self, identity):
        """The player's identity has been retrieved.  Now, check their password.
        """

        auth = identity.verifyPlainPassword(self.pw)
        auth.addCallbacks(self.verifyOk, self.verifyFailed, (identity,))
        auth.arm()

    def verifyOk(self, result, identity):
        # The identity checks out.
        characters = []
        # XXX REFACTOR: Hmm.  Is this next bit common behavior?
        r = self.factory.reality
        nm = r.getServiceName()
        for serviceName, perspectiveName in identity.getAllKeys():
            if serviceName == nm:
                ### XXX FIXME
                ### This can't really be done this way.
                ### getPerspectiveNamed ought to be asynchronous.
                characters.append(r.getPerspectiveNamed(perspectiveName))
        lc = len(characters)
        if lc == 1:
            p = characters[0]
        elif lc > 1:
            p = characters[0]
            self.write("TODO: character selection menu\r\n")
        else:
            raise Unauthorized("that identity has no TR characters")

        p = p.attached(self, identity)
        self.player = p
        self.identity = identity
        self.write("Hello "+self.player.name+", welcome to Reality!\r\n"+
                             telnet.IAC+telnet.WONT+telnet.ECHO)
        self.mode = "Command"
    
    def verifyFailed(self, error):
        log.msg(error)
        self.transport.loseConnection()

    def notLoggedIn(self, err):
        log.msg('requested bad username')
        self.transport.loseConnection()

    def telnet_Pending(self, pend):
        self.write("Please hold...\r\n")
        return "Pending"


    shortcuts = [("'", 'say %s'),
                 (':', 'emote %s'),
                 ('$', 'exec %s'),
                 ]

    def telnet_Command(self, cmd):
        """Execute a command as a player.
        """
        if not cmd: return "Command"
        cmd = string.strip(cmd)

        #shortcut translations.
        for short, long in self.shortcuts:
            l = len(short)
            if cmd.startswith(short):
                cmd = long % cmd[l:]

        self.player.execute(cmd)
        return "Command"

    def connectionLost(self, reason):
        """Disconnect player from this Intelligence, and clean up connection.
        """
        telnet.Telnet.connectionLost(self, reason)
        if hasattr(self, 'player'):
            if hasattr(self.player, 'intelligence'):
                self.player.detached(self, self.identity)

    def seeName(self, name):
        """Display a focused name bracketed, in bold.
        """
        self.write(telnet.BOLD_MODE_ON+"[ "+name+" ]"+telnet.BOLD_MODE_OFF+
                             "\r\n")

    def callRemote(self, key, *args, **kw):
        # pass-through of remote methods
        apply(getattr(self, key), args, kw)


    def seeItem(self, key, parent, value):
        """Display an item that's present.
        """
        self.write(" "+value+"\r\n")

    def dontSeeItem(self, key, parent):
        """no-op; would be nonsensical over telnet.
        """

    def seeNoItems(self):
        """no-op; would be nonsensical over telnet.
        """

    def seeExit(self, direction):
        """Display a single exit.
        """
        self.write("You can go "+direction+"\r\n")

    def dontSeeExit(self, direction):
        """no-op; would be nonsensical over telnet.
        """

    def seeNoExits(self):
        """no-op; would be nonsensical over telnet.
        """

    def seeDescription(self, key, description):
        """Displays a description.
        """
        self.write(description+"\r\n")

    def dontSeeDescription(self, key):
        """no-op; would be nonsensical over telnet.
        """

    def seeNoDescriptions(self):
        """no-op; would be nonsensical over telnet.
        """

    def seeEvent(self, string):
        """Displays an event to the player.
        """
        self.write(string+'\r\n')

    def request(self, question,ok,cancel):
        """Requests are not supported by this interface; calls cancel() immediately.
        """
        self.write('edit operations not supported in telnet!\r\n')
        cancel()



class Spigot(protocol.Factory):
    """
    A telnet factory for Reality.
    """

    def buildProtocol(self, addr):
        p = Hose()
        p.factory = self
        return p
    
    def __init__(self, world):
        """Initialize with a reality.Reality instance.
        """
        self.reality = world

class ThingWidget(widgets.StreamWidget):
    """A web-based interface to a reality.thing.Thing.
    """
    def __init__(self, thing):
        """Initialize with a particular thing.
        """
        self.thing = thing

    def getTitle(self, request):
        """Return a page title formatting the request.
        """
        session = request.getSession()
        return "Twisted Reality: %s" % self.thing.shortName(session.truser)

    def stream(self, write, request):
        """Display representation of a Thing (or move a Thing and redirect, depending on URI).
        """
        player = request.getSession().truser
        if request.args.has_key("action"):
            # cheating...
            # request.setHeader("refresh","0; URL=%s" % (request.prePathURL()))
            player.location = self.thing
            log.msg("Eep?")
            write("I have an action key! %s, %s" % (player.location, self.thing))
            # write("Redirecting...")
        write("<table><tr><td colspan=2>")
        write(self.thing.descriptionTo(player))
        write('<br><A HREF="%s?action=moveMe">Move Me Here</a>' %
              (request.prePathURL()))
        write("</td></tr><tr><td><ul>")
        for thing in self.thing.getThings(player):
            write('<LI><A HREF="%s">%s</A>' % (
                thing.thing_id,
                thing.presentPhrase(player)))
        if self.thing in player.locations:
            write('<hr><li><A HREF="%s">You are here.</a>' % (player.thing_id))
        write("</ul></td><td>")
        write("<UL>")
        for direc in self.thing.exits:
            dest = self.thing.findExit(direc)
            write("<LI>")
            write(direc)
            write(": ")
            write('<A HREF="%s">' % dest.thing_id)
            write(dest.shortName(player))
            write('</A>')
        write("</UL>")
        write("</td></tr></table>")

class Web(guard.ResourceGuard):
    def __init__(self, reality):
        guard.ResourceGuard.__init__(self, _Web(reality), reality, 'realIdent', 'truser')

class _Web(widgets.Gadget, widgets.StreamWidget):
    """A web interface to a reality.reality.Reality.
    """
    def __init__(self, in_reality):
        """Initialize with a reality.
        """
        widgets.Gadget.__init__(self)
        self.reality = in_reality

    def getWidget(self, name, request):
        """Get a Thing from this reality.
        """
        return ThingWidget(self.reality.getThingById(int(name)))

    def stream(self, write, request):
        """List all availble Things and there IDs
        """
        player = request.getSession().truser
        write('<UL>\n')
        for thing in self.reality.objects():
            np = thing.nounPhrase(player)
            write('<LI><A HREF="%s">%s</a>\n'% (str(thing.thing_id),np))
        write('</UL>\n')

