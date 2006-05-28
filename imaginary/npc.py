# -*- test-case-name: imaginary.test.test_npc -*-

from axiom import item, attributes

from imaginary import events, objects


class Mouse(item.Item):
    squeakiness = attributes.integer(doc="""
    How likely the mouse is to squeak when intruded upon (0 - 100).

    This mouse is so angry that he will pretty much always squeak.
    """, default=100)

    def prepare(self, concept):
        if isinstance(concept, events.ArrivalEvent):
            return self.squeak
        return lambda: None


    def squeak(self):
        actor = self.store.findUnique(
            objects.Actor,
            objects.Actor._enduringIntelligence == self)
        evt = events.Success(
            actor=actor.thing,
            otherMessage=u"SQUEAK!")
        evt.broadcast()


def createMouse(**kw):
    store = kw['store']
    mouse = objects.Thing(**kw)
    mouseActor = objects.Actor(store=store)
    mouseActor.installOn(mouse)
    mousehood = Mouse(store=store)
    mouseActor.setEnduringIntelligence(mousehood)
    return mouse
