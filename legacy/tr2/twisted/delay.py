from time import sleep
from bisect import insort
from threading import Thread

def ticks_of(ev):
	""" get the ticks (time at which the event should occur) from an event tuple """
	return ev[0]

def func_of(ev):
	""" get the function from an event tuple """
	return ev[1]

def args_of(ev):
	""" get the arguments from an event tuple """
	return ev[2]

class StopLooping(Exception):
	def __init__(self):
		Exception.__init__(self)
		raise self

class Looping:
	def __init__(self, ticks,func,delayed):
		""" Looping(ticks,func,delayed)

		This initializer is only called internally.
		"""
		self.ticks=ticks
		self.func=func
		self.delayed=delayed
		
	def __call__(self, *args,**kw):
		"""
		call my function with the given arguments, then reschedule me
		"""
		try:
			apply(self.func,args,kw)
			self.delayed.later(self,self.ticks,args)
		except StopLooping: pass

class Steps(Looping):
	offset=0
	def __init__(self, ticks,func,list,delayed):
		Looping.__init__(self,ticks,self.go,delayed)
		self.list=list
		self.func2=func

	def go(self):
		self.func2(self.list[self.offset])
		self.offset=self.offset+1
		if self.offset >= len(self.list):
			StopLooping()
			
		
class Delayed:
	"""\
	
A delayed event scheduler which, in my humble but correct opinion, is
much better and more featureful than the built-in 'sched' module,
especially when you're working with event insertions from multiple
threads.

"""

	def __init__(self):
		""" Initialize the delayed event queue. """
		self.queue=[]
		self.ticks=0
		self.is_running=1
		self.ticktime=5
		
	def later(self, func,ticks=0,args=()):
		"""Delayed.later(func [, ticks [, args]]) -> None
		
		This function schedules the function 'func' for execution with
		the arguments 'args', 'ticks' ticks in the future.  A 'tick'
		is one call to the 'run' function.
		"""
		
		insort(self.queue, (self.ticks-ticks,func,args))

	def step(self, func,list,ticks=0):
		"""Delayed.step(func,list[,ticks]) -> None

		This schedules the function *func* for execution with each
		element in *list* as its only argument, pausing *ticks* ticks
		between each invocation.
		"""
		Steps(ticks,func,list,self)()
		
	def loop(self, func,ticks=0,args=()):
		"""Delayed.loop(ticks,func[,args=()]) -> None

		This schedules the function *func* for repeating execution
		every *ticks* ticks.
		"""
		self.later(apply,args=(Looping(ticks,func,self),args),ticks=ticks)
		
	def run(self):
		"""Delayed.run() -> None

		This runs one cycle of events, and moves the tickcount by one.
		(I would say "increments", but it actually decrements it for
		simplicity of implementation reasons)
		"""
		sticks=self.ticks-1
		self.ticks=sticks
		while self.queue and ticks_of(self.queue[-1]) > sticks:
			pop=self.queue.pop()
			apply(func_of(pop),
				  args_of(pop))
		
	def runloop(self):
		"""
		Runs until the is_running flag is false.
		"""
		while self.is_running:
			self.run()
			sleep(self.ticktime)

	def threadloop(self):
		t=Thread(target=self.runloop)
		t.start()
		
	def stop(self):
		"""
		In multithreaded mode, stops the current thread.
		"""
		self.is_running=0
