# -*- test-case-name:reality.test_reality -*-

from twisted.python import components

class RealityException(Exception):
    """RealityException()

    This is the base superclass of all formattable exceptions.
    """
##     def __init__(self, *args):
##         components.Componentized.__init__(self)
##         Exception.__init__(self, *args)

class Nonsense(RealityException):
    """
    This exception is raised when what the player types makes no damn sense to
    the game at all.
    """

class NoSuchObject(RealityException):
    def __init__(self, name):
        RealityException.__init__(self, name)
        self.name = name

class ActionFailed(RealityException):
    """
    """

class ActionRefused(ActionFailed):
    """
    """
