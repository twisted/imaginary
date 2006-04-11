# -*- test-case-name: pottery.test.test_objects -*-

from __future__ import division

import math

from zope.interface import implements

from twisted.python import reflect

from epsilon import structlike

from axiom import item, attributes

from pottery import ipottery, epottery, text as T, iterutils, events


def merge(d1, *dn):
    """
    da = {a: [1, 2]}
    db = {b: [3]}
    dc = {b: [5], c: [2, 4]}
    merge(da, db, dc)
    da == {a: [1, 2], b: [3, 5], c: [2, 4]}
    """
    for d in dn:
        for (k, v) in d.iteritems():
            d1.setdefault(k, []).extend(v)


class Points(item.Item):
    max = attributes.integer(doc="""
    Maximum number of points.
    """, allowNone=False)

    current = attributes.integer(doc="""
    Current number of points.
    """, allowNone=False)

    def __init__(self, **kw):
        if 'max' in kw and 'current' not in kw:
            kw['current'] = kw['max']
        super(Points, self).__init__(**kw)

    def __cmp__(self, other):
        return cmp(self.current, other)

    def __str__(self):
        return '%d/%d' % (self.current, self.max)

    def __repr__(self):
        d = {'class': reflect.qual(self.__class__),
             'current': self.current,
             'max': self.max}
        return '%(class)s(%(max)d, %(current)d)' % d

    def increase(self, amount):
        return self.modify(amount)

    def decrease(self, amount):
        return self.modify(-amount)

    def modify(self, amount):
        self.current = max(min(self.current + amount, self.max), 0)
        return self.current


OPPOSITE_DIRECTIONS = {
    u"north": u"south",
    u"south": u"north",
    u"west": u"east",
    u"east": u"west"}


class Exit(item.Item):
    implements(ipottery.IDescribeable)

    fromLocation = attributes.reference(doc="""
    Where this exit leads from.
    """, allowNone=False, whenDeleted=attributes.reference.CASCADE)

    toLocation = attributes.reference(doc="""
    Where this exit leads to.
    """, allowNone=False, whenDeleted=attributes.reference.CASCADE)

    name = attributes.text(doc="""
    What this exit is called/which direction it is in.
    """, allowNone=False)

    sibling = attributes.reference(doc="""
    The reverse exit object, if one exists.
    """)


    def link(cls, a, b, forwardName, backwardName=None):
        if backwardName is None:
            backwardName = OPPOSITE_DIRECTIONS[forwardName]
        me = cls(store=a.store, fromLocation=a, toLocation=b, name=forwardName)
        him = cls(store=b.store, fromLocation=b, toLocation=a, name=backwardName)
        me.sibling = him
        him.sibling = me
    link = classmethod(link)


    def destroy(self):
        if self.sibling is not None:
            self.sibling.deleteFromStore()
        self.deleteFromStore()


    # IDescribeable
    def formatTo(self, who):
        return ('the exit to ',
                ipottery.IDescribeable(self.toLocation).formatTo(who))


    def longFormatTo(self, who):
        raise NotImplemented("Please implement this.")



