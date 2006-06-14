# -*- test-case-name: imaginary.test -*-

"""
Virtual simulation framework.
"""

from imaginary._version import version

# XXX - Okay the reason this is here is that importing action has side-effects
# that are really important.
from imaginary import action
