

x=range(1000000)

from time import time
t=time()
x[0];x[1]
t1=time()-t
t=time()
x[0];x[999999]
t2=time()-t
print t1/t2
