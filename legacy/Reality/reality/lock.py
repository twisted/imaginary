
# Twisted, the Framework of Your Internet
# Copyright (C) 2001 Matthew W. Lefkowitz
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of version 2.1 of the GNU Lesser General Public
# License as published by the Free Software Foundation.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


"""
Lockable objects
"""

#TR imports
import thing
import error

from twisted.python import reflect
from reality.phrase import registerSubparser, Subparser, Parsing, IParsing
from reality.actions import ToolAction
from twisted.python.components import Interface, implements, registerAdapter, Adapter

class NoTargetMatch(error.RealityException):
    """Exception raised when a key doesn't fit a lock.
    """

class ItsLocked(error.RealityException):
    """Exception raised when an object is locked.
    """

class ILockTool(Interface):
    """A tool that can be used to lock things.
    """
    def checkLockTarget(self, target):
        """Determine whether I match a lock target.

        @raise NoTargetMatch: when the lock does match.
        @return None: Upon success.
        """

class IUnlockTool(Interface):
    """A tool that can be used to unlock things.
    """
    def checkUnlockTarget(self, target):
        """Determine whether I match a lock target.

        See ILockTool.checkLockTarget
        """

class ILockTarget(Interface):
    def lock(self):
        """Lock it!
        """

class IUnlockTarget(Interface):
    def unlock(self):
        """Unlock it!
        """

class Lock(ToolAction):
    """I am an action to lock an object with another.
    """
    def doAction(self):
        self.tool.checkLockTarget(self.target)
        self.target.lock()
        

class Unlock(ToolAction):
    """I am an action to unlock an object with another.
    """
    def doAction(self):
        self.tool.checkUnlockTarget(self.target)
        self.target.unlock()

class LockVerbs(Subparser):
    simpleToolParsers = {"lock": Lock,
                         "unlock": Unlock}

registerSubparser(LockVerbs())


class Key(Adapter):
    """ A generic key; something you can unlock stuff with.
    """
    __implements__ = ILockTool, IUnlockTool

    def __init__(self, original):
        Adapter.__init__(self, original)
        self.lockTypes = []
        self.unlockTypes = self.lockTypes

    def _checkTarget(self, target, l):
        if not reflect.isinst(target, Lockable):
            # TODO: clean this up to use an interface
            NoTargetMatch(target.original, "isn't lockable.")
        for type in key.lockTypes:
            if type in self.lockTypes:
                return
        raise NoTargetMatch(self.original, " doesn't seem to fit.")

    def checkLockTarget(self, target):
        return self._checkTarget(target, self.lockTypes)

    def checkUnlockTarget(self, target):
        return self._checkTarget(target, self.unlockTypes)


class SkeletonKey(Adapter):

    __implements__ = ILockTool, IUnlockTool

    def checkLockTarget(self, target):
        """Always Allow Locking
        """

    def checkUnlockTarget(self, target):
        """Always Allow Unlocking
        """

class Lockable(Adapter):
    """ Mixable superclass of all lockable objects.

    This is a mixin because it's a feature which can be added to existing Thing
    classes (see door.py for an example of this)
    """
    __implements__ = ILockTarget, IUnlockTarget
    locked = 0

    def __init__(self, original):
        Adapter.__init__(self, original)
        self.locked = 0
        self.unlockTypes = self.lockTypes = []

    def lock(self):
        "cause self to become locked"
        if self.locked:
            raise error.Already(self.original, " is already locked.")
        self.locked = 1

    def unlock(self):
        "cause self to become unlocked"
        if not self.locked:
            raise error.Already(self.original, " is already unlocked.")
        self.locked = 0

    def checkLock(self):
        "raise an appropriate exception if this is locked."
        if self.locked:
            ItsLocked(self," is locked.")

