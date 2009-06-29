
"""
Tests for L{imaginary.enhancement}.
"""

from zope.interface import Interface, implements

from twisted.trial.unittest import TestCase

from axiom.store import Store
from axiom.item import Item
from axiom.attributes import integer, reference, boolean
from axiom.dependency import installOn

from imaginary.enhancement import Enhancement
from imaginary.objects import Thing

class INonPowerupInterface(Interface):
    """
    This is an interface, but not a powerup interface.
    """



class IStubSimulation(Interface):
    """
    A stub interface for simulations.
    """



class StubEnhancement(Item, Enhancement):
    """
    An enhancement for testing.  This adds functionality to a L{Thing}.
    """

    implements(IStubSimulation, INonPowerupInterface)
    powerupInterfaces = [IStubSimulation]

    thing = reference()
    stubValue = integer()



class StrictEnhancement(Item, Enhancement):
    """
    An enhancement for testing with an attribute that has C{allowNone=False}
    and no default.
    """

    requiredValue = integer(allowNone=False)
    thing = reference(allowNone=False)



class CustomizedEnhancement(Item, Enhancement):
    """
    An enhancement which has customized apply / remove behavior.
    """

    thing = reference(allowNone=False)
    applied = boolean()
    removed = boolean()

    def applyEnhancement(self):
        """
        The enhancement is about to be applied; modify our attributes to
        account for that.
        """
        self.applied = True
        super(CustomizedEnhancement, self).applyEnhancement()


    def removeEnhancement(self):
        """
        The enhancement is about to be removed; modify our attributes to
        account for that.
        """
        self.removed = True
        super(CustomizedEnhancement, self).removeEnhancement()



class EnhancementTests(TestCase):
    """
    Tests for L{Enhancement}
    """

    def setUp(self):
        """
        Create a store with a thing in it.
        """
        self.store = Store()
        self.thing = Thing(store=self.store, name=u'test object')


    def test_createForSimple(self):
        """
        L{Enhancement.createFor} will create an enhancement of the appropriate
        type and install it as a powerup on the Thing it is passed.
        """
        stub = StubEnhancement.createFor(self.thing)
        self.assertIdentical(stub.thing, self.thing)
        self.assertIdentical(IStubSimulation(self.thing), stub)
        self.assertIdentical(INonPowerupInterface(self.thing, None), None)


    def test_createForArguments(self):
        """
        Keyword arguments passed to L{Enhancement.createFor} will be passed on
        to the class.
        """
        stub = StubEnhancement.createFor(self.thing, stubValue=4321)
        self.assertEquals(stub.stubValue, 4321)


    def test_createForAllowNoneFalse(self):
        """
        If an L{Enhancement} subclass requires a particular attribute,
        L{Enhancement.createFor} will require that argument just as
        L{Item.__init__} would.
        """
        self.assertRaises(
            TypeError, StrictEnhancement.createFor, self.thing)


    def test_overrideApplyEnhancement(self):
        """
        Subclasses of L{Enhancement} can override applyEnhancement to determine
        what happens when createFor does its powering up.
        """
        custom = CustomizedEnhancement.createFor(self.thing, applied=False)
        self.assertEquals(custom.applied, True)


    def test_dontRelyOnInstalledHook(self):
        """
        L{Enhancement.installed} raises a L{RuntimeError}, to make sure that
        nothing uses L{installOn} to install enhancements any more.
        """
        se = StubEnhancement(store=self.store, thing=self.thing)
        theError = self.assertRaises(RuntimeError, installOn, se, self.thing)
        self.assertEquals(str(theError),
                         "Use Enhancement.createFor, not installOn(), "
                         "to apply an Enhancement to a Thing.")


    def test_destroyFor(self):
        """
        L{Enhancement.destroyFor} powers down the L{Enhancement} from its
        L{Thing}, and removes it from its store.
        """
        StubEnhancement.createFor(self.thing)
        otherThing = Thing(store=self.store, name=u'test other thing')
        stub2 = StubEnhancement.createFor(otherThing)
        StubEnhancement.destroyFor(self.thing)
        self.assertIdentical(IStubSimulation(self.thing, None), None)
        self.assertEquals([stub2], list(self.store.query(StubEnhancement)))


    def test_removeEnhancement(self):
        """
        L{Enhancement.removeEnhancement} removes the L{Enhancement} from its
        L{Thing}, but leaves it in place.
        """
        stub = StubEnhancement.createFor(self.thing)
        stub.removeEnhancement()
        self.assertIdentical(IStubSimulation(self.thing, None), None)
        self.assertEquals([stub], list(self.store.query(StubEnhancement)))


    def test_destroyForRemovesEnhancement(self):
        """
        L{Enhancement.destroyFor} will first invoke C{removeEnhancement},
        allowing subclasses to hook it to provide custom cleanup logic.
        """
        custom = CustomizedEnhancement.createFor(
            self.thing, applied=False, removed=False)
        CustomizedEnhancement.destroyFor(self.thing)
        self.assertEquals(custom.removed, True)


    def test_destroyForNothing(self):
        """
        L{Enhancement.destroyFor} does nothing when invoked on a Thing that
        doesn't have any enhancements of the specified type installed.
        """
        # I have to write code in order to make this happen, rather than an
        # exception getting raised; i.e. a 'default=None'.  So it's worth
        # testing.  Unfortunately I don't actually have anything to assert
        # about it except "an exception wasn't raised, and all the other stuff
        # in the other tests still work"
        StubEnhancement.destroyFor(self.thing)

