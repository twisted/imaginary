
from twisted.internet import protocol
from twisted.cred import credentials, portal
from twisted.application import internet
from twisted.protocols import policies

from twisted.conch import telnet
from twisted.conch.insults import insults

from pottery import ipottery
from pottery.wiring import textserver

class PotteryTelnetFactory(protocol.ServerFactory):
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
            ipottery.IPlayer)

    def create(self, username, password):
        return self.realm.create(username, password)

def makeService(realm, port, applicationProtocolFactory=textserver.TextServer, debug=True):
    p = portal.Portal(realm)
    p.registerChecker(realm)

    factory = PotteryTelnetFactory(realm, p, applicationProtocolFactory)

    if debug:
        factory = policies.TrafficLoggingFactory(factory, 'telnet')

    netsvc = internet.TCPServer(port, factory)

    return netsvc
