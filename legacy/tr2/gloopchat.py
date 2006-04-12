#!/usr/bin/env python

from gloop import *

portno=40398

class ChatHandler(Handler):
	def init(self):
		self.add_name('chat',self.do_chat)
		
	def startup(self):
		self.talkback=self['chat']
		self.server.add_chatter(self)
		
	def do_chat(self,words):
		if not hasattr(self,'uname'):
			self.uname=self['name']
		self.server.chat(self.uname,words)

class ChatServer(Server):
	handler=ChatHandler
	def init(self):
		self.chatters=[]

	def add_chatter(self,chatter):
		self.chatters.append(chatter)

	def chat(self, user, words):
		#from time import sleep
		#sleep(.05)
		for chatter in self.chatters[:]:
			# this is an insanely common programming error.
			# print chatter.talkback, user, words
			try:
				print 'hello'
				chatter.talkback(user,words)
			except ConnectionLost,cl:
				print 'excepted gloop...'
				import traceback
				traceback.print_exc()
				self.chatters.remove(chatter)
			except GloopException:
				self.chatters.remove(chatter)

class ChatClient(Client):

	def init(self):
		self.add_name('chat',self.chat)
		self.add_name('name',self.user_name())

	def chat(self,otheruser,words):
		print otheruser,'sez: ',words

	def user_name(self):
		return self.challenge
		
	def run(self):
		self.do_chat=self['chat']
		while 1:
			try:
				#x=raw_input('chat: ')
				x='bark'
				print 'doing chat'
				self.do_chat(x)
			except GloopException,ge:
				print ge.traceback


if __name__=='__main__':
	import sys
	from getpass import getpass
	if sys.argv[1] == 'client':
		#u=raw_input("username: ")
		#p=getpass("password: ")
		u=p='guest'
		cc=ChatClient('localhost',portno,u,p)
		cc.run()
	else:
		s=ChatServer(portno)
		s.serve()