class Object(item.Item):
    implements(ipottery.IObject)

    weight = attributes.integer(doc="""
    Units of weight of this object.
    """, default=1, allowNone=False)

    location = attributes.reference(doc="""
    Direct reference to the location of this object
    """)

    portable = attributes.boolean(doc="""
    Whether this can be picked up, pushed around, relocated, etc
    """, default=True, allowNone=False)

    name = attributes.text(doc="""
    The name of this object.
    """, allowNone=False)

    description = attributes.text(doc="""
    What this object looks like.
    """, default=u"")


    def destroy(self):
        if self.location is not None:
            ipottery.IContainer(self.location).remove(self)
        self.deleteFromStore()


    def links(self):
        d = {self.name.lower(): [self]}
        for pup in self.powerupsFor(ipottery.ILinkContributor):
            merge(d, pup.links())
        for exit in self.getExits():
            merge(d, {exit.name: [exit.toLocation]})
        return d


    def find(self, name):
        """
        deprecated, don't use this.  look at search.
        """
        i = self.search(1, lambda x, y: x, name)
        try:
            return i.next()
        except StopIteration:
            return None


    def locate(self, interface, name):
        name = name.lower()
        for (k, v) in self.links().iteritems():
            if k.startswith(name):
                for ob in v:
                    facet = interface(ob, None)
                    if facet is not None:
                        yield (ob, facet)


    def search(self, distance, interface, name):
        """
        Retrieve game objects answering to the given name which provide the
        given interface and are within the given distance.

        @type distance: C{int}
        @param distance: How many steps to traverse (note: this is wrong, it
        will become a real distance-y thing with real game-meaning someday).

        @param interface: The interface which objects within the required range
        must be adaptable to in order to be returned.

        @type name: C{str}
        @param name: The name of the stuff.

        @return: An iterable of L{ipottery.IObject} providers which are found.
        """
        seen = {}
        visited = {self: True}

        if name == "me" or name == "self":
            facet = interface(self, None)
            if facet is not None:
                seen[self] = True
                yield facet
        if name == "here" and self.location is not None:
            facet = interface(self.location, None)
            if facet is not None:
                seen[self.location] = True
                yield facet

        n = 1
        descendTo = [(distance, 0, self)]
        if self.location is not None:
            descendTo.append((distance - 1, 1, self.location))
        while descendTo:
            distance, _, target = descendTo.pop()
            for ob, facet in target.locate(interface, name):
                if ob not in seen:
                    seen[ob] = True
                    yield facet
            if distance:
                for (k, obs) in target.links().iteritems():
                    for ob in obs:
                        if ob not in visited:
                            visited[ob] = True
                            n += 1
                            descendTo.append((distance - 1, n, ob))
            descendTo.sort()


    def canSee(self, thing):
        return True


    def moveTo(self, where):
        if where is self.location:
            return
        where = ipottery.IContainer(where)
        oldLocation = self.location
        if oldLocation is not None and not self.portable:
            raise epottery.CannotMove(self, where)
        where.add(self)
        if oldLocation is not None:
            ipottery.IContainer(oldLocation).remove(self)


    def formatTo(self, who):
        return self.name


    def longFormatTo(self, who):
        exitNames = list(self.getExitNames())
        if exitNames:
            exits = ([T.fg.blue, '( ', [T.fg.cyan,
                                        iterutils.interlace(' ', exitNames)],
                      ' )'], '\n')
        else:
            exits = ''

        description = ''
        if self.description:
            description = (self.description, '\n')

        descriptionComponents = []
        for pup in self.powerupsFor(ipottery.IDescriptionContributor):
            descriptionComponents.append(pup.longFormatTo(who))

        return (
            [T.fg.magenta, '[ ', [T.fg.yellow, self.name], ' ]'], '\n',
            exits,
            [T.fg.green, description],
            descriptionComponents)


    def getExits(self):
        return self.store.query(Exit, Exit.fromLocation == self)


    def getExitNames(self):
        return self.getExits().getColumn("name")


    _marker = object()
    def getExitNamed(self, name, default=_marker):
        result = self.store.findUnique(
            Exit,
            attributes.AND(Exit.fromLocation == self,
                           Exit.name == name),
            default=default)
        if result is self._marker:
            raise KeyError(name)
        return result



class Containment(object):
    """Functionality for containment to be used as a mixin in Powerups.
    """

    implements(ipottery.IContainer, ipottery.IDescriptionContributor, 
               ipottery.ILinkContributor)

    # Units of weight which can be contained
    capacity = None

    # Reference to another object which serves as this container's lid.
    # If None, this container cannot be opened or closed.
    # lid = None

    # Boolean indicating whether the container is currently closed or open.
    closed = False

    def contains(self, other):
        for child in self.getContents():
            if other is child:
                return True
            cchild = ipottery.IContainer(child, None)
            if cchild is not None and cchild.contains(other):
                return True
        return False

    def getContents(self):
        if self.installedOn is None:
            return []
        return self.store.query(Object, Object.location == self.installedOn)

    def add(self, obj):
        if self.closed:
            raise epottery.Closed(self, obj)
        containedWeight = self.getContents().getColumn("weight").sum()
        if containedWeight + obj.weight > self.capacity:
            raise epottery.DoesntFit(self, obj)
        assert self.installedOn is not None
        obj.location = self.installedOn

    def remove(self, obj):
        if self.closed:
            raise epottery.Closed(self, obj)
        if obj.location is self.installedOn:
            obj.location = None

    # ILinkContributor
    def links(self):
        d = {}
        if not self.closed:
            for ob in self.getContents():
                merge(d, ob.links())
        return d


    # IDescriptionContributor
    def longFormatTo(self, who):
        contentStuff = [c for c in self.getContents() if c is not who]
        if contentStuff:
            return [iterutils.interlace(', ', contentStuff), '\n']
        return ''


    def installOn(self, other):
        super(Containment, self).installOn(other)
        other.powerUp(self, ipottery.IContainer)
        other.powerUp(self, ipottery.ILinkContributor)
        other.powerUp(self, ipottery.IDescriptionContributor)



