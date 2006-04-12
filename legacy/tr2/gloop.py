#!/usr/bin/env python

"""G.L.O.O.P.

The _G_eneric, _L_ist and _O_bject _O_riented _P_rotocol

Version 0.3, (C) 2000 Twisted Matrix Enterprises

This is a generic, multi-tiered, list and object transmission
protocol.

As implemented here, it works for transparent remote method
invocation.  There was a working Java binding at one point; the stub
generator still works, and when I get around to it again, there will
probably be a full implementation of this in both Java and C.

WARNING: this is a DEVELOPMENT VERSION of this protocol!
"""

##################
# standard imports

from struct import pack, unpack, calcsize
from crypt import crypt
from random import randint
from types import IntType, StringType, TupleType, NoneType
from threading import Thread, Condition, RLock

from threading import _get_ident,_active,_DummyThread
# currentThread uses 'print'; that's no good.
def currentThread():
	try: return _active[_get_ident()]
	except KeyError: return _DummyThread()
# del _get_ident,_active,_DummyThread # can't do this...

from cStringIO import StringIO
from sys import exc_info
from traceback import print_exc
from socket import socket,error,AF_INET,SOCK_STREAM,SOL_SOCKET,SO_REUSEADDR,MSG_WAITALL

SocketError=error
del error
from select import select
from errno import EAGAIN
from time import strftime,localtime,time,sleep
from string import replace
from Queue import Queue, Full

import sys

# make sure exceptions go to the main thread!
import signal

gloop_threads={ }

############
# some stuff for logging
file_protocol=['close', 'closed', 'fileno',
			   'flush', 'isatty', 'mode',
			   'name', 'read', 'readinto',
			   'readline', 'readlines', 'seek',
			   'softspace', 'tell', 'truncate',
			   'write', 'writelines']

class Log:
	def __init__(self, file):
		self.file=file
		self.lock=RLock()
		for attr in file_protocol:
			if not hasattr(self,attr):
				setattr(self,attr,getattr(file,attr))

	def write(self,bytes):
		self.lock.acquire()
		
		try:
			try:  gloop=gloop_threads[currentThread()]
			except KeyError: pass
			else: bytes=gloop.log(bytes)

			self.file.write(bytes)
			self.file.flush()
		finally:
			self.lock.release()

	def writelines(self, lines):
		self.lock.acquire()
		try:
			for line in lines:
				self.write(line)
		finally:
			self.lock.release()

class PseudoMethod:
	def __init__(self, object):
		self.object=object

class GetItem(PseudoMethod):
	def __call__(self, item): return self.object[item]

class SetItem(PseudoMethod):
	def __call__(self, key, val): self.object[key]=val

class DelItem(PseudoMethod):
	def __call__(self, key): del self.object[key]

class GetSlice(PseudoMethod):
	def __call__(self, begin,end): return self.object[begin:end]

class SetSlice(PseudoMethod):
	def __call__(self, begin,end,val): self.object[begin:end]=val

class DelSlice(PseudoMethod):
	def __call__(self, begin,end): del self.object[begin:end]

class Len:
	def __call__(self): return len(self.object)

special_method={"__getitem__":  GetItem,
				"__setitem__":  SetItem,
				"__delitem__":  DelItem,
				"__getslice__": GetSlice,
				"__setslice__": SetSlice,
				"__delslice__": DelSlice,
				"__len__":      Len
				}

WorkerStop=None

