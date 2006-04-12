from threading import Thread
import sys


# import threading
# def currentThread(delegate=threading.currentThread):
# 	import traceback
# 	d=delegate()
# 	traceback.print_stack(file=sys.stdout)
# 	print
# 	return d

# threading.currentThread=currentThread

p=sys.stdout.write
v=sys.stdout.flush
black=0
white=1

def makeCheck(testCaseClass, prefix='check'):
	testFnNames = filter(lambda n,p=prefix: n[:len(p)] == p,
						 dir(testCaseClass))
	return map(testCaseClass, testFnNames)

import unittest

def nop(): pass
from twisted import delay
class DelayTestCase(unittest.TestCase):
	def setUp(self):
		self.delayed=delay.Delayed()

	def checkSingleNoDelay(self):
		self.delayed.later(ticks=0,func=nop,args=())
		self.delayed.run()
		assert self.delayed.queue == [], "queue not empty: "+str(self.delayed.queue)
		
	def checkMultiNoDelay(self):
		later=self.delayed.later
		run=self.delayed.run
		for i in xrange(100):
			later(ticks=0,func=nop,args=())
		run()
		assert self.delayed.queue == [], "queue not empty: "+str(self.delayed.queue)

	def checkMultiDelay(self):
		later=self.delayed.later
		run=self.delayed.run
		for i in xrange(100):
			later(ticks=i,func=nop,args=())
		for i in xrange(100):
			run()
		assert self.delayed.queue == [], "queue not empty: "+str(self.delayed.queue)

	def checkStepping(self):
		def func(foo):
			foo[0].TEST_LIST.append(foo[1])
		d=self.delayed
		d.TEST_LIST=[]
		
		d.step(func,[(d,0),(d,1),
					 (d,2),(d,3),
					 (d,4)])
		
		run=self.delayed.run
		for i in xrange(100):
			run()
			
		assert self.delayed.TEST_LIST == [0,1,2,3,4]

	def checkLooping(self):
		class TestLoop:
			def __init__(self):
				self.loops=100
			def loopMe(self):
				self.loops=self.loops-1
				if not self.loops:
					delay.StopLooping()
				
		t=TestLoop()

		loop=self.delayed.loop
		later=self.delayed.later
		
		loop(t.loopMe,0)

		run=self.delayed.run
		r=range(t.loops)
		r.reverse()
		for i in r:
			run()
			assert i == t.loops, "Looping too fast / slow ..."

		assert self.delayed.queue == [], "queue not empty: "+str(self.delayed.queue)
		
delayCheck=makeCheck(DelayTestCase,'check')

from twisted import observable

class Asserter:
	
	def __init__(self, *args):
		self.args=args
		self.flag=0
		
	def run(self, *args):
		assert args == self.args, "arguments are off"
		self.flag=1
		
	def post(self):
		assert self.flag, "method wasn't called"

class ObservableTestCase(unittest.TestCase):
	def setUp(self):
		self.observable=observable.Observable()

	def checkNotify(self):
		ob=self.observable
		a=Asserter(ob,'a','b')
		ob.add_observer(a.run)
		ob.notify('a','b')
		a.post()
		
	def checkHashInit(self):
		x=observable.Hash()
		x['a']='b'
		a=Asserter(x,'a','b')
		x.add_observer(a.run)
		x.remove_observer(a.run)
		x['y']='z'
		a.post()
		
	def checkHashChange(self):
		x=observable.Hash()
		a=Asserter(x,'a','b')
		x.add_observer(a.run)
		x['a']='b'
		a.post()

	def checkMultiHashChange(self):
		x=observable.Hash()
		a=Asserter(x,'a','b')
		b=Asserter(x,'a','b')
		x.add_observer(a.run)
		x.add_observer(b.run)
		x['a']='b'
		x.remove_observer(a.run)
		x.remove_observer(b.run)
		x['x']='y'
		a.post()
		b.post()
		
observableCheck=makeCheck(ObservableTestCase)

from twisted import noungraph

