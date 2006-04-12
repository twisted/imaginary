
from imagination.simulacrum import ISeer, IHearer
from imagination.simulacrum import ICollector, collect, always

ifaceToMethodMap = {
    ISeer: "see",
    IHearer: "hear"}

def emitEvent(source, radius, iface, mname, *args, **kw):
    collected = collect(ICollector(source), iface, always, radius)
    for (radius, receiver) in collected:
        getattr(receiver, mname)(*args, **kw)

def broadcastToActor(actor, msg, iface=ISeer):
    """Send a message to the given actor.
    """
    o = iface(action.actor, None)
    if o is not None:
        getattr(o, ifaceToMethodMap[iface])(msg)

def broadcastToAll(locatable, msg, radius=1, iface=ISeer):
    """Send a message to all observers at the same location as the given locatable.
    """
    from imagination import containment
    return broadcastToLocation(containment.ILocatable(locatable).location, msg, radius, iface)

def broadcastToLocation(location, msg, radius=1, iface=ISeer):
    """
    Send to a location.
    """
    from imagination import containment
    mname = ifaceToMethodMap[iface]
    collected = collect(ICollector(location), iface,
                        always,
                        radius)
    for (radius, receiver) in collected:
        getattr(receiver, mname)(msg)

def broadcastToSeveral(location, groupInfo, rest, radius=1, iface=ISeer):
    """Send a group of messages to a group of observers, and another message to everyone else.
    """
    notRest = {}
    for (actor, msg) in groupInfo:
        o = iface(actor, None)
        if o is not None:
            notRest[o] = True
            getattr(o, ifaceToMethodMap[iface])(msg)

    collected = collect(ICollector(location), iface,
                        always,
                        radius)
    for (distance, obj) in collected:
        if obj not in notRest:
            getattr(obj, ifaceToMethodMap[iface])(rest)

def broadcastToOthers(actor, msg, radius=1, iface=ISeer):
    """Send a message to everyone except a particular actor.
    """
    from imagination import containment
    broadcastToSeveral(containment.ILocatable(actor).location,
                       [], msg, radius, iface)

def broadcastEvent(actor, actorMsg, otherMsg, radius=1, iface=ISeer):
    """Send a message to an actor and another message to everyone else.
    """
    from imagination import containment
    broadcastToSeveral(containment.ILocatable(actor).location,
                       [(actor, actorMsg)], otherMsg, radius, iface)
