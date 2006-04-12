#include <glib.h>
#include <gtk/gtk.h>
#include <netinet/in.h>

#include "sockhelp.h"
#include "reality_stream.h"

gboolean
rstream_write_utf(gint rstream,
				  const char* data)
{
	int mlen;
	mlen=strlen(data);
	rstream_write_short(rstream,mlen);
	write(rstream,data,mlen);
	fsync(rstream);
	return TRUE;
}

/*
 * This assumes that an 'int' in C is a 'short' and therefore 2 bytes
 * long... luckily, thanks to htons I don't have to assume the
 * host-byte-order ... hopefully network byte order is never
 * little-endian :-P
 */

gboolean
rstream_write_short(gint rstream,
					gint data)
{
	char toWrite[2];
	int netdata = htons(data);
	int ret;
	toWrite[1]= (netdata >> 8) & 0x00FF;
	toWrite[0]= netdata&0x00FF;
	
	ret=write(rstream,toWrite,2);
	fdatasync(rstream);
	if(ret!=2)
	{
		return FALSE;
	}
	return TRUE;
}

gboolean
rstream_write_byte(gint rstream,
				   char data)
{
	int wrotestuff;
	wrotestuff=write(rstream,&data,1);
	fsync(rstream);
	if(wrotestuff!=1)
	{
		return FALSE;
	}
	return TRUE;
}

int
rstream_open(const char* hostname)
{
	return make_connection("8889",SOCK_STREAM,hostname);
}

void
rstream_close(gint rstream)
{
	close(rstream);
}

/* MUST BE FREED WITH g_free() !! */

char*
rstream_read_utf(gint rstream)
{
	gint strsize;
	char* databuffer;
	strsize=rstream_read_short(rstream);
	databuffer=g_new(char,sizeof(char)*(strsize+1));
	sock_read(rstream,databuffer,strsize);
	databuffer[strsize]='\0';
	return databuffer;
}

gint
rstream_read_short(gint rstream)
{
	char small[2];
	gint ret;

	small[0]=rstream_read_byte(rstream);
	small[1]=rstream_read_byte(rstream);
	
	ret = ntohs(small[0] | (small[1] << 8));
	
	return ret;
}

char
rstream_read_byte(gint rstream)
{
	char ret;
	read(rstream,&ret,1);
	return ret;
}
