from twisted.reality import Thing
from twisted.observable import Dynamic

class Describer(Dynamic):
	def __init__(self, car):
		self.car=car
	def evaluate(self, observer, hash, key):
		car=self.car
		if observer.place is car: return car.interior
		else: return car.exterior

	def __repr__(self): # I AM CHEATING HERE
		return "inherit.car.Describer(t(%s))"%repr(self.car.name)

class Car(Thing):
	"""
	This is a car. You can do everything with it that you should be
	able to do with any ford runabout -- except drive it. It is
	broken, and won't start. It will sometimes make a loud scary noise
	when you attempt to start it though, which can be useful later in
	the game. (See BFNT section below.) You'll need the starter crank
	to start it, although it's conveniently located in the trunk,
	along with the brochure.
	"""
	def verb_enter(self, sentence):
		sentence.subject.place=self
		sentence.subject.hears("You enter the car.")

	def verb_exit(self, sentence):
		sentence.subject.place=self.place
		sentence.subject.hears("You exit the car.")
	
	def __init__(self, name):
		Thing.__init__(self,name)
		self.description=Describer(self)

class Trunk(Thing):
	"""
	This is the trunk part of the car.
	"""

	def verb_open(self, sentence):
		self.description=self.opened

	def verb_close(self, sentence):
		self.description=self.closed
