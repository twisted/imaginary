from twisted.trial import unittest

from axiom import store

from imaginary import iimaginary, objects, garments, language, action
from imaginary.eimaginary import ActionFailure
from imaginary.test import commandutils
from imaginary.test.commandutils import E
from imaginary.world import ImaginaryWorld

class WearIt(unittest.TestCase, commandutils.LanguageMixin):

    def setUp(self):
        self.store = store.Store()

        self.dummy = objects.Thing(store=self.store, name=u'dummy')
        self.dummyContainer = objects.Container.createFor(self.dummy, capacity=100)

        self.shirt = objects.Thing(store=self.store, name=u'shirt')
        self.shirtGarment = garments.Garment.createFor(
            self.shirt,
            garmentDescription=u'a shirt',
            garmentSlots=[garments.GarmentSlot.LEFT_ARM,
                          garments.GarmentSlot.RIGHT_ARM,
                          garments.GarmentSlot.CHEST,
                          garments.GarmentSlot.BACK,
                          ])

        self.wearer = garments.Wearer.createFor(self.dummy)


    def testWearing(self):
        self.wearer.putOn(self.shirtGarment)
        self.assertIdentical(self.shirt.location, self.dummy)



class GarmentPluginTestCase(commandutils.LanguageMixin, unittest.TestCase):
    def setUp(self):
        self.store = store.Store()
        self.world = ImaginaryWorld(store=self.store)
        self.daisy = self.world.create(u"daisy", gender=language.Gender.FEMALE)
        self.observer = self.world.create(u"NONDESCRIPT", gender=language.Gender.MALE)
        self.dukes = garments.createPants(store=self.store,
                                          name=u'pair of Daisy Dukes')
        self.blouse = garments.createShirt(store=self.store,
                                           name=u"blue blouse")
        self.undies = garments.createUnderwear(store=self.store,
                                               name=u"pair of lacy underwear")


    def visualizeDaisy(self):
        """
            
        """
        [description] = action.visualizations(
            self.daisy,
            lambda path: path.targetAs(iimaginary.IThing) is self.daisy)
        return description


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

        description = self.visualizeDaisy()
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
        description = self.visualizeDaisy()
        self.assertEquals(
            self.flatten(description.plaintext(self.observer)),
            u'[ daisy ]\n'
            u'daisy is great.\n'
            u'She is naked.\n'
            u'She is carrying a pair of Daisy Dukes.'
            )
        self.assertIdentical(self.dukes.location, self.daisy)


    def testPersonRemovesPantsAndUnderwear(self):
        wearer = iimaginary.IClothingWearer(self.daisy)
        wearer.putOn(iimaginary.IClothing(self.undies))
        wearer.putOn(iimaginary.IClothing(self.dukes))
        wearer.takeOff(iimaginary.IClothing(self.dukes))
        wearer.takeOff(iimaginary.IClothing(self.undies))
        description = self.visualizeDaisy()
        self.assertEquals(
            self.flatten(description.plaintext(self.observer)),
            u'[ daisy ]\n'
            u'daisy is great.\n'
            u'She is naked.\n'
            u'She is carrying a pair of Daisy Dukes and a pair of lacy '
            u'underwear.'
            )
        self.assertIdentical(self.dukes.location, self.daisy)


    def test_cantDropSomethingYouAreWearing(self):
        """
        If you're wearing an article of clothing, you should not be able to
        drop it until you first take it off.  After taking it off, however, you
        can move it around just fine.
        """
        wearer = iimaginary.IClothingWearer(self.daisy)
        wearer.putOn(iimaginary.IClothing(self.undies))
        af = self.assertRaises(ActionFailure, self.undies.moveTo,
                               self.daisy.location)
        self.assertEquals(
            u''.join(af.event.plaintext(self.daisy)),
            u"You can't move the pair of lacy underwear "
            u"without removing it first.\n")

        wearer.takeOff(iimaginary.IClothing(self.undies))
        self.undies.moveTo(self.daisy.location)
        self.assertEquals(self.daisy.location, self.undies.location)


    def testTakeOffUnderwearBeforePants(self):
        # TODO - underwear removal skill
        wearer = iimaginary.IClothingWearer(self.daisy)
        wearer.putOn(iimaginary.IClothing(self.undies))
        wearer.putOn(iimaginary.IClothing(self.dukes))

        self.assertRaises(garments.InaccessibleGarment,
                          wearer.takeOff, iimaginary.IClothing(self.undies))


    def testPersonWearsPantsAndShirt(self):
        iimaginary.IClothingWearer(self.daisy).putOn(
            iimaginary.IClothing(self.dukes))
        iimaginary.IClothingWearer(self.daisy).putOn(
            iimaginary.IClothing(self.blouse))

        description = self.visualizeDaisy()

        self.assertEquals(
            self.flatten(description.plaintext(self.observer)),
            u"[ daisy ]\n"
            u"daisy is great.\n"
            u"She is wearing a blue blouse and a pair of Daisy Dukes.")


    def testPersonWearsUnderpantsAndPants(self):
        iimaginary.IClothingWearer(self.daisy).putOn(
            iimaginary.IClothing(self.undies))
        iimaginary.IClothingWearer(self.daisy).putOn(
            iimaginary.IClothing(self.dukes))

        description = self.visualizeDaisy()

        self.assertEquals(
            self.flatten(description.plaintext(self.observer)),
            u"[ daisy ]\n"
            u"daisy is great.\n"
            u"She is wearing a pair of Daisy Dukes.")


    def testPersonWearsPantsAndFailsAtPuttingOnUnderpants(self):
        iimaginary.IClothingWearer(self.daisy).putOn(
            iimaginary.IClothing(self.dukes))
        self.assertRaises(garments.TooBulky,
                          iimaginary.IClothingWearer(self.daisy).putOn,
                          iimaginary.IClothing(self.undies))



