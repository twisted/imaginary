
# A few useful things to know about this Makefile:

# *: All classes will be compiled into $(CURDIR)/../javaclasses.  The
# runscripts that this makefile generates are not yet at all geared toward
# distribution -- they are intended to get a developer working with the code to
# be able to run them instantly.

# *: If you wish to define a class as an entrypoint, make a file called
# ClassName.main where ClassName.java is the name of the source file.  This
# will automatically generate runscripts.  The ClassName.main file may be empty.

# *: If you wish to create a new implementation of a remote object, make a file
# called ClassName.rmic, and it will be processed by $(RMIC) on the next
# compile.  You may have to 'make depclean' first to get this to work.

# *: If you experience a problem, check out Makefile.config.local first, and
# see if there are any variables you can customize.

include Makefile.config.local


all: $(BINDIR).d deps
	make -f Makefile.make world

javac.jar: deps
	mkdir jrt
	javac -classpath $(CLASSPATH) `find . -name "*.java"` -d jrt
	cd jrt; jar c0f ../javac.jar *
	rm -rf jrt

Makefile.config.local:
	cp Makefile.config Makefile.config.local

deps: Class.dep RMI.dep Main.dep

#classes which need to be made
Class.dep: 
	find . -name "*.java" | perl Dep.pl class >> Class.dep
#RMI classes which need to be RMIC'd
RMI.dep: Class.dep
	find . -name "*.rmic" | sed "s/\.rmic/.java/g" | perl Dep.pl rmi >> RMI.dep
#Classes which have a "Main" method that can be run.
Main.dep: Class.dep
	find . -name "*.main" | sed "s/\.main/.java/g" | perl Dep.pl main >> Main.dep

#This doesn't work.  Jikes doesn't appear to use GNU compatible 'make' syntax.
Jikes.dep: Class.dep
	jikes -classpath $(CLASSPATH) +F +M=Jikes_pre.dep -nowrite `find . -name "*.java"`
	perl -ne "if (/\.java/o) { print '\$$(BINDIR)/'; } print;" < Jikes_pre.dep > Jikes.dep
	$(RM) Jikes_pre.dep

depclean:
	$(RM) *.dep

clean:
	make -f Makefile.make cleanup
	make depclean

dist: deps
	make -f Makefile.make dist-make

dist-clean:
	make -f Makefile.make dist-clean-make



FQCN=`echo -n "$*" | sed "s/\//./g"`

%.rmi: %.java $(BINDIR)/%.class
	$(RMIC) -classpath $(CLASSPATH) -d $(BINDIR) $(FQCN)
	touch $(BINDIR)/$*.rmi

$(BINDIR)/%.class: $(BINDIR).d %.java
	$(COMPILE) $*.java

$(BINDIR)/%.main: %.java $(BINDIR)/%.class $(SCRIPTDIR).d
	echo "#!/bin/bash" > $(SCRIPTDIR)/$(FQCN)
	echo "$(JAVA_HOME)/bin/java -classpath $(CLASSPATH) $(FQCN) $$"* >> $(SCRIPTDIR)/$(FQCN)
	chmod a+x $(SCRIPTDIR)/$(FQCN)
	touch $(BINDIR)/$*.main

$(BINDIR)/%.class-clean: # $(BINDIR)/%.class
	$(RM) $(BINDIR)/$*.class
	$(RM) $(BINDIR)/$*\$$*.class

$(BINDIR)/%.rmi-clean:
	$(RM) $(BINDIR)/$*.rmi
	$(RM) $(BINDIR)/$*_Skel.class
	$(RM) $(BINDIR)/$*_Stub.class

$(BINDIR)/%.main-clean:
	$(RM) $(BINDIR)/$*.main
	rm -rf scripts

cleanup: class-clean rmi-clean main-clean dist-clean

%.d:
	if [ -d $* ]; then echo $@; touch $@; else mkdir $*; echo $@; touch $@; fi
