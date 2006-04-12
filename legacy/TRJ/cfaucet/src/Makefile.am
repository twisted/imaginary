## Process this file with automake to produce Makefile.in

INCLUDES = \
	-I$(top_srcdir)/intl \
	$(GNOME_INCLUDEDIR)

bin_PROGRAMS = gtkfaucet

gtkfaucet_SOURCES = \
	main.c \
	support.c support.h \
	interface.c interface.h \
	callbacks.c callbacks.h \
	faucet.c faucet.h \
	reality_stream.c reality_stream.h \
	fileutils.c fileutils.h \
	sockhelp.c sockhelp.h \
	history.c history.h



gtkfaucet_LDADD = $(GNOME_LIBDIR) $(GNOMEUI_LIBS) $(INTLLIBS)

