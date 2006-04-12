# -*- test-case-name: imagination.test -*-

from zope.interface import Interface, interface, adapter, implements, declarations

registry = adapter.AdapterRegistry()

def registerAdapter(adapterFactory, origInterface, *interfaceClasses):
    
    """Total ripoff of twisted.python.components.registerAdapter.  I
    just didn't want to lug all that history into our nice shiny new
    components system..."""

    
    self = registry
    assert interfaceClasses, "You need to pass an Interface"
    # deal with class->interface adapters:
    if not isinstance(origInterface, interface.InterfaceClass):
        origInterface = declarations.implementedBy(origInterface)

    for interfaceClass in interfaceClasses:
        factory = self.get(origInterface).selfImplied.get(interfaceClass, {}).get('')
        if factory:
            raise ValueError("an adapter (%s) was already registered." % (factory, ))
    for interfaceClass in interfaceClasses:
        self.register([origInterface], interfaceClass, '', adapterFactory)

def _hook(iface, ob, lookup=registry.lookup1):
    factory = lookup(declarations.providedBy(ob), iface)
    if factory is None:
        return None
    else:
        return factory(ob)

interface.adapter_hooks.append(_hook)
_nope = object()

class IReprable(Interface):
    def __str__():
        """Format this Faceted nicely as a string.
        """
    
class Faceted(dict):
    __slots__ = ()

    def __conform__(self, interface):
        if self.has_key(interface):
            return self[interface]
        else:
            adapter = registry.queryAdapter(
                self, interface, default=_nope)
            if adapter is _nope:
                return None
            else:
                self[interface] = adapter
                return adapter

    def __repr__(self):
        s = IReprable(self, None)
        if s is None:
            return str(self)
        return '<Faceted %r>' % (s,)

    def __str__(self):
        return 'Faceted(' + super(Faceted, self).__repr__() + ')'

class Facet(object):
    def __init__(self, original):
        self.original = original

    def __conform__(self, interface):
        return self.original.__conform__(interface)

#this one is fzzzy's fault
def isid(one, other):
    while hasattr(one, 'original'):
        one = one.original
    while hasattr(other, 'original'):
        other = other.original
    return one is other
                
