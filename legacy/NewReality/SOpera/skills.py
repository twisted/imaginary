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

# System imports
import sys, traceback, copy, types, cStringIO as StringIO

# Twisted imports
from twisted.python.components import Adapter, Interface, registerAdapter

# Reality imports
from Reality import thing, container, reality, player, error, room, phrase
from Reality.beyondspike import NoTargetAction, TargetAction, codeInterfaceForAction

# Sibling imports
import utils, skills, objects, vending, sopera


def findClass(name, moduleSequence):
    for mod in moduleSequence:
        if hasattr(mod, name):
            return getattr(mod, name)
    return None


class Grant(TargetAction):
    def __init__(self, actor, target, capAdapter):
        TargetAction.__init__(self, actor, target)
        self.actorMethodArgs = self.actorMethodArgs + (capAdapter,)
exec codeInterfaceForAction(Grant)

class IGrantTarget(Interface):
    def targetActionGrant(self, actor):
        pass

    def addCapability(self, adapter, interfaces):
        pass
    

class GrantList(NoTargetAction):
    pass
exec codeInterfaceForAction(GrantList)


class Revoke(TargetAction):
    def __init__(self, actor, target, capInterface):
        TargetAction.__init__(self, actor, target)
        self.actorMethodArgs = self.actorMethodArgs + (capInterface,)
exec codeInterfaceForAction(Revoke)


class IRevokeTarget(Interface):
    def targetActionRevoke(self, actor):
        pass


    def remCapability(self, revoker, adapter):
        pass


class GrantRevokeAdapter(Adapter):
    __implements__ = (IGrantTarget, IRevokeTarget)

    capabilities = {}
    
    def targetActionGrant(self, actor):
        raise NotImplemented
    
    def targetActionRevoke(self, actor):
        raise NotImplemented
    
    def addCapability(self, adapter, interfaces):
        if not self.capabilities:
            self.capabilities = {}
        self.capabilities[adapter] = interfaces
        for i in interfaces:
            self.original.setComponent(i, adapter)


    def remCapability(self, revoker, adapterType):
        r = 0
        for adapter in self.capabilities:
            if isinstance(adapter, adapterType):
                if adapter.granter is not revoker:
                    raise ValueError # XXX
                r = len(self.capabilities[adapter])
                for i in self.capabilities[adapter]:
                    self.original.remComponent(i)
                del self.capabilities[adapter]
        return r


class RevokeList(TargetAction):
    pass
exec codeInterfaceForAction(RevokeList)


class GrantCapability(thing.SkillSet):
    """
    Endows the capability to grant and revoke capabilities.
    """
    __implements__ = (IGrantActor, IGrantListActor, IRevokeActor, IRevokeListActor)

    _skillModules = [skills]
    
    grantedBy = None

    def __init__(self, actor, grantedBy = None):
        thing.SkillSet.__init__(self, actor)
        self.grantedBy = grantedBy
        self.code_space = {}

    def __getstate__(self):
        dict = self.__dict__.copy()
        dict['code_space'] = {'self': self.original, 'Reality': sopera.SpaceOpera}
        return dict


    def actorActionGrant(self, target, capAdapter):
        capAdapter = findClass(capAdapter, self._skillModules)
        if capAdapter is None:
            self.original.hears("There is no such capability.")
        else:
            for i in capAdapter.__implements__:
                try:
                    target.original.getComponent(i)
                    self.original.hears(target.original, " already has that capability.")
                    break
                except KeyError:
                    pass
            else:
                a = capAdapter(target.original, self.original)
                target.addCapability(a, a.__implements__)
                self.original.hears("Capability ", capAdapter, " granted to ", target.original, ".")
                target.original.hears(self.original, " has granted you the ", capAdapter, " capability.")
    
    
    def actorActionGrantList(self):
        out = []
        for mod in self._skillModules:
            for attr in dir(mod):
                cl = getattr(mod, attr)
                if isinstance(cl, types.ClassType) and issubclass(cl, thing.SkillSet):
                    out.append(attr)
        self.original.hears(utils.format(out))


    def actorActionRevoke(self, target, capAdapter):
        capAdapter = findClass(capAdapter, self._skillModules)
        if capAdapter is None:
            self.original.hears("There is no such capability.")
        else:
            try:
                r = target.remCapability(self.original, capAdapter)
            except ValueError:
                self.original.hears("You can only revoke capabilities you have granted.")
            else:
                if not r:
                    self.original.hears(target.original, " does not have that capability.")
                else:
                    self.original.hears("You have revoked the ", capAdapter, " capability from ", target.original, ".")
                    target.original.hears(self.original, " has revoked your ", capAdapter, " capability.")


    def actorActionRevokeList(self, target):
        self.original.hears(utils.format(map(str, target.capabilities)))


