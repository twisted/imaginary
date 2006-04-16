# -*- test-case-name: imaginary.test -*-

from zope.interface import implements

from imaginary import iimaginary, language

class Event(language.BaseExpress):
    implements(iimaginary.IConcept)

    actorMessage = targetMessage = toolMessage = otherMessage = None

    def __init__(self,
                 location=None, actor=None, target=None, tool=None,
                 actorMessage=None, targetMessage=None, toolMessage=None,
                 otherMessage=None):

        if location is None and actor is not None:
            location = actor.location

        self.location = location
        self.actor = actor
        self.target = target
        self.tool = tool
        if actorMessage is not None:
            self.actorMessage = iimaginary.IConcept(actorMessage)
        if targetMessage is not None:
            self.targetMessage = iimaginary.IConcept(targetMessage)
        if toolMessage is not None:
            self.toolMessage = iimaginary.IConcept(toolMessage)
        if otherMessage is not None:
            self.otherMessage = iimaginary.IConcept(otherMessage)


    def conceptFor(self, observer):
        # This can't be a dict because then the ordering when actor is target
        # or target is tool or etc is non-deterministic.
        if observer is self.actor:
            msg = self.actorMessage
        elif observer is self.target:
            msg = self.targetMessage
        elif observer is self.tool:
            msg = self.toolMessage
        else:
            msg = self.otherMessage
        return msg


    def broadcast(self):
        for ob in iimaginary.IContainer(self.location).getContents():
            observer = iimaginary.IEventObserver(ob, None)
            if observer:
                observer.send(self)


    def vt102(self, observer):
        c = self.conceptFor(observer)
        if c is not None:
            return [c.vt102(observer), '\n']
        return u''



class ThatDoesntMakeSense(Event):
    """
    An action was attempted which is logically impossible.
    """
    def __init__(self, actorMessage="That doesn't make sense.", **kw):
        super(ThatDoesntMakeSense, self).__init__(actorMessage=actorMessage, **kw)


class ThatDoesntWork(Event):
    """
    An action was attempted which is phyically impossible.
    """
    def __init__(self, actorMessage="That doesn't work.", **kw):
        super(ThatDoesntWork, self).__init__(actorMessage=actorMessage, **kw)


class Success(Event):
    """
    You do it.  Swell.
    """
