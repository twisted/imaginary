#include <glib.h>

#ifndef __FAUCET_H__
#define __FAUCET_H__ 1

extern int faucet_fd;
extern GHashTable* faucet_descriptors;
extern GHashTable* faucet_things;

void faucet_answer(gchar *string);
void faucet_free(gpointer foo);
void faucet_init(void);
void faucet_make_progress(void);
void faucet_reset_progress(void);
void faucet_login(const char *login, const char *password, const char *hostname);
gint faucet_recieve(gint mfaucet, GArray **resultaddr, int *mint);
void faucet_data_in(gpointer data, gint mfaucet, GdkInputCondition cond);
void faucet_response_send(char *key, char *response);
void faucet_verb_send(char *cmd);
void faucet_send(gint command, GArray *arry);
void edit_file_to_use(gchar *file, gchar *theme);
gboolean faucet_retheme(GtkWidget *toSwitch);
void faucet_set_theme(const char *themename);
void faucet_gtk_theme_setup(void);
void faucet_internal_thing_add(gpointer key, gpointer value, gpointer foo);
void faucet_internal_desc_add(gpointer key, gpointer value, gpointer foo);
void faucet_redesc(void);
void faucet_add_descriptor(char *key, char *value);
void faucet_remove_descriptor(char *key);
void faucet_clear_descriptors(void);
gboolean faucet_keyval_cleanup(gpointer a, gpointer b, gpointer user_data);
void faucet_hears(char *toHear);
void faucet_name(GArray *gary, int garylen);
void faucet_exits(GArray *gary, int garylen);
void faucet_request_response(char *timekey, char *wintitle, char *bodyText);
void faucet_got_response(char *str, char *key);
void faucet_completed_action(void);
void faucet_rething(void);
void faucet_clear_things(void);
gint faucet_done(gpointer data);
void faucet_el_thing(char *key, char *val, int to_choose);
void faucet_remove_thing(char *key);
void faucet_add_thing(char *key, char *val);
void faucet_leave_thing(char *key, char *message);
void faucet_enter_thing(char *key, char *message);
void faucet_logout(void);

#endif

