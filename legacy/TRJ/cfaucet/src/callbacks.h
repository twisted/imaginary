#include <gnome.h>


gboolean
on_CommandPanel_key_press_event        (GtkWidget       *widget,
                                        GdkEventKey     *event,
                                        gpointer         user_data);

void
on_CommandPanel_activate               (GtkEditable     *editable,
                                        gpointer         user_data);

void
on_charname_entry_activate             (GtkEditable     *editable,
                                        gpointer         user_data);

void
on_pw_entry_activate                   (GtkEditable     *editable,
                                        gpointer         user_data);

void
on_engageButton_clicked                (GtkButton       *button,
                                        gpointer         user_data);

void
on_answerdialog_ok_clicked             (GtkButton       *button,
                                        gpointer         user_data);

void
on_ok_button_clicked                   (GtkButton       *button,
                                        gpointer         user_data);

void
on_notok_button_clicked                (GtkButton       *button,
                                        gpointer         user_data);

gboolean
on_gamewindow_delete_event             (GtkWidget       *widget,
                                        GdkEvent        *event,
                                        gpointer         user_data);

gboolean
on_loginwindow_delete_event            (GtkWidget       *widget,
                                        GdkEvent        *event,
                                        gpointer         user_data);

gboolean
on_loginwindow_destroy_event           (GtkWidget       *widget,
                                        GdkEvent        *event,
                                        gpointer         user_data);

void
on_loginwindow_destroy                 (GtkObject       *object,
                                        gpointer         user_data);

extern GtkWidget* loginwindow;
extern GtkWidget* gamewindow;
