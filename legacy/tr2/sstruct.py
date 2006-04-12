"""sstruct.py -- SuperStruct

Higher level layer on top of the struct module, enabling to 
bind names to struct elements. The interface is similar to 
struct, except the objects passed and returned are not tuples 
(or argument lists), but dictionaries or instances. 

Just like struct, we use format strings to describe a data 
structure, except we use one line per element. Lines are 
separated by newlines or semi-colons. Each line contains 
either one of the special struct characters ('@', '=', '<', 
'>' or '!') or a 'name:formatchar' combo (eg. 'myFloat:f'). 
Repetitions as the struct module offers them are not useful in 
this context, except for fixed length strings  (eg. 'myInt:5h' 
is not allowed but 'myString:5s' is). The 'x' format character 
(pad byte) is treated as 'special', since it is by definition 
anonymous. Extra whitespace is allowed everywhere.

pack(format, object):
	'object' is either a dictionary or an instance (or actually
	anything that has a __dict__ attribute). If it is a dictionary, 
	its keys are used for names. If it is an instance, it's 
	attributes are used to grab struct elements from. Returns
	a string containing the data.

unpack(format, data, object=None)
	If 'object' is omitted (or None), a new dictionary will be 
	returned. If 'object' is a dictionary, it will be used to add 
	struct elements to. If it is an instance (or in fact anything
	that has a __dict__ attribute), an attribute will be added for 
	each struct element. In the latter two cases, 'object' itself 
	is returned.

unpack2(format, data, object=None)
	Convenience function. Same as unpack, except data may be longer 
	than needed. The returned value is a tuple: (object, leftoverdata).

calcsize(format)
	like struct.calcsize(), but uses our own format strings:
	it returns the size of the data in bytes.
"""

# XXX I would like to support pascal strings, too, but I'm not
# sure if that's wise. Would be nice if struct supported them
# "properly", but that would certainly break calcsize()...

__version__ = "1.1"
__copyright__ = "Copyright 1998, Just van Rossum <just@letterror.com>"

import struct
import re
import types


error = "sstruct.error"

def pack(format, object):
	formatstring, names = _getformat(format)
	elements = []
	if type(object) is not types.DictType:
		object = object.__dict__
	for name in names:
		elements.append(object[name])
	data = apply(struct.pack, (formatstring,) + tuple(elements))
	return data

def unpack(format, data, object=None):
	if object is None:
		object = {}
	formatstring, names = _getformat(format)
	if type(object) is types.DictType:
		dict = object
	else:
		dict = object.__dict__
	elements = struct.unpack(formatstring, data)
	for i in range(len(names)):
		dict[names[i]] = elements[i]
	return object

def unpack2(format, data, object=None):
	length = calcsize(format)
	return unpack(format, data[:length], object), data[length:]

def calcsize(format):
	formatstring, names = _getformat(format)
	return struct.calcsize(formatstring)


# matches "name:formatchar" (whitespace is allowed)
_elementRE = re.compile(
		"\s*"							# whitespace
		"([A-Za-z_][A-Za-z_0-9]*)"		# name (python identifier)
		"\s*:\s*"						# whitespace : whitespace
		"([cbBhHiIlLfd]|[0-9]+[ps])"	# formatchar
		"\s*"							# whitespace
		"(#.*)?$"						# [comment] + end of string
	)

# matches the special struct format chars and 'x' (pad byte)
_extraRE = re.compile("\s*([x@=<>!])\s*(#.*)?$")

# matches an "empty" string, possibly containing whitespace and/or a comment
_emptyRE = re.compile("\s*(#.*)?$")

_formatcache = {}

def _getformat(format):
	try:
		formatstring, names = _formatcache[format]
	except KeyError:
		lines = re.split("[\n;]", format)
		formatstring = ""
		names = []
		for line in lines:
			if _emptyRE.match(line):
				continue
			m = _extraRE.match(line)
			if m:
				formatchar = m.group(1)
				if formatchar <> 'x' and formatstring:
					raise error, "a special format char must be first"
			else:
				m = _elementRE.match(line)
				if not m:
					raise error, "syntax error in format: '%s'" % line
				names.append(m.group(1))
				formatchar = m.group(2)
			formatstring = formatstring + formatchar
		_formatcache[format] = formatstring, names
	return formatstring, names

def _test():
	format = """
		# comments are allowed
		>  # big endian (see documentation for struct)
		# empty lines are allowed:
		
		ashort: h
		along: l
		abyte: b	# a byte
		achar: c
		astr: 5s
		afloat: f; adouble: d	# multiple "statements" are allowed
	"""
	
	print 'size:', calcsize(format)
	
	class foo:
		pass
	
	i = foo()
	
	i.ashort = 0x7fff
	i.along = 0x7fffffff
	i.abyte = 0x7f
	i.achar = "a"
	i.astr = "12345"
	i.afloat = 0.5
	i.adouble = 0.5
	
	data = pack(format, i)
	print 'data:', `data`
	print unpack(format, data)
	i2 = foo()
	unpack(format, data, i2)
	print vars(i2)

if __name__ == "__main__":
	_test()
