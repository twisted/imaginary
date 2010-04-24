
"""
Some basic unit tests for L{imaginary.idea} (but many tests for this code are in
other modules instead).
"""

from zope.interface import implements

from twisted.trial.unittest import TestCase

from epsilon.structlike import record

from imaginary.iimaginary import IWhyNot, INameable, ILinkContributor
from imaginary.language import ExpressString
from imaginary.idea import Idea, Link, Path, AlsoKnownAs, ProviderOf, Named, DelegatingRetriever


class Reprable(record('repr')):
    def __repr__(self):
        return self.repr


class PathTests(TestCase):
    """
    Tests for L{imaginary.idea.Path}.
    """
    def test_repr(self):
        """
        A L{Path} instance can be rendered into a string by C{repr}.
        """
        bottle = Idea(AlsoKnownAs("bottle"))
        table = Idea(AlsoKnownAs("table"))
        hall = Idea(AlsoKnownAs("hall"))
        path = Path([Link(hall, table), Link(table, bottle)])
        self.assertEquals(
            repr(path),
            "Path(\n"
            "\t'hall' => 'table' []\n"
            "\t'table' => 'bottle' [])")


    def test_unnamedDelegate(self):
        """
        The I{repr} of a L{Path} containing delegates without names includes the
        I{repr} of the delegates.
        """
        bottle = Idea(Reprable("bottle"))
        table = Idea(Reprable("table"))
        hall = Idea(Reprable("hall"))
        path = Path([Link(hall, table), Link(table, bottle)])
        self.assertEquals(
            repr(path),
            "Path(\n"
            "\thall => table []\n"
            "\ttable => bottle [])")



class OneLink(record('link')):
    implements(ILinkContributor)

    def links(self):
        return [self.link]


class TooHigh(object):
    implements(IWhyNot)

    def tellMeWhyNot(self):
        return ExpressString("the table is too high")


class Reachable(DelegatingRetriever):
    def moreObjectionsTo(self, path, result):
        named = path.targetAs(INameable)
        if named.knownTo(None, "bottle"):
            return [TooHigh()]
        return []


class IdeaTests(TestCase):
    """
    Tests for L{imaginary.idea.Idea}.
    """
    def test_something(self):
        bottle = Idea(AlsoKnownAs("bottle"))
        table = Idea(AlsoKnownAs("table"))
        hall = Idea(AlsoKnownAs("hall"))
        alice = Idea(AlsoKnownAs("alice"))

        alice.linkers.append(OneLink(Link(alice, hall)))
        hall.linkers.append(OneLink(Link(hall, table)))
        table.linkers.append(OneLink(Link(table, bottle)))

        # XXX The last argument is the observer, and is supposed to be an
        # IThing.
        retriever = Named("bottle", ProviderOf(INameable), alice)

        # Sanity check.  Alice should be able to reach the bottle if we don't
        # restrict things based on her height.
        self.assertEquals(list(alice.obtain(retriever)), [bottle.delegate])

        # But when we consider how short she is, she should not be able to reach
        # it.
        results = alice.obtain(Reachable(retriever))
        self.assertEquals(list(results), [])
