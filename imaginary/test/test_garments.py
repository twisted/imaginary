from twisted.trial import unittest

from axiom import store

from imaginary import objects, garments, language
from imaginary.test import commandutils



class WearIt(unittest.TestCase, commandutils.LanguageMixin):

    def setUp(self):
        self.store = store.Store()

        self.dummy = objects.Thing(store=self.store, name=u'dummy')
        self.dummyContainer = objects.Container(store=self.store, capacity=100)
        self.dummyContainer.installOn(self.dummy)

        self.shirt = objects.Thing(store=self.store, name=u'shirt')
        self.shirtGarment = garments.Garment(
            store=self.store,
            garmentDescription=u'a shirt',
            garmentSlots=[garments.GarmentSlot.LEFT_ARM,
                          garments.GarmentSlot.RIGHT_ARM,
                          garments.GarmentSlot.CHEST,
                          garments.GarmentSlot.BACK,
                          ])
        self.shirtGarment.installOn(self.shirt)

        self.wearer = garments.Wearer(store=self.store)
        self.wearer.installOn(self.dummy)


    def testWearing(self):
        self.wearer.putOn(self.shirtGarment)

        self.assertEquals(self.shirt.location, None)

        self.assertEquals(
            self.flatten(language.Noun(self.dummy).description().plaintext(self.dummy)),
            u'[ dummy ]\n'
            u'It is wearing a shirt.')
