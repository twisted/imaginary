#!/usr/bin/env python

from twisted.reality import Thing, Player

from divunal.stats import make_modifier,coinflip
from random import randint,random
import string

def any(list):
	return list[randint(0,len(list)-1)]

def aan(name):
	if string.lower(name[0]) in ('a','e','i','o','u'):
		return 'an '
	else:
		return 'a '

def AAn(name):
	return string.capitalize(aan(name))

class PlayerCreationDial(Thing):
	minval = -1.0
	maxval =  1.0
	def verb_turn(self,sentence):
		try:
			val = float(sentence.indirect_string('to'))
		except ValueError:
			sentence.subject.hears("That's not a number, you pathetic excuse for a human being.")
			return
		
		if (val <= self.maxval) and (val >= self.minval):
			sentence.subject.hears("You set ",self," to %02f"%val,'.')
			self.value=val
			self.machine.machine_update()
		else:
			sentence.subject.hears("No such number is on ",self,'.')

class PlayerCreationButton(Thing):
	def verb_push(self,sentence):
		self.machine.push_button(self.button_title,sentence.subject)
			
class PlayerCreationMachine(Thing):
	stats=('strength',  'dexterity',
		   'endurance', 'memory',
		   'agility',   'psyche')

	buttons=('generate',
			 'randomize',
			 'release')
	
	basedesc=('The control panel of the machine has three buttons, '
			  'labeled "GENERATE", "RELEASE", and "RANDOMIZE", and '
			  'six dials, each labeled and marked on a range from -1.0 '
			  'to 1.0.  There are two black rectangles above the '
			  'control panel, each with an engraved label in the silver '
			  'below, "Point Total" and "Name" respectively, and '
			  'immediately below those, there is a silver keyboard.')

	created=0

	def die(self):
		"clean up all of my buttons and dials, before going away"
		for stat in self.stats:
			dial=getattr(self,stat)
			del dial.machine
			dial.die()
			
		for button in self.buttons:
			btn=getattr(self,button)
			del btn.machine
			btn.die()
			
		if self.person:
			self.person.die()
			
		self.tube.die()
		Thing.die(self)
	
	def create(self):
		"create all of my component parts"
		assert not self.created, "You can't create the machine twice."
		
		self.created=1
		self.description=self.basedesc
		self.surface=1
		for stat in self.stats:
			dial=PlayerCreationDial(stat+" dial")
			dial.synonyms=[stat,'dial']
			dial.machine=self
			dial.place=self
			dial.component=1
			dial.value=0.
			setattr(self,stat,dial)

		for button in self.buttons:
			btn=PlayerCreationButton(button+" button")
			btn.synonyms=[button,'button']
			btn.button_title=button
			btn.machine=self
			btn.component=1
			btn.place=self
			setattr(self,button,btn)

		self.tube=Thing("player creation tube")
		self.tube.synonyms=['tube','creation tube']
		self.tube.place=self
		self.tube.description=("A large, vertical glass tube, capable "
							   "of holding a standing humanoid person "
							   "comfortably within it.")
		self.tube.component=1
		self.tube.surface=1
		self.tube.display_name='long glass tube'
		self.tube.contained_preposition='in'

	def push_button(self, pushed, pusher):
		try:
			method=getattr(self,"button_%s"%pushed)
		except AttributeError:
			pusher.hears("There is no such button.") # this really shouldn't be possible...
			return
		strup=string.upper(pushed)
		self.place.one_hears(
			pusher,
			to_subject = ("You push the "+strup+" button on ",self,"."),
			to_other   = (pusher," pushes the "+strup+" button on ",self,'.')
			)
		method()
		self.machine_update()
		
	def button_randomize(self):
		
		for stat in self.stats:
			dial=getattr(self,stat)
			mod=make_modifier()
			dial.value=mod-(mod%0.05)

		self.place.all_hear(self,' makes a large buzzing sound')

	def button_generate(self):
		nam=self.player_name
		try:
			self.reality[nam]
		except KeyError:
			p=Player(nam)
			p.synonyms=['uup']
			p.place=self.tube
			self.person=p
		else:
			self.place.all_hear(self.tube,' lurches sideways and then re-adjusts itself.')
	person=None
	player_name=""
	
	def button_release(self):
		if self.person:
			self.person.place=self.place
			self.place.all_hear(self.person," floats through the wall of the glass tube and slumps to the floor.")
			del self.person
		else:
			self.place.all_hear("You hear a faint sloshing sound.")
			
	def verb_type(self,sentence):
		s=sentence.direct_string()
		sentence.subject.place.one_hears(
			sentence.subject,
			to_subject=("You type on ",self,"'s keyboard."),
			to_other=(sentence.subject," types something on ",self,"'s keyboard.")
			)
		self.player_name=s
		self.machine_update()
		
	def machine_update(self):
		strength  = self.strength.value
		dexterity = self.dexterity.value
		endurance = self.endurance.value
		memory    = self.memory.value
		agility   = self.agility.value
		psyche    = self.psyche.value

		remaining = -(strength+dexterity+
					  endurance+memory+
					  agility+psyche) % 0.05

		if remaining < 0.:
			color="red"
		elif remaining > 0.:
			color="yellow"
		else:
			color="green"

		name=self.player_name
		
		try:             self.reality[name]
		except KeyError: namcol="bright white"
		else:            namcol="grey"

		self.description['dials']=string.join(
			map(lambda x,local=locals(): string.capitalize("%s is set to %s. "%(x,str(local[x]))),
				self.stats)
			)

		self.description['points_remain']=(
			'The black "Points Remaining" rectangle is displaying '
			'the number %s in a %s script.'
			% (str(remaining),color))

		self.description['name_rect']=(
			'The "Name" rectangle is displaying: "%s" in a %s script.'%(name,namcol)
			)

		p=self.person
		if p:
			map(lambda x,p=p,local=locals(): setattr(p,x,local[x]),
				self.stats)

			if coinflip():
				p.gender='m'
				face=any(male_face)
				title=["young man","man"][coinflip()]
			else:
				p.gender='f'
				face=any(female_face)
				title=["young woman","woman"][coinflip()]

			if psyche > random()+0.1:
				complexion=any(divuthan_complexion)
			else:
				if endurance < -0.3:
					complexion=any(sickly_complexion)
				else:
					complexion=any(normal_complexion)

			if psyche > random()+0.1:
				eye_color=any(divuthan_eye_color)
			else:
				eye_color=any(normal_eye_color)

			if psyche > random()+0.2:
				eye_style=any(divuthan_eye_style)
			else:
				eye_style=any(normal_eye_style)

			if psyche > random():
				hair_tone=any(divuthan_hair_tone)
				hair_color=any(divuthan_hair_color)
			else:
				hair_tone=any(normal_hair_tone)
				hair_color=any(normal_hair_color)

			hair_style=any(normal_hair_style)

			if memory > random() + 0.2:
				demeanor = any(memory_demeanor)
			else:
				demeanor = any(normal_demeanor)

			if strength > 0.3 and endurance > 0.3 and agility > 0.3:
				build = any(perfect_build)
			elif strength > 0.3 and endurance > 0.3:
				build = any(strong_build)
			elif (agility > 0.3 and strength > 0.3) or endurance > 0.3:
				build=any(agile_build)
			elif agility > 0.3:
				build = any(thin_build)
			elif (strength > -0.3 and endurance > -0.3 and agility > -0.3):
				build = any(normal_build)
			elif strength > 0.3:
				build = any(fat_build)
			else:
				build = any(sick_build)

			pran=random()
			if pran < 0.3:
				desc=("(Test Version: Type A)\n"+
					  AAn(build)+build+", "+demeanor+" looking "+title+
					  " with "+eye_style+" "+eye_color+" eyes, "+
					  hair_style+" "+hair_tone+" "+hair_color+" hair, and a "+
					  complexion+" complexion.")
			elif pran < 0.6:
				desc=("(Test Version: Type B)\n"+
					  AAn(build)+build+" "+title+" with "+
					  hair_style+" "+hair_color+" hair, "+eye_style+" "+eye_color+
					  " eyes, and "+aan(demeanor)+demeanor+", "+face+
					  " face.")
			else:
				desc=("(Test Version: Type C)\n"+
					  AAn(title)+title+" with ")
				if coinflip():
					desc=desc+hair_tone+", "
				desc=(desc+hair_style+' '+hair_color+" hair and "+eye_color+" eyes. "+
					  p.He_She(p)+" is "+build+", ")
				if coinflip():
					desc=desc+"with "+complexion+" skin and "
				else:
					desc=desc+"and has "
				desc=desc+aan(face)+face+", "+demeanor+" face."

			p.description=desc

	def verb_kick(self, sentence):
		self.place.one_hears(
			sentence.subject,
			to_subject=("You give the machine swift kick,"),
			to_other=(sentence.subject," gives the machine a swift kick."),
			)
		self.machine_update()
				
