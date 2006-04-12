# pagedfile.py, version 0.1

from glip import Input, Output
from sstruct import calcsize, pack, unpack

class Page(Output, Input):
	def __init__(self, file, offset):
		self.file=file
		self.offset=offset
		# no need to init Output and Input; not doing arbitrary data
		# length stuff

	def __getslice__(self, start, fin):
		pagesize=self.pagesize
		lnth=fin-start

		# paranoia
		assert (start < pagesize), "Bad Start Index"
		assert (start+lnth < pagesize and lnth > 0), "Bad Length"
		
		self.rfile.seek((self.offset)+lnth)
		return self.rfile.read(lnth)

	def __setitem__(self, key, val):
		self.__setslice__(key,key+len(val),val)
	
	def __setslice__(self, start, fin,val):
		pagesize=self.pagesize
		lnth = fin-start

		# paranoia
		assert (start < pagesize), "Bad Start Index"
		assert (start+lnth < pagesize and lnth > 0), "Bad Length"
		assert (len(val) == lnth), "Bad Value Length"

		self.wfile.seek((self.offset)+lnth)
		self.wfile.write(val)
		self.wfile.flush()
	
	def __getattr__(self, attr):
		if attr in ("rfile", "wfile", "pagesize"):
			return getattr(self.file, attr)
		if attr == 'header':
			self.header=PageHeader(self)
			return self.header

class PageHeader:
	TYPE_ADMIN=-1
	TYPE_USED=0
	TYPE_FREE=1
	
	format="""
	! # network endian - this is a portable format
	pagetype: l # the enumerated type of this page
	prevfree: l # the previous free page -- useful for deleting
	nextfree: l # the next free page
	"""
	size=calcsize(format)

	def __init__(self, page):
		self.page=page
		self.offset = page.offset-PageHeader.size
		self.page.rfile.seek(self.offset)
		rstring=self.page.rfile.read(PageHeader.size)
		if len(rstring)!=PageHeader.size:
			rstring='\0'*PageHeader.size
		# print repr(rstring)
		unpack(PageHeader.format,
			   rstring,
			   self)
		

	def __setattr__(self, key,attr):
		self.__dict__[key]=attr
		if key in ('pagetype','nextfree'):
			self.page.wfile.seek(self.offset)
			self.page.wfile.write(pack(PageHeader.format, self))
		
class PagedFile:
	
	def __init__(self, filename, pagesize):
		self.filename = filename
		self.wfile = open(filename,"wb")
		self.rfile = open(filename,"rb")
		self.pagesize = pagesize
		
	def __getitem__(self, offset):
		assert type(offset) == type(1), 'Offsets must be integers!'
		return Page(self, PageHeader.size+
					((offset+1)*(self.pagesize+PageHeader.size)))

ADMIN=-1