class FunSimulationStuff(commandutils.CommandTestCaseMixin, unittest.TestCase):

    def createPants(self):
        """
        Create a pair of Daisy Dukes for the test player to wear.
        """
        self._test("create pants named 'pair of daisy dukes'",
                   ["You create a pair of daisy dukes."],
                   ["Test Player creates a pair of daisy dukes."])



    def testWearIt(self):
        self.createPants()
        self._test("wear 'pair of daisy dukes'",
                   ["You put on the pair of daisy dukes."],
                   ["Test Player puts on a pair of daisy dukes."])


    def test_takeItOff(self):
        """
        A garment can be removed with the I{take off} action or the
        I{remove} action.
        """
        self.createPants()
        self._test("wear 'pair of daisy dukes'",
                   ["You put on the pair of daisy dukes."],
                   ["Test Player puts on a pair of daisy dukes."])
        self._test("take off 'pair of daisy dukes'",
                   ["You take off the pair of daisy dukes."],
                   ["Test Player takes off a pair of daisy dukes."])

        self._test("wear 'pair of daisy dukes'",
                   ["You put on the pair of daisy dukes."],
                   ["Test Player puts on a pair of daisy dukes."])
        self._test("remove 'pair of daisy dukes'",
                   ["You take off the pair of daisy dukes."],
                   ["Test Player takes off a pair of daisy dukes."])


    def testProperlyDressed(self):
        self.createPants()
        self._test("create underwear named 'pair of lace panties'",
                   ["You create a pair of lace panties."],
                   ["Test Player creates a pair of lace panties."])
        self._test("wear 'pair of lace panties'",
                   ["You put on the pair of lace panties."],
                   ["Test Player puts on a pair of lace panties."])

        self._test("wear 'pair of daisy dukes'",
                   ["You put on the pair of daisy dukes."],
                   ["Test Player puts on a pair of daisy dukes."])
        self._test("look me",
                   [E("[ Test Player ]"),
                    E("Test Player is great."),
                    E("She is wearing a pair of daisy dukes.")])


    def testTooBulky(self):
        self.createPants()
        self._test("create pants named 'pair of overalls'",
                   ["You create a pair of overalls."],
                   ["Test Player creates a pair of overalls."])
        self._test("wear 'pair of overalls'",
                   ["You put on the pair of overalls."],
                   ["Test Player puts on a pair of overalls."])
        self._test("wear 'pair of daisy dukes'",
                   ["The pair of overalls you are already wearing is too bulky for you to do that."],
                   ["Test Player wrestles with basic personal problems."])
        self._test("look me",
                   [E("[ Test Player ]"),
                    E("Test Player is great."),
                    E("She is wearing a pair of overalls."),
                    E("She is carrying a pair of daisy dukes."),
                    ])


    def testInaccessibleGarment(self):
        self.createPants()
        self._test("create underwear named 'pair of lace panties'",
                   ["You create a pair of lace panties."],
                   ["Test Player creates a pair of lace panties."])
        self._test("wear 'pair of lace panties'",
                   ["You put on the pair of lace panties."],
                   ["Test Player puts on a pair of lace panties."])
        self._test("wear 'pair of daisy dukes'",
                   ["You put on the pair of daisy dukes."],
                   ["Test Player puts on a pair of daisy dukes."])
        self._test("remove 'pair of lace panties'",
                   [E("You cannot take off the pair of lace panties because you are wearing a pair of daisy dukes.")],
                   ["Test Player gets a dumb look on her face."])


    def testEquipment(self):
        self.createPants()
        self._test("create underwear named 'pair of lace panties'",
                   ["You create a pair of lace panties."],
                   ["Test Player creates a pair of lace panties."])
        self._test("wear 'pair of lace panties'",
                   ["You put on the pair of lace panties."],
                   ["Test Player puts on a pair of lace panties."])
        self._test("wear 'pair of daisy dukes'",
                   ["You put on the pair of daisy dukes."],
                   ["Test Player puts on a pair of daisy dukes."])
        self._test("equipment",
                   ["You are wearing a pair of daisy dukes and a pair of lace panties."]),


    def testNoEquipment(self):
        self._test("equipment",
                   ["You aren't wearing any equipment."])



class ContainmentInteractionTests(unittest.TestCase):
    def test_locationConceptExcludesWorn(self):
        """
        An L{IClothing} provider worn by an L{IClothingWearer} provider which
        is contained by a L{IContainer} provider is not included in the concept
        for the L{IContainer} provider.
        """
        db = store.Store()

        observer = objects.Thing(store=db, name=u"observer")

        clothing = garments.Garment.createFor(
            objects.Thing(store=db, name=u"hat"),
            garmentDescription=u"a boring hat",
            garmentSlots=[garments.GarmentSlot.CROWN])
        wearer = garments.Wearer.createFor(
            objects.Thing(store=db, name=u"wearer"))
        location = objects.Container.createFor(
            objects.Thing(store=db, name=u"somewhere"),
            contentsTemplate=u"Contents: {contents}")

        wearer.putOn(clothing)
        location.add(wearer.thing)

        concept = location.conceptualize()
        self.assertEqual(
            u"Contents: a wearer",
            u"".join(list(concept.plaintext(observer))))
