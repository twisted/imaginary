/* X-Chat
 * Copyright (C) 1998 Peter Zelezny.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA
 */

#include <string.h>
#include <stdlib.h>
#include <gdk/gdkkeysyms.h>
#include <gtk/gtk.h>
#include "history.h"
#include "faucet.h"

struct history * history_history;

void history_add(char *text)
{
	if(history_history->lines[history_history->realpos])
		free(history_history->lines[history_history->realpos]);
	history_history->lines[history_history->realpos] = strdup(text);
	history_history->realpos++;
	if(history_history->realpos == HISTORY_SIZE)
		history_history->realpos = 0;
	history_history->pos = history_history->realpos;
}
void history_init()
{
	history_history=g_new(struct history,sizeof(struct history));
}
void history_free()
{
	int i;
	for(i = 0; i < HISTORY_SIZE; i++)
	{
		if(history_history->lines[i]) free(history_history->lines[i]);
	}
}

void history_insert_text(GtkWidget *entry, char *text)
{
	char newtext[3000];
	char *oldtext;
	int pos;
	
	oldtext = gtk_entry_get_text(GTK_ENTRY(entry));
	pos = gtk_editable_get_position((GtkEditable*)entry);
	strcpy(newtext, oldtext);
	newtext[pos] = 0;
	strcat(newtext, text);
	strcat(newtext, &oldtext[pos]);
	gtk_entry_set_text(GTK_ENTRY(entry), newtext);
	gtk_entry_set_position(GTK_ENTRY(entry), pos + strlen(text));
}
/*
  Ostensibly, this does *something* but I can't figure out what.
  
  void history_function_key(GtkWidget *entry, int which)
  {
  GSList *list = fkey_list;
  int i = 0;
  
  while(list)
  {
  char *macro = (char *)list -> data;
  i++;
  if(i == which)
  {
  history_insert_text(entry, macro);
  return;
  }
  list = list -> next;
  }
  }
*/
int history_keypress(GtkWidget *widget, GdkEventKey *event)
{
	char* blurp;
	char* murp;
	murp=NULL;
	switch (event->keyval)
	{
		/*case GDK_F1: history_function_key(widget, 1); break;
		  case GDK_F2: history_function_key(widget, 2); break;
		  case GDK_F3: history_function_key(widget, 3); break;
		  case GDK_F4: history_function_key(widget, 4); break;
		  case GDK_F5: history_function_key(widget, 5); break;
		  case GDK_F6: history_function_key(widget, 6); break;
		  case GDK_F7: history_function_key(widget, 7); break;
		  case GDK_F8: history_function_key(widget, 8); break;
		  case GDK_F9: history_function_key(widget, 9); break;
		  case GDK_F10: history_function_key(widget, 10); break;*/
	case GDK_KP_0:
		faucet_verb_send("go up");
		break;
	case GDK_KP_1:
		faucet_verb_send("go southwest");
		break;
	case GDK_KP_2:
		faucet_verb_send("go south");
		break;
	case GDK_KP_3:
		faucet_verb_send("go southeast");
		break;
	case GDK_KP_4:
		faucet_verb_send("go west");
		break;
	case GDK_KP_5:
		faucet_verb_send("go down");
		break;
	case GDK_KP_6:
		faucet_verb_send("go east");
		break;
	case GDK_KP_7:
		faucet_verb_send("go northwest");
		break;
	case GDK_KP_8:
		faucet_verb_send("go north");
		break;
	case GDK_KP_9:
		faucet_verb_send("go northeast");
		break;
    case GDK_Down:
		history_history->pos++;
		if(history_history->pos == HISTORY_SIZE) history_history->pos = 0;
		if(history_history->lines[history_history->pos])
		{
			gtk_entry_set_text(GTK_ENTRY(widget), history_history->lines[history_history->pos]);
		} else {
			if(history_history->pos != 0)
				history_history->pos--;
			else
				history_history->pos = (HISTORY_SIZE-1);
		}
		break;
		
    case GDK_Up:
		if(history_history->pos == 0)
			history_history->pos = (HISTORY_SIZE-1);
		else
			history_history->pos--;
		if(history_history->lines[history_history->pos])
		{
			gtk_entry_set_text(GTK_ENTRY(widget), history_history->lines[history_history->pos]);
		} else {
			if(history_history->pos == (HISTORY_SIZE-1))
				history_history->pos = 0;
			else
				history_history->pos++;
		}
		break;
		/* ok, not *strictly* history stuff here */
	case '\'':
		murp="say \"";
	case ';':
		if(!murp) murp="emote \"";
		blurp=gtk_entry_get_text(GTK_ENTRY(widget));
		if(blurp[0]==0)
		{
			gtk_entry_set_text(GTK_ENTRY(widget),murp);
		}
		else
		{
			return 0;
		}
		break;
		/*case GDK_Page_Up:
		  break;
		  
		  case GDK_Page_Down:
		  break;*/
		
    default:
		return 0;
	}
	gtk_signal_emit_stop_by_name(GTK_OBJECT(widget), "key_press_event");
	return 1;
}
