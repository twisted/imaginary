# -*- test-case-name: imaginary.test -*-

from zope.interface import implements

import pyparsing

from twisted.internet import defer
from twisted.python import context

from imaginary import iimaginary, eimaginary


_quoteRemovingQuotedString = pyparsing.quotedString.copy()
_quoteRemovingQuotedString.setParseAction(pyparsing.removeQuotes)

def targetString(name):
    return (
        pyparsing.Word(pyparsing.alphanums) ^
        _quoteRemovingQuotedString).setResultsName(name)



class TransactionalEventBroadcaster(object):
    """
    Collect a bunch of output events as a transaction is being executed, then
    distribute them when it has completed.

    Events can be added normally or as revert events.  Normal events are
    broadcast after the transaction is successfully committed.  Revert events
    are broadcast if the transaction failed somehow and was been reverted.
    """
    implements(iimaginary.ITransactionalEventBroadcaster)

    def __init__(self):
        self._events = []
        self._revertEvents = []


    def addEvent(self, event):
        """
        Add a normal event.

        @param event: A no-argument callable to be invoked when this
        transaction has been committed.
        """
        if not callable(event):
            raise ValueError("Events must be callable", event)
        self._events.append(event)


    def addRevertEvent(self, event):
        """
        Add a revert event.

        @param event: A no-argument callable to be invoked when this
        transaction has been reverted.
        """
        if not callable(event):
            raise ValueError("Events must be callable", event)
        self._revertEvents.append(event)


    def broadcastEvents(self):
        """
        Send all normal events.
        """
        events = self._events
        self._events = self._revertEvents = None
        map(apply, events)


    def broadcastRevertEvents(self):
        """
        Send all revert events.
        """
        events = self._revertEvents
        self._events = self._revertEvents = None
        map(apply, events)



class CommandType(type):
    commands = []
    def __new__(cls, name, bases, attrs):
        infrastructure = attrs.pop('infrastructure', False)
        t = super(CommandType, cls).__new__(cls, name, bases, attrs)
        if not infrastructure:
            cls.commands.append(t)
        return t


    def parse(self, player, line):
        for cls in self.commands:
            try:
                match = cls.match(player, line)
            except pyparsing.ParseException:
                pass
            else:
                if match is not None:
                    match = dict(match)
                    for k,v in match.items():
                        if isinstance(v, pyparsing.ParseResults):
                            match[k] = v[0]

                    return cls().runEventTransaction(player, line, match)
        return defer.fail(eimaginary.NoSuchCommand(line))



class Command(object):
    __metaclass__ = CommandType
    infrastructure = True

    def match(cls, player, line):
        return cls.expr.parseString(line)
    match = classmethod(match)


    def runEventTransaction(self, player, line, match):
        """
        Take a player, line, and dictionary of parse results and execute the
        actual Action implementation.

        This takes responsibility for setting up the transactional event
        broadcasting junk, handling action errors, and broadcasting commit or
        revert events.

        @param player: A provider of C{self.actorInterface}
        @param line: A unicode string containing the original input
        @param match: A dictionary containing some parse results to pass
        through to the C{run} method.
        """
        broadcaster = TransactionalEventBroadcaster()
        def runHelper():
            # Set up event context for the duration of the action
            # run.  Additionally, handle raised ActionFailures by
            # adding their events to the revert event list and
            # re-raising them so they will revert the transaction.
            try:
                return context.call(
                    {iimaginary.ITransactionalEventBroadcaster: broadcaster},
                    self.run, player, line, **match)
            except eimaginary.ActionFailure, e:
                broadcaster.addRevertEvent(e.event.reify())
                raise
        try:
            result = player.store.transact(runHelper)
        except eimaginary.ActionFailure, e:
            broadcaster.broadcastRevertEvents()
            return None
        else:
            broadcaster.broadcastEvents()
            return result
