
"""Persistence support for Pottery

For now, this defines a service which holds a reference to the game's
realm instance.  Periodically, the realm is pickled and written to
disk.  When the service is created, if an existing pickled realm
exists on disk, it is loaded and used instead of the realm passed in.
"""


import os, errno
import cPickle as pickle

from twisted.application import service
from twisted.internet import task
from twisted.python import log

class PersistenceService(service.Service):
    def __init__(self, fname, realm):
        self.fname = fname
        if os.path.exists(fname):
            realm = self._unpersist()
        self.realm = realm

    def startService(self):
        self.loop = task.LoopingCall(self._persist)
        self.loop.start(60).addErrback(log.err)

    def stopService(self):
        self.loop.stop()
        self._persist()

    def _persist(self):
        # Try to reap the previous persistence child.
        try:
            os.waitpid(-1, os.WNOHANG)
        except OSError, e:
            if e.errno != errno.ECHILD:
                raise

        # Fork and continue normal execution in the parent.  In the child,
        # try to acquire the persist lock.  If it cannot be acquired,
        # return.  Otherwise, pickle game state to a new file, move the
        # entire result over the existing game state file, and release the
        # lock.
        pid = os.fork()
        if pid == 0:
            try:
                try:
                    os.mkdir(self.fname + '.lock')
                except OSError, e:
                    if e.errno != errno.EEXIST:
                        raise
                else:
                    try:
                        fObj = file(self.fname + '.tmp', 'wb')
                        fObj.write(pickle.dumps(self.realm))
                        fObj.close()
                        os.rename(self.fname + '.tmp', self.fname)
                    finally:
                        os.rmdir(self.fname + '.lock')
            finally:
                os._exit(0)

    def _unpersist(self):
        fObj = file(self.fname, 'rb')
        return pickle.loads(fObj.read())

