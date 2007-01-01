# -*- test-case-name: imaginary.test.test_wiring -*-

from zope.interface import implements

from twisted.internet import protocol
from twisted.cred import credentials, portal, checkers
from twisted.protocols import policies

from twisted.conch import telnet
from twisted.conch.insults import insults

from axiom import item, attributes, userbase

from xmantissa.ixmantissa import IProtocolFactoryFactory
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



class TelnetService(item.Item):
    implements(IProtocolFactoryFactory, iimaginary.ITelnetService)

    powerupInterfaces = (IProtocolFactoryFactory, iimaginary.ITelnetService)

    # A cred portal, a Twisted TCP factory and an IListeningPort.
    portal = attributes.inmemory()
    factory = attributes.inmemory()

    # When enabled, toss all traffic into logfiles.
    debug = False

    # An attribute which exists only because Axiom requires at least one
    # attribute on any Item subclass.
    garbage = attributes.integer(default=82671623)

    def activate(self):
        self.portal = None
        self.factory = None


    # IProtocolFactoryFactory
    def getFactory(self):
        if self.factory is None:
            ls = self.store.findUnique(userbase.LoginSystem)
            appStore = ls.accountByAddress(u'Imaginary', None)
            realm = portal.IRealm(appStore)
            chk = checkers.ICredentialsChecker(appStore)
            p = portal.Portal(realm, [chk])

            self.factory = ImaginaryTelnetFactory(realm, p, textserver.TextServer)

            if self.debug:
                self.factory = policies.TrafficLoggingFactory(self.factory, 'telnet')

            self.factory = stats.BandwidthMeasuringFactory(self.factory, 'telnet')
        return self.factory
