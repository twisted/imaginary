from twisted.reality import *
from twisted.library.door import Door
reality=default_reality
story="RUINS"
headline="""An Interactive Worked Example
Copyright (c) 2000 Graham Nelson
Revisited 1998 by Roger Firth
Translation to Twisted Reality by Glyph Lefkowitz"""

release=3
serial="000711"

# pretty printing utilities; should these be part of the standard tr?
t=reference.Reference
def d(**kw): return kw
	


# a little single-player game cheating
Thing.visited=0

class Protagonist(Thing):
	score=0
	winning=100
	def add_score(self,score):
		self.score=self.score+score
		if self.score==self.winning:
			reality.loop(packing_case.endgame)
			self.hears("The case is full, and you're feeling really homesick.  Now, how to get out of here?")

	def ability_go(self,sentence):
		Thing.ability_go(self,sentence)
		# TODO: real event handlers for movement...
		self.place.visited=1

hero=Protagonist("Dashing Hero")(
	place=t("Dark Forest"))
	
class Packing_Case(Thing):
	number=0
	def verb_take(self,sentence):
		sentence.subject.hears(
			"The case is too heavy to bother moving, as long as your expedition is still incomplete.  It'll probably have to be taken out by helecopter."
			)
	drop_phrases=[
		"You hear the distant drone of an aeroplane.",
		"The plane is much louder, and seems to be flying very low. Terrified birds rise in screeching flocks.",
		"You involuntarily crouch as the plane flies directly overhead, seemingly only inches above the treetops. With a loud thump, something drops heavily to the ground.",
		"The roar dies away; calm returns to the forest."
		]

	def boxdrop(self):
		# okay, this gets awkward...
		if hero.place==forest:
			hero.hears(self.drop_phrases[self.number])
		if self.number==len(self.drop_phrases)-2:
			if hero.place != forest:
				hero.hears("Even underground, the engine roar is deafening. Then there's a dull thump overhead and a little dust falls from the ceiling.")
			self.place=forest
		elif self.number == len(self.drop_phrases)-1:
			self.number=0
			delay.StopLooping()
			
		self.number=self.number+1
	raise_phrases=["A deep throbbing noise can be heard.",
				   "A helicopter appears, hovering overhead.",
				   "The helicopter lowers a rope; you tie it around the packing case, which is hauled up into the air, then a rope ladder comes dangling down. With one last look around the clearing, you climb the ladder into the waiting craft. Back to civilisation, and a decent pint of Brakspear's!"]

	def endgame(self):
		hero.hears(raise_phrases[self.number])
		if self.number == len(raise_phrases)-1:
			hero.win()
			delay.StopLooping()

		self.number=self.number+1
		
	verb_remove=verb_take
	verb_push=verb_take

packing_case=Packing_Case("packing case")(
	# note: twisted reality _does not use_ 'initial'... it should though
	initial="Your packing case rests here, ready for you to hold any important cultural finds you might make, for shipping back to civilisation.",
	description="A stout wooden crate, only slightly battered by its fall through the branches.",
	synonyms=['packing','case','crate','box','strongbox']
	)

class Treasure(Thing):
	cultural_value=10

	def verb_take(self,sentence):
		if self.place.name == "packing case":
			sentence.subject.hears("Unpacking such a priceless artifact had best wait until the Metropolitan Museum can do it.")
		else:
			raise InappropriateVerb()
	verb_remove=verb_take

	def action_insert(self, where):
		hero.add_score(self.cultural_value)
		self.place=where
		
	def verb_insert(self, sentence):
		self.action_insert(sentence.indirect_object('into'))

	def verb_put(self,sentence):
		self.action_insert(sentence.indirect_object('in'))

statuette=Treasure("pygmy statuette")(
	synonyms=['pygmy','statuette','statue','mayan','snake','spirit'],
	description="A menacing, almost cartoon-like statuette of a pygmy spirit with an enormous snake around its neck.")
	
Treasure("silver bangle")(
	synonyms=['silver','bangle','bracelet','ring'],
	cultural_value=20,
	description="An intricately chased piece of jewellery.")

Treasure("blood-red ruby")(
	synonyms= ['blood','red','blood-red','ruby','stone','jewel'],
	cultural_value=20,
	description="A vivid red jewel, as large as a hen's egg.")

class Honeycomb(Treasure):
	def verb_eat(self,sentence):
		# possible limitation of TR: this shouldn't have to be a
		# separate class.  A property like string_eat=... should be
		# able to take care of this, as it appears to be fairly
		# common.
		sentence.subject.hears("Perhaps the most expensive meal of your life.  The honey tastes odd, perhaps because it was used to store the entrails of the king buried here, but still like honey.")
		self.die()
		
Treasure("lump of wax")(
	description="On closer examination, the lump appears to be an old honeycomb.",
	# I don't think this does anything for me since there's no "edible" class...
	edible=1
	)



