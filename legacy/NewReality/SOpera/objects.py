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
import random, string

# Sibling imports
import space, portal

# Reality imports
from Reality import thing, container, electronic


class Ship(thing.Thing, space.Located, portal.Portal):
    __implements__ = (
        thing.Thing.__implements__,
        space.Located.__implements__,
        portal.Portal.__implements__
    )

    __all = {}

    def __init__(self, name, airlock, registry = None, reality = ''):
        thing.Thing.__init__(self, name, reality)
        portal.Portal.__init__(self, airlock)

        self.registry = registry or Ship.generateRegistry()
        self.__all[self.registry] = self


    def __setstate__(self, state):
        self.__dict__ = state
        self.__all[self.registry] = self


    def generateRegistry():
        a = ''.join([random.choice(string.letters) for x in range(6)])
        b = ''.join([random.choice(string.digits) for x in range(10)])
        c = ''.join([random.choice(string.letters) for x in range(2)])
        return '%s-%s-%s'.join((a, b, c))
    generateRegistry = staticmethod(generateRegistry)


class RadioFactory(container.Container, electronic.Electronic, space.Located):
    __implements__ = (
        container.Container.__implements__,
        space.Located.__implements__,
        electronic.Electronic.__implements__
    )
    
    surface = 0

    def dispenseRadio(self):    
        r = Radio()
        r.location = self

    def action_dispense(self, actor):
        self.dispenseRadio()
        actor.broadcastToOne(
            to_subject = ('You press the dispense button on ', self, '.'),
            to_other = (actor, ' presses the dispense button on ', self, '.')
        )
        self.broadcast(self, ' whirs and spits out ', r, '.')
    
    def targetActionActivate(self, actor):
        self.action_activate(actor)
        self.action_dispense(actor)
        self.turnOff()


class NavigationPanel(thing.Thing, electronic.Electronic, space.Located):
    def verb_examine(self, sentence):
        if isinstance(self.location.location, sopera.SpaceRoom):
            ship = self.locaiton.location
            s = """
     Coordinates:   %s
     Velocity:      %s
     Acceleration:  %s""" % (ship.coordinates, ship.velocity, ship.acceleration)
            sentence.subject.hears(s)
        else:
            sentence.subject.hears('%s is not installed on any ship.' % self.nounPhrase())


class Food(thing.Thing, space.Located):
    def __init__(self, name, calories, reality = ''):
        thing.Thing.__init__(self, name, reality)
        self.calories = calories

    def action_taste(self, taster):
        to_other = taster, ' takes a taste of ', self, '.'
        if taster.isFull():
            to_subject = "You just can't eat any more!"
        else:
            to_subject = 'It tastes like ', self, '.'
            taster.consumeCalories(min(10, self.calories / 10))
            self.calories = self.calories - min(10, self.calories / 10)
            if self.calories <= 0:
                to_subject = to_subject + '  You have finished ', self, '.'
                self.destroy()
        taster.broadcastToOne(to_subject = to_subject, to_other = to_other)

    def verb_taste(self, sentence):
        self.action_taste(sentence.subject)

    def action_eat(self, eater):
        to_other = eater, ' eats ', self, '.'
        if eater.isFull():
            to_subject = "You just can't eat any more!"
        else:
            to_subject = 'You eat ', self, '.'
            eater.consumeCalories(self.calories)
            self.destroy()
        eater.broadcastToOne(to_subject = to_subject, to_other = to_other)

    def verb_eat(self, sentence):
        self.action_eat(sentence.subject)


