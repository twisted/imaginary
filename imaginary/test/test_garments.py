
from axiom.store import Store

from imaginary.places import Thing
from imaginary.garments import Garment, GarmentSlot, Wearer

from imaginary.language import express

from twisted.trial.unittest import TestCase

class WearItThenTakeItOff(TestCase):
    """
    """

    def setUp(self):
        s = self.store = Store()

        self.dummy = Thing(store=s, baseName=u'dummy')
        self.shirt = Thing(store=s)

        self.shirtGarment = Garment(store=s,
                                    garmentDescription=u'a shirt',
                                    garmentSlots=[
                GarmentSlot.LEFT_ARM,
                GarmentSlot.RIGHT_ARM,
                GarmentSlot.CHEST,
                GarmentSlot.BACK,
                ])

        self.shirtGarment.installBehavior(
            self.shirt)

        self.wearer = Wearer(store=s)
        self.wearer.installBehavior(self.dummy)

    def testWearing(self):
        self.wearer.putOn(self.shirtGarment)

        self.assertEquals(self.shirt.location,
                          self.dummy)

        self.assertEquals(
            express(self.dummy.fullyConceptualize(), None),
            u'It is wearing a shirt.')