class ThreadPool:
	def __init__(self,minthreads=5,maxthreads=100,qlen=1000):
		assert minthreads <= maxthreads, 'minimum is greater than maximum'
		self.q=Queue(qlen)
		self.max=maxthreads
		self.waiters=[]
		self.threads=[]
		self.working={}
		self.workers=0
		self.joined=0
		for i in range(minthreads):
			self.start_worker()
		self.mutex=RLock()
		
	def start_worker(self):
		self.workers=self.workers+1
		Thread(target=self.worker).start()
	
	def dispatch(self, func, *args, **kw):
		if self.joined: return
		o=(func,args,kw)
		
		self.mutex.acquire()
		if not self.waiters:
			if self.workers < self.max:
				self.start_worker()
		self.mutex.release()
		
		self.q.put(o)

	def worker(self):
		ct=currentThread()
		self.threads.append(ct)
		while 1:
			self.waiters.append(ct)
			o=self.q.get()
			self.waiters.remove(ct)
			if o == WorkerStop: break
			try:
				self.working[ct]=o
				apply(apply,o)
			except:
				print 'exception in pool'
				print_exc()
				exc=exc_info()
				if isinstance(exc[1],GloopException):
					print exc[1].traceback
				
			del self.working[ct]
		self.threads.remove(ct)
		self.workers=self.workers-1

	def join(self):
		self.mutex.acquire()
		self.joined=1
		from copy import copy
		threads=copy(self.threads)
		for thread in range(self.workers):
			self.q.put(WorkerStop)

		# and let's just make sure
		for thread in threads:
			thread.join()
		self.mutex.release()

####################
# typecode constants

LIST=31
STRING=32
INT=33
BYTE=34
SHORT=35
REFERENCE=36
VOID=37

##########################################
# this should be in the standard library ;)

def nop(*args): pass

def fail(gloop, object, member):
	"The simplest, and probably most common, filter."
	assert 0, 'Disallowed.'

###################
# writing functions

def writer(typechar):
	def writeX(data, file, typechar="!%s"%typechar):
		return file.write(pack(typechar, data))
	return writeX

writeVoid=nop
writeShort=writer("H")
writeByte=writer("B")
writeInt=writer("i")

def writeString(string,file):
	writeShort(len(string),file)
	file.write(string)
	
_longdivisor=2**32L	
def writeLong( lng, file):
	file.write(pack("!lL", lng/_longdivisor,lng % _longdivisor))

writes={IntType: writeInt,
		StringType: writeString,
		NoneType: writeVoid}

codes={TupleType: LIST,
	   StringType: STRING,
	   IntType: INT,
	   NoneType: VOID}

class Output:
	def writeList(self, lst, file):
		writeShort(len(lst),file)
		for i in lst: self.write(i,file)

	def write(self,dat,file):
		typ=type(dat)
		code=codes.get(typ) or REFERENCE
		if typ == TupleType: write=self.writeList
		else: write=writes.get(typ) or self.writeReference
		writeByte(code,file)
		write(dat,file)
		
	def encode(self, data):
		wfile=StringIO()
		self.write(data,wfile)
		return wfile.getvalue()


###################
# reading functions
	
def reader(typechar):
	def readX(file, typechar="!%s"%typechar):
		return unpack(typechar,file.read(calcsize(typechar)))[0]
	return readX

readVoid=nop
readShort=reader("H")
readByte=reader("B")
readInt=reader("i")

def readLong(file):
	data=file.read(8)
	result=unpack("!lL",data)
	result=(result[0] * (2**32L) )+result[1]
	return result

def readString(file):
	return file.read(readShort(file))

reads={STRING: readString,
	   INT: readInt,
	   SHORT: readShort,
	   BYTE: readByte,
	   VOID: readVoid}
	
class Input:
	def readList(self,file):
		result=range(readShort(file))
		for i in result:
			result[i]=self.read(file)
		return tuple(result)
	
	def read(self,file):
		typ=readByte(file)
		try: read=reads[typ]
		except KeyError:
			if typ == LIST: read=self.readList
			else:           read=self.readReference
		return read(file)
	
	def decode(self, bytes):
		return self.read(StringIO(bytes))

class GloopException(Exception):
	traceback="<<no traceback>>"
	
class ConnectionLost(Exception):
	pass
	
class NotReadyYet:
	pass

class Unauthorized(Exception):
	pass

