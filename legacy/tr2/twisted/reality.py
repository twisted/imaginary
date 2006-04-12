#!/usr/bin/env python

"""
Twisted Reality ](|?)[

Even animals die.
"""

# python system imports

import types
import random
import string
import sys
from popen2 import popen2
from cStringIO import StringIO
from copy import copy, deepcopy

# twisted matrix imports

import pickleplus, tokenizer, sentence, reference
import observable, reference, delay
from reflect import isinst, Settable, getcurrent, Accessor
from threading import RLock, currentThread

class RealityException(Exception):
	"""RealityException()

	This is the base superclass of all formattable exceptions."""
	def __init__(*args,**kw):
		apply(Exception.__init__,args,kw)
	
class InappropriateVerb(Exception):
	"""InappropriateVerb()

	This exception is not formattable: raise it if you want to cease
	executing and default to another verb down the parse chain."""

class Ambiguous:
	def __init__(self):
		self.data={}
	def put(self, key,value):
		if type(key)==types.StringType:
			key=string.lower(key)
		try:
			x=self.data[key]
			x.append(value)
		except:
			self.data[key]=[value]
			
	def get(self,key):
		if type(key)==types.StringType:
			key=string.lower(key)
		x=self.data[key]
		if len(x) == 1:
			return x[0]
		else:
			raise Ambiguity(key,x)
		
	def remove(self,key,value):
		if type(key)==types.StringType:
			key=string.lower(key)
		x=self.data[key]
		x.remove(value)
		if len(x)==0:
			del self.data[key]

class CantFind(RealityException):
	def __init__(self,name):
		self.name=name
	def format(self, observer=None):
		return "I can't see a %s here." % self.name

class Ambiguity(RealityException):
	def __init__(self, word, list):
		self.word=word
		self.list=list
	def format(self,observer=None):
		x=StringIO()
		x.write("When you say %s, do you mean " % self.word)
		lx=len(self.list)
		i=0
		while i < lx:
			z=self.list[i].noun_phrase(observer=observer)
			if i == lx-1:
				x.write("or %s?"%z)
			else:
				x.write("%s, "%z)
			i=i+1
		return x.getvalue()

class Failure(RealityException):
	def __init__(self,*args,**kw):
		apply(RealityException.__init__,((self,)+args),kw)
		raise self
	def format(self,observer=None):
		if observer:
			return observer.format(self.args)
		else:
			return string.join(self.args)
	
class NoVerb(RealityException):
	errors=["You don't think that you want to waste your time with that.",
			"There are probably better things to do with your life.",
			"You are nothing if not creative, but that creativity could be better applied to developing a more productive solution.",
			"Perhaps that's not such a good idea after all.",
			"Surely, in this world of limitless possibility, you could think of something better to do.",
			"An interesting idea...",
			"A valiant attempt.",
			"What a concept!",
			"You can't be serious."]
	def __init__(self,verb):
		self.verb=verb
	def format(self,observer=None):
		errors=self.errors
		try: errors = observer.noverb_messages
		except: pass
		return errors[random.randint(0,len(errors)-1)]
		
class NoObject(RealityException):
	def __init__(self,mstr):
		self.string=mstr
	def format(self,observer=None):
		return "There is no %s here."%self.string

class NoExit(RealityException):
	def __init__(self,room,string,error=None):
		self.room=room
		self.string=string
		self.error=error
	def format(self,observer=None):
		if self.error: return self.error
		else:          return "You can't go %s from here."%self.string
	
class NoString(RealityException):
	def __init__(self,verb,prep):
		self.verb=verb
		self.prep=prep
	def format(self, observer=None):
		xio=StringIO()
		xio.write("What do you want to ")
		xio.write(self.verb)
		if (self.prep):
			xio.write(" ")
			xio.write(self.prep)
		xio.write("?")
		return xio.getvalue()

