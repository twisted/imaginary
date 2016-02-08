
from zope.interface import implementer

from twisted.trial import unittest

from axiom import store

from imaginary import iimaginary, objects, garments, language, vision
from imaginary.eimaginary import ActionFailure
from imaginary.test import commandutils
from imaginary.test.commandutils import E
from imaginary.world import ImaginaryWorld

class WearIt(unittest.TestCase, commandutils.LanguageMixin):

    def setUp(self):
        self.store = store.Store()

        self.dummy = objects.Thing(store=self.store, name=u'dummy')
        self.dummyContainer = objects.Container.createFor(self.dummy,
                                                          capacity=100)

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
        self.mannequin = self.world.create(u"mannequin",
                                           gender=language.Gender.NEUTER,
                                           proper=False)
        self.observer = self.world.create(u"NONDESCRIPT")
        self.underwear = garments.createPants(store=self.store,
                                              name=u'pair of blue pants')
        self.blouse = garments.createShirt(store=self.store,
                                           name=u"blue blouse")
        self.undies = garments.createUnderwear(
            store=self.store, name=u"pair of polka dot underwear"
        )


    def visualizeMannequin(self):
        """
        Present the description rendered when our protagonist, Mannequin, looks
        at itself.

        @return: a concept representing Mannequin's self-description, including
            all her clothes.
        @rtype: L{IConcept}
        """
        [description] = vision.visualizations(
            self.mannequin,
            lambda path: path.targetAs(iimaginary.IThing) is self.mannequin)
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
            iimaginary.IClothingWearer(self.mannequin)))


    def testPersonWearsPants(self):
        iimaginary.IClothingWearer(self.mannequin).putOn(
            iimaginary.IClothing(self.underwear))

        description = self.visualizeMannequin()
        self.assertEquals(
            self.flatten(description.plaintext(self.observer)),
            u'[ mannequin ]\n'
            u'the mannequin is great.\n'
            u'It is wearing a pair of blue pants.')


    def testPersonRemovesPants(self):
        iimaginary.IClothingWearer(self.mannequin).putOn(
            iimaginary.IClothing(self.underwear))
        iimaginary.IClothingWearer(self.mannequin).takeOff(
            iimaginary.IClothing(self.underwear))
        description = self.visualizeMannequin()
        self.assertEquals(
            self.flatten(description.plaintext(self.observer)),
            u'[ mannequin ]\n'
            u'the mannequin is great.\n'
            u'It is naked.\n'
            u'It is carrying a pair of blue pants.'
            )
        self.assertIdentical(self.underwear.location, self.mannequin)


    def testPersonRemovesPantsAndUnderwear(self):
        wearer = iimaginary.IClothingWearer(self.mannequin)
        wearer.putOn(iimaginary.IClothing(self.undies))
        wearer.putOn(iimaginary.IClothing(self.underwear))
        wearer.takeOff(iimaginary.IClothing(self.underwear))
        wearer.takeOff(iimaginary.IClothing(self.undies))
        description = self.visualizeMannequin()
        self.assertEquals(
            self.flatten(description.plaintext(self.observer)),
            u'[ mannequin ]\n'
            u'the mannequin is great.\n'
            u'It is naked.\n'
            u'It is carrying a pair of blue pants and a pair of polka dot '
            u'underwear.'
            )
        self.assertIdentical(self.underwear.location, self.mannequin)


    def test_cantDropSomethingYouAreWearing(self):
        """
        If you're wearing an article of clothing, you should not be able to
        drop it until you first take it off.  After taking it off, however, you
        can move it around just fine.
        """
        wearer = iimaginary.IClothingWearer(self.mannequin)
        wearer.putOn(iimaginary.IClothing(self.undies))
        af = self.assertRaises(ActionFailure, self.undies.moveTo,
                               self.mannequin.location)
        self.assertEquals(
            u''.join(af.event.plaintext(self.mannequin)),
            u"You can't move the pair of polka dot underwear "
            u"without removing it first.\n")

        wearer.takeOff(iimaginary.IClothing(self.undies))
        self.undies.moveTo(self.mannequin.location)
        self.assertEquals(self.mannequin.location, self.undies.location)


    def testTakeOffUnderwearBeforePants(self):
        # TODO - underwear removal skill
        wearer = iimaginary.IClothingWearer(self.mannequin)
        wearer.putOn(iimaginary.IClothing(self.undies))
        wearer.putOn(iimaginary.IClothing(self.underwear))

        self.assertRaises(garments.InaccessibleGarment,
                          wearer.takeOff, iimaginary.IClothing(self.undies))


    def testPersonWearsPantsAndShirt(self):
        iimaginary.IClothingWearer(self.mannequin).putOn(
            iimaginary.IClothing(self.underwear))
        iimaginary.IClothingWearer(self.mannequin).putOn(
            iimaginary.IClothing(self.blouse))

        description = self.visualizeMannequin()

        self.assertEquals(
            self.flatten(description.plaintext(self.observer)),
            u"[ mannequin ]\n"
            u"the mannequin is great.\n"
            u"It is wearing a blue blouse and a pair of blue pants.")


    def testPersonWearsUnderpantsAndPants(self):
        iimaginary.IClothingWearer(self.mannequin).putOn(
            iimaginary.IClothing(self.undies))
        iimaginary.IClothingWearer(self.mannequin).putOn(
            iimaginary.IClothing(self.underwear))

        description = self.visualizeMannequin()

        self.assertEquals(
            self.flatten(description.plaintext(self.observer)),
            u"[ mannequin ]\n"
            u"the mannequin is great.\n"
            u"It is wearing a pair of blue pants.")


    def testPersonWearsPantsAndFailsAtPuttingOnUnderpants(self):
        iimaginary.IClothingWearer(self.mannequin).putOn(
            iimaginary.IClothing(self.underwear))
        self.assertRaises(garments.TooBulky,
                          iimaginary.IClothingWearer(self.mannequin).putOn,
                          iimaginary.IClothing(self.undies))



