
from imagination.templates.basic import Thing as T
from imagination.templates.basic import Room
from imagination import simulacrum, containment
from imagination.text import english

def wayRightCurry(cls, *a, **kw):
    return lambda o: cls(o, *a, **kw)
wRC = wayRightCurry

NamedTemplate = T[
    english.INoun: english.Noun]

RoomTemplate = Room

TrinketTemplate = NamedTemplate[
    (simulacrum.ICollector, containment.ILinkable): containment.Atom,
    containment.ILocatable: containment.AtomMobility]
