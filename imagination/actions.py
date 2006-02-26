# -*- test-case-name: imagination.test -*-
import sys, new, types
# Twisted imports
from zope.interface import Interface, implements, interface
from imagination.facets import Facet, isid
from twisted.python import failure, log
from twisted.python.reflect import accumulateClassList, qual

from imagination import simulacrum
from imagination import errors
from imagination.text import english

class MetaAction(type):
    """
    I am a metaclass that does nothing but tell Action when it's been
    subclassed.
    """
    def __init__(self, name, bases, dict):
        super(MetaAction, self).__init__(name, bases, dict)
        if '__metaclass__' not in dict:
            self.subclassed()

def _funcopy(f, name=None, globs=None):
    if name is None:
        name = f.func_name
    if globs is None:
        globs = f.func_globals
    code = f.func_code
    return new.function(code, globs, name)

def _interfacecopy(typ, name=None, bases=None, dict=None, methodPostfix=None):
    """Interface copier.
    """
    if name is None:
        name = typ.__name__
    if bases is None:
        bases = typ.__bases__
    if dict is None:
        dict = typ.__dict__.copy()
        doc = dict['__doc__'].replace("TYPE", methodPostfix)
        attrs = typ._InterfaceClass__attrs
        if methodPostfix:
            for k, v in attrs.items():
                if not isinstance(v, types.FunctionType):
                    continue
                del dict[k]
                fc = _funcopy(v, v.func_name+methodPostfix)
                fc.__doc__ = fc.__doc__.replace("TYPE", methodPostfix)
                dict[k+methodPostfix] = fc
                # TODO: perhaps some criterea for methods whose names not to
                # munge?
    return interface.InterfaceClass(name, bases, attrs, __doc__=doc)


def checkIdentity(action, interfaceTypes):
    """Verify that the identity of the interface targets of an action object are as
    expected.  In particular make sure that no interface targets are None when
    they are not supposed to be, and verify that the objects are still
    reachable through a scene graph query as they were when collected by the
    parser.
    """
    for iType in interfaceTypes:
        ourO = getattr(action, iType.lower())
        iName = getattr(action, iType.lower()+"Name")
        potentialOs = action.collectThings(iName, action.getInterface(iType))
        potentialOs = list(potentialOs)
        if ourO is None and iType in action.allowNoneInterfaceTypes:
            continue
        for radius, potentialO in potentialOs:
            if ourO is potentialO:
                break
        else:
            raise errors.LostThing()


