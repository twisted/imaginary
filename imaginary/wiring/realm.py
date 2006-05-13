# -*- test-case-name: imaginary.test -*-

from zope.interface import implements

from twisted.python import log
from twisted.cred import checkers, credentials, portal

from axiom import iaxiom, item, attributes

from imaginary import iimaginary
from imaginary import objects, eimaginary


class PlayerCredentials(item.Item):
    """
    An association of a set of login credentials with a game object.
    """
    username = attributes.text(doc="""
    The username of the user. Such as: carmstro1243
    """, allowNone=False, caseSensitive=False)

    password = attributes.text(doc="""
    The password of the user!  Oh man can you believe it?
    """, allowNone=False)

    actor = attributes.reference(doc="""
    A reference to the L{objects.Thing} with which these credentials are
    associated.
    """, whenDeleted=attributes.reference.CASCADE)



class ImaginaryRealm(item.Item, item.InstallableMixin):
    implements(portal.IRealm, checkers.ICredentialsChecker)

    origin = attributes.reference(doc="""
    The location where new players enter the world.
    """)

    connected = attributes.inmemory(doc="""
    A list of player L{objects.Thing} which are currently associated with a
    network connection.
    """)

    installedOn = attributes.reference(doc="""
    The item on which this realm is installed.
    """)


    def __init__(self, **kw):
        super(ImaginaryRealm, self).__init__(**kw)
        self.origin = objects.Thing(store=self.store, name=u"The Place")
        objects.Container(store=self.store,
                          capacity=1000).installOn(self.origin)


    def installOn(self, other):
        super(ImaginaryRealm, self).installOn(other)
        other.powerUp(self, portal.IRealm)
        other.powerUp(self, checkers.ICredentialsChecker)


    def activate(self):
        self.connected = []


    def create(self, username, password, **kw):
        from imaginary import garments
        playerObj = objects.Thing(store=self.store,
                                  weight=100,
                                  name=username,
                                  proper=True, **kw)
        objects.Container(store=self.store, capacity=10).installOn(playerObj)
        objects.Actor(store=self.store).installOn(playerObj)
        PlayerCredentials(
            store=self.store,
            username=username,
            password=password,
            actor=playerObj)
        iimaginary.IContainer(self.origin).add(playerObj)
        wearer = garments.Wearer(store=self.store)
        wearer.installOn(playerObj)
        return playerObj


    def loggedIn(self, actor):
        self.connected.append(actor)


    # IRealm
    def requestAvatar(self, avatarId, mind, *interfaces):
        actor = self.store.query(PlayerCredentials, PlayerCredentials.username == avatarId).getColumn("actor").next()
        for iface in interfaces:
            asp = iface(actor, None)
            if asp is not None:
                log.msg(
                    name='cred',
                    interface=iaxiom.IStatEvent,
                    cred_interface=iface)
                actor.moveTo(self.origin)
                self.loggedIn(actor)
                return (iface, asp, lambda: self.connected.remove(actor))
        raise NotImplementedError()


    # ICredentialsChecker
    credentialInterfaces = (credentials.IUsernamePassword,)
    def requestAvatarId(self, credentials):
        u, p = credentials.username, credentials.password
        for creds in self.store.query(PlayerCredentials,
                                      PlayerCredentials.username == u):
            if creds.password != p:
                raise eimaginary.BadPassword()
            return credentials.username
        raise eimaginary.NoSuchUser()
