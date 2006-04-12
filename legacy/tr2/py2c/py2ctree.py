import genc, sys, os, os.path

py_dir=sys.argv[1]
c_dir=sys.argv[2]

def mkcfile(pyfile):
	genc.Generator(pfilename+".py",
				   "_"+pfilename+".c",
				   "/dev/null")

def mkdirs(dir_tup,d,files):
	pytup=[]
	for i in files:
		if i[-3:]=='.py':
			pytup.append(i)
	existing=dir_tup[0]
	new=dir_tup[1]
	o=d[len(existing):]
	z="%s/%s"%(new,o)

	if not os.path.isdir(new):
		os.mkdir(new)

	print d
	print z
	
	if not os.path.isdir(z):
		print '!!'
		print z
		os.mkdir(z)
		
	for i in pytup:
		b=z+i[:-3]+'.c'
		# byp=z+"/"+i
		byp='/dev/null'
		q=d+"/"+i
		sys.stdout.write( "  %s -> "%q )
		sys.stdout.flush()
		reload(genc)
		genc.Generator(q,b,byp)
		sys.stdout.write('.c -> ')
		sys.stdout.flush()
		mdl=b[:-2]+'module.so'
		cmd='gcc -w --shared -I/usr/include/python1.5 %s -o %s' % (b,mdl)
		# print '\t%s'%cmd
		
		x=os.system(cmd)
		sys.stdout.write('.so')
		sys.stdout.write('\n')
		if x != 0:
			print '\n\n\t*** FAILED ***'
	
os.path.walk(py_dir,mkdirs,(py_dir,c_dir))