class Glob:
	"""Glob(gloop,glid)

	This is a transparent reference to a remote object.
	
	It can *ALSO* act as a message-passing system; if you want it to
	do that, call glob.__message_callback__('callback_name', callback,
	error_callback).  Then, every time you run glob.callback_name(),
	it'll send that message to the other side, but return immediately.
	When a response is available, the specified callback will be
	invoked (or the error callback, if the invocation was not
	successful).

	The callback will be invoked with a single argument, that being
	the return value of the message.  The error callback will be
	invoked with a GloopException describing the error.
	"""
	def __init__(self, gloop,glid):
		self.__dict__['glid']=glid
		self.__dict__['gloop']=gloop
		self.__dict__['_messengers']={}
		self.__dict__['_messenger']=None
		
	def __setattr__(self, key,attr):
		if self._messengers:
			raise "attribute assignment attempted on messengers object"
		s=self.gloop.request_id()
		self.gloop.send_((Gloop.SET, s, object, key, value))
		self.gloop.wait_for(s)
		
	def __getattr__(self, key):
		try: return MessageMethod(self, key, self._messengers[key])
		except KeyError:
			r=self.gloop.request_id()
			self.gloop.send_((Gloop.GET, r, self.glid, key))
			return self.gloop.wait_for(r)

	def __message_callback__(self, key,callback=None,errback=None):
		self.__dict__['_messengers'][key]=(callback,errback)

	def __message__(self,call=None,err=None):
		self.__dict__['_messenger']=(call,err)
		
	def __call__(self, *args):
		gloop=self.gloop
		r=gloop.request_id()
		if self._messenger:
			gloop.register_callback(r, self._messenger)
			gloop.send_((Gloop.CALL, r, self.glid)+args)
		else:
			gloop.send_((Gloop.CALL, r, self.glid)+args)
			return gloop.wait_for(r)

	def __str__(self):
		gloop=self.gloop
		return "<Glob(%d-%s@%s)>" % (self.glid,gloop.username,gloop.hostname)
	
	def __repr__(self):
		return self.__str__()
	
	def __del__(self):
		try:    self.gloop.send_((Gloop.FORGET, object))
		except: pass

	# sigh
	def __cmp__(self,other):
		return cmp(hash(self),other)
	
	def __hash__(self):
		return self.glid

class MessageMethod:
	def __init__(self, glob,key,callbacks):
		self.glob=glob
		self.key=key
		self.callbacks=callbacks
		
	def __call__(self, *args):
		glob=self.glob
		gloop=glob.gloop
		r=glob.gloop.request_id()
		stupl=(Gloop.MESSAGE,r,glob.glid,self.key)+args
		#print 'MESSAGE',stupl
		gloop.send_(stupl)
		gloop.register_callback(r,self.callbacks)


# There are 7 kinds of protocol statements:

# NAME request "name"
# SET request object "member" value
# GET request object "member"
# FORGET object
# CALL request object *args
# MESSAGE request object "message" *args

# ANSWER request value
# ERROR request value traceback

