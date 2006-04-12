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

"""
The Phrase Parser.

This is the core of the system that takes your input, breaks it up, and figures
out what it was you wanted to do.

(Hint: it's called phrase because it's shorter than Sentence!)

"""



from twisted.python.reflect import accumulateMethods
from reality.error import Nonsense, RealityException

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
        return tuple(map(lambda thing, self=self: self.actionClass(player, thing), player.lookAroundFor(text, self.actionClass.getInterface("Target"))))


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

from twisted.python.components import Interface, registerAdapter, implements, Adapter

class IParsing(Interface):
    def parse(self, text):
        "parse!"

class Parsing(Adapter):
    __implements__ = IParsing,
    potentialActions = None

    def parse(self, text):
        """Parse the text entered by a player and act on it!
        """
        try:
            self._parseInternal(text)
        except RealityException, re:
            self.original.hears(re.format(self.original))
            return re

    def _parseInternal(self, text):
        if self.potentialActions:
            # The user already entered some text that might have been an
            # action.  Let's see if they're selecting a choice from that list.
            try:
                val = int(text)
            except ValueError:
                pass
            else:
                potentialAction = self.potentialActions[val - 1]
                self.potentialActions = None
                potentialAction.performAction()
                return
        # I'm in a normal state
        potentialActions = parseToActions(self.original, text)
        # print 'parsed to potentials:',potentialActions
        if not potentialActions:
            raise Nonsense()
        potentialRealActions = [act for act in potentialActions if not act.isPlaceholder()]
        if len(potentialRealActions) and len(potentialRealActions) < len(potentialActions):
            potentialActions = potentialRealActions
        if len(potentialActions) == 1:
            potentialActions[0].performAction()
        else:
            self.potentialActions = potentialActions
            i = 0
            for act in self.potentialActions:
                i += 1
                self.original.hears("%d: %s" % (i, str(act)))

### Utility Functions

def rsplit1(s, sep):
    """Find a delimiter backwards through a string.

    Returns a 2-tuple of (before-last-sep, after-last-sep).  If sep is not
    found, it returns (s,'').
    """
    n = s.rfind(sep)
    if n == -1:
        return (s, '')
    return (s[:n].strip(), s[n+len(sep):].strip())

def _simpleToolact(player, toolActionClass, bobName, gunName):
    guns = player.lookAroundFor(gunName, toolActionClass.getInterface("Tool"))
    bobs = player.lookAroundFor(bobName, toolActionClass.getInterface("Target"))
    return [toolActionClass(player, tool, target)
            for tool, target in zip(bobs, guns)]

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
    if text.count(' with '):            # case #1
        bobName, gunName = rsplit1(text, ' with ')
        return _simpleToolact(player, toolActionClass, bobName, gunName)
    elif text.count(' at '):            # case #2
        gunName, bobName = rsplit1(text, ' at ')
        return _simpleToolact(player, toolActionClass, bobName, gunName)
    # you rolled a 9 (case #4 & 5)
    lr = []
    if "Tool" in toolActionClass.allowNoneInterfaceTypes:
        lr.extend([toolActionClass(player, target, None) for target in
                   player.lookAroundFor(text,
                                        toolActionClass.getInterface("Target"))])
    if "Target" in toolActionClass.allowNoneInterfaceTypes:
        lr.extend([toolActionClass(player, None, tool) for tool in
                   player.lookAroundFor(text,
                                        toolActionClass.getInterface("Tool"))])
    return lr
