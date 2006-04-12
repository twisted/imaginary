
import types

"""
Standardized versions of various cool things that you can do with
Python's reflection capabilities.  This should probably involve
metaclasses somehow, but I don't understand them, so nyah :-)
"""

class Settable:
	"""
	A mixin class for syntactic sugar.  Lets you assign attributes by
	calling with keyword arguments; for example, x(a=b,c=d,y=z) is the
	same as x.a=b;x.c=d;x.y=z.  The most useful place for this is
	where you don't want to name a variable, but you do want to set
	some attributes; for example, X()(y=z,a=b).
	"""
	def __call__(self,**kw):
		for key,val in kw.items():
			setattr(self,key,val)
		return self

class Accessor:
	
	"""
	Extending this class will give you explicit accessor methods; a
	method called set_foo, for example, is the same as an if statement
	in __setattr__ looking for 'foo'.  Same for get_foo and del_foo.
	There are also really_del and really_set methods, so you can
	override specifics in subclasses without clobbering __setattr__
	and __getattr__.
	"""
	
	def __setattr__(self, k,v):
		kstring='set_%s'%k
		if hasattr(self.__class__,kstring):
			return getattr(self,kstring)(v)
		else:
			self.really_set(k,v)
			
	def __getattr__(self, k):
		kstring='get_%s'%k
		if hasattr(self.__class__,kstring):
			return getattr(self,kstring)()
		raise AttributeError("No Attribute or Accessor Found: %s"%k)

	def __delattr__(self, k):
		kstring='del_%s'%k
		if hasattr(self.__class__,kstring):
			getattr(self,kstring)()
			return
		self.really_del(k)

	def really_set(self, k,v):
		"""
		*actually* set self.k to v without incurring side-effects.
		This is a hook to be overridden by subclasses.
		"""
		self.__dict__[k]=v
		
	def really_del(self, k):
		"""
		*actually* del self.k without incurring side-effects.  This is a
		hook to be overridden by subclasses.
		"""
		del self.__dict__[k]


class Summer(Accessor):
	"""
	Extend from this class to get the capability to maintain 'related
	sums'.  Have a tuple in your class like the following:

	sums=(('amount','credit','credit_total'),
		  ('amount','debit','debit_total'))

	and the 'credit_total' member of the 'credit' member of self will
	always be incremented when the 'amount' member of self is
	incremented, similiarly for the debit versions.
	"""

	def really_set(self, k,v):
		"This method does the work."
		for sum in self.sums:
			attr=sum[0]
			obj=sum[1]
			objattr=sum[2]
			if k == attr:
				try:
					oldval=getattr(self, attr)
				except:
					oldval=0
				diff=v-oldval
				if hasattr(self, obj):
					ob=getattr(self,obj)
					if ob is not None:
						try:oldobjval=getattr(ob, objattr)
						except:oldobjval=0.0
						setattr(ob,objattr,oldobjval+diff)

			elif k == obj:
				if hasattr(self, attr):
					x=getattr(self,attr)
					setattr(self,attr,0)
					y=getattr(self,k)
					Accessor.really_set(self,k,v)
					setattr(self,attr,x)
					Accessor.really_set(self,y,v)
		Accessor.really_set(self,k,v)

def funcinfo(function):
	"""
	this is more documentation for myself than useful code.
	"""
	code=function.func_code
	name=function.func_name
	argc=code.co_argcount
	argv=code.co_varnames[:argc]
	defaults=function.func_defaults

	print 'The function',name,'accepts',argc,'arguments.'
	if defaults:
		required=argc-len(defaults)
		print 'It requires',required,'arguments.'
		print 'The arguments required are: ',argv[:required]
		print 'additional arguments are:'
		for i in range(argc-required):
			j=i+required
			print argv[j],'which has a default of',defaults[i]

from threading import _get_ident,_active,_DummyThread
# currentThread uses 'print'; that's no good.
def currentThread():
	try: return _active[_get_ident()]
	except KeyError: return _DummyThread()
# del _get_ident,_active,_DummyThread
			
class ThreadAttr:
	def __init__(self,threads=None,default=None):
		self.__dict__['_threads']=threads or {}
		self.__dict__['_default']=default
	def __get(self):
		try: return self._threads[currentThread()]
		except KeyError: return self._default
	def __getattr__(self,key):
		return getattr(self.__get(),key)
	def __setattr__(self,key,val):
		return setattr(self.__get(),key)
	def __delattr__(self,key):
		return delattr(self.__get(),key)

ISNT=0
WAS=1
IS=2

def qual(clazz):
	return  clazz.__module__+'.'+clazz.__name__

def getcurrent(clazz):
	assert type(clazz) == types.ClassType, 'must be a class...'
	module=__import__(clazz.__module__,None,None,1)
	currclass=getattr(module,clazz.__name__)
	return currclass

# class graph nonsense

# I should really have a better name for this...
def isinst(inst,clazz):
	if type(inst) != types.InstanceType or type(clazz)!=types.ClassType:
		return isinstance(inst,clazz)
	cl=inst.__class__
	cl2=getcurrent(cl)
	clazz=getcurrent(clazz)
	if issubclass(cl2,clazz):
		if cl == cl2:
			return WAS
		else:
			inst.__class__=cl2
			return IS
	else:
		return ISNT

def named_module(name):
	return __import__(name,None,None,1)
	
def _byname(clazz):
	return getattr(named_module(clazz.__module__),clazz.__name__)

# i need to be reloaded if any of my bases do not match their
# currently loaded version. (i do not match my currently loaded
# version if I need to be reloaded -- but that does not mean that
# I need to be reloaded too (in fact it means I have necessarily been
# reloaded already))

def buildbaselist(clazz,modules):
	needreloadself=0
	needreloadsub=0
	
	for i in clazz.__bases__:
		if buildbaselist(i,modules):
			needreloadself=1
	if needreloadself and clazz.__module__ not in modules:
		# print 'reloading',clazz.__module__
		reload(named_module(clazz.__module__))
		modules.append(clazz.__module__)
	else:
		clz=_byname(clazz)
		if clazz != clz:
			needreloadsub=1
		
	return needreloadself or needreloadsub
	
def reclass(clazz):
	"figure out if you need to reload any other stuff to get back in sync"
	modules=[]
	buildbaselist(clazz,modules)
	return _byname(clazz)

def refrump(obj):
	x=obj.__class__
	y=reclass(x)
	if x!=y:
		obj.__class__=y
