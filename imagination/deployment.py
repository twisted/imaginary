

def deploy(telnetPort=23, sshPort=22, webPort=80,

           manholePort=9987, manholeUser='admin', manholePassword='password',

           actorTemplate=None,

           **kwargs):

    # Set up an Application and some cred goo
    from twisted.application import service
    from twisted.cred import portal, checkers

    application = service.Application("Imagination")
    svc = service.IServiceCollection(application)

    # Telnet server
    from twisted.application import internet

    from imagination.wiring.telnet import TextFactory

    telnetServer = internet.TCPServer(telnetPort, TextFactory(actorTemplate))
    telnetServer.setServiceParent(svc)

    # SSH server
    from imagination.wiring.ssh import ConchFactory

    conchServer = internet.TCPServer(sshPort, ConchFactory(actorTemplate))
    conchServer.setServiceParent(svc)

    # Web server
    from nevow import appserver, guard, liveevil, inevow
    from imagination.wiring import web

    class AnonRealm:
        def requestAvatar(self, avatarId, mind, *interfaces):
            return inevow.IResource, web.WebPage(actorTemplate), lambda:None

    webServer = internet.TCPServer(
        webPort,
        appserver.NevowSite(
            guard.SessionWrapper(
                portal.Portal(AnonRealm(), (checkers.AllowAnonymousAccess(), )),
                mindFactory=liveevil.LiveEvil))).setServiceParent(svc)

    # Manhole server

    from twisted.manhole import service as mhservice
    from twisted.spread import pb

    mhsvc = mhservice.Service(True)
    #mhsvc.namespace['store'] = st

    mhrealm = mhservice.Realm(mhsvc)
    mhpt = portal.Portal(mhrealm, [
        checkers.InMemoryUsernamePasswordDatabaseDontUse(**{manholeUser: manholePassword})
        ])
    serverFactory = pb.PBServerFactory(mhpt, True)
    manholeServer = internet.TCPServer(manholePort, serverFactory, interface="localhost")
    manholeServer.setServiceParent(svc)

    return application
