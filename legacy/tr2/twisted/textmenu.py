"""
Text Menu
"""

def menu(hash,banner="Menu",prompt="Enter your selection: "):
	while 1:
		clrscr()
		print banner
		for key,func in hash.items():
			print key, ' -- ', func.__doc__

		x=raw_input(prompt)
		try:
			x=hash[x]
		except: pass
		else:
			x()
			break

def menu_done():
	"go up one level in the menu system"

def clrscr():
	for i in range(24):
		print

def enterkey():
	raw_input("Press enter to continue.")

def input_int(prompt=""):
	while 1:
		try:
			return int(raw_input(prompt))
		except ValueError:
			pass

def input_float(prompt=""):
	while 1:
		try:
			return float(raw_input(prompt))
		except ValueError:
			pass

def seqmenu(seq, banner="", prompt="Choose one: "):
	while 1:
		clrscr()
		print banner
		for x in range(len(seq)):
			print x, ':', seq[x]

		x=raw_input(prompt)
		try:
			return seq[int(x)]
		except: pass
		
