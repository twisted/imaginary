
#include <glib.h>
#include <gtk/gtk.h>
#include "Python.h"

static PyObject*
gtk_theme_setup(self, args)
	 PyObject *self;
	 PyObject *args;
{
	char** newdefaults;
	
	newdefaults=g_new(char*,sizeof(char*)*2);

	newdefaults[0]="./themes/gtkrc";
	newdefaults[1]=NULL;
	gtk_rc_set_default_files(newdefaults);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyMethodDef NativeMethods[] = {
  {"setup", gtk_theme_setup, METH_VARARGS},
  {NULL, NULL}, /* Sentinel... what's this? */
};

void
init_gtktheme()
{
  (void) Py_InitModule("_gtktheme", NativeMethods);
}