class NounGraphTestCase(unittest.TestCase):
	def setUp(self):
		self.root=noungraph.default_root

	def checkRoot(self):
		n=noungraph.Node('Beta')
		assert self.root['beta'] is n, 'root validation is wrong'

	def checkPlace(self):
		fred=noungraph.Node('Fred')
		fred.add_synonym('f-man')
		lucy=noungraph.Node('Lucy')
		bob=noungraph.Node('Bob')
		gert=noungraph.Node('Gert')
		
		fred.place=lucy
		bob.place=fred

		assert lucy.find('Fred') is fred, 'basic placement is broken'
		assert lucy.find('f-man') is fred, 'basic synonyms are broken'

		del fred.place

		try: lucy.find('Fred')
		except noungraph.CantFind: pass
		else: assert black is white, "naming doesn't go away"

		try: lucy.find('Fred')
		except noungraph.CantFind: pass
		else: assert black is white, "synonyms don't go away"

	def checkNaming(self):
		a=noungraph.Node("A")
		b=noungraph.Node("B")
		a.place=b
		a.realname="x"
		assert b.find('a') is a, 'lost real name syn'
		a.name="x"
		try: b.find('a')
		except noungraph.CantFind: pass
		else: assert black is white, 'kept nonreal syn'
		
	def checkAmbiguity(self):
		x=noungraph.Ambiguous()
		x.put("a","b")
		x.put("a","c")
		x.put("a","d")
		x.put("a","q")
		x.remove("a","q")
		x.put("b","q")
		assert x.get("b") == 'q', 'wrong value'
		try: print x.get("a")
		except noungraph.Ambiguity, a:
			assert a.possibles() == ['b','c','d'], 'wrong ambiguity list'
		x.remove("b","q")
		try: x.get("b")
		except KeyError: pass
		else: assert black is white, "should have thrown a key error"
		x.remove("a","d")
		x.remove("a","c")
		assert x.get("a") == 'b', 'wrong value'


noungraphCheck=makeCheck(NounGraphTestCase)

from twisted import reflect

class ReflectySaysNo: pass

class Reflecty(reflect.Accessor,reflect.Settable):
	def get_a(self):
		return 'a'
	
	def set_a(self,val):
		self.really_set('a',val)

	def del_a(self):
		pass # self.really_del('a')

	def set_b(self,b):
		self.really_set('_b',b)

	def get_b(self):
		return self._b

	def del_b(self):
		raise ReflectySaysNo()

class ReflectTestCase(unittest.TestCase):
	def setUp(self):
		self.r=Reflecty()

	def checkGet(self):
		r=self.r
		assert r.a == 'a', 'get not called'
		try: r.b
		except AttributeError: pass
		else: assert black is white, "nonexistant property didn't raise exception"

	def checkSet(self):
		r=self.r
		z='b'
		r.b=z
		assert r.b is z, "property became something different"
		r.a=z
		assert r.a is z, "property became something different"
		
	def checkDel(self):
		r=self.r
		try: del r.b
		except ReflectySaysNo: pass
		else: assert black is white, "exception not thrown"

		del r.a
		assert r.a == 'a', "deletion actually happened"

	def checkCall(self):
		self.r(a='foo',
			   b='bar')
		
		assert self.r.a == 'foo' and self.r._b == 'bar', 'calling failed'
		

reflectCheck=makeCheck(ReflectTestCase)

from twisted import tokenizer

class TokenTestCase(unittest.TestCase):
	
	def checkTokenization(self):
		import cStringIO
		cs=cStringIO.StringIO("""\
hello this is a big string i am going to [ read from ] and then ' foo ' blarg blarg blarg
	indent
	indent
		indent
		dedent
	dedent
dedent
foo { bar } (bar) "bar"
"""
							  )
		# correct result
		ct=((1, 'hello', 1), (1, 'this', 1), (1, 'is', 1),
			(1, 'a', 1), (1, 'big', 1), (1, 'string', 1),
			(1, 'i', 1), (1, 'am', 1), (1, 'going', 1),
			(1, 'to', 1), (37, '[', 1), (1, 'read', 1),
			(1, 'from', 1), (37, ']', 1), (1, 'and', 1),
			(1, 'then', 1), (3, ' foo ', 1), (1, 'blarg', 1),
			(1, 'blarg', 1), (1, 'blarg', 1), (1, 'indent', 2),
			(1, 'indent', 3), (1, 'indent', 4), (1, 'dedent', 5),
			(1, 'dedent', 6), (1, 'dedent', 7),(1, 'foo', 8),
			(37, '{', 8), (1, 'bar', 8), (37, '}', 8), (37, '(', 8),
			(1, 'bar', 8), (37, ')', 8), (3, 'bar', 8), (0, '', 9))
		
		t=tokenizer.Tokenizer(cs)

		for i in range(len(ct)):
			tk=t[i]
			assert (tk.ttype,tk.value,tk.line) == ct[i], 'data is wrong %s != %s' % (tk,ct)
		
