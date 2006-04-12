"""
The Twisted Plumber
An Editor for Twisted Reality.
"""

# tried gtk, but frankly, gnome canvas sucks.

from Tkinter import *

# we're going to shamelessly assume that we are running within IDLE right
# now, in order to conserve code... this Scrolled Canvas code has GOT
# to be useful elsewhere though

from TreeWidget import ScrolledCanvas

# okay, really shameless here...
import PyShell

class Tool:
	name="ERROR"
	def __init__(self, bar, default=0):
		self.bar=bar
		self.plumber=bar.plumber
		self.default=default
		self.button=Button(bar.win,
						   text=self.name,
						   relief='flat')
		self.button.pack(side=TOP,fill='x')
		self.button.configure(command=self.command)

	def command(self):
		print 'no command defined'

class Select(Tool):
	name="Select"

class CreateExit(Tool):
	name="Create Exit"

class PlumBar:
	"""
	toolbar for Twisted Plumber!
	"""
	
	def __init__(self, plumber):
		self.plumber=plumber
		self.win=plumber.win
		
		Select(self,1)
		CreateExit(self)

class ScrolledList:
	def __init__(self,master, **opts):
		self.frame=Frame(master)
		self.frame.rowconfigure(0,weight=1)
		self.frame.columnconfigure(0,weight=1)
		self.box=apply(Listbox, (self.frame,), opts)
		self.box.grid(row=0,column=0,sticky="nsew")
		self.vbar=Scrollbar(self.frame, name='vbar')
		self.vbar.grid(row=0,column=1, sticky='nse')
		# hbar elided
		self.box['yscrollcommand']=self.vbar.set
		self.vbar['command']=self.box.yview

		self.box.bind("<Key-Prior>", self.page_up)
		self.box.bind("<Key-Next>", self.page_down)
		self.box.bind("<Key-Up>", self.unit_up)
		self.box.bind("<Key-Down>", self.unit_down)

	def addprop(self, name):
		f=Frame(self.box)
		l=Label(f,text=name)
		b=Entry(f,text=name)
		l.pack(); b.pack(); f.pack()
	
	def page_up(self, event):
		self.canvas.yview_scroll(-1, "page")
		return "break"
	def page_down(self, event):
		self.canvas.yview_scroll(1, "page")
		return "break"
	def unit_up(self, event):
		self.canvas.yview_scroll(-1, "unit")
		return "break"
	def unit_down(self, event):
		self.canvas.yview_scroll(1, "unit")
		return "break"
	def zoom_height(self, event):
		ZoomHeight.zoom_height(self.master)
		return "break"

def cadprop(sc, name):
	f=Frame(sc.canvas)
	l=Label(f,text=name)
	b=Entry(f,text=name)
	b.pack(side=LEFT,expand=YES,fill=BOTH);l.pack(side=LEFT);f.pack(expand=YES,fill=BOTH)

def sltest():
	t=Toplevel(PyShell.root)
	sl=ScrolledCanvas(t)
	cadprop(sl,'a')
	cadprop(sl,'b')
	cadprop(sl,'c')
	sl.frame.pack(expand=YES,fill='both')
	

class Plumber:
	def __init__(self):
		# create our window, and group it into the idle app
		self.win=Toplevel(PyShell.root)
		self.win.group(PyShell.root)
		self.scroll=ScrolledCanvas(self.win,
								   xscrollincrement=1,
								   yscrollincrement=1)
		self.scroll.frame.pack(side=RIGHT,expand=YES,fill='both')
		self.canvas=self.scroll.canvas
		self.toolbar=PlumBar(self)
