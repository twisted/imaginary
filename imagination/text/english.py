# -*- test-case-name: imagination.test -*-

import pprint

from zope import interface
from zope.interface import Interface, implements
from twisted.python.reflect import accumulateMethods

from imagination import iimagination
from imagination.facets import Facet, IReprable, registerAdapter
from imagination.errors import Nonsense, NoSuchObject, RealityException, ActionFailed, ActionRefused, Refusal, LostThing


# English-Specific Interfaces

class INoun(Interface):
    """This interface is intended to specify a specifically English noun.
    """

class INoun(Interface):
    """An abstract concept that can be expressed in some language.

    @type name: C{str}
    @ivar name: A simple string describing this noun.
    """

    def getLanguage():
        """Return a brief string identifier of the language this concept is in.
        """

    def expressTo(observer):
        """
        Return a string or unicode object that expresses this concept in some
        language.
        """

    def describe(component, text, priority=1):
        """Describe a facet of this object with some text in my native language.
        """

    def explainTo(observer):
        """Return a long description of this object.
        """

    def knownAs(name, observer):
        """Determine whether the given name refers to this object.
        """

    def changeName(newname):
        """Change the name which refers to this object.
        """


class IThinker(Interface):
    def recognizes(name):
        """
        XXX Whether or not this thinker recognizes this name. What name??? I dunno!
        """

    def parse(text):
        """
        parse and execute a command from the thinker.
        """


# Formatting

class Noun(Facet):
    implements(INoun, IReprable)

    def __init__(self, original, name = '', description = None, unique = False):
        Facet.__init__(self, original)
        self.name = name
        self.description = description
        self.unique = unique
        original[IReprable] = name

    def describe(self, component, text, priority=1):
        if self.description is None:
            self.description = []
        for idx in xrange(len(self.description)):
            p, c, t = self.description[idx]
            if c == component:
                if text is None:
                    del self.description[idx]
                else:
                    self.description[idx] = priority, component, text
                break
        else:
            self.description.append((priority, component, text))
        self.description.sort()

    def explainTo(self, observer, component=None):
        if self.description is None:
            return ''
        return express(self.description, observer)
        #return express([t for p, c, t in self.description if (component is None)
        #                       or (c == component)], observer)

    def getLanguage(self):
        return 'english'

    def expressTo(self, observer):
        return self.nounPhrase(observer)

    def hasName(self, name):
        return name and self.name == name or [
            None for n in self.name.lower().split()
            if n.startswith(name.lower())]

    def knownAs(self, name, observer):
        # print "HELLO????"
        if IThinker(observer).recognizes(self, name):
            # print "using recognizes"
            return True
        else:
            # print "using hasName"
            return self.hasName(name)

    def changeName(self, newName):
        self.name = newName
        # TODO: broadcast a name change event?

    def article(self, observer):
        if self.unique:
            return self.definiteArticle(observer)
        else:
            return self.indefiniteArticle(observer)

    def indefiniteArticle(self, observer):
        if self.name[0].lower() in 'aeiou':
            return 'an '
        return 'a '

    def definiteArticle(self, observer):
        return 'the '

    def shortName(self, observer):
        return self.name

    def nounPhrase(self, observer):
        return (self.article(observer) + self.shortName(observer))

    def containerPreposition(self, content, observer):
        """When this object acts as a container, this is the preposition that
        objects will be in relation to it."""
        return "on"

    def containedPhrase(self, observer, containerNoun):
        # A self is container.preposition the container
        return "%s is %s %s." % (self.nounPhrase(observer),
                                 containerNoun.containerPreposition(self, observer),
                                 containerNoun.nounPhrase(observer))

    def presentPhrase(self, observer):
        # ugh: this is terrible.
        if (isinstance(self.original, things.Movable) and
            isinstance(observer, things.Movable) and
            self.original.location == observer.location):
            return "%s is here." % self.nounPhrase(observer)
        else:
            return INoun(self).containedPhrase(self)

    def heShe(self, observer):
        if self.original.gender == things.MALE:
            return 'he'
        elif self.original.gender == things.FEMALE:
            return 'she'
        else:
            return 'it'

    def himHer(self, observer):
        if self.original.gender == things.MALE:
            return 'him'
        elif self.original.gender == things.FEMALE:
            return 'her'
        else:
            return 'its'

    def hisHer(self, observer):
        if self.original.gender == things.MALE:
            return 'his'
        elif self.original.gender == things.FEMALE:
            return 'her'
        else:
            return 'its'

