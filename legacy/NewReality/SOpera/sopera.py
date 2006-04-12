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

"""
Space Opera basic objects
"""

# System imports
import random, string, md5, cStringIO as StringIO 

# Reality imports
from Reality import thing, container, reality, player, error, room, phrase
from Reality.beyondspike import NoTargetAction, codeInterfaceForAction

# Twisted imports
from twisted.python.components import Interface, registerAdapter
from twisted.internet import passport
from twisted.python import reflect

# Sibling imports
import utils, skills, mailer, space


class SpaceOpera(reality.Reality):
    __pendingPlayers = []
    zeusAdmin = None
    systems = []

    def isOkName(self, name):
        try:
            self[name]
            return 0
        except:
            return 2 < len(name) < 11

    def addPendingPlayer(self, player):
        self.__pendingPlayers.append(player)
        # XXX - make this a timer or something
        if len(self.__pendingPlayers) > 10:
            del self.__pendingPlayers[0]

class Room(room.Room, space.Located):
    def ambient_go(self, sentence):
        try:
            t = self.findExit(sentence.strings[''])
        except error.NoExit, e:
            sentence.subject.hears("You can't go that way.")
        except KeyError, e:
            sentence.subject.hears("Go where?")
        else:
            self.toss(sentence.subject, t)
            t.grab(sentence.subject)


class Leave(NoTargetAction):
    pass
exec codeInterfaceForAction(Leave)

class Create(NoTargetAction):
    def __init__(self, actor, name, email):
        NoTargetAction.__init__(self, actor)
        self.actorMethodArgs = (name, email)
exec codeInterfaceForAction(Create)

class Help(NoTargetAction):
    def __init__(self, actor, text):
        NoTargetAction.__init__(self, actor)
        self.actorMethodArgs = (text,)
exec codeInterfaceForAction(Create)

class Commands(NoTargetAction):
    pass
exec codeInterfaceForAction(Commands)

class Player(player.Player, space.Located):
    FOOD_MSGS = [
        "Your stomach rumbles hungrily.",
        "Your hunger is sated for the moment.",
        "Your stomach rumbles contentedly.",
        "You are full.",
        "You are stuffed."
    ]
    
    __implements__ = (
        player.Player.__implements__,
        space.Located.__implements__,
        ILeaveActor
    )

    __all = []
    _calories = 0

    def __init__(self, name, reality = '', identityName = 'Nobody'):
        player.Player.__init__(self, name, reality, identityName)
        self.parseStyle = 'new'
        self.__all.append(self)

    def __setstate__(self, state):
        self.__dict__ = state
        self.__all.append(self)

    def execute(self, string):
        if string == "!BEYOND":
            self.parseStyle = 'new'
        elif string == "!BEFORE":
            self.parseStyle = 'old'
        elif self.parseStyle == 'new':
            c = self.getComponent(phrase.IParsing)
            print c
            c.parse(string)

        elif self.parseStyle == 'old':
            return player.Player.execute(self, string)
        else:
            raise Exception("Bwah??")

    def formatUser(self, observer):
        return (self.nounPhrase(observer),)

    def formatAllUsers(observer):
        r = []
        for i in Player.__all:
            pass
            #if i.intelligence:
            #     x = i.formatUser(observer)
            #     if x:
            #         r.append(x)
        return r
    formatAllUsers = staticmethod(formatAllUsers)

    def isFull(self):
        return self._calories > 2500

    def consumeCalories(self, amount):
        self._calories = self._calories + amount
        if self._calories > 2500:
            self.hears("You are stuffed.")
        elif self._calories > 2000:
            msg = reduce(operator.add, map(self._calories.__gt__, range(500, 2500, 500)))
            self.hears(self.FOOD_MSGS[msg])

    def actorActionPassword(self, password):
        """Usage: password <new password>
        
        Changes your password to <new password>
        """
        if len(password) < 3:
            self.hears('Try something a little longer.')
        else:
            self.password = md5.md5(password).digest()
            self.identity.setPassword(password)
            self.hears('Password changed.')

    def actorActionCommands(self):
        """Usage: commands
        
        Print a list of all your character abilities
        """
        d = {}
        reflect.addMethodNamesToDict(self.__class__, d, 'actorAction')
        self.hears('You have the following abilities:')
        d = d.keys()
        d.sort()
        self.hears(utils.format(d))


    def actorActionHelp(self, text):
        """Usage: help [topic]
        
        Disply help text for the given topic
        """
        try:
            topic = self.getAbility(text)
            self.hears(topic.__doc__ or "That action has no help information.")
        except AttributeError:
            self.hears('There is no help on that subject.')


    def actorActionLeave(self):
        if self.location and self.location.location:
            self.location = self.location.location
        else:
            self.hears("There is nowhere to go.")


