# -*- test-case-name: imaginary.test.test_wiring -*-

from zope.interface import implements

from twisted.python.components import registerAdapter
from twisted.internet import defer
from twisted.protocols import policies
from twisted.conch.ssh import factory, userauth, keys, session
from twisted.conch.interfaces import IConchUser
from twisted.conch import avatar
from twisted.cred import portal, credentials, checkers

from twisted.conch.insults import insults
from twisted.conch.scripts import ckeygen

from axiom import item, attributes, userbase

from xmantissa.ixmantissa import IProtocolFactoryFactory
from xmantissa import stats

from imaginary import iimaginary
from imaginary.wiring import textserver

class ConchUser(avatar.ConchUser):
    def __init__(self, factory):
        avatar.ConchUser.__init__(self)
        self.factory = factory
        self.channelLookup["session"] = session.SSHSession

registerAdapter(ConchUser, iimaginary.IActor, IConchUser)

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
    @ivar realm: A imaginary realm (for user creation, probably)

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
            iimaginary.IActor)


    def create(self, username, password):
        return self.realm.create(username, password)


    def loggedIn(self, avatar):
        return self.realm.loggedIn(avatar)



class SSHService(item.Item):
    implements(IProtocolFactoryFactory, iimaginary.ISSHService)

    powerupInterfaces = (IProtocolFactoryFactory, iimaginary.ISSHService)

    publicKeyFile = attributes.path(doc="""
    Path to a file containing a public key for this SSH server.
    """, allowNone=False)

    privateKeyFile = attributes.path(doc="""
    Path to a file containing a private key for this SSH server.
    """, allowNone=False)

    # A cred portal, a Twisted TCP factory and a IListeningPort.
    portal = attributes.inmemory()
    factory = attributes.inmemory()

    # When enabled, toss all traffic into logfiles.
    debug = False

    def __init__(self, **kw):
        store = kw['store']
        if 'publicKeyFile' not in kw:
            privateKeyFile = store.newFilePath('ssh', 'ssh_key')
            publicKeyFile = privateKeyFile.sibling('ssh_key.pub')
            tmp = privateKeyFile.temporarySibling()

            privateKeyFile.parent().makedirs()

            # XXX oh god oh god oh god :(
            ckeygen.generateRSAkey({
                'bits': 1024,
                'filename': tmp.path,
                'pass': 'no passphrase'})
            tmp.moveTo(privateKeyFile)
            tmp.sibling(tmp.basename() + '.pub').moveTo(publicKeyFile)

            kw['privateKeyFile'] = privateKeyFile
            kw['publicKeyFile'] = publicKeyFile
        super(SSHService, self).__init__(**kw)


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

            self.factory = ConchFactory(
                realm, p,
                {"ssh-rsa": keys.getPublicKeyString(data=self.publicKeyFile.open().read())},
                {"ssh-rsa": keys.getPrivateKeyObject(data=self.privateKeyFile.open().read(), passphrase='no passphrase')})

            if self.debug:
                self.factory = policies.TrafficLoggingFactory(self.factory, 'ssh')

            self.factory = stats.BandwidthMeasuringFactory(self.factory, 'ssh')
        return self.factory
