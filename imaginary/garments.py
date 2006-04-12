# -*- test-case-name: imaginary.test.test_garments -*-

"""

Layered clothing.

"""

from axiom import item, attributes

from zope.interface import implements

from imaginary.iimaginary import IClothingWearer, IClothing, IDescriptor, IConcept

from imaginary.places import BehaviorMixin

from imaginary.language import ItemizedList, Noun


class Unwearable(Exception):
    pass

class TooBulky(Unwearable):
    def __init__(self, wornGarment, newGarment):
        self.wornGarment = wornGarment
        self.newGarment = newGarment
        Unwearable.__init__(wornGarment, newGarment)


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
    for gslot in GARMENT_SLOTS:
        gslotname = gslot.upper().replace(" ", "_").encode('ascii')
        exec '%s = %r ' % (gslotname, gslot)


class Garment(item.Item, BehaviorMixin):
    implements(IClothing,
               IConcept,
               IDescriptor)

    # it's a behavior hooray
    thing = attributes.reference()

    # templated / constant stuff
    garmentSlots = attributes.textlist(allowNone=False)
    bulk = attributes.integer(allowNone=False,
                              default=1)
    garmentDescription = attributes.text(allowNone=False, doc="""
    description of this as an individual garment.  """)

    # transient / mutable stuff
    wearer = attributes.reference()
    wearLevel = attributes.integer(default=0,
                                   allowNone=False)

    def conceptualize(self):
        return u'This can be worn.'

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

class Wearer(item.Item, BehaviorMixin):
    """
    The clothing-wearing component of an object that can wear clothing; e.g. a
    person or mannequin.
    """

    implements(IClothingWearer, IDescriptor)

    thing = attributes.reference()

    currentLevel = attributes.integer(default=0)

    def getGarmentDict(self):
        c = {}
        for garment in self.store.query(
            Garment, attributes.AND(Garment.wearer == self),
            sort=Garment.wearLevel.ascending):

            for usedSlot in garment.garmentSlots:
                c.setdefault(usedSlot, []).append(garment)
        return c

    def putOn(self, newGarment):
        newGarment.thing.moveTo(self.thing)
        c = self.getGarmentDict()
        for garmentSlot in newGarment.garmentSlots:
            if garmentSlot in c:
                # We don't want to be able to wear T-shirts over heavy coats;
                # therefore, heavy coats have a high "bulk"
                currentTopOfSlot = c[garmentSlot][-1]
                currentTopOfSlot.bulk >= newGarment.bulk
                raise TooBulky(currentTopOfSlot, newGarment)

        self.currentLevel += 1
        newGarment.wearer = self
        newGarment.wearLevel = self.currentLevel

        for garmentSlot in newGarment.garmentSlots:
            c.setdefault(garmentSlot, []).append(newGarment)

    def conceptualize(self):
        """
        Describe the list of clothing.
        """
        L = _orderTopClothingByGlobalSlotList(self.getGarmentDict())
        return [lambda obs : Noun(self.thing).heShe(obs).capitalize(),
                u' is wearing ',
                ItemizedList(L), '.']

