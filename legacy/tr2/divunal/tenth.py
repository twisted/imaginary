#!/usr/bin/env python

from twisted.reality import *
		
class LibraryDoor:
	def verb_open(self, sentence):
		ph=sentence.subject.place.one_hears
		ph(sentence.subject,
		   to_subject=("After some experimentation, you discover that the door is large, heavy, and has no usable handholds, and that standing around tugging inneffectually on the pistons makes you look silly.",)
		   to_other=(sentence.subject, " gropes for a handhold on the door, and spends a few seconds tugging inneffectually on one of the pistons before finally giving up.")
		   )
