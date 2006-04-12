# -*- test-case-name: reality.test_reality -*-

# System imports
import sys, new, types

# Twisted imports
from twisted.python.components import Interface, getAdapter, Componentized
from twisted.python.components import implements, Adapter
from twisted.python import failure

# Reality imports
from reality import things
from reality.text import common, english


### NoTargetAction & TargetAction Actions

class MetaAction(type):
    """
    I am a metaclass that does nothing but tell Action when it's been
    subclassed.
    """
    def __init__(self, name, bases, dict):
        super(MetaAction, self).__init__(name, bases, dict)
        if not dict.has_key("__metaclass__"):
            self.subclassed()

def _funcopy(f, name=None, globs=None):
    if name is None:
        name = f.func_name
    if globs is None:
        globs = f.func_globals
    code = f.func_code
    return new.function(code, globs, name)

def _typecopy(typ, name=None, bases=None, dict=None, methodPostfix=None):
    """Type copier.
    """
    if name is None:
        name = typ.__name__
    if bases is None:
        bases = typ.__bases__
    if dict is None:
        dict = typ.__dict__.copy()
        dict['__doc__'] = dict['__doc__'].replace("TYPE", methodPostfix)
        if methodPostfix:
            for k, v in dict.items():
                if not isinstance(v, types.FunctionType):
                    continue
                del dict[k]
                fc = _funcopy(v, v.func_name+methodPostfix)
                fc.__doc__ = fc.__doc__.replace("TYPE", methodPostfix)
                dict[k+methodPostfix] = fc
                # TODO: perhaps some criterea for methods whose names not to
                # munge?
    return new.classobj(name, bases, dict)

from twisted.python.reflect import accumulateClassList, qual

class _TruthAccumulator:
    first = 1
    def accum(self, this, last):
        if self.first:
            self.first = 0
            return this
        return this and last

class Action(object):
    """Action class
    """
    __metaclass__ = MetaAction
    def subclassed(klass):
        mod = sys.modules[klass.__module__]
        for itype in klass.interfaceTypes:
            iname = "I%s%s" % (klass.__name__, itype)
            if getattr(mod, iname, None):
                continue
            idefault = getattr(klass, "I%sDefault" % itype)
            iface = _typecopy(idefault, iname, methodPostfix=klass.__name__)
            iface.__module__ = klass.__module__
            setattr(mod, iname, iface)
    subclassed = classmethod(subclassed)


    def getInterface(klass, itype):
        assert itype in klass.interfaceTypes, repr((itype, klass.interfaceTypes))
        mod = sys.modules[klass.__module__]
        return getattr(mod, "I%s%s" % (klass.__name__, itype))

    def getAllInterfaces(klass):
        return [klass.getInterface(itype) for itype in klass.interfaceTypes]

    getAllInterfaces = classmethod(getAllInterfaces)
    getInterface = classmethod(getInterface)

    def performAction(self):
        def _():
            self.preAction()
            result = self.doAction()
            self.postAction(result)
        # HACK: the actor may not always have the same store as everyone else...?
        things.IThing(self.actor).store.transact(_)
        
    def checkRefusals(self):
        from reality.errors import ActionRefused
        for ifname in self.interfaceTypes:
            o = getattr(self, ifname.lower())
            if isinstance(o, things.Refusal):
                raise ActionRefused(o.whyNot)

    def preAction(self):
        self.checkRefusals()
        l = []
        truth = self.interfacePrefixMethods("pre", _TruthAccumulator().accum,
                                            1, erraccum=l.append)
        if l:
            raise l[0].value
        return truth
        
    def postAction(self, result):
        self.interfacePrefixMethods("post", args=(result,))

    def interfacePrefixMethods(self, prefix, accum=lambda a,b: None, default=None, args=(), erraccum=lambda e: None):
        cn = self.__class__.__name__
        result = None
        for ifname in self.interfaceTypes:
            o = getattr(self, ifname.lower())
            mname = "%s%s%s" % (prefix, ifname, cn)
            meth = getattr(o, mname, None)
            if meth:
                try:
                    val = meth(self, *args)
                except:
                    val = erraccum(failure.Failure())
            else:
                # print "%s doesn't *actually* implement %s (from %s)" % (qual(o.__class__), mname, qual(self.getInterface(ifname)))
                val = default
            result = accum(val, result)
        return result

    def doAction(self):
        raise NotImplementedError(qual(self.__class__)+".doAction")

    def _getComponentType(self, obj, itype):
        if isinstance(obj, things.Refusal):
            return obj
        iface = self.getInterface(itype)
        if obj is None:
            assert itype in self.allowNoneInterfaceTypes, repr(itype)
            return None
        if not isinstance(obj, Componentized):
            assert implements(obj, iface), repr((obj, iface))
            return obj
        comp = obj.getComponent(iface)
        assert comp, "Component for %s not found on %s." % (iface, obj)
        return comp

    def isPlaceholder(self):
        """Returns true if I am a `placeholder' action.

        Placeholder actions are those who should be considered irrelevant in
        the case of a conflict between multiple possible meanings of an action.
        """
        i = 0
        for itype, actobj in [(x, getattr(self, x.lower(), None))
                              for x in self.interfaceTypes]:
            if actobj is None:
                if itype not in self.allowNoneInterfaceTypes:
                    #print self, 'placeholder because', itype, 'was None'
                    return True
                else:
                    continue
            if isinstance(actobj, things.Refusal):
                #print self, 'placeholder because', itype, ': %s' % (
                #    common.express(actobj.whyNot, self.actor))
                return True
            if getattr(actobj, "temporaryAdapter", False):
                #print self, 'placeholder because', itype, 'was temporary'
                return True
        return False