class Gloop(Input,Output):
	
	"""Gloop([naming [,threaded]])
	
	The Generic List and Object Oriented Protocol
	"""
	FORGET=49
	SET=50
	GET=51
	CALL=52
	ANSWER=53
	ERROR=54
	NAME=55
	MESSAGE=56
	LOGOUT=57
	SUCCESS=0
	
	read_thread=None
	username='server'
	hostname='local'
	__commands={SET: 'got_set',
				GET: 'got_get',
				FORGET: 'got_forget',
				CALL: 'got_call',
				NAME: 'got_name',
				ANSWER: 'got_answer',
				ERROR: 'got_error',
				MESSAGE: 'got_message',
				LOGOUT: 'got_logout'}
	
	__final_error=None
	
	def __init__(self, naming=None,threaded=1):
		"Initialize this Gloop instance, with the given registry"
		
		self.__references={}
		self.__answers={}
		self.__callbacks={}
		self.__naming=naming or {}
		self.__filters=[]

		self.threaded=threaded
		if threaded:
			self.__condition=Condition()
		
		self.__request=0

		self.logged_out=0

	def startup(self):
		pass
	def init(self):
		pass

	def wake_up(self):
		if self.threaded:
			c=self.__condition
			c.acquire()
			c.notify()
			c.release()
				
	def register(self, object):
		refs=self.__references
		ido=id(object)
		if refs.has_key(ido):
			refs[ido][1]=refs[ido][1]+1
		else:
			refs[ido]=[object,1]
		return ido

	def unregister(self, object):
		refs=self.__references
		if refs.has_key(object):
			count=refs[object][1]
			if count == 1:
				del refs[object]
			else:
				refs[object][1]=count-1

	def registered(self, object):
		return self.__references[object][0]
	
	def read_forever(self):
		"""Gloop.read_forever() -> ...

		This never returns.  Call it to run a Gloop input loop forever.
		"""
		try:
			self.read_thread=currentThread()
			self.startup()
			while not self.logged_out:
				self.parse(self.recv_())
		finally:
			del self.read_thread
			self.__final_error=GloopException("Read Thread Interrupted")
			self.wake_up()
		
	def add_filter(self, filter):
		"""Gloop.add_filter(filter) -> None

		Adds a filter to the list of filters.  A filter should be a
		callable object which accepts 3 arguments: 'gloop', 'object'
		and 'member'.  The first argument is the Gloop from which the
		attribute is being requested.  The second is the object which
		an attribute is being requested on.  The third is the name of
		the attribute.

		The attribute will be registered and returned to the
		requesting client unless an exception is thrown by a filter.
		By default, there are no filters.

		NOTE: Once a reference has been retrieved, it is possible to
		CALL it; in order to remain orthogonal, MESSAGE is disallowed
		along with GET (using the same filters).
		"""
		self.__filters.append(filter)


	def add_name(self, name, binding):
		"""Gloop.add_name(name,binding) -> None

		This adds an accessible name to the client.
		"""
		self.__naming[name]=binding

	def writeReference(self, ref, file):
		self.register(ref)
		writeInt(id(ref),file)

	def readReference(self, file):
		return Glob(self,readInt(file))
	
	def deny_get(self):
		self.add_filter(fail)
		
	def run_filters(self, object, member):
		for filter in self.__filters:
			filter(self,object,member)
		
	def start_reading(self):
		if self.threaded:
			self.read_thread=Thread(target=self.read_forever)
			self.read_thread.start()
			return
		raise GloopException('unthreaded thread start?')
		
	def register_callback(self, request, callback):
		self.__callbacks[request]=callback
	
	def got_set(self, request,object,member,value):

		try:
			setattr(self.registered(object), member,value)
		except:
			self.send_error(request, "Couldn't set %s to %s" %
							(member, str(value)),exc_info())
		else: self.send_answer(request, Gloop.SUCCESS)

	def got_call(self, request,object,*args):

		try:
			rfunc=self.registered(object)
			result=apply(rfunc,args)
		except:
			exc=exc_info()
			try: err="could not invoke %s" % repr(rfunc)
			except NameError: err="could not invoke %s" % str(object)
			self.send_error(request, err, exc)
		else: self.send_answer(request, result)

	def got_logout(self):
		if not self.logged_out:
			self.logged_out=1
			self.send_logout()
			
	def got_message(self, request,object,message,*args):
		try:
			#print 'request: ',request
			#print 'object: ',object
			#print 'message: ',message
			#print 'args: ',args

			object=self.registered(object)
			self.run_filters(object,message)
			result=apply(getattr(object,message),args)
		except: self.send_error(request, "message handling failed",exc_info())
		else:   self.send_answer(request,result)

	def got_name(self, request,name):
		try:    w=self.__naming[name]
		except: self.send_error(request,"No such object %s"%repr(name),exc_info())
		else:   self.send_answer(request,w)
	
	def got_get(self, request,object,member):
		try:
			object=self.registered(object)
			self.run_filters(object,member)
			try: result=special_method[member](object)
			except: result=getattr(object, member)
		except: self.send_error(request,"no such value %s " % member,exc_info())
		else:   self.send_answer(request, result)

	def got_answer(self, request,value):
		try:
			callback=self.__callbacks[request][0]
			del self.__callbacks[request]
		except KeyError:
			self.__answers[request]=(Gloop.ANSWER,value)
			self.wake_up()
		else:
			if callback is not None:
				callback(value)

	def got_forget(self, obj):
		self.unregister(obj)
		
	def got_error(self, request,value,tb):
		ge=GloopException(value)
		ge.traceback=tb
		try:
			callback=self.__callbacks[request][1]
			del self.__callbacks[request]
		except KeyError:
			self.__answers[request]=(Gloop.ERROR,ge)
			self.wake_up()
		else:
			if callback is not None:
				callback(ge)
	
	def request_id(self):
		self.__request=self.__request+1
		return self.__request

	def wait_for(self,r):
		thread=self.threaded and self.read_thread is not currentThread()
		if thread and self.read_thread is None:
			raise GloopException('read thread gone')
		while 1:
			if thread: self.__condition.acquire()
			try:
				try:
					return self.ansorerr(r)
				except NotReadyYet:
					if thread: self.__condition.wait()
					else:      self.parse(self.recv_())
			finally:
				if thread: self.__condition.release()
				
	def ansorerr(self,r):
		try:
			x=self.__answers[r]
			del self.__answers[r]
		except KeyError:
			if self.__final_error:
				raise self.__final_error
		else:
			if x[0]==Gloop.ANSWER: return x[1]
			else: raise x[1]

		
		raise NotReadyYet()

	def end_threads(self):
		self.__condition.acquire()
		self.__condition.notifyAll()

		self.__final_error=GloopException("Threads Terminated")
		
		self.__condition.release()

	def send_(self,data):
		self.write(data)

	def recv_(self):
		return self.read()

	def send_logout(self):
		self.logged_out=1
		self.send_((Gloop.LOGOUT,))
		
	def send_answer(self, request,result):
		self.send_((Gloop.ANSWER, request,result)) # don't wait for anything, obviously

	def send_error(self, request,result,exc):
		io=StringIO()
		io.write("* Gloop Remote Traceback: %s@%s\n"%(self.username,self.hostname))
		print_exc(file=io)
		if isinstance(exc[1],GloopException):
			io.write("\n"+exc[1].traceback)
		self.send_((Gloop.ERROR, request,result,io.getvalue()))
	
	def send_name(self, name):
		r=self.request_id()
		self.send_((Gloop.NAME, r, name))
		return self.wait_for(r)
	
	__getitem__=send_name

	held_threads=0

	def take_control(self):
		ct=currentThread()
		try:
			older=gloop_threads[ct]
			older.held_threads=older.held_threads-1
		except: pass
		self.held_threads=self.held_threads+1
		gloop_threads[currentThread()]=self
		try: return older
		except: return None

	def give_control(self,older):
		ct=currentThread()
		if older:
			gloop_threads[ct]=older
			older.held_threads=older.held_threads+1
		else:
			del gloop_threads[ct]
		self.held_threads=self.held_threads-1
		
	def parse(self, lst):
		"dispatch a protocol message"
		latent=is_latent(lst)
		if self.threaded and latent:
			older=self.take_control()
		try:
			cmd=lst[0]
			arg=tuple(lst[1:])
			apply(getattr(self,self.__commands[cmd]), arg)
		finally:
			if self.threaded and latent:
				self.give_control(older)
	written=1
	def log(self,bytes):
		written=self.written
		if bytes[-1]=='\n':
			self.written=self.written+1
			bytes=replace(bytes[:-1],'\n','\n'+self.__format())+'\n'
		else:
			bytes=replace(bytes,'\n','\n'+self.__format())
		if written:
			bytes=self.__format()+bytes
			self.written=self.written-1
		return bytes

	def __format(self):
		return ("%s %s@%s"%(self.sessionno,self.username,self.hostname))+strftime(' %d/%b/%Y %T - ',localtime(time()))

