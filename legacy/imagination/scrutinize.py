
from zope.interface import implements
from imagination import actions, simulacrum, facets
from imagination.text import english
from pprint import pformat

## This probably needs major refactoring.


class Scrutinizable(facets.Facet):
    implements(english.INoun)
    getComponent = None
    def expressTo(self, who):
        noun = english.INoun(self.original)
        interf = ''
        adapters = self.original
        for interface in adapters:
            adapt = adapters[interface]
            if not hasattr(adapt, '__class__'): continue
            interf += interface
            interf += ': '
            interf += adapt.__class__.__name__
            interf += '\n\t'
            interf += '\n\t'.join(pformat(dict([(key, value) for (key, value) in adapt.__dict__.items() if key is not 'original'])).split('\n'))
            interf += '\n'
        return """You peer closely at the %(name)s...
%(description)s

%(interfaces)s""" % {'name':noun.name, 'description': noun.description, 'interfaces': interf}


class Scrutinize(actions.TargetAction):
    allowNoneInterfaceTypes = []

    target = None
    location = None
    def doAction(self):
        simulacrum.ISeer(self.actor).see(Scrutinizable(self.target.original))

IScrutinizeTarget = english.INoun


class ScrutinizeParser(english.Subparser):
    simpleTargetParsers = {'scrutinize': Scrutinize, 'inspect': Scrutinize}


class Scrutinizeer(facets.Facet):
    implements(IScrutinizeActor)


english.registerSubparser(ScrutinizeParser())
