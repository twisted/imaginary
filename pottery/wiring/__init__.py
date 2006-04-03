
from zope.interface import implements

from twisted.internet import defer
from twisted.application import service
from twisted.python import log, context
from twisted.cred import checkers, credentials, portal

from pottery.commands import Command

# XXX
from pottery import action

from pottery.wiring import telnet, ssh, tuiserver
from pottery import persistence, objects, epottery

def parse(transport, player, line):
    def cbParse(result):
        # transport.write('\r\n> ')
        pass

    def ebParse(err):
        err.trap(epottery.NoSuchCommand)
        # transport.write('Bad command or filename\r\n> ')
        transport.write('Bad command or filename\r\n')

    def ebAmbiguity(err):
        err.trap(epottery.AmbiguousArgument)
        exc = err.value
        if len(exc.objects) == 0:
            transport.write(getattr(err.value.action, err.value.part + "NotAvailable", "Who's that?") + "\r\n")
        else:
            transport.write("Could you be more specific?\r\n")

    def ebUnexpected(err):
        log.err(err)
        # transport.write('\r\nerror\r\n> ')
        transport.write('\r\nerror\r\n')

    player.send(('> ', line, '\n'))
    d = defer.maybeDeferred(Command.parse, player, line)
    d.addCallbacks(cbParse, ebParse)
    d.addErrback(ebAmbiguity)
    d.addErrback(ebUnexpected)
    return d

class PotteryRealm(object):
    implements(portal.IRealm, checkers.ICredentialsChecker)

    def __init__(self, origin):
        self.players = {}
        self.origin = origin
        self.connected = []

    def __setstate__(self, state):
        self.__dict__ = state
        self.connected = []

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['connected']
        return state

    def create(self, username, password):
        p = objects.Player(username.lower())
        p.realm = self
        self.players[username.lower()] = (password, p)
        self.connected.append(p)
        self.origin.add(p)
        return p

    def destroy(self, player):
        del self.players[player.name]

    # IRealm
    def requestAvatar(self, avatarId, mind, *interfaces):
        player = self.players[avatarId][1]
        for iface in interfaces:
            asp = iface(player, None)
            if asp is not None:
                player.moveTo(self.origin)
                self.connected.append(player)
                return (iface, asp, lambda: self.connected.remove(player))
        raise NotImplementedError()

    # ICredentialsChecker
    credentialInterfaces = (credentials.IUsernamePassword,)
    def requestAvatarId(self, credentials):
        u, p = credentials.username, credentials.password
        u = u.lower()
        try:
            if self.players[u][0] == p:
                return u
            raise epottery.BadPassword()
        except KeyError:
            raise epottery.NoSuchUser()

def makeService(
    place,
    sshOptions = {"port": 22,
                  "applicationProtocolFactory": tuiserver.WidgetyServer},
    telnetOptions = {"port": 23,
                     "applicationProtocolFactory": tuiserver.WidgetyServer}):

    msvc = service.MultiService()

    realm = PotteryRealm(place)
    psvc = persistence.PersistenceService('popsicle', realm)
    psvc.setServiceParent(msvc)
    realm = psvc.realm

    ssh.makeService(realm, **sshOptions
                    ).setServiceParent(msvc)

    telnet.makeService(realm, **telnetOptions
                       ).setServiceParent(msvc)


    return msvc
