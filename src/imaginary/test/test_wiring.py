
"""
Tests for L{imaginary.wiring}

These tests are not particularly good at the moment.  They are, however, a
minor step up from nothing.
"""

from zope.interface.verify import verifyObject

from twisted.trial.unittest import TestCase
from twisted.python.filepath import FilePath

from axiom.store import Store
from axiom.dependency import installOn
from axiom.userbase import LoginSystem, getAccountNames

from xmantissa.ixmantissa import ITerminalServerFactory
from xmantissa.offering import installOffering
from xmantissa.terminal import _AuthenticatedShellViewer
from axiom.plugins.mantissacmd import Mantissa

from imaginary.world import ImaginaryWorld
from imaginary.wiring.textserver import ImaginaryApp
from xmantissa.plugins.imaginaryoff import imaginaryOffering
from twisted.test.proto_helpers import StringTransport
from twisted.conch.insults.insults import ServerProtocol

from characteristic import attributes

@attributes("proto world".split())
class TestWorld(object):
    """
    A fixture for testing a terminal protcol.
    """



def buildWorld(testCase):
    """
    Build a L{TestWorld}.
    """
    # XXX This is too many stores for a unit test to need to create.
    siteStore = Store(filesdir=FilePath(testCase.mktemp()))
    Mantissa().installSite(siteStore, u'example.com', u'', False)
    installOffering(siteStore, imaginaryOffering, {})
    login = siteStore.findUnique(LoginSystem)
    account = login.addAccount(u'alice', u'example.com', u'password')
    userStore = account.avatars.open()

    app = ImaginaryApp(store=userStore)
    installOn(app, userStore)

    imaginary = login.accountByAddress(u'Imaginary', None).avatars.open()
    world = imaginary.findUnique(ImaginaryWorld)

    # Alice connects to her own ImaginaryApp (all that is possible at the
    # moment).
    viewer = _AuthenticatedShellViewer(getAccountNames(userStore))
    return TestWorld(proto=app.buildTerminalProtocol(viewer),
                     world=world)



class ImaginaryAppTests(TestCase):
    """
    Tests for L{ImaginaryApp}, which provides access to Imaginary via
    L{ShellServer}, the top-level Mantissa SSH handler.
    """
    def test_interface(self):
        """
        L{ImaginaryApp} implements L{ITerminalServerFactory}
        """
        self.assertTrue(verifyObject(ITerminalServerFactory, ImaginaryApp()))


    def test_powerup(self):
        """
        L{installOn} powers up the target for L{ITerminalServerFactory} with
        L{ImaginaryApp}.
        """
        store = Store()
        app = ImaginaryApp(store=store)
        installOn(app, store)
        self.assertIdentical(ITerminalServerFactory(store), app)


    def test_buildTerminalProtocol(self):
        """
        L{ImaginaryApp.buildTerminalProtocol} returns a
        L{CharacterSelectionTextServer} instance with a role representing the
        store it is in, a reference to the L{ImaginaryWorld} installed on the
        Imaginary application store, and a list of L{Thing} items shared to the
        role.
        """
        testWorld = buildWorld(self)
        self.assertIdentical(testWorld.proto.world, testWorld.world)
        self.assertEqual(testWorld.proto.role.externalID, u'alice@example.com')
        self.assertEqual(testWorld.proto.choices, [])


    def test_connectionMadePrompt(self):
        """
        L{CharacterSelectionTextServer} prompts the player upon connection,
        giving them the option to create a character.
        """
        testWorld = buildWorld(self)
        transport = StringTransport()
        terminal = ServerProtocol(lambda: testWorld.proto)
        terminal.makeConnection(transport)
        self.assertIn("0) Create", transport.io.getvalue())
