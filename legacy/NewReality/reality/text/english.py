# -*- test-case-name: reality.test_reality -*-

from twisted.python import components
from twisted.python.components import Interface, registerAdapter, implements, Adapter
from twisted.python.reflect import accumulateMethods


from reality import things
from reality.text import common
from reality.errors import Nonsense, RealityException, NoSuchObject

# English-Specific Interfaces

class INoun(components.Interface):
    """This interface is intended to specify a specifically English noun.
    """

class IThinker(components.Interface):
    pass


# Formatting

class Noun(components.Adapter):
    unique = 0
    name = ''
    __implements__ = INoun, common.INoun, common.IConcept, common.IDescribeable
    description = None

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
        return common.express([t for p, c, t in self.description if (component is None)
                               or (c == component)], observer)

    def getLanguage(self):
        return 'english'

    def expressTo(self, observer):
        return self.nounPhrase(observer)

    def hasName(self, name):
        return name and self.name.lower().find(name.lower()) != -1

    def knownAs(self, name, observer):
        if IThinker(observer).recognizes(self, name):
            return True
        else:
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

components.registerAdapter(Noun, things.Thing, common.INoun)
components.registerAdapter(Noun, things.Thing, common.IDescribeable)
components.registerAdapter(Noun, things.Thing, INoun)

class ProperNoun(Noun):
    def indefiniteArticle(self, observer):
        return ''

    def definiteArticle(self, observer):
        return ''

components.registerAdapter(ProperNoun, things.Actor, common.INoun)
components.registerAdapter(ProperNoun, things.Actor, INoun)

class CollectiveNoun(Noun):
    __implements__ = common.IConcept, common.INoun, INoun
    def indefiniteArticle(self, observer):
        return ''


# Errors

import random

class EException(components.Adapter):
    __implements__ = common.IConcept
    def expressTo(self, observer):
        return common.express(self.original.args, observer)

class ENonsense(components.Adapter):
    __implements__ = common.IConcept
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

class ENoSuchObject(components.Adapter):
    __implements__ = common.IConcept
    def expressTo(self, observer):
        return common.express(("You don't see a %r here." % self.original.name), observer)

components.registerAdapter(ENonsense, Nonsense, common.IConcept)
components.registerAdapter(EException, RealityException, common.IConcept)
components.registerAdapter(ENoSuchObject, NoSuchObject, common.IConcept)

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
        actor = player.getComponent(self.actionClass.getInterface("Actor"))
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

