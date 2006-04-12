from zope.interface import Interface
from imagination.facets import Facet
from twisted.trial import unittest

from imagination import simdata

class IFoo(Interface):
    pass
class IBar(Interface):
    pass
class IBaz(Interface):
    pass

class Foo(Facet):
    pass
class Bar(Facet):
    pass

class TemplateTest(unittest.TestCase):
    def testSingular(self):
        thing = simdata.baseTemplate[
            IFoo: Foo,
            IBar: Bar,
            ]
        o = thing.new()
        self.failUnless(isinstance(IFoo(o), Foo))
        self.failUnless(isinstance(IBar(o), Bar))

    def testMulti(self):
        thing = simdata.baseTemplate[
            (IFoo, IBar): Foo
            ]
        o = thing.new()
        self.assertIdentical(IFoo(o), IBar(o))

    def testRepeated(self):
        thing = simdata.baseTemplate[
            (IFoo, IBar): Foo
            ]
        newThing = thing[
            IBaz: Bar
            ]
        o = thing.new()
        self.assertIdentical(IFoo(o), IBar(o))
        o = newThing.new()
        self.failUnless(isinstance(IBaz(o), Bar))
