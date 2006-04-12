# -*- test-case-name: reality.test_reality -*-

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


# System Imports
import string
import cPickle
import os
import traceback
import time


# Twisted Imports
from twisted.python import reflect, log, rebuild, components
from twisted.spread import pb
from twisted.cred import authorizer, util
from twisted.python.components import Interface, implements, registerAdapter, Adapter

# Reality Imports
from actions import NoTargetAction, TargetAction, ToolAction
from reality.phrase import registerSubparser, Subparser, Parsing, IParsing
from reality.thing import Thing, IThing
from reality.room import Room
from reality.findsource import findSource
from reality.geometry import reverse
from reality import error



#import cStringIO as StringIO..
import cStringIO
StringIO = cStringIO
del cStringIO

class Say(NoTargetAction):
    def __init__(self, actor, speech):
        NoTargetAction.__init__(self, actor)
        self.speech = speech
        self.actorMessage = ('You say, "%s"' % speech)
        self.otherMessage = (self.actor,' says, "%s"' % speech)

    def doAction(self):
        """Nothing.
        """

class Walk(NoTargetAction):
    # TODO: calculations as to whether I will *fit* in this wonderful new place
    # I've discovered
    def __init__(self, actor, direction):
        NoTargetAction.__init__(self, actor)
        self.direction = direction
        self.where = self.place.findExit(self.direction)
        self.actorMessage = "You went ", self.direction, "."
        # TODO: nicer otherMessage!
        self.otherMessage = self.actor, " came from ", reverse(self.direction), "."
        self.oldPlaceMessage = self.otherMessage
        self.oldPlaceMessage = self.actor, " went ", self.direction, "."

    def doAction(self):
        "Move in a direction."
        self.actor.getComponent(IThing).location = self.where

    def broadcastFormat(self):
        self.place.allHear(*self.formatToOldPlace())
        NoTargetAction.broadcastFormat(self)

    def formatToOldPlace(self):
        return self.oldPlaceMessage


class Emote(NoTargetAction):
    def __init__(self, actor, emotion):
        NoTargetAction.__init__(self, actor)
        self.otherMessage = self.actorMessage = ('* ', self.actor,' ', emotion)

    def doAction(self):
        pass


class Look(TargetAction):
    def doAction(self):
        "Change focus to an object or refresh current focus."
        self.actor.getComponent(IThing).focus = self.target.getComponent(IThing)

class DropAll(NoTargetAction):
    def doAction(self):
        for t in self.actor.get_things():
            Drop(self.actor, t.getComponent(IDropTarget))
                
class Drop(TargetAction):
    def __init__(self, *a,**k):
        TargetAction.__init__(self,*a,**k)
        self.actorMessage = "You drop ",self.target,"."

    def doAction(self):
        """Place an object currently in this player into the Room which
        contains them.
        """
        t = self.target.getComponent(IThing)
        a = self.actor.getComponent(IThing)
        if t.location == a:
            t.move(destination = a.place, actor = a)
        else:
            error.Failure("You weren't holding that.")


class Inventory(NoTargetAction):
    def __init__(self, *a,**k):
        NoTargetAction.__init__(self,*a,**k)
        self.actorMessage = ''
        self.otherMessage = ''

    def doAction(self):
        "Pretty-print the list of things this Player is holding."
        actor = self.actor
        strings = map(lambda f, actor=actor: f.nounPhrase(actor),
                      actor.getThings(actor))
        if len(strings) == 0:
            actor.hears("You aren't carrying anything.")
        else:
            if len(strings) > 1:
                strings[-1] = 'and '+strings[-1]
            if len(strings) == 2:
                fin = string.join(strings)
            else:
                fin = string.join(strings,', ')
            actor.hears("You are carrying "+fin+'.')

class Take(ToolAction):
    def __init__(self, *a,**k):
        ToolAction.__init__(self,*a,**k)
        self.actorMessage = "You take ",self.target,"."

    def doAction(self):
        t = self.target.getComponent(IThing)
        a = self.actor.getComponent(IThing)
        if t.place == a:
            raise error.Already("You were already holding ",t)
        t.location = a


