
from twisted.cred import error

# Authentication errors
class BadPassword(error.UnauthorizedLogin):
    pass

class NoSuchUser(error.UnauthorizedLogin):
    pass


# Base Pottery error
class PotteryError(Exception):
    pass


# Input handling errors
class NoSuchCommand(PotteryError):
    """
    There is no command like the one you tried to execute.
    """

class AmbiguousArgument(PotteryError):
    """
    One or more of the inputs specified can not be narrowed down to
    just one thing.  This can be due to the presence of multiple
    things with similar names, or due to the absence of anything named
    similarly to the given input.

    @type part: C{str}
    @ivar part: The part of the command which was ambiguous.
    Typically something like 'target' or 'tool'.

    @type objects: C{list} of C{IObject}
    @ivar objects: The objects which were involved in the ambiguity.
    """

    def __init__(self, part, objects):
        PotteryError.__init__(self)
        self.part = part
        self.objects = objects

# Game logic errors
class DoesntFit(PotteryError):
    """
    An object tried to go into a container, but the container was
    full.
    """