normal_eye_color=[
	"blue", "grey", "green", "brown", "hazel", "yellow", "pink", "purple", "amber"
	]

divuthan_eye_color=[
	"red", "violet", "bright white", "silver", "translucent pink"
	]

divuthan_eye_style=[
	"gleaming", "shining", "sunken", "piercing", "bright", "cold"
	]

normal_eye_style=[
	"bright", "light", "soft", "clear", "wide", "dark",
	"cold", "cloudy", "stormy", "slanted", "almond-shaped"
	]

normal_hair_color=[
	"blonde", "gold", "copper", "brown", "red", "blue",
	"green", "purple", "pink", "grey", "auburn", "violet"
	]

divuthan_hair_color=[
	"jet black", "gray", "silver", "white", "sable"
	]

normal_hair_tone=[
	"bright", "light"
	]

divuthan_hair_tone=[
	"glossy", "shiny"
	]

normal_hair_style=[
	"unkempt", "messy", "uneven", "stringy", "curly", "wavy", "straight",
	"neat", "neatly trimmed", "smooth", "sleek", "thin", "sparse", "cropped",
	"short", "shoulder length", "long", "flowing"
	]

normal_complexion=[
	"light", "pale", "freckled", "tanned", "dark"
	]

sickly_complexion=[
	"extremely pale", "pale", "unhealthy", "sickly"
	]

