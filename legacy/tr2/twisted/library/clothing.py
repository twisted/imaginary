from twisted.reality import *

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

def new_slot_dict():
	new={}
	for slot in slots:
		new[slot]=[None]
	return new

def clothing_descript(player):
	desc=[player.He_She,' is wearing ']
	try:
		clothes=player.clothing
	except:
		return '' # %s is naked!!
	descd=[]
	for slot in slots:
		item=clothes[slot][-1]
		if item and item not in descd:
			if descd:
				desc.append(', ')
			desc.append(item.worn_appearance)
			descd.append(item)

	if len(desc) > 3:
		desc.insert(len(desc)-1,'and ')
	if len(desc) < 3:
		return ''
	desc.append('.')
	return desc
	
class Clothing(Thing):

	wearer=None
	clothing_appearance=None
	
	def __wear(self, player):
		try:
			clothes=player.clothing
		except:
			clothes=new_slot_dict()
			player.clothing=clothes

		for location in self.clothing_slots:
			clothes[location].append(self)

		self.wearer=player
		self.component=1
		# should add myself as an observer for name changes...
		player.description['clothing']=clothing_descript(player)

	def __remove(self):
		if self.wearer:
			wearer=self.wearer
			clothes=self.wearer.clothing
			for location in self.clothing_slots:
				cloth=clothes[location][-1]
				if cloth is not self:
					raise Failure("You'd have to remove ",cloth," first.")
			for location in self.clothing_slots:
				clothes[location].pop()
			del self.component
			del self.wearer
			wearer.description['clothing']=clothing_descript(wearer)
			
	def worn_appearance(self,observer):
		if self.clothing_appearance:
			return self.clothing_appearance
		return self.aan(observer)+self.short_name(observer)

	def verb_wear(self, sentence):
		assert not self.wearer, "That's already being worn."
		self.__wear(sentence.subject())

	def verb_remove(self, sentence):
		assert sentence.subject() is self.wearer, "You're not wearing that."
		self.__remove()

class Shirt(Clothing):
	clothing_slots=["chest",
					"left arm",
					"right arm"]

class Pants(Clothing):
	clothing_slots=["left leg",
					"right leg"]

class Cloak(Clothing):
	clothing_slots=["right arm",
					"left arm",
					"left leg",
					"right leg"]

class Robe(Clothing):
	clothing_slots=["right arm",
					"left arm",
					"left leg",
					"right leg"]

class Hat(Clothing):
	clothing_slots=["crown"]

class Necklace(Clothing):
	clothing_slots=["neck"]
class Cape(Clothing):
	clothing_slots=["neck"]

class Shoes(Clothing):
	clothing_slots=["left foot",
					"right foot"]
class Socks(Clothing):
	clothing_slots=["left foot",
					"right foot"]

class Shorts(Clothing):
	clothing_slots=Pants.clothing_slots

class Belt(Clothing):
	clothing_slots=['waist']

class Tie(Clothing):
	clothing_slots=['neck']

class Tunic(Clothing):
	clothing_slots=['chest']

class Blindfold(Clothing):
	# TODO: make this actually blind you!
	clothing_slots=['left eye',
					'right eye']

class Coat(Clothing):
	# TODO: make this openable/closable!
	clothing_slots=['left arm',
					'right arm']

class Spectacles(Clothing):
	clothing_slots=['left eye',
					'right eye',
					'right ear',
					'left ear']
