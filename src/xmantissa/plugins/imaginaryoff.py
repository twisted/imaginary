# -*- test-case-name: imaginary.test -*-

"""
Mantissa Offering Plugin for Imaginary
"""

from xmantissa import offering

from imaginary.world import ImaginaryWorld
from imaginary.wiring.textserver import ImaginaryApp

imaginaryOffering = offering.Offering(
    name = u"imaginary",
    description = u"""
    A simulation framework for text adventures.
    """,
    siteRequirements = [],
    appPowerups = [ImaginaryWorld],
    installablePowerups = [
        (u"Imaginary Game", u"A text adventure of some variety.",
         ImaginaryApp)],
    loginInterfaces = [],
    themes = [])


