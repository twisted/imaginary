
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
        key = Idea(AlsoKnownAs("key"))
        table = Idea(AlsoKnownAs("table"))
        hall = Idea(AlsoKnownAs("hall"))
        path = Path([Link(hall, table), Link(table, key)])
        self.assertEquals(
            repr(path),
            "Path(\n"
            "\t'hall' => 'table' []\n"
            "\t'table' => 'key' [])")


    def test_unnamedDelegate(self):
        """
        The I{repr} of a L{Path} containing delegates without names includes the
        I{repr} of the delegates.
        """
        key = Idea(Reprable("key"))
        table = Idea(Reprable("table"))
        hall = Idea(Reprable("hall"))
        path = Path([Link(hall, table), Link(table, key)])
        self.assertEquals(
            repr(path),
            "Path(\n"
            "\thall => table []\n"
            "\ttable => key [])")



class OneLink(record('link')):
    implements(ILinkContributor)

    def links(self):
        return [self.link]


class TooHigh(object):
    implements(IWhyNot)

    def tellMeWhyNot(self):
        return ExpressString("the table is too high")


class ArmsReach(DelegatingRetriever):
    """
    Restrict retrievable to things within arm's reach.

        alas for poor Alice! when she got to the door, she found he had
        forgotten the little golden key, and when she went back to the table for
        it, she found she could not possibly reach it:
    """
    def moreObjectionsTo(self, path, result):
        """
        Object to finding the key.
        """
        # This isn't a very good implementation of ArmsReach.  It doesn't
        # actually check distances or paths or anything.  It just knows the
        # key is on the table, and Alice is too short.
        named = path.targetAs(INameable)
        if named.knownTo(None, "key"):
            return [TooHigh()]
        return []


class IdeaTests(TestCase):
    """
    Tests for L{imaginary.idea.Idea}.
    """
    def test_objections(self):
        """
        The L{IRetriver} passed to L{Idea.obtain} can object to certain results.
        This excludes them from the result returned by L{Idea.obtain}.
        """
        key = Idea(AlsoKnownAs("key"))
        table = Idea(AlsoKnownAs("table"))
        hall = Idea(AlsoKnownAs("hall"))
        alice = Idea(AlsoKnownAs("alice"))

        alice.linkers.append(OneLink(Link(alice, hall)))
        hall.linkers.append(OneLink(Link(hall, table)))
        table.linkers.append(OneLink(Link(table, key)))

        # XXX The last argument is the observer, and is supposed to be an
        # IThing.
        retriever = Named("key", ProviderOf(INameable), alice)

        # Sanity check.  Alice should be able to reach the key if we don't
        # restrict things based on her height.
        self.assertEquals(list(alice.obtain(retriever)), [key.delegate])

        # But when we consider how short she is, she should not be able to reach
        # it.
        results = alice.obtain(ArmsReach(retriever))
        self.assertEquals(list(results), [])
