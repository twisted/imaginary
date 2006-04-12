
from twisted.reality import Thing, InappropriateVerb, PseudoSentence

from random import randint

class Leaflet(Thing):
	def verb_read(self, sentence):
		import os
		os.system('more pamphlet.txt')
	verb_look=verb_read

class Gun(Thing):
	"""
	What would a survival horror game be without a gun! It might not
	be your standard-issue combination shotgun/flamethrower with a
	laser sight, but it does shoot.

	"""
	def __init__(self, *args, **kw):
		apply(Thing.__init__,(self,)+args,kw)
		self.must_hit=0
		self.misses=0
		
	def verb_shoot(self, sentence):
		d=sentence.direct_object()
		x=self.must_hit or not randint(0,100)
		if self.things and self.things[0].things:
			clip=self.things[0]
			bullet=clip.things[0]
			casing=Casing(bullet.name+" casing")
			casing.description="This is the casing from a %s."%bullet.name
			casing.place=sentence.subject.place
			bullet.die()
		else:
			sentence.subject.hears("*click*")
			return 0
		if x:
			sentence.subject.hears("** BANG! **  The gun's aim is true!  You hit ",sentence.subject,'!')
			d.die()
		else:
			sentence.subject.hears("** BLAM! **  Your hand is jerked forcefully out of line with the target, and the bullet goes wide.")
			self.misses=self.misses + 1
			if self.misses == 2:
				self.must_hit = 1
			
	verb_fire=verb_shoot
	
	autoverbs={"shoot":"with",
			   "fire":"with"}

class TypeContainer(Thing):
	def verb_put(self, sentence):
		container=sentence.indirect_object("in")
		if isinstance(container,self.container_class) and sentence.direct_object() is self:
			if self.place is not container:
				self.place=container
				sentence.subject.hears("You put ",self," in ",container,".")
			else:
				sentence.subject.hears(self, " is already in ",container,".")
		else:
			raise InappropriateVerb()

class Clip(TypeContainer):
	container_class=Gun
	"""
	It should accept both literal and conceptual commands (both "load
	gun" and "put clip in gun", maybe even "load gun with clip" like
	it used to) and keep most of the functionality of the original
	(rackable slide, misfires, etc).
	"""
	def verb_load(self, sentence):
		"load <gun> with <clip>"
		self.verb_put(PseudoSentence(
			subject=sentence.subject,
			verb="put",
			objects={"":sentence.indirect_object("with"),
					 "in":sentence.direct_object()}
			))

	autoverbs={"load":"with"}

class Casing(Thing):
	""" An expired bullet. """

class Bullet(TypeContainer):
	container_class=Clip
	
	"""
	As noted earlier, the ammo fairy hasn't visited this mansion yet
	either, so you've only got the bullets that your grandfather
	actually purchased for it. That means you have a dented bullet, a
	dirty bullet, and a moldy bullet. Strangely enough, all three will
	work -- however, you're not a very good shot, and the gun may
	misfire. If you put all three bullets into the gun and fire them
	all at one thing, you are garuanteed to hit at least once. You may
	hit more than that.
	"""

class Lamp(Thing):
	pass

class Matchbook(Thing):
	"""
	These are for feeding to the psychic worms on level 3. Yum! They
	love sulphur! Ahem. That was sarcasm. They're for lighting the
	lamp, and they can also make fire, but less of it. They don't last
	long as light-sources go (about 2 moves or so, or 60 seconds in
	multiplayer). You should be able to light them in the dark, with
	some difficulty, but holding a lit match as a light source should
	be inconvenient (affects your ability to carry lots of stuff, has
	a chance of going out prematurely when you move, etc.)
	"""

class Match(Thing):
	pass

class Knife(Thing):
	"""
	It starts the game in the knife rack, and you can use it to cut a
	few things... But for the most part, it really isn't that
	useful. Unlike the other random useless objects you can find,
	there are some places you could use it, and it could also be used
	as a weapon, (although given the circumstances, it's really not
	that useful.)
	"""

	def verb_cut(self, x):
		x.subject.hears("You attempt to cut ",x.direct_object(),
						", but the knife isn't very sharp.")

class Gloves(Thing):
	"""
	A pair of thick leather work gloves, the only wearable item you
	will probably find in Inheritance. While wearing the gloves, your
	hands are protected from various nasty poisonous things described
	later. There's no real drawback to wearing them, although I think
	since they're thick and described as being too big for you, it
	should drastically increase the chance of breaking/dropping
	matches when you try to light one, and taking them on/off might
	require that you put your stuff down first. (Put all on table? ;-)
	"""

	def verb_wear(self, sentence):
		pass

	def verb_remove(self, sentence):
		pass
	

class Nightshade(Thing):
	"""
	This was originally going to be part of the ritual the player
	needed to perform to undo what his or her grandfather had
	started. The plant essentially needs to be burned as incense, but
	it is growing in the strange patch of woods near the west end of
	the Darkened Road, and is covered in poisonous thorns as well. If
	you aren't wearing gloves when you pick it, you get poisoned (and
	die after hallucinating for a little while) and if you handle it
	later without the gloves, there is still a chance of it happening.
	"""

	def verb_eat(self, sentence):
		sentence.subject.hears("You die.  You go to hell, and you die.  Like, really.  You die a lot.  bad.")
		sentence.subject.die()

	def verb_take(self, sentence):
		sentence.subject.hears("There should be some time-delay stuff happening here, but we'll deal with that later.")
		sentence.subject.die()


