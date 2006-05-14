from twisted.trial import unittest

from axiom import store

from imaginary import iimaginary, objects, garments, language
from imaginary.test import commandutils
from imaginary.test.commandutils import E
from imaginary.wiring import realm


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



class GarmentPluginTestCase(commandutils.LanguageMixin, unittest.TestCase):
    def setUp(self):
        self.store = store.Store()
        self.realm = realm.ImaginaryRealm(store=self.store)
        self.daisy = self.realm.create(u"daisy", u"password",
                                       gender=language.Gender.FEMALE)
        self.observer = self.realm.create(u"NONDESCRIPT", u"I am boring :(",
                                          gender=language.Gender.MALE)
        self.dukes = garments.createPants(store=self.store,
                                          name=u'pair of Daisy Dukes')
        self.blouse = garments.createShirt(store=self.store,
                                           name=u"blue blouse")
        self.undies = garments.createUnderwear(store=self.store,
                                               name=u"pair of lacy underwear")


    def _creationTest(self, garment):
        self.failUnless(
            iimaginary.IClothing.providedBy(iimaginary.IClothing(garment)))


    def testShirtCreation(self):
        self._creationTest(
            garments.createShirt(store=self.store, name=u'red shirt'))


    def testPantsCreation(self):
        self._creationTest(
            garments.createPants(store=self.store, name=u'blue pants'))


    def testPersonIsAWearer(self):
        self.failUnless(iimaginary.IClothingWearer.providedBy(
            iimaginary.IClothingWearer(self.daisy)))


    def testPersonWearsPants(self):
        iimaginary.IClothingWearer(self.daisy).putOn(
            iimaginary.IClothing(self.dukes))

        description = self.daisy.visualize()
        self.assertEquals(
            self.flatten(description.plaintext(self.observer)),
            u'[ daisy ]\n'
            u'daisy is great.\n'
            u'She is wearing a pair of Daisy Dukes.')


    def testPersonRemovesPants(self):
        iimaginary.IClothingWearer(self.daisy).putOn(
            iimaginary.IClothing(self.dukes))
        iimaginary.IClothingWearer(self.daisy).takeOff(
            iimaginary.IClothing(self.dukes))
        description = self.daisy.visualize()
        self.assertEquals(
            self.flatten(description.plaintext(self.observer)),
            u'[ daisy ]\n'
            u'daisy is great.\n'
            u'She is naked.\n'
            u'a pair of Daisy Dukes'
            )
        self.assertIdentical(self.dukes.location, self.daisy)


    def testPersonRemovesPantsAndUnderwear(self):
        wearer = iimaginary.IClothingWearer(self.daisy)
        wearer.putOn(iimaginary.IClothing(self.undies))
        wearer.putOn(iimaginary.IClothing(self.dukes))
        wearer.takeOff(iimaginary.IClothing(self.dukes))
        wearer.takeOff(iimaginary.IClothing(self.undies))
        description = self.daisy.visualize()
        self.assertEquals(
            self.flatten(description.plaintext(self.observer)),
            u'[ daisy ]\n'
            u'daisy is great.\n'
            u'She is naked.\n'
            u'a pair of Daisy Dukes and a pair of lacy underwear'
            )
        self.assertIdentical(self.dukes.location, self.daisy)


    def testTakeOffUnderwearBeforePants(self):
        # TODO - underwear removal skill
        wearer = iimaginary.IClothingWearer(self.daisy)
        wearer.putOn(iimaginary.IClothing(self.undies))
        wearer.putOn(iimaginary.IClothing(self.dukes))

        self.assertRaises(garments.InaccessibleGarment,
                          wearer.takeOff, iimaginary.IClothing(self.undies))


    def testPersonWearsPantsAndShirt(self):
        description = self.daisy.visualize()

        iimaginary.IClothingWearer(self.daisy).putOn(
            iimaginary.IClothing(self.dukes))
        iimaginary.IClothingWearer(self.daisy).putOn(
            iimaginary.IClothing(self.blouse))

        self.assertEquals(
            self.flatten(description.plaintext(self.observer)),
            u"[ daisy ]\n"
            u"daisy is great.\n"
            u"She is wearing a blue blouse and a pair of Daisy Dukes.")


    def testPersonWearsUnderpantsAndPants(self):
        description = self.daisy.visualize()

        iimaginary.IClothingWearer(self.daisy).putOn(
            iimaginary.IClothing(self.undies))
        iimaginary.IClothingWearer(self.daisy).putOn(
            iimaginary.IClothing(self.dukes))

        self.assertEquals(
            self.flatten(description.plaintext(self.observer)),
            u"[ daisy ]\n"
            u"daisy is great.\n"
            u"She is wearing a pair of Daisy Dukes.")


    def testPersonWearsPantsAndFailsAtPuttingOnUnderpants(self):
        description = self.daisy.visualize()

        iimaginary.IClothingWearer(self.daisy).putOn(
            iimaginary.IClothing(self.dukes))
        self.assertRaises(garments.TooBulky,
                          iimaginary.IClothingWearer(self.daisy).putOn,
                          iimaginary.IClothing(self.undies))

    def testWornClothingIsFindable(self):
        iimaginary.IClothingWearer(self.daisy).putOn(
            iimaginary.IClothing(self.dukes))
        dukes = list(self.daisy.findProviders(
            iimaginary.IClothing, 0))
        self.assertEquals(len(dukes), 1)
        self.assertIdentical(dukes[0].thing, self.dukes)