class IMoveable:
    def moveTo(self, newLocation, actor=None):
        """
        Move self to the Thing newLocation.  The optional Actor argument is the
        person who moved it.
        """

class Scenery(Adapter):
    __implements__ = ITakeTarget, IDropTarget
    temporaryAdapter = 1
    def preTargetTake(self, action):
        error.Failure(self.original, " is not something you can move.")
    def preTargetDrop(self, action):
        error.Failure(self.original, " is not something you can move.")

registerAdapter(Scenery, Thing, ITakeTarget)
registerAdapter(Scenery, Thing, IDropTarget)

class Portable(Adapter):
    __implements__ = ITakeTarget, IDropTarget
    def __init__(self, original, weight = 1, bulk = 1):
        Adapter.__init__(self, original)
        self.weight = weight
        self.bulk = bulk

class PlayerVerbs(Subparser):

    def parse_say(self, player, text):
        return Say(player, text),

    def parse_go(self, player, text):
        return Walk(player, text),

    parse_walk = parse_go

    def parse_look(self, player, text):
        if not text:
            return Look(player, player.location),
        if text[:3] == 'at ':
            text = text[3:]
        things = player.lookAroundFor(text)
        return map(lambda t, player=player: Look(player, t), things)

    def parse_drop(self, player, text):
        things = player.lookAroundFor(text)
        if not things and text == "all":
            return DropAll(player),
        else:
            return map(lambda t, player=player: Drop(player, t), things)
    def parse_inventory(self, player, text):
        return Inventory(player),

    def parse_emote(self, player, text):
        return Emote(player, text),

    def parse_i(self, player, text):
        if text:
            return []
        else:
            return Inventory(player),

    simpleToolParsers = {"take": Take,
                         "get": Take
                         # and at last, the circle is complete. (and this time it doesn't suck!)
                        }
    def getParserBits(self):
        items = Subparser.getParserBits(self)
        items.extend([['"', self.parse_say], [":", self.parse_emote]])
        return items

registerSubparser(PlayerVerbs())

class Player(Thing, pb.Perspective):
    """Player
    A convenience class for sentient beings
    (implying turing-test quality intelligence)
    """

    __implements__ = Thing.__implements__, ITakeActor, IDropActor
    
    def __init__(self, name, reality='', identityName="Nobody"):
        """Initialize me.
        """
        self.identityName = identityName
        Thing.__init__(self, name, reality)
        #        self.reality.addPlayer(self)



    def set_reality(self, reality):
        if self.reality is reality:
            return
        assert self.reality is None, 'player migration not implemented.'
        Thing.set_reality(self, reality)
        pb.Perspective.__init__(self, self.name, self.identityName)

    def set_service(self, svc):
        """Don't really set the service, since it can be retrieved through self.reality.
        """
        assert svc == self.reality, "Service _must_ be the same as reality."

    def get_service(self):
        """Return my reality, so that it's not duplicately stored.

        This is so that my perspective.Perspective methods work properly.
        """
        return self.reality

    hollow = 1
    def indefiniteArticle(self, observer):
        return ""

    def containedPhrase(self, observer, held):
        return "%s is holding %s." % (string.capitalize(self.nounPhrase(observer)),
                                      held.nounPhrase(observer))

    definiteArticle=indefiniteArticle
    aan=indefiniteArticle
    the=definiteArticle

    ### Remote Interface

    def perspective_execute(self, st):
        self.execute(st)

    def attached(self, remoteIntelligence, identity):
        """A user-interface has been attached to this player.

        This equates to a message saying that they're logged in.  It takes one
        argument, the interface.  This will be signature-compatible with
        RemoteIntelligence.  This is an implementation of::

            twisted.cred.perspective.Perspective.attached(reference, identity)

        and therefore follows those rules.
        """
        if not hasattr(remoteIntelligence, 'callRemote'):
            # web sessions may be attached too.
            log.msg("web viewer login: [%s]")
            return self

        if hasattr(self, 'intelligence'):
            log.msg("player duplicate: [%s]" % self.name)
            raise util.Unauthorized("Already logged in from another location.")
        log.msg("player login: [%s]" % (self.name))
        if hasattr(self, 'oldlocation'):
            self.location = self.oldlocation
            del self.oldlocation
        self.intelligence = LocalIntelligence(remoteIntelligence)
        return self

    def detached(self, remoteIntelligence, identity):
        if self.intelligence and hasattr(self.intelligence, 'remote'):
            log.msg("player logout: [%s]" % self.name)
            del self.intelligence
            self.oldlocation = self.location
            self.location = None
        else:
            log.msg("web viewer logout: [%s]" % self.name)


