
# Twisted, the Framework of Your Internet
# Copyright (C) 2001 Matthew W. Lefkowitz
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of version 2.1 of the GNU Lesser General Public
# License as published by the Free Software Foundation.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import string
import copy

from Tkinter import *
from ScrolledText import *

from twisted.spread import pb
from twisted.internet import tksupport

class MainWindow(Toplevel, pb.Referenceable):

    shortcuts = {"n":"go north",
                 "s":"go south",
                 "e":"go east",
                 "w":"go west",
                 "l":"look",
                 "ne":"go northeast",
                 "nw":"go northwest",
                 "sw":"go southwest",
                 "se":"go southeast",
                 "u":"go up",
                 "d":"go down"}
    
    def __init__(self, *args,**kw):
        self.descriptions = {}
        self.items = {}
        self.exits = []
        apply(Toplevel.__init__,(self,)+args,kw)
        self.title("Reality Faucet")
        self.happenings = ScrolledText(self, height=6, width=72, wrap='word')
        
        midf = Frame(self)
        ddf = Frame(midf)
        idf = Frame(midf)
        
        a = self.descriptionField = ScrolledText(ddf, height=12, width=72, wrap='word')
        b = self.itemsField = ScrolledText(idf, height=12, width=36, wrap='word')

        a.pack(fill=BOTH, expand=YES)
        b.pack(fill=BOTH, expand=YES)
        ddf.pack(side=LEFT, fill=BOTH, expand=YES)
        idf.pack(side=LEFT, fill=BOTH, expand=NO)
        
        f=Frame(self)
        self.entry=Entry(f)
        self.bind("<Return>",self.doSend)
        # self.bind("<KP-1>", self.doSend)
        self.button=Button(f,text=".",command=self.doSend)
        self.entry.pack(side=LEFT,expand=YES,fill=BOTH)
        self.button.pack(side=LEFT)

        self.nameLabel = Label(self, text="hellO")
        
        f.pack(side=BOTTOM, expand=NO, fill='x')
        self.happenings.pack(side=BOTTOM, expand=YES, fill=BOTH)
        midf.pack(side=BOTTOM, expand=YES, fill=BOTH)
        self.nameLabel.pack(side=TOP, expand=NO)
        
        self.protocol("WM_DELETE_WINDOW",self.close)

    def close(self):
        self.tk.quit()
        self.destroy()

    def connected(self, rem):
        print 'connected'
        rem.broker.notifyOnDisconnect(self.connectionLost)
        self.remote = rem
        self.deiconify()
        login.withdraw()

    def connectionLost(self):
        self.withdraw()
        login.deiconify()
        login.loginReport("Disconnected from Server.")

    def verbSuccess(self, nne):
        self.verbDone()

    def verbFailure(self, nne):
        if hasattr(nne, 'traceback'):
            self.seeEvent(nne.traceback)
        self.seeEvent(nne)
        self.verbDone()

    def verbDone(self):
        # unlock the text field
        pass 

    def doNow(self, verb):
        self.remote.callRemote("execute", verb).addCallbacks(self.verbSuccess, self.verbFailure)

    def remote_seeEvent(self,text):
        self.happenings.insert('end',text+'\n')
        self.happenings.see('end')

    def reitem(self):
        self.itemsField.delete('1.0','end')
        self.itemsField.insert('end', string.join(self.items.values(), '\n'))

    def redesc(self):
        z = copy.copy(self.descriptions)
        m = z.get('__MAIN__','')
        e = z.get('__EXITS__','')

        try: del z['__MAIN__']
        except: pass
        try: del z['__EXITS__']
        except: pass
        
        self.descriptionField.delete(1.0,'end')
        self.descriptionField.insert('end', string.join([m]+z.values()+[e]))

    def remote_seeName(self, name):
        self.nameLabel.configure(text=name)

    def remote_dontSeeItem(self, key,parent):
        try:
            del self.items[key]
        except:
            print 'tried to remove nonexistant item %s' % str(key)
        self.reitem()
    
    def doSend(self, *evstuf):
        sentence = self.entry.get()
        possible_shortcut = self.shortcuts.get(sentence)
        if possible_shortcut:
            sentence = possible_shortcut
        self.doNow(sentence)
        self.entry.delete('0','end')

    def remote_dontSeeItem(self,key,parent):
        try: del self.items[key]
        except: print 'tried to remove nonexistant item %s' % str(key)
        self.reitem()
        
    def remote_seeNoItems(self):
        self.items = {}
        self.reitem()
    
    def remote_seeItem(self,key,parent,value):
        self.items[key] = value
        self.reitem()
        
    def remote_seeDescription(self,key,value):
        self.descriptions[key] = value
        self.redesc()

    def remote_dontSeeDescription(self,key):
        del self.descriptions[key]
        self.redesc()

    def remote_seeNoDescriptions(self):
        self.descriptions = {}
        self.redesc()

    def reexit(self):
        self.remote_seeDescription('__EXITS__',"\nObvious Exits: %s"%string.join(self.exits,', '))
        
    def remote_seeExit(self,exit):
        self.exits.append(exit)
        self.reexit()

    def remote_dontSeeExit(self,exit):
        self.exits.remove(exit)
        self.reexit()

    def remote_seeNoExits(self):
        self.exits = []
        self.reexit()



def main():
    global root
    global login
    root = Tk()
    root.withdraw()
    tksupport.install(root)
    print 'displaying login'
    from twisted.spread.ui import tkutil
    m = MainWindow()
    m.withdraw()
    login = tkutil.Login(m.connected,m)
    mainloop()

