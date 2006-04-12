"""
Various implements of destruction that will aid you in your quest to
stay alive a few more hours.
"""

from twisted.reality import thing, clothing, lock

from random import randint

class Leaflet(thing.Thing):
    """
    This is a readable object which provides you with a brief introduction to
    the game.
    """

class KeyRing(thing.Thing):
    """
    A broadcast container that only holds keys. Found amongst the gore
    that was once your estate lawyer.
    """

class Key(lock.Key):
    container_class=KeyRing
    """
    Keys should probably have their own class, so you can at least tell the
    character if they're being a total idiot or just an unlucky or inobservant
    idiot. ("unlock bedroom door with shed key" should probably have a
    different error than "unlock bedroom door with mummy".)

       Rusty Key (unlocks shed, in groundskeeper's clothes)
         Yale Lock Key (unlocks front and back doors, on estate lawyer's keyring)
       Small Brass Keys (unlock bedrooms, on estate lawyer's keyring)
         (Square Handled Brass Key, Round Handled Brass Key)
       Small Silver Key (unlocks workroom, in/on bedroom cabinet)
    """
    keyTypes = []


class Whetstone(thing.Thing):
    """
    This handy object is very heavy, but can be used to sharpen things.
    namely, the kitchen knife. You shouldn't even need to pick it up,
    but if you're a real masochist, you can.
    """

class Flute(thing.Thing):
    """
    The flute is engraved with odd egyptian and non-egyptian symbols, and is
    found in the crate in the basement, having arrived after your grandfather's
    death and left there by the estate lawyer.

    You can play the flute randomly ("play flute") and get a description of the
    eerie, echoing sound it makes, or play one of the pieces of sheet music,
    which will cause the sarcophagus to open from the inside as the mummy
    awakens if played in the same room. The other sheet music, attributed to
    one Erich Zann, is a violent, jolting series of high piping notes, and will
    do nothing other than to cause the Big Nasty Thing to become enraged and
    immediately attack you.

    (playing the egyptian or random music will cause the Big Nasty thing to
    stop and cock it's head to the side for a turn, but only once. Note that
    you can't play the flute with the gloves on.)
    """

    def verb_play(self, sentence):
        """play <music> on flute (or play flute, play <music> with flute)
        """
        player = sentence.subject
        sarcophagus = self.reality['sarcophagus']
        if player.place is sarcophagus.place:
            # TODO: activate the mummy
            pass


class SheetMusic(thing.Thing):
    """
    There are two pieces of sheet music: One apparently plucked after much
    research from a book about traditional egyptian religious ceremonies, and
    the other a work by one Erich Zann, a reknowned violinist who went insane
    and vanished into obscurity some time ago. One is more useful than the
    other.
    """

class Cudgel(thing.Thing):
    """
    Generic class for blunt objects you hit things with, like croquet mallets
    and rakes and what have you. Some are more effective than others.

       Croquet Mallet: Probably the most effective melee weapon in the game. It
       packs a good wallop, and can be used to shatter the doll (it's the only
       weapon aside from the gun your squeamish character seems willing to turn
       on the doll), bonk the big nasty thing on the nose, and wonk the mummy
       into a pile of nasty putrescence. I would assume you'd have to hit the
       Mummy more than once, but a successful hit (only a minor chance of
       missing) would stagger it back. See the Big Nasty Thing for more info on
       how it reacts to melee attacks.

       Spade/Shovel: Also digs. Moderately effective for bashing or stabbing at
       things, but not as hefty or effective as the mallet.

       Kitchen Knife: Not really a cudgel, but you can hit things with it. And
       stab, slash, and kill them. (Once it's sharpened, anyway.)  Moderately
       effective once it has been sharpened.  Can be used to commit suicide.
       (Yay!)

       Wrench: A hefty little metal thing that does inflict some damage, and
       could be used to beat down the mummy if luck is on your side, in
       addition to it's other use.

       Rake: Also rakes. Pretty worthless as a melee weapon, although it may
       annoy monsters and drive them back for a turn, but just makes the Big
       Nasty Thing angry.

       Foil: Not really a cudgel... But it can hit and kill and stab and thrust
       at things. Much like the rake, it unfortunately only annoys and drives
       back the monsters your character is willing to use it on.

       Straight Razor: Again, not really a cudgel, but capable of being used as
       a weapon. A very feeble, annoying weapon. Using it on the monsters
       should pretty much just piss them off and get you killed, but it is
       sharp, and can be used to cut the violet, or slit your wrists, but
       that's about it. In fact, it really does seem to want to do that...

       Shears: Rusted shut. They should cut and snip, but they don't. Mostly
       they feebly swat at things and transmit tetanus.
    """