class Rebuild(NoTargetAction):
    pass
exec codeInterfaceForAction(Rebuild)

class Exec(NoTargetAction):
    def __init__(self, actor, text):
        NoTargetAction.__init__(self, actor)
        self.actorMethodArgs = self.actorMethodArgs + (text,)
exec codeInterfaceForAction(Exec)

class InterpreterCapability(thing.SkillSet):
    __implements__ = (IRebuildActor, IExecActor)

    def actorActionRebuild(self):
        rebuilt = []
        for mod in sys.modules:
            try:
                rebuild.rebuild(sys.modules[mod])
            except:
                s = StringIO()
                traceback.format_exc(file = s)
                self.original.hears(s.getvalue())
            else:
                rebuilt.append(mod)
        if len(rebuilt):
            self.original.hears(utils.format(rebuilt))
        else:
            self.original.hears("No modules rebuilt successfully.")


    def actorActionExec(self, text):
        if not self.code_space.has_key('self'):
            self.code_space['self'] = self.original
        try:
            return self.runcode(text)
        except error.RealityException, re:
            self.thing.hears(re.format(self))


    def runcode(self, cmd):
        func = '$%s$' % self.name
        try:
            code = compile(cmd, func, 'eval')
        except:
            try:
                code = compile(cmd, func, 'single')
            except:
                self.original.hears("That won't compile.")
                return
        
        try:
            val = eval(code, self.code_space)
            if val is not None:
                self.original.hears(repr(val))
            else:
                self.original.hears('Okay.')
            return val
        except:
            sio = StringIO.StringIO()
            traceback.print_exc(file = sio)
            self.original.hears(sio.getvalue())



class NetworkCapability(thing.SkillSet):
    def skill_users(self, sentence):
        self.thing.hears('-' * 79)
        for i in sopera.Player.formatAllUsers(self.thing):
            self.thing.hears('%-20s' % i)


class BuilderSkills(thing.SkillSet):
    _createModules = [objects, vending]

    def skill_create(self, sentence):
        """Usage: create <type> [with <initial settings>]
        
        Create a new instance of <type> with the given initial settings
        """
        ds = sentence.directString()
        thing = findClass(ds, self._createModules)
        if thing is None:
            self.thing.hears('There is nothing by the name %s.' % ds)
            return
        
        try:
            instObj = thing.createFromSentence(self.thing, sentence)
            instObj.location = self.thing
            self.thing.hears('You create %s.  Good job.' % instObj.nounPhrase(self.thing))
        except AttributeError:
            try:
                instObj = thing()
                instObj.location = self.thing
                self.thing.hears('You create %s.  Good job.' % instObj.nounPhrase(self.thing))
            except TypeError, e:
                self.thing.hears(e)
                self.thing.hears('Cannot create %s.' % ds)


class SkillsParser(phrase.Subparser):
    def parse_grant(self, actor, text):
        """Usage: grant [<capability> to <player>]
        
        Give access to the commands in <capability> to <player>, using the
        implementation provided by <adapter>, or list all capabilities
        that can be granted.
        """
        if not len(text):
            return [GrantList(actor)]

        res = text.split(' to ', 1)
        if len(res) == 2:
            cap, target = res
            target = actor.locate(target, IGrantTarget)
            return [Grant(actor, target, cap)]


    def parse_grants(self, actor, text):
        """Usage: grants <player>
        
        List all capabilities <player> has been granted.
        """
        target = actor.locate(text, IGrantTarget)
        return [RevokeList(actor, target)]


    def parse_revoke(self, actor, text):
        """Usage: revoke <capability> from <player>

        Remove access to the commands in <capability> from <player>
        """
        res = text.split(' from ')
        if len(res) == 2:
            cap, target = res
            target = actor.locate(target, IRevokeTarget)
            return [Revoke(actor, target, cap)]
    
    
    def parse_exec(self, actor, text):
        """Usage: exec <Python source code>
        
        Run the given source.
        """
        return [Exec(actor, text)]
    
    
    def parse_rebuild(self, actor, text):
        """Usage: rebuild
        
        Rebuild all modules and instances from updated source on disk.
        """
        return [Rebuild(actor)]


phrase.registerSubparser(SkillsParser())
