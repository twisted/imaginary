"""
Some 'friends' your grandfather never told you about...
"""


from twisted.reality import thing
from twisted.python.delay import StopLooping
from random import randint
from twisted.python import reflect, observable

class Sarcophagus(thing.Thing):
    """
    One of the more interesting trinkets in your grandfather's library, the
    sarcophagus is still sealed, and set with a number of translatable runes
    that give you hints on how to open it. It does contain a useful item or
    two, but it unfortunately also contains the (understandably possessive)
    owner of those items.

    The hieroglyphics property contains the string returned when you translate
    the runes with the appropriate book.
    """

    hieroglyphics='After flipping through the voluminous pages of the guide, you identify some of the symbols. "To sleep/rest of the Longest River(Nile), future/distant shall rise the devoted slave/servant to Nya-Leh-Hotep".'

    def verb_open(self, x):
        x.subject.hears("The cover is far too heavy; it feels as if it were bolted in place.")

class Monster(thing.Thing):
    """
    So far we have 3 monsters planned.
    """

    def __init__(self,*args):
        apply(thing.Thing.__init__,(self,)+args)


class Mummy(Monster):
    """

    "Put it back. Bury it where you found it. You have read the curse. You dare
    defy it?"

    The mummy is probably the most straightforward and well-defined monster. It
    is very simple. After solving a puzzle, the mummy will exit its sarcophagus
    and spring to life. After being confused for a short time (probably 1 event
    cycle which ~=30sec) it will begin chasing the player. It is very slow.
    When a player is in a room with it, it will first "lock on" to the player
    (The mummy is stumbling towards you!), then attack the player. If it
    succeeds in attacking the player, the player will first be "tainted", then
    killed. When a player leaves a room that the mummy is in, it remembers the
    direction that the player left in, and will leave in that direction next.
    If it can't find the player again, it wanders randomly. Being a mummy, and
    still kind of cranky and stiff from getting up after 4000 years or so, it
    can't do stairs too well. If it attacks you successfully a second time, it
    probably latches it's bony hands around your throat and strangles you,
    Boris Karloff style.

    Being tainted means that you have contracted a horrible rotting disease
    from the Mummy and will eventually die and get Glyph's sarcastic You Have
    Died message; This disease can also be contracted by touching the dead
    mummy. If the mummy has been burned to death, it's safe. You should also be
    okay if you wear the Gloves when taking items off of it's body. I was
    originally going to have it so that if you contracted the disease simply by
    touching the corpse, your hands would start to itch, and you had a chance
    to go and wash them or something first, but I'll have to see if we feel
    like doing a Kitchen Sink/Hand Washing API. ;-) In any case, if you get the
    disease from the mummy attacking/biting you, you're just fscked. The mummy
    will actually go down if you shoot it a couple times, but as explained
    above, it's just as dangerous when it's dead if you don't burn it.

    The mummy is wearing The Amulet, a special object that does nothing but be
    wearable. Well, and allow you to complete the more powerful rituals in the
    Necronomicon. But that's about it. Speaking of rituals, it doesn't really
    give a shit about the elder minion ritual of binding, because it's a mummy.
    And your grandfather never did find the papyrus that had what you'd need to
    say to it (and no one is quite sure how to pronounce ancient egyptian in
    the first place).

    Missing the mummy with the gun means you hit a limb or the body to no
    effect, but hitting it means you hit it in the head, killing it. (to be
    true to egyptian mythology, you'd shoot it in the heart, but the heart was
    removed and put in a jar. As was the brain, but if I learned anything from
    horror movies, it's "aim for the head".) If you hit it with the mallet, it
    is both injured and driven back... A second hit will destroy it. If you hit
    it with the sharpened knife, wrench, or spade/shovel, it is hurt but
    doesn't really stagger much. (You should run away and hit it again when it
    enters the room, before it "locks on" to you.) Those weapons should take
    more like three hits. The rake and the foil just knock it back.  Sometimes.
    The straight razor doesn't have much visible effect against the dried,
    leathery skin, and bones, but does give it a good chance to grab at you,
    and for you to possibly hurt yourself with the evil cursed thing. Only
    dousing it and burning it will actually kill it AND disinfect the amulet
    for you. Optionally, we could have weapons used to hit it get moldy and
    nasty, and infect you if you don't discard them soon.

    Thanks to Arthur Conan Doyle, who wrote some spooky stories about mummies
    and why you shouldn't fuck with them (Lot #249, and The Ring Of Thoth) and
    british sensationalist news for the idea that mummies carry a hideous
    disease rather than a "curse".
    """

    def __init__(self, *args,**kw):
        apply(thing.Thing.__init__,(self,)+args,kw)
        # self.loop(3, self.shuffle, ())

    def verb_touch(self, sentence):
        self.reality.later(self.reality.loop,2, (Rot(),3,(sentence.subject,)))
        sentence.subject.hears("You touch ",self,", and begin to feel mildly queasy...")

