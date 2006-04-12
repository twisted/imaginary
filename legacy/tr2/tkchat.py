#!/usr/bin/env python

from Tkinter import *
from ScrolledText import *
from gloopchat import *

class TkChatClient(ChatClient):
	
	def chat(self, otheruser, words):
		self.window.xxx("%s: %s"%(otheruser,words))

class MainWindow(Toplevel):
	def __init__(self,echo,*args,**kw):
		apply(Toplevel.__init__,(self,)+args,kw)
		self.text=ScrolledText(self)
		self.text.pack(expand=YES)
		f=Frame(self)
		self.entry=Entry(f)
		self.bind("<Return>",self.blankxxx)
		self.button=Button(f,text="SEND!",command=self.blankxxx)
		self.entry.pack(side=LEFT,expand=YES,fill=BOTH)
		self.button.pack(side=LEFT)
		f.pack(expand=YES,fill=BOTH)
		self.send=echo
		self.protocol("WM_DELETE_WINDOW",self.close)

	def close(self):
		self.gc.send_logout()
		self.tk.quit()
		self.destroy()

	def xxx(self,text):
		self.text.insert('end',text+'\n')
		self.text.see('end')

	def blankxxx(self,*evornot):
		try:
			self.send(self.entry.get())
			self.entry.delete('0','end')
		except GloopException, ge:
			print ge.traceback

class Login(Toplevel):
	def __init__(self, *args,**kw):
		apply(Toplevel.__init__,(self,)+args,kw)
		f=Frame(self)
		l=Label(f,text='Username:')
		self.username=Entry(f)
		self.username.insert('0','guest')

		l.grid(column=0,row=0); self.username.grid(column=1,row=0)

		l=Label(f,text="Password: ")
		self.password=Entry(f,show="*")
		self.password.insert('0','guest')

		l.grid(column=0,row=1); self.password.grid(column=1,row=1)

		l=Label(f,text="Hostname: ")
		self.hostname=Entry(f)
		self.hostname.insert('0','localhost')

		l.grid(column=0,row=2); self.hostname.grid(column=1,row=2)

		l=Label(f,text="Port:")
		self.port=Entry(f)
		self.port.insert('0',str(portno))

		l.grid(column=0,row=3); self.port.grid(column=1,row=3)
		f.pack()

		self.go=Button(self,text="Allez!",command=self.go_go_gadget_login)
		self.go.pack()
		self.resizable(width=0,height=0)
		self.bind('<Return>',self.go_go_gadget_login)
		self.protocol("WM_DELETE_WINDOW",self.close)

	def close(self):
		self.destroy()
		self.tk.quit()

	def go_go_gadget_login(self, *args):
		username=self.username.get()
		hostname=self.hostname.get()
		port=int(self.port.get())
		password=self.password.get()
		
		gc=TkChatClient(hostname,port,username,password)
		
		m=MainWindow(gc['chat'],self.master)
		gc.window=m
		m.gc=gc
		self.withdraw()


if __name__=='__main__':
	root=Tk()
	root.withdraw()
	Login(root)
	mainloop()