class Action(object):
    """Abstract representation of a potential or taken action.

    I am an action that the user has expressed an intent to commit, and I
    contain all the appropriate logic to determine whether I'm plausible,
    possible, and allowed, and then to execute.

    At the class level, I, and my subclasses, specify a list of 'interface
    types', which is a list of slots (AKA 'interface targets') which specify
    interfaces to automatically create and adapt attributes of myself to.  For
    example, an interfaceTypes list of ['foo', 'bar'], on an Action subclass
    named Transmogrify will result in the class statement defining Transmogrify
    to also define the interfaces ITransmogrifyFoo and ITransmogrifyBar and for
    all Transmogrify instances to indicate a 'foo' and a 'bar' that will be
    involved in the action.

    Actual game actions should probably subclass the utility subclasses
    NoTargetAction, TargetAction, and ToolAction in order to provide some
    useful interface targets and verification behavior.  They provide interface
    targets such as 'place', the area where the action is happening, 'actor',
    the actor performing the action, etc.

    """

    allowNoneInterfaceTypes = []
    __metaclass__ = MetaAction

    def subclassed(klass):
        mod = sys.modules[klass.__module__]
        for itype in klass.interfaceTypes:
            iname = "I%s%s" % (klass.__name__, itype)
            if getattr(mod, iname, None):
                continue
            idefault = getattr(klass, "I%sDefault" % itype)
            iface = _interfacecopy(idefault, iname, methodPostfix=klass.__name__)
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
            return result
        # XXX WRONG
        #self.actor.store.transact(_)
        return _()

    def checkRefusals(self):
        for ifname in self.interfaceTypes:
            o = getattr(self, ifname.lower())
            if isinstance(o, Refusal):
                raise errors.ActionRefused(o.whyNot)

    def checkIdentity(self):
        """
        Verify the identity of my action slots.  This, the default
        implementation, always succeeds, but subclasses may wish to use the
        'checkIdentity' utility function to verify that all interface targets
        are still accessible as they were at parse time.
        """

    def preAction(self):
        """The 'pre' action phase.  Check several things before proceeding with the
        action:

        - Make sure that none of the interface slots required by this action
          are a Refusal.  If so, raise an ActionRefused to indicate the Refusal
          to the user sensibly.

        - Verify that the identity of all action target slots are still
          reachable as they were at the time of action parsing.

        - Run all 'pre' action phase hooks, logging any errors, and tracking
          all errors.  If any errors were encountered, raise the first error as
          the reason for not proceeding.

        Note that _all_ 'pre' phase hooks will be run, even if one encounters
        an error.  This is explicitly done to avoid creating a dependency
        between different 'pre' phase hooks and to avoid creating dependencies
        upon their execution order which, while deterministic, will often be
        surprising in unexpected circumstances.  Please keep in mind when
        writing 'pre' phase hooks that the action is not necessarily happening
        yet - the hooks should just check to verify that it _can_ happen.
        """
        self.checkRefusals()
        self.checkIdentity()
        l = []
        def handle(error):
            log.err(e)
            l.append(e)
        self.runActionPhaseHooks(handle, "pre")
        if l:
            raise l[0]

    def postAction(self, result):
        """
        The 'post' action phase.  The action completed successfully, with a
        result.  Run the 'post' action phase hooks with the result of the 'do'
        phase as an argument.  Log any errors.
        """
        self.runActionPhaseHooks(log.err, "post", result)

    def runActionPhaseHooks(self, errorHandler, phase, *args, **kw):
        """
        Call a set of methods based on the phase and interfaces available for this
        action.

        This method is used by action phase methods such as preAction() and
        postAction() in order to invoke hook methods.  For each interface type
        in C{self.interfaceTypes}, I will get the attribute from myself
        corresponding to that interface, then look up a method on that object
        corresponding to the phase.  For example, if I am a TargetAction called
        Foo, I have the interfaceTypes list of 'Actor', 'Target', and 'Place',
        in that order.  In that case, this method called as
        runActionPhaseHooks(log.err, 'pre', 1, 2, 3) is similar to the
        following code::

            self.actor.preActorFoo(1, 2, 3)
            self.target.preTargetFoo(1, 2, 3)
            self.place.prePlaceFoo(1, 2, 3)

        The difference is in error handling.  If Raise is set, the first
        exception encountered is re-raised after all methods have been called.
        If not, exceptions are logged.

        @param phase: a string, the name of a phase, currently only either
        'pre' or 'post'.

        @param args: arguments to be passed to each hook.

        @param kw: keyword arguments to be passed to each hook.

        """
        cn = self.__class__.__name__
        for ifname in self.interfaceTypes:
            o = getattr(self, ifname.lower())
            mname = "%s%s%s" % (phase, ifname, cn)
            meth = getattr(o, mname, None)
            if meth:
                try:
                    meth(self, *args, **kw)
                except:
                    f = failure.Failure()
                    errorHandler(f)

    def doAction(self):
        raise NotImplementedError(qual(self.__class__) + ".doAction")

    def _getComponentType(self, obj, itype):
        if isinstance(obj, Refusal):
            return obj
        iface = self.getInterface(itype)
        if obj is None:
            assert itype in self.allowNoneInterfaceTypes, repr(itype)
            return None
        return iface(obj)

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
            if isinstance(actobj, Refusal):
                #print self, 'placeholder because', itype, ': %s' % (
                #    english.express(actobj.whyNot, self.actor))
                return True
            if getattr(actobj, "temporaryAdapter", False):
                #print self, 'placeholder because', itype, 'was temporary'
                return True
        return False


