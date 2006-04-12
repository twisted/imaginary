# -*- test-case-name: reality.test_reality -*-
"""
#1: Charge code will probably be moved to (New?)Divunal
#2: The design of these interfaces is very likely to change.
"""

from twisted.python import components
from twisted.python import util as tputil

from reality import things, errors
from reality.text import common
from reality.chronology import timer

## exceptions

class NotEnoughCharge(Exception):
    pass


class ConnectionError(Exception):
    pass

class Incompatible(ConnectionError):
    """
    Some source is incompatible with some sink.
    """
    pass

class AlreadyConnected(ConnectionError):
    pass

class NotConnected(ConnectionError):
    pass


## interfaces

# The decision to put `sinkTo' and `unsink' on IChargeSource rather
# than putting `sourceTo' on IChargeSink is *completely* arbitrary.

class IChargeSource(components.Interface):

    def requestChargeRate(self, sink, rate):
        """
        A request to send `rate' charge per second to `sink'.
        Suggested behavior is to call sink.receivingCharge(self, rate)
        """

    def sinkTo(self, sink):
        """
        A request to connect to `sink' somehow. Suggested behavior is
        to try to adapt the sink to an Interface representing the kind
        of objects you can sink to.
        """

    def unsink(self, sink):
        """
        Try to disconnect yourself from this sink.
        """

    def supports(self, sinkTypes):
        """
        Return True if this sink supports any of these sinkTypes, False otherwise.
        """

class IChargeSink(components.Interface):

    currentRate = property(doc="The current rate that this sink is receiving charge.")

    def receivingCharge(self, source, rate):
        """
        You're getting charge! `rate' is charge per second.
        """

    def gotSourced(self, source):
        """
        I have been successfully connected to the source `source'.
        """

    def getShapes(self):
        """
        Return a sequence of shape descriptors, usually to be passed
        to IChargeSource.supports.
        """



## Actions

from reality.text import english
from reality import actions

IZapTarget = IChargeSink
ITouchTarget = IChargeSink

class IZapActor(components.Interface):
    def preActor(self, action):
        """What?"""
    def postActor(self, action):
        """What??"""

    def zap(self, sink):
        """
        Zap this sink forcibly.
        """

class Touch(actions.TargetAction):
    """
    Allow charge to go from the actor to the target.
    """

    def doAction(self):
        print "touching", self.target
        zapper = ITouchActor(self.actor)
        try:
            zapper.sinkTo(self.target)
            zapper.unsink(self.target)
        except NotEnoughCharge:
            raise errors.ActionFailed("You don't have enough charge to touch ", self.target, "!")


class Zap(actions.TargetAction):
    """
    Force some charge into the target.
    TODO: `zapAbility', or something?
    """
    def doAction(self):
        print "zapping", self.target
        zapper = IZapActor(self.actor)
        try:
            zapper.zap(self.target)
        except NotEnoughCharge:
            raise errors.ActionFailed("You don't have enough charge to zap ", self.target, "!")
        except AlreadyConnected:
            raise errors.ActionFailed("You're already zapping ", zapper.sink)


class Connect(actions.ToolAction):
    """
    Try to connect some IChargeSource to some IChargeSink (order
    doesn't matter).
    """

    def getPotentialAmbiguities(self, iName, iType):
        """
        Allow tools and targets to be interchangeable
        """
        if iType in ('Tool', 'Target'):
            t = things.IInterfaceForwarder(self.actor)
            return tputil.uniquify((t.lookFor(iName, IChargeSink) +
                                    t.lookFor(iName, IChargeSource)))
        return actions.ToolAction.getPotentialAmbiguities(self, iName, iType)

    def doIt(self, source, sink):
        IChargeSource(source).sinkTo(IChargeSink(sink))

    def failed(self):
        raise errors.ActionFailed("You can't connect ", self.tool, " to ", self.target, "!")

    def doAction(self):
        for source, sink in ((self.tool, self.target),
                             (self.target, self.tool)):
            try:
                self.doIt(source, sink)
                break
            except (ConnectionError, components.CannotAdapt):
                pass
        else:
            self.failed()


class Disconnect(Connect):
    def doIt(self, source, sink):
        IChargeSource(source).unsink(IChargeSink(sink))

    def failed(self):
        raise errors.ActionFailed("You can't disconnect ", self.tool, " and ", self.target, "!")

class IBatterySink:
    pass

