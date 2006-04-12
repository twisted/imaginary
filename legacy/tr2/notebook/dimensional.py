
optimize=0

class SubArray:
	def __init__(self, arr, offset):
		self.lst=arr.lst
		self.offset=offset
		if optimize:
			self.__getitem__=self.__getitem__
			self.__setitem__=self.__setitem__
	def __getitem__(self, item):
		return self.lst[item+self.offset]
	def __setitem__(self, key, val):
		self.lst[key+self.offset]=val
	
class Array:
	def __init__(self, xdim, ydim):
		self.xdim=xdim
		self.lst=range(xdim*ydim)
	def __getitem__(self, item):
		return SubArray(self, self.xdim*item)

def ListOfLists(xdim,ydim):
	a=range(1000)
	for i in a:
		a[i]=range(1000)
	return a
