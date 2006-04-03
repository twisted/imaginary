
from zope.interface import implements, Interface

from twisted.python import components

from pottery import ipottery, objects, action, events


class ICoin(Interface):
    """
    Something small and probably flat and round and which probably serves as
    some form of currency.
    """


class Quiche(objects.Object):
    pass



class VendingMachine(objects.Container):
    closed = True

    _currencyCounter = 0

    def coinAdded(self, coin):
        """
        Called when a coin is added to this thing.

        @type coin: C{ICoin} provider
        """
        self._currencyCounter += 1
        if self._currencyCounter >= 5 and self.contents:
            self._currencyCounter = 0
            obj = self.contents.pop()
            evt = events.Success(
                actor=self,
                target=obj,
                otherMessage=(self, " thumps loudly and spits out ", obj, " onto the ground."))
            self.location.add(obj)
            evt.broadcast()


    def add(self, obj):
        if ICoin.providedBy(obj):
            self.coinAdded(obj)
        else:
            return objects.Container.add(self, obj)


class Quarter(objects.Object):
    implements(ICoin)
