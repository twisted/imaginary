#!/usr/bin/env python
from gloop import *
from twisted import reality
from twisted import ui
import sys
portno=8889

class RealityHandler(Handler,ui.LocalIntelligence):
	def init(self):
		user=self.server.reality[self.username]
		self.ux=user
		self.add_name('verb', user)
		
	def startup(self):
		self.remote=self['client']
		self.ux.intelligence=self
		print self.ux.name,'logged in.'

	def cleanup(self):
		del self.ux.intelligence
		# game-specific stuff, maybe?
		print self.ux.name,'logged out.'
		
class RealityAuthenticator(Authenticator):
	def __init__(self, world):
		self.reality=world
	def get_password(self, user):
		try:    return self.reality[user].password
		except:
			raise KeyError('bad login')

class RealityPump(Server):
	handler=RealityHandler
	def __init__(self, world):
		Server.__init__(self, portno)
		self.reality=world
		self.authenticator=RealityAuthenticator(self.reality)

if __name__=='__main__':
	from twisted import copyright
	
	print copyright.longversion
	print copyright.disclaimer
	print copyright.copyright
	try:
		mapname=sys.argv[1]
		from cPickle import load
		print 'Loading %s...'%mapname,
		sys.stdout.flush()
		reality.default_reality=load(open(mapname))
		print 'Loaded.'
	except IndexError:
		print "Loading defaults...",
		sys.stdout.flush()
		import rpl
		print "Loaded."
	RealityPump(reality.default_reality).serve()
