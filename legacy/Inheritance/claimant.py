"""
Player Characters for Inheritance
"""

from Reality.player import Author

##class Shiver(Skill):
##    name="shiver"
##    def run(self, sentence):
##        sentence.subject.hears("I see you've learned to shiver.")

class Claimant(Author):
    def destroy(self):
        self.hears( '***** YOU HAVE DIED *****')
        self.hears("Would you like to RESTART, RESTORE, or QUIT?")
        self.restricted_verbs=['restart','restore', 'quit']
        self.noverb_messages=["I'm sorry.  You can only RESTART, RESTORE, or QUIT."]

    def ability_quit(self, sentence):
        self.hears("Uhmm.. That hasn't been implemented. Have a nice day.")

    def ability_save(self, sentence):
        fn=sentence.directString()+".isav"
        from cPickle import dump
        dump(self.reality,open(fn,'w'))
        self.hears("Saved.")
        
    def ability_restore(self, sentence):
        try:
            fn=sentence.directString()+".isav"
            from cPickle import load
            root=load(open(fn))
            f=self.intelligence
            del self.intelligence
            root[self.name].intelligence=f
            f.seeEvent("Restored.")
        except IOError:
            sentence.subject.hears("No such file: "+fn)

##    unfortunately broken...
##    def ability_restart(self, sentence):
##        import inherit.grounds
##        reload (inherit.grounds)
##        f=self.intelligence
##        del self.intelligence
##        Inheritance.grounds.damien.intelligence=f
##        f.seeEvent("Restarted.")
        
##    def ability_learn(self, sentence):
##        self.addSkill(Shiver)
##        self.hears("You learn to shiver.")
        
##    ability_think=ability_learn
    
##    def ability_forget(self, sentence):
##        self.removeSkill(Shiver)
##        self.hears("You forget how to shiver.")