divuthan_complexion=[
	"white", "extremely pale", "translucent", "greyish"
	]

normal_demeanor=[
	"solemn", "thoughtful", "mischievous", "wry", "distant",
	"cold","troubled", "bright", "proud", "nervous", "haughty",
	"crazy", "mysterious", "inscrutable", "youthful", "tired",
	"shifty", "lively", "personable", "crafty", "stern", "wise"
	]

male_face=[
	"crooked", "round", "thin", "narrow", "jagged", "sharply pointed",
	"bony", "angular", "weathered", "rough", "grizzled", "handsome"
	]

female_face=[
	"round", "thin", "narrow", "sharply pointed", "angular",
	#hmm... are we exposing a heterosexual male bias here? ;-P
	"smooth", "rosy", "pretty", "beautiful"
	]

memory_demeanor=[
	"friendly", "gentle", "cheerful", "peaceful", "serene", "calm", "good natured"
	]

perfect_build=[
	"imposing", "statuesque", "finely sculpted", "well proportioned"
	]

agile_build=[
	"agile", "sinuous", "athletic", "lean", "well poised"
	]

normal_build=[
	"tall", "short", "thin", "lean", "small", "heavy set", "large"
	]

strong_build=[
	"muscular", "hefty", "huge", "broad shouldered", "powerfully built"
	]

thin_build=[
	"thin", "lean", "skinny", "gracefully built"
	]


sick_build=[
	"weak", "scrawny", "gaunt", "frail"
	]

fat_build=[
	"portly", "overweight", "blocky", "large"
	]
