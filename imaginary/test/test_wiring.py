
"""
Tests for L{imaginary.wiring}

These tests are not particularly good at the moment.  They are, however, a
minor step up from nothing.
"""

from twisted.trial.unittest import TestCase
from twisted.internet.protocol import ServerFactory

from axiom.store import Store
from axiom.dependency import installOn

from imaginary.wiring.telnet import TelnetService
from imaginary.wiring.ssh import SSHService


class TelnetTests(TestCase):
    """
    Tests for L{imaginary.wiring.telnet}
    """
    def setUp(self):
        self.dbdir = self.mktemp()
        self.store = Store(self.dbdir)


    def test_serviceCreation(self):
        """
        Test that L{TelnetService} can at least be instantiated.
        """
        service = TelnetService(store=self.store)


    def test_getFactory(self):
        """
        Test that L{TelnetService.getFactory} returns a Twisted server factory.
        """
        service = TelnetService(store=self.store)
        installOn(service, self.store)
        factory = service.getFactory()
        self.failUnless(isinstance(factory, ServerFactory))
    test_getFactory.todo = "TelnetService needs to do something with dependency declarations."



class SSHTests(TestCase):
    """
    Tests for L{imaginary.wiring.ssh}
    """
    def setUp(self):
        self.dbdir = self.mktemp()
        self.store = Store(self.dbdir)


    def test_serviceCreation(self):
        """
        Test that L{SSHService} can at least be instantiated.
        """
        service = SSHService(store=self.store)


    def test_getFactory(self):
        """
        Test that L{SSHService.getFactory} returns a Twisted server factory.
        """
        service = SSHService(store=self.store)
        installOn(service, self.store)
        factory = service.getFactory()
        self.failUnless(isinstance(factory, ServerFactory))
    test_getFactory.todo = "SSHService needs to do something with dependency declarations."
