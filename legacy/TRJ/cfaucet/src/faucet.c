#include <glib.h>
#include <gtk/gtk.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

#include "interface.h"
#include "faucet.h"
#include "fileutils.h"
#include "reality_stream.h"
#include "callbacks.h"
#include "sockhelp.h"
#include "history.h"
#include "support.h"

gchar mytheme[128];
gchar mytheme2[128];

int faucet_fd;

#define CMD_Hears 1
#define CMD_SetName 2
#define CMD_SetPict 3
#define CMD_SetTheme 4
#define CMD_RequestResponse 5
#define CMD_ReturnResponse 5
#define CMD_CompletedAction 6
#define CMD_Quit 7
#define CMD_Exits 8
#define CMD_DisplayErrorDialog 9
#define CMD_Ping 10
#define CMD_Pong 11

#define CMD_DescClear 100
#define CMD_DescAppend 101
#define CMD_DescRemove 102

#define CMD_ListClear 110
#define CMD_ListAdd 111
#define CMD_ListRemove 112
#define CMD_ListEnter 113
#define CMD_ListLeave 114

#define CMD_CXStart 120
#define CMD_CXData 121
#define CMD_CXSupported 123

#define TYPE_None 0
#define TYPE_String 1
#define TYPE_RawData 2

/*define __BROKEN_PINGS__*/

/* initialization */
int faucet_inited;

void
faucet_answer(gchar* string)
{
	GtkWidget* mydlg;
	GtkText* mytxt;
	mydlg=create_answerdialog();
	mytxt=GTK_TEXT(lookup_widget(mydlg,"tarea"));
	gtk_text_set_word_wrap(mytxt,TRUE);
	gtk_text_insert(mytxt,
					NULL,
					NULL,
					NULL,
					string,
					strlen(string));
	gtk_widget_show(mydlg);
}

void
faucet_free(gpointer foo)
{
	g_free(foo);
}

GHashTable* faucet_shortcuts;

void
faucet_init()
{
	faucet_inited=0;
	
	faucet_descriptors=g_hash_table_new(g_str_hash,
										g_str_equal);
	
	faucet_things=g_hash_table_new(g_str_hash,
								   g_str_equal);
	
	faucet_shortcuts=g_hash_table_new(g_str_hash,
									  g_str_equal);
	
	g_hash_table_insert(faucet_shortcuts,"n","go north");
	g_hash_table_insert(faucet_shortcuts,"e","go east");
	g_hash_table_insert(faucet_shortcuts,"s","go south");
	g_hash_table_insert(faucet_shortcuts,"w","go west");
	g_hash_table_insert(faucet_shortcuts,"ne","go northeast");
	g_hash_table_insert(faucet_shortcuts,"nw","go northwest");
	g_hash_table_insert(faucet_shortcuts,"l","look");
	g_hash_table_insert(faucet_shortcuts,"d","go down");
	g_hash_table_insert(faucet_shortcuts,"u","go up");
	g_hash_table_insert(faucet_shortcuts,"se","go southeast");
	g_hash_table_insert(faucet_shortcuts,"sw","go southwest");
	g_hash_table_insert(faucet_shortcuts,"i","inventory");
	
	faucet_gtk_theme_setup();
	
	faucet_inited=1;
	ignore_pipe();
}

int faucet_fd_rm=0;
float current_progress=0.0;
float increment=1./14.;
void
faucet_make_progress()
{
	GtkProgressBar* prog;
	current_progress=current_progress+increment;
	prog=GTK_PROGRESS_BAR(lookup_widget(loginwindow,"login_progress"));
	gtk_progress_bar_update(prog,current_progress);
	
	while (gtk_events_pending())
		gtk_main_iteration();
	
	/* Why do I need these? */
	usleep(10);
	while (gtk_events_pending())
		gtk_main_iteration();
}

