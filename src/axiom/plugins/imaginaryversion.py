# Copyright 2008 Divmod, Inc.
# See LICENSE file for details

"""
Register an Axiom version plugin for Imaginary.
"""

from zope.interface import directlyProvides
from twisted.plugin import IPlugin
from axiom.iaxiom import IVersion
from imaginary import version
directlyProvides(version, IPlugin, IVersion)
