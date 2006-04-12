
from token import *
from tokenize import *

class Token:
	def __init__(self,ttype,val,no):
		self.ttype=ttype
		self.value=val
		self.line=no
	def __repr__(self):
		return '< Token %s at %s >'%(repr((self.ttype,
										   self.value,
										   self.line)),
									 hex(id(self)))

# A much more useful, generalized tokenizer than the one included in
# python by default... although only slightly changed.

class Tokenizer:
	def eat(self, ttype, tstring, tokBegin, tokEnd, line):
		if ttype in (NUMBER, STRING):
			try:
				value=eval(tstring)
			except OverflowError:
				# temporary hack for parsing Longs
				value=eval(tstring+'L')
		else:
			value=tstring
		
		if (self._neg):
			if type(value).__name__ in ('int', 'float', 'long'):
				value = -value
			else:
				self.tokens.append(self._neg)
			self._neg=None

		# sorry guido
		tkn=Token(ttype,value,tokBegin[0])
		if value == '-':
			self._neg=tkn
			return
		if not ttype in self.ignored:
			self.tokens.append(tkn)
	
	def __init__(self, file,ignored=(INDENT, DEDENT, NL, NEWLINE)):
		self.tokens=[]
		self.ignored=ignored
		self._neg=None
		tokenize(file.readline,self.eat)
		self.reset()
	
	def next(self):
		current=self.tokens[self.counter]
		self.counter=self.counter+1
		return current

	def backtrack(self):
		self.counter=self.counter-1

	def reset(self):
		self.counter=0
	
	def go(self):
		for i in self.tokens:
			print i.ttype
			print i.value

	def __getitem__(self, itemnum):
		return self.tokens[itemnum]

	def stripcppcomments(self):
		"hack -- this will break if an unterminated string is inside a comment, for obvious reasons"
		t=[]
		p=''
		for i in self.tokens:
			if p == '':
				if i.value == '/':
					p='/'
					c=i
				elif i.value == '\012':
					pass
				else:
					t.append(i)
			elif p == '/':
				if i.value == '/':
					p='//'
					del c
				elif i.value == '*':
					p='/*'
					del c
				else:
					p=''
					t.append(c)
					t.append(i)
					del c
					
			elif p == '//':
				if i.value == '\012':
					p=''
			elif p == '/*':
				if i.value == '*':
					p='/**'
			elif p == '/**':
				if i.value == '/':
					p = ''
				else:
					p='/*'
					
		self.tokens=t
		self.reset()