class NoTargetAction(Action):
    __metaclass__ = MetaAction
    __implements__ = common.IConcept
    interfaceTypes = ["Actor", "Place"]
    allowNoneInterfaceTypes = ["Place"]
    onlyBroadcastToActor = False

    class IActorDefault(Interface):
        """Default interface for actor doing TYPE actions.
        """
        def preActor(self, action):
            """Default pre-action for actor doing TYPE actions.
            """
        def postActor(self, action):
            """Default post-action for actor doing TYPE actions.
            """

    class IPlaceDefault(Interface):
        """Default interface for place where the TYPE action happens.
        """
        def prePlace(self, action):
            """Default pre-action for place of TYPE actions.
            """
        def postPlace(self, action):
            """Default post-action for place of TYPE actions.
            """

    def __init__(self, actor):
        self.actor = self._getComponentType(actor, "Actor")
        self.place = None
        self.actorMessage = "(to actor) ", self.actor, " ", self.__class__.__name__
        self.otherMessage = "(to other) ", self.actor," ", self.__class__.__name__

    def postAction(self, result):
        Action.postAction(self, result)
        self.broadcastFormat()

    def formatToActor(self):
        return self.actorMessage

    def formatToOther(self):
        return self.otherMessage

    def broadcastFormat(self):
        """
        Broadcast a successfully-done action.  This will call
        self.formatToActor(), self.formatToTarget(), and self.formatToOther()
        """
        evt = self.toEvent()
        if self.onlyBroadcastToActor:
            comp = self.actor.getComponent(things.IEventReceiver)
            if comp is not None:
                comp.eventReceived(self.actor, evt)
        else:
            things.IThing(self.actor).emitEvent(evt)

    def toEvent(self):
        return self

    def expressTo(self, other):
        o = other.getComponent(things.IThing)
        a = self.actor.getComponent(things.IThing)
        if o is a:
            txt = self.formatToActor()
        else:
            txt = self.formatToOther()
        return common.express(txt, other)

    def getPotentialAmbiguities(self, iName, iType):
        return things.IInterfaceForwarder(self.actor).lookFor(iName, self.getInterface(iType))

    def getAmbiguities(self):
        """Get a list of interface implementors I'm not sure about.

        Returns a list of 2-tuples of the form:
            (iType, [impl, impl, impl])

        where iType is an 'interface type' string, something like 'Actor' or
        'Tool' or 'Target', and impl is an implementor of the given interface
        or a Refusal.
        """
        ambig = []
        for iType in self.interfaceTypes:
            if self.getImplementor(iType) or iType == 'Place':
                continue
            iName = getattr(self, iType.lower()+"Name")
            o = getattr(self, "potential"+iType+"s", None)
            if o is None:
                potentials = self.getPotentialAmbiguities(iName, iType)
                # filter for refusals --
                # XXX TODO this should really be in the ambiguity selector
                # (english.py) because you need to be able to explicitly select
                # a refusal sometimes (to see why it is that you're not allowed
                # to do something...)
                if len(potentials) > 1:
                    noRefusalPotentials = [potential for potential in potentials
                                           if not isinstance(potential,
                                                             things.Refusal)]
                    if len(noRefusalPotentials) == 0:
                        potentials = [potentials[0]]
                    else:
                        potentials = noRefusalPotentials
                setattr(self, 'potential'+iType+'s', potentials)
            else:
                potentials = o
            if len(potentials) == 1:
                self.setImplementor(iType, potentials[0])
            elif len(potentials) == 0:
                if iType in self.allowNoneInterfaceTypes:
                    self.setImplementor(iType, None)
                else:
                    self.setImplementor(iType,
                                        things.Refusal(None,
                                                       self.whyCantFind(iType, iName)))
            else:
                ambig.append((iType, potentials))
        return ambig

    def whyCantFind(self, iType, iName):
        return "You don't see a %r here." % iName

    def getAmbiguousDescription(self):
        """
        Get a string that describes this Action, perhaps ambiguously:
        i.e., some of the objects invvolved may not be known yet.
        """
        return self.__class__.__name__

    def setImplementor(self, iType, obj):
        setattr(self, iType.lower(), obj)

    def getImplementor(self, iType):
        return getattr(self, iType.lower(), None)

