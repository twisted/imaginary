from twisted.trial import unittest

from twisted.internet import defer

from imagination import actions, errors, simulacrum, iimagination, social
from imagination import iimagination, containment, facets
from imagination.templates import basic

class TestUI(facets.Facet):

    def __init__(self, original):
        facets.Facet.__init__(self, original)
        self.events = []

    def presentMenu(self, list, typename=None):
        #I don't even know what this means!
        pass

    def presentEvent(self, iface, event):
        self.events.append((iface, event))


SenseActor = basic.Actor[
    iimagination.IUI: TestUI,
    social.ISayActor: facets.Facet]

from imagination.text.english import INoun

class TestSenses(unittest.TestCase):

    def setUp(self):
        self.room = basic.Room.fill(INoun,name="Room").new()
        self.speaker = SenseActor.fill(INoun,name="Speaker").new()
        self.listener = SenseActor.fill(INoun,name="Listener").new()
        containment.ILocatable(self.speaker).location = self.room
        containment.ILocatable(self.listener).location = self.room

    def test_say(self):
        social.Say(self.speaker, "haha you suck").doAction()
        self.assertIn((simulacrum.IHearer, (social.ISayActor(self.speaker), ' says, "', "haha you suck", '"')), iimagination.IUI(self.listener).events)
