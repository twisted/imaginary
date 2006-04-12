from twisted.conch import avatar, interfaces as iconch
from twisted.conch.ssh import session, keys, factory, userauth
from twisted.python import components, failure
from twisted.internet import defer, error
from twisted.cred import credentials, checkers, portal

from imagination.wiring.telnet import ImaginationTextServer
from imagination import simulacrum, containment, iimagination
from imagination.templates import basic
from imagination.text import english

class ImaginationAvatar(avatar.ConchUser):
    def __init__(self, name, actorTemplate):
        avatar.ConchUser.__init__(self)
        self.name = name
        self.actorTemplate = actorTemplate
        self.channelLookup.update({'session' : session.SSHSession})

class ImaginationRealm:
    def __init__(self, actorTemplate):
        self.actorTemplate = actorTemplate

    def requestAvatar(self, avatarId, mind, *interfaces):
        if iconch.IConchUser not in interfaces:
            raise NotImplementedError()
        return (iconch.IConchUser,
                ImaginationAvatar(avatarId, self.actorTemplate),
                lambda: None)

class PromiscuousChecker:
    __implements__ = (checkers.ICredentialsChecker,)

    credentialInterfaces = (credentials.IUsernamePassword,)

    def requestAvatarId(self, credentials):
        return credentials.username

class ImaginationSession:
    def __init__(self, avatar):
        self.avatar = avatar

    def getPty(self, term, windowSize, attrs):
        pass

    def openShell(self, proto):
        ImaginationSessionTransport(proto, self.avatar)

    def execCommand(self, proto, cmd):
        from twisted.conch import error
        raise error.ConchError('cannot execute commands')

    def closed(self):
        pass

components.registerAdapter(ImaginationSession, ImaginationAvatar, session.ISession)

class ImaginationSessionTransport(ImaginationTextServer):
    buf = ''
    closed = False
    mode = "Command"

    def __init__(self, proto, avatar):
        self.proto = proto
        self.avatar = avatar.actorTemplate[
            iimagination.IUI: lambda x: self].fill(
            english.INoun, name=avatar.name).new()
        proto.makeConnection(self)

        proto.outReceived(self.welcomeMessage())
        self.telnet_Command('look')

    def send(self, text):
        if not self.needsPrompt:
            text = '\r\n' + text
        self.needsPrompt = True
        self.proto.outReceived(text)

    def write(self, data):
        # XXX we really need insults for this kind of parsing
        if data == '\x03':
            self.loseConnection()
        data = data.replace('\r', '\r\n')
        self.proto.outReceived(data) # echo
        self.buf += data
        s = self.buf.split('\r\n')
        for line in s[:-1]:
            self.processLine(line.rstrip('\r\n'))
        self.buf = s[-1]

    def loseConnection(self):
        if not self.closed:
            self.closed = True
            self.proto.processEnded(failure.Failure(error.ProcessDone('')))

class ConchFactory(factory.SSHFactory):
    publicKey = 'ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAGEArzJx8OYOnJmzf4tfBEvLi8DVPrJ3/c9k2I/Az64fxjHf9imyRJbixtQhlH9lfNjUIx+4LmrJH5QNRsFporcHDKOTwTTYLh5KmRpslkYHRivcJSkbh/C+BR3utDS555mV'

    publicKeys = {
        'ssh-rsa' : keys.getPublicKeyString(data = publicKey)
    }
    del publicKey

    privateKey = """-----BEGIN RSA PRIVATE KEY-----
MIIByAIBAAJhAK8ycfDmDpyZs3+LXwRLy4vA1T6yd/3PZNiPwM+uH8Yx3/YpskSW
4sbUIZR/ZXzY1CMfuC5qyR+UDUbBaaK3Bwyjk8E02C4eSpkabJZGB0Yr3CUpG4fw
vgUd7rQ0ueeZlQIBIwJgbh+1VZfr7WftK5lu7MHtqE1S1vPWZQYE3+VUn8yJADyb
Z4fsZaCrzW9lkIqXkE3GIY+ojdhZhkO1gbG0118sIgphwSWKRxK0mvh6ERxKqIt1
xJEJO74EykXZV4oNJ8sjAjEA3J9r2ZghVhGN6V8DnQrTk24Td0E8hU8AcP0FVP+8
PQm/g/aXf2QQkQT+omdHVEJrAjEAy0pL0EBH6EVS98evDCBtQw22OZT52qXlAwZ2
gyTriKFVoqjeEjt3SZKKqXHSApP/AjBLpF99zcJJZRq2abgYlf9lv1chkrWqDHUu
DZttmYJeEfiFBBavVYIF1dOlZT0G8jMCMBc7sOSZodFnAiryP+Qg9otSBjJ3bQML
pSTqy7c3a2AScC/YyOwkDaICHnnD3XyjMwIxALRzl0tQEKMXs6hH8ToUdlLROCrP
EhQ0wahUTCk1gKA4uPD6TMTChavbh4K63OvbKg==
-----END RSA PRIVATE KEY-----"""
    privateKeys = {
        'ssh-rsa' : keys.getPrivateKeyObject(data = privateKey)
    }
    del privateKey

    def __init__(self, actorTemplate):
        self.portal = portal.Portal(ImaginationRealm(actorTemplate), [PromiscuousChecker()])
