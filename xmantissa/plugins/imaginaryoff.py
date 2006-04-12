# -*- test-case-name: imaginary.test -*-

"""
Mantissa Offering Plugin for Imaginary
"""

from xmantissa import offering

from imaginary import iimaginary
from imaginary.wiring import realm, telnet

imaginaryOffering = offering.Offering(
    name = u"imaginary",
    description = u"""
    A Text Adventure!  Kill the dragon!  Kill it!!!
    """,
    siteRequirements = [(iimaginary.ITelnetService, telnet.TelnetService)],
    appPowerups = [realm.ImaginaryRealm],
    benefactorFactories = [],
    loginInterfaces = [],
    themes = [])
