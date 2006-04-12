# -*- test-case-name: reality.test_reality -*-

# Beyond, a Portable Simulation Framework for Virtual Worlds
# Copyright (C) 2001-2002 Jason L. Asbahr
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

from twisted.python.components import Interface, getAdapter, Componentized


### Error Handling

class BeyondError(Exception):
    """Oops.  An error occurred.
    """

class DispatchException(Exception):
    """Something happened during dispatch that needed to stop it.
    """

class DispatchKeepGoing(DispatchException):
    """Dispatch should keep going!

    I decided I didn't want to handle it after all.
    """

class DispatchFailed(DispatchException):
    """Dispatch found nowhere to go to.
    """


### SimObjects

class SimObject(Componentized):
    """
    In Beyond, a thing active in the simulation domain is called a
    SimObject. Simulation elements are modeled as SimObject attributes, with
    instance variables representing the state and methods implementing the
    behavior of the simulated elements.
    
    Simulations are assembled by hierarchically organizing SimObjects in
    containment graphs, where logically general instances contain more
    logically specific instances.
    """


### Basic Actions

class IAction(Interface):
    """An action.
    """
    def performAction(self):
        """Execute this action.
        """

class MethodAction:
    """Beyond-style action, as described in the paper.
    """
    __implements__ = IAction,
    def __init__(self, method, *args, **kw):
        self.method = method
        self.args = args
        self.kw = kw

    def performAction(self):
        self.method(*self.args, **self.kw)


### NoTargetAction & TargetAction Actions

def defaultMethodName(prefix, cls):
    return prefix + cls.__name__

class INothing(Interface):
    """Null interface.

    For simplicity's sake, proper interfaces are not always required.  They
    are, however, recommended.
    """

class DispatchingAction:
    __implements__ = IAction,

    def getDispatchList(self):
        raise NotImplementedError("%s.getDispatchList" % (self.__class__,))

    def getInterface(klas, nam):
        return getattr(klas, "%sInterface"%nam)

    getInterface = classmethod(getInterface)

    def performAction(self):
        dl = self.getDispatchList()
        for interface, object, methodName, args, kw in dl:
            object = hasattr(object, 'getComponent') and object.getComponent(interface) or object
            possibleMethod = getattr(object, methodName, None)
            if callable(possibleMethod):
                try:
                    return possibleMethod(*args, **kw)
                except DispatchKeepGoing:
                    pass
        import pprint
        pprint.pprint(dl)
        raise DispatchFailed('Nobody to dispatch to!', dl)
    

class NoTargetAction(DispatchingAction):
    actionMethodName = None
    ActorInterface = INothing
    
    def __init__(self, actor):
        try:
            actor = actor.getComponent(self.ActorInterface) or actor
        except:
            pass
        self.actor = actor
        self.actorMethodArgs = ()
        self.actorMethodKwArgs = {}

    def getDispatchList(self):
        actorMethod = (self.actionMethodName or
                       defaultMethodName("actorAction", self.__class__))
        return [[self.ActorInterface, self.actor, actorMethod, self.actorMethodArgs, self.actorMethodKwArgs]]

    def __repr__(self):
        return "<action: %s %s>"% (self.__class__, self.actor.name)

class TargetAction(NoTargetAction):
    def __init__(self, actor, target):
        NoTargetAction.__init__(self, actor)
        self.target = target
        self.actorMethodArgs = (self.target,)
        self.targetMethodArgs = (self.actor,)
        self.actorMethodKwArgs = {}
        self.targetMethodKwArgs = {}        
    actionActorMethodName = None
    actionTargetMethodName = None
    TargetInterface = INothing

    def getDispatchList(self):
        actorMethod = (self.actionActorMethodName or
                       defaultMethodName("actorAction", self.__class__))
        targetMethod = (self.actionTargetMethodName or
                        defaultMethodName("targetAction", self.__class__))
        return [
            [self.ActorInterface, self.actor, actorMethod, self.actorMethodArgs,self.actorMethodKwArgs],
            [self.TargetInterface, self.target, targetMethod, self.targetMethodArgs,self.targetMethodKwArgs]]