void 
faucet_reset_progress()
{
	GtkProgressBar* prog;
	prog=GTK_PROGRESS_BAR(lookup_widget(loginwindow,"login_progress"));
	gtk_progress_bar_update(prog,current_progress=0.0);
	while (gtk_events_pending())
		gtk_main_iteration();
	
	/* Why do I need these? */
	usleep(10);
	while (gtk_events_pending())
		gtk_main_iteration();
}

int dontclick=0;
void
faucet_login(const char* login,
			 const char* password,
			 const char* hostname)
{
	if (dontclick) return;
	dontclick=1;
	// 1
	faucet_make_progress();
	faucet_fd=rstream_open(hostname);
	// 2
	faucet_make_progress();
	if(faucet_fd > 0)
	{
		char* loginline;
		int loginnum;
		// 3
		faucet_make_progress();
		loginline=rstream_read_utf(faucet_fd);
		// 4
		faucet_make_progress();
		// 5
		faucet_free(loginline);
		// 6
		faucet_make_progress();
		/** VERSION **/
		
		rstream_write_short(faucet_fd,3);
		// 7
		faucet_make_progress();
		loginnum=rstream_read_short(faucet_fd);
		// 8
		faucet_make_progress();
		loginline=rstream_read_utf(faucet_fd);
		// 9
		faucet_make_progress();
		faucet_free (loginline);
		// 10
		faucet_make_progress();
		rstream_write_utf(faucet_fd,login);
		// 11
		faucet_make_progress();
		rstream_write_utf(faucet_fd,password);
		// 12
		faucet_make_progress();
		loginline=rstream_read_utf(faucet_fd);
		// 13
		faucet_make_progress();
		if (strcmp(loginline,"CONNECTED"))
		{
			faucet_answer("Bad User And/Or Password:\nIf you're sure you entered it correctly, please contact a system administrator (tenth@twistedmatrix.com) or file a bug report (glyph@twistedmatrix.com)");
			goto done;
		}
		faucet_free(loginline);
		// 14
		faucet_make_progress();
		/* Okay, I'm connected! */
		{
		  GtkText* desc;
		  int textlen;
		  
		  desc=GTK_TEXT(lookup_widget(gamewindow,"happenings_field"));
		  gtk_text_freeze(GTK_TEXT(desc));
		  gtk_text_set_word_wrap(GTK_TEXT(desc),TRUE);
		  textlen=gtk_text_get_length(GTK_TEXT(desc));
		  gtk_editable_delete_text(GTK_EDITABLE(desc),0,textlen);
		  gtk_text_set_point(GTK_TEXT(desc),0);
		  gtk_text_thaw(GTK_TEXT(desc));
		}
		gtk_widget_hide(loginwindow);
		gtk_widget_show(gamewindow);
		
		faucet_fd_rm=gdk_input_add(faucet_fd,GDK_INPUT_READ,faucet_data_in,NULL);
		/*rstream_close(faucet_fd);*/
	}
	else
	{
		faucet_answer("Couldn't establish TCP/IP connection.");
	}
 done:
	dontclick=0;
	faucet_reset_progress();
}

gint
faucet_recieve(gint mfaucet,GArray** resultaddr, int* mint)
{
	gint command;
	gint parts;
	GArray* result;
	gint i;
	result = g_array_new(FALSE,TRUE,sizeof(char*));
	
	*resultaddr = result;
	
	command = rstream_read_short(mfaucet);
	parts = (gint) rstream_read_byte(mfaucet);
	*mint=parts;
	for(i = 0; i < parts; i++)
	{
		char type;
		char* data;
		type = rstream_read_byte(mfaucet);

		switch(type)
		{
		case TYPE_RawData:
		case TYPE_String:
			data=rstream_read_utf(mfaucet);
			g_array_append_val(result,data);
			break;
		case TYPE_None:
			data=NULL;
			g_array_append_val(result,data);
			break;
		default:
		}
	}
	return command;
}