class IBatteryChargerSink:
    pass

class DefaultSource(components.Adapter):
    """
    Convenience for default implementations of some IChargeSource methods.
    Assumes that there can only be one sink for this source.

    @cvar compatibleSinks: A sequence of descriptors (Suggested:
                           Interfaces) that this object supports as sinks.
    """

    #sinkInterface = None
    compatibleSinks = ()
    sink = None

    def sinkTo(self, sink):
        if self.sink:
            raise AlreadyConnected("Can't set my (%s) sink to %s, because %s is already connected." % (self.original, sink, self.sink))
        sink = IChargeSink(sink)
        shapes = sink.getShapes()
        if not self.supports(shapes):
            raise Incompatible("Can't fit %s (which supports %s) with %s (which supports %s)." %
                               (self.original, self.compatibleSinks, sink, shapes))
        self.sink = sink
        self.sink.gotSourced(self)

    def supports(self, shapes):
        return bool(filter(shapes.__contains__, self.compatibleSinks))

    def unsink(self, sink):
        sink = IChargeSink(sink)
        if not self.sink or self.sink != sink:
            raise NotConnected("Can't disconnect %s from myself (%s), %s is currently connected." % (sink, self.original, self.sink))
        self.sink.receivingCharge(self, 0)
        self.sink = None


class Capacitor(DefaultSource):

    __implements__ = IChargeSink, IChargeSource 

    # setting these *needs* extra calculation, don't touch!

    # there should eventually be a blowupCapacity that's higher than
    # maximumCapacity. When in between them, charge should be reduced
    # over time and cause some minor damage. When blowupCapacity is
    # met, well, boom.
    _maximumCapacity = 150
    _charge = 100

    defaultRate = 5 #cps; Charge Per Second

    sink = None

    lastRateChange = 0
    currentRate = 0

    dcall = None

    def setMaximumCapacity(self, val):
        self._maximumCapacity = val
        self.updateCharge()


    def updateCharge(self, newRate=None, newCharge=None):
        """
        newRate can be a positive or negative integer. Positive if
        we're gaining charge, negative if we're losing it.

        newCharge should be an integer representing the absolute
        charge value you want to set it to.

        Note that if there is a current rate or you have passed in a
        non-zero newRate (positive or negative), I will still
        calculate charge that
        """
        # this should be the only place EVER that touches _charge or
        # _maximumCapacity.

        if self.dcall and self.dcall.active():
            self.dcall.cancel()

        if newRate is None:
            newRate = self.currentRate
        if newCharge is not None:
            self._charge = newCharge
            if not newRate:
                return

        # Don't create something from nothing, mr sink!  XXX this will
        # need to be either formalized or taken out, because
        # sink.currentRate isn't API.

        if self.sink:
            assert abs(self.currentRate) >= self.sink.currentRate, (self.currentRate, self.currentRate)


        # update the current charge
        lastRateChange = self.lastRateChange
        self.lastRateChange = timer.time()

        diff = self.lastRateChange - lastRateChange
        self._charge += diff * self.currentRate

        self.currentRate = newRate

        # make sure we notice when the charge reaches boundaries

        if newRate < 0:
            # we're heading for a power-outage
            self.dcall = timer.callLater(self._charge / abs(newRate),
                                           self.outOfCharge)

        elif newRate > 0:
            #we're heading for meltdown
            meltdown = (self._maximumCapacity - self._charge) / newRate
            if meltdown < 0:
                return self.blowup()
            self.dcall = timer.callLater(
                (self._maximumCapacity - self._charge) / newRate,
                self.fullOfCharge)

        return self._charge

    def outOfCharge(self):
        self.requestChargeRate(self.sink, 0)

    #ISource

    def requestChargeRate(self, sink, rate):
        assert sink is self.sink, "I can only give charge to my sink!"
        if not self.updateCharge():
            raise NotEnoughCharge()
        self.updateCharge(newRate=-rate)
        sink.receivingCharge(self, rate)


    #ISink

    chargingCall = None

    def gotSourced(self, source):
        assert not self.sink, "omfg, don't even try it."
        source = IChargeSource(source)
        self.source = source
        source.requestChargeRate(self, self.defaultRate)

    def receivingCharge(self, source, rate):
        assert source is self.source, "I can only take charge from my source!"
        self.updateCharge(newRate=rate)
        return rate

    #not ISink, but related
    def fullOfCharge(self):
        assert self.source
        self.source.requestChargeRate(self, 0)
        self.blowupCall = timer.callLater(1, self.maybeBlowup)

    def maybeBlowup(self):
        if self.updateCharge() > self._maximumCapacity:
            self.blowup()

    def blowup(self):
        print "blowing up!"
        self.original.emitEvent(("BOOM, goes ", self.original))
        self.original.destroy()

