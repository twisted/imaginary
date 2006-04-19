# -*- test-case-name: imaginary.test.test_vending -*-

from zope.interface import implements, Interface

from twisted.python import components

from axiom import item, attributes

from imaginary import iimaginary, objects, action, events, language


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
            pup(store=store, **pupkw or {}).installOn(o)
        return o
    return create



class Coinage(object):
    implements(ICoin)

    def installOn(self, other):
        super(Coinage, self).installOn(other)
        other.powerUp(self, ICoin)



class Quarter(item.Item, Coinage, item.InstallableMixin):
    installedOn = objects.installedOn
    thing = attributes.reference(doc="""
    The object this coin powers up.
    """)



class VendingMachine(item.Item, objects.Containment, item.InstallableMixin):
    implements(iimaginary.IContainer)

    capacity = attributes.integer(doc="""
    Units of weight which can be contained.
    """, allowNone=False, default=1)

    closed = attributes.boolean(doc="""
    Indicates whether the container is currently closed or open.
    """, allowNone=False, default=True)

    installedOn = objects.installedOn
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
    VendingMachine(store=store).installOn(o)
    return o



def createQuiche(store, name, description=u""):
    return objects.Thing(store=store, name=name, description=description)



createCoin = createCreator((Quarter, {}))
createVendingMachine = createCreator((VendingMachine, {}))
createQuiche = createCreator()
