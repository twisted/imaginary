
"""
Some basic unit tests for L{imaginary.idea} (but many tests for this code are in
other modules instead).
"""

from twisted.trial.unittest import TestCase

from epsilon.structlike import record

from imaginary.idea import Idea, Link, Path


class Named(record('name')):
    pass


class PathTests(TestCase):
    """
    Tests for L{imaginary.idea.Path}.
    """
    def test_repr(self):
        """
        A L{Path} instance can be rendered into a string by C{repr}.
        """
        monitor = Idea(Named("monitor"))
        desk = Idea(Named("desk"))
        office = Idea(Named("office"))
        path = Path([Link(office, desk), Link(desk, monitor)])
        self.assertEquals(
            repr(path),
            "Path(\n"
            "\t'office' => 'desk' []\n"
            "\t'desk' => 'monitor' [])")
