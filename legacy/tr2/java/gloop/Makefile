
all: stubs Naming.class Glip.class Glob.class Gloop.class Bolg.class BolgObject.class BolgMethod.class A.class B.class Test.class _A.class _B.class _Test.class B_.class

%.class: %.java
	export CLASSPATH=..; javac $*.java

stubs: _Test.java _A.java _B.java

_%.java:
	../../joopstub $*.java

clean:
	rm -f *.class *~ _*.java *.pyc
