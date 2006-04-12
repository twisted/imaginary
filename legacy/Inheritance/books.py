"""
Various books you find in your uncle's chateau.
"""

from Reality.thing import Thing

class ReadableThing(Thing):
    """ Generic simple readable book type thing. """
    """ This includes:
             Ford Runabout Brochure
             Estate Lawyer's Note
             Grandfather's Will
             Letters (Correspondence)
             Rejection Notice
             News Clippings
             Research
             Sheet Music
             Leaflet """

    def verb_read(self, x):
        """ read the book, displaying its read_text message """
        x.subject.hears(self.read_text)

class ReadableBook(Thing):
    """ More complex book-like thing, with turnable pages and such.
        You often fail to turn pages with gloves on.

        This includes:
             Hieroglyph Translator (Large Leather Bound Book)
             Necronomicon (and notes)
			 Volume G-M of The Golden Bough, a guide to magic and mysticism (abridged version), bookmarked to H, "Harvest Ceremonies And Corn Gods: He Who Walks Behind The Rows". (Thank you, Sir James George Frazer, and of course, Stephen King)
             Diary
             Lab Notebook
             The Fantastical Mr. Sahtaan (thank you P.L. Travers, Glyph, and Lucifer Morningstar.)
             Photo Album
             Je Roi En Jaune """
    pass

class Necronomicon(ReadableBook):
    """		 
    A partial german translation of the book commonly referred to as
    the Necronomicon, complete with illustrations, the centerpiece to
    many classic Lovecraft stories. This is the book your grandfather
    has been obsessing over, and it holds the rituals he has been
    using to summon and bind the servants of the old ones. It also
    contains the rites which, if performed correctly, might allow you
    to undo some of what he has done. (Only an inserted set of pages
    in the middle of the book are actually readable, the rest are
    simply described as being horrible and unintelligible, although
    there should still be just enough that you can flip through
    manually for it to be confusing.)

    You can douse it in kerosense and burn it, too, but afterwards
    your character will realize that it was probably a fatal skip
    of logic to destroy the book before completing the ritual.

    The book contains a few rituals, and is interspersed with your
    grandfather's handwritten notes (when you turn pages, it might
    have a few different descriptions of the funny german stuff and
    strange illustrations you go past to get to the next set of notes
    he inserted). It describes how to make/fork/gesture the elder sign
    (looks sort of like the Spinal Tap salute... Oy! Satan! Argh!) at
    the elder spirits, and includes a ritual of binding (both in
    english and arabic), a ritual of summoning, and rituals of opening
    and closing.  Opening and closing involve a bell, a candle, the
    book, special incense, and an incantation, to be repeated three
    times (say words, ring bell) at a "holy" spot, followed by
    extinguishing the candle and closing the book. (The only
    difference between opening and closing is the words.) The ritual
    of binding is just an elder sign followed by some words.

    The ritual of summoning is fairly complex, and if you try to do it,
	you get possessed by something and go insane (and die). Outside the
	house, it might bring big nasty, to eat you immediately.

    The ritual of opening will seem to be working and then eventually
    fail in most places, with a sense that the borders between this
    world and the great aeons were too thick. performed in the
    clearing by the fountain, a gate will tear through the sky and
    into the darkness beyond, and a thousand eyes will watch as your
    soul is picked apart by the old ones. Uh, and you die, and
    stuff. And the world is doomed. +200 points for style, -1000
    points for the eventual enslavement of and consumption of your
    species and destruction of the universe as you know it.

    The ritual of closing will also not work in most places, but at
    the forest clearing, it will drive back all that should not be
    into the abyss forever... or at least for a while. All the
    monsters disappear and are replaced by appropriately colored
    stains of ichor. You win.

    Doing either ritual and having it fail results in the feeling that
    you've really screwed things up and should consider suicide or
    restarting.

    The ritual of binding involves forking the elder sign at the elder
    minion and repeating a phrase in arabic. If you fork the sign at
    big nasty, it will hold still for a moment, unless it's pissed off
    already.  If you say the incantation in english, it gets fed up
    and just eats you.  If you say the incantation in arabic, it bows
    it's head and slinks off into the woods and never bothers you
    again.
	
    """

    def verb_read(self, sentence):
        sentence.subject.hears("You read the necronomicon.  And go crazy and die.")
        sentence.subject.destroy()

class Translator(ReadableThing):
    """
    A ReadableThing that can be used to translate (glean extra
    information from) special, otherwise unreadable objects. In this
    case, objects with hieroglyphics. A more generic version would
    have the name of the property it translates as a string property,
    rather than being hardcoded the way this is.
	
    Used for "A Practical Guide to Egyptian Hieroglyphs, by Lord
    Rutherford P. Beaucavage, Esquire". Ancestor of Melvin
    C. Buttcavage, who is apparently a real life person somewhere. No,
    seriously.

    This does what it sounds like it does... Namely, it gives vague
    symbolic translations of the egyptian hieroglyphs found on a few
    of the artifacts in the house. See the Sarcophagus object for an
	example.
    """
    autoverbs={"translate":"with"}

    def verb_translate(self, sentence):
        """ translate something (preferably something with hieroglyphs) """
        obj = sentence.directObject()
        hiero = getattr(obj, 'hieroglyphics', '')
        if hiero:
            sentence.subject.hears(hiero)
        else:
		    sentence.subject.hears("That doesn't seem to have any hieroglyphics on it... Or anything else that this book might help you to translate.")

class LeRoiEnJaune(ReadableBook):
    """	
    A rather obtuse play in two parts, based on the fictional book
    described byRobert W. Chambers (one of lovecraft's influences) in
    the real book of the same name. After reading the introduction and
    an excerpt from a poem recited in the first act, it begins to
    become rather confusing, and any additional attempts to read it
    leave the player somewhat disoriented, eventually causing them to
    pass out. The player would then have a strange dream about a lost
    city, a pallid mask, and a King in Yellow, which they might not
    wake up from. (This doesn't have much of a connection to any of
    the other plot elements in Inheritance, but it is the sort of
    thing we can integrate later if we get bored.)
    """

    def verb_read(self, x):
        k=King("King in Yellow")
        k(description = ("Woah.  He looks totally fucking nasty.  Like, I "
                         "can't even tell you."),
        location = x.place)
        
    