class Wrench(Cudgel):
    """
    The wrench is a cudgel which can also be used to turn the rusty valve that
    supplies gas to the stove, allowing it to be used to bake and thus dry
    various deadly flowers for use in obscure religious ceremonies.
    """

class StraightRazor(thing.Thing):
    """
    The Straight Razor is a straight razor, stained with some dark reddish
    brown gunk, found in the bathroom of the Opposite Bedroom.  It seems your
    grandmother used this to take her own life when her illness was at it's
    peak. It is very sharp, and can be used to cut the violet or slit your own
    wrists.

    It's also cursed. It can be opened and closed (the blade is attached to a
    handle which it can swing in and out of) and when you open it, close it,
    pick it up, drop it, or use it to cut something, it will seem to shift
    slightly in your hands or slip and cut you. The first time, nothing
    happens, but each time you manipulate it after that, it should start acting
    funny and have an increasing chance that it hurts you (often ending in you
    dropping it, which requires that you pick it up again) and/or causes a
    strange, compelling urge to draw it across your wrist, until some point at
    which you attempt to do something with it and instead find yourself
    committing suicide and smiling calmly to yourself.

    If you just pick it up, open it, and use it, you should only be threatened
    and maybe drop it and get a superficial cut... but if you play with it too
    much, it should become more likely that you will kill yourself with it
    rather than successfully use it to cut something (other than yourself).
    """
    # Is the razor open or not?  (Starts closed, but will be open in the map.)
    opened = 0
    # How fucked are you?
    use_count = 0

    def _use(self, actor):
        "cause the razor to be 'used', invoking the curse upon it"
        # TODO: add some randomness to this.
        self.use_count = self.use_count + 1
        if use_count == 1:
            self.reality.later(
                func=actor.hears,
                args=("Faintly, you hear a sad voice, whispering to you...",))
        if use_count == 5:
            self.reality.later(
                func=actor.hears,
                args=("A voice calls to you, and you feel a staggering weight of despair.",))
        if use_count > 10:
            if self.opened:
                actor.hears("You draw ",self," slowly across your wrists, smiling calmly to yourself... finally at peace.")
                actor.destroy()

    def verb_cut(self, sentence):
        player = sentence.subject
        # TODO: what kinds of things can be cut, and how do they react?
        self._use()

    verb_kill = verb_cut

    def verb_open(self, sentence):
        "open razor -> open the straight razor"
        if self.opened:
            Failure("It's already open.")
        self._use()
        self.opened = 1

    def verb_close(self, sentence):
        "close razor -> close the straight razor"
        if not self.opened:
            Failure("It's already closed.")
        self._use()
        self.opened = 0



class Stove(thing.Thing):
    """
    The Stove is a container with a dial on it. If the valve on the tanks on
    the back of the house is closed, it does nothing, although you can open and
    close the door. If the valve is open and the dial is set to something other
    than off (the dial has "Off" and 200 through 500 in 50 point increments) a
    faint hissing noise description element appears in the room (and in the
    oven) and gas starts to come out. If you put a match in the stove or try to
    light the stove or the gas, the stove turns on, and begins to become warm.
    If the gas stays on without the stove being on, the kitchen will eventually
    develop a strong scent of gas, and lighting a match inside it will cause an
    explosion that kills you.

    If you put the flower in the oven and leave it in there with the door
    closed and the temperature above 300 degrees for a few turns/minutes, wisps
    of smoke and a strange aroma will start to come from the oven, and if you
    open the door, the flower will be withered and dried. If you leave it in
    there with the door closed for a few more turns, it crumbles into a
    strange, useless, ashy powder, and you get a message about probably having
    done something very, very dumb.
    """


class Brazier(thing.Thing):
    """
    A fairly passive object whose primary purpose is to have dried violet
    nightshade burned in it. Burning the nightshade otherwise will result in it
    blowing away or going out in the wind/rain/etc.  This is, of course, a
    fairly important part of the Big Ritual that will end the game, one way or
    another.  ;-)

    The Violet Nightshade will burn in the brazier and produce a translucent,
    purple smoke that makes you dizzy (and also makes the ritual possible) for
    several turns or a few minutes, but not forever... If it runs out and the
    game isn't over, you feel you have missed a vital opportunity.
    """


