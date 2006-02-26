
class Event(object):
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
        self.actorMessage = actorMessage
        self.targetMessage = targetMessage
        self.toolMessage = toolMessage
        self.otherMessage = otherMessage

    def formatTo(self, observer):
        msg = self.formattedFor(observer)
        if msg is not None:
            return msg, "\n"
        return ''

    def formattedFor(self, observer):
        msg = {self.actor: self.actorMessage,
               self.target: self.targetMessage,
               self.tool: self.toolMessage}.get(observer, self.otherMessage)
        return msg

    def broadcast(self):
        for ob in self.location.contents:
            if hasattr(ob, 'send'):
                ob.send(self.formatTo(ob))


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