class Reality(delay.Delayed,reference.Resolver):
	def __init__(self):
		delay.Delayed.__init__(self)
		reference.Resolver.__init__(self,self)
		self.__counter=0
		self.__ids={}
		self.__names={}
		
	def _add_thing(self,thing):
		self.__counter=self.__counter+1
		thing.thing_id=self.__counter
		self.__ids[thing.thing_id]=thing
		self.__names[thing.name]=thing
		
	def _remove_thing(self,thing):
		if self.__ids.get(thing.thing_id) is thing:
			del self.__ids[thing.thing_id]
		if self.__names.get(thing.name) is thing:
			del self.__names[thing.name]
			
	def unplaced(self):
		return filter(lambda x: not x.place, self.__ids.values())

	get_things=unplaced
	
	def _update_name(self,thing,oldname,newname):
		assert (not oldname) or self.__names[string.lower(oldname)] is thing , 'Bad mojo.'
		if oldname:
			del self.__names[string.lower(oldname)]
		self.__names[string.lower(newname)]=thing
		
	def __getitem__(self,name):
		return self.__names[string.lower(name)]

	def objects(self):
		return self.__ids.values()

	def resolve_all(self):
		return self.resolve(self.objects())

	def print_source(self,write):
		"Create a source representation of the map"
		self.sourcemods={}
		
		write("from twisted.reality import *")
		write("")
		write("t=reference.Reference")
		write("m=reference.AttributeReference")
		write("def d(**kw): return kw")
		write("")

		oo=self.objects()
		oo.sort()
		
		for o in oo:
			o.print_source(write)
			write("")

		write("default_reality.resolve_all()")	
		del self.sourcemods

# note: the following hack makes TR incompatible with JPython.  (I
# would be worried about this, except for the fact that Java sucks too
# much even to have multiplexing I/O so we damned ourselves with use
# of select()... foo on you, sun)

try:
	#have we been loaded yet?
	default_reality
except NameError:
	#if not, init something
	default_reality=Reality()
else:
	# otherwise just make sure that our class is up-to-date
	isinst(default_reality,Reality)


class Intelligence:
	"""
	An 'abstract' class, specifying all methods which TR user
	interfaces must implement.
	"""
	
	def name(self, name):
		pass
	def item_add(self, thing,name):
		pass
	def item_remove(self, thing):
		pass
	def items_clear(self):
		pass
	def exit_add(self, direction, exit):
		pass
	def exit_remove(self, direction):
		pass
	def exits_clear(self):
		pass
	def description_add(self, key, description):
		pass
	def description_remove(self, key):
		pass
	def descriptions_clear(self):
		pass
	def event(self, string):
		pass
	def request(self, question,default,ok,cancel):
		cancel()

class Skill:
	name="SKILL"
	synonyms=()
	def __init__(self, thing):
		if self.name == Skill.name:
			raise Exception ("Unnamed Skill")
		self.score=0
		self.thing=thing

	def run(self, sentence):
		"""Override this."""
		
	def __call__(self, sentence):
		self.run(sentence)


		