class Rot:
    def __init__(self):
        self.count=0

    rotting=["Your hand itches a little bit.",
             "Your hand itches, and feels a little funny.",
             "Your hand feels tingly and numb.",
             "Your hand is numb, and you feel a slight pain in your lower arm.",
             "Half of your body is itching and burning like crazy.  You feel very ill, and the scent of death and rot lingers."]

    death_message="""\
Your intreped experiment in archeology having failed, you find yourself now \
content to wander the halls of this bizarre mansion for the rest of eternity, \
occasionally moaning, occasionally feasting upon the flesh of the unwary who \
wander within its depraved walls.  After a while you realize that this is \
unusual, but the irony of your torment is now beyond your cursed cerebellum's \
grasp.
"""

    def __call__(self,player):
        if hasattr(player,"pure") and player.pure:
            raise StopLooping()
        if self.count > len(self.rotting)-1:
            player.hears(self.death_message)
            player.destroy()
            StopLooping()
        player.hears(self.rotting[self.count])
        self.count=self.count+1

class Doll(Monster):
    """
    The doll is a bit quicker than the mummy, and more subtle. It is also
    dormant when the game starts, but much easier to activate.

    There will be a room with a few dolls and other collectible items up on a
    shelf. One of these dolls is a large disturbing wood and porcelain specimen
    that bears a striking resemblance to Dear Departed Grandma shortly before
    she died of consumption. You can pick the doll up, but it's sort of bulky,
    and if you ever leave it alone somewhere (or where no one can see it, like
    in a dark room), it won't be there when you come back. And if you are ever
    in the dark while carrying it, it will tumble out of your arms, and not be
    there by the time you get the lights back on.

    Once "activated", the doll won't attack you directly, but it is somewhat
    grue-like. If you end up in a Dark Place inside the mansion, and stay there
    for any length of time, you will start hearing skittering noises and
    then... well, something bad happens. (I think it would be cliche for the
    doll to kill you with a steak knife, but it's what immediately comes to
    mind. ^_^) Also, once the doll is active, if you ever try to go up or down
    any stairs in the dark, you trip over something and fall to your
    death. (You can read somewhere that one of the last housekeepers your
    grandfather kept in his employ fell down the main spiral staircase and
    broke her neck, and that after some investigation it was eventually blamed
    on a light going out.)

    And yes, I was also going to have it appropriate the steak knife if it was
    left on the floor or in it's original spot in the kitchen, but it will
    probably do something equally horrible to you if the knife isn't
    available. (Taking the knife is more of a "psyching out the player" thing.)

    Note that you can douse the doll in kerosene and light it up the first time
    you see it, but this uses up your only reliable light source, and requires
    that you get it to a well lit place first anyway, or light match /
    extinguish lantern / open lantern / splash kerosene on doll / light doll
    (or something) in less than 30 seconds, without the match going out. ;-)

    Your character is also willing to shoot it or hit it with the hammer, which
    will destroy it.

    Thanks to all the countless authors who wrote horror stories with
    spooky dolls in them, and to whomever came up with the idea of
    trapping souls in vessels shaped like their original bodies at the
    time of their death.
    """

class King(Monster):
    """
    "Not upon us, oh King, not upon us!"

    (If the "Le Roi En Jaune" makes it into the game) The King In Yellow is a
    symbolic figure of death, decay, and insanity, but if you are trapped
    inside of the symbolic imagery of a book called "The King In Yellow", he
    can be dangerous. The KIY is a nebulous, half seen figure, but where flap
    the tatters of the King, songs unsung must die unheard, so watch out.
    """

