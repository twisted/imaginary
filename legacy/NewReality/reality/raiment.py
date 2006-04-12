# -*- test-case-name: reality.test_reality -*- 
"""Things that can be worn."""

from twisted.python import components 

from reality import things
from reality import errors
from reality import actions
from reality.text import english


class Wear(actions.TargetAction):
    def formatToActor(self):
        return "You put on ",self.target,"."
    def formatToOther(self):
        return self.actor," puts on ",self.target,"."
    def doAction(self):
        t = self.target.getComponent(IWearTarget)
        a = self.actor.getComponent(IWearActor)
        if t.wearer == a:
            raise errors.ActionFailed("You were already wearing ",t,".")
        t.dress(a)

class Unwear(actions.TargetAction):
    def formatToActor(self):
        return "You take off ",self.target,"."

    def doAction(self):
        t = self.target.getComponent(IUnwearTarget)
        a = self.actor.getComponent(IWearActor)
        if t.wearer == a:
            t.undress(a)
        else:
            raise errors.ActionFailed("You weren't wearing ",t,".")
        
class Wearable(components.Adapter):
    __implements__ = IWearTarget, IUnwearTarget    
    wearer = None
    clothingAppearance = None
    clothingStyle = None

    def clothingSlots(self):
        if self.clothingStyle is None:
            raise errors.ActionFailed(self, " appears to be an incomplete garment...")
        return _clothingNames[self.clothingStyle]

    def setStyle(self, clothingStyle):
        # TODO: some events or something to stop things getting stuck in slots
        self.clothingStyle = clothingStyle

    def dress(self, wearer):
        self.wearer = wearer
        clothes = wearer.clothing        
        for location in self.clothingSlots():
            clothes[location].append(self)        
        wearer.describeClothing()

    def undress(self, wearer):
        clothes = wearer.clothing
        for location in self.clothingSlots():
            cloth = clothes[location][-1]
            if cloth is not self:
                raise errors.ActionFailed("You'd have to remove ",cloth," first.")
        for location in self.clothingSlots():
            clothes[location].pop()
        self.wearer = None
        wearer.describeClothing()


class Wearer(components.Adapter):
    __implements__ = IWearActor, IUnwearActor

    def __init__(self, original):
        components.Adapter.__init__(self, original)
        self.clothing = {}
        for slot in slots:
            self.clothing[slot]=[None]

    def getClothing(self, slot):
        """wearer.get(slotname) -> Clothing or None
        
        Returns a piece of clothing if a player is wearing something in that
        slot, or None if not.
        """
        assert slot in slots, "That's not a valid slot: %s" % slot
        return self.clothing[slot][-1]

    def describeClothing(self):
        """Uninplemented until i understand english.Noun better."""

slots = [
    "crown",
    "left eye",
    "right eye",
    "left ear",
    "right ear",

    "neck",
    "chest",

    "left arm",
    "right arm",
    "left wrist",
    "right wrist",
    "left hand",
    "right hand",
    "left fingers",
    "right fingers",

    "waist",
    "left leg",
    "right leg",
    "left ankle",
    "right ankle",
    "left foot",
    "right foot"
    ]

_clothingNames = {"shirt": ["chest",
                            "left arm",
                            "right arm"],
                  "pants": ["left leg",
                            "right leg"],
                  "shorts": ["left leg",
                             "right leg"],
                  "cloak": ["right arm",
                            "left arm",
                            "left leg",
                            "right leg"],
                  "gloves": ["right hand",
                             "left hand"],
                  "robe": ["right arm",
                           "left arm",
                           "left leg",
                           "right leg"],
                  "crown": ["crown"],
                  "necklace": ["neck"],
                  "cape": ["neck"],
                  "shoes": ["left foot",
                            "right foot"],
                  "socks": ["left foot",
                            "right foot"],
                  "belt": ['waist'],
                  "tie": ['neck'],
                  "tunic": ['chest'],
                  "blindfold": ['left eye',
                                'right eye'],
                  "coat": ['left arm',
                           'right arm'],
                  "spectacles": ['left eye',
                                 'right eye',
                                 'right ear',
                                 'left ear'],
                  "hat": ["crown"],
                  }


class WearUnwearParser(english.Subparser):
    simpleTargetParsers = {
        "wear": Wear,
        "unwear": Unwear,
        "put on": Wear,
        "take off": Unwear,
        "remove": Unwear
        }

english.registerSubparser(WearUnwearParser())

components.registerAdapter(Wearer, things.Movable, IWearActor)
components.registerAdapter(Wearer, things.Movable, IUnwearActor)
