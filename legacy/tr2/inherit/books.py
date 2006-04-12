from twisted.reality import Thing


class Necronomicon(Thing):
	"""
	A partial german translation of the book commonly referred to as
	the Necronomicon, complete with illustrations. This is the book
	your grandfather has been obsessing over, and it holds the rituals
	he has been using to summon and bind the servants of the old
	ones. It also contains the rites which, if performed correctly,
	might allow you to undo some of what he has done. (Only an
	inserted set of pages in the middle of the book are actually
	readable, the rest are simply described as being horrible and
	unintelligible, although there should still be just enough that
	you can flip through manually for it to be confusing.)
	"""

	def verb_read(self, sentence):
		sentence.subject.hears("You read the necronomicon.  And go crazy and die.")
		sentence.subject.die()

class Translator(Thing):
	"""
	"A Practical Guide to Egyptian Hieroglyphs, by Lord Rutherford
	P. Beaucavage, Esquire"

	This does what it sounds like it does... Namely, it gives vague
	symbolic translations of the egyptian hieroglyphs found on a few
	of the artifacts in the house.
	"""

	def verb_read(self, x):
		""" read the translator book, displaying its reading text """
		x.subject.hears(self.read_text)

class LeRoiEnJaune(Thing):
	"""
	A rather obtuse play in two parts. After reading the introduction
	and an excerpt from a poem recited in the first act, it begins to
	become rather confusing, and any additional attempts to read it
	leave the player somewhat disoriented, eventually causing them to
	pass out. The player would then have a strange dream about a lost
	city, a pallid mask, and a King in Yellow, which they might not
	wake up from. (This doesn't have much of a connection to any of
	the other plot elements in Inheritance, but it is the sort of
	thing we can integrate later if we get bored.)
	"""
	def verb_read(self, x):
		k=King("King in Yellow")
		k.description="Woah.  He looks totally fucking nasty.  Like, I can't even tell you."
		k.place=x.place
		
	