class Thing(Accessor,
			observable.Observable,
			Settable):
	"""Thing(name[,reality])

	name: a string, which will be both the unique keyed name of this
	object, and the displayed name.

	reality: an instance of a twisted.reality.Reality.  If not
	specified, this will efault to twisted.reality.default_reality.

	This is Observable, Settable, and an Accessor.
	"""

	####
	# Defaults:
	# here are some useful default constants
	####

	# Version: this is independant of the twisted reality version; it
	# is important so that the pickles can be re-read and frobbed as
	# necessary

	__version=1
	
	# Most rooms aren't doors; they don't "go" anywhere.
	destination = None

	# most things are opaque.
	transparent = 0

	# most things aren't containers; they don't have an "inside", to
	# speak of.  This isn't a hard and fast rule, since it's useful to
	# be able to combine objects in this relationship, but this is a
	# useful hint.
	
	hollow=0

	# See the "room" classes below for more details.
	
	enterable = 0

	antecedent = None

	####
	# Methods:
	####
	
	def __init__(self,name,reality=default_reality):
		observable.Observable.__init__(self)

		self.really_set('synonyms',[])
		self.reality=reality
		reality._add_thing(self)
		
		try:
			self.name=name
		except AssertionError:
			self.name=str(self.thing_id)
			self.display_name=name
			
		self.__contents=observable.Hash()
		self.__index=Ambiguous()
		self.__version=self.__version
		
		self.really_set('description',observable.Hash())
		self.really_set('exits',observable.Hash())
		
		self.__mutex=RLock()


	### Threading
		
	def begin_sync(self):
		self.__mutex.acquire()
		
	def end_sync(self):
		self.__mutex.release()

	### Naming

	name=None
	display_name=None
	
	def set_name(self, name):
		assert type(name)==types.StringType, "Name must be a string."
		
		if name == self.name: return
		self.remove_synonym(self.name)
		oldname=self.name
		self.really_set('name',name)
		self.reality._update_name(self,oldname,name)
		self.add_synonym(name)
		
		if not self.display_name:
			self.notify(self)
			if isinst(self.place,Thing):
				self.place.__namechange(self)

	def __namechange(self, content):
		assert self.__contents.has_key(content), "You can't back-door your way around 'place' this way..."
		self.__contents[content]=content.thing_id # re-set it so clients hear about it again.

	def set_display_name(self, name):
		if type(name)==types.StringType:
			self.add_synonym(name)
		if self.display_name and type(self.display_name) == types.StringType:
			self.remove_synonym(self.display_name)
		self.really_set('display_name',name)
		
		self.notify(self)
		if isinst(self.place,Thing):
			self.place.__namechange(self)

	### Perspectives
		
	article=None

	def indefinite_article(self, observer):
		name=self.short_name(observer)
		if string.lower(name[0]) in ('a','e','i','o','u'):
			return 'an '
		else: return 'a '

	def definite_article(self, observer):
		return 'the '

	aan=indefinite_article
	the=definite_article
	
	unique=0

	# mental note to self -> 'get_name' is gone now, and hasn't been
	# replaced where it's been called (it was a bad name, anyway)
	
	def article(self, observer):
		# TODO: insert some context determination stuff here.
		return self.definite_article(observer)

	def Noun_Phrase(self,observer):
		return string.capitalize(self.noun_phrase(observer))
	
	def noun_phrase(self, observer):
		return self.article(observer)+self.short_name(observer)

	contained_preposition="on"
	
	def present_phrase(self, observer):
		# TODO: "on the chair" style formatting
		place=self.place
		if observer.place == place:
			observed_place="here"
		else:
			observed_place=("%s %s"%(place.contained_preposition,
									 place.noun_phrase(observer)))
			
		return string.capitalize("%s%s is %s."%(self.indefinite_article(observer),
												self.short_name(observer),
												observed_place))
	
		
	def short_name(self, observer):
		dn=self.display_name
		n=self.name
		if dn:
			if isinst(dn, observable.Dynamic):
				return dn(observer)
			else: return dn
		else:
			return n
		
	def get_things(self,observer=None):
		return self.__contents.keys()

	# yay gendered pronouns in english :-(
	
	gender='n'
	
	def __gender(self, observer):
		if isinst(self.gender,observable.Dynamic):
			return self.gender(observer)
		else:
			return self.gender
	
	def him_her(self, observer):
		return {'m':'him','f':'her','n':'it'}[self.__gender(observer)]
	def Him_Her(self, observer):
		return string.capitalize(self.him_her(observer))
	
	def his_her(self, observer):
		return {'m':'his','f':'her','n':'its'}[self.__gender(observer)]
	def His_Her(self, observer):
		return string.capitalize(self.his_her(observer))
	
	def he_she(self, observer):
		return {'m':'he','f':'she','n':'it'}[self.__gender(observer)]
	def He_She(self, observer):
		return string.capitalize(self.he_she(observer))
	
	def format(self, persplist):
		if type(persplist)==types.StringType:
			return persplist
		elif type(persplist)==types.NoneType:
			return ""
		persplist=list(persplist)
		if isinst(persplist[0],Thing):
			persplist[0]=persplist[0]=persplist[0].Noun_Phrase
		x=StringIO()
		for i in persplist:
			if isinst(i,Thing):
				val=i.noun_phrase(self)
			elif callable(i):
				# this could be one of the things we just defined (wrt
				# gender) or it could be an observable.Dynamic
				val=i(self)
			else:
				val=str(i)
			x.write(val)
		return x.getvalue()
	
	def hears(self, *args):
		string=self.format(args)
		if self.has_int():
			self.intelligence.event(string)

	def pair_hears(self,
				   subject,
				   target,
				   to_subject,
				   to_target,
				   to_other):
		"""
		
		Sends a message to a list of 3 parties - an initiator of an
		action, a target of that action, and everyone else observing
		that action.  The messages to each party may be a single
		formattable object, or a list or tuple of such objects, which
		will be formatted by the 'hears' method on each observer.

		Example:
		room.pair_hears(sentence.subject, target,
		to_subject=("You wave to ",target," and ",target.he_she," nods."),
		to_target= (sentence.subject," waves to you, and you nod."),
		to_other=(sentence.subject," waves to ",target," and ",target.he_she," nods.")
		)

		In this example, when bob executes "wave to jethro", the
		effect is:
		
		BOB hears: "You wave to Jethro, and he nods."
		JETHRO hears: "Bob waves to you, and you nod."
		EVERYONE ELSE hears: "Bob waves to Jethro, and he nods."

		This sort of interaction is useful almost anywhere a verb
		enables a player to take action on another player.
		"""
		
		if type(to_subject) not in (types.TupleType,types.ListType):
			to_subject = (to_subject,)
		if type(to_target)  not in (types.TupleType,types.ListType):
			to_target  = (to_target,)
		if type(to_other)   not in (types.TupleType,types.ListType):
			to_other   = (to_other,)
			
		apply(subject.hears,to_subject)
		apply(target.hears,to_target)
		
		map(lambda x, to_other=to_other: apply(x.hears,to_other),
			filter(lambda x, subject=subject, target=target: x not in (subject,target),
				   self.things)
			)
		
	def all_hear(self, *args):
		"""
		Sends a message to everyone in the room.  This method
		should be used when there isn't a specific Player who is the
		source of the message. (an example would be Gate disappearing).

		Its arguments should be in the same form as 'hear'

		Examples: room.all_hear(disembodied_voice," says 'hello'.")
		          room.all_hear("Nothing happens here.")
		"""
		
		map(lambda x, args=args: apply(x.hears,args),
			self.things)

	def one_hears(self, subject, to_subject, to_other):
		"""
		
		Sends a one to everyone in the room except one player, to whom
		a different message is sent.  The arguments may be a valid
		formattable object (a String, Thing, Dynamic, or Exception) or
		a list or tuple of formattable objects.

		Example: room.one_hears(sentence.subject,
		                        to_subject=("You pull on ",knob," but it just sits there.")
								to_other=(sentence.subject," pulls on ",knob," and looks rather foolish."))
		
		"""
		if type(to_subject) not in (types.TupleType,types.ListType):
			to_subject = (to_subject,)
		if type(to_other)   not in (types.TupleType,types.ListType):
			to_other   = (to_other,)
		
		apply(subject.hears,to_subject)
		
		map(lambda x, to_other=to_other: apply(x.hears,to_other),
			filter(lambda x, subject=subject: x != subject,
				   self.things)
			)
		
	def add_observer(self, observer):
		observer(self)
		observable.Observable.add_observer(self,observer)
		
	def has_int(self):
		return hasattr(self,"intelligence")

	def notice_item(self, hash, thing, thing_id):
		if self.has_int():
			if thing is self:
				return
			if thing_id == observable.Gone:
				self.intelligence.item_remove(thing)
			else: self.intelligence.item_add(thing,thing.present_phrase(self))

	def notice_name(self, name):
		if self.has_int():
			self.intelligence.name(self.focus.noun_phrase(self))

	def notice_description(self, hash, key, desc):
		if self.has_int():
			desc=self.format(desc)
			if desc is observable.Gone: self.intelligence.description_remove(key)
			else: self.intelligence.description_add(key,desc)

	def notice_exit(self, hash, direction, exit):
		if self.has_int():
			if exit is observable.Gone: self.intelligence.exit_remove(direction)
			else: self.intelligence.exit_add(direction,exit)
			
	def no_items(self):
		if self.has_int():
			self.intelligence.items_clear()
	def no_descriptions(self):
		if self.has_int():
			self.intelligence.descriptions_clear()
	def no_exits(self):
		if self.has_int():
			self.intelligence.exits_clear()

	def del_focus(self):
		focus=self.focus
		self.really_del('focus')
		if not isinst(focus,Thing): return
		self.no_exits()
		self.no_items()
		self.no_descriptions()

		focus.remove_observer(self.notice_name)
		focus.description.remove_observer(self.notice_description)
		focus.__contents.remove_observer(self.notice_item)
		focus.exits.remove_observer(self.notice_exit)

	def set_focus(self, focus):
		if hasattr(self,'focus'):
			del self.focus
		self.really_set('focus',focus)
		if isinst(focus,Thing):
			focus.add_observer(self.notice_name)
			focus.description.add_observer(self.notice_description)
			focus.__contents.add_observer(self.notice_item)
			focus.exits.add_observer(self.notice_exit)

	def del_intelligence(self):
		del self.intelligence.thing
		self.really_del('intelligence')
			
	def set_intelligence(self, intelligence):
		"""
		Change the intelligence currently governing this Thing.
		"""
		try:   del self.intelligence
		except KeyError: pass
		except AttributeError: pass
			
		self.really_set('intelligence',intelligence)
		self.intelligence.thing=self
		if hasattr(self,'focus'):
			self.focus=self.focus
		else:
			self.focus=self.place

	### Skills
			
	skills=None
	
	def add_skill(self, skill):
		if not self.skills:
			self.skills={}
		s=skill(self)
		self.skills[skill.name]=s
		for i in skill.synonyms:
			self.skills[i]=s

	def remove_skill(self, skill):
		if not self.skills: return
		oldskill=self.skills[skill.name]
		if isinst(oldskill,skill):
			del self.skills[skill.name]
			for i in skill.synonyms:
				if isinst(self.skills[i],skill):
					del self.skills[i]
		if not self.skills:
			del self.skills	

	### Utility Interfaces
			
	def loop(self,*args,**kw):
		apply(self.reality.loop,args,kw)
		
	def later(self,*args,**kw):
		apply(self.reality.later,args,kw)
		
	def add_exit(self, direction, otherroom):
		self.exits[direction]=otherroom

	### Client Interaction

	def request(self, question, default,
				ok, cancel):
		"""Thing.request(question,default,ok,cancel)

		question: a question you want to ask the player
		
		default: a default response you supply
		
		ok: a callable object that takes a single string argument.
		    This will be called if the user sends back a response.
			
	    cancel: this will be called if the user performs an action that
		        indicates they will not be sending a response.  There is
				no garuantee that this will ever be called in the event
				of a disconnection.  (It SHOULD be garbage collected for
				sure, but garbage collection is tricky. ^_^)
		"""
		self.intelligence.request(question,default,ok,cancel)

	def execute(self, sentencestring):
		self.begin_sync()
		try:
			try:
				s=Sentence(sentencestring,self)
				return s.run()
			except RealityException, re:
				self.hears(re.format(self))
				return re
			except AssertionError, ae:
				self.hears(ae.args[0])
		finally:
			self.end_sync()

	
	def get_verb(self, verbstring):
		return getattr(self, 'verb_%s'%verbstring)

	def get_ability(self, verbstring):
		try:
			return getattr(self, 'ability_%s'%verbstring)
		except AttributeError,ae:
			try:
				return self.skills[verbstring]
			except:
				raise ae

	### Placement
			
	place=None
	was_surface=0
	
	def set_place(self,place):
		
		oldplace=self.place
		
		if oldplace:
			del self.place
			
		self.really_set('place',place)
		
		if isinst(place,Thing):
			place.grab(self)

		if self.has_int():
			self.focus=place

	def del_place(self):
		if self.place:
			place=self.place
			if isinst(place,Thing):
				# this is structured in this way so that it's OK
				# if 'toss' throws an exception
				place.toss(self)
			self.really_del('place')
			if hasattr(self,'focus'):
				del self.focus

	# special bits (THE FEWER OF THESE THE BETTER!!!)

	# Special bits change the way that objects are managed, so if the
	# code managing them is buggy, the map will become corrupt.  This
	# is the source of many of the problems that arose with TR 1.
	
	component=0
	surface=0
	
	# To begin with, let's say we'll do transparency without any
	# special bits.  Transparent objects should be able to do things
	# quite easily by subclassing and overriding grab, toss, and find.
	
	def set_surface(self, surf):
		"""
		This sets the 'surface' boolean.  A 'surface' object
		broadcasts its list of contents (including components) to the
		room that it is found in.
		"""
		assert surf == 1 or surf == 0, '"Surface" should be a boolean.'
		if surf == self.surface:
			return
		if self.place:
			if surf:
				for i in self.__contents.keys():
					self.place.grab(i)
			else:
				for i in self.__contents.keys():
					self.place.toss(i)
					
		self.really_set('surface',surf)

	def set_component(self,comp):
		"""
		This sets the 'component' boolean.  A 'component' object is a
		part of the object which contains it, and cannot be moved or
		altered independantly.
		"""
		assert comp == 1 or comp == 0, '"Component" should be a boolean.'
		if comp == self.component:
			return
		
		place=self.place
		
		# this loop updates all containers of this object (since the
		# 'surface' property is designed to cascade recursively...)

		while isinst(place,Thing):
			
			if comp:
				place._ungrab(self)
			else:
				place._grab(self)
				
			# if the place we just set ourselves visible/invisible in
			# is a surface, that means that its container will have a
			# reference to us too; we need to keep going and update it
			# as well.
			
			if place.surface:
				place=place.place
			else:
				break

		self.really_set('component',comp)

	def grab(self, thing):

		if thing.was_surface:
			thing.surface=1
			del thing.was_surface
		
		if self.surface and isinst(self.place,Thing):
			self.place.grab(thing)
		for i in thing.synonyms:
			self.__addref(i,thing)
		if thing.component:
			self._ungrab(thing)
		else:
			self._grab(thing)

	def _grab(self, thing):
		self.__contents[thing]=self.thing_id

	def _ungrab(self, thing):
		self.__contents[thing]=observable.DontTell

	def _toss(self, thing):
		del self.__contents[thing]
		
	def toss(self, thing):
		assert not (thing.component and thing.place is self), "That's a silly idea."
		
		if thing.surface:
			thing.surface=0
			thing.was_surface=1
			
		if self.surface and isinst(self.place,Thing):
			self.place.toss(thing)
			
		for i in thing.synonyms:
			self.__remref(i,thing)
			
		self._toss(thing)
		
	def add_synonym(self,nm):
		if nm in self.synonyms:
			return
		if isinst(self.place,Thing):
			self.place.__addref(nm,self)
		self.synonyms.append(nm)
	
	def remove_synonym(self,nm):
		if (nm == self.name) or (not nm in self.synonyms): return
		
		if isinst(self.place,Thing):
			self.place.__remref(nm,self)
		self.synonyms.remove(nm)
		
	def set_synonyms(self, syns):
		for i in syns:
			self.add_synonym(i)

	def __addref(self,k,t):
		self.__index.put(k,t)

	def __remref(self,k,t):
		self.__index.remove(k,t)
		
	def __repr__(self):
		return "<%s '%s'>" % (self.__class__.__name__,
							  self.name)

	def __del__(self):
		print self,' bit the dust'
	
	def die(self):
		self.component=0
		del self.place
		self.reality._remove_thing(self)

	### Searching
		
	def find(self, name):
		try:
			return self.__index.get(name)
		except KeyError:
			raise CantFind(name)
		
	def locate(self, word):
		searchlist=[self]
		try: searchlist.append(self.place)
		except: pass
		try: searchlist.append(self.focus)
		except: pass
		
		for i in searchlist:
			try: return i.find(word)
			except CantFind: pass
	
		if word == 'here':
			return self.place
		elif word == 'me':
			return self
		elif word == 'this':
			return self.focus
		elif word in ('him','her','it'):
			if self.antecedent:
				return self.antecedent

		raise CantFind(word)

	def find_exit(self, direction):
		try:
			where=self.exits[direction]
		except KeyError:
			raise NoExit(self,direction)
		else:
			if isinst(where,Thing):
				if where.destination:
					return where.destination
				if not where.enterable:
					raise NoExit(self,direction)
				return where
			elif isinst(where,types.StringType):
				raise NoExit(self,direction,where)

	def set_description(self,description):
		if type(description)==types.StringType or isinst(description,observable.Dynamic):
			self.description['__MAIN__']=description
		elif type(description)==types.DictType or isinst(description,observable.Hash):
			self.description.update(description)

		else:
			assert 0, "Not a valid description"
			
			

	def set_exits(self, exits):
		# keep in mind that setting the exits is additive.
		self.exits.update(exits)
			
	### Basic Abilities
			
	def ability_go(self, sentence):
		direct=sentence.direct_string()
		where=self.place.find_exit(direct)
		
		# TODO: calculations as to whether I will *fit* in
		# this wonderful new place I've discovered
		
		self.hears("You go ",direct,".")
		self.place=where

	def ability_look(self, sentence):
		try:
			object=sentence.indirect_object('at')
		except NoString:
			object=self.place
		self.focus=object

	def ability_take(self, sentence):
		object=sentence.direct_object()
		if object.place is self:
			Failure("You were already holding that.")
		else:
			object.place=self
			self.hears(object,": Taken.")

	def ability_wait(self, sentence):
		self.hears("Time passes...")

	def ability_drop(self, sentence):
		object=sentence.direct_object()
		if object.place == self:
			object.place=self.place
			self.hears(object,": Dropped.")
		else:
			self.hears("You weren't holding that.")

	def ability_inventory(self,sentence):
		try:
			obj=sentence.direct_object()
		except:
			obj=self
		self.hears(str(obj.things))

	### Sorting
	
	def __cmp__(self,other):
		if isinst(other,Thing):
			return cmp(string.lower(self.name),
					   string.lower(other.name))
		else: return 1
		
	def __hash__(self): return id(self)

	### Persistence

	def __upgrade_0(self):
		print 'upgrading from version 0 to version 1'

	def __setstate__(self, dict):
		self.__dict__.update(dict)
		self.__mutex=RLock()
		while self.__version != Thing.__version:
			getattr(self,'_Thing__upgrade_%s'%self.__version)()
			self.__version=self.__version+1
	
	def __getstate__(self):
		dict=copy(self.__dict__)
		try:
			del dict['_Thing__mutex']
		except:
			pass
		if dict.has_key('intelligence'):
			i=dict['intelligence']
			if isinst(i,LocalIntelligence):
				del dict['intelligence']

		if dict.has_key('code_space'):
			cs=copy(dict['code_space'])
			if cs.has_key('__builtins__'):
				del cs['__builtins__']
				dict['code_space']=cs
		return dict
	
	def print_source(self,write):
		'''
		this method is REALLY a hack.
		'''
		if self.__class__.__module__!='twisted.reality':
			# ok this should only happen once per file, but okay if it doesn't
			if (not hasattr(self.reality,'sourcemods') or not
				self.reality.sourcemods.has_key(self.__class__.__module__)):
				write("import %s"%self.__class__.__module__)
				if hasattr(self.reality,'sourcemods'):
					self.reality.sourcemods[self.__class__.__module__]=1
				
			write("%s.%s(%s)("%(self.__class__.__module__,
								self.__class__.__name__,
								repr(self.name)))
		else:
			write("%s(%s)("%(self.__class__.__name__,
							 repr(self.name)))

		# now, about that 'hack'...
		dct=copy(self.__dict__)

		# These will all automatically be re-generated when the object
		# is constructed, so they're not worth writing to the file.
		
		del dct['_Thing__contents']
		del dct['_Thing__index']
		del dct['_Thing__mutex']
		del dct['_Thing__version']
		del dct['reality']
		del dct['thing_id']
		del dct['observers']

		# And this has to be specified in the constructor.
		del dct['name']
		
		s=copy(dct['synonyms'])
		s.remove(self.name)
		try: s.remove(self.display_name)
		except ValueError: pass
		if s: dct['synonyms']=s
		else: del dct['synonyms']
		if dct['exits']: dct['exits']=dct['exits'].properties
		else: del dct['exits']
		if dct.has_key('focus'):
			if dct['focus']==dct['place']:
				del dct['focus']

		if dct.has_key('code_space'):
			s=copy(dct['code_space'])
			if s.has_key('__builtins__'):
				del s['__builtins__']
				dct['code_space']=s
				
		if dct.has_key('intelligence'):
			i=dct['intelligence']
			if isinst(i,LocalIntelligence):
				del dct['intelligence']
				
		d=dct['description']
		if len(d)==0:
			del dct['description']
		if len(d)==1 and d.has_key('__MAIN__'):
			dct['description']=d['__MAIN__']

		# whew.  let's just pretend like THAT didn't happen.

		# oh by the way, this is more for human readability than
		# anything.  since you can end up with [...] lists and what
		# have you.

		for k,v in dct.items():
			del dct[k]
			v=sanitize(v)
			if dct: nn=','
			else: nn=''
			write("\t%s=%s%s"%(k,repr(v),nn))
			
		write(")")

