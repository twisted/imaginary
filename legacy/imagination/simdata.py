# -*- test-case-name: imagination.test -*-
import os, types

from twisted.python import  reflect, log, util as tputil
from imagination.facets import Faceted

__metaclass__ = type


def lazy(adapter, kw):
    def doLazyAdapt(original):
        return adapter(original, **kw)
    return doLazyAdapt


def lazyApply(interface, methodName, args, kw):
    def doLazyApply(original):
        component = interface(original)
        return getattr(component, methodName)(*args, **kw)
    return doLazyApply


class ThingTemplate:
    """
    A facilitate creation of templates. Do something like this.

    SomeThing = thingTemplateInstance[
        IFoo: iFooAdapterFactory,
        (IBar, IBaz): wrc(iMultiFactory, arg1, arg2),
        ]
    # 'template' will then be a callable object
    someThing = SomeThing()
    IFoo(someThing) -> iFooAdapter
    """

    ObjectFactory = Faceted

    def __init__(self, templateList=None, templateMap=None, order=None):
        """Create a new template.

        @param templateList: A list of two-tuples.  The first element
        of each two-tuple must be a tuple consisting of only Interface
        subclasses.  The second element of each two-tuple must be a
        one-argument callable which will be called with an object to
        be adapted and which will return a component implementing all
        of the Interfaces present in the first element of the
        two-tuple.
        """
        if templateMap is None:
            templateMap = {}
        self.templateMap = templateMap
        if order is None:
            order = []
        self.order = order
        if templateList:
            for (ifaces, adapter) in templateList:
                self.order.extend(ifaces)
                for iface in ifaces:
                    self.templateMap[iface] = (ifaces, adapter)

    def __getitem__(self, items):
        """Create a new ThingTemplate based on, but not identical to, this one.
        """
        map = self.templateMap.copy()
        order = self.order[:]
        if not isinstance(items, (list, tuple)):
            items = [items]
        for slice in items:
            ifaces = slice.start
            adapter = slice.stop
            if not isinstance(ifaces, (list, tuple)):
                ifaces = [ifaces]
            for iface in ifaces:
                if iface in map:
                    previousGroup = map[iface][0]
                    for prevIface in previousGroup:
                        if prevIface not in ifaces:
                            raise ValueError(
                                "Interfaces in a group must be changed "
                                "all at once or not at all: %s not in %s"
                                % (prevIface, ifaces))
                else:
                    order.append(iface)
                map[iface] = (ifaces, adapter)
        return ThingTemplate(templateMap=map, order=order)

    def fill(self, interfaces, **kw):
        if not isinstance(interfaces, (list, tuple)):
            interfaces = [interfaces]
        map = self.templateMap.copy()
        ifmap = {}
        for iface in interfaces:
            for identicalIface in map.get(iface, ((),))[0]:
                ifmap[identicalIface] = 1
        interfaces = ifmap.keys()
        order = self.order[:]
        for iface in interfaces:
            map[iface] = (map[iface][0], lazy(map[iface][1], kw))
        return ThingTemplate(templateMap=map, order=order)

    def apply(self, methodClass, methodName, *args, **kw):
        map = self.templateMap.copy()
        order = self.order[:]
        order.append(
            lazyApply(methodClass, methodName, args, kw))
        return ThingTemplate(templateMap=map, order=order)

    def copy(self):
        return self.__getitem__(())

    def new(self):
        """
        Instantiate the template.
        """
        o = self.ObjectFactory()
        skip = {}
        for iface in self.order:
            if isinstance(iface, types.FunctionType):
                ## Apply a lazy method invocation
                iface(o)
                continue
            if iface in skip:
                continue
            value = self.templateMap[iface]
            if isinstance(value, types.FunctionType):
                ## Apply a lazy component construction
                comp = value(o)
                ifaces = [iface]
            else:
                ifaces, adapter = value
                comp = adapter(o)
            for iface in ifaces:
                o[iface] = comp
                skip[iface] = None
        return o

try:
    baseTemplate
except NameError:
    baseTemplate = ThingTemplate()
