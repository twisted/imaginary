from tokenizer import Tokenizer
from reality import Thing,default_reality,Container,Room,Player
import traceback
import cPickle
import crypt
import types
from reference import Reference, AttributeReference

from token import *
from tokenize import *
from author import Author

class PORMap(Tokenizer):
	def name(self, thing):
		thing.name=self.next().value
	
	def desc(self, thing):
		thing.description=self.next().value

	def readPerspective(self):
		self.backtrack()
		isName=(self.next().value == 'Name')
		# technically, this could be 'pos' or 'obj' for pronouns, but
		# ... ahh ...  I have every map that I knew of ever made with
		# TR, and not a single one of them takes advantage of at
		# feature, so 'of' is good enough a guess
		ofOrOf=(self.next().value == '0') # 0 or 1, lowercase or caps
		self.next() # ignore, left paren
		# (again, technically, this could be a second argument to
		# 'name' that specifies who owns the pronoun, but I think this
		# will be done differently anyway (and as I said before,
		# nothing uses this feature))
		thingName=self.next().value
		self.next() # ignore, right paren
		if isName:
			return AttributeReference(thingName,'noun_phrase')
		else:
			return AttributeReference(thingName,['him_her','Him_Her'][ofOrOf])
	
	def readList(self):
		val=self.next().value
		if val == '{':
			val=[]
			vl=self.next()
			while vl.value != '}':
				if vl.ttype != STRING:
					if vl.value != ',':
						val.append(self.readPerspective())
				else:
					val.append(vl.value)
				vl = self.next()
		return val
		
	def prop(self, thing):
		key = self.next().value
		value = self.readList()
		key=self.strmung(key)
		if key == 'name':
			key = 'display_name'
		setattr(thing,key,value)

	def strmung(self,key):
		key=string.replace(key,' ','_')
		key=string.replace(key,'#','')
		key=string.replace(key,"'",'')
		key=string.replace(key,".",'')
		key=string.replace(key,",",'')
		key=string.replace(key,"!",'')
		return key
		
	def handle(self,thing):
		event=self.next().value
		value=self.next().value
		# thing.putHandler(event,value)
		# no point...
		
	def thing(self, thing):
		key = self.next().value
		value = self.next().value
		key=self.strmung(key)
		setattr(thing, key, Reference(value))
	
	def descript(self,thing):
		key = self.next().value
		value = self.readList()
		thing.description[key]=value
		
	def place(self, thing):
		placename = self.next().value
		thing.place=Reference(placename)
		
	def exit(self, thing):
		direction=self.next().value
		self.next() # to
		roomname=self.next().value
		iswith=self.next().value
		if iswith == 'with':
			doorname=self.next().value
			# print 'cant handle doors right now'
		else:
			self.backtrack()
		thing.add_exit(direction,Reference(roomname))
	
	def syn(self,thing):
		sn=self.next().value
		thing.add_synonym(sn)

	def super(self,thing):
		x=self.next().value
		thing.OBSOLETE_super=Reference(x)

	def theme(self,thing):
		thing.theme=self.next().value

	def persistableXXX(self,thing):
		# since pickle should take care of this, this is STRICTLY so
		# we don't error out while reading the map.
		self.next() # this would be the key
		self.next() # this would be the classname
		korv=self.next().value # either key or value
		if korv == 'val':
			self.next() # read the value string
			self.next() # read the word 'key'
		self.next() # read the key
		
	def wizbit(self, thing):
		thing.__class__=Author
	def nop(self,thing):
		pass
	
	def mood(self, thing):
		self.next()
		
	def gender(self, thing):
		thing.gender=self.next().value

	def password(self, thing):
		pw = self.next().value
		pw = crypt.crypt(pw,pw)
		print 'UNCRYPTED USER'

	def component(self, thing):
		thing.component=1
		
	def passwd(self,thing):
		pw=self.next().value
		# crypted passwords aren't useful to me...
		
	def feature(self,thing):
		classname=self.next().value # yeah, like this will do us any good
		modname=string.lower(classname)
		# and guess what, it doesn't...
		# thing.putVerb(modname)
	
	def __init__(self,filename,worldname):
		Tokenizer.__init__(self,filename)
		self.worldname=worldname
		self.filename=filename
		
	def parse(self):
		laters=[]
		nt=self.next()
		pytr=default_reality
		parseCommand={'name': self.name,
					  'describe': self.desc,
					  'descript': self.descript,
					  'syn': self.syn,
					  'theme': self.theme,
					  'extends': self.super,
					  'place': self.place,
					  'feature': self.feature,
					  'ability': self.feature,
					  'mood': self.mood,
					  'gender': self.gender,
					  
					  'int': self.prop,
					  'long': self.prop,
					  'string': self.prop,
					  'property': self.prop,
					  'float': self.prop,
					  'double': self.prop,
					  'boolean': self.prop,
					  
					  # the following two probably need fixing of some sort
					  'thing': self.thing,
					  'handler': self.handle,
					  'persistable': self.persistableXXX,
					  
					  'password': self.password,
					  'passwd': self.passwd,
					  
					  'opaque': self.nop,
					  'architect': self.wizbit,
					  'component': self.component,
					  'broadcast': self.nop,
					  'shut': self.nop,
					  'claustrophobic': self.nop,
					  
					  'exit': self.exit}
		while nt.ttype != ENDMARKER:
			#print 'This should be Thing, Location or Room: '+nt.value
			tlor=nt.value
			if tlor == 'Location':
				tlor='Container'
			tlor=eval(tlor)
			
			nt=self.next()
			#print 'This should be {: '+nt.value
			nt=self.next()
			t=tlor('noname')
			while nt.value != '}':
				later=parseCommand[nt.value](t)
				nt=self.next()
			nt=self.next()
		pytr.resolve_all()
		return pytr

# reality pickle stuff

def loadReality(filename):
	f=open(filename,'rb')
	pytr=cPickle.load(f)
	f.close()
	tr.addReality(pytr)
	return pytr

