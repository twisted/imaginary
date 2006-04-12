from twisted.python import components

from reality.text import common, english
from reality import things, actions, ambulation


class Look(actions.TargetAction):
    allowNoneInterfaceTypes = ['Actor', 'Target', 'Tool', 'Place']
    allowImplicitTarget = 1
    onlyBroadcastToActor = 1

    description = None

    def formatToActor(self):
        inv = [(x, ', ') for x in self.inventory]
        if len(inv):
            if len(inv) == 1:
                inv[-1] = inv[-1][0]
            else:
                inv[-1] = ('and ', inv[-1][0])
        else:
            inv = "nothing special"
        if self.description:
            spacer = " "
        else:
            spacer = ''
        if self.exits:
            exits = ("\nExits: ", 
                [[x, 
                  ", ", 
                  x.source is self.actor.original.location 
                      and x.direction 
                      or (x.reverseName or ambulation.opposite(x.direction)),
                  '; '] for x in self.exits])
            exits[1][-1][3] = ''
        else:
            exits = ''
        return self.target, "\n", self.description, spacer, "You see ", inv, ".", exits

    def doAction(self):
        ## If we aren't looking at anything in particular, look at the location
        if self.targetName == '':
            self.target = self.actor.original.location.getItem()

        ## Figure out what the real target is (xxx this should not be required)
        if hasattr(self.target, 'original'):
            target = self.target.original
        else:
            target = self.target
        if target is None:
            from reality import errors
            raise errors.ActionFailed("Can't look at nothing.")

        ## Find all the IThings lying around
        collected = target.collectImplementors(
            self, things.IThing, {}, {}, intensity=1).values()

        ## Check for a nice description of what we're looking at
        desc = target.getComponent(common.IDescribeable)
        if desc is not None:
            self.description = desc.explainTo(self.actor.original)
        
        ## Look for stuff contained by what we're looking at
        self.inventory = [x for x in collected 
            if x is not self.target 
            and x is not self.actor.original
            and getattr(x.getComponent(things.IThing), 'location', None) == target]
        
        ## If the player is looking at the room
        if components.implements(self.target, ambulation.IWalkTarget):
            ## Gather a list of exits
            self.exits = [x for x in collected
                if isinstance(x, ambulation.Exit)]
        else:
            self.exits = []


class LookParser(english.Subparser):
    simpleTargetParsers = {'look': Look,
                           'look at': Look}

class Lookable(components.Adapter):
    __implements__ = ILookTarget, ILookActor, things.IInterfaceForwarder
    
    def collectImplementors(self, *args, **kwargs):
        kwargs['intensity'] = 1
        return self.original.collectImplementors(*args, **kwargs)

    
english.registerSubparser(LookParser())
components.registerAdapter(Lookable, things.Thing, ILookTarget)
components.registerAdapter(Lookable, things.Thing, ILookActor)
