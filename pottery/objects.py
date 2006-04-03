# -*- test-case-name: pottery.test.test_objects -*-

from __future__ import division

import math, random, itertools

from zope.interface import implements

from twisted.internet import reactor
from twisted.python import reflect, util

from pottery import ipottery, epottery, text as T, iterutils

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

class Points(object):
    max = 0
    current = 0

    def __init__(self, max, current=None):
        self.max = max
        if current is None:
            current = max
        self.current = current

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

class Object(object):
    implements(ipottery.IObject)

    # Units of weight of this object
    weight = 1

    # Yay, experience!
    experience = 0

    # Direct reference to the location of this object
    location = None

    # Whether this can be picked up, pushed around, relocated, etc
    portable = True

    def __init__(self, name, description=''):
        self.name = name
        self.description = description

    def __str__(self):
        d = {'class': self.__class__.__name__,
             'name': self.name,
             'location': self.location}
        return '%(class)s %(name)r at %(location)s' % d

    def __repr__(self):
        d = {'class': self.__class__.__name__,
             'name': self.name,
             'location': self.location}
        return '%(class)s(name=%(name)r, location=%(location)r)' % d

    def destroy(self):
        if self.location is not None:
            self.location.remove(self)
            self.location = None

    def links(self):
        return {self.name.lower(): [self]}

    def find(self, name):
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
        oldLocation = self.location
        if oldLocation is where:
            return
        if oldLocation is not None and not self.portable:
            raise epottery.CannotMove(self, where)
        where.add(self)
        if oldLocation is not None:
            oldLocation.remove(self)

    def formatTo(self, who):
        return self.name

    def longFormatTo(self, who):
        if self.description:
            return (T.fg.yellow, self.name, '\n',
                    T.fg.green, self.description, '\n')
        return (T.fg.yellow, self.name, '\n')

class Container(Object):
    implements(ipottery.IContainer)

    # Units of weight which can be contained
    capacity = 1

    # Reference to another object which serves as this container's lid.
    # If None, this container cannot be opened or closed.
    lid = None

    # Boolean indicating whether the container is currently closed or open.
    closed = False

    def __init__(self, *a, **kw):
        super(Container, self).__init__(*a, **kw)
        self.contents = []

    def links(self):
        d = super(Container, self).links()
        if not self.closed:
            for ob in self.contents:
                merge(d, ob.links())
        return d

    def longFormatTo(self, who):
        return (super(Container, self).longFormatTo(who),
                [(T.fg.cyan, c.formatTo(who), '\n') for c in self.contents if c is not who])

    def add(self, obj):
        if self.closed:
            raise epottery.Closed(self, obj)
        if sum([o.weight for o in self.contents]) + obj.weight > self.capacity:
            raise epottery.DoesntFit(self, obj)
        self.contents.append(obj)
        obj.location = self

    def remove(self, obj):
        if self.closed:
            raise epottery.Closed(self, obj)
        self.contents.remove(obj)
        if obj.location is self:
            obj.location = None

    def contains(self, other):
        for child in self.contents:
            if other is child:
                return True
            cchild = ipottery.IContainer(child, None)
            if cchild is not None and cchild.contains(other):
                return True
        return False



class Room(Container):
    capacity = 1000

    def __init__(self, *a, **kw):
        super(Room, self).__init__(*a, **kw)
        self.exits = {}

    def links(self):
        d = super(Room, self).links()
        for ex, dest in self.exits.iteritems():
            merge(d, {ex: [dest]})
        return d

    def longFormatTo(self, who):
        contents = iterutils.interlace(
            ', ',
            [c for c in self.contents if c is not who])
        exits = iterutils.interlace(' ', self.exits)
        description = ''
        if self.description:
            description = (self.description, '\n')
        return (
            [T.fg.magenta, '[ ', [T.fg.yellow, self.name], ' ]'], '\n',
            [T.fg.blue, '( ', [T.fg.cyan, exits], ' )'], '\n',
            [T.fg.green, description], contents, '\n')

    def broadcastIf(self, pred, *what):
        for c in self.contents:
            if pred(c):
                if hasattr(c, 'broadcastIf'):
                    c.broadcastIf(pred, *what)
                elif hasattr(c, 'send'):
                    c.send(*what)

class Actor(Container):
    HEARTBEAT_INTERVAL = 30
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

    weight = 100
    capacity = 90

    level = 0

    useColors = True

    def __init__(self, *a, **kw):
        super(Actor, self).__init__(*a, **kw)

        self.termAttrs = T.AttributeSet()

        self.hitpoints = Points(100)
        self.stamina = Points(100)
        self.strength = Points(100)

        self.heartbeat()

    def __setstate__(self, state):
        self.__dict__ = state
        self.heartbeat()

    def __getstate__(self):
        d = self.__dict__.copy()
        d.pop('_heartbeatCall', '')
        return d

    def destroy(self):
        super(Actor, self).destroy()
        self._heartbeatCall.cancel()

    def heartbeat(self):
        self.stamina.increase(random.randrange(1, 5))
        self.hitpoints.increase(random.randrange(1, 5))
        self._heartbeatCall = reactor.callLater(self.HEARTBEAT_INTERVAL,
                                                self.heartbeat)

    def _condition(self):
        if self.hitpoints.current == 0:
            return self.CONDITIONS[0]
        ratio = self.hitpoints.current / self.hitpoints.max
        idx = int(ratio * (len(self.CONDITIONS) - 2))
        return self.CONDITIONS[idx + 1]

    def longFormatTo(self, who):
        return (super(Actor, self).longFormatTo(who),
                [T.bold, T.fg.yellow, self.formatTo(who)],
                " is ",
                [T.bold, T.fg.red, self._condition()],
                ".",
                "\n")

    def format(self, *args):
        L = []
        it = T.flatten(args, currentAttrs=self.termAttrs)
        while True:
            try:
                obj = it.next()
            except StopIteration:
                break
            else:
                if ipottery.IDescribeable.providedBy(obj):
                    it = itertools.chain(
                        T.flatten(obj.formatTo(self),
                                  currentAttrs=self.termAttrs), it)
                else:
                    if self.useColors:
                        L.append(str(obj))
                    else:
                        if hasattr(obj, 'startswith'):
                            if hasattr(obj, 'endswith'):
                                if obj.startswith('\x1b['):
                                    if obj.endswith('m'):
                                        continue
                        L.append(str(obj))

        return ''.join(L)


class Mob(Actor):
    def send(self, *a):
        pass

class Player(Actor):
    implements(ipottery.IPlayer)

    proto = None
    realm = None

    def __getstate__(self):
        d = super(Player, self).__getstate__()
        d.pop('proto', '')
        return d

    def setProtocol(self, proto):
        if self.proto is not None:
            self.send("Your body has been usurped!\n")
            self.disconnect()
        self.proto = proto
        self.termAttrs = T.AttributeSet()

    def disconnect(self):
        if self.proto and self.proto.terminal:
            self.proto.player = None
            self.proto.terminal.loseConnection()

    proto = None
    def send(self, *args):
        if self.proto is not None:
            bytes = self.format(*args)
            self.proto.write(bytes)


    def destroy(self):
        super(Player, self).destroy()
        self.realm.destroy(self)
        self.disconnect()

    def gainExperience(self, amount):
        experience = self.experience + amount
        level = int(math.log(experience) / math.log(2))
        if level > self.level:
            self.send("You gain ", level - self.level, " levels!\n")
        elif level < self.level:
            self.send("You lose ", self.level - level, " levels!\n")
        self.level = level
        self.experience = experience