# my silly little security thingy

def multicrypt(password,salt):
	"""multicrypt(password,salt) -> incomprehensible gibberish

	This crypts a password 4 times, with an 8 character salt.  This is
	for sending a password from a client to a server, so the server
	does not need to know the real password, and the real password
	need not be sent on the wire.
	
	"""
	return crypt(crypt(crypt(crypt(password,salt[0:2]),salt[2:4]),salt[4:6]),salt[6:8])

def lesscrypt(password,salt):
	"""lesscrypt(password,salt) -> slightly less incomprehensible gibberish

	This crypts a password 3 times, with an 8 character salt: the
	first possible crypt (with the first 2 characters) is omitted.
	This is for receiving a password on a server.
	"""
	return crypt(crypt(crypt(password,salt[2:4]),salt[4:6]),salt[6:8])

def mkpasswd(plaintext):
	return crypt(plaintext,chr(randint(65,90))+chr(randint(97,122)))

def is_latent(message):
	return message[0] not in (Gloop.ANSWER, Gloop.ERROR,
							  Gloop.FORGET, Gloop.LOGOUT,
							  Gloop.NAME  )

class Authenticator:
	def __init__(self, userdict=None, encrypted=0):
		self.userdict=userdict or {'guest':'guest'}
		
		if self.userdict and not encrypted:
			for u,p in self.userdict.items():
				self.add_user(u,p)
				
	def add_user(self, user,password):
		self.userdict[user]=mkpasswd(password)

	def get_password(self, username):
		return self.userdict[username]
		
	def challenge(self, user):
		try: salt=self.get_password(user)[:2]
		except KeyError:
			salt=chr(randint(65,90))+chr(randint(65,90))
		for i in range(6):
			salt=salt+chr(randint(65,90))
		return salt

	def authenticate(self, user,salt,saltpass):

		try: pw=self.get_password(user)
		except: pass
		else:
			if lesscrypt(pw,salt)==saltpass:
				return user
		raise Unauthorized()


