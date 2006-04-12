#include <glib.h>

#ifndef __REALITY_STREAM_H__
#define __REALITY_STREAM_H__ 1
gboolean
rstream_write_utf(gint rstream,
				  const gchar* data);

gboolean
rstream_write_short(gint rstream,
					gint data);

gboolean
rstream_write_byte(gint rstream,
				   gchar data);

gint
rstream_open(const gchar* hostname);

void
rstream_close(gint rstream);

gchar*
rstream_read_utf(gint rstream);

gint
rstream_read_short(gint rstream);

gchar
rstream_read_byte(gint rstream);
#endif
