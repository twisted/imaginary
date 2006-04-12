#ifdef HAVE_CONFIG_H
#  include <config.h>
#endif

#include <gnome.h>

#include "callbacks.h"
#include "interface.h"
#include "support.h"
#include "history.h"
#include "faucet.h"

GtkWidget* loginwindow;
GtkWidget* gamewindow;
/* themewindow & compasswindow are gone */

gboolean
on_CommandPanel_key_press_event        (GtkWidget       *widget,
                                        GdkEventKey     *event,
                                        gpointer         user_data)
{
  return history_keypress(widget,event);
}


void
on_CommandPanel_activate               (GtkEditable     *editable,
                                        gpointer         user_data)
{
  char* userverb;
  userverb = gtk_entry_get_text(GTK_ENTRY(editable));
  faucet_verb_send(userverb);
  gtk_entry_set_text(GTK_ENTRY(editable),"");
}


void
on_charname_entry_activate             (GtkEditable     *editable,
                                        gpointer         user_data)
{
  	GtkWidget* wdgt;
	wdgt=lookup_widget(GTK_WIDGET(editable),"pw_entry");
	gtk_widget_grab_focus(wdgt);
}


void
on_pw_entry_activate                   (GtkEditable     *editable,
                                        gpointer         user_data)
{
  on_engageButton_clicked(GTK_BUTTON(lookup_widget(GTK_WIDGET(editable),"engageButton")),NULL);
}


void
on_engageButton_clicked                (GtkButton       *button,
                                        gpointer         user_data)
{
  GtkWidget* loginent;
  GtkWidget* passent;
  GtkWidget* hostent;
  
  loginent=lookup_widget(GTK_WIDGET(button),"charname_entry");
  passent=lookup_widget(GTK_WIDGET(button),"pw_entry");
  hostent=lookup_widget(GTK_WIDGET(button),"hostname_entry");
  if (loginent && passent && hostent)
	{
	  faucet_login
		(gtk_entry_get_text(GTK_ENTRY(loginent)),
		 gtk_entry_get_text(GTK_ENTRY(passent)),
		 gtk_entry_get_text(GTK_ENTRY(hostent)));
	  /*gtk_widget_show(compasswindow);*/
	}
  else
	{
	  g_print("bail!\n");
	}
}


void
on_answerdialog_ok_clicked             (GtkButton       *button,
                                        gpointer         user_data)
{
  gtk_widget_destroy(lookup_widget(GTK_WIDGET(button),"answerdialog"));
}


void
on_ok_button_clicked                   (GtkButton       *button,
                                        gpointer         user_data)
{
  char* key;
  char* val;
  GtkWidget* tarea;
  
  tarea = GTK_WIDGET(lookup_widget(GTK_WIDGET(button),"descriptive_text"));
  
  val=gtk_editable_get_chars
	(GTK_EDITABLE(tarea),
	 0,
	 gtk_text_get_length(GTK_TEXT(tarea))
	 );
  key=(char*) gtk_object_get_data(GTK_OBJECT(lookup_widget(tarea,"responsewindow")),"timekey");
  faucet_got_response(key,val);
  gtk_widget_destroy(lookup_widget(GTK_WIDGET(button),"responsewindow"));
}


void
on_notok_button_clicked                (GtkButton       *button,
                                        gpointer         user_data)
{
  gtk_widget_destroy(lookup_widget(GTK_WIDGET(button),"responsewindow"));
}


gboolean
on_gamewindow_delete_event             (GtkWidget       *widget,
                                        GdkEvent        *event,
                                        gpointer         user_data)
{
  faucet_logout();
  return TRUE;
}


gboolean
on_loginwindow_delete_event            (GtkWidget       *widget,
                                        GdkEvent        *event,
                                        gpointer         user_data)
{
  /* ho hum, ho hum... I don't think this really needs to be trapped */
  return FALSE;
}


gboolean
on_loginwindow_destroy_event           (GtkWidget       *widget,
                                        GdkEvent        *event,
                                        gpointer         user_data)
{
  /* nor this, but whatever... */
  return FALSE;
}


void
on_loginwindow_destroy                 (GtkObject       *object,
                                        gpointer         user_data)
{
  gtk_main_quit();
}