class ToolAction(TargetAction):
    def __init__(self, actor, target, tool=None):
        TargetAction.__init__(self, actor, target)
        self.tool = tool
        self.actorMethodArgs = (self.target, self.tool)
        self.targetMethodArgs = (self.actor, self.tool)
        self.toolMethodArgs = (self.actor, self.target)
        self.toolMethodKwArgs = {}
        
    actionToolMethodName = None
    ToolInterface = INothing
    
    def __repr__(self):
        return "<action: %s %s %s using %s>" % (
            str(self.actor), self.__class__,
            str(self.target), str(self.tool))

    def getDispatchList(self):
        actorMethod = (self.actionActorMethodName or
                       defaultMethodName("actorAction", self.__class__))
        targetMethod = (self.actionTargetMethodName or
                        defaultMethodName("targetAction", self.__class__))
        toolMethod = (self.actionToolMethodName or
                      defaultMethodName("toolAction", self.__class__))
        return [[self.TargetInterface, self.target, targetMethod, self.targetMethodArgs, self.targetMethodKwArgs],
                [self.ToolInterface, self.tool, toolMethod, self.toolMethodArgs, self.toolMethodKwArgs],
                [self.ActorInterface, self.actor, actorMethod, self.actorMethodArgs, self.actorMethodKwArgs]]

### Interface Code Generation
### XXX TODO: emacs support for this

def makeInterfaceCode(className, docstring, methods):
    stmts = []; w = stmts.append
    # w("from twisted.python.components import Interface")
    w("class %s(Interface):" % className)
    w("    '''%s'''" % docstring)
    for docstring, method, args in methods:
        w("    def %s(%s):" % (method, ", ".join(args)))
        w("        '''%s'''" % docstring)
    return '\n'.join(stmts)

def codeInterfaceForNoTargetAction(intransClass):
    """I kissed her powdered lips
    """
    stmts = []; w = stmts.append
    newClassName = ("I"+intransClass.__name__ + "Actor")
    w(makeInterfaceCode(
        newClassName,
        "An actor interface for %s." % intransClass.__name__,
        [["No Docstring", (intransClass.actionMethodName or defaultMethodName("actorAction", intransClass)), ["self"]]]))
    w(intransClass.__name__ + ".ActorInterface = " + newClassName)
    return '\n'.join(stmts)
    
def codeInterfaceForTargetAction(transClass):
    """at the funeral
    """
    stmts = []; w = stmts.append
    targetClassName = ("I"+transClass.__name__ + "Target")
    actorClassName = ("I"+transClass.__name__ + "Actor")
    w(makeInterfaceCode(
        actorClassName,
        "An actor interface for %s." % transClass.__name__,
        [["No Docstring", (transClass.actionMethodName or defaultMethodName("actorAction", transClass)), ["self", "target"]]]))
    w(makeInterfaceCode(
        targetClassName,
        "The target of a %s action." % transClass.__name__,
        [["No Docstring", (transClass.actionMethodName or defaultMethodName("targetAction", transClass)), ["self", "actor"]]]))
    w(transClass.__name__ + '.ActorInterface = ' + actorClassName)
    w(transClass.__name__ + '.TargetInterface = ' + targetClassName)
    return '\n'.join(stmts)

def codeInterfaceForToolAction(transClass):
    """the taste was dry and sweet
    """
    stmts = []; w = stmts.append
    targetClassName = ("I"+transClass.__name__ + "Target")
    actorClassName = ("I"+transClass.__name__ + "Actor")
    toolClassName = ("I"+transClass.__name__ + "Tool")
    w(makeInterfaceCode(
        actorClassName,
        "An actor interface for %s." % transClass.__name__,
        [["Actor Interface", (transClass.actionActorMethodName or
                              defaultMethodName("actorAction", transClass)),
          ["self", "target", "tool"]]]))
    w(makeInterfaceCode(
        targetClassName,
        "The target of a %s action." % transClass.__name__,
        [["Target Interface", (transClass.actionTargetMethodName or
                               defaultMethodName("targetAction", transClass)),
          ["self", "actor", "tool"]]]))
    w(makeInterfaceCode(
        toolClassName,
        "The tool used for a %s action." % transClass.__name__,
        [["Tool Interface", (transClass.actionToolMethodName or
                             defaultMethodName("toolAction", transClass)),
          ["self", "actor", "target"]]]))
    w(transClass.__name__ + '.ActorInterface = ' + actorClassName)
    w(transClass.__name__ + '.TargetInterface = ' + targetClassName)
    w(transClass.__name__ + '.ToolInterface = ' + toolClassName)
    return '\n'.join(stmts)


def codeInterfaceForAction(actClass):
    if issubclass(actClass, ToolAction):
        return codeInterfaceForToolAction(actClass)
    elif issubclass(actClass, TargetAction):
        return codeInterfaceForTargetAction(actClass)
    else:
        return codeInterfaceForNoTargetAction(actClass)

### Test Fixtures


if __name__ == '__main__':
    test()
