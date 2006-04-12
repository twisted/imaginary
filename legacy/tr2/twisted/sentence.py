#!/usr/bin/env python

from tokenizer import Tokenizer, NL
from cStringIO import StringIO
from tokenize import tokenize
from token import INDENT, DEDENT, NEWLINE, ERRORTOKEN, ENDMARKER

class Sentence(Tokenizer):
	def stringioize(self,string):
		# the following is really just a stupid hack to emulate the
		# quirky behavior of the string tokenizer in java; it should
		# be gotten rid of once the faucet does say "|" by default
		# instead of say "|
		self.tokens=[]
		self._neg=None
		fd=StringIO(string)
		tokenize(fd.readline,self.eat)
		self.reset()
		sn=self.next()
		try:
			while sn.ttype != ERRORTOKEN:
				sn=self.next()
			# this is the best part.  It works completely by accident.
			# After 3 tries, you end up with a """ on the end of your
			# string, which is a multi-line string -- the tokenizer
			# will throw an exception for that (god knows why it
			# doesn't throw an exception for an EOF in a single-line
			# string...)
			self.stringioize(string+'"')
		except: pass
			# import traceback
			# traceback.print_exc()
			# print 'resetting'
		self.reset()
		
		
	def __init__(self, string):
		# quirkily format stuff
		self.ignored=(INDENT,DEDENT,NL,NEWLINE)
		self.stringioize(string)
		prepositions=['into',
					  'in',
					  'on',
					  'off',
					  'to',
					  'at',
					  'from',
					  'through',
					  'except',
					  'with',
					  'by']
		self.strings={}
		prp=''
		self._verb=self.next().value
		try:
			while 1:
				tkn=self.next()
				longword=''
				while (not tkn.value in prepositions):
					tkv=str(tkn.value)
					if longword and not tkn.ttype == ENDMARKER:
						tkv=' '+tkv
					longword=longword+tkv
					self.strings[prp]=longword
					tkn=self.next()
				prp=tkn.value
			print 'unreachable code'
		# I expect that self.next() will eventually throw an
		# exception, so
		except: pass
		# small bug.  This should probably be taken care of above, but
		# the parser can't ignre prepositions...
		if self.strings.get('')=='':
			del self.strings['']
	def has_indirect(self, preposition):
		return self.strings.has_key(preposition)
	def has_direct(self):
		return self.hasIndirect('')
	def indirect_string(self, preposition):
		return self.strings[preposition]
	def direct_string(self):
		return self.indirect_string('')
	def verb_string(self):
		return self._verb
	
if __name__=='__main__':
	s=Sentence("get dog with 44")
	print s.direct_string()
	print s.verb_string()
	print s.indirect_string('with')
