#!/usr/bin/env python

from string import replace


sys.stdout=ThreadAttr(
	{t1:LogFile(sys.stdout,prefix="T1 - "),
	 t2:LogFile(sys.stdout,prefix="T2 - "),
	 tm:sys.stdout}
	)


print 'hello',
print 'goodbye'
t1.start()
t2.start()

print 'boop'
print 'boop'