class Gun(thing.Thing):
    """
    What would a survival horror game be without a gun! It might not be your
    standard-issue combination shotgun/flamethrower with a laser sight, but it
    does shoot. See Bullet for more info.

    When you pull the trigger on the gun, not much happens initially.  The
    hammer needs to be drawn back before the trigger will make it fall, and hit
    the bullet in the chamber. Also, there will be no bullet in the chamber
    until the slide is racked (and a bullet is pulled up from the clip... so
    there must be one or more bullets in the clip for that to succeed). Racking
    the slide also cocks the hammer.

    When you find the gun, the safety is on. (this should be fairly obvious,
    although we could be mean and not mention it implicitly until you try to
    fire it.) The Colt 1911 also has an integral grip safety, which I don't
    feel like going into in detail... But it means that the gun won't fire
    without someone gripping the handle, so the gun won't go off if you drop it
    or even fall down the stairs with it stuck into your waistband.

    When the gun is successfully fired, the force of the blast also racks the
    slide for you, thus ejecting the shell casing, cocking the hammer, and
    chambering the next round. If the gun misfires (the bullet doesn't go off,
    about %25 with your bullets), nothing much happens at all.  You can cock
    the hammer back and pull the trigger again to fire that same bullet, or
    rack the slide to eject the bullet (thus chambering the next one and
    dumping the current one out onto the floor.) To be extra nasty, there could
    be a small chance after a successful firing that the gun jams; The shell
    casing doesn't eject and/or the slide doesn't rack. In that case, you have
    to rack the slide repeatedly until it clears (the shell falls out, and the
    gun is racked normally, thus making it ready to fire again).

    Guns weren't terribly useful in Lovecraft's books, either. Special thanks
    to Drew Gleason for clearing up some of the info on automatic pistols and
    the Colt 1911 in particular.

    """
    must_hit = 0
    misses = 0

    def verb_shoot_with(self, sentence):
        d=sentence.directObject()
        x=self.must_hit or not randint(0,100)
        if self.things and self.things[0].things:
            clip = self.things[0]
            bullet = clip.things[0]
            casing = Casing(bullet.name+" casing")
            casing.description = "This is the casing from a %s."%bullet.name
            casing.location = sentence.subject.place
            bullet.destroy()
        else:
            sentence.subject.hears("*click*")
            return 0
        if x:
            sentence.subject.hears("** BANG! **  The gun's aim is true!  You hit ",d,'!')
            d.destroy()
        else:
            sentence.subject.hears("** BLAM! **  Your hand is jerked forcefully out of line with the target, and the bullet goes wide.")
            self.misses=self.misses + 1
            if self.misses == 2:
                self.must_hit = 1

    verb_fire_with=verb_shoot_with

    autoverbs={"shoot":"with",
               "fire":"with"}


class TypeContainable(thing.Thing):
    """
    An object which can be contained by another class of object.
    """
    def verb_put(self, sentence):
        container=sentence.indirectObject("in")
        if (isinstance(container,self.container_class)
            and sentence.directObject() is self):
            if self.location is not container:
                self.location = container
                sentence.subject.hears("You put ",self," in ",container,".")
            else:
                sentence.subject.hears(self, " is already in ",container,".")
        else:
            raise thing.InappropriateVerb()

class Clip(TypeContainable):
    container_class=Gun
    """
    It should accept both literal and conceptual commands (both "load gun" and
    "put clip in gun", maybe even "load gun with clip" like it used to) and
    keep most of the functionality of the original (rackable slide, misfires,
    etc).
    """
    def verb_load(self, sentence):
        "load <gun> with <clip>"
        self.verb_put(thing.PseudoSentence(
            subject=sentence.subject,
            verb="put",
            objects={"":sentence.indirectObject("with"),
                     "in":sentence.directObject()}
            ))

    autoverbs = {"load":"with"}

class Casing(thing.Thing):
    """ An expired bullet. """

