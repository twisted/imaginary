# -*- test-case-name: reality.test_reality -*-
from twisted.python import reflect, log
from twisted.internet import reactor, base, error
from bisect import insort

import time

"""
Everything in reality should use me for scheduling and time-telling.
"""

# TODO: Don't make delays of 1000 ticks actually take
# 1000+(1000*mainloop_iteration_time) seconds.

class DelayedCall(base.DelayedCall):
    #a couple of rape'n'pastes to not use time.time()
    def reset(self, secondsFromNow):
        if self.cancelled:
            raise error.AlreadyCancelled
        elif self.called:
            raise error.AlreadyCalled
        else:
            self.time = timer.time() + secondsFromNow
            self.resetter(self)

    def __str__(self):
        try:
            func = self.func.func_name
            try:
                func = self.func.im_class.__name__ + '.' + func
            except:
                func = self.func
                if hasattr(func, 'func_code'):
                    func = func.func_code # func_code's repr sometimes has more useful info
        except:
            func = reflect.safe_repr(self.func)
        return "<Reality DelayedCall [%ds] called=%s cancelled=%s %s%s>" % (self.time - timer.time(), self.called, self.cancelled, func,
                                                                    reflect.safe_repr(self.args))


class Timer:
    """
    I simulate a real-time timing system for the purpose of simulation.
    """

    def __init__(self, test=False):
        self.test = test
        self.currentTicks = 0
        self._pendingTimedCalls = []
        self.synchedTime = time.time()
        if not test:
            self.dcall = reactor.callLater(1, self.runUntilCurrent)

    def runUntilCurrent(self):
        """Run all pending timed calls.
        """
        currentRealTime = time.time()
        while self.synchedTime < currentRealTime:
            self.tick()
        if not self.test:
            self.dcall = reactor.callLater(1, self.runUntilCurrent)

    def tick(self):
        self.synchedTime += 1
        self.currentTicks += 1
        while self._pendingTimedCalls and (self._pendingTimedCalls[-1].time <= self.currentTicks):
            call = self._pendingTimedCalls.pop()
            try:
                call.called = 1
                call.func(*call.args, **call.kw)
            except:
                log.deferr()


    def time(self):
        """
        Return time in ticks. A tick is one roughly one second.
        """
        return self.currentTicks

    def callLater(self, ticks, f, *args, **kw):
        """
        Call a function delayed by some amount of time.
        If ticks is 0, call the function synchronously. If you want
        `call in the next iteration', you should be using
        reactor.callLater.
        """
        assert callable(f)
        ticks = int(ticks)
        assert ticks >= 0, ticks

        if ticks == 0:
            return reactor.callLater(0, f, *args, **kw)

        tple = DelayedCall(self.currentTicks + ticks, f, args, kw, self._pendingTimedCalls.remove, self._resetCallLater)
        insort(self._pendingTimedCalls, tple)
        return tple

    def _resetCallLater(self, tple):
        self._pendingTimedCalls.remove(tple)
        insort(self._pendingTimedCalls, tple)
        return tple

class FakeTimer(Timer):
    def runUntilCurrent(self):
        """Run all pending timed calls.
        """
        self.tick()
        if not self.test:
            self.dcall = reactor.callLater(1, self.runUntilCurrent)



timer = Timer()