void
faucet_data_in(gpointer data,
			   gint mfaucet,
			   GdkInputCondition cond)
{
	GArray* arg;
	int arglen;
	/*	int i;*/
	int command;
	command = faucet_recieve(mfaucet, &arg, &arglen);
	
	switch(command)
	{
	case CMD_Hears:
		faucet_hears(g_array_index(arg,char*,0));
		break;
	case CMD_DisplayErrorDialog:
		faucet_answer(g_array_index(arg,char*,0));
		break;
	case CMD_SetName:
		faucet_name(arg,arglen);
		break;
	case CMD_SetPict:
		g_print("CMD_SetPict - I cannot be killed!\nWhy is this even in the protocol?\n");
		break;
	case CMD_DescAppend:
		faucet_add_descriptor(g_array_index(arg,char*,0),
							  g_array_index(arg,char*,1));
		break;
	case CMD_DescRemove:
		faucet_remove_descriptor(g_array_index(arg,char*,0));
		break;
	case CMD_DescClear:
		faucet_clear_descriptors();
		break;
	case CMD_ListClear:
		faucet_clear_things();
		break;
	case CMD_ListAdd:
		faucet_add_thing(g_array_index(arg,char*,0),
						 g_array_index(arg,char*,2));
		break;
	case CMD_ListLeave:
		faucet_leave_thing(g_array_index(arg,char*,0),
						   g_array_index(arg,char*,2));
		break;
	case CMD_ListEnter:
		faucet_enter_thing(g_array_index(arg,char*,0),
						   g_array_index(arg,char*,2));
		break;
	case CMD_ListRemove:
		faucet_remove_thing(g_array_index(arg,char*,0));
		break;
	case CMD_CompletedAction:
		faucet_completed_action();
		break;
		/* heeehee... non thread safe operations can go to hell (in
           the Java version here is where we have code to handle
           thread-non-safeness) */
	case CMD_RequestResponse:
		faucet_request_response(g_array_index(arg,char*,0),
								g_array_index(arg,char*,1),
								g_array_index(arg,char*,2));
		break;
	case CMD_Exits:
		faucet_exits(arg,arglen);
		break;
	case CMD_SetTheme:
		faucet_set_theme(g_array_index(arg,char*,0));
		break;
	case CMD_Ping:
		/* sometimes we want to turn this off for bugtesting broken
           connections */
#ifndef __BROKEN_PINGS__
		faucet_send(CMD_Pong,arg);
#endif
		break;
	case CMD_Quit:
		faucet_logout();
	}
	g_array_free(arg,TRUE);
}

void
faucet_response_send(char* key,char* response)
{
	GArray* atemp;
	atemp=g_array_new(FALSE,TRUE,sizeof(char*));
	g_array_append_val(atemp,key);
	g_array_append_val(atemp,response);
	faucet_send(CMD_ReturnResponse,atemp);
	g_array_free(atemp,TRUE);
}

void
faucet_verb_send(char* cmd)
{
	GtkWidget* editable;
	GArray* atemp;
	char* cmd2;
	char hrbf[2048];
	
	hrbf[0]='\0';
	strcat(hrbf,"$ ");
	cmd2=cmd;
	if (!cmd || !(cmd[0])) return;
	atemp=g_array_new(FALSE,TRUE,sizeof(char*));
	if( (cmd2=g_hash_table_lookup(faucet_shortcuts,cmd)))
	{
		g_array_append_val(atemp,cmd2);
		history_add(cmd2);
		strcat(hrbf,cmd2);
	}
	else
	{
		g_array_append_val(atemp,cmd);
		history_add(cmd);
		strcat(hrbf,cmd);
	}
	editable=lookup_widget(gamewindow,"CommandPanel");
	gtk_entry_set_editable(GTK_ENTRY(editable),FALSE);
	gtk_widget_set_sensitive(editable,FALSE);
	
	faucet_hears(hrbf);
	faucet_send(CMD_Hears,atemp);
	g_array_free(atemp,TRUE);

}

