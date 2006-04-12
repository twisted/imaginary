
import random

from twisted.python import components

from imagination import simulacrum, actions, containment, errors
from imagination.simulacrum import ISeer, IHearer
from imagination.text import english

from imagination.event import broadcastToLocation, broadcastEvent
from imagination.event import broadcastToAll, broadcastToActor
from imagination.event import broadcastToSeveral, broadcastToOthers

class SqueakyPortable(components.Adapter):
    """Something which makes noises when it gets moved around.
    """
    __implements__ = (containment.ITakeTarget, containment.IDropTarget)

    def postTargetTake(self, action, result):
        actor, target = action.actor, action.target
        broadcastEvent(actor,
                       (target, " emits a faint squeak as you pick it up."),
                       (target, " emits a faint squeak as ", actor, " picks it up."),
                       iface=IHearer)

    def postTargetDrop(self, action, result):
        target = action.target
        broadcastToAll(target,
                       (target, " emits a faint squeak as it lands on the floor."),
                       iface=IHearer)

class Pull(actions.TargetAction):
    pass

class PullSpeaker(components.Adapter):
    """Something which speaks random gibberish when it is pulled.
    """
    __implements__ = (IPullTarget,)

    def __init__(self, original, strings=("This PullSpeaker was poorly initialized.",)):
        components.Adapter.__init__(self, original)
        self.speech = list(strings)

    def postTargetPull(self, action, result):
        f = random.random()
        speech = '"' + random.choice(self.speech) + '"'
        if f < 0.3:
            s = ('It reels back in, and it chirps, ', speech, ' in a faint, high-pitched voice.')
        elif f < 0.7:
            s = ('It reels itself back in, and it chirps, ', speech, ' in a faint, high-pitched voice.')
        else:
            s = ('As ', self, "'s string reels in, it squeaks, ", speech)
        broadcastEvent(action.actor,
                       ("You yank ", self, "'s string.  ") + s,
                       (action.actor, " yanks ", self, "'s string.  ") + s)

class Squeeze(actions.TargetAction):
    def doAction(self):
        both = (self.target, ' squeaks, "That tickles!"')
        broadcastEvent(action.actor,
                       ("You squeeze ", self.target, ".  ") + both,
                       (self.actor, "squeezes ", self.target, ".  ") + both)


class Push(actions.TargetAction):
    def doAction(self):
        pass

class Pusher(components.Adapter):
    __implements__ = (IPushActor,)
    
class Drink(actions.TargetAction):
    def doAction(self):
        pass

class Drinker(components.Adapter):
    __implements__ = (IDrinkActor,)
    
# Make these two ToolActions
class Open(actions.TargetAction):
    def doAction(self):
        pass

class Close(actions.TargetAction):
    def doAction(self):
        pass

class Type(actions.TargetAction):
    def __init__(self, player, targetName, typedIn):
        actions.TargetAction.__init__(self, player, targetName)
        self.typedIn = typedIn

    def doAction(self):
        pass

class Typer(components.Adapter):
    __implements__ = (ITypeActor,)

class Dance(actions.TargetAction):
    def doAction(self):
        broadcastEvent(action.actor,
                       ("You get down, get funky, and dance around with ",
                        self.target, "."),
                       (self.actor, " gets down and gets funky, dancing with ",
                        self.target, "."))

class Dancer(components.Adapter):
    __implements__ = (IDanceActor,)

class Wind(actions.ToolAction):
    def doAction(self):
        pass