# blek; source sanitization routines
		
def san_tuple(o):
	return tuple(san_list(o))

def san_instance(o):
	if isinst(o,Thing):
		return SourceThing(o)
	if isinst(o,observable.Hash):
		return SourceHash(o)
	else: return o # flag a warning here; you're screwed

def san_method(o):
	if isinst(o.im_self,Thing):
		return SourceMethod(o)
	else:
		return o # screwed here too...
	
def san_list(o):
	return map(sanitize,o)

def san_dict(o):
	n={}
	for k,v in o.items():
		n[k]=sanitize(v)
	return n

def sanitize(o):
	try:
		action={types.InstanceType: san_instance,
				types.ListType:     san_list,
				types.DictType:     san_dict,
				types.TupleType:    san_tuple,
				types.MethodType:   san_method}[type(o)]
	except KeyError:
		return o # you *may* also be screwed here; but this also
	             # works for stuff like strings
	else:
		return action(o)
	
class SourceMethod:
	def __init__(self,m):
		self.method=m
	def __repr__(self):
		return "m(%s,%s)"%(repr(self.method.im_self.name),
						   repr(self.method.__name__))

class SourceHash:
	def __init__(self,hash):
		self.hash=hash
	def __repr__(self):
		return "observable.Hash(%s)"%repr(san_dict(self.hash.properties))
	