void
faucet_send(gint command,GArray* arry)
{
	int i;
	rstream_write_short(faucet_fd,command);
	rstream_write_byte(faucet_fd,(char)arry->len);
	for(i=0;i<arry->len;i++)
	{
		rstream_write_byte(faucet_fd,TYPE_String);
		rstream_write_utf(faucet_fd,g_array_index(arry,char*,i));
	}
}

/*
 * Themes!
 */

#define MARK_STRING "# -- THEME AUTO-WRITTEN DO NOT EDIT\n"
static void
print_standard_stuff(FILE *fout, gchar *theme)
{
	fprintf(fout, MARK_STRING);
	fprintf(fout, "include \"%s\"\n\n", theme);
	/*fprintf(fout, "include \"~/.gtkrc.mine\"\n\n");*/
	fprintf(fout, MARK_STRING);
}

void
edit_file_to_use(gchar *file, gchar *theme)
{
	FILE *fout;
	gchar tmp[4096];
	
	srand(time(NULL));
	g_snprintf(tmp, sizeof(tmp), "/tmp/gtkrc_%i", rand());
	fout = fopen(tmp, "w");
	if (!fout)
		return;
	rm(file);
	print_standard_stuff (fout, theme);
	fclose(fout);
	cp(tmp, file);
	rm(tmp);
}

gboolean
faucet_retheme(GtkWidget* toSwitch)
{
	if(gtk_rc_reparse_all())
	{
		gtk_widget_reset_rc_styles(toSwitch);
		gtk_widget_ensure_style(toSwitch);
		return TRUE;
	}
	else
	{
		return FALSE;
	}
	
}
#define tofile "./themes/gtkrc"
void
faucet_set_theme(const char* themename)
{
  /* ok, better name for this would have been "theme_rc_file" but I
     didn't know what I was doing at the time... */

	char fromfile[128];

	/*g_print("theme: %s (orig: %s)\n",themename,mytheme2);*/
	if(strcmp(themename,mytheme2))
	{
		/*g_print("\tactually theming.\n");*/
		fromfile[0]='\0';

		strcat (fromfile,"./themes/");
		strcat (fromfile,themename);
		strcat (fromfile,"/gtkrc");
		
		if(exists(fromfile))
		{
			edit_file_to_use(tofile,fromfile);
		}
		else
		{
			faucet_set_theme("default");
			return;
		}
		if(faucet_inited)
		{
		  faucet_retheme(gamewindow);
		  /*
			if (!faucet_retheme(gamewindow))
			{
				g_print("x");
				while(!faucet_retheme(gamewindow))
				{
					usleep(250000);
					edit_file_to_use(tofile,fromfile);
					g_print(".");
				}
				g_print("!\n");
			}
		  */
		}
		mytheme2[0]='\0';
		strcat(mytheme2,themename);
	}
}
void
faucet_gtk_theme_setup()
{
	char** newdefaults;
	
	newdefaults=g_new(char*,sizeof(char*)*2);

	mytheme[0]='\0';
	/* strcat(mytheme,cwd());*/
	strcat(mytheme,"./themes/gtkrc");
	newdefaults[0]=mytheme;
	newdefaults[1]=NULL;
	gtk_rc_set_default_files(newdefaults);
	faucet_set_theme("default");
}

/* descriptors */

GHashTable* faucet_descriptors;

char* faucet__main__;
char* faucet__exits__;

void
faucet_internal_thing_add(gpointer key,
						  gpointer value,
						  gpointer foo)
{
	GtkText* wdgt;
	char* thegc;
	
	wdgt= (GtkText*) foo;
	/*ignore key*/
	if(value)
	{
		thegc=g_new(char,sizeof(char)* (2+strlen( (char*) key)));
		thegc[0]=0;
		strcat(thegc,"+");
		strcat(thegc,(char*)key);
		if(!g_hash_table_lookup(faucet_things,thegc))
		{
			if(wdgt)
			{
				gtk_text_insert(wdgt,
								NULL,
								NULL,
								NULL,
								(char*)value,
								strlen((char*) value));
				gtk_text_insert(wdgt,NULL,NULL,NULL,"\n",1);
			}
		}
		faucet_free(thegc);
	}
	else
	{
		g_print("Yip!\n");
	}
	
}

