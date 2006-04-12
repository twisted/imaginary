#ifndef __HISTORY_H__
#define __HISTORY_H__ 1

#include <glib.h>
#define HISTORY_SIZE 100

struct history
{
   char *lines[HISTORY_SIZE];
   int pos;
   int realpos;
};

extern struct history* history_history;
extern GSList *fkey_list;

void history_add(char *text);
void history_free(void);
int history_keypress(GtkWidget *widget, GdkEventKey *event);
void history_init(void);
void history_insert_text(GtkWidget *entry, char *text);
#endif