class FunSimulationStuff(commandutils.CommandTestCaseMixin, unittest.TestCase):
    def testWearIt(self):
        self._test("create pants 'pair of daisy dukes'",
                   ["Pair of daisy dukes created."],
                   ["Test Player creates pair of daisy dukes."])
        self._test("wear 'pair of daisy dukes'",
                   ["You put on pair of daisy dukes."],
                   ["Test Player puts on pair of daisy dukes."])


    def testTakeItOff(self):
        # WOO
        self._test("create pants 'pair of daisy dukes'",
                   ["Pair of daisy dukes created."],
                   ["Test Player creates pair of daisy dukes."])
        self._test("wear 'pair of daisy dukes'",
                   ["You put on pair of daisy dukes."],
                   ["Test Player puts on pair of daisy dukes."])
        self._test("take off 'pair of daisy dukes'",
                   ["You take off pair of daisy dukes."],
                   ["Test Player takes off pair of daisy dukes."])

        self._test("wear 'pair of daisy dukes'",
                   ["You put on pair of daisy dukes."],
                   ["Test Player puts on pair of daisy dukes."])
        self._test("remove 'pair of daisy dukes'",
                   ["You take off pair of daisy dukes."],
                   ["Test Player takes off pair of daisy dukes."])


    def testProperlyDressed(self):
        self._test("create pants 'pair of daisy dukes'",
                   ["Pair of daisy dukes created."],
                   ["Test Player creates pair of daisy dukes."])
        self._test("create underwear 'lace panties'",
                   ["Lace panties created."],
                   ["Test Player creates lace panties."])
        self._test("wear 'lace panties'",
                   ["You put on lace panties."],
                   ["Test Player puts on lace panties."])
        self._test("wear 'pair of daisy dukes'",
                   ["You put on pair of daisy dukes."],
                   ["Test Player puts on pair of daisy dukes."])
        self._test("look me",
                   [E("[ Test Player ]"),
                    E("Test Player is great."),
                    E("She is wearing pair of daisy dukes.")])


    def testTooBulky(self):
        self._test("create pants 'pair of daisy dukes'",
                   ["Pair of daisy dukes created."],
                   ["Test Player creates pair of daisy dukes."])
        self._test("create pants 'overalls'",
                   ["Overalls created."],
                   ["Test Player creates overalls."])
        self._test("wear 'overalls'",
                   ["You put on overalls."],
                   ["Test Player puts on overalls."])
        self._test("wear 'pair of daisy dukes'",
                   ["Overalls you are already wearing is too bulky for you to do that."],
                   ["Test Player wrestles with basic personal problems."])
        self._test("look me",
                   [E("[ Test Player ]"),
                    E("Test Player is great."),
                    E("She is wearing overalls."),
                    E("pair of daisy dukes"),
                    ])


    def testInaccessibleGarment(self):
        self._test("create pants 'pair of daisy dukes'",
                   ["Pair of daisy dukes created."],
                   ["Test Player creates pair of daisy dukes."])
        self._test("create underwear 'lace panties'",
                   ["Lace panties created."],
                   ["Test Player creates lace panties."])
        self._test("wear 'lace panties'",
                   ["You put on lace panties."],
                   ["Test Player puts on lace panties."])
        self._test("wear 'pair of daisy dukes'",
                   ["You put on pair of daisy dukes."],
                   ["Test Player puts on pair of daisy dukes."])
        self._test("remove 'lace panties'",
                   [E("You cannot take off lace panties because you are wearing pair of daisy dukes.")],
                   ["Test Player gets a dumb look on her face."])


    def testEquipment(self):
        self._test("create pants 'pair of daisy dukes'",
                   ["Pair of daisy dukes created."],
                   ["Test Player creates pair of daisy dukes."])
        self._test("create underwear 'lace panties'",
                   ["Lace panties created."],
                   ["Test Player creates lace panties."])
        self._test("wear 'lace panties'",
                   ["You put on lace panties."],
                   ["Test Player puts on lace panties."])
        self._test("wear 'pair of daisy dukes'",
                   ["You put on pair of daisy dukes."],
                   ["Test Player puts on pair of daisy dukes."])
        self._test("equipment",
                   ["You are wearing lace panties and pair of daisy dukes."]),


    def testNoEquipment(self):
        self._test("equipment",
                   ["You aren't wearing any equipment."])