void
faucet_internal_desc_add(gpointer key,
						 gpointer value,
						 gpointer foo)
{
	GtkText* wdgt;
	wdgt= (GtkText*) foo;
	if(value)
	{
		
		gtk_text_insert(wdgt,
						NULL,
						NULL,
						NULL,
						(char*)value,
						strlen((char*) value));
		gtk_text_insert(wdgt,NULL,NULL,NULL," ",1);
	}
}


void
faucet_redesc()
{
	GtkWidget* desc;
	int textlen;
	
	desc=lookup_widget(gamewindow,"description_field");
	
	gtk_text_freeze(GTK_TEXT(desc));
	gtk_text_set_word_wrap(GTK_TEXT(desc),TRUE);
	textlen=gtk_text_get_length(GTK_TEXT(desc));
	gtk_editable_delete_text(GTK_EDITABLE(desc),0,textlen);
	gtk_text_set_point(GTK_TEXT(desc),0);
	faucet_internal_desc_add("__MAIN__",faucet__main__,GTK_TEXT(desc));
	g_hash_table_foreach(faucet_descriptors,
						 faucet_internal_desc_add,
						 (gpointer)GTK_TEXT(desc));
	faucet_internal_desc_add("__EXITS_KLUDGE",faucet__exits__,GTK_TEXT(desc));
	gtk_text_thaw(GTK_TEXT(desc));
}

void
faucet_add_descriptor(char* key,
					  char* value)
{
	if(!strcmp(key,"__MAIN__"))
	{
		faucet__main__=value;
	}
	else if (!strcmp(key,"__EXITS_KLUDGE__"))
	{
		faucet__exits__=value;
	}
	else
	{
		g_hash_table_insert(faucet_descriptors,key,value);
	}
	faucet_redesc();
}

void
faucet_remove_descriptor(char* key)
{
	g_hash_table_remove(faucet_descriptors,key);
	faucet_redesc();
}

void
faucet_clear_descriptors()
{
	g_hash_table_foreach_remove(faucet_descriptors,
								faucet_keyval_cleanup,NULL);
	g_hash_table_destroy(faucet_descriptors);
	faucet_descriptors=g_hash_table_new(g_str_hash,g_str_equal);
	faucet_redesc();
}

gboolean
faucet_keyval_cleanup(gpointer a,
					  gpointer b,
					  gpointer user_data)
{
	faucet_free(a);
	faucet_free(b);
	return TRUE;
}


static void fix_text(GtkWidget *text)
{
	float f;
	
	do
	{
		gtk_main_iteration();
	}
	while(gtk_events_pending());
	f = GTK_TEXT(text)->vadj->upper;
	f = f - text->allocation.height;
	
	if (f < 0)
		f=0;
	/* Special case */
	else if (text->allocation.height == 1) f = 0;
	
	gtk_adjustment_set_value(GTK_TEXT(text)->vadj, f);
}

/* your "hearing" */

void
faucet_hears(char* toHear)
{
	GtkWidget* happ;
	/*g_print("hears: %s\n",toHear);*/
	happ = lookup_widget(GTK_WIDGET(gamewindow),"happenings_field");
	gtk_text_set_word_wrap(GTK_TEXT(happ),TRUE);
	if (happ != NULL)
	{
		
		gtk_text_set_point(GTK_TEXT(happ),
						   gtk_text_get_length(GTK_TEXT(happ)));
		gtk_text_freeze(GTK_TEXT(happ));
		gtk_text_insert(GTK_TEXT(happ),
						/*GTK_WIDGET(happ)->style->font,*/
						NULL,
						/*& GTK_WIDGET(happ)->style->black,*/
						NULL,
						NULL,
						toHear,
						strlen(toHear));
		gtk_text_insert(GTK_TEXT(happ),
						NULL,NULL,NULL,"\n",1);
		gtk_text_thaw(GTK_TEXT(happ));
		fix_text(happ);
	}
}

