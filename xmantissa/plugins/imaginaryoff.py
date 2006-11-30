# -*- test-case-name: imaginary.test -*-

"""
Mantissa Offering Plugin for Imaginary
"""

from xmantissa import offering

from imaginary import iimaginary
from imaginary.wiring import realm, telnet

siteRequirements = [(iimaginary.ITelnetService, telnet.TelnetService)]
try:
    from imaginary.wiring import ssh
except ImportError:
    pass
else:
    siteRequirements.append((
        iimaginary.ISSHService, ssh.SSHService))

imaginaryOffering = offering.Offering(
    name = u"imaginary",
    description = u"""
    A Text Adventure!  Kill the dragon!  Kill it!!!
    """,
    siteRequirements = siteRequirements,
    appPowerups = [realm.ImaginaryRealm],
    installablePowerups = (),
    benefactorFactories = [],
    loginInterfaces = [(iimaginary.IActor, "Imaginary logins")],
    themes = [])