class SourceThing:
	def __init__(self,th):
		self.thing=th
	def __repr__(self):
		return "t(%s)"%repr(self.thing.name)

class Container(Thing):
	"""Container

	A convenience class, setting a few defaults that wouldn't be reasonable for most stuff.
	"""
	hollow=1

class Room(Container):
	"""Room
	
	A convenience class, setting a few defaults that wouldn't be reasonable for most stuff.
	"""
	enterable=1

class Player(Container):
	"""Player

	This is a player in the world."""

	def indefinite_article(self, observer):
		return ""

	definite_article=indefinite_article
	aan=indefinite_article
	the=definite_article

	
class PseudoSentence:
	def __init__(self, subject=None,verb="",thing="",strings={},objects={}):
		self.subject=subject
		self.verb=verb
		self.verbThing=thing
		self.strings=strings
		self.objects=objects

	def indirect_string(self,string):
		try:
			return self.strings[string]
		except:
			raise NoString(self.verb_string(),string)
		
	def direct_object(self):
		return self.indirect_object('')
	
	def verb_string(self):
		return self.verb
	
	def indirect_object(self, string):
		try:
			return self.objects[string]
		except:
			raise NoObject(self.indirect_string(string))

class Sentence(sentence.Sentence):
	"""
	Represents a single typed phrase by the user, of the form: verb
	[direct-object] [preposition indirect-object] [preposition
	indirect-object]...
	"""
	
	def resolve(self, thing):
		if not (thing in map (lambda z: z[1],self.candidates)):
			try:
				self.candidates.append((thing.get_verb(self._verb),
										thing,
										None))
			except AttributeError:
				pass

	def ability_resolve(self, thing):
		if not (thing in map (lambda z: z[1],self.candidates)):
			try:
				self.candidates.append((thing.get_ability(self._verb),
										thing,
										None))
			except AttributeError:
				pass
	def auto_resolve(self, thing):
		try:
			self.candidates.append((thing.get_verb(self._verb),
									thing,
									thing.autoverbs[self._verb]))
		except AttributeError: pass
		except KeyError: pass
				
	def run(self):
		for verb, thing, xprep in self.candidates:
			self.verbThing=thing
			if xprep is not None:
				try:
					self.indirect_string(xprep)
				except:
					tn=thing.short_name(self.subject)
					self.strings[xprep]=tn
					self.objects[xprep]=thing
					# The following line needs some thought:
					self.subject.hears("(",xprep," the ",tn,")")
					
					# It's very difficult to figure out when the verb
					# has decided to "go through with it" and it's
					# committed to not raising an InappropriateVerb.
					# One would suppose this would be the first time
					# that the verb calls 'hears'... I suppose I
					# should be intercepting that, somehow.  Since a
					# player can only run one sentence at a time it
					# would be possible to, but it seems somehow
					# wrong.
					
				else:
					continue
			try:
				if len(self.objects) == 1:
					self.subject.antecedent=self.objects.values()[0]
				else:
					try: del self.subject.antecedent
					except: pass
					
				return verb(self)
			except InappropriateVerb: pass
			
			if xprep is not None:
				del self.strings[xprep]
				del self.objects[xprep]
		
		if len(self.ambiguities) == 0:
			raise NoVerb(self.verb_string())
		else:
			raise self.ambiguities.values()[0]
			
	def __init__(self,istr,player):
		sentence.Sentence.__init__(self,istr)
		self.subject=player
		self.objects={}
		self.ambiguities={}
		self.candidates=[]
		if (hasattr(player,"restricted_verbs") and
			self.verb_string() not in player.restricted_verbs):
			raise NoVerb(self.verb_string())
			
		# resolve all the words I have to be things
		for prep,word in self.strings.items():
			try:
				self.objects[prep]=player.locate(word)
				# player.hears("I found: "+str(self.objects[prep])+" for "+word)
			except Ambiguity, a:
				self.ambiguities[prep]=a
			except CantFind: pass
		# resolve my verb-word into some code
		for i in self.objects.values():
			if isinst(i,Thing):
				self.resolve(i)
		self.resolve(player.place)
		self.ability_resolve(player)
		if not self.candidates:
			flist=player.get_things(player)+player.place.get_things(player)
			if player.focus is not player and player.focus is not player.place:
				flist=flist+player.focus.get_things(player)
				
			flist=filter(lambda thing: hasattr(thing,"autoverbs"),
						 flist)
			
			for thing in flist:
				self.auto_resolve(thing)
		#for i in string.split(self.log_all_parts(),'\n'):
		#	player.hears(i)

	def indirect_string(self,preposition):
		try:
			return sentence.Sentence.indirect_string(self,preposition)
		except:
			raise NoString(self.verb_string(),preposition)
		
	def direct_object(self):
		return self.indirect_object('')
	def indirect_object(self, preposition):
		x=self.ambiguities.get(preposition)
		if x:
			raise x
		x=self.objects.get(preposition)
		if x:
			return x
		raise NoObject(self.indirect_string(preposition))
	def log_all_parts(self):
		x="*** Sentence ***\n"
		x=x+" verb [%s]\n" % self._verb
		x=x+" --- Objects ---\n"
		for prep,obj in self.objects.items():
			x=x+ "  [%s]: [%s]\n" % (prep, obj)
		x=x+ " --- Strings ---\n"
		for prep,name in self.strings.items():
			x=x+ "  [%s]: [%s]\n" % (prep, name)
		x=x+ " --- Ambiguities ---\n"
		for prep,name in self.ambiguities.items():
			x=x+ "  [%s]: [%s]\n" % (prep, name)
		return x
	
from ui import LocalIntelligence
# this for the 'get rid of known bad refs' hack...
