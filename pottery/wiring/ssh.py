
from Crypto.PublicKey import RSA

from zope.interface import implements, Interface
from twisted.python.components import backwardsCompatImplements, registerAdapter

from twisted.protocols import basic
from twisted.internet import defer
from twisted.application import internet
from twisted.conch.ssh import factory, userauth, keys, common, session
from twisted.conch.interfaces import IConchUser, ISession
from twisted.conch import avatar
from twisted.cred import portal, credentials

from twisted.conch.insults import insults

from pottery import ipottery
from pottery.wiring import telnet, textserver

class ConchUser(avatar.ConchUser):
    def __init__(self, factory):
        avatar.ConchUser.__init__(self)
        self.factory = factory
        self.channelLookup["session"] = session.SSHSession

registerAdapter(ConchUser, ipottery.IPlayer, IConchUser)

class ConchSession(object):
    implements(session.ISession)

    protocol = staticmethod(
        lambda: insults.ServerProtocol(textserver.TextServer))

    def __init__(self, avatar):
        self.factory = avatar.factory

    def getPty(self, term, windowSize, attrs):
        pass

    def windowChanged(self, newWindowSize):
        pass

    def execCommand(self, proto, cmd):
        raise Exception("no executing commands")

    def eofReceived(self):
        pass

    def closed(self):
        pass

    def openShell(self, transport):
        transport.disconnecting = False
        appProto = self.protocol()
        appProto.factory = self.factory
        appProto.makeConnection(transport)
        transport.makeConnection(session.wrapProtocol(appProto))
backwardsCompatImplements(ConchSession)

registerAdapter(ConchSession, ConchUser, session.ISession)

class UnauthServer(userauth.SSHUserAuthServer):
    def serviceStarted(self):
        userauth.SSHUserAuthServer.serviceStarted(self)
        self.supportedAuthentications = ['none']

    def auth_none(self, packet):
        # return self.portal.login(self.user, None, IConchUser)
        return defer.succeed((IConchUser,
                              ConchUser(self.factory),
                              lambda: None))

class ConchFactory(factory.SSHFactory):
    """
    @ivar realm: A pottery realm (for user creation, probably)

    @ivar portal: A cred Portal through which login will be performed.

    @ivar publicKeys: A dictionary mapping strings describing
    key-types to key data.  Valid keys in this dictionary are:

        'ssh-rsa': An RSA key

    @ivar privateKeys: A dictionary mapping strings describing
    key-types to key data.  Valid keys in this dictionary are the same
    as those in C{publicKeys}.
    """

    def __init__(self, realm, portal, publicKeys, privateKeys):
        self.realm = realm
        self.portal = portal
        self.publicKeys = publicKeys
        self.privateKeys = privateKeys

        server = UnauthServer()
        server.factory = self
        self.services = self.services.copy()
        self.services['ssh-userauth'] = lambda: server

    def login(self, username, password):
        return self.portal.login(
            credentials.UsernamePassword(username, password),
            None,
            ipottery.IPlayer)

    def create(self, username, password):
        return self.realm.create(username, password)

def makeService(realm, port, pubKeyFile=None, privKeyFile=None):
    p = portal.Portal(realm)
    p.registerChecker(realm)

    if pubKeyFile is None or privKeyFile is None:
        key = RSA.generate(1024, common.entropy.get_bytes)

    f = ConchFactory(
        realm, p,
        {"ssh-rsa": keys.getPublicKeyString(data=file(pubKeyFile).read())},
        {"ssh-rsa": keys.getPrivateKeyObject(data=file(privKeyFile).read())})

    netsvc = internet.TCPServer(port, f)

    return netsvc