class Battery(Capacitor):

    compatibleSinks = IBatterySink,

    def getShapes(self):
        return IBatteryChargerSink, IBatterySink


class PlayerZapper(Capacitor):
    __implements__ = IChargeSink, IChargeSource, IZapActor, ITouchActor, IConnectActor, IDisconnectActor

    compatibleSinks = IBatterySink,
    
    zapping = 0

    #IZapActor
    def zap(self, sink):
        if self.sink:
            raise AlreadyConnected("You're already zapping", self.sink)
        if self.updateCharge() < 20:
            raise NotEnoughCharge("You don't have enough charge for that.")

        self.zapping = 20
        Capacitor.sinkTo(self, sink)
        self.sink.receivingCharge(self, 20)
        timer.callLater(1, self.doneZapping)

    def doneZapping(self):
        self.zapping = 0
        self.unsink(self.sink)


    #ISource
    def requestChargeRate(self, sink, rate):
        if not self.zapping:
            return Capacitor.requestChargeRate(self, sink, rate)


    #ISink
    def getShapes(self):
        return IBatteryChargerSink,

class BatteryCharger(DefaultSource):
    """
    Infini-charger!
    """

    __implements__ = IChargeSource, 

    compatibleSinks = IBatteryChargerSink,



    def __init__(self, original):
        DefaultSource.__init__(self, original)
        fmt = ", with a light that is currently %s."
        self.offDesc = (self.original, fmt % 'dark')
        self.chargeDesc = (self.original, fmt % 'shining red')
        self.doneDesc = (self.original, fmt % 'shining green.')
        common.IDescribeable(self.original).describe('__main__', self.offDesc)

    def sinkTo(self, sink):
        DefaultSource.sinkTo(self, sink)
        self.original.emitEvent(("A light on ", self.original, " turns red."))
        common.IDescribeable(self.original).describe('__main__', self.chargeDesc)

    def unsink(self, sink):
        DefaultSource.unsink(self, sink)
        self.original.emitEvent(("A light on ", self.original, " goes out."))
        common.IDescribeable(self.original).describe('__main__', self.offDesc)

    def requestChargeRate(self, sink, rate):
        sink = IChargeSink(sink)
        sink.receivingCharge(self, rate)
        if not rate:
            self.original.emitEvent(("A light on ", self.original, " turns green."))
            common.IDescribeable(self.original).describe('__main__', self.doneDesc)


class Radio(components.Adapter):
    """
    I have a place to put batteries, and play music when I have power.
    """

    __implements__ = IChargeSink, ITouchTarget, IZapTarget, 

    defaultRate = 5
    currentRate = 0

    def getShapes(self):
        return IBatterySink,

    def gotSourced(self, source):
        self.source = source
        source.requestChargeRate(self, self.defaultRate)

    def receivingCharge(self, source, rate):
        self.currentRate = rate
        if rate == 0:
            msg = "Off"
        elif rate == self.defaultRate:
            msg = "la la"
        elif rate > self.defaultRate:
            msg = "BOOM"
        else:
            msg = "whimper :("
        self.original.emitEvent((msg, ", says", self.original), intensity=2)
        common.IDescribeable(self.original).describe('__main__',
                                                     (self.original, ", saying ", msg))



class ZapParser(english.Subparser):
    simpleTargetParsers = {'touch': Touch,
                           'zap': Zap}
    simpleToolParsers = {'connect': Connect,
                         'disconnect': Disconnect}

english.registerSubparser(ZapParser())


components.registerAdapter(PlayerZapper, things.Actor, ITouchActor)
components.registerAdapter(PlayerZapper, things.Actor, IZapActor)
components.registerAdapter(PlayerZapper, things.Actor, IConnectActor)
components.registerAdapter(PlayerZapper, things.Actor, IDisconnectActor)
components.registerAdapter(PlayerZapper, things.Actor, IChargeSource)
components.registerAdapter(PlayerZapper, things.Actor, IChargeSink)