class Fountain(components.Adapter):
    __implements__ = (IPushTarget, IDrinkTarget)

    isOn = False

    sounds = ["There is a rumbling sound from underneath",
              "There is a lound clanking sound from underneath",
              "There is a metallic rattling sound from beneath",
              "There is a deep, echoing rumble from beneath"]

    def __init__(self, original):
        components.Adapter.__init__(self, original)
        self.drinks = {}
        self.stuff = []  # XXX This isn't used?  I can't tell

    def postTargetPush(self, action, result):
        actor = action.actor
        if self.isOn:
            broadcastToActor(action.actor, "Nothing happens.")
        if len(self.stuff) > 0:
            # If there is stuff in the fountain, eject the first one you come across
            launched = self.stuff.pop()
            containment.ILocatable(launched).location = simulacrum.ILocatable(self).location
            s = random.choice(self.sounds)
            r = " the floor and ", self, "'s spigot bulges alarmingly as ", launched, " pops out of it."
            broadcastToAll(self, (s,) + r)
        else:
            # XXX Futz with the description here
            self.isOn = True
            broadcastToAll(self, "Cool, refreshing water begins to flow from the fountain.")
            from twisted.internet import reactor
            reactor.callLater(2, self.fountainOff)
            # IReactorTime(context).callLater(2, self.fountainOff)

    def fountainOff(self):
        # XXX Futz with description here again
        self.isOn = False
        broadcastToAll(self, ("Water ceases to flow from ", self, "."))

    def preTargetDrink(self, action):
        if not self.isOn:
            raise errors.ActionRefused(self, " is not producing any water "
                                       "for you to drink.")

    goodDrinkMsgs = ["drinking from a cold mountain stream",
                     "skiing down an arctic mountain",
                     "sailing through arctic waters"]
    badDrinkMsgs = ["freezing to death on the set of a breathmint commercial",
                    "repeatedly drinking water",
                    "weren't so much of a loser that you spent most of your "
                    "time drinking from a fountain"]

    def postTargetDrink(self, action, result):
        drinks = self.drinks.setdefault(action.actor, 0)
        if drinks < 4:
            msg = random.choice(self.goodDrinkMsgs)
            self.drinks[action.actor] += 1
        else:
            msg = random.choice(self.badDrinkMsgs)
            self.drinks[action.actor] = 0
        broadcastEvent(action.actor,
                       ("You take a drink of cool, refreshing water from ",
                        self, " and feel refreshed and invigorated, as if "
                        "you were ", msg, "..."),
                       (action.actor, " drinks from ", self, "."))

class Mop(components.Adapter):
    __implements__ = (IDanceTarget,)

    def postTargetDance(self, action, result):
        """dance with mop

        Who's a man and a half?  I'm a man and a half -- a man and a half with
        a fucking DANCING MOP!!!!!
        """

class Winder(components.Adapter):
    """A key that can wind things.

    Currently this is justt to wind up the brass cockroach, but it's certainly
    likely that it'll wind other automata.
    """
    # XXX weak lazy bum
    __implements__ = (IWindTool, IWindActor)

def seqreplace(seq, orig, repl):
    return [(e, repl)[e == orig] for e in seq]

class Roach(components.Adapter):
    """
    This item brought to you by The Society for Putting Things on Top of Other
    Things.  I am an automatic cockroach.  Thanks (and apologies) to Mr. Tenth.
    """
    __implements__ = (IWindTarget,)

    SELF = object()

    bugSounds = [(SELF, " wiggles its antennae curiously."),

                 (SELF, " skitters around frantically for a moment, and then "
                  "comes to a rather sudden stop."),

                 (SELF, " flutters its wings and emitts a faint clicking."),

                 (SELF, " waves its antennae and wiggles its abdomen, "
                  "apparently having found a small but tasty particle of "
                  "something on the ground."),

                 (SELF, " waves its antennae."),

                 (SELF, " skitters around."),

                 (SELF, " flutters its wings and suddenly takes to the air, "
                  "flying around in erratic circles for a few seconds, "
                  "emitting a rasping metallic buzz... and then plummets to "
                  "the ground with a faint clinking sound.")]

    winds = 0
    mood = "lying on its back"

    def startTicking(self, action):
        from twisted.internet import reactor
        reactor.callLater(1, self.roachMove)
        # IReactorTime(context).callLater(1, self.roachMove)

    def postTargetWind(self, action, result):
        if self.winds < 15:
            broadcastEvent(action.actor,
                           ("You wind ", self, "."),
                           (action.actor, " winds ", self, "."))
            if self.winds == 0:
                self.startTicking(action)
            self.winds += 5
        else:
            broadcastEvent(action.actor,
                           ("You attempt to wind ", self, " but it is already "
                            " wound as tightly as possible."),
                           (action.actor, " attempts to wind ", self, "."))

    def roachMove(self):
        """Move the roach.
        """
        if self.winds == 0:
            broadcastToAll(self,
                           (self, " flips over onto its back, twitches its "
                            "legs momentarily, and falls silent."))
            self.mood = "lying on its back"
            return

        L = containment.ILocatable(self).location
        LL = containment.ILocatable(L).location

        self.mood = ""
        self.winds -= 1

        from twisted.internet import reactor
        reactor.callLater(1, self.roachMove)
        # IReactorTime(context).callLater(1, self.roachMove)

        if L is None:
            log.msg("%r at None location (I guess it's a bug!)" % (self,))
            return

        if containment.ITakeActor(L, None) is not None:
            # Someone grabbed us!  Probably at least.  Who knows, actually.

            broadcastEvent(L,
                           (self, " wriggles its way out of your hands, ",
                            "and lands on the ground."),
                           (self, " wriggles its way out of ", L, "'s hands, "
                            "ands lands on the ground."))
            containment.ILocatable(self).location = LL
        else:
            # XXX Totally generalize and expand this
            sound = random.choice(self.bugSounds)
            sound = seqreplace(sound, self.SELF, self)
            broadcastToLocation(L, sound)            

        # XXX Implement flying off tables
        # XXX Impleemnt scrambling around inside boxes

