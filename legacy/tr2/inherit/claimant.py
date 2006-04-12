
from twisted.reality import Skill
from twisted.author import Author

class Shiver(Skill):
	name="shiver"
	def run(self, sentence):
		sentence.subject.hears("I see you've learned to shiver.")

class Claimant(Author):
	def die(self):
		self.hears( '***** YOU HAVE DIED *****')
		self.hears("Would you like to RESTART, RESTORE, or QUIT?")
		self.restricted_verbs=['restart','restore','quit']
		self.noverb_messages=["I'm sorry.  You can only RESTART, RESTORE, or QUIT."]
	def ability_quit(self, sentence):
		import sys
		sys.exit(0)
		
	def ability_save(self, sentence):
		fn=sentence.direct_string()+".isav"
		from cPickle import dump
		dump(self.root,open(fn,'w'))
		self.hears("Saved.")
		
	def ability_restore(self, sentence):
		try:
			fn=sentence.direct_string()+".isav"
			from cPickle import load
			root=load(open(fn))
			f=self.intelligence
			del self.intelligence
			root[self.name].intelligence=f
			f.event("Restored.")
		except IOError:
			sentence.subject.hears("No such file: "+fn)

	def ability_restart(self, sentence):
		import inherit.grounds
		reload (inherit.grounds)
		f=self.intelligence
		del self.intelligence
		inherit.grounds.damien.intelligence=f
		f.event("Restarted.")
		
	def ability_learn(self, sentence):
		self.add_skill(Shiver)
		self.hears("You learn to shiver.")
		
	ability_think=ability_learn
	
	def ability_forget(self, sentence):
		self.remove_skill(Shiver)
		self.hears("You forget how to shiver.")
