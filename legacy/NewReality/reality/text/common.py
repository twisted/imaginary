# -*- test-case-name: reality.test_reality -*-
"""
Common linguistic patterns.

This is a baseline for interfaces implementing the Sapir-Whorf RFC.
"""


from twisted.python import components

class IConcept(components.Interface):
    """An abstract concept that can be expressed in some language.
    """

    def getLanguage(self):
        """Return a brief string identifier of the language this concept is in.
        """

    def expressTo(self, observer):
        """
        Return a string or unicode object that expresses this concept in some
        language.
        """

class IDescribeable(IConcept):
    def describe(self, component, text, priority=1):
        """Describe a facet of this object with some text in my native language.
        """

    def explainTo(self, observer):
        """Return a long description of this object.
        """

class INoun(IConcept):
    """A concept describing something that is persistent.
    
    @type name: C{str}
    @ivar name: A simple string describing this noun.
    """
    def knownAs(self, name, observer):
        """Determine whether the given name refers to this object.
        """
    
    def changeName(self, newname):
        """Change the name which refers to this object.
        """

class IThinker(components.Interface):
    """A person who can think in this language.
    """



# Utilities.

import operator

def express(tup, obs, iface=IConcept):
    if isinstance(tup, str):
        return tup
    if (isinstance(tup, components.Componentized) or
        isinstance(tup, components.Adapter)):
        c = tup.getComponent(iface)
        if c is None:
            raise Exception(tup,obs,iface)
        return c.expressTo(obs)
    if (isinstance(tup, tuple) or isinstance(tup, list)):
        l = [express(t, obs, iface) for t in tup]
        if l:
            return reduce(operator.add, l)
        else:
            return ''
    if tup is None:
        return ''
    return components.getAdapter(tup, iface, adapterClassLocator=components.getAdapterClassWithInheritance).expressTo(obs)