##     def __repr__(self):
##         return "<action: %s %s>"% (self.__class__, self.actor.name)

class TargetAction(NoTargetAction):
    __metaclass__ = MetaAction
    interfaceTypes = ["Actor", "Target", "Place"]
    allowNoneInterfaceTypes = ["Place"]
    allowImplicitTarget = 0

    class ITargetDefault(Interface):
        """Default interface for targets of TYPE actions.
        """
        def preTarget(self, action):
            """Default pre-action for targets of TYPE actions.
            """
        def postTarget(self, action):
            """Default post-action for targets of TYPE actions.
            """

    def __init__(self, actor, targetName):
        NoTargetAction.__init__(self, actor)
        self.targetName = targetName

    def preAction(self):
        self.actorMessage = "(to actor) ", self.actor, " ", self.__class__.__name__, " ", self.target
        self.otherMessage = "(to other) ", self.actor," ", self.__class__.__name__, " ", self.target
        self.targetMessage = "(to target)", self.actor," ", self.__class__.__name__, " ", self.target
        NoTargetAction.preAction(self)

    def doAction(self):
        raise NotImplementedError()

    def formatToTarget(self):
        return self.targetMessage

    def expressTo(self, other):
        o = other.getComponent(things.IThing)
        a = self.actor.getComponent(things.IThing)
        t = self.target.getComponent(things.IThing)
        if o is a:
            txt = self.formatToActor()
        elif o is t:
            txt = self.formatToTarget()
        else:
            txt = self.formatToOther()
        return common.express(txt, other)

    
    def getAmbiguousDescription(self):
        return "%s %s" % (self.__class__.__name__, self.targetName)

##     def __repr__(self):
##         if hasattr(self, 'target'):
##             t = self.target
##         else:
##             t = self.targetName
        
##         return "<action: %s %s %s>" % (
##             str(self.actor), self.__class__, t)


class ToolAction(TargetAction):
    __metaclass__ = MetaAction
    interfaceTypes = ["Actor", "Target", "Tool", "Place"]
    allowNoneInterfaceTypes = ["Tool", "Place"]

    class IToolDefault(Interface):
        """Default interface for tools of TYPE actions.
        """
        def preTool(self, action):
            """Default pre-action for tools of TYPE actions.
            """
        def postTool(self, action):
            """Default post-action for tools of TYPE actions.
            """

    def __init__(self, actor, targetName, toolName=None):
        TargetAction.__init__(self, actor, targetName)
        self.toolName = toolName

    def getAmbiguousDescription(self):
        return "%s %r with %r" % (self.__class__.__name__, self.targetName, self.toolName)

##     def __repr__(self):
##         if hasattr(self, 'target'):
##             targ = str(self.target)
##         else:
##             targ = self.targetName

##         if hasattr(self, 'tool'):
##             tool = str(self.tool)
##         else:
##             tool = self.toolName

##         return "<action: %s %s %s using %s>" % (
##             str(self.actor), self.__class__, targ, tool)
        