forest=Room("Dark Forest")(
	synonyms=['forest','jungle','clearing','olive','tree','trees','midges'],
	description="In this tiny clearing, the pine-needle carpet is broken by stone-cut steps leading down into the darkness. Dark olive trees crowd in on all sides, the air steams with warm recent rain, midges hang in the air.",
	exits=d(down=t("Stone-Cut Steps"),
			up="The trees are spiny and you'd cut your hands to ribbons trying to climb them."
			),
	cant_go="The rainforest-jungle is dense, and you haven't hacked through it for days to abandon your discovery now. Really, you need a good few artifacts to take back to civilisation before you can justify giving up the expedition."

	)


class Mushroom(Thing):
	general=0
	def verb_eat(self, sentence):
		from random import randint
		if randint(0,100)>30:
			sentence.subject.hears("You nibble at one corner, but the curious taste repels you.")
		else:
			sentence.subject.hears("The tiniest nibble is enough.  It was a toadstool, and a poisoned one at that!")
			sentence.subject.die()
	def verb_drop(self, sentence):
		# this is like an "after"... I guess it's more wordy, but it
		# makes lots of sense to me
		sentence.subject.ability_drop(sentence)
		
		# interesting feature of inform to note; not only does it
		# combine these actions and make them nice and brief, it
		# manages to have returning something _after_ the drop phase
		# alter the flavor text that the verb generates by returning a
		# string from the after handler.
		# clever.
		if self.place.sunlit:
			trails.place=self.place
			sentence.subject.hears("You drop the mushroom on the floor, in the glare of the shaft of sunlight.  It bubbles obscenely, distends and then bursts into a hundred tiny insects which run for the darkness in every direction, leaving strange trails in the sandy floor.  No trace of fungus remain.")
			self.die()
		else:
			sentence.subject.hears("The mushroom drops to the ground, battered slightly.")
	def verb_take(self,sentence):
		sentence.subject.ability_take(sentence)
		if self.general:
			# again, what I *really* want to say here is "return <string>"
			sentence.subject.hears("You pick up the slowly-disintegrating mushroom.")
		else:
			self.general=1
			sentence.subject.hears("You stoop to pick the mushroom, neatly cleaving its thin stalk. As you straighten up, you notice what looks like a snake in the grass.")
			# this is not very twisted-reality like.  It should not be
			# actually *moving* the statuette, it should be making you
			# *notice* the statuette.
			statuette.place=sentence.subject.place

square_chamber=Thing("Square Chamber")(
	synonyms=['square','chamber','sand','dust','lintel','lintels','lintelled',
			  'east','south','doorways','doors','steps'],
	description="A sunken, gloomy stone chamber, ten yards across, whose floor is covered with fine sandy dust.  A shaft of sunlight cuts in from the steps above, giving the chamber a diffuse light, but in the shadows low lintelled doorways to east and south lead into the deeper darkness of the Temple.",
	sunlit=1,
	exits=d( up=t('Dark Forest')
			 # east=t('Inner Web'),
			 # south=t('Corridor') 
			 )
	)

# this talks about door properties, but there is absolutely nothing
# door-like about it.  need to enhance the door class.

stone_steps=Door("stone-cut steps")(
	synonyms=['stone','stone-cut','steps','stairs','cobwebs'],
	place=t("Dark Forest"),
	description="The cracked and worn steps descend into a dim chamber. ",
	destination=t("Square Chamber"),
	# door_dir="down", # is this necessary?
	door_state="open"
	)

stone_steps.description['other']=observable.Dynamic(
	lambda a,b,c,sq=square_chamber: (
		["Cobwebs form a flimsy barrier, unlikely to impede your descent.","The filmy cobwebs which once spanned the entrance now hang in tatters."][sq.visited]
		))

mushroom=Mushroom("speckled mushroom")(
	place=t("Dark Forest"),
	synonyms=['speckled', 'mushroom', 'fungus', 'toadstool'],
	description="The mushroom is capped with blotches, and you aren't at all sure it's not a toadstool."
	)

# 'Ephemera' class, subclass of Scenery, maybe?
Thing("shaft of sunlight")(
	description="The shaft of sunlight glimmers motes of dust in the air, making it seem almost solid."
	)

carvnames=['carved','inscription','inscriptions','carving','carvings','group','of']

Thing("carved inscriptions")(
	place=t("Square Chamber"),
	synonyms=carvnames
	)
	

reality.resolve_all()

if __name__=='__main__':
	from twisted.ui import ConsoleIntelligence
	print story
	print
	print headline
	print
	hero.place=forest
	# this needs to be done for real!
	#dark.description = "The darkness of ages presses in on you, and you feel claustrophobic."
	ci=ConsoleIntelligence()
	hero.intelligence=ci
	reality.loop(packing_case.boxdrop)
	ci.run_input()
