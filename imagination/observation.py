from zope.interface import implements
from imagination import simulacrum, actions, errors, architecture, containment
from imagination.text import english
from imagination.facets import Faceted, Facet

# XXX I think (hope) we've reached the last major problem with
# look. That is, we don't know the relationship of objects returned
# from our collect(): things in the next room over are getting mixed
# in with things in our current room. There are two solutions two
# solutions to this, afaict:

# * Implement some kind of relationship inferencer right here in
# observation.py that, given a flat list of objects (collect's return
# value), figures out their relationship by looking at
# ILocatable.locations. I'm not sure this is sufficient.

# * Implement an alternative collector (in simulacrum.py) that returns
# information about how an object was reached. A rough guess at what
# the return value would look like: {room1: [book, {door: [{room:
# rock}]}]}. But that looks a bit ugly, perhaps something more
# encapsulated. - rade


# XXX - I think, ultimately, the event we should be sending to the
# actor ought to be an actual graph of the things around him. The way
# we're sending each object as its own event is going to make it
# really hard to make a richer UI -- but if we send a single event
# describing the visible things starting at his location, things like
# graphical maps would be easy-shmeasy. Or, simpler, putting headers
# above relevant sections of items in the text UI.

class Look(actions.TargetAction):
    allowImplicitTarget = True
    onlyBroadcastToActor = True

    allowNoneInterfaceTypes = ['Target']

    def collectThings(self, iName, iface, start=None):
        if start is None:
            start = self.actor
        visionEvaluator = Faceted()
        if iName is None:
            visionEvaluator[simulacrum.ICallableCriterion] = simulacrum.always
        else:
            ka = simulacrum.KnownAs(iName, self.actor)
            visionEvaluator[simulacrum.ICallableCriterion] = ka
            visionEvaluator[simulacrum.IKnownAs] = ka
        visionEvaluator[architecture.ISightOnly] = True
        return simulacrum.collect(start, ILookTarget, visionEvaluator, radius=2)

    def doAction(self):
        if self.target is None:
            self.target = containment.ILocatable(self.actor).location
        else:
            pass

        if self.target is None:
            raise errors.ActionFailed("Can't look at nothing (YOU ARE NOWHERE!)")

        if simulacrum.ICollector(self.target) is not containment.ILocatable(self.actor).location:
            simulacrum.ISeer(self.actor).see(english.INoun(self.target).explainTo(self.actor))
            return

        # We don't have a very specific target --
        # Find everything that can be looked at which is nearby.
        collected = self.collectThings(None, None, start=self.target)

        # Emit explanations of everything found to the
        # actor as events which can be seen.
        loc = containment.ILocatable(self.actor).location
        locations = {}
        exits = []
        for radius, thing in collected:
            if english.INoun(thing) is english.INoun(self.actor):
                continue
            else:
                where = containment.ILocatable(thing).location
                if where is not None and where is not simulacrum.ICollector(self.actor):
                    locations.setdefault(where, []).append(thing)
                elif architecture.IExit(thing, None) is not None:
                    exits.append(thing)

        L = []
        see = L.append
        see(("[ ", loc, " ]", "\n"))
        see((english.INoun(loc).explainTo(self.actor), "\n\n"))
        thingsHere = locations.pop(loc, ())
        for t in thingsHere:
            if t not in locations:
                see((t, " is here.", "\n"))

        def commify(L):
            if len(L) > 1:
                return [(e, ", ") for e in L[:-1]], "and ", L[-1]
            return L
        for (where, what) in locations.iteritems():
            see((where, " containing ", commify(what), " is here.", "\n"))

        see("Exits:\n")
        for exit in exits:
            see((exit, "\n"))
        simulacrum.ISeer(self.actor).see(L)

##        location = None
##        otherLocs = []
##        exits = []
##        allElse = []
##        inventory = []
##        for radius, thing in collected:
##            elif simulacrum.ICollector(thing) is containment.ILocatable(self.actor).location:
##                location = thing
##            elif architecture.IExit(thing, None) is not None:
##                exits.append(thing)
##            elif containment.ILocatable(thing).location is simulacrum.ICollector(self.actor):
##                inventory.append(thing)
##            else:
##                allElse.append(thing)

##        if location is not None:
##            header = "\x1B[31m%s\x1B[0m" % (location.expressTo(self.actor),)
##            see(header)
##            see(location.explainTo(self.actor))

##        for (header, stuff) in [("\x1B[32mExits\x1B[0m", exits),
##                                ("\x1B[33mOther Stuff\x1B[0m", allElse),
##                                ("\x1B[34mInventory\x1B[0m", inventory)]:
##            if stuff:
##                see(header)
##                for thing in stuff:
##                    see(thing.expressTo(self.actor))

ILookTarget = english.INoun

from imagination.text import english

class LookParser(english.Subparser):
    simpleTargetParsers = {'look': Look}

class Looker(Facet):
    implements(ILookActor)

english.registerSubparser(LookParser())
