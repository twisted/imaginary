#!/usr/bin/env python

from Reality.room import Room
from random import random, randint

class Cloudscape(Room):
    messages=(
        (0.1, "The clouds are as tranquil as a lake on a cool summer's night."),
        (0.4,  "The clouds look slightly turbulent.  They are swirling around in little eddies."),
        (0.6, "The clouds are very turbulent.  They are swirling and thundering quite a bit."),
        (0.63, "The clouds are violent. They are spinning around rapidly, creating vortices and soft thunder everywhere.")
        )

    cloudiness=0.0
    
    def fling(self):
        coinflip=randint(0,1)
        cloudiness=self.cloudiness
        
        if coinflip:
            if cloudiness > 0:
                cloudiness=cloudiness-(random()/10)
        else:
            cloudiness=cloudiness+(random()/10)
            
        if cloudiness>0.65:
            lcn = self.fling_place
            for thing in self.things:
                thing.hears("The clouds roil and rise up to engulf you, gently lifting you off of your feet and pulling you somewhere else...")
                thing.location = lcn
            cloudiness = 0.
        for threshhold, message in self.messages:
            if cloudiness < threshhold:
                self.describe('cloudiness',message)
                break
                
        self.cloudiness=cloudiness