class BFNT(Monster):
    """
    The Big Nasty Thing is out in the woods somewhere. This is one of your
    grandfather's last experiments, and probably the most successful, although
    you will later learn that his original intentions had been much
    different. It thinks of the house, particularly the cellar, as 'home'; It
    can get into the house, and while it probably will go down the shallow
    stairs to the cellar, it cannot climb the spiral staircase to the second
    floor. It is essentially unkillable, twice as fast as the mummy, and
    hungry.

    It will behave in very cinematic (read: inconsistant) ways in multiplayer,
    as it's primary job is to kill players who attempt to leave the map (via
    the Darkened Road areas). Later on in the evening, when the weather
    worsens, it will return to the house, and attempt to gain entrance via the
    back or front doors... (it doesn't like the rain, and is startled by loud
    noises, like thunder) Although it will still come for you if you try to
    leave.

    I pictured it working sort of like a Wumpus... i.e. if you are in an area
    that it happens to be prowling, there is a chance that it will wander
    somewhere near you, and you will be able to hear it coming from adjacent
    rooms, usually with a directional indication. It doesn't actually have to
    wander around for real; It might actually make more sense to have it more
    or less teleport around. (If it's in the same general "zone" as you (inside
    house, front lawn, back lawn, darkened road, cornfield, etc.) you hear it
    occasionally, and if it's near you, you get more of a warning and a
    direction as well.)

    If it is in the same room as you, you have a brief ammount of time to react
    before it lunges and Pretty Much Just Kills You (TM). This delay could
    either be slightly randomized, or act sort of like a Zork
    monster... i.e. it will actually stare at you for a few seconds, sizing you
    up, and while it will attack you after a little while, it will also spring
    on you if you do something that doesn't drive it away.  I was also thinking
    about maybe having it keep track of which direction players entered the
    room from, or keep track of which direction it had entered in if it was
    actually wandering... The idea being that you could stumble into the room
    it was in and then flee the way you came, but if you tried to just rush
    past it, it would roll right up and eat you.

    While you can't really kill it, you can stun it or scare it away. Some
    actions will confuse or startle it, causing it to increase the delay before
    it attacks/moves: Creating a new light source (lighting a match/lantern) or
    setting something on fire, Firing the gun (in general), attempting to
    attack it with a melee weapon, or anything else that might make it think
    twice about just jumping on you. A few things will Scare It Away, which
    causes it to howl pitiably and run off (out of the house if in the house,
    and towards the darkened road if outside, although it pretty much just
    teleports when this happens) and just guard the exits for a while (say,
    5-10 real time minutes): Successfully shooting it with the gun, starting
    the Runabout until it produces "its customary ungodly racket, followed by a
    deafening backfire", or dousing it with kerosene and setting it on fire. In
    most of these cases, actually shooting it in the face is the only thing
    that should work more than once... (some are limited by resources, but
    others it just should not care the second time, like lighting a match or
    firing the gun and not hitting it. Just stick booleans onto it, like
    LoudNoiseScared, LightScared, etc.) Particularly, if you scare it off with
    the runabout (RunaboutScared), its first order of business upon coming back
    should be to find it and fsck it up bad. (this should probably be audible
    everywhere, and kill anyone inside the runabout at the time, as it is left
    a ruined pile of twisted metal and canvas.)

    It's emotional scale basically goes:

        Gone for good
        Fleeing
        Wandering
        Paused
        Observing
        Attacking
        Enraged

    If you burn it with kerosene, shoot it with the gun, or clock it a
    few times with the mallet, it will take off and not come back.

    If you successfully hit it with the mallet once, play the flute for the
    first time, or fork it the elder sign, it will Pause for a minute (hurt and
    surprised, confused and curious, or fearful, respectively) and then go back
    to observing or attacking you (enraged, in the case of hitting it with the
    mallet and then just standing there.)

    If you hit it with the wrench or the spade, it pauses and seems annoyed,
    and then kills you. Hitting it with the wrench or spade again just enrages
    it (HitScared?).

    Hitting it with the foil or the rake or anything else just enrages it, and
    it instantly kills you.

    Thanks to T.E.D. Klein, another student of Lovecraft, for "Petey",
    the inspiration for the big nasty thing and the Call Of Cthulhu
    module I wrote that later became this game.
    """

    def __init__(self, *args,**kw):
        apply(thing.Thing.__init__,(self,)+args,kw)
        self.reality.loop(self.scuttle, 3)

    def verb_take(self, sentence):
        """ You can't pick up the big nasty thing, and that's that. """
        sentence.subject.hears("NO! You must be out of your friggin' MIND!")
    verb_get = verb_take

    def when_place_enter(self, sender, channel, event):
        thing = event.mover
        if hasattr(thing,'edible') and thing.edible:
            thing.hears(self.nounPhrase,
                        " looks at you with a huge carnivorous grin!")

    def scuttle(self):
        if self.place is None: return
        x = self.place.exits
        if x:
            y = randint(0,len(x)-1)
            direction=x[y]
            foo = self.place.findExit(direction)
            bar = self.place
            self.location = foo
            if bar:
                for i in bar.things:
                    i.hears('A huge nasty thing slithers %sward.'%direction)
            if foo:
                for i in foo.things:
                    i.hears('A huge nasty thing slithers into where you are!')

observable.registerWhenMethods(BFNT)
