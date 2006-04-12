
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


"""Twisted Reality ]I[

This is the simulation core of a single OR multi player text-based game.
"""

# System Imports
from copy import copy
import string

# Twisted Imports
import twisted
from twisted.python import reflect, reference, delay
from twisted.spread import pb
from twisted.cred import identity
from twisted.persisted import styles

# Sibling Imports
import player

class Reality(delay.Delayed,
              reference.Resolver,
              pb.Service):

    serviceName = 'Reality'
    def __init__(self, name='Reality', app=None):
        delay.Delayed.__init__(self)
        reference.Resolver.__init__(self, self)
        pb.Service.__init__(self, name, app)
        self._counter = 0
        self._ids = {}   #{id: object}
        self._names = {} #{name: [objects]}
        #self._players = {}

    def addPlayersAsIdentities(self):
        """Add all players with passwords as identities.
        """
        for th in self._ids.values():
            if isinstance(th, player.Player) and hasattr(th, 'password'):
                styles.requireUpgrade(th)
                idname = th.name
                print "Adding identity %s" % idname
                ident = identity.Identity(idname, self.application)
                ident.setAlreadyHashedPassword(th.password)
                ident.addKeyForPerspective(th)
                try:
                    self.application.authorizer.addIdentity(ident)
                except KeyError:
                    print 'unable to add reality identity for %s' % idname

##    def addPlayer(self, player):
##        """Add a player to this reality.
##        """
##        print 'Adding identity %s' % player.name
##        ident = identity.Identity(player.name, self.application)
##        if hasattr(player, 'password'):
##            ident.setAlreadyHashedPassword(player.password)
##        ident.addKeyForPerspective(player)
##        try:
##            self.application.authorizer.addIdentity(ident)
##        except KeyError:
##            print 'unable to add reality identity for', idname
##        self._players[player.name.lower()] = player


    def addThing(self,thing):
        """add a thing to this reality
        """
        self._counter = self._counter+1
        thing.thing_id = self._counter
        idname = string.lower(thing.name)
        assert not self._ids.has_key(thing.thing_id),\
               "Internal consistency check failure."\
               "I don't know what's going on."
        self._ids[thing.thing_id] = thing
        self._names.setdefault(idname, []).append(thing)
        self.changed = 1



    def removeThing(self,thing):
        """remove a thing from this reality
        """
        if self._ids.get(thing.thing_id) is thing:
            del self._ids[thing.thing_id]
        else:
            print "WARNING:",thing," ID CANNOT BE REMOVED FROM",self
        tlist = self._names.get(string.lower(thing.name), [])
        if thing in tlist:
            tlist.remove(thing)
        else:
            print "WARNING:",thing," NAME CANNOT BE REMOVED FROM",self
        self.changed = 1


    def unplaced(self):
        """return a list of objects in this Reality that have no place
        """
        return filter(lambda x: not x.location, self._ids.values())


    def updateName(self,thing,oldname,newname):
        assert (not oldname) or thing in self._names[string.lower(oldname)], 'Bad mojo.'
        if oldname:
            self._names[oldname.lower()].remove(thing)
        self._names.setdefault(string.lower(newname), []).append(thing)


    def __getitem__(self,name):
        print 'RADIX HATES YOU'
        l = self._names[string.lower(name)]
        if l:
            return l[0]

    def getThingById(self, thingid):
        return self._ids[thingid]

    def getThingsByName(self, name,defarg=None):
        return self._names.get(string.lower(name),defarg)

    def get(self, name):
        return self.__getitem__(name)

    def objects(self):
        return self._ids.values()

    def resolveAll(self):
        #XXX: :-(
        self.resolve(self.objects())

    ##
    # PB
    ##
    def getPerspectiveNamed(self, playerName):
        """Get a perspective from a named player.

        This will dispatch to an appropriate player by locating the named
        player.
        """
        return self[playerName.lower()]




def fromSourceFile(pathName, application=None):
    """Load a Reality from a Python source file.

    I will load and return a Reality from a python source file, similiar to one
    output by Reality.printSource.  I will optionally attach it to an
    application.
    """
    ns = {}
    execfile(pathName, ns, ns)
    result = ns['result']
    result.resolveAll()
    if application:
        result.setApplication(application)
        application.addDelayed(result)
    result.addPlayersAsIdentities()
    return result
