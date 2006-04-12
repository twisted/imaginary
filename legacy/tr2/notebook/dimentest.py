from time import time
from dimensional import Array, ListOfLists
import c_notebook.dimensional
import dimensional

xdim,ydim=1000,1000

def clock(f,*args,**kw):
	t=time()
	r=apply(f,args,kw)
	print f.func_name,'->\t',int(1000*(time()-t)),'ms'
	return r

def carray_init():
	return c_notebook.dimensional.Array(xdim,ydim)

def carray_zero(a):
	array_zero(a)

def array_init():
	dimensional.optimize=0
	return Array(xdim,ydim)

def opt_init():
	dimensional.optimize=1
	return Array(xdim,ydim)

def array_zero(a):
	for i in xrange(xdim):
		f=a[i]
		for j in xrange(ydim):
			f[j]=0

def opt_zero(a):
	array_zero(a)
	
def list_init():
	return ListOfLists(xdim,ydim)

def list_zero(a):
	array_zero(a)

for x,y in ((array_zero,array_init),
			(opt_zero,opt_init),
			(carray_zero,carray_init),
			(list_zero,list_init)):
	clock(x,clock(y))