class Describability(Facet):
    implements(INoun)

    description = None

    def describe(*a): raise NotImplementedError

    def explainTo(self, observer):
        if self.description is not None:
            return self.description
        noun = INoun(self, default=None)
        if noun is not None:
            return noun.nounPhrase(observer)
        return "an nondescript object"



class ProperNoun(Noun):
    def indefiniteArticle(self, observer):
        return ''

    def definiteArticle(self, observer):
        return ''


class CollectiveNoun(Noun):
    implements(INoun)
    def indefiniteArticle(self, observer):
        return ''


# Errors

import random

class EException(Facet):
    implements(INoun)
    def expressTo(self, observer):
        return express(self.original.args, observer)

class ENonsense(Facet):
    implements(INoun)
    errors=["You don't think that you want to waste your time with that.",
            "There are probably better things to do with your life.",
            "You are nothing if not creative, but that creativity could be better applied to developing a more productive solution.",
            "Perhaps that's not such a good idea after all.",
            "Surely, in this world of limitless possibility, you could think of something better to do.",
            "An interesting idea...",
            "A valiant attempt.",
            "What a concept!",
            "You can't be serious."]

    def expressTo(self, observer):
        return random.choice(self.errors)

class ENoSuchObject(Facet):
    implements(INoun)
    def expressTo(self, observer):
        return express(("You don't see a %r here." % self.original.name), observer)

registerAdapter(ENonsense, Nonsense, INoun)
registerAdapter(ENoSuchObject, NoSuchObject, INoun)
for rex in RealityException, ActionFailed, ActionRefused, Refusal, LostThing:
    registerAdapter(EException, rex, INoun)

# Parsing

class Subparser:
    """A subparser is a class that implements some number of parse_<word>
    methods.  These methods will be called by the parser engine for a player.
    For example, when a player types '<word> foo', the subparser will be
    invoked (if it implements such a method) with
    subparser.parse_<word>(player, <text>), where text is the remainder of the
    sentence after '<word> '.

    the 'simpleToolParsers' attribute is a dictionary of {"verb_name":
    ToolActionClass}.

    """
    simpleToolParsers = {}
    simpleTargetParsers = {}
    def getParserBits(self):
        dict = {}
        accumulateMethods(self, dict, "parse_")
        for parseWord, actionClass in self.simpleToolParsers.items():
            dict[parseWord] = SimpleToolParser(actionClass).parse
        for parseWord, actionClass in self.simpleTargetParsers.items():
            dict[parseWord] = SimpleTargetParser(actionClass).parse
        items = dict.items()
        return items

class SimpleTargetParser:

    def __init__(self, actionClass):
        self.actionClass = actionClass

    def parse(self, player, text):
        actor = self.actionClass.getInterface("Actor")(player)
        if actor is None:
            return []
        return [self.actionClass(actor, text)]


class SimpleToolParser:

    def __init__(self, actionClass):
        self.actionClass = actionClass

    def parse(self, player, text):
        return simpleToolAction(player, self.actionClass, text)


class VerbParserEngine:

    def __init__(self):
        self.subparsers = {}
        self.spitems = self.subparsers.items()

    def registerSubparser(self, subparser):
        bits = subparser.getParserBits()
        for name, method in bits:
            name = name.lower().replace("_", " ")
            self.subparsers.setdefault(name, []).append(method)
        self.spitems = self.subparsers.items()

    def parseToActions(self, player, text):
        """Dispatch to all appropriate subparsers.
        """
        # note, this is slightly buggy
        # look_up shouldn't be different than look__up but the work necessary
        # to equalize them just doesn't seem worth it.
        matchtext = text.lower() #.replace(' ', '_')
        potentialActions = []
        for prefx, methods in self.spitems:
            if matchtext.startswith(prefx):
                subtext = text[len(prefx):].strip()
                for method in methods:
                    potact = method(player, subtext)
                    if potact:
                        potentialActions.extend(potact)
        return potentialActions
try:
    theParserEngine
except NameError:
    theParserEngine = VerbParserEngine()
    registerSubparser = theParserEngine.registerSubparser
    parseToActions = theParserEngine.parseToActions

