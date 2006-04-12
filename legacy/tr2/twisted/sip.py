#!/usr/bin/env python

"""
Simple Internet Protocol

A very simple set of classes for sending packets prefixed with their
length.  Optimized to be friendly to select().
"""

from struct import pack, unpack
from types import StringType
from threading import RLock

SocketError=error
del error
from select import select

from errno import EAGAIN

CONNECTION_LOST=-1

class ConnectionLost(Exception): pass


class Client:
	def __init__(self,host,port):
		
			

class Handler:
	state='init'
	def callback(self,string):
		try:
			pto='proto_'+self.state
			statehandler=getattr(self,pto)
			
		except AttributeError:
			print 'callback',self.state,'not found'
		else:
			# try/except madness here?
			self.state=statehandler(string)
			if self.state == 'done':
				self.server.remove_read(self)

class Server:
	handler=Handler
	def __init__(self, port):
		skt=socket(AF_INET,SOCK_STREAM)
		skt.bind( ('',port) )
		skt.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
		skt.listen(5)
		self.socket=skt
		self.readlist=[self]
		self.writelist=[]
		self.running=1
		self.fileno=self.socket.fileno

	def serve(self):
		while self.running:
			print 'polling'
			reads,writes,ignored=select(self.readlist,
										self.writelist,
										[])
			print 'not polling'
			for reader in reads:
				try:
					reader.do_read()
				except ConnectionLost:
					print reader,'is unreadable'
					reader.conn_lost()
					import traceback
					traceback.print_exc()
					self.remove_read(reader)
			for writer in writes:
				try:
					writer.do_write()
				except ConnectionLost:
					self.remove_write(writer)

	def conn_lost(self):
		print 'server socket connection lost'
	def do_read(self):
		skt,addr=self.socket.accept()
		self.add_read(self.handler(skt,addr,self))

	def add_read(self, reader):
		self.readlist.append(reader)

	def remove_read(self, reader):
		self.readlist.remove(reader)

	def add_write(self, writer):
		self.writelist.append(writer)

	def remove_write(self, writer):
		self.writelist.remove(writer)