registerAdapter(Parsing, Player, IParsing)


class Intelligence:
    """
    An 'abstract' class, specifying all methods which TR user
    interfaces must implement.
    """

    def seeName(self, name):                         pass
    def seeItem(self, thing,name):                   pass
    def dontSeeItem(self, thing):                    pass
    def seeNoItems(self):                            pass
    def seeExit(self, direction, exit):              pass
    def dontSeeExit(self, direction):                pass
    def seeNoExits(self):                            pass
    def seeDescription(self, key, description):      pass
    def dontSeeDescription(self, key):               pass
    def seeNoDescriptions(self):                     pass
    def seeEvent(self, string):                      pass
    def request(self, question,default,c):           cancel()
    def disconnect(self):                            pass

class RemoteIntelligence:
    """
    An interface to preserve bandwidth, and keep the number of remote
    references minimal.  This wasn't strictly necessary, but it seems
    cleaner to have it.
    """
    def seeName(self, name):                        pass
    def seeItem(self, thing, parent, value):    pass
    def dontSeeItem(self, thing, parent):        pass
    def seeNoItems(self):                       pass
    def seeExit(self, direction):               pass
    def dontSeeExit(self, direction):            pass
    def seeNoExits(self):                       pass
    def seeDescription(self, key, desc):         pass
    def dontSeeDescription(self, key):             pass
    def seeNoDescriptions(self):                  pass
    def seeEvent(self, string):                       pass
    # ain't nothin' you can do about this.
    def request(self, question,default,c): pass

class LocalIntelligence(Intelligence):
    """
    This translates local intelligence calls to remote intelligence
    calls.
    """
    remote=None
    def __init__(self,remote):
        self.remote=remote
    def seeName(self, name):
        self.remote.callRemote("seeName", name)
    def seeItem(self, thing,name):
        self.remote.callRemote("seeItem", id(thing),
                               id(thing.place),
                               name)
    def dontSeeItem(self, thing):
        self.remote.callRemote("dontSeeItem", id(thing),
                               id(thing.place))
    def seeNoItems(self):
        self.remote.callRemote('seeNoItems')
    def seeExit(self, direction, exit):
        self.remote.callRemote('seeExit', direction)
    def dontSeeExit(self, direction):
        self.remote.callRemote('dontSeeExit', direction)
    def seeNoExits(self):
        self.remote.callRemote('seeNoExits',)
    def seeDescription(self, key, description):
        self.remote.callRemote('seeDescription', key,description)
    def dontSeeDescription(self, key):
        self.remote.callRemote('dontSeeDescription',key)
    def seeNoDescriptions(self):
        self.remote.callRemote('seeNoDescriptions')
    def seeEvent(self, string):
        self.remote.callRemote('seeEvent', string)
    def request(self, question,default,c):
        self.remote.callRemote('request', question,default,c)
    def disconnect(self):
        self.remote.transport.loseConnection()

