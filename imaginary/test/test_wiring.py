
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
        # XXX This is too many stores for a unit test to need to create.
        siteStore = Store(filesdir=FilePath(self.mktemp()))
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
        proto = app.buildTerminalProtocol(viewer)
        self.assertIdentical(proto.world, world)
        self.assertEqual(proto.role.externalID, u'alice@example.com')
        self.assertEqual(proto.choices, [])
