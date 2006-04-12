# -*- test-case-name: reality.test_reality -*-
# system imports
import os
import re

from cStringIO import StringIO

try:
    from new import instance
    from new import instancemethod
except:
    from org.python.core import PyMethod
    instancemethod = PyMethod

# twisted imports
from twisted.python.components import getAdapter, Interface, Adapter, registerAdapter, getAdapterClassWithInheritance
from twisted.python.reflect import qual, namedClass

from twisted.popsicle.mailsicle import getSaver, IHeaderSaver, dictToHeaders, quotify
from twisted.popsicle import freezer

class ThingPersistor(Adapter):
    __implements__ = IHeaderSaver

    def getIndexes(self):
        return [
            ("thing-name", self.original.name.lower())
            ]

    def getItems(self):
        t = self.original
        l = [
            ("Name", t.name),
            ("Location", thingAddress(t.location))
            ]
        desc = t.descriptions
        if len(t.synonyms)>1:
            l.append(("Synonyms", ', '.join(map(quotify, t.synonyms))))

        if len(desc) == 1 and desc.has_key("__MAIN__") and isinstance(desc["__MAIN__"], str):
            if t.description:
                l.append(("Desc",t.description))
        else:
            d2 = desc.copy()
            for k,v in d2.items():
                d2[k] = _fmtObjToStr(v)
            l.append(("Description", dictToHeaders(d2)))
        tl = thingList(t.things)
        if tl:
            l.append(("Contents", tl))
        return l

    def getContinuations(self):
        l = []
        d = {}
        for iface, adapt in self.original._adapterCache.items():
            if d.has_key(adapt):
                d[adapt].append(iface)
            else:
                d[adapt] = [iface]
        for aedapther, ifaces in d.items():
            adapt = getSaver(aedapther, self)
            ll = []
            l.append(ll)
            ll.extend([("Class",qual(aedapther.__class__)),
                       ("Implements", ', '.join(map(qual, ifaces)))
                       ])
            ll.extend(adapt.getItems())
        return l

from reality.thing import Thing
registerAdapter(ThingPersistor, Thing, IHeaderSaver)

def thingAddress(t):
    if t is not None:
        return ('%s <%s>' % (quotify(t.name), freezer.ref(t).acquireOID()))
    else:
        return '<>'

def thingList(l):
    return ', '.join(map(thingAddress, l))

def _fmtObjToStr(o):
    """Only call this from within save() methods.
    
    I convert a TR object to a format string.
    """
    if isinstance(o, str):
        return o
    if isinstance(o, list) or isinstance(o, tuple):
        return ''.join(map(_fmtObjToStr,o))
    if isinstance(o, Thing):
        return "%%{%s}" % freezer.ref(o).acquireOID()
    import types
    if isinstance(o, types.MethodType):
        if isinstance(o.im_self, Thing):
            return "%%{%s.%s}" % (freezer.ref(o.im_self).acquireOID(),
                                   o.im_func.func_name)
        elif isinstance(o.im_self, Adapter):
            orig = o.im_self.original
            adap = o.im_self
            for k, v in o.im_self.original._adapterCache.iteritems():
                if v is adap:
                    break
            else:
                raise NotImplementedError(
                    'TODO: ephemeral adapters that have methods trapped anyway'
                    )
            return "%%{%s:%s.%s}" % (freezer.ref(orig).acquireOID(),
                                      k, o.im_func.func_name)
    # TODO: method types
    raise NotImplementedError("fmt string not implemented for your type", o.__class__)

class _FmtProxy:
    # TODO: this is an object that can "gate" the loading of another... how do
    # we double-defer in order to make the final callback not get called?

    def __init__(self, ref, l):
        self.l = l
        ref().addCallback(self.loaded)
        
    def loaded(self, obj):
        oo = self.getO(obj)
        while 1:
            try:
                dx = self.l.index(self)
            except ValueError:
                break
            self.l[dx] = method

    def getO(self, obj):
        return obj

class _MethodProxy(_FmtProxy):

    def __init__(self, name, ref, l):
        self.name = name
        _FmtProxy.__init__(self, ref, l)

    def getO(self, obj):
        return getattr(obj, self.name)

class _IFaceProxy(_FmtProxy):
    def __init__(self, iface, name, ref, l):
        self.name = name
        self.iface = iface
        _FmtProxy.__init__(self, ref, l)

    def getO(self, obj):
        return obj.getAdapter(namedClass(self.iface)) # or some shit.... stopped here

def _strToFmtObj(s, repo):
    l = re.split(r'(?:^|[^%])%{(.*?)}',s) # find %{foo} but don't find %%{foo}
    parsed = False
    fmtobj = []
    for s in l:
        if parsed:
            if s.count(":"):
                oid, rest = s.split(":")
                names = rest.split(".")
                interface = '.'.join(names[:-1])
                method = names[-1]
                fmtobj.append(freezer.ref(oid, repo))
            elif s.count("."):
                oid, method = s.split(".")
                
        else:
            fmtobj.append(s)
        parsed = not parsed
    return l



class WearPersistor(Adapter):
    __implements__ = IHeaderSaver

    def getItems(self):
        l = []
        if (self.original.clothingSlots is not
            self.original.__class__.__dict__.get('clothingSlots')):
            l.append(("Clothing-Slots", ', '.join(self.original.clothingSlots)))
        if self.original.wearer is not None:
            l.append(("Wearer", thingAddress(self.original.wearer)))
        if self.original.clothingAppearance is not None:
            l.append(("Clothing-Appearance", _fmtObjToStr(self.original.clothingAppearance)))
        return l

from reality.clothing import Wearable
registerAdapter(WearPersistor, Wearable, IHeaderSaver)

class PortaPersistor(Adapter):
    __implements__ = IHeaderSaver
    def getItems(self):
        a = self.original
        return [("Weight", str(a.weight)),
                ("Bulk", str(a.bulk))]

from reality.player import Portable
registerAdapter(PortaPersistor, Portable, IHeaderSaver)

class NoInfo(Adapter):
    __implements__ = IHeaderSaver
    def getItems(self):
        return []

    def loadItems(self, items, toplevel):
        self.original.__init__(toplevel)

from reality.phrase import Parsing
registerAdapter(NoInfo, Parsing, IHeaderSaver)

from reality.container import OpenableContainer, ContainerAdapter
registerAdapter(NoInfo, OpenableContainer, IHeaderSaver)

registerAdapter(NoInfo, ContainerAdapter, IHeaderSaver)