registerAdapter(skills.GrantRevokeAdapter, Player, skills.IGrantTarget)
registerAdapter(skills.GrantRevokeAdapter, Player, skills.IRevokeTarget)


class Guest(Player):
    """A guest to this Space Opera.
    """
    def execute(self, action):
        """log any action performed by a guest.
        """
        print "%s: %s" % (self.name, repr(action))
        Player.execute(self, action)

    def detached(self, i, identity):
        """Reinitialize score and location on logout, as well as adding this to the list of available guests.
        """
        Player.detached(self, i, identity)
        for item in self.things:
            item.location = self.factory.start
        self.factory.guests.append(self)

    def actorActionCreate(self, name, email):
        """create <character name> <email address>
        
        Create a new character with the given name.  Email the password
        to the given email address.
        """
        if not self.reality.isOkName(name):
            self.hears('"%s" is not an acceptable character name, try again.' % name)
        else:
            pwd = ''.join([random.choice(string.letters) for x in range(8)])
            p = Player(name, self.reality)
            
            if not self.reality.zeusAdmin:
                p.addSkillSet(skills.WizardSkills())
                self.reality.zeusAdmin = 1

            p.identity = p.makeIdentity(pwd)
            self.reality.addPendingPlayer(p)
            mailer.sendPwd(name, email, pwd)

            self.hears('A password for %s has been mailed to %s.' % (name, email))
            self.intelligence.disconnect()
            p.location = self.reality.defaultStartRoom


class PlayerParser(phrase.Subparser):
    def parse_leave(self, actor, text):
        return [Leave(actor)]


    def parse_commands(self, actor, text):
        return [Commands(actor)]


    def parse_create(self, actor, text):
        try:
            return [Create(actor, *text.split())]
        except TypeError:
            return None


    def parse_help(self, actor, text):
        return [Help(text)]


phrase.registerSubparser(PlayerParser())


class GuestFactory(Player):
    """Provides guest logins.

    This is a Thing which provides guest logins.  In order to use it, install
    it in your map, and name it `guest', then call 
    """

    # md5.md5("guest").digest()
    password = '\010N\003C\240Ho\360U0\337lp\\\213\264'

    flavors = [ "Enterprise-Wide", "Networked", "Dynamic", "Multitasking",
                "Robust", "Multiuser", "Internet-Enabled", "Cross-platform",
                "Open-Source", "Scratch-and-Sniff", "Java", "Scalable",
                "Fault-Tolerant", "Mission-Critical", "Intuitive",
                "Object-Oriented", "Multimedia", "Web-Based", "P2P", "B2B",
                "Proactive", "Broadband", "Intranet", "Multithreaded",
                "Themeable"]

    def init(self, start):
        """GuestFactory.init(startingLocation) -> None: initialize

        Call this to make this object usable for logins.
        """
        guests = []
        self.start = start
        self.reality = self.start.reality
        for flavor in self.flavors:
            guest = Guest(flavor + " Guest", self.reality)
            guest.factory = self
            guest.addSynonym(flavor)
            for x in string.split(flavor, '-'):
                if x != flavor:
                    guest.addSynonym(x)
            guests.append(guest)
        self.guests = guests

    def attached(self, client, identity):
        """Find an available guest.

        This will find and return an available guest, removing them from the
        list of available guests as it does so.  It will return that guest.
        """
        if self.guests:
            guest = random.choice(self.guests)
            self.guests.remove(guest)
            guest.oldlocation = self.start
            return guest.attached(client, identity)
        else:
            raise passport.Unauthorized("Too many guests.  Try again later.")

    def destroy(self):
        """Free resources associated with this GuestFactory.
        
        This will clean up the list of related guests when this object is
        destroyed.
        """
        for guest in self.guests:
            guest.destroy()
        del self.guests
        thing.Thing.destroy(self)

# Action modules
import vending, comm
