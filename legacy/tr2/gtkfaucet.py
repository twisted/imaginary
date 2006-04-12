#!/usr/bin/env python


# Okay.  It doesn't do themes, it doesn't even do inventory; but it
# does descriptive elements and it has a command buffer.  So we have
# something you can connect with. That's cool, right? ;-)

import sys
try: import gtktheme
except: pass
import gtk
import gnome.ui
import string
from threading import currentThread
from gloop import Client
portno=8889

class RealityClient(Client):
	def init(self):
		self.add_name('client',self)

		# prevent against race conditions if we type too fast / send
		# scripted shit
		
		self.pending=[]
		
	def startup(self):
		self.sendVerb_=self['verb']
		self.sendVerb_.__message_callback__('execute',self.fin_verb,self.err_verb)

	def sendVerb(self,verb):
		if not self.pending:
			self.do_now(verb)
		self.pending.append(verb)

	def do_now(self,verb):
		self.event("> "+verb)
		self.cmdarea.set_text(verb)
		self.sendVerb_.execute(verb)

	def verb_done(self):
		del self.pending[0]
		if self.pending:
			self.cmdarea.set_text(self.pending[0])
			self.do_now(self.pending[0])
		else:
			self.cmdarea.set_sensitive(gtk.TRUE)
			self.cmdarea.set_editable(gtk.TRUE)
			self.focus_text()
			self.cmdarea.set_text("")
		
	def err_verb(self,nne):
		self.event(nne.traceback)
		self.verb_done()
		
	def fin_verb(self,nne):
		self.verb_done()

def scrollify(widget):
	widget.set_word_wrap(gtk.TRUE)
	scrl=gtk.GtkScrolledWindow()
	scrl.add(widget)
	scrl.set_policy(gtk.POLICY_NEVER, gtk.POLICY_ALWAYS)
	# scrl.set_update_policy(gtk.POLICY_AUTOMATIC)
	return scrl

def defocusify(widget):
	widget.unset_flags(gtk.CAN_FOCUS)


def gtktextget(text):
	return text.get_chars(0,text.get_length())
def dontgo(*ev):
	return gtk.TRUE

class ResponseWindow(gtk.GtkWindow):
	def __init__(self,question,default,callifok,callifcancel):
		gtk.GtkWindow.__init__(self)
		self.callifok=callifok
		self.callifcancel=callifcancel
		if callifok is not None:
			callifok.__message__()
		if callifcancel is not None:
			callifcancel.__message__()
		self.text=gtk.GtkText()
		self.set_title(question)
		self.text.set_editable(gtk.TRUE)
		self.text.insert_defaults(default)
		scrl=scrollify(self.text)
		vb=gtk.GtkVBox()
		bb=gtk.GtkHButtonBox()
		vb.pack_start(scrl)
		bb.set_spacing(0)
		bb.set_layout(gtk.BUTTONBOX_END)
		cancelb=gnome.ui.GnomeStockButton(gnome.ui.STOCK_BUTTON_CANCEL)
		bb.add(cancelb)
		okb=gnome.ui.GnomeStockButton(gnome.ui.STOCK_BUTTON_OK)
		cancelb.set_flags(gtk.CAN_DEFAULT)
		okb.set_flags(gtk.CAN_DEFAULT)
		okb.set_flags(gtk.HAS_DEFAULT)
		bb.add(okb)
		okb.connect('clicked',self.callok)
		cancelb.connect('clicked',self.callcancel)
		vb.add(bb,expand=gtk.FALSE)
		
		self.add(vb)
		self.set_usize(300,200)
		self.connect('delete_event',dontgo)
		self.show_all()

	def callok(self,*ev):
		if self.callifok is not None:
			self.callifok(gtktextget(self.text))
		self.destroy()

	def callcancel(self,*ev):
		if self.callifcancel is not None:
			self.callifcancel()
		self.destroy()

	
