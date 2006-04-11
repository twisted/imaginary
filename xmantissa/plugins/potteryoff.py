# -*- test-case-name: pottery.test -*-

"""
Mantissa Offering Plugin for Pottery
"""

from xmantissa import offering

from pottery import ipottery
from pottery.wiring import realm, telnet

potteryOffering = offering.Offering(
    name = u"pottery",
    description = u"""
    A Text Adventure!  Kill the dragon!  Kill it!!!
    """,
    siteRequirements = [(ipottery.ITelnetService, telnet.TelnetService)],
    appPowerups = [realm.PotteryRealm],
    benefactorFactories = [],
    loginInterfaces = [],
    themes = None)
