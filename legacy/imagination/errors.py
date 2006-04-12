# -*- test-case-name: imagination.test -*-

"""
Exception class definitions for Twisted Reality.
"""

class RealityException(Exception):
    """Superclass of all formattable exceptions.
    """

class Nonsense(RealityException):
    """Indicates input that could be made neither heads nor tails of.
    """

class NoSuchObject(RealityException):
    def __init__(self, name):
        RealityException.__init__(self, name)
        self.name = name

class ActionFailed(RealityException):
    """Indicates an action could not be taken.
    """

class ActionRefused(ActionFailed):
    """Indicates an action was refused.
    """

class Refusal(RealityException):
    pass

class LostThing(RealityException):
    pass
