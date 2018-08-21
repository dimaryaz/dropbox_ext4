/*
 * Wraps statfs64 and changes the filesystem type to EXT4.
 */

#include <stdlib.h>
#include <dlfcn.h>
#include <sys/vfs.h>
#include <linux/magic.h>

int statfs64(const char *path, struct statfs64 *buf) {
  static int (*orig_statfs64)(const char *path, struct statfs64 *buf) = NULL;

  if (orig_statfs64 == NULL) {
    orig_statfs64 = dlsym(RTLD_NEXT, "statfs64");
  }

  int retval = orig_statfs64(path, buf);
  if (retval == 0) {
    buf->f_type = EXT4_SUPER_MAGIC;
  }
  return retval;
}
