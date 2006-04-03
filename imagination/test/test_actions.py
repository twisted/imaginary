from zope.interface import implements
from twisted.trial import unittest
from twisted.internet import defer

from imagination import actions, errors, simulacrum, iimagination, containment
from imagination.text import english
from imagination.templates import basic
from imagination.facets import Facet

def getTestUI(actor, SELECTION):
    class TestUI(Facet):
        implements(iimagination.IUI)
        def presentMenu(self, list, typename=None):
            self.typename = typename
            self.list = list
            return defer.succeed(SELECTION)
    return TestUI(actor)

class TestAction:
    didPreAction = 0
    didPostAction = 0
    didAction = 0

    def preAction(self):
        self.didPreAction += 1
        return self.parentClass.preAction(self)
    
    def postAction(self, result):
        self.didPostAction += 1
        return self.parentClass.postAction(self, result)

    def doAction(self):
        self.didAction += 1
        return self


class NoTargetTestAction(TestAction, actions.NoTargetAction):
    parentClass = actions.NoTargetAction
    def __init__(self, player, text, *a, **kw):
        actions.NoTargetAction.__init__(self, player, *a, **kw)
        self.initText = text

class TargetTestAction(TestAction, actions.TargetAction):
    parentClass = actions.TargetAction
    
    def __init__(self, player, targetName):
        actions.TargetAction.__init__(self, player, targetName)

class ToolTargetTestAction(TestAction, actions.ToolAction):
    parentClass = actions.ToolAction
    def __init__(self, player, targetName, toolName=None):
        actions.ToolAction.__init__(self, player, targetName, toolName)

class TestParser(english.Subparser):
    def parse_test(self, player, text):
        return [NoTargetTestAction(player, text)]

    simpleTargetParsers = {'target': TargetTestAction}
    simpleToolParsers = {'throw': ToolTargetTestAction}

class TestActionTarget(Facet):
    implements(ITargetTestActionTarget)

class TargetTestActionTarget(Facet):
    implements(ITargetTestActionTarget)

class TargetTestActionActor(Facet):
    implements(ITargetTestActionActor)

class ToolTargetTestActionActor(Facet):
    implements(IToolTargetTestActionActor)

class ToolTargetTestActionTarget(Facet):
    implements(IToolTargetTestActionTarget)

class ToolTargetTestActionTool(Facet):
    implements(IToolTargetTestActionTool)

Ball = basic.Thing[
    # simulacrum.ICollector: containment.Container,
    ITargetTestActionTarget: TestActionTarget,
    ]


class ActionTests(unittest.TestCase):
    def setUp(self):
        self.parserEngine = english.VerbParserEngine()
        self.parserEngine.registerSubparser(TestParser())
        self.actor = basic.Actor[
            INoTargetTestActionActor: Facet,
            ITargetTestActionActor: TargetTestActionActor,
            IToolTargetTestActionActor: ToolTargetTestActionActor
            ].new()
        self.ball1 = Ball[
                IToolTargetTestActionTool: ToolTargetTestActionTool
                ].fill(english.INoun, name='ball').new()
        bob = basic.Actor[
            IToolTargetTestActionTarget: ToolTargetTestActionTarget
            ].fill(english.INoun, name='bob').new()
        simulacrum.ICollector(self.actor).grab(bob)
        simulacrum.ICollector(self.actor).grab(self.ball1)
        parsing = english.IThinker(self.actor)
        parsing.parseToActions = self.parserEngine.parseToActions
        self.parse = parsing.parse


class SimpleActions(ActionTests):

    def testNoTargetAction(self):
        action = self.parse("test")

        self.failUnless(isinstance(action, NoTargetTestAction))
        self.assertEquals(action.didPreAction, 1)
        self.assertEquals(action.didAction, 1)
        self.assertEquals(action.didPostAction, 1)

        self.assertIdentical(action.actor, INoTargetTestActionActor(self.actor))
        self.assertEquals(action.initText, "")

    def testTargetAction(self):
        action = self.parse('target ball')
        self.failUnless(isinstance(action, TargetTestAction))
        self.assertEquals(action.didPreAction, 1)
        self.assertEquals(action.didAction, 1)
        self.assertEquals(action.didPostAction, 1)

        self.assertIdentical(action.actor, ITargetTestActionActor(self.actor))
        self.assertEquals(action.targetName, "ball")

    def testFailingTargetAction(self):
        self.assertRaises(errors.ActionRefused, self.parse, 'target foo')
        # self.parse('target foo')
    
    def testToolTargetAction(self):
        action = self.parse('throw ball at bob')


class Ambiguity(ActionTests):
    def setUp(self):
        ActionTests.setUp(self)
        self.ball2 = Ball[
            IToolTargetTestActionTool: ToolTargetTestActionTool
            ].fill(english.INoun, name='ball').new()
        simulacrum.ICollector(self.actor).grab(self.ball2)

    def testAmbiguousTarget(self):
        testui = getTestUI(self.actor, 0)
        self.actor[iimagination.IUI] = testui
        action = self.parse('target ball')
        self.failUnless(isinstance(action, defer.Deferred))
        self.assertEquals(testui.typename, 'Target')

        promptBalls = testui.list[:]

        balls = [ITargetTestActionTarget(self.ball1), ITargetTestActionTarget(self.ball2)]
        self.assertEquals(promptBalls, balls)

        def cbTarget(action):
            self.failUnless(isinstance(action, TargetTestAction))
            self.assertEquals(action.didPreAction, 1)
            self.assertEquals(action.didPostAction, 1)
            self.assertEquals(action.didAction, 1)

            self.assertIdentical(action.actor, ITargetTestActionActor(self.actor))
            self.assertIdentical(action.target, ITargetTestActionTarget(promptBalls[0]))
        return action.addCallback(cbTarget)