tokenizerCheck=makeCheck(TokenTestCase)

from twisted import reality

class RealityTestCase(unittest.TestCase):

	def setUp(self):

		"""
.
+---+  +---+
| 2 |  | 4 |
+---+  +---+
  |      |
+---+  +---+
| 1 |--| 3 |
+---+  +---+
.
		"""
		self.bob=reality.Player("Bob")
		bob=self.bob
		room=reality.Room("Room")
		
		room.description="This is a description"
		room2=reality.Room("Room 2")
		room.add_exit("north",room2)
		room2.description="This is another description"
		room2.add_exit("south",room)
		room3=reality.Room("Room 3")
		room4=reality.Room("Room 4")

		room3.description="Room 3's description"
		room4.description="Room 4's description"

		room3.add_exit("west",room)
		room.add_exit("east",room3)

		room4.add_exit("south",room3)
		room3.add_exit("north",room4)

		ball=reality.Thing("Ball")

		ball.place=room
		
		bob.place=room
		self.room=room
		self.room2=room2
		self.ball=ball
		
	def checkMovingAround(self):
		bob=self.bob
		map(bob.execute,
			("go north",
			 "go south",
			 "go east",
			 "go west",
			 "go east",
			 "go north",
			 "go south",
			 "go west"))
		
		assert bob.place is self.room, 'bob ended up in the wrong place.'

	def checkMovingStuff(self):
		bob=self.bob
		map(bob.execute,
			("take ball",
			 "go east",
			 "go north",
			 "drop ball",
			 "go south",
			 "go north",
			 "take ball",
			 "go south",
			 "go west",
			 "go north",
			 "drop ball"))
		
		assert self.ball.place is self.room2

		map(bob.execute,
			("take ball",
			 "go south",
			 "drop ball"))
		
		assert self.ball.place is self.room
		
realityCheck=makeCheck(RealityTestCase)

from twisted import glip, gloop

# note to self; this is bad, bad stuff.

# gloop test case is broken, because handle_request creates its own
# thread using GlipServer.

class GloopTestCase(unittest.TestCase):
	def setUp(self):
		pass

	def checkGlipNetwork(self):
		class TestHandler(glip.GlipHandler):
			def queue(self,list):
				self.server.response=list
				self.write(list)
			def handle(self):
				# handle only 1 request
				self.queue(self.read())
				
		s=glip.Server(81324,TestHandler)
		l=['a','b',1,2,['a','x']]
		t=Thread(target=s.handle_one_request)
		t.start()
		c=glip.GlipClient('localhost',81324)
		c.write(l)
		al=c.read()
		t.join()
		c.connection.close()

		assert s.response == l , 'server didnt get it right'
		assert al == l, 'client didnt get back what it sent'

	def checkGloopNetwork(self):
		a=Asserter(1)
		gs=gloop.GloopServer(10101)
		gs["a"]=a
		t=Thread(target=gs.handle_one_request)
		t.start()
		gc=gloop.GloopClient('localhost',10101)
		gc.start_reading()
		x=gc["a"]
		x.run(1)
		gc.send_logout()
		gc.read_thread.join()
		#gc.connection.close()
		del gc
		t.join()
		a.post()

	def checkBadGloopLogin(self):
		portnum=500050
		#explicitly; no users
		gs=gloop.GloopServer(portnum, glip.Authenticator({'groovy':'baby'}))
		t=Thread(target=gs.handle_one_request)
		t.start()
		try: gc=gloop.GloopClient('127.0.0.1',portnum)
		except glip.Unauthorized: pass
		else: assert black is white, "I shouldn't be able to log in..."
		t.join()
		
gloopCheck=makeCheck(GloopTestCase)

from twisted.pagedfile import PagedFile

class PagedFileTest(unittest.TestCase):
	def checkGeneral(self):
		p=PagedFile("Hello.pgf",100)
		p[-1].header.nextfree=500
		p[0].header.nextfree=500
		p[0][0]='start'
		p[10][5:15]='0123456789'
		p[5][0]='asdfasdfasdf'

pagedCheck=makeCheck(PagedFileTest)

def test():
	runner=unittest.TextTestRunner()
	runner.run(unittest.TestSuite
			   (delayCheck+observableCheck+noungraphCheck+reflectCheck+
				tokenizerCheck+realityCheck+gloopCheck+pagedCheck))
	
if __name__=='__main__':
	test()

