# -*- test-case-name: reality.test_reality -*-

# System imports
import sys, new, types

# Twisted imports
from twisted.python.components import Interface, getAdapter, Componentized
from twisted.python.components import implements, Adapter
from twisted.python import failure

# Reality imports
import thing

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
        self.preAction()
        result = self.doAction()
        self.postAction(result)

    def preAction(self):
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
        iface = self.getInterface(itype)
        if obj is None:
            assert itype in self.allowNoneInterfaceTypes, repr(itype)
            return None
        if not isinstance(obj, Componentized):
            assert implements(obj, iface), repr((obj, iface))
            return obj
        return obj.getComponent(iface) or obj

    def getActionObjects(self):
        """Return a list of all adapters involved in this action.
        """
        return [getattr(self, x.lower()) for x in self.interfaceTypes]

    def isPlaceholder(self):
        """Returns true if I am a `placeholder' action.

        Placeholder actions are those who should be considered irrelevant in
        the case of a conflict between multiple possible meanings of an action.
        """
        i = 0
        for actobj in self.getActionObjects():
            if actobj and getattr(actobj, "temporaryAdapter", 0):
                return True
        return False

class NoTargetAction(Action):
    __metaclass__ = MetaAction
    interfaceTypes = ["Actor", "Place"]
    allowNoneInterfaceTypes = []

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
        self.place = actor.place
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
        p = self.actor.getComponent(thing.IThing)
        p.broadcastToOne(to_subject=self.formatToActor(),
                         to_other=self.formatToOther())

    def __repr__(self):
        return "<action: %s %s>"% (self.__class__, self.actor.name)

class TargetAction(NoTargetAction):
    __metaclass__ = MetaAction
    interfaceTypes = ["Actor", "Target", "Place"]
    allowNoneInterfaceTypes = []

    class ITargetDefault(Interface):
        """Default interface for targets of TYPE actions.
        """
        def preTarget(self, action):
            """Default pre-action for targets of TYPE actions.
            """
        def postTarget(self, action):
            """Default post-action for targets of TYPE actions.
            """

    def __init__(self, actor, target):
        NoTargetAction.__init__(self, actor)
        self.target = self._getComponentType(target, "Target")
        self.actorMessage = "(to actor) ", self.actor, " ", self.__class__.__name__, " ", self.target
        self.otherMessage = "(to other) ", self.actor," ", self.__class__.__name__, " ", self.target
        self.targetMessage = "(to target)", self.actor," ", self.__class__.__name__, " ", self.target

    def broadcastFormat(self):
        """
        Broadcast a successfully-done action.  This will call
        self.formatToActor(), self.formatToTarget(), and self.formatToOther()
        """
        p = self.actor.getComponent(thing.IThing)
        if self.target:
            t = self.target.getComponent(thing.IThing)
        else:
            t = None
        p.broadcastToPair(t, to_subject=self.formatToActor(),
                          to_target=self.formatToTarget(),
                          to_other=self.formatToOther())

    def doAction(self):
        getattr(self.target, "actionTarget"+self.__class__.__name__)(self)

    def formatToTarget(self):
        return self.targetMessage

    def __repr__(self):
        return "<action: %s %s %s>" % (
            str(self.actor), self.__class__,
            str(self.target))
    
class ToolAction(TargetAction):
    __metaclass__ = MetaAction
    interfaceTypes = ["Actor", "Target", "Tool", "Place"]
    allowNoneInterfaceTypes = ["Tool"]

    class IToolDefault(Interface):
        """Default interface for tools of TYPE actions.
        """
        def preTool(self, action):
            """Default pre-action for tools of TYPE actions.
            """
        def postTool(self, action):
            """Default post-action for tools of TYPE actions.
            """

    def __init__(self, actor, target, tool=None):
        TargetAction.__init__(self, actor, target)
        self.tool = self._getComponentType(tool, "Tool")

    def __repr__(self):
        return "<action: %s %s %s using %s>" % (
            str(self.actor), self.__class__,
            str(self.target), str(self.tool))

# TODO: (maybe?) have a helper Adapter class for actions which re-forwards
# getComponent to its 'original' attribute?  Should this be in t.p.components?


from twisted.python.reflect import namedModule

def unify(*classes):
    """Unify a set of similar action interfaces to be identical.

    This functionality is HIGHLY EXPERIMENTAL and may be obsoleted before it is
    ever used by the multiComponent attribute of adapters.  It is here as a
    proof of concept for automatic interface manipulation.
    """
    try:
        primary = classes[0]
        pitypes = primary.interfaceTypes
        secondary = classes[1:]
        print 'UNIFYING', classes
        newprimedict = primary.__dict__.copy()
        salist = []
        for clas in secondary:
            assert pitypes == clas.interfaceTypes, "Zow."
            for typ in pitypes:
                iclas = clas.getInterface(typ)
                iprim = primary.getInterface(typ)
                for k, v in iclas.__dict__.items():
                    if isinstance(v, types.FunctionType):
                        print 'setting'
                        print iprim, k, v
                        iprim.__dict__[k] = v
                setattr(sys.modules[iclas.__module__], iclas.__name__, iprim)
    except:
        failure.Failure().printTraceback()
    raw_input("Just making sure you see this, sir.")
