# -*- test-case-name: imaginary.test.test_vending -*-

from zope.interface import implements, Interface

from axiom import item, attributes
from axiom.dependency import installOn

from imaginary import iimaginary, objects, events, language
from imaginary.objects import ThingMixin


class ICoin(Interface):
    """
    Something small and probably flat and round and which probably serves as
    some form of currency.
    """



def createCreator(*powerups):
    def create(**kw):
        store = kw['store']
        o = objects.Thing(**kw)
        for pup, pupkw in powerups:
            installOn(pup(store=store, **pupkw or {}), o)
        return o
    return create



class Coinage(object):
    implements(ICoin)
    powerupInterfaces = (ICoin,)



class Quarter(item.Item, Coinage, ThingMixin):
    thing = attributes.reference(doc="""
    The object this coin powers up.
    """)



class VendingMachine(item.Item, objects.Containment, ThingMixin):
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
                    otherMessage=language.Sentence([self.thing, " thumps loudly and spits out ", obj, " onto the ground."]))
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
    installOn(VendingMachine(store=store), o)
    return o



def createQuiche(store, name, description=u""):
    return objects.Thing(store=store, name=name, description=description)



createCoin = createCreator((Quarter, {}))
createVendingMachine = createCreator((VendingMachine, {}))
createQuiche = createCreator()

createTorch = createCreator((objects.LightSource, {"candelas": 80}))