class Handler(Gloop):
	state='init'
	def __init__(self, socket,client,server):

		self.__wremove=0
		self.socket=socket
		self.socket.setblocking(0)
		self.server=server
		self.client=client
		self.hostname=client[0]
		self.fileno=self.socket.fileno
		self.unsent=""
		self.recvbuf=""
		self.slock=RLock()
		
		self.getting_len=1
		self.unrecd=4

		self.read_thread=1
		Gloop.__init__(self)
		
	def send(self, data):
		self.slock.acquire()
		try:
			assert type(data) == StringType, "Data must be a string."
			unsent=self.unsent
			self.unsent=unsent+pack("!i",len(data))+data
			self.do_write()
		finally: self.slock.release()

	def do_write(self):
		self.slock.acquire()
		try:
			self.unsent=self.unsent[esend(self.socket,self.unsent):]
			if self.unsent:
				self.__wremove=1
				self.server.add_read(self)
			elif self.__wremove:
				self.server.remove_write(self)
				self.__wremove=0
		finally:
			self.slock.release()

	def do_read(self):
		while 1:
			while self.unrecd:
				recd=erecv(self.socket,self.unrecd)
				if recd:
					self.unrecd=self.unrecd-len(recd)
					self.recvbuf=self.recvbuf+recd
					if self.unrecd == 0:
						buf=self.recvbuf
						self.recvbuf=""
						if self.getting_len:
							self.getting_len=0
							self.unrecd=unpack("!i",buf)[0]
							if self.unrecd==0:
								self.callback('')
						else:
							self.callback(buf)
							# hmm.
							return
				else: return
				
			self.unrecd=4
			self.getting_len=1
			
	def callback(self,string):
		try:
			pto='proto_'+self.state
			statehandler=getattr(self,pto)
		except AttributeError:
			print 'callback',self.state,'not found'
		else:
			self.state=statehandler(string)
			if self.state == 'done':
				self.server.remove_read(self)

	def authorize(self):
		self.init()
		self.server.pool.dispatch(self._startup)
		return 'gloop'

	def conn_lost(self):
		if self.threaded:
			o=self.take_control()
		try:
			self.end_threads()
			self.cleanup()
		finally:
			if self.threaded:
				self.give_control(o)

	def cleanup(self):
		pass

	def proto_init(self, username):
		self.username=username
		self.challenge=self.server.authenticator.challenge(username)
		self.send(self.challenge)
		return 'password'

	def proto_password(self, password):
		try:
			self.server.authenticator.authenticate(self.username,
												   self.challenge,
												   password)
			self.send(self.username)
			return self.authorize()
		except Unauthorized:
			self.send('')
			return 'done'

	def proto_gloop(self,packet):
		message=self.decode(packet)
		if is_latent(message):
			self.server.pool.dispatch(self.parse,message)
		else:
			self.parse(message)
		return 'gloop'

	def _startup(self):
		if self.threaded:
			o=self.take_control()
		try:
			self.startup()
		finally:
			if self.threaded:
				self.give_control(o)
	
	
	def send_(self,data):
		self.send(self.encode(data))

	def recv_(self):
		print 'WAARRRNNNIIINNNGGGG'