class Bullet(TypeContainable):
    container_class=Clip

    """
    As noted earlier, the ammo fairy hasn't visited this mansion yet either, so
    you've only got the bullets that your grandfather actually purchased for
    it. That means you have a dented bullet, a dirty bullet, and a moldy
    bullet. Strangely enough, all three will work -- however, you're not a very
    good shot (%50 - %75 against moving targets like the mummy and the Big
    Nasty), and the gun may misfire (%25 chance?), ejecting the bullet without
    it going off and requiring that you rack the slide again. If you
    successfully fire two bullets, you are guaranteed to hit your target on the
    third try if you haven't already. You may, of course, hit more than that if
    fate smiles upon you. (Fat chance.)

    The only exception is if you have attempted to wash the bullets in the
    sink, in which case the washed bullets will never fire.

    If Hit:

    The doll shatters into bits (accompanied by distant screaming and crying
    sounds. Missed shots against the the mummy count as ineffective hits to the
    body or limbs, but if a hit takes it in the face, and it collapses into a
    tangled mass of bones, dried wrappings, and crumbling flesh on the floor
    with the amulet embedded in it (the amulet as well as the mummy bits are
    still quite poisonous) and the Big Nasty Thing is injured enough that it
    will run away and not come back for a while.  (Firing the gun will also
    make it cringe away from you and revert to observation/normal mode, and
    possibly send it into Flee mode.)
    """

class Kerosene(thing.Thing):
    """
    The Kerosene can be poured into the lamp, out onto the floor or onto a
    specific thing/object (Monsters, the doll, the book, the flower, etc.) and
    lit. If it or anything else soaked in it is ignited on the floor of the
    house (not the dirt floor of the basement or a non-flammable container like
    the sink or the tub) the fire will spread the next turn (and your character
    can muffle/stamp/extinguish/put it out) and then spread to fill the room,
    driving the character out a random exit. It will spread from room to room
    and eventually burn down the house, changing the description of the house
    scenery object and making it impossible to enter, which fucks up the game
    if you don't have all the necessary ritual stuff out of the house yet. It
    can also trap you and burn you to death.
    """
    # TODO: This really should be a subclass of library.substance.Fluid.
    # Implementing that class is probably non-trivial.

class Lamp(thing.Thing):
    """
    There is an old brass lantern here, beeyotch. The lantern can be opened and
    closed, and contains kerosene. You can also pour/put kerosene into it. When
    lit, it slowly consumes the kerosene. It has a nice brass-capped glass
    flute on the top to protect the flame from wind and rain. The cap seems
    sort of loose when you take it off or put it on.

    When you pick it up, you should get a little message indicating how much
    kerosene seems to be sloshing around in it. (A lot, some, not very much,
    roughly equivalent to %100, %67, %33). When it is below %10, it should
    start to flicker and dim and gutter and mutter and sputter and otherwise
    indicate that it is running out of fuel.

    The lantern should start with a relatively small ammount (%10?) enough to
    run for a while, but it should start to flicker almost immediately.

    If you throw it at/hit something with it, the flute shatters, the cap comes
    off, and the thing is drenched in burning kerosene (only if the lantern is
    lit, of course.) and becomes a light source for a while. (see Kerosene for
    other side effects of things being on fire.) The doll will burn away into a
    twisted mass of nastiness, accompanied by distant screaming and crying; The
    Mummy will stagger around (easily avoided by your character) and then
    collapse and burn away into a pile of ash with the amulet gleaming in it.
    The big nasty thing will make and awful screeching roaring sound, run away,
    and not come back. If this happens in a part of the house with a wood
    floor, and not in a non-flammable container (the sink, a tub, the dirt
    floor of the basement) the fire starts to spread, until it fills the room
    and drives the character out through a random exit, at which point it
    quickly spreads to the rest of the house and destroys it. If you are ever
    trapped by the fire, you get a trapped and burned to death message. (You
    should also get the "You've probably done something irrevocably bad"
    message if you burn the house down while important house stuff isn't done
    yet.

    The first Lovecraft story I read, "The Shuttered Room", ended with the
    titular occupant being set on fire with a kerosene lantern and then
    crashing through a window. Although that story was written shortly before
    his death and finished by August Dereleth, so it's not clear how much of
    that was actually his idea.
    """


class Candelabra(thing.Thing):
    """
    Doesn't do much, aside from holding a bunch of candles for you. Otherwise,
    candles won't stay lit if you aren't holding them (they fall over and go
    out when you drop/put them.)
    """

class Candle(TypeContainable):
    container_class = Candelabra
    """
    Temporary light source that tends to go out sporadically, especially strong
    winds, and run away into nothing after a while. Handy for arcane rituals.
    Goes well into a Candelabra.
    """