class GameWindow(RealityClient,gtk.GtkWindow):

	request=ResponseWindow
	
	shortcuts={"n":"go north",
			   "s":"go south",
			   "e":"go east",
			   "w":"go west",
			   "ne":"go northeast",
			   "nw":"go northwest",
			   "sw":"go southwest",
			   "se":"go southeast",
			   "u":"go up",
			   "d":"go down"}
	
	keycuts={gtk.GDK.KP_0:"go up",
			 gtk.GDK.KP_1:"go southwest",
			 gtk.GDK.KP_2:"go south",
			 gtk.GDK.KP_3:"go southeast",
			 gtk.GDK.KP_4:"go west",
			 gtk.GDK.KP_5:"go down",
			 gtk.GDK.KP_6:"go east",
			 gtk.GDK.KP_7:"go northwest",
			 gtk.GDK.KP_8:"go north",
			 gtk.GDK.KP_9:"go northeast"}
	
	histpos=0

	def read_callback(self,*args):
		self.parse(self.recv_())
	
	def __init__(self,h,p,u,pw):
		RealityClient.__init__(self,h,p,u,pw,threaded=0)
		gtk.input_add(self.socket,
					  gtk.GDK.INPUT_READ,
					  self.read_callback)
		#print self.send_
		gtk.GtkWindow.__init__(self,gtk.WINDOW_TOPLEVEL)
		self.set_title("Reality Faucet")
		self.set_usize(640,480)
		
		self.namelabel=gtk.GtkLabel("NameLabel")

		self.descbox=gtk.GtkText()
		self.descbox.set_usize(370,255)
		self.descscrl=scrollify(self.descbox)
		defocusify(self.descbox)
		
		self.itembox=gtk.GtkText()
		self.itemscrl=scrollify(self.itembox)
		defocusify(self.itembox)
		
		self.happenings=gtk.GtkText()
		self.happscrl=scrollify(self.happenings)
		defocusify(self.happenings)
		self.cmdarea=gtk.GtkEntry()

		self.hpaned=gtk.GtkHPaned()
		self.hpaned.add1(self.descscrl)
		self.hpaned.add2(self.itemscrl)
		
		self.vpaned=gtk.GtkVPaned()
		self.vpaned.add1(self.hpaned)
		self.vpaned.add2(self.happscrl)

		self.vbox=gtk.GtkVBox()
		self.vbox.pack_start(self.namelabel, expand=0)
		
		self.vbox.add(self.vpaned)
		self.vbox.pack_start(self.cmdarea, expand=0)
		
		self.add(self.vbox)
		
		self.signal_connect('destroy',gtk.mainquit,None)
		
		self.cmdarea.connect("key_press_event", self.key_function)
		self.cmdarea.grab_focus()

		self.history = ['']
		self.descriptions={}
		self.items={}
		self.exits=[]
		
	def key_function(self, entry, event):
		possible_fill=self.keycuts.get(event.keyval)
		if possible_fill:
			self.cmdarea.set_sensitive(gtk.FALSE)
			self.cmdarea.set_editable(gtk.FALSE)
			self.sendVerb(possible_fill)
			self.clear_key()
		if len(entry.get_text()) == 0:
			if event.keyval == 39:
				entry.set_text("say \"")
				self.clear_key()
			elif event.keyval == 59:
				entry.set_text("emote \"")
				self.clear_key()
		if event.keyval == gtk.GDK.Return:
			self.sendText(entry)
		elif event.keyval == gtk.GDK.Tab:
			gtk.idle_add(self.focus_text)
		elif event.keyval in (gtk.GDK.KP_Up, gtk.GDK.Up):
			self.historyUp()
			gtk.idle_add(self.focus_text)
		elif event.keyval in (gtk.GDK.KP_Down, gtk.GDK.Down):
			self.historyDown()
			gtk.idle_add(self.focus_text)
		else: return
		self.clear_key()
		
	def historyUp(self):
		if self.histpos > 0:
			l = self.cmdarea.get_text()
			if len(l) > 0 and l[0] == '\n': l = l[1:]
			if len(l) > 0 and l[-1] == '\n': l = l[:-1]
			self.history[self.histpos] = l
			self.histpos = self.histpos - 1
			self.cmdarea.set_text(self.history[self.histpos])
			
	def historyDown(self):
		if self.histpos < len(self.history) - 1:
			l = self.cmdarea.get_text()
			if len(l) > 0 and l[0] == '\n': l = l[1:]
			if len(l) > 0 and l[-1] == '\n': l = l[:-1]
			self.history[self.histpos] = l
			self.histpos = self.histpos + 1
			self.cmdarea.set_text(self.history[self.histpos])

	def focus_text(self):
		self.cmdarea.grab_focus()
		return gtk.FALSE  # don't requeue this handler

	def script(self,filename):
		for i in open(filename).readlines():
			i=i[:-1]
			self.sendVerb(i)
	
	def sendText(self, entry):
		tosend=entry.get_text()
		if tosend[0]=='@':
			exec tosend[1:]
			return
		possible_shortcut=self.shortcuts.get(tosend)
		if possible_shortcut:
			tosend = possible_shortcut
			gtk.idle_add(self.focus_text)
		# Put this line into the History
		if len(tosend) > 0:
			self.histpos = len(self.history) - 1
			self.history[self.histpos] = tosend
			self.histpos = self.histpos + 1
			self.history.append('')
		# tosend should now be the "final" command sent to the server
		self.cmdarea.set_sensitive(gtk.FALSE)
		self.cmdarea.set_editable(gtk.FALSE)
		
		self.sendVerb(tosend)
		
	def event(self,phrase):
		self.lock()
		txt=self.happenings
		txt.set_point(txt.get_length())
		txt.freeze()
		txt.insert_defaults(phrase+"\n")
		adj=txt.get_vadjustment()
		txt.thaw()
		adj.set_value(adj.upper - adj.page_size)
		self.unlock()
		
	def name(self,*args):
		self.namelabel.set_text(string.join(args,' - '))

	def item_remove(self,key,parent):
		self.lock()
		try: del self.items[key]
		except: print 'tried to remove nonexistant item %s' % str(key)
		self.reitem()
		self.unlock()
		
	def items_clear(self):
		self.lock()
		self.items={}
		self.reitem()
		self.unlock()
	
	def item_add(self,key,parent,value):
		self.lock()
		self.items[key]=value
		self.reitem()
		self.unlock()
		
	def description_add(self,key,value):
		self.lock()
		self.descriptions[key]=value
		self.redesc()
		self.unlock()

	def description_remove(self,key):
		self.lock()
		del self.descriptions[key]
		self.redesc()
		self.unlock()

	def descriptions_clear(self):
		self.lock()
		self.descriptions={}
		self.redesc()
		self.unlock()

	def reexit(self):
		self.description_add('__EXITS__',"\nObvious Exits: %s"%string.join(self.exits,', '))
		
	def exit_add(self,exit):
		self.lock()
		self.exits.append(exit)
		self.reexit()
		self.unlock()

	def exit_remove(self,exit):
		self.lock()
		self.exits.remove(exit)
		self.reexit()
		self.unlock()

	def exits_clear(self):
		self.lock()
		self.exits=[]
		self.reexit()
		self.unlock()
		
	def reitem(self):
		txt=self.itembox
		txt.freeze()
		txt.delete_text(0,txt.get_length())
		txt.set_point(0)
		x=string.join(self.items.values(),'\n')
		txt.insert_defaults(x)
		txt.thaw()
		
	def theme(self,th):
		self.lock()
		try: gtktheme.theme(th)
		except: pass
		self.unlock()
		
	def redesc(self):
		txt=self.descbox
		txt.freeze()
		txt.delete_text(0,txt.get_length())
		txt.set_point(0)
		from copy import copy
		descs=copy(self.descriptions)
		try:
			del descs["__EXITS__"]
		except: pass
		try:
			del descs["__MAIN__"]
		except: pass
		mn=[self.descriptions.get('__MAIN__') or '']
		ex=[self.descriptions.get('__EXITS__') or '']
		x=string.join(mn+descs.values()+ex)
		txt.insert_defaults(x)
		txt.thaw()


	# none of this shit works at all... single-threaded is waaay
	# faster anyway, and we're reasonably sure about packet sizes...
	
	locklevel=0
	lockthread=None
	def lock(self):
		if not self.threaded: return
		if not self.locklevel or self.lockthread is not currentThread():
			print 'locking'
			gtk.threads_enter()
		if self.lockthread is None:
			self.lockthread=currentThread()
		self.locklevel=self.locklevel+1

	def unlock(self):
		if not self.threaded: return
		if self.locklevel==1 and self.lockthread is currentThread():
			print 'unlocking'
			gtk.threads_leave()
			del self.lockthread
			
		self.locklevel=self.locklevel-1
		
	def clear_key(self):
		self.cmdarea.emit_stop_by_name("key_press_event")