def eapply(func,*args):
	try:
		result=apply(func,args)
		return result
	except SocketError, se:
		if se.args[0] == EAGAIN: return 0
		# ECONNRESET, EPIPE?  I don't know if I can find a
		# comprehensive list of all reasons that a socket can close,
		# so I'll just assume that if we're throwing non-EAGAIN
		# exceptions it's bad.
		else: raise ConnectionLost(se)

def erecv(socket,len):
	bytes=eapply(socket.recv,len)
	if bytes == 0: return ""
	elif bytes == '': raise ConnectionLost()
	return bytes

def esend(socket,data):
	return eapply(socket.send, data)

		
class Server:
	handler=Handler
	authenticator=Authenticator()
	sessionno=0
	def __init__(self, port):
		skt=socket(AF_INET,SOCK_STREAM)
		skt.bind( ('',port) )
		self.port=port
		skt.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
		skt.listen(5)
		self.socket=skt
		self.readlist=[self]
		self.writelist=[]
		self.running=1
		self.fileno=self.socket.fileno

		self.pool=ThreadPool(1,2)
		self.init()

	def serve(self):
		sys.stdout=Log(sys.stdout)
		sys.stderr=Log(sys.stderr)
		try:
			print 'Started %s on port %d.'%(self.__class__.__name__,self.port)
			while 1:
				reads,writes,ignored=select(self.readlist,
											self.writelist,
											[])
				for reader in reads:
					try:
						reader.do_read()
					except ConnectionLost:
						reader.conn_lost()
						self.remove_read(reader)
				for writer in writes:
					try:
						writer.do_write()
					except ConnectionLost:
						self.remove_write(writer)

		except:
			print 'trying to shut down as cleanly as possible...'
			print 'readlist:',self.readlist
			for i in self.readlist:
				i.conn_lost()
			print 'queue:',self.pool.q.queue
			print 'waiters:',self.pool.waiters
			print 'workers:',self.pool.working
			print 'total:',self.pool.threads
			self.pool.join()
		sys.stdout=sys.stdout.file
		sys.stderr=sys.stderr.file
		self.socket.close()
			
	def conn_lost(self): pass
		
	def do_read(self):
		skt,addr=self.socket.accept()
		handler=self.handler(skt,addr,self)
		handler.sessionno=self.sessionno
		self.sessionno=self.sessionno+1
		self.add_read(handler)

	def add_read(self, reader):
		self.readlist.append(reader)

	def remove_read(self, reader):
		self.readlist.remove(reader)

	def add_write(self, writer):
		self.writelist.append(writer)

	def remove_write(self, writer):
		self.writelist.remove(writer)

	def init(self): pass

class Client(Gloop):
	def __init__(self, host,port,username,password, threaded=1):

		self.socket=socket(AF_INET,SOCK_STREAM)
		self.socket.connect((host, port))
		self.socketlock=RLock()
		
		self.send(username)
		self.challenge=self.recv()
		self.send(multicrypt(password,self.challenge))
		if not self.recv():
			raise Unauthorized()

		Gloop.__init__(self, threaded=threaded)
		self.init()
		if threaded:
			self.start_reading()
		else:
			self.startup()

	def send(self,bytes):
		self.socketlock.acquire()
		try:     self.socket.send(pack("!i", len(bytes))+bytes)
		finally: self.socketlock.release()
			
	def recv(self):
		ln=unpack("!i", self.socket.recv(4))[0]
		result=self.socket.recv(ln)
		return result
		
	def init(self): pass

	def recv_(self):
		return self.decode(self.recv())
	
	def send_(self,data):
		self.send(self.encode(data))