class Matchbook(thing.Thing):
    """
    These are for feeding to the psychic worms on level 3. Yum! They love
    sulphur! Ahem. That was sarcasm. They're for lighting the lamp, and they
    can also make fire, but less of it. They don't last long as light-sources
    go (about 2 moves or so, or 60 seconds in multiplayer). You should be able
    to light them in the dark, with some difficulty, but holding a lit match as
    a light source should be inconvenient (affects your ability to carry lots
    of stuff, has a chance of going out prematurely when you move, etc.)

    While wearing the gloves, you should have a good chance of dropping matches
    while you attempt to get them, and always either break the match or drop it
    when attempting to strike them.

    You can't put matches back into the book, since you're essentially tearing
    them out of it.

    H.P. Lovecraft had an odd habit of calling matches "lucifers", which will
    probably end up being the brand name printed on the cover. 
    """


class Match(thing.Thing):
    """
    See Matchbook. Since these are matchbook matches, they basically suck and
    can't just be struck on any old surface, only the matchbook.
    """
    def verb_strike(self, sentence):
        sentence.subject.hears("If this worked, you would strike the match here, but only if it were on the matchbook.")

    verb_light = verb_strike


class Knife(thing.Thing):
    """
    It starts the game in the knife rack, which I think a lot of players may
    overlook. You can use it to cut a few things... But for the most part, it
    really isn't that useful. Unlike the other random useless objects you can
    find, there are some places you could use it, and it could also be used as
    a weapon, (although given the circumstances, it's really not that useful.)

    The knife will now start off dull, but be sharpenable with the whetstone.
    It's primary uses are as a weapon, and to cut the Violet Nightshade.

    In H.P. Lovecraft stories, knives are usually wielded by insane people or
    used to slit the wrists of sacrificial victims.
    """

    def verb_cut(self, x):
        x.subject.hears("You attempt to cut ",x.directObject(),
                        ", but the knife isn't very sharp.")

class Gloves(clothing.Gloves):
    """
    A pair of thick leather work gloves, the only wearable item you will
    probably find in Inheritance. While wearing the gloves, your hands are
    protected from various nasty poisonous things described later. There's no
    real drawback to wearing them, although I think since they're thick and
    described as being too big for you, it should drastically increase the
    chance of breaking/dropping matches when you try to light one, and taking
    them on/off might require that you put your stuff down first. (Put all on
    table? ;-)

    While wearing the gloves, you will probably fail or drop matches when you
    attempt to get them, and always drop or break them when attempting to
    strike them. (broken matches are useless.) You also can't play the flute,
    load bullets into the gun, and intermittently fail to turn	pages in books.

    The gloves begin the game locked in the shed.
    """


class Nightshade(thing.Thing):
    """
    This was originally going to be part of the ritual the player needed to
    perform to undo what his or her grandfather had started. The plant
    essentially needs to be burned as incense, but it is growing in the strange
    patch of woods near the west end of the Darkened Road, and is covered in
    poisonous thorns as well. If you aren't wearing gloves when you pick it,
    you get poisoned (and die after hallucinating for a little while) and if
    you handle it later without the gloves, there is still a chance of it
    happening.  Addendum: It's also firmly attached to the stem, so you'll need
    the knife or the shears. If you keep tugging on it with the gloves on, the
    thorns will eventually poke through the glove with preternatural ease, and,
    well, kill you.

    Note: The knife has to be sharpened, and the shears are rusted and
    basically useless. Also, if you remove the gloves while carrying the
    nightshade, it will most likely poke (and poison, and kill) you... The same
    goes for handling it.

    It also needs to be dried... This can be accomplished by putting it in the
    oven and baking it for a while. (See the Oven for more info.)

    Lovecraft occasionally mentions odd plants and whatnot as manifestations of
    Eldritch influence and as a part of rituals.
    """

    def verb_eat(self, sentence):
        sentence.subject.hears("Oh, you die.  You go to hell, and you die.  Like, really.  You die a lot.  bad.")
        sentence.subject.destroy()

    def verb_take(self, sentence):
        sentence.subject.hears("Assuming you had something to cut the stem with in the first place, you've just poked (and poisoned) yourself on one of the many tiny thorns of this delicious plant. There should be some time-delay stuff happening here, but we'll deal with that later.")
        sentence.subject.destroy()

