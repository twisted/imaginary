
import copy


from imagination.text import english
from imagination import containment
from imagination import errors
from imagination import simulacrum


class Describe(object):
    target = None
    splitter = ' as '
    def __init__(self, actor, text):
        self.actor = actor
        self.text = text

    def getAmbiguities(self):
        if self.splitter in self.text:
            what, self.rest = self.text.split(self.splitter, 1)
            found = list(
                simulacrum.lookFor(
                    self.actor, what, lambda it, *args, **kw: it))
            if len(found) == 1:
                self.target = found[0][1]
                return []
            return [('Target', [it for (_, it) in found])]
        raise errors.Refusal(
            'Syntax is "%s <dobj> %s <description>.' % (
                self.__class__.__name__, self.splitter))

    def isPlaceholder(self):
        return False

    def setImplementor(self, iface, thing):
        self.target = thing

    def performAction(self):
        english.INoun(self.target).description = self.rest
        simulacrum.ISeer(self.actor).see("Described.")


class Rename(Describe):
    splitter = ' to '
    def performAction(self):
        english.INoun(self.target).name = self.rest
        simulacrum.ISeer(self.actor).see("Renamed.")


class Create(Describe):
    splitter = ' named '
    def performAction(self):
        ## This is probably not the way to do this!!!
        newCopy = copy.deepcopy(self.target.original)
        english.INoun(newCopy).name = self.rest
        containment.ILocatable(newCopy).location = self.actor


class BuildingParser(english.Subparser):
    def parse_describe(self, actor, text):
        return [Describe(actor, text)]

    def parse_rename(self, actor, text):
        return [Rename(actor, text)]

    def parse_create(self, actor, text):
        return [Create(actor, text)]


english.registerSubparser(BuildingParser())
