/* fileutils.c */
/* cproto tells me this stuff is part of this file: something tells me it's not */
/*__inline__ int __stat(__const char *__path, struct stat *__statbuf);
  __inline__ int stat(__const char *__path, struct stat *__statbuf);
  __inline__ int __lstat(__const char *__path, struct stat *__statbuf);
  __inline__ int lstat(__const char *__path, struct stat *__statbuf);
  __inline__ int __fstat(int __fd, struct stat *__statbuf);
  __inline__ int fstat(int __fd, struct stat *__statbuf);
  __inline__ int __mknod(__const char *__path, __mode_t __mode, __dev_t __dev);
  __inline__ int mknod(__const char *__path, __mode_t __mode, __dev_t __dev);*/

#ifndef __FILE_UTILS_H__
#define __FILE_UTILS_H__ 1
void md(char *s);
int exists(char *s);
int isfile(char *s);
int isdir(char *s);
int ls_compare_func(const void *a, const void *b);
char **ls(char *dir, int *num);
void freestrlist(char **l, int num);
void rm(char *s);
void mv(char *s, char *ss);
void cp(char *s, char *ss);
unsigned long moddate(char *s);
int filesize(char *s);
void cd(char *s);
char *cwd(void);
int permissions(char *s);
int owner(char *s);
int group(char *s);
char *username(int uid);
char *homedir(int uid);
char *usershell(int uid);
char *atword(char *s, int num);
char *atchar(char *s, char c);
void word(char *s, int num, char *wd);
int canread(char *s);
int canwrite(char *s);
int canexec(char *s);
char *fileof(char *s);
char *fullfileof(char *s);
char *noext(char *s);
void mkdirs(char *s);
#endif
