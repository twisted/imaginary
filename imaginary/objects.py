# -*- test-case-name: imaginary.test.test_objects -*-

from __future__ import division

import math

from zope.interface import implements

from twisted.python import reflect, components

from axiom import item, attributes

from imaginary import iimaginary, eimaginary, text as T, iterutils, events, language


def installedOn():
    def get(self):
        return self.thing
    def set(self, value):
        self.thing = value
    def delete(self):
        del self.thing
    doc = """
    A proxy for the C{thing} attribute, intended to be used only by
    L{item.InstallableMixin}, since it expects this attribute to have a
    particular name, while we want another one.
    """
    return property(get, set, delete, doc)
installedOn = installedOn()


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


    # NOTHING
    def conceptualize(self):
        return language.ExpressList([u'the exit to ', language.Noun(self.toLocation).nounPhrase()])
components.registerAdapter(lambda exit: exit.conceptualize(), Exit, iimaginary.IConcept)


class Thing(item.Item):
    implements(iimaginary.IThing)

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

    gender = attributes.integer(doc="""
    The grammatical gender of this thing.  One of L{language.Gender.MALE},
    L{language.Gender.FEMALE}, or L{language.Gender.NEUTER}.
    """, default=language.Gender.NEUTER, allowNone=False)

    proper = attributes.boolean(doc="""
    Whether my name is a proper noun.
    """, default=False, allowNone=False)


    def destroy(self):
        if self.location is not None:
            iimaginary.IContainer(self.location).remove(self)
        self.deleteFromStore()


    def links(self):
        d = {self.name.lower(): [self]}
        for pup in self.powerupsFor(iimaginary.ILinkContributor):
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

        @return: An iterable of L{iimaginary.IThing} providers which are found.
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
        oldLocation = self.location
        if where is not None:
            where = iimaginary.IContainer(where)
            if oldLocation is not None and not self.portable:
                raise eimaginary.CannotMove(self, where)
            where.add(self)
        if oldLocation is not None:
            iimaginary.IContainer(oldLocation).remove(self)


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
components.registerAdapter(lambda thing: language.Noun(thing).nounPhrase(), Thing, iimaginary.IConcept)


class Containment(object):
    """Functionality for containment to be used as a mixin in Powerups.
    """

    implements(iimaginary.IContainer, iimaginary.IDescriptionContributor, 
               iimaginary.ILinkContributor)

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
            cchild = iimaginary.IContainer(child, None)
            if cchild is not None and cchild.contains(other):
                return True
        return False

    def getContents(self):
        if self.thing is None:
            return []
        return self.store.query(Thing, Thing.location == self.thing)

    def add(self, obj):
        if self.closed:
            raise eimaginary.Closed(self, obj)
        containedWeight = self.getContents().getColumn("weight").sum()
        if containedWeight + obj.weight > self.capacity:
            raise eimaginary.DoesntFit(self, obj)
        assert self.thing is not None
        obj.location = self.thing

    def remove(self, obj):
        if self.closed:
            raise eimaginary.Closed(self, obj)
        if obj.location is self.thing:
            obj.location = None

    # ILinkContributor
    def links(self):
        d = {}
        if not self.closed:
            for ob in self.getContents():
                merge(d, ob.links())
        return d


    # IDescriptionContributor
    def conceptualize(self):
        return ExpressSurroundings(self.getContents())


    def installOn(self, other):
        super(Containment, self).installOn(other)
        other.powerUp(self, iimaginary.IContainer)
        other.powerUp(self, iimaginary.ILinkContributor)
        other.powerUp(self, iimaginary.IDescriptionContributor)



class ExpressSurroundings(language.ItemizedList):
    def concepts(self, observer):
        return [iimaginary.IConcept(o)
                for o in super(ExpressSurroundings, self).concepts(observer)
                if o is not observer]



class Container(item.Item, Containment, item.InstallableMixin):
    """A generic powerup that implements containment."""

    capacity = attributes.integer(doc="""
    Units of weight which can be contained.
    """, allowNone=False, default=1)

    closed = attributes.boolean(doc="""
    Indicates whether the container is currently closed or open.
    """, allowNone=False, default=False)

    installedOn = installedOn
    thing = attributes.reference(doc="""
    The object this container powers up.
    """)



class ExpressCondition(language.BaseExpress):
    implements(iimaginary.IConcept)

    def vt102(self, observer):
        return [
            [T.bold, T.fg.yellow, language.Noun(self.original.thing).shortName().plaintext(observer)],
            u" is ",
            [T.bold, T.fg.red, self.original._condition(), u"."]]


class Actable(object):
    implements(iimaginary.IActor, iimaginary.IEventObserver)

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
        other.powerUp(self, iimaginary.IActor)
        other.powerUp(self, iimaginary.IEventObserver)
        other.powerUp(self, iimaginary.IDescriptionContributor)

    # IDescriptionContributor
    def conceptualize(self):
        return ExpressCondition(self)


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
                actor=self.thing,
                actorMessage=event)
        else:
            event = event[0]
        if self.intelligence is not None:
            self.intelligence.send(event)


    def gainExperience(self, amount):
        experience = self.experience + amount
        level = int(math.log(experience) / math.log(2))
        evt = None
        if level > self.level:
            evt = events.Success(
                actor=self.thing,
                actorMessage=("You gain ", level - self.level, " levels!\n"))
        elif level < self.level:
            evt = events.Success(
                actor=self.thing,
                actorMessage=("You lose ", self.level - level, " levels!\n"))
        self.level = level
        self.experience = experience
        if evt is not None:
            self.send(evt)



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

    installedOn = installedOn
    thing = attributes.reference(doc="""
    The L{IThing} that this is installed on.
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
