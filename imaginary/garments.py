# -*- test-case-name: imaginary.test.test_garments -*-

"""

Layered clothing.

"""

from zope.interface import implements

from axiom import item, attributes

from imaginary import iimaginary, language, objects
from imaginary.eimaginary import ActionFailure
from imaginary.events import ThatDoesntWork
from imaginary.idea import Link
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
    """
    An enhancement for a L{Thing} representing its utility as an article of
    clothing.
    """
    implements(iimaginary.IClothing,
               iimaginary.IDescriptionContributor,
               iimaginary.IMovementRestriction)

    powerupInterfaces = (iimaginary.IClothing,
                         iimaginary.IDescriptionContributor,
                         iimaginary.IMovementRestriction)

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


    def nowWornBy(self, wearer):
        """
        This garment is now worn by the given wearer.  As this garment is now
        on top, set its C{wearLevel} to be higher than any other L{Garment}
        related to the new C{wearer}.
        """
        self.wearer = wearer
        self.wearLevel = wearer.store.query(
            Garment,
            Garment.wearer == wearer).getColumn("wearLevel").max(default=0) + 1


    def noLongerWorn(self):
        """
        This garment is no longer being worn by anyone.
        """
        self.wearer = None
        self.wearLevel = None


    def movementImminent(self, movee, destination):
        """
        Something is trying to move.  Don't allow it if I'm currently worn.
        """
        if self.wearer is not None and movee is self.thing:
            # XXX I don't actually know who is performing the action :-(.
            raise ActionFailure(
                ThatDoesntWork(
                    actor=self.thing.location,
                    actorMessage=[
                        "You can't move ",
                        language.Noun(self.thing).definiteNounPhrase(),
                        " without removing it first."]))



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

    _interfaces = (iimaginary.IClothingWearer,
                   iimaginary.IDescriptionContributor,
                   iimaginary.ILinkContributor,
                   iimaginary.ILinkAnnotator)

    implements(*_interfaces)

    powerupInterfaces = _interfaces


    thing = attributes.reference()


    def getGarmentDict(self):
        c = {}
        for garment in self.store.query(Garment, Garment.wearer == self,
                                        sort=Garment.wearLevel.ascending):
            for usedSlot in garment.garmentSlots:
                c.setdefault(usedSlot, []).append(garment)
        return c


    def putOn(self, newGarment):
        """
        Wear a new L{Garment} on this L{Wearer}, first moving it to this
        L{Wearer}'s C{thing} if it is not already there.

        @param newGarment: the article of clothing to wear.

        @type newGarment: L{Garment}

        @raise TooBulky: if the bulk of any of the slots occupied by
            C{newGarment} is greater than the bulk of any other clothing
            already in that slot.  (For example, if you tried to wear a T-shirt
            over a heavy coat.)
        """
        c = self.getGarmentDict()
        for garmentSlot in newGarment.garmentSlots:
            if garmentSlot in c:
                currentTopOfSlot = c[garmentSlot][-1]
                if currentTopOfSlot.bulk >= newGarment.bulk:
                    raise TooBulky(currentTopOfSlot, newGarment)

        newGarment.thing.moveTo(self.thing)
        newGarment.nowWornBy(self)


    def takeOff(self, garment):
        """
        Remove a garment which this player is wearing.

        (Note: no error checking is currently performed to see if this garment
        is actually already worn by this L{Wearer}.)

        @param garment: the article of clothing to remove.

        @type garment: L{Garment}

        @raise InaccessibleGarment: if the garment is obscured by any other
            clothing, and is therefore not in the top slot for any of the slots
            it occupies.  For example, if you put on an undershirt, then a
            turtleneck, you can't remove the undershirt without removing the
            turtleneck first.
        """
        gdict = self.getGarmentDict()
        for slot in garment.garmentSlots:
            if gdict[slot][-1] is not garment:
                raise InaccessibleGarment(self, garment, gdict[slot][-1])
        garment.noLongerWorn()


    # IDescriptionContributor
    def conceptualize(self):
        """
        Describe the list of clothing.
        """
        return ExpressClothing(self.thing, self.getGarmentDict())


    # ILinkContributor
    def links(self):
        for garmentThing in self.store.query(objects.Thing,
                                  attributes.AND(
                Garment.thing == objects.Thing.storeID,
                Garment.wearer == self)):
            yield Link(self.thing.idea, garmentThing.idea)


    def annotationsFor(self, link, idea):
        """
        Tell the containment system to disregard containment relationships for
        which I will generate a link.
        """
        if list(link.of(iimaginary.IContainmentRelationship)):
            if link.source.delegate is self.thing:
                clothing = iimaginary.IClothing(link.target.delegate, None)
                if clothing is not None:
                    if clothing.wearer is self:
                        yield _DisregardYourWearingIt()



class _DisregardYourWearingIt(object):
    """
    This is an annotation, produced by L{Wearer} for containment relationships
    between people (who are containers) and the clothing that they're wearing.
    A hopefully temporary workaround for the fact that clothing is rendered in
    its own way and therefor shouldn't show up in the list of a person's
    contents.
    """
    implements(iimaginary.IElectromagneticMedium)

    def isOpaque(self):
        """
        I am opaque, so that clothing will show up only once (in your "wearing"
        list, rather than there and in your "contained" list), and obscured
        clothing won't show up at all.
        """
        return True




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
