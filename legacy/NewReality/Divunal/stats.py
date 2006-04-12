#!/usr/bin/env python

from random import randint, random
from math import log

one_day=60*60*24 # sixty seconds * sixty minutes * 24 hours
magic_time=60*10 # ten minutes...?

def coinflip():
    return randint(0,1)

def make_modifier():
    """
    Okay kiddies, this is the GNUPLOT expression used to
    obtain the really funky-ass randomization routine.
    hemhem.

    plot [0:1] [0:1] (-( (log( (x + 0.01) * 100 ) ) / log(10))+2)/2
    
    For all you english speaking types, this returns a number
    between -1 and +1, but much distributed in such a way that
    numbers at or close to 0 are more common, and numbers
    approaching 1 are much less likely.
    """
    rand=random()
    coin=randint(0,1)
    modifier=((-((log((rand+0.01)*100))
                 /log(10))
               +2)
              /2)

    if coinflip():
        return -modifier
    else:
        return modifier
    

class PlayerStats:
    """
    A mixin class that provides some statistical stuff.  (Obviously,
    mix it in with Player)
    """
    def stat_get_current(self,statname):
        return getattr(self,statname)+self.mojo

    def stat_check(self, statname):
        stat=self.stat_get_current(statname)
        return (stat > modifier())

    def weighted_check(self, statname, statbase):
        """
        weighted_check performs a statistics check of the Player's
        requested stat from a base other than zero, and returns the
        difference.
        
        For example, bob.weighted_check('strength',0.5) would be based
        on the comparatively high value of 0.5 rather than the average
        of 0.  A positive number would indicate the degree of Bob's
        success, and a negative number would indicate the extent of
        his failure.
        """

        return self.stat_get_current(statname) - (make_modifier()+statbase)

    def combined_stat_check(self, other, statname, statbase):
        """
        Does a weighted check based on the total of the two players
        involved, for cooperative efforts, as complex as like Mind
        Speak and Mental Chorus, and as simple as many people pushing
        a stone out of the way.
        """

        stat=self.stat_get_current(statname)
        stat=stat+other.stat_get_current(statname)
        stat=stat-(make_modifier()+statbase)
        return stat

    def opposed_stat_check(self, other, statname, advantage):
        stat=self.stat_get_current(statname)+advantage
        stat=stat+other.stat_get_current(statname)
        stat=stat+make_modifier()
        return stat

    def set_health(self,health):
        self._health=health
        self._health_time=time()
        
    def get_health(self):
        """
        whenever you say player.health, it updates the player's
        current health with whatever they would have recovered over
        time since the last check.
           
        BTW: Players will normally regenerate their health (up to 1.0)
        in 24 hours (864 x 10^5 Milliseconds). This rate is also
        governed by the Player's Healing Factor. A healing factor of 0
        has no effect, 0.5 will double recovery speed, -0.5 will halve
        it, etc.
        """
        old_health=self._health
        old_time=self._health_time
        current_time=time()
        healing_factor=self.healing_factor

        heal_time=one_day*(healing_factor+1.)
        new_health=((current_time-old_time)/heal_time)
        new_health=new_health+old_health

        if new_health>1:
            health=1

        self._health=new_health
        self._health_time=current_time
        return new_health

    def set_stamina(self,stamina):
        self._stamina=stamina
        self._stamina_time=time()
        
    def get_stamina(self):
        """
        In short, whenever you say player.stamina, it updates the
        player's current stamina with whatever they would have
        recovered over time since the last check. Stamina is capped at
        the player's max stamina (their endurance, which runs from -1
        to 1), and also cannot be proportionately higher than their
        current health.
        
        BTW: Players will normally regenerate their stamina completely in
        10 minutes (864 x 10^5 Milliseconds). A healing factor of 0 has 
        no effect, 0.5 will double recovery speed, 1.5 will halve it, etc.
        """
        old_stamina=self._stamina
        old_time=self._stamina_time

        max_stamina=self.endurance+1
        current_time=time()
        current_health=self.health+1
        healing_factor=self.healing_factor
        
        heal_time=magic_time*(healing_factor+1)
        new_stamina=((current_time-old_time)/heal_time)+old_stamina
        if new_stamina > max_stamina:
            new_stamina=max_stamina
        if (new_stamina/max_stamina) > current_health:
            new_stamina=max_stamina*current_health

        new_stamina=new_stamina-1 # put it back on a -1 to +1 scale

        self._stamina=new_stamina
        self._stamina_time=current_time
        return new_stamina

    def minor_stun(self, amount):
        "Inflict Stamina damage, but never knock the subject unconcious."
        stamina=self.stamina
        amount=amount * (1 - self.defense)
        stamina=stamina-amount
        if stamina < -1:
            stamina = -1
        self.stamina=stamina
        return stamina

    def major_stun(self, amount):
        "Inflict Stamina damage, with the possibility of being knocked out."
        stamina=self.stamina-(amount*(1-self.defense))
        if stamina < -1:
            downtime = (stamina + 0.9) * -100
            # self.knock_out(downtime)
            stamina=-1

        self.stamina=stamina
        return stamina

    def minor_wound(self, amount):
        "Inflict health damage, but with no possibility of being killed."

    def major_wound(self, amount):
        """
        Inflict health damage. The target player may be knocked out or
        killed if the damage is sufficient.
        """

    

