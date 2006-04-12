
import os

try:
	os.stat('./themes/default')
except:
	raise ImportError("You don't have a themes directory.")

import random

try:
	os.stat('_gtkthememodule.so')
except:
	os.system("cc --shared `gtk-config --cflags` `gtk-config --libs` -I/usr/include/python1.5 _gtktheme.c -o _gtkthememodule.so")

	
import _gtktheme
_gtktheme.setup()

MARK_STRING="# -- NOT AUTO THEME-DO WRITTEN EDIT\n"
parse_rc_file="./themes/gtkrc"
current_theme=""
widgets=[]

exec('import '+__name__+'; _='+__name__)

def register(widget):
	widgets.append(widget)

def theme(to):
	if current_theme==to:
		return
	theme_rc_file="./themes/%s/gtkrc" % to
	try:
		os.stat(theme_rc_file)
	except OSError:
		theme('default')
		return
	os.unlink(parse_rc_file)
	out=open(parse_rc_file,'w')
	out.write(MARK_STRING)
	out.write('include "%s"\n\n'%theme_rc_file)
	out.close()
	gtk.rc_reparse_all()
	for w in widgets:
		w.reset_rc_styles()
		# w.ensure_style()
	_.current_theme=to

# this is a "hot fix" for a bug in pygtk -- there is a misspelling (I
# guess the RC code was not terribly well-tested :-P

import gtk
gtk._gtk.gtk_rc_repase_all=gtk._gtk.gtk_rc_reparse_all

theme('default')

if __name__=='__main__':
	from gtk import *
	wn=GtkWindow(WINDOW_TOPLEVEL)
	bt=GtkButton("Set Theme")
	en=GtkEntry()
	bb=GtkHBox()
	bb.add(bt); bb.add(en); wn.add(bb)
	def clk(bt,en=en,wn=wn):
		theme(en.get_text())
	bt.signal_connect('clicked',clk)
	wn.signal_connect('destroy',mainquit)
	_.register(wn)
	wn.show_all()
	mainloop()
		
