# Space Opera - A Multiplayer Science Fiction Game Engine
# Copyright (C) 2002 Jean-Paul Calderone
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	 See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
#

# System imports
import random

# Twisted imports
from twisted.python.components import Interface, implements

# Reality imports
from Reality.beyondspike import NoTargetAction, TargetAction, ToolAction, codeInterfaceForAction
from Reality.phrase import registerAdapter, registerSubparser, Subparser, Parsing, IParsing
from Reality.thing import Thing
from Reality.container import Box

# Sibling imports
import space

class IInsertTarget(Interface):
    """A target into which things can be inserted."""
    def targetActionInsert(self, target, tool):
        pass

class IInsertTool(Interface):
    """A tool which can be inserted into something."""
    def toolActionInsert(self, actor, target):
        pass

class Insert(ToolAction):
    pass
exec codeInterfaceForAction(Insert)

class CurrencyVerbs(Subparser):
    def parse_insert(self, player, text):
        """
        Handles these cases:
        
        'insert <currency> into <target>'
        """
        prep = ' into '
        i = text.find(prep)
        if i != -1:
            currency = text[:i]
            target = text[i + len(prep):]
            if len(currency) > 0 and len(target) > 0:
                currencyObj = player.locate(currency, IInsertTool)
                targetObj = player.locate(target, IInsertTarget)
                return [Insert(player, targetObj, currencyObj)]
        return []

registerSubparser(CurrencyVerbs())

class Coin(Thing, space.Located):
    __implements__ = (IInsertTool,)

    NAMES = {1: 'penny', 5: 'nickle', 10: 'dime', 25: 'quarter'}

    cents = 0    
    def __init__(self, cents = 25, name = None, reality = ''):
        if name is None:
            if Coin.NAMES.has_key(cents):
                name = Coin.NAMES[cents]
            else:
                name = '%d cent piece'
        Thing.__init__(self, name, reality)
        self.cents = cents

    def sameAs(self, other):
        return isinstance(other, Coin) and self.cents == other.cents or 0

    def __hash__(self):
        return id(self)

    def minimalChange(amount):
        amnts = Coin.NAMES.keys()
        amnts.sort()
        amnts.reverse()
        result = []
        while amount:
            for i in amnts:
                if amount - i >= 0:
                    result.append(Coin(i))
                    amount = amount - i
                    break
        return result
    minimalChange = staticmethod(minimalChange)


class VendingMachine(Box, space.Located):
    __implements__ = (Box.__implements__, IInsertTarget)

    DEFAULT_PRODUCTS = [('quiche', 150, 700), ('chex mix', 75, 500), ('brains', 25, 250)]
    surface = 0
    coinage = 0
    products = None

    def __init__(self, name = 'vending machine', items = None, reality = ''):
        Thing.__init__(self, name, reality)
        self.products = items and items or self.DEFAULT_PRODUCTS[:]
        self.description = "It's a vending machine.  It's got, you know, food in it.  It sells: \n"
        for i in self.products:
            self.description = self.description + '%10s: $%d.%02d\n' % ((i[0],) + divmod(i[1], 100))

    def targetActionInsert(self, tool, actor):
        if not isinstance(tool, Coin):
            strs = self.action_insert(tool, actor)
        else:
            strs = {'to_other': (actor, ' tries to put ', coin, ' into ', self, '.'),
                    'to_subject': (coin, " won't fit into ", self, '.')}
        apply(actor.broadcastToOne, (), strs)

    def action_insert(self, coin, actor):
        if random.random() >= 0.05:
            self.coinage = self.coinage + coin.cents
        coin.destroy()
        subject = 'You insert ', coin,' into ', self, '.  It clinks.  ', self, (' now reads $%d.%02d.' % divmod(self.coinage, 100))
        other = actor, ' puts ', coin, ' into ', self, '.'
        return {'to_subject': subject, 'to_other': other}

    def action_buttonPress(self, presser, name, button):
        if name == 'return':
            to_other = presser, ' presses the coin return button on ', self, '.'
            to_subject = 'You press the coin return button on ', self, '.'
            if self.coinage == 0:
                to_subject = to_subject + ('  Nothing happens.',)
            elif random.random() >= 0.05:
                for i in Coin.minimalChange(self.coinage):
                    i.move(destination = self, actor = self)
                to_subject = to_subject + ('  You hear some change fall into ', self, "'s coin return slot.")
                self.coinage = 0
            else:
                to_subject = to_subject + ('  The display resets to $0.00, but no change falls into the coin return.',)
                self.coinage = 0
        elif button is None:
            presser.hears('There is no ', name, '.')
            return
        else:
            to_other = presser, 'presses the ', button[0], ' button on ', self, '.'
            to_subject = 'You press the ', button[0], ' button on ', self, '.'
            if self.coinage < button[1]:
                to_other = to_other + ('  ', self, ' buzzes loudly.')
                to_subject = to_subject + ('  ', self, 'buzzes loudly.')
            else:
                self.coinage = self.coinage - button[1]
                food = Food(button[0], button[1])
                food.location = self
                to_other = to_other + ('  You hear a clunk from ', self, '.')
                to_subject = to_subject + ('  You hear a clunk from ', self, '.')
                if self.coinage:
                    for i in Coin.minimalChange(self.coinage):
                        i.location = self
                    to_other = to_other + ('  You hear some change fall into ', self, "'s coin return.")
                    to_subject = to_subject + ('  You hear some change fall into ', self, "'s coin return.")
                    self.coinage = 0
        presser.broadcastToOne(to_other = to_other, to_subject = to_subject)

    def verb_press_on(self, sentence):
        presser = sentence.subject
        button = sentence.directString().lower()

        if button.startswith('coin return') or button.startswith('change return'):
            self.action_buttonPress(presser, 'return', None)
        else:
            for i in self.products:
                if button == i[0].lower() + ' button':
                    self.action_buttonPress(presser, button, i)
                    return
            self.action_buttonPress(presser, button, None)

registerAdapter(VendingMachine, VendingMachine, IInsertTarget)
