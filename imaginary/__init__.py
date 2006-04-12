# -*- test-case-name: imaginary.test -*-

"""
Virtual simulation framework.
"""

from epsilon import versions
version = versions.Version(__name__, 0, 0, 0)
del versions

# XXX - Okay the reason this is here is that importing action has side-effects
# that are really important.
from imaginary import action
