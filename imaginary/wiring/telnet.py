
from zope.interface import implements

from twisted.internet import protocol, reactor, defer
from twisted.cred import credentials, portal, checkers
from twisted.application import service
from twisted.protocols import policies

from twisted.conch import telnet
from twisted.conch.insults import insults

from axiom import item, attributes, userbase

from xmantissa import stats

from imaginary import iimaginary
from imaginary.wiring import textserver

class ImaginaryTelnetFactory(protocol.ServerFactory):
    def __init__(self, realm, portal, applicationProtocolFactory):
        self.realm = realm
        self.portal = portal
        self.applicationProtocolFactory = applicationProtocolFactory

    def protocol(self):
        return telnet.TelnetTransport(
            telnet.TelnetBootstrapProtocol,
            insults.ServerProtocol,
            self.applicationProtocolFactory)

    def login(self, username, password):
        return self.portal.login(
            credentials.UsernamePassword(username, password),
            None,
            iimaginary.IActor)

    def create(self, username, password):
        return self.realm.create(username, password)


    def loggedIn(self, avatar):
        return self.realm.loggedIn(avatar)



class TelnetService(item.Item, service.Service):
    implements(iimaginary.ITelnetService)

    portNumber = attributes.integer(
        "The TCP port to bind to serve telnet.",
        default=4023)

    # These are for the Service stuff
    parent = attributes.inmemory()
    running = attributes.inmemory()

    # A cred portal, a Twisted TCP factory and an IListeningPort.
    portal = attributes.inmemory()
    factory = attributes.inmemory()
    port = attributes.inmemory()

    # When enabled, toss all traffic into logfiles.
    debug = False

    def activate(self):
        self.portal = None
        self.factory = None
        self.port = None


    powerupInterfaces = (service.IService, iimaginary.ITelnetService)

    def installed(self):
        self.setServiceParent(self.store)


    def privilegedStartService(self):
        ls = self.store.findUnique(userbase.LoginSystem)
        appStore = ls.accountByAddress(u'Imaginary', None)
        realm = portal.IRealm(appStore)
        chk = checkers.ICredentialsChecker(appStore)
        p = portal.Portal(realm, [chk])

        self.factory = ImaginaryTelnetFactory(realm, p, textserver.TextServer)

        if self.debug:
            self.factory = policies.TrafficLoggingFactory(self.factory, 'telnet')

        self.factory = stats.BandwidthMeasuringFactory(self.factory, 'telnet')

        if self.portNumber is not None:
            self.port = reactor.listenTCP(self.portNumber, self.factory)


    def stopService(self):
        L = []
        if self.port is not None:
            L.append(defer.maybeDeferred(self.port.stopListening))
            self.port = None
        return defer.DeferredList(L)