void
faucet_name(GArray* gary, int garylen)
{
	gchar foo[1024];
	int i;
	
	foo[0]='\0';
	
	for (i=(garylen-1);i>=0;i--)
	{
		strcat(foo,g_array_index(gary,char*,i));
		if (i>0)
			strcat(foo, " : ");
	}
	
	/*g_print("name: %s\n",mname);*/
	gtk_label_set_text(GTK_LABEL(lookup_widget(GTK_WIDGET(gamewindow),"NameLabel")), foo);
	/*faucet_free(mname);*/
}

void
faucet_exits(GArray* gary, int garylen)
{
	gchar foo[1024];
	int i;
	
	foo[0]='\0';
	strcat (foo,"\n\nObvious Exits: ");
	for (i=(garylen-1);i>=0;i--)
	{
		strcat(foo,g_array_index(gary,char*,i));
		if (i>0)
			strcat(foo, ", ");
	}
	
	/*g_print("name: %s\n",mname);*/
	/*gtk_label_set_text(GTK_LABEL(lookup_widget(GTK_WIDGET(gamewindow),"NameLabel")), foo);*/

   faucet__exits__=strdup(foo);
   faucet_redesc();
	/*faucet_free(mname);*/
}


/* requested responses */

void
faucet_request_response(char* timekey,
						char* wintitle,
						char* bodyText)
{
	GtkWidget* rw;
	GtkText* mgtxt;
	int foo=1;
	if (!bodyText)
	{
		bodyText="(null)";
		foo=0;
	}
	
	rw= create_responsewindow();
	mgtxt = GTK_TEXT(lookup_widget(rw,"descriptive_text"));
	gtk_object_set_data(GTK_OBJECT(rw),"timekey",timekey);
	gtk_window_set_title(GTK_WINDOW(rw),wintitle);
	gtk_text_set_point(mgtxt,
					   gtk_text_get_length(mgtxt));
	gtk_text_freeze(mgtxt);
	gtk_text_insert(mgtxt,
					/*GTK_WIDGET(mgtxt)->style->font,*/NULL,
					/*& GTK_WIDGET(mgtxt)->style->black,*/NULL,
					NULL,
					bodyText,
					strlen(bodyText));
	gtk_text_set_word_wrap(mgtxt,TRUE);
	gtk_text_thaw(mgtxt);
	gtk_widget_show(rw);
	
	faucet_free(wintitle);
	if(foo)
		faucet_free(bodyText);
}

void faucet_got_response(char* str, char* key)
{
	/*g_print("faucet_got_response (\"%s\",\"%s\");\n",str,key);*/
	faucet_response_send(str,key);
}

void
faucet_completed_action()
{
	/*g_print("faucet_completed_action ();\n");*/
	GtkEntry* commandpanel;
	commandpanel=GTK_ENTRY(lookup_widget(gamewindow,"CommandPanel"));
	
	gtk_entry_set_editable(commandpanel,TRUE);
	gtk_widget_set_sensitive(GTK_WIDGET(commandpanel),TRUE);
	gtk_widget_grab_focus(GTK_WIDGET(commandpanel));
}

/* things */

GHashTable* faucet_things;

void
faucet_rething()
{
	
	GtkWidget* thin;
	int textlen;
	
	/*g_print("faucet_rething ();\n");*/
	
	thin=lookup_widget(gamewindow,"items_field");
	
	gtk_text_freeze(GTK_TEXT(thin));
	gtk_text_set_word_wrap(GTK_TEXT(thin),TRUE);
	textlen=gtk_text_get_length(GTK_TEXT(thin));
	gtk_editable_delete_text(GTK_EDITABLE(thin),0,textlen);
	gtk_text_set_point(GTK_TEXT(thin),0);
	
	g_hash_table_foreach(faucet_things,
						 faucet_internal_thing_add,
						 (gpointer) GTK_TEXT(thin));
	
	gtk_text_thaw(GTK_TEXT(thin));
}

