#!/usr/bin/env python

from reality import *
from reflect import named_module, refrump

import string
from cStringIO import StringIO
from traceback import print_exc
from cPickle import dump



def discover(name,x,y,z,
			 north=1,east=1,west=1,south=1,up=1,down=1):
	# this is arbitrary, so:
	#    pos   neg
	# z= north-south
	# y= up-down
	# x= east-west
	matrix=[]
	for i in range(x):
		xrow=[]
		for j in range(y):
			zrow=[]
			for k in range(z):
				zrow.append(Room('%s (%d,%d,%d)'%(name,i,j,k)))
			xrow.append(zrow)
		matrix.append(xrow)
	for i in range(x):
		for j in range(y):
			for k in range(z):
				if south:
					if k > 0:
						matrix[i][j][k].add_exit('south',matrix[i][j][k-1])
				if north:
					if k < z-1:
						matrix[i][j][k].add_exit('north',matrix[i][j][k+1])
				if west:
					if i > 0:
						matrix[i][j][k].add_exit('west',matrix[i-1][j][k])
				if east:
					if i < x-1:
						matrix[i][j][k].add_exit('east',matrix[i+1][j][k])
				if down:
					if j > 0:
						matrix[i][j][k].add_exit('down',matrix[i][j-1][k])
				if up:
					if j < y-1:
						matrix[i][j][k].add_exit('up',matrix[i][j+1][k])
					
				
	return matrix



class Author(Player):
	def __init__(self,*args,**kw):
		apply(Player.__init__,(self,)+args,kw)
		self.code_space={'self':self,
						 'Thing':Thing
						 #'__builtins__':None
						 }
		
	wizbit=1
	def ability_adduser(self, sentence):
		name=sentence.direct_string()
		p=Player(name)
		p.place=self.place
		self.hears('poof')

	def findskill(self, sentence):
		skillname = sentence.indirect_string('to')
		
		try:
			skill=self.code_space[skillname]
			assert isinstance(skill,Skill)
		except:
			Failure("No such skill as %s -- did you import it?")
		
	def ability_allow(self, sentence):
		player    = sentence.direct_object()
		skill=findskill(self,sentence)
		player.add_skill(skill)
		
	def ability_disallow(self, sentence):
		player    = sentence.direct_object()
		skill=findskill(self,sentence)
		player.add_skill(skill)

	def execute(self, string):
		self.begin_sync()
		# self.hears("< "+repr(string))
		try:
			if string[0]=='$':
				try:
					return self.runcode(string[1:])
				except RealityException, re:
					self.hears(re.format(self))
					return re
			else:
				return Player.execute(self,string)
		finally:
			#self.hears("ending execution: "+repr(string))
			self.end_sync()

	def runcode(self, cmd):
		fn='$'+self.name+'$'
		try:    code=compile(cmd,fn,'eval')
		except:
			try: code=compile(cmd,fn,'single')
			except:
				Failure("That won't compile.")

		try:
			val=eval(code,self.code_space)
			if val is not None:
				self.hears(repr(val))
				return val
		except:
			sio=StringIO()
			print_exc(file=sio)
			v=sio.getvalue()
			Failure(v)

	def ability_describe(self,sentence):
		"""describe object

		this will prompt you for a description.  enter something."""
		obj=sentence.direct_object()
		# ha ha, python can do lexical closures good enough for me
		def setdesc(desc, obj=obj):
			obj.description=desc
		def forgetit(obj=obj): pass
			#print 'forgot it, %s'%obj.name

		try:
			desc=obj.description['__MAIN__']
		except KeyError:
			desc=""
			
		if type(desc)==type(""):
			self.request("Please describe %s"%obj.noun_phrase(self),desc,
						 setdesc,forgetit)
		else:
			self.hears(
				"That object's description is a dynamic property -- "
				"(%s, to be precise) -- you probably shouldn't mess "
				"with it directly.  Take a look at the source for details."
				%str(desc))
		
	def ability_mutate(self, sentence):
		"""mutate object to new_type

		This will mutate an object into a different type of object.
		"""
		mutator=sentence.direct_object()
		try:
			newtype=sentence.indirect_string('to')
			newtype=self.code_space[newtype]
		except:
			Failure("You don't know of any such type.")
		newtype=getcurrent(newtype)
		x=issubclass(newtype,getcurrent(Thing))
		assert x, "You shouldn't mutate Things to types which are not Things."
		if not isinst(mutator,newtype):
			mutator.__class__=newtype

	def ability_scrutinize(self,sentence):
		"""scrutinize object

		display some code which may be helpful..."""
		
		object=sentence.direct_object()
		
		stio=StringIO()
		def writ(bytes,stio=stio):
			stio.write(bytes)
			stio.write('\n')

		object.print_source(writ)
		self.hears(stio.getvalue())

	def ability_import(self, sentence):
		"""import (object|.python.object) [to varname]

		If you have a pathname that starts with a '.', this will
		attempt to load a module and import the last thing on the
		dotted path.  (For example, if you say 'import
		.twisted.reality.Thing', that would be equivalent to 'from
		twisted.reality import Thing'.  Otherwise, it attempts to
		search for an object and import it as the synonym you
		specify. (Spaces will be replaced with underscores.)
		"""
		
		ds=sentence.direct_string()
		if ds[0]=='.':
			ds=ds[1:]
			if ds:
				dt=string.split(ds,'.')
				dt=map(string.strip,dt)
				if len(dt)==1:
					st='import %s'%dt[0]
				else:
					st='from %s import %s'%(string.join(dt[:-1],'.'),dt[-1])
				self.runcode(st)
				self.hears("%s: success."%st)
		else:
			dt=sentence.direct_object()
			ds=string.replace(ds,' ','_')
			self.code_space[ds]=dt
			self.hears("You remember %s as %s."%(dt.noun_phrase(self),repr(ds)))

	def ability_reload(self, sentence):
		"""reload (name|.python.name)

		This will reload either a Thing (reloading its toplevel module
		(the one that its class is in) and changing its class as
		appropriate. this won't always be adequate, but works for most
		simple cases), an object in your namespace, or a qualified
		python module name (prefixed with a dot).
		"""

		ds=sentence.direct_string()

		if ds[0]=='.':
			module=ds[1:]
			reload(named_module(module))
		else:
			try:    object=self.code_space[ds]
			except:	object=sentence.direct_object()

			if isinst(object,Thing):
				refrump(object)
			else:
				reload(object)
	def ability_persist(self, sentence):
		"""persist mapname

		This will create a file called mapname.rp, containing the
		saved state of the current game."""

		file=open(sentence.direct_string()+'.rp','wb')
		from twisted.reality import default_reality # did we reload? huh?
		dump(default_reality,file)
		file.flush()
		file.close()
		
		self.hears('Saved "%s.rp".'%sentence.direct_string())

	def ability_source(self, sentence):
		file=open(sentence.direct_string()+"_rp.py",'wb')
		def writeln(bytes,file=file):
			file.write(bytes);file.write('\n')
		default_reality.print_source(writeln)

	def ability_dig(self, sentence):
		direction=sentence.direct_string()
		try:
			name=sentence.indirect_string('to')
		except:
			name="Untitled Room"
		r=Room(name)
		self.place.exits[direction]=r
		r.exits[reverse(direction)]=self.place

from geometry import revdict

def reverse(direction):
	try:   return revdict[direction]
	except KeyError: return 'back'