class Parsing(Facet):
    implements(IThinker)
    potentialActions = None
    action = None

    def __init__(self, *args, **kwargs):
        Facet.__init__(self, *args, **kwargs)
        self.resolved = []
        self.potentialThings = []

    def recognizes(self, noun, name):
        return False


    def parse(self, text):
        """
        Parse a command.
        My return values are only for debugging purposes.
        """
        potentialActions = self.parseToActions(self.original, text)

        if not potentialActions:
            raise Nonsense("That doesn't make sense!")

        #argh, we're relying on getAmbiguities' side-effects.
        for act in potentialActions:
            act.getAmbiguities()

        potentialRealActions = [act for act in potentialActions if not act.isPlaceholder()]

        if (len(potentialRealActions) and
            (len(potentialRealActions) < len(potentialActions))):
            potentialActions = potentialRealActions

        if len(potentialActions) == 1:
            # Command was not ambiguous Action-wise
            return self._runAction(potentialActions[0])
        else:
            # More than one Action!
            return self.askForAction(potentialActions
                ).addCallback(self._runAction
                )

    def _runAction(self, action):
        # print '[][][][][][][][][][][][][][][][]'
        potentialThings = action.getAmbiguities()
        # print '][][][][][][][][][][][][][][][]['
        # print 'Lala', potentialThings

        if potentialThings:
            # It _was_ ambiguous wrt the Things involved
            return self.askForThing(potentialThings, action)
        else:
            #No ambiguities! Woohoo
            return action.performAction()

    def parseToActions(self, original, text):
        return parseToActions(original, text)

    def askForAction(self, potentialActions):
        return iimagination.IUI(self.original).presentMenu(potentialActions
            ).addCallbacks(potentialActions.__getitem__, lambda x: None)

    def askForThing(self, potentialThings, action):
        pt = potentialThings
        def getThing(result):
            thing = pt[0][1][result]
            return self.doneResolvingThing(thing, potentialThings, action)
        return iimagination.IUI(self.original).presentMenu(pt[0][1], pt[0][0]
            ).addCallbacks(getThing, lambda x: None)

    def doneResolvingThing(self, thing, potentialThings, action):
        self.resolved.append((potentialThings[0][0], thing))
        del potentialThings[0]
        if potentialThings:
            return self.askForThing(potentialThings, action)
        else:
            #RESOLVED ALL THINGS!
            for iface, thing in self.resolved:
                action.setImplementor(iface, thing)
            return action.performAction()


### Utility Functions

def rsplit1(s, sep):
    """Split on a delimiter found backwards through a string.

    Returns a 2-tuple of (before-last-sep, after-last-sep).  If sep is not
    found, it returns (s,'').
    """
    n = s.rfind(sep)
    if n == -1:
        return (s, '')
    return (s[:n].strip(), s[n+len(sep):].strip())

def _simpleToolact(player, toolActionClass, targetName, toolName):
    return [toolActionClass(player, targetName, toolName)]

def simpleToolAction(player, toolActionClass, text):
    """
    # gun is the tool, bob is the target
    1) 'shoot bob with gun'
    # still the same, though 'at' reverses the order
    2) 'shoot gun at bob'
    # the gun is the tool; north is the target.  Do I need to handle this case?
    3) 'point gun north'

    ### The action is going to have to deal properly with implicit (None)
    ### targets and tools, and locate them itself, either in the constructor or
    ### in processAction. (Some actions might not even need both tool and
    ### target)

    # implicit tool (yuck)
    4) 'shoot bob'
    # implicit _target_ (extra yuck)
    5) 'shoot gun'
    """

    actor = toolActionClass.getInterface("Actor")(player)
    if actor is None:
        return []
    if text.count(' with '):            # case #1
        bobName, gunName = rsplit1(text, ' with ')
        return _simpleToolact(player, toolActionClass, bobName, gunName)
    else:                               # case #2
        # XXX What is the use-case for ' and '?
        for splitter in (' at ', ' to ', ' from ', ' and '):
            if splitter in text:
                gunName, bobName = rsplit1(text, splitter)
                return _simpleToolact(player, toolActionClass, bobName, gunName)
    # you rolled a 9 (case #4 & 5)
    lr = []
    if toolActionClass.allowImplicitTarget:
        lr.extend(_simpleToolact(player, toolActionClass, None, text))

    lr.extend(_simpleToolact(player, toolActionClass, text, None))
    return lr

## Some utilities.

class _ExpressSeq(Facet):
    def expressTo(self, observer):
        return ''.join([INoun(x).expressTo(observer) for x in self.original])

class _ExpressNothing(Facet):
    def expressTo(self, observer):
        return ''

class _ExpressYourself(Facet):
    def expressTo(self, observer):
        return self.original

registerAdapter(_ExpressSeq, tuple, INoun)
registerAdapter(_ExpressSeq, list, INoun)
registerAdapter(_ExpressNothing, type(None), INoun)
registerAdapter(_ExpressYourself, str, INoun)

def express(tup, obs, iface=INoun):
    return iface(tup).expressTo(obs)
