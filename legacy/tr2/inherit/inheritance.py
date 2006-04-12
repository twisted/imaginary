
from twisted import reality
from twisted.observable import Dynamic
from random import randint

from car import Car, Trunk
from claimant import Claimant

from tools import Gun,Clip,Bullet
from tools import Lamp,Matchbook,Match
from tools import Knife,Gloves,Nightshade
from tools import Leaflet

from monsters import Sarcophagus, Mummy, Doll, BFNT

from books import Translator, Necronomicon, LeRoiEnJaune

class ThingFactory:
	def create(self, name, initdesc):
		t=reality.Thing(name)
		t.description=initdesc
		return t



