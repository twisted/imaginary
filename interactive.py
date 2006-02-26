
from imagination.iimagination import IUI
from imagination.text.english import IThinker

__metaclass__ = type

class Event:
    def __init__(self, iface, event):
        self.iface, self.event = iface, event

class Command:
    def __init__(self, text):
        self.text = text

class Menu:
    def __init__(self, choices):
        self.choices = choices
        self.choice = None


class ActorWrapper(components.Adapter):
    __implements__ = IUI, IThinker

    def install(self, actor):
        self.ui = IUI(actor)
        # IComponentized(actor)
        self.ui.original.setComponent(IUI, self)
        self.thinker = IThinker(actor)
        self.thinker.original.setComponent(IThinker, self)
        self.happenings = []


    def uninstall(self):
        self.ui.original.setComponent(IUI, self.ui)
        self.ui.original.setComponent(IThinker, self.thinker)

    def save(self):
        # XXX How should this save stuff? At first, I was thinking I'd
        # want to serialize the event objects straight-up, but I think
        # I might just save the result of express() instead, and
        # basically this thing will turn into a transcript
        # auto-saver...
        raise "argh"
    

    # IUI

    def presentEvent(self, eventInterface, event):
        self.happenings.append(Event(eventInterface, event))
        self.ui.presentEvent(eventInterface, event)

    def presentMenu(self, items, typename=None):
        # XXX Potential problem here: If we receive an event before
        # the user gets around to making a choice, things will
        # probably blow up
        d = self.ui.presentMenu(items, typename)
        menu = Menu(items)
        self.happenings.append(menu)
        d.addCallback(self._gotChoice, menu)
        return d

    def _gotChoice(self, choice, menu):
        menu.choice = choice
        return choice


    # IThinker

    def recognizes(self, name):
        return self.thinker.recognizes(name)

    def parse(self, text):
        self.happenings.append(Command(text))
        return self.thinker.parse(text)