class FunSimulationStuff(commandutils.CommandTestCaseMixin, unittest.TestCase):

    genderForTest = language.Gender.NEUTER

    def createPants(self):
        """
        Create a pair of blue pants for the test player to wear.
        """
        self._test("create pants named 'pair of blue pants'",
                   ["You create a pair of blue pants."],
                   ["Test Player creates a pair of blue pants."])



    def testWearIt(self):
        self.createPants()
        self._test("wear 'pair of blue pants'",
                   ["You put on the pair of blue pants."],
                   ["Test Player puts on a pair of blue pants."])


    def test_takeItOff(self):
        """
        A garment can be removed with the I{take off} action or the
        I{remove} action.
        """
        self.createPants()
        self._test("wear 'pair of blue pants'",
                   ["You put on the pair of blue pants."],
                   ["Test Player puts on a pair of blue pants."])
        self._test("take off 'pair of blue pants'",
                   ["You take off the pair of blue pants."],
                   ["Test Player takes off a pair of blue pants."])

        self._test("wear 'pair of blue pants'",
                   ["You put on the pair of blue pants."],
                   ["Test Player puts on a pair of blue pants."])
        self._test("remove 'pair of blue pants'",
                   ["You take off the pair of blue pants."],
                   ["Test Player takes off a pair of blue pants."])


    def testProperlyDressed(self):
        self.createPants()
        self._test("create underwear named 'pair of polka dot underwear'",
                   ["You create a pair of polka dot underwear."],
                   ["Test Player creates a pair of polka dot underwear."])
        self._test("wear 'pair of polka dot underwear'",
                   ["You put on the pair of polka dot underwear."],
                   ["Test Player puts on a pair of polka dot underwear."])

        self._test("wear 'pair of blue pants'",
                   ["You put on the pair of blue pants."],
                   ["Test Player puts on a pair of blue pants."])
        self._test("look me",
                   [E("[ Test Player ]"),
                    E("Test Player is great."),
                    E("It is wearing a pair of blue pants.")])


    def testTooBulky(self):
        self.createPants()
        self._test("create pants named 'pair of overalls'",
                   ["You create a pair of overalls."],
                   ["Test Player creates a pair of overalls."])
        self._test("wear 'pair of overalls'",
                   ["You put on the pair of overalls."],
                   ["Test Player puts on a pair of overalls."])
        self._test("wear 'pair of blue pants'",
                   ["The pair of overalls you are already wearing is too "
                    "bulky for you to do that."],
                   ["Test Player wrestles with basic personal problems."])
        self._test("look me",
                   [E("[ Test Player ]"),
                    E("Test Player is great."),
                    E("It is wearing a pair of overalls."),
                    E("It is carrying a pair of blue pants."),
                    ])


    def testInaccessibleGarment(self):
        self.createPants()
        self._test("create underwear named 'pair of polka dot underwear'",
                   ["You create a pair of polka dot underwear."],
                   ["Test Player creates a pair of polka dot underwear."])
        self._test("wear 'pair of polka dot underwear'",
                   ["You put on the pair of polka dot underwear."],
                   ["Test Player puts on a pair of polka dot underwear."])
        self._test("wear 'pair of blue pants'",
                   ["You put on the pair of blue pants."],
                   ["Test Player puts on a pair of blue pants."])
        self._test("remove 'pair of polka dot underwear'",
                   [E("You cannot take off the pair of polka dot underwear "
                      "because you are wearing a pair of blue pants.")],
                   ["Test Player gets a dumb look on its face."])


    def testEquipment(self):
        self.createPants()
        self._test("create underwear named 'pair of polka dot underwear'",
                   ["You create a pair of polka dot underwear."],
                   ["Test Player creates a pair of polka dot underwear."])
        self._test("wear 'pair of polka dot underwear'",
                   ["You put on the pair of polka dot underwear."],
                   ["Test Player puts on a pair of polka dot underwear."])
        self._test("wear 'pair of blue pants'",
                   ["You put on the pair of blue pants."],
                   ["Test Player puts on a pair of blue pants."])
        self._test("equipment",
                   ["You are wearing a pair of blue pants and a pair of "
                    "polka dot underwear."]),


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
        @implementer(iimaginary.IRetriever)
        class ThePathItself(object):
            def retrieve(self, path):
                return path
            def objectionsTo(self, path, result):
                return []
            def shouldKeepGoing(self, path):
                return True

        concept = location.contributeDescriptionFrom(
            location.thing.idea.obtain(ThePathItself())
        )
        self.assertEqual(
            u"Contents: a wearer",
            u"".join(list(concept.plaintext(observer))))
