#!/usr/bin/env python
# note: this does NOT work with JPython
try:
	x
except NameError:
	print "I am being loaded for the first time"
else:
	print "I am being reloaded"

class x:pass