class Parsing(Adapter):
    __implements__ = IThinker, common.IThinker
    potentialActions = None
    action = None

    def __init__(self, *args, **kwargs):
        Adapter.__init__(self, *args, **kwargs)
        self.resolved = []
        self.ambigs = []

    def recognizes(self, noun, name):
        return False


    def parse(self, text):
        """
        Parse a command.
        My return values are only for debugging purposes.
        """

        # Oh ho ho! You want funcalls, I'll give you funcalls.

        ## States
        #
        # 1. Choosing from a list of Actions
        #   : input must be a number
        # 2. Choosing from a list of Things involved with an action
        #   : input must be a number or a name
        # 3. Parsing Action
        #
        # If 1 or 2 is invalid, then 3 happens
        #

        ## 2: An Action has already been selected, but not disambiguated.
        if self.ambigs:
            return self.parseResolveThing(text)

        ## 1: A command has been typed, but it resulted in more than one Action
        if self.potentialActions:
            return self.parseResolveAction(text)

        return self.parseAction(text)



    def parseAction(self, text):

        potentialActions = parseToActions(self.original, text)

        if not potentialActions:
            raise Nonsense()

        #argh, we're relying on getAmbiguities' side-effects.
        for act in potentialActions:
            act.getAmbiguities()

        potentialRealActions = [act for act in potentialActions if not act.isPlaceholder()]

        if (len(potentialRealActions) and
            (len(potentialRealActions) < len(potentialActions))):
            potentialActions = potentialRealActions


        if len(potentialActions) == 1:
            # Command was not ambiguous Action-wise
            
            self.action = action = potentialActions[0]

            self.ambigs = action.getAmbiguities()

            if self.ambigs:
                # It _was_ ambiguous wrt the Things involved
                return self.askForThing()
            else:
                #No ambiguities! Woohoo
                return action.performAction()

        # More than one Action!
        self.potentialActions = potentialActions
        return self.askForAction()


    def parseResolveAction(self, text):
        # The user already entered some text that might have been an
        # action.  Let's see if they're selecting a choice from the list of
        # actions that were presented.
        try:
            val = int(text)
        except ValueError:
            #Not a number. Give up.
            self.potentialActions = None
            self.parseAction(text)
        else:
            try:
                potentialAction = self.potentialActions[val - 1]
            except IndexError:
                #Invalid number! Ask again.
                return self.askForAction()
            self.potentialActions = None
            potentialAction.performAction()


    def askForAction(self):
        return things.IThing(self.original).emitEvent(ActionMenu(self.potentialActions), intensity=1)

    def askForThing(self):
        return things.IThing(self.original).emitEvent(ThingMenu(self.ambigs[0]), intensity=1)


    def doneResolvingThing(self, thing):
        self.resolved.append((self.ambigs[0][0], thing))
        del self.ambigs[0]
        if self.ambigs:
            self.askForThing()
        else:
            #RESOLVED ALL THINGS!
            for iface, thing in self.resolved:
                self.action.setImplementor(iface, thing)
            self.action.performAction()
            

    def parseResolveThing(self, text):

        #We've already given a menu for disambiguating a particular
        #thing involved with an Action.
        
        ambig = self.ambigs[0]
        #Did they answer it with a number?
        try:
            val = int(text)
            try:
                thing = ambig[1][val - 1]
            except IndexError:
                #That number wasn't listed! Ask again.
                self.askForThing()
                return

            else:
                return self.doneResolvingThing(thing)
                
        except ValueError:

            #Non-number. Maybe they typed out a more accurate name?
            
            val = text
            potentialThings = [thing for thing in ambig[1] if common.INoun(thing).knownAs(val, self.getComponent(things.IThing))]

            if len(potentialThings) == 1:
                #Woohoo!
                return self.doneResolvingThing(potentialThings[0])

            elif len(potentialThings) > 1:
                #The name matched the things involved, but wasn't accurate enough.
                #Ask again.
                self.ambigs[0] = (text, potentialThings) # s/text/self.ambigs[0][0]/ ?
                self.askForThing()
                return

            else:

                #It wasn't a relevant thing at all. Maybe they just
                #ignored the menu and wanted to do something
                #completely different.  Parse it as an action.

                self.ambigs = None
                self.parseAction(text)


components.registerAdapter(Parsing, things.Actor, IThinker)
components.registerAdapter(Parsing, things.Actor, common.IThinker)


class ActionMenu:
    __implements__ = common.IConcept
    def __init__(self, actions):
        self.actions = actions

    def expressTo(self, observer):
        i = 1
        l = []
        for a in self.actions:
            l.append('%s: %s' % (i, a.getAmbiguousDescription()))
            i += 1
        return '\n'.join(l)


class ThingMenu:
    __implements__ = common.IConcept
    
    def __init__(self, ambig):
        self.ambig = ambig

    def expressTo(self, observer):
        ambig = self.ambig
        l = ["Which %s?" % ambig[0]]
        i = 1
        for thing in ambig[1]:
            l.append("%s: %s" % (i, common.INoun(thing).name))
            i += 1
        return '\n'.join(l)


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
    actor = player.getComponent(toolActionClass.getInterface("Actor"))
    if actor is None:
        return []
    if text.count(' with '):            # case #1
        bobName, gunName = rsplit1(text, ' with ')
        return _simpleToolact(player, toolActionClass, bobName, gunName)
    else:                               # case #2 
        for splitter in (' at ', ' to ', ' from ', ' and '):
            if text.count(splitter):
                gunName, bobName = rsplit1(text, splitter)
                return _simpleToolact(player, toolActionClass, bobName, gunName)
    # you rolled a 9 (case #4 & 5)
    lr = []
    if toolActionClass.allowImplicitTarget:
        lr.extend(_simpleToolact(player, toolActionClass, None, text))
    
    lr.extend(_simpleToolact(player, toolActionClass, text, None))
    return lr