class NoTargetAction(Action):
    __metaclass__ = MetaAction
    implements(english.INoun)
    interfaceTypes = ["Actor", "Place"]
    allowNoneInterfaceTypes = ["Place"]
    onlyBroadcastToActor = False

    class IActorDefault(Interface):
        """Default interface for actor doing TYPE actions.
        """
        def preActor(action):
            """Default pre-action for actor doing TYPE actions.
            """
        def postActor(action):
            """Default post-action for actor doing TYPE actions.
            """

    class IPlaceDefault(Interface):
        """Default interface for place where the TYPE action happens.
        """
        def prePlace(action):
            """Default pre-action for place of TYPE actions.
            """
        def postPlace(action):
            """Default post-action for place of TYPE actions.
            """

    def __init__(self, actor):
        self.actor = self._getComponentType(actor, "Actor")
        self.place = None

    def expressTo(self, other):
        if isid(other, self.actor):
            txt = self.formatToActor()
        else:
            txt = self.formatToOther()
        return english.express(txt, other)

    def collectThings(self, iName, iface):
        """
        Search the graph for relevant objects (tools, targets, what have you).

        YOU WILL PROBABLY WANT TO OVERRIDE THIS. The default is to
        just find all objects named iName within radius 2.
        """
        return simulacrum.lookFor(self.actor, iName, iface, 2)

    def getPotentialThings(self, iName, iType):
        if not iName and iType in self.allowNoneInterfaceTypes:
            # print '@@@@ No name and none allowed for', iType, 'so returning nothing'
            return []
        return [x[1] for x in self.collectThings(iName, self.getInterface(iType))]

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
                potentials = list(self.getPotentialThings(iName, iType))
                # filter for refusals --
                # XXX TODO this should really be in the ambiguity selector
                # (english.py) because you need to be able to explicitly select
                # a refusal sometimes (to see why it is that you're not allowed
                # to do something...)
                if len(potentials) > 1:
                    noRefusalPotentials = [potential for potential in potentials
                                           if not isinstance(potential,
                                                             Refusal)]
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
                if iType in self.allowNoneInterfaceTypes and self.targetName == '':
                    self.setImplementor(iType, None)
                else:
                    self.setImplementor(iType,
                                        Refusal(None,
                                                self.whyCantFind(iType, iName)))
            else:
                ambig.append((iType, potentials))
        return ambig


    def whyCantFind(self, iType, iName):
        # XXX - This needs to be made more specific for different kinds of
        # refusals.  For example, "throw foo at bar" could fail because
        # there is no foo here, or because foo does not implement
        # IThrowActionTool or because bar does not implement IThrowActionTarget
        return "You don't see a %r here." % iName


    def getAmbiguousDescription(self):
        """
        Get a string that describes this Action, perhaps ambiguously:
        i.e., some of the objects involved may not be known yet.
        """
        return self.__class__.__name__


    def setImplementor(self, iType, obj):
        """Set the target for a particular interface on this action.  This is really
        just a 'setattr', but it is the convention to use it to set attributes
        in the interfaceTypes list for an action.
        """
        assert iType in self.interfaceTypes
        setattr(self, iType.lower(), obj)


    def getImplementor(self, iType):
        """Get the target for a particular interface from this action.  This is really
        just a 'getattr', but it is the convention to use it to set attributes
        in the interfaceTypes list for an action.
        """
        assert iType in self.interfaceTypes
        return getattr(self, iType.lower(), None)


    def doAction(self):
        raise NotImplementedError()

    def formatToTarget(self):
        return self.targetMessage

    def expressTo(self, other):
        if isid(other, self.actor):
            txt = self.formatToActor()
        elif isid(o, self.target):
            txt = self.formatToTarget()
        else:
            txt = self.formatToOther()
        return english.express(txt, other)


    def getAmbiguousDescription(self):
        return "%s %s" % (self.__class__.__name__, self.targetName)



class TargetAction(NoTargetAction):
    __metaclass__ = MetaAction
    interfaceTypes = ["Actor", "Target", "Place"]
    allowNoneInterfaceTypes = ["Place"]
    allowImplicitTarget = 0

    class ITargetDefault(Interface):
        """Default interface for targets of TYPE actions.
        """
        def preTarget(action):
            """Default pre-action for targets of TYPE actions.
            """
        def postTarget(action):
            """Default post-action for targets of TYPE actions.
            """

    def __init__(self, actor, targetName):
        NoTargetAction.__init__(self, actor)
        self.targetName = targetName


    def doAction(self):
        raise NotImplementedError()

    def checkIdentity(self):
        return checkIdentity(self, ['Target'])

    def formatToTarget(self):
        return self.targetMessage

    def expressTo(self, other):
        if isid(other, self.actor):
            txt = self.formatToActor()
        elif isid(other, self.target):
            txt = self.formatToTarget()
        else:
            txt = self.formatToOther()
        return english.express(txt, other)


    def getAmbiguousDescription(self):
        return "%s %s" % (self.__class__.__name__, self.targetName)




class ToolAction(TargetAction):
    __metaclass__ = MetaAction
    interfaceTypes = ["Actor", "Target", "Tool", "Place"]
    allowNoneInterfaceTypes = ["Tool", "Place"]

    class IToolDefault(Interface):
        """Default interface for tools of TYPE actions.
        """
        def preTool(action):
            """Default pre-action for tools of TYPE actions.
            """
        def postTool(action):
            """Default post-action for tools of TYPE actions.
            """

    def __init__(self, actor, targetName, toolName=None):
        TargetAction.__init__(self, actor, targetName)
        self.toolName = toolName

    def checkIdentity(self):
        return checkIdentity(self, ['Target', 'Tool'])

    def getAmbiguousDescription(self):
        return "%s %r with %r" % (self.__class__.__name__, self.targetName, self.toolName)



class Refusal:
    """
    When I ask for implementors of an interface, I can get one of three
    answers:

      - Yes, I implement that - an implementor of the interface.
      - No, I don't implement that - no result.
      - I might implement that, but in any event you can't access it for the
        following reason...

    The first two are obvious: collect / don't collect in collectImplementors.
    However, when one wants to refuse an interface in the general case, an
    interface that the system in question may not even know about, this is the
    object that should be returned.

    This allows us to to implement the following sequence, without having
    portability intimately aware of INeebleTarget ::

        > LOOK
        [ Contrived Example ]
        There is a glass box here.  It is closed.
          The glass box contains:
            - a gurfle
            - a smoodle
        > NEEB GURFLE
        You can't neeble that: The gurfle is in a closed box.
    """

    def __init__(self, implementor, whyNot):
        """Create a Refusal.

        I take an implementor and a reason why that implementor is not
        appropriate.  The implementor, in addition to having a XXX
        glyph got distracted by shininess.
        """
        self.implementor = implementor
        self.whyNot = whyNot