class LoginWindow(gtk.GtkWindow):
	def __init__(self):
		gtk.GtkWindow.__init__(self,gtk.WINDOW_TOPLEVEL)
		version_label=gtk.GtkLabel("GTK Faucet II 0.0.1\n"
								   "Protocol V3")
		version_label.show()
		self.character=gtk.GtkEntry()
		self.password=gtk.GtkEntry()
		self.hostname=gtk.GtkEntry()
		self.password.set_visibility(gtk.FALSE)

		self.character.set_text("Maxwell")
		self.password.set_text("kronor")
		self.hostname.set_text("localhost")

		charlbl=gtk.GtkLabel("Character Name:")
		passlbl=gtk.GtkLabel("Password:")
		hostlbl=gtk.GtkLabel("Hostname:")
		
		self.prgbar=gtk.GtkProgressBar()
		self.okbutton=gtk.GtkButton("OK")

		okbtnbx=gtk.GtkHButtonBox()
		okbtnbx.add(self.okbutton)
		
		vbox=gtk.GtkVBox()
		vbox.add(version_label)
		table=gtk.GtkTable(2,3)
		z=0
		for i in [[charlbl,self.character],
				  [passlbl,self.password],
				  [hostlbl,self.hostname]]:
			table.attach(i[0],0,1,z,z+1)
			table.attach(i[1],1,2,z,z+1)
			z=z+1

		vbox.add(table)
		vbox.add(self.prgbar)
		vbox.add(okbtnbx)
		self.add(vbox)

		self.okbutton.signal_connect('clicked',self.play)
		self.signal_connect('destroy',gtk.mainquit,None)
		
	def play(self,button):
		host=self.hostname.get_text()
		port=portno
		char=self.character.get_text()
		pswd=self.password.get_text()
		gw=GameWindow(host,port,char,pswd)
		
		
		self.hide()
		gw.show_all()

def debug_main_quit():
	"""Create a window with a button to call mainquit"""
        win = gtk.GtkWindow()
	win.set_title("Quit")
	win.set_usize(125, -1)
	b = gtk.GtkButton("Main Quit")
	b.connect("clicked", gtk.mainquit)
	win.add(b)
	b.show()
	win.show()

if __name__=='__main__':
	x=LoginWindow()
	x.show_all()
	#debug_main_quit()
	gtk.mainloop()
