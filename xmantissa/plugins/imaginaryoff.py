# -*- test-case-name: imaginary.test -*-

"""
Mantissa Offering Plugin for Imaginary
"""

from xmantissa import offering

from imaginary import iimaginary
from imaginary.wiring import realm, telnet, ssh

imaginaryOffering = offering.Offering(
    name = u"imaginary",
    description = u"""
    A Text Adventure!  Kill the dragon!  Kill it!!!
    """,
    siteRequirements = [(iimaginary.ITelnetService, telnet.TelnetService),
                        (iimaginary.ISSHService, ssh.SSHService)],
    appPowerups = [realm.ImaginaryRealm],
    benefactorFactories = [],
    loginInterfaces = [(iimaginary.IActor, "Imaginary logins")],
    themes = [])
