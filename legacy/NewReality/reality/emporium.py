# -*- test-case-name: reality.test_reality -*- 
"""
``Jockey of Norfolk, be not too bold,
 For Dickon, thy master, is bought and sold.''

"""
from twisted.python import components 

from reality import things, errors, actions, ambulation, conveyance
from reality.text import english

class IVendor(components.Interface): pass
class IMerchandise(components.Interface): pass

class Buy(actions.TargetAction):
    def formatToOther(self):
        return ""
    def formatToActor(self):
        return ("You buy ",self.target," from ",self.vendor," for ",
                self.target.price," zorkmids.")
    
    def doAction(self):
        vendors = things.IInterfaceForwarder(self.actor.original).lookFor(None, IVendor)
        if vendors:
            #assume only one vendor per room, for now
            self.vendor = vendors[0]
        else:
            raise errors.Failure("There appears to be no shopkeeper here to receive your payment.")
        amt = self.target.price
        self.actor.withdraw(amt)
        self.vendor.buy(self.target, amt)

class ShopParser(english.Subparser):
    simpleTargetParsers = {"buy": Buy}
english.registerSubparser(ShopParser())

class Customer(components.Adapter):
    __implements__ = IBuyActor,

    def withdraw(self, amt):
        self.balance = self.balance - amt
        
class Vendor(components.Adapter):
    __schema__ = {
        'balance': int
        }
    __implements__ = IVendor
    def shoutPrice(self, merch, cust):
        n = english.INoun(self)
        title = ('creature', 'sir','lady')[things.IThing(cust).gender]
        self.original.emitEvent('%s says "For you, good %s, only %d zorkmids for this %s."' % (n.nounPhrase(cust), title, merch.price, english.INoun(merch).name))

    def buy(self, merchandise, amount):
        self.deposit(amount)
        merchandise.original.removeComponent(merchandise)

    def stock(self, obj, price):
        m = Merchandise(obj)
        m.price = price
        m.owner = self.original.referenceTo(IVendor)
        m.home = self.original.location
        obj.addComponent(m, ignoreClass=1)

    def deposit(self, amt):
        self.balance += amt
        

class Merchandise(components.Adapter):
    __schema__ = {
        'price': int,
        'owner': Vendor,
        'home': things.Thing
        }
    __implements__ = IMerchandise, things.IMoveListener, IBuyTarget

    def thingArrived(*args):
        pass
    def thingLeft(*args):
        pass
    def thingMoved(self, emitter, event):
        if self.original == emitter and isinstance(event, conveyance.Take):
            self.owner.getItem().shoutPrice(self, self.original.location.getItem())
        if self.original.getOutermostRoom() != self.home.getItem():
            self.original.emitEvent("The %s vanishes with a *foop*."
                                    % english.INoun(self).name)
            self.original.moveTo(self.home.getItem())

class ShopDoor(ambulation.Door):
    def collectImplementors(self, asker, iface, collection, seen, event=None, name=None, intensity=2):
        seen[self.storeID] = None
        if iface == ambulation.IWalkTarget:
            unpaidItems = asker.searchContents(None, IMerchandise)
            if unpaidItems:                
                collection[self] = things.Refusal(self, "You cant leave, you haven't paid!")
                return
                
        ambulation.Door.collectImplementors(self, asker, iface,
                                            collection, seen, event,
                                            name, intensity)
        return collection
