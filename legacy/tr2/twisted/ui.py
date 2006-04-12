
from reality import Intelligence

from cStringIO import StringIO

import string
import sys
import time

"""
User Intelligence.  This contains some sample implementations of
intelligences.
"""

cols=80
rows=24

shortcuts = {
	"n":"go north",
	"ne": "go northeast",
	"e": "go east",
	"se": "go southeast",
	"s": "go south",
	"sw": "go southwest",
	"w": "go west",
	"nw": "go northwest",
	"u": "go up",
	"d": "go down",
	"l": "look",
	"i": "inventory",
	"z": "wait"
}

class RemoteIntelligence:
	"""
	An interface to preserve bandwidth, and keep the number of remote
	references minimal.  This wasn't strictly necessary, but it seems
	cleaner to have it.
	"""
	def name(self, name):                        pass
	def item_add(self, thing, parent, value):    pass
	def item_remove(self, thing, parent):        pass
	def items_clear(self):                       pass
	def exit_add(self, direction):               pass
	def exit_remove(self, direction):            pass
	def exits_clear(self):                       pass
	def description_add(self, key, desc):         pass
	def description_remove(self, key):             pass
	def descriptions_clear(self):                  pass
	def event(self, string):                       pass
	# ain't nothin' you can do about this.
	def request(self, question,default,ok,cancel): pass

class LocalIntelligence(Intelligence):
	"""
	This translates local intelligence calls to remote intelligence
	calls.
	"""
	remote=None
	def __init__(self,remote):
		self.remote=remote
	def name(self, name):
		self.remote.name(name)
	def item_add(self, thing,name):
		self.remote.item_add(id(thing),
							 id(thing.place),
							 name)
	def item_remove(self, thing):
		self.remote.item_remove(id(thing),
								id(thing.place))
	def items_clear(self):
		self.remote.items_clear()
	def exit_add(self, direction, exit):
		self.remote.exit_add(direction)
	def exit_remove(self, direction):
		self.remote.exit_remove(direction)
	def exits_clear(self):
		self.remote.exits_clear()
	def description_add(self, key, description):
		self.remote.description_add(key,description)
	def description_remove(self, key):
		self.remote.description_remove(key)
	def descriptions_clear(self):
		self.remote.descriptions_clear()
	def event(self, string):
		self.remote.event(string)
	def request(self, question,default,ok,cancel):
		self.remote.request(question,default,ok,cancel)

class ConsoleIntelligence(Intelligence):
	"""
	This provides a minimally useful console interface to TR.
	"""
	dflag=0
	def __init__(self):
		self.items={}
		self.descriptions={}
		self.exits={}
		self.olddescs={}
		self.items_mark=1
		self.exits_mark=1
		self.descriptions_mark=1
		self.hq=[]

	def name(self, name):
		self.event('[ %s ]'%name)

	def item_add(self, thing,name):
		self.items[thing]=thing.aan(self.thing)+thing.short_name(self.thing)
		self.items_mark=1

	def item_remove(self, thing):
		del self.items[thing]
		self.items_mark=1

	def items_clear(self):
		self.items={}
		self.items_mark=1

	def exit_add(self, direction, exit):
		self.exits[direction]=exit
		self.exits_mark=1

	def exit_remove(self, direction):
		del self.exits[direction]
		self.exits_mark=1

	def exits_clear(self):
		self.exits={}
		self.exits_mark=1

	def description_add(self, key, description):
		self.descriptions[key]=description
		self.descriptions_mark=1

	def description_remove(self, key):
		del self.descriptions[key]
		self.descriptions_mark=1

	def descriptions_clear(self):
		self.descriptions={}
		self.descriptions_mark=0
	
	def event(self, string):
		self.hq.append(string)
		# self.hq=self.hq[-9:]
		
	def format(self,st):
		lines=0
		q=1
		xx=string.split(string.replace(st,'\n',' '),' ')
		for i in xx:
			q=q+len(i)+1
			if q>cols:
				self.cout.write('\n')
				q=len(i)+1
				lines=lines+1
			self.cout.write(i)
			self.cout.write(' ')
		self.cout.write('\n')
		return lines+1

	def show_state(self):
		l=0

		self.cout=StringIO()

		for i in self.hq:
			l=l+self.format(i)
		self.hq=[]
		
		if self.descriptions_mark:
			st=string.join(map(str,self.descriptions.values())," ")
			if not self.olddescs.has_key(st) or self.dflag:
				self.olddescs[st]=1
				l=l+self.format(st)
				self.dflag=0
			self.descriptions_mark=0
			
		if self.items_mark and self.items:
			self.cout.write('\n')
			l=l+self.format ("You see: "+string.join(self.items.values(),", "))
			self.items_mark=0
			
		if self.exits_mark:
			self.cout.write('\n')
			l=l+self.format ("Obvious Exits: "+string.join(self.exits.keys(),", "))
			self.exits_mark=0
			
		self.cout.write("\n")
		
		# for i in xrange((rows-2)-l):
		# 	self.cout.write("\n")
			
		self.cout.write("> ")
		for i in self.cout.getvalue():
			sys.stdout.write(i)
			sys.stdout.flush()
			time.sleep(0.000001)
		del self.cout

	def run_input(self):
		try:
			while 1:
				self.show_state()
				x=raw_input()
				# self.event("> %s"%x)
				try: x=shortcuts[x]
				except: pass
				
				# hack hack, but then what isn't, in this file?
				
				if x[:4]=='look':
					self.dflag=1
					self.descriptions_mark=1
				self.thing.execute(x)
				self.thing.reality.run()
		except SystemExit:
			self.show_state()