void
faucet_clear_things()
{
	g_hash_table_foreach_remove(faucet_things,
								faucet_keyval_cleanup,
								NULL);
	g_hash_table_destroy(faucet_things);
	faucet_things=g_hash_table_new(g_str_hash,g_str_equal);
	faucet_rething();
}

#define FAUCET_DONE_ENTER 1
#define FAUCET_DONE_LEAVE 2

typedef struct _faucet_done_data
{
	GHashTable* mhash;
	char* mval;
	char* mkey;
} faucet_done_data;

gint
faucet_done(gpointer data)
{
	faucet_done_data* f;
	char* freeable;
	
	f = (faucet_done_data*) data;
	if(f->mhash==faucet_things)
	{
		freeable=g_hash_table_lookup(faucet_things,f->mkey);
		if(freeable==f->mval)
		{
			g_hash_table_remove(faucet_things,f->mkey);
			faucet_free(f->mval);
			faucet_free(f->mkey);
		}
		faucet_rething();
	}
	
	faucet_free(f);
	/* don't need to do this... I can return false...
	 * gtk_timeout_remove(f->my_id);*/
	return FALSE;
}

/* ATHRD 
 *
 * I know this is screwed up and hacky -- don't complain ... I had no
 * idea what I was doing...
 */

void
faucet_el_thing(char* key,
			    char* val,
				int to_choose)
{
	gpointer oldkey=0;
	gpointer oldval=0;
	
	faucet_done_data* donedata;
	donedata=g_new(faucet_done_data,sizeof(faucet_done_data));
	donedata->mkey=g_new(char,sizeof(char)*(2+strlen(key)));
	donedata->mhash=faucet_things;
	donedata->mval=g_new(char,sizeof(char)*(7+strlen(val)));
	(donedata->mkey)[0]=0;
	donedata->mval[0]=0;
	strcat(donedata->mkey,"+");
	if(to_choose==FAUCET_DONE_ENTER)
	{
		strcat(donedata->mval," +++ <");
	}
	else
	{
		strcat(donedata->mval," --- (");
	}
	strcat(donedata->mval,val);
	strcat(donedata->mkey,key);
	if (g_hash_table_lookup_extended(faucet_things,donedata->mkey,&oldkey,&oldval))
	{
		g_hash_table_remove(faucet_things,donedata->mkey);

		if (oldkey)
		{
			g_free(oldkey);
		}
		if (oldval)
		{
			g_free(oldval);
		}
	}
	g_hash_table_insert(faucet_things,
						donedata->mkey,
						donedata->mval);
	faucet_rething();
	/*donedata->my_id=*/gtk_timeout_add(8000,faucet_done,donedata);
	faucet_free(key);
	faucet_free(val);
}

void
faucet_remove_thing(char* key)
{
	g_hash_table_remove(faucet_things,key);
	faucet_rething();
}

void
faucet_add_thing(char* key, char* val)
{
	g_hash_table_insert(faucet_things,key,val);
	faucet_rething();
}

void
faucet_leave_thing(char* key, char* message)
{
	faucet_el_thing(key,message,FAUCET_DONE_LEAVE);
}

void
faucet_enter_thing(char* key, char* message)
{
	faucet_el_thing(key,message,FAUCET_DONE_ENTER);
}

void
faucet_logout()
{
	GArray* atemp;
	atemp=g_array_new(FALSE,TRUE,sizeof(char));
	faucet_send(CMD_Quit,atemp);
	rstream_close(faucet_fd);
	gtk_widget_hide(gamewindow);
	gtk_widget_show(loginwindow);
	faucet_completed_action();
	/* TODO: add something like this here -- */
	rstream_close(faucet_fd);
	gdk_input_remove(faucet_fd_rm);
	faucet_fd_rm=0;
	g_array_free(atemp,TRUE);
}
