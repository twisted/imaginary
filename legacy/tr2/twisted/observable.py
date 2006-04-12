import types

class _DontTell:
	def __cmp__(self,other):
		if isinstance(other,_DontTell):
			return 0
		else:
			return -1

	def __hash__(self): return id(self)
	def __repr__(self):
		return "observable.DontTell"
	
class _Gone:
	def __cmp__(self,other):
		if isinstance(other,_Gone):
			return 0
		else:
			return -1

	def __hash__(self): return id(self)
	def __repr__(self):
		return "observable.Gone"

DontTell=_DontTell()
Gone=_Gone()

class Dynamic:
	def __init__(self, caller=None):
		if caller:
			self.evaluate=caller
			
	def evaluate(self,observer,hash=None,key=None):
		print 'observe.py: Dynamic.evaluate called directly --> override this'
		print 'observer %s\nhash %s\nkey %s'%(observer,hash,key)
		return DontTell

	def __call__(self,observer,hash=None,key=None):
		if type(observer)==types.MethodType:
			observer=observer.im_self
		return self.evaluate(observer,hash,key)

def propertize(self, observer,key,prop):
	if isinstance(prop,Dynamic): p=prop(observer,self,key)
	else: p=prop
	if p == DontTell: raise p
	return p

class EventSource:
	def __init__(self):
		self.listeners={}

	def bind(self, event, command, args=()):
		if not self.listeners.has_key(event):
			self.listeners[event]=[]
		self.listeners[event].append(command)

	def fire(self, event, *args,**kw):
		for listener in self.listeners[event]:
			apply(listener,args,kw)

class Observable:
	def __init__(self):
		self.observers=[]

	def add_observer(self, observer):
		self.observers.append(observer)

	def remove_observer(self, observer):
		self.observers.remove(observer)

	def notify(self, *rgs):
		args=(self,)+rgs
		for observer in self.observers:
			self.tell(observer, args)

	def tell(self,observer,args):
		apply(observer,args)

class Hash(Observable):

	def __init__(self,properties=None):
		Observable.__init__(self)
		if properties is None:
			properties={}
		self.properties=properties

	def tell(self,observer,targs):
		self2,key,value=targs
		# I assume I haven't seen this yet.
		already_seen=0
		try:
			# Does this observer think there's something in this hash
			# under this key already?
			propertize(self,observer,key,self[key])
			# Correction, I have.
			already_seen=1
		except _DontTell:
			# If not, well,
			if targs[2]==Gone:
				# if we were just going to tell them that it was gone,
				# forget about it.
				return
		except KeyError:
			# That wasn't even in the dictionary before!
			pass
		try:
			apply(observer,
				  (self2, key,
				   propertize(self,observer,key,value)))
		except _DontTell:
			# Okay, so this observer isn't supposed to know about this
			# property.
			if already_seen:
				# If they already have it "in view", tell them it's
				# gone now.
				apply(observer,(self2,key,Gone))
			# Otherwise, well, they don't know that anything has happened.

	def add_observer(self, observer):
		Observable.add_observer(self,observer)
		for k,v in self.properties.items():
			self.tell(observer,(self,k,v))

	def __setitem__(self, key,val):
		self.notify(key,val)
		self.properties[key]=val

	def __getitem__(self, key):
		return self.properties[key]

	def __len__(self):
		return len(self.properties)

	def __delitem__(self, key):
		self.notify(key,Gone)
		del self.properties[key]

	def keys(self):
		return self.properties.keys()

	def values(self):
		return self.properties.values()

	def items(self):
		return self.properties.items()

	def update(self,dict):
		for k,v in dict.items():
			self[k]=v

	def has_key(self,key):
		return self.properties.has_key(key)
	
	def __repr__(self):
		if self.observers:
			x=repr(self.observers)
		else:
			x=""
		return "observable.Hash(%s%s)"%(repr(self.properties),x)
										

class Delegator:
	def __init__(self, callhash):
		self.hash=callhash
	def __call__(self, *args):
		try: observer=self.hash[args[1]]
		except: 'no delegation'
		else: apply(self.hash[args[1]],args)
