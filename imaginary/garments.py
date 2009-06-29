# -*- test-case-name: imaginary.test.test_garments -*-

"""

Layered clothing.

"""

from zope.interface import implements

from axiom import item, attributes

from imaginary import iimaginary, language, objects
from imaginary.creation import createCreator
from imaginary.enhancement import Enhancement


class Unwearable(Exception):
    pass

class TooBulky(Unwearable):
    def __init__(self, wornGarment, newGarment):
        self.wornGarment = wornGarment
        self.newGarment = newGarment
        Unwearable.__init__(self, wornGarment, newGarment)



class InaccessibleGarment(Exception):
    """The garment is covered by another, therefore it cannot be removed.
    """
    def __init__(self, wearer, garment, obscuringGarment):
        self.wearer = wearer
        self.garment = garment
        self.obscuringGarment = obscuringGarment


    def __str__(self):
        return "%s tried taking off %s which was covered by %s" % (
            self.wearer, self.garment, self.obscuringGarment)



GARMENT_SLOTS = [
    u"crown",
    u"left eye",
    u"right eye",
    u"left ear",
    u"right ear",

    u"neck",
    u"chest",
    u"back",

    u"left arm",
    u"right arm",
    u"left wrist",
    u"right wrist",
    u"left hand",
    u"right hand",
    u"left fingers",
    u"right fingers",

    u"waist",
    u"left leg",
    u"right leg",
    u"left ankle",
    u"right ankle",
    u"left foot",
    u"right foot"
    ]

class GarmentSlot:
    pass

for gslot in GARMENT_SLOTS:
    gslotname = gslot.upper().replace(" ", "_").encode('ascii')
    setattr(GarmentSlot, gslotname, gslot)



class Garment(item.Item, Enhancement):
    implements(iimaginary.IClothing,
               iimaginary.IDescriptionContributor)
    powerupInterfaces = (iimaginary.IClothing, iimaginary.IDescriptionContributor)

    thing = attributes.reference()

    # templated / constant stuff
    garmentSlots = attributes.textlist(allowNone=False)
    bulk = attributes.integer(allowNone=False,
                              default=1)
    garmentDescription = attributes.text(doc="""
    Description of this as an individual garment.
    """, allowNone=False)

    # transient / mutable stuff
    wearer = attributes.reference()
    wearLevel = attributes.integer(default=0)


    def conceptualize(self):
        return language.ExpressString(u'This can be worn.')


    def expressTo(self, observer):
        """
        Describe the garment as it looks when it is worn.

        The garment's normal description is C{self.thing.description} or
        somesuch.
        """
        return self.garmentDescription


def _orderTopClothingByGlobalSlotList(tempClothes):
    """
    This function orders a dict as returned by getGarmentDict in the order that
    they should be shown to the user.

    @param tempClothes: {clothingSlot: list of clothing objects (top last)}
    @type tempClothes: dict
    """
    if not tempClothes:
        return None
    yetDescribed = []
    for universalSlot in GARMENT_SLOTS:
        slotlist = tempClothes.pop(universalSlot, ())
        if slotlist:
            topGarment = slotlist[-1]
            if topGarment not in yetDescribed:
                yetDescribed.append(topGarment)

    # if somebody decided to make a wacky slot that is not in the universal
    # slots list, just describe it last.
    for k in tempClothes.keys():
        x = tempClothes.pop(k)
        if x:
            topGarment = x[-1]
            if topGarment not in yetDescribed:
                yetDescribed.append(topGarment)

    assert tempClothes == {}, (
        "tempClothes not empty after all clothes eliminated: " +
        repr(tempClothes))

    return yetDescribed



class Wearer(item.Item, Enhancement):
    """
    The clothing-wearing component of an object that can wear clothing; e.g. a
    person or mannequin.
    """

    implements(iimaginary.IClothingWearer, iimaginary.IDescriptionContributor)
    powerupInterfaces = (iimaginary.IClothingWearer, iimaginary.IDescriptionContributor,
                         iimaginary.ILinkContributor)


    thing = attributes.reference()


    def getGarmentDict(self):
        c = {}
        for garment in self.store.query(Garment, Garment.wearer == self,
                                        sort=Garment.wearLevel.ascending):
            for usedSlot in garment.garmentSlots:
                c.setdefault(usedSlot, []).append(garment)
        return c


    def putOn(self, newGarment):
        c = self.getGarmentDict()
        for garmentSlot in newGarment.garmentSlots:
            if garmentSlot in c:
                # We don't want to be able to wear T-shirts over heavy coats;
                # therefore, heavy coats have a high "bulk"
                currentTopOfSlot = c[garmentSlot][-1]
                if currentTopOfSlot.bulk >= newGarment.bulk:
                    raise TooBulky(currentTopOfSlot, newGarment)

        newGarment.thing.moveTo(None)
        newGarment.wearer = self
        newGarment.wearLevel = self.store.query(Garment, Garment.wearer == self).getColumn("wearLevel").max(default=0) + 1


    def takeOff(self, garment):
        gdict = self.getGarmentDict()
        for slot in garment.garmentSlots:
            if gdict[slot][-1] is not garment:
                raise InaccessibleGarment(self, garment, gdict[slot][-1])
        garment.thing.moveTo(garment.wearer.thing)
        garment.wearer = garment.wearLevel = None


    # IDescriptionContributor
    def conceptualize(self):
        """
        Describe the list of clothing.
        """
        return ExpressClothing(self.thing, self.getGarmentDict())


    # ILinkContributor
    def links(self):
        d = {}
        for t in self.store.query(objects.Thing, attributes.AND(Garment.thing == objects.Thing.storeID,
                                                                Garment.wearer == self)):
            d.setdefault(t.name, []).append(t)
        return d



class ExpressClothing(language.BaseExpress):
    def __init__(self, thing, garments):
        self.thing = thing
        self.garments = garments


    def vt102(self, observer):
        heshe = language.Noun(self.thing).heShe()
        L = _orderTopClothingByGlobalSlotList(self.garments)
        if L is None:
            return language.Sentence([heshe, u' is naked.']).vt102(observer)
        return language.Sentence([
            heshe,
            u' is wearing ',
            language.ItemizedList([language.Noun(g.thing).nounPhrase()
                                   for g in L]),
            u'.']).vt102(observer)



createShirt = createCreator(
    (Garment, dict(garmentDescription=u'an undescribed shirt',
                   bulk=2,
                   garmentSlots=[GarmentSlot.CHEST,
                                 GarmentSlot.BACK,
                                 GarmentSlot.RIGHT_ARM,
                                 GarmentSlot.LEFT_ARM])))


createUnderwear = createCreator(
    (Garment, dict(garmentDescription=u'an undescribed pair of underwear',
                   bulk=1,
                   garmentSlots=[GarmentSlot.WAIST])))

createPants = createCreator(
    (Garment, dict(garmentDescription=u'an undescribed pair of pants',
                   bulk=2,
                   garmentSlots=[GarmentSlot.RIGHT_LEG,
                                 GarmentSlot.LEFT_LEG,
                                 GarmentSlot.WAIST,
                                 GarmentSlot.LEFT_ANKLE,
                                 GarmentSlot.RIGHT_ANKLE])))
