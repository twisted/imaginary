# -*- test-case-name: examplegame.test.test_quiche -*-

"""
This module is a mid-level proof of concept of various features in Imaginary.

Currently its implementation is a bit messy and it assumes lots of things about
the reader's knowledge, but we are working on more thoroughly documenting it
and making it into a good example of how to build functionality that interacts
with multiple systems (currency, containment, object creation) in Imaginary.

"""

from zope.interface import implements, Interface

from axiom import item, attributes

from imaginary import iimaginary, objects, events, language
from imaginary.enhancement import Enhancement

from imaginary.creation import createCreator


class ICoin(Interface):
    """
    Something small and probably flat and round and which probably serves as
    some form of currency.
    """



class Coinage(object):
    implements(ICoin)
    powerupInterfaces = (ICoin,)



class Quarter(item.Item, Coinage, Enhancement):
    thing = attributes.reference(doc="""
    The object this coin powers up.
    """)



class VendingMachine(item.Item, objects.Containment, Enhancement):
    implements(iimaginary.IContainer)

    capacity = attributes.integer(doc="""
    Units of weight which can be contained.
    """, allowNone=False, default=1)

    closed = attributes.boolean(doc="""
    Indicates whether the container is currently closed or open.
    """, allowNone=False, default=True)

    thing = attributes.reference(doc="""
    The object this container powers up.
    """)

    _currencyCounter = attributes.integer(doc="""
    The number of coins which have been added to this vending machine since it
    last ejected an item.
    """, allowNone=False, default=0)

    def coinAdded(self, coin):
        """
        Called when a coin is added to this thing.

        @type coin: C{ICoin} provider
        """
        self._currencyCounter += 1
        if self._currencyCounter >= 5 and self.getContents():
            self._currencyCounter = 0
            try:
                obj = iter(self.getContents()).next()
            except StopIteration:
                evt = events.Success(
                    actor=self.thing,
                    target=obj,
                    otherMessage=language.Sentence([self.thing, " thumps loudly."]))
            else:
                evt = events.Success(
                    actor=self.thing,
                    target=obj,
                    otherMessage=language.Sentence([
                        language.Noun(self.thing).definiteNounPhrase(),
                        " thumps loudly and spits out ", obj,
                        " onto the ground."]))
                state = self.closed
                self.closed = False
                try:
                    obj.moveTo(self.thing.location)
                finally:
                    self.closed = state
            evt.broadcast()


    def add(self, obj):
        coin = ICoin(obj, None)
        if coin is not None:
            self.coinAdded(coin)
        else:
            return super(VendingMachine, self).add(obj)



def createVendingMachine(store, name, description=u""):
    o = objects.Thing(store=store, name=name, description=description)
    VendingMachine.createFor(o)
    return o



createCoin = createCreator((Quarter, {}))
createVendingMachine = createCreator((VendingMachine, {}))
createQuiche = createCreator()

