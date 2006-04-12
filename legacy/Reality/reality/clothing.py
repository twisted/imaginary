# -*- test-case-name: reality.test_reality -*-

# Twisted, the Framework of Your Internet
# Copyright (C) 2001 Matthew W. Lefkowitz
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of version 2.1 of the GNU Lesser General Public
# License as published by the Free Software Foundation.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


"""
Clothing support for twisted reality.
"""

# twisted imports
from twisted.persisted import styles

# reality imports
from reality import thing, error
from reality.player import Player

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


from actions import NoTargetAction, TargetAction, ToolAction
from twisted.python.components import Interface, registerAdapter, Adapter
from phrase import Subparser, registerSubparser

class Wear(TargetAction):
    pass

class Unwear(TargetAction):
    pass

class WearUnwearParser(Subparser):
    simpleTargetParsers = {
        "wear": Wear,
        "unwear": Unwear,
        "put on": Wear,
        "take off": Unwear,
        "remove": Unwear
        }

registerSubparser(WearUnwearParser())

class Wearable(Adapter):
    __implements__ = IWearTarget, IUnwearTarget

    wearer = None
    clothingAppearance = None

    def actionTargetWear(self, action):
        """ Cause a particular piece of clothing to be worn by a wearer.
        """
        t = self.getComponent(thing.Thing)
        wearer = action.actor
        clothes = wearer.clothing
        for location in self.clothingSlots:
            clothes[location].append(self)
        self.wearer = wearer
        self.component = 1
        # TODO: add myself as an observer for name changes...
        wearer.describeClothing()

    def actionTargetUnwear(self, action):
        """ Remove a piece of clothing.
        """
        wearer = action.actor
        assert wearer is self.wearer
        clothes = self.wearer.clothing
        for location in self.clothingSlots:
            cloth = clothes[location][-1]
            if cloth is not self:
                raise error.Failure("You'd have to remove ",cloth," first.")
        for location in self.clothingSlots:
            clothes[location].pop()
        self.component = 0
        self.wearer = None
        wearer.describeClothing()

    def wornAppearance(self, observer):
        if self.clothingAppearance:
            return self.clothingAppearance
        return self.aan(observer) + self.shortName(observer)


class Clothing(thing.Thing, styles.Versioned):
    """Obsoleted thing-inheriting junk.
    """

    def __init__(self, name, r=''):
        thing.Thing.__init__(self, name, r)
        wb = Wearable(self)
        wb.clothingSlots = self.clothingSlots
        self.addComponent(wb, True)
        self.__class__ = thing.Thing

    persistentVersion = 1
    def upgradeToVersion1(self):
        wb = Wearable(self)
        if hasattr(self, 'wearer'):
            wb.wearer = self.wearer
            del self.wearer
        if hasattr(self, 'clothing_appearance'):
            wb.clothingAppearance = self.clothing_appearance
            del self.clothing_appearance
        self.__class__ = thing.Thing
        self.addComponent(wb)

class Wearer(Adapter):
    __implements__ = IWearActor, IUnwearActor

    def __init__(self, original):
        Adapter.__init__(self, original)
        self.clothing = {}
        for slot in slots:
            self.clothing[slot]=[None]

    def describeClothing(self):
        desc = [self.original.capHeShe, ' is wearing ']
        clothes = self.clothing
        descd = []
        for slot in slots:
            item = clothes[slot][-1]
            if item and item not in descd:
                if descd:
                    desc.append(', ')
                desc.append(item.getComponent(IWearTarget).wornAppearance)
                descd.append(item)
        if len(desc) > 3:
            desc.insert(len(desc)-1,'and ')
        if len(desc) < 3:
            return ''
        desc.append('.')
        self.original.describe('clothing', desc)

    def getClothing(self, slot):
        """clothing.get(player, slot name) -> Clothing or None
        
        Returns a piece of clothing if a player is wearing something in that
        slot, or None if not.
        """
        assert slot in slots, "That's not a valid slot: %s" % slot
        return self.clothing[slot][-1]



registerAdapter(Wearer, Player, IWearActor)
registerAdapter(Wearer, Player, IUnwearActor)

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

# stupid hack... there will be real classes here later as we add the abilities
# to open and close clothes.

for k, v in _clothingNames.items():
    s = """
class Wear%s(Wearable):
    clothingSlots = %r

class %s(Clothing):
    clothingSlots = %r
""" % (k.capitalize(), v, k.capitalize(), v)
    # print s
    exec s

del k
del v
