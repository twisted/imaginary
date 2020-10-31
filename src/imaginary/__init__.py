# -*- test-case-name: imaginary,examplegame -*-

"""
Virtual simulation framework.
"""

# Verbs are only registered when they are imported, and important verbs are
# found in the following modules:
from imaginary import action, creation
action                          # exported
creation                        # exported


# Ideally there would be a nice, passive way to register verbs which would only
# load them as necessary rather than forcing the entire package to get
# imported, but this will work okay for now.

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