class Register(components.Adapter):
    __implements__ = (IOpenTarget, ICloseTarget, ITypeTarget)

    isOpen = False
    isLocked = True

    code = 0

    def preTargetOpen(self, action, result):
        if self.isOpen:
            raise actions.Refusal(self, " is already open.")

    def postTargetOpen(self, action, result):
        broadcastEvent(action.actor,
                       ("You pull on ", self, "'s drawer, but it simply won't open.  ",
                        "It's almost like it's locked, or something.  Almost EXACTLY ",
                        "as if it were locked, in fact..."),
                       (action.actor, " grabs ", self, " and pulls on it, to no effect."))

    def preTargetClose(self, action, result):
        if not self.isOpen:
            raise actions.Refusal(self, " is already closed.")

    def postTargetClose(self, action, result):
        self.isOpen = False
        self.isLocked = True
        broadcastEvent(action.actor,
                       ("You close ", self, "."),
                       (action.actor, " closes ", self, "."))

    def postTargetType(self, action, result):
        try:
            n = int(action.typedIn)
        except ValueError:
            broadcastEvent(action.actor,
                           (self, "'s numeric keypad doesn't seem to be equipped "
                            "to handle your literary urges."),
                           (action.actor, " stares thoughtfully at ", self,
                            "'s numeric keypad."))
        else:
            broadcastEvent(action.actor,
                           ("You type ", str(n), " on ", self, "'s numeric keypad."),
                           (action.actor, " types a few buttons on ", self, "'s keypad."))

            if n == self.code:
                self.isLocked = False
                self.isOpen = True
                broadcastToAll(self,
                               (self, "'s drawer pops open with a noise that "
                                "sounds suspiciously llike *kCHING*!"))
                IScore(action.actor).gainPoints(100, "register")


class Crap(components.Adapter):
    """You don't want to pick this up, really.
    """
    __implements__ = (containment.ITakeTarget,)

    def preTargetTake(self, action):
        """get crap

        I *said* you didn't want it.
        """
        # XXX This needs to broadcast to observers too, but how?
        raise actions.Refusal(action, ("You really don't want to pick that up.  "
                                       "You feel you would be somehow... "
                                       "tainted by it -- It's the stench, if there is such a thing... "
                                       "You don't want it."))


class GenderChanger(components.Adapter):
    """A gender changer.

    This sort of object won't be available in most games (I hope).
    """
    __implements__ = (IPushTarget,)

    transitionMap = {'m': 'f',
                     'f': 'n',
                     'n': 'm'}
    state = 'm'

    actorDescriptions = {'m': 'masculine',
                         'f': 'feminine',
                         'n': 'neutral'}
    otherDescriptions = {'m': 'masculinity',
                         'f': 'femininity',
                         'n': 'gender-neutrality'}

    def postTargetPush(self, action, result):
        b = IGenderedBeing(action.actor)
        if b.gender == self.state:
            broadcastEvent(action.actor,
                           "You press the button, but nothing interested "
                           "happens.",
                           (action.actor, " presses the button on the gender "
                            "changer, but nothing happens."))
        else:
            b.gender = self.state
            self.state = self.transitionMap[self.state]
            toActor = self.actorDescriptions[b.gender]
            toOther = self.otherDescriptions[b.gender]
            broadcastEvent(action.actor,
                           ("You press the button and there is a blinding "
                            "flash of light... When your vision clears, you "
                            "feel a great deal more ", toActor, "."),
                           (action.actor, " presses the button on the gender "
                            "changer and there is a blinding flash of ",
                            toOther, "."))

class Subparser(english.Subparser):
    simpleTargetParsers = {'pull': Pull,
                           'squeeze': Squeeze,
                           'push': Push,
                           'drink': Drink,
                           'dance': Dance}
    simpleToolParsers = {'wind': Wind}

    def parse_type(self, player, text):
        text, targetName = english.rsplit1(text, ' on ')
        if targetName:
            return [Type(player, targetName, text)]
        return []
english.registerSubparser(Subparser())