class Container(item.Item, Containment, item.InstallableMixin):
    """A generic powerup that implements containment."""

    capacity = attributes.integer(doc="""
    Units of weight which can be contained.
    """, allowNone=False, default=1)

    closed = attributes.boolean(doc="""
    Indicates whether the container is currently closed or open.
    """, allowNone=False, default=False)

    installedOn = attributes.reference(doc="""
    The object this container powers up.
    """)



class Actable(object):
    implements(ipottery.IActor, ipottery.IEventObserver)

    # Yay, experience!
    experience = 0
    level = 0

    # Something with a send method, maybe, sometimes.
    intelligence = None

    CONDITIONS = (
        'dead',
        'dying',
        'incapacitated',
        'mortally wounded',
        'injured',
        'bleeding',
        'shaken up',
        'fine',
        'chipper',
        'great')


    def installOn(self, other):
        super(Actable, self).installOn(other)
        other.powerUp(self, ipottery.IActor)
        other.powerUp(self, ipottery.IEventObserver)
        other.powerUp(self, ipottery.IDescriptionContributor)

    # IDescriptionContributor
    def longFormatTo(self, who):
        return ([T.bold, T.fg.yellow, self.installedOn.formatTo(who)],
                " is ",
                [T.bold, T.fg.red, self._condition()],
                ".",
                "\n")


    def _condition(self):
        if self.hitpoints.current == 0:
            return self.CONDITIONS[0]
        ratio = self.hitpoints.current / self.hitpoints.max
        idx = int(ratio * (len(self.CONDITIONS) - 2))
        return self.CONDITIONS[idx + 1]


    # IEventObserver
    def send(self, *event):
        if len(event) != 1 or isinstance(event[0], (str, tuple)):
            event = events.Success(
                actor=self.installedOn,
                actorMessage=event)
        else:
            event = event[0]
        if self.intelligence is not None:
            self.intelligence.send(event)


    def gainExperience(self, amount):
        experience = self.experience + amount
        level = int(math.log(experience) / math.log(2))
        if level > self.level:
            evt = events.Success(
                actor=self.installedOn,
                actorMessage=("You gain ", level - self.level, " levels!\n"))
        elif level < self.level:
            evt = events.Success(
                actor=self.installedOn,
                actorMessage=("You lose ", self.level - level, " levels!\n"))
        self.send(evt)
        self.level = level
        self.experience = experience



class Actor(item.Item, Actable, item.InstallableMixin):
    hitpoints = attributes.reference(doc="""
    """)
    stamina = attributes.reference(doc="""
    """)
    strength = attributes.reference(doc="""
    """)

    intelligence = attributes.inmemory(doc="""
    The intelligence provider associated with this actor, generally a L{wiring.player.Player} instance.
    """)

    installedOn = attributes.reference(doc="""
    The L{IObject} that this is installed on.
    """)

    level = attributes.integer(doc="""
    Don't you hate level-based games?  They're so stupid.
    """, default=0, allowNone=False)

    experience = attributes.integer(doc="""
    XP!  Come on, you know what this is.
    """, default=0, allowNone=False)


    def __init__(self, **kw):
        super(Actor, self).__init__(**kw)
        if self.hitpoints is None:
            self.hitpoints = Points(store=self.store, max=100)
        if self.stamina is None:
            self.stamina = Points(store=self.store, max=100)
        if self.strength is None:
            self.strength = Points(store=self.store, max=100)