def discover(name,x,y,z,
             north=1,east=1,west=1,south=1,up=1,down=1):
    """
    Jedin's `discover' verb from Divunal Classic.
    """
    # this is arbitrary, so:
    #    pos   neg
    # z= north-south
    # y= up-down
    # x= east-west
    matrix=[]
    for i in range(x):
        xrow=[]
        for j in range(y):
            zrow=[]
            for k in range(z):
                zrow.append(Room('%s (%d,%d,%d)'%(name,i,j,k)))
            xrow.append(zrow)
        matrix.append(xrow)
    for i in range(x):
        for j in range(y):
            for k in range(z):
                if south:
                    if k > 0:
                        matrix[i][j][k].connectExit('south',matrix[i][j][k-1])
                if north:
                    if k < z-1:
                        matrix[i][j][k].connectExit('north',matrix[i][j][k+1])
                if west:
                    if i > 0:
                        matrix[i][j][k].connectExit('west',matrix[i-1][j][k])
                if east:
                    if i < x-1:
                        matrix[i][j][k].connectExit('east',matrix[i+1][j][k])
                if down:
                    if j > 0:
                        matrix[i][j][k].connectExit('down',matrix[i][j-1][k])
                if up:
                    if j < y-1:
                        matrix[i][j][k].connectExit('up',matrix[i][j+1][k])


    return matrix


def persist_log(author, reality, filename, time):
    log.msg("%s persisted %s to %s.rp at %s" % (author, reality.name, filename, asctime(gmtime(time))))


class Author(Player):

    wizbit = 1

    def __init__(self,*args,**kw):
        apply(Player.__init__,(self,)+args,kw)
        self.code_space={'self':self,
                         'Thing':Thing,
                         'log_dig':None,
                         'log_create':None,
                         'log_persist':persist_log,
                         'trashcan':None,
                         #'__builtins__':None
                         }


    def util_wizuser(self, p):
        """wizuser (name)
        Upgrades a Player to an Author.
        """
        #I would use isinstance(), but I don't wanna be suprised.
        if p.__class__ == Player:
            p.__class__ = Author
            p.code_space={'self':p,
                          'Thing':Thing,
                          'log_dig':None,
                          'log_create':None,
                          'log_persist':persist_log,
                          'trashcan':None,
                          }
            self.hears(p,"has been wiz'd upon.")
            p.hears(self,"wizzes all over you. Ewww!")
        else:
            self.hears("That's not a Player!")


    def execute(self, string):
        """
        overrides execute from Player; this adds the "$python" capability.
        """
        if string != "" and string[0]=='$':
            try:
                return self.runcode(string[1:])
            except error.RealityException, re:
                self.hears(re.format(self))
                return re
        return Player.execute(self,string)

    def runcode(self, cmd):
        """
        Run a block of code as this user.
        """
        fn='$'+self.name+'$'
        try:    code=compile(cmd,fn,'eval')
        except:
            try: code=compile(cmd,fn,'single')
            except:
                error.Failure("That won't compile.")

        try:
            val=eval(code,self.code_space)
            if val is not None:
                self.hears(repr(val))
                return val
        except:
            sio=StringIO.StringIO()
            traceback.print_exc(file=sio)
            error.Failure(sio.getvalue())

    def util_snippet(self, snipname):
        """snippet {name}
This creates an arbitrarily named string in your namespace from a
response-request and runs it as a block of python code.  BE CAREFUL when using
this; do not define functions, for example, or they will render your map
unpickleable.
        """
        def cancel(self): pass
        def ok(self,code,o=self, snipname=snipname):
            cs = o.code_space
            cs[snipname] = code
            try:
                code = compile(code, '$$'+o.name+'$$', 'exec')
                exec code in cs, cs
            except:
                sio = StringIO.StringIO()
                traceback.print_exc(file=sio)
                o.hears(sio.getvalue())

        c = pb.Referenceable()
        c.remote_ok = ok
        c.remote_cancel = cancel

        code = self.code_space.get(snipname, "")
        self.request("Snippet %s" % snipname,code,c)


    def util_describe(self,obj):
        """describe object
this will prompt you for a description.  enter something."""

        def setdesc(desc, obj=obj):
            obj.description = desc
        def forgetit():
            pass
        c = pb.Referenceable()
        c.obj = obj
        c.remote_ok=setdesc
        c.remote_cancel=forgetit

        desc=obj.get_description()
        if desc != "<not a string>":
            self.request("Please describe %s"%obj.nounPhrase(self),desc,c)
        else:
            self.hears(
                "That object's description is a dynamic property -- "
                "you probably shouldn't mess "
                "with it directly.  Take a look at the source for details.")

