from twisted.reality import *

from twisted.library.furniture import *
from divunal.dream import Cloudscape
t=reference.Reference
m=reference.AttributeReference
def d(**kw): return kw

Room('A Crumbling Stairway')(
	theme='crack',
	description='Nothing special.',
	exits={'up': t('Wrecked Street, curve')}
)

Room('A Dark Narrow Passage')(
	inhibit_exits='true',
	theme='greystone',
	inhibit_items='true',
	display_name='A Dark Place',
	OBSOLETE_super=t('Class_Dark Room'),
	exits={'south': t('A Small Opening'), 'north': t('A Small Dark Crevice')},
	description="It's too dark in here to see!"
)

import twisted.library.clothing
twisted.library.clothing.Pants('a pair of black slacks')(
	place=t('Tenth'),
	synonyms=['slacks'],
	clothing_appearance='black slacks',
	description='A creased, loose fitting pair of black pants.'
)

Room('A Small Dark Crevice')(
	inhibit_exits='true',
	theme='greystone',
	inhibit_items='true',
	display_name='A Dark Place',
	OBSOLETE_super=t('Class_Dark Room'),
	exits={'south': t('A Dark Narrow Passage'), 'north': t('Deeper In The Rock')},
	description="It's too dark in here to see!"
)

Room('A Small Opening')(
	inhibit_exits='true',
	theme='greystone',
	inhibit_items='true',
	display_name='A Dark Place',
	OBSOLETE_super=t('Class_Dark Room'),
	exits={'south': t('Silver Shadowed Glade'), 'north': t('A Dark Narrow Passage')},
	description="It's too dark in here to see!"
)

Thing('a small piece of plaster')(
	place=t("Damien's Cubicle"),
	description='A white box.'
)

Room('A Swirling Mass Of Colors')(
	description='A swirling, chaotic mass of colors... Or whatever else Tsiale wants it to be.'
)

import twisted.author
twisted.author.Author('Aaron')(
	health='1.0',
	stamina='0.0',
	health_time=938212952099L,
	gender='m',
	OBSOLETE_super=t('Class_Human'),
	description=observable.Hash({'__MAIN__': 'A tall young man with blond hair.\012', 'clothing': [m('Aaron','him_her'), ' is wearing ', 'Faded brown coat', '.']}),
	stamina_time=938212952099L
)

twisted.author.Author('Agatha')(
	oldlocation=t("Agatha's Lighthouse"),
	description=observable.Hash({'__MAIN__': 'Shadows settle  all around Agatha. She seems at once bathed in a soft glow and obsured in darkness, with the exclusion of a string of clear faceted stones encircling her throat. The necklace reflects a source-less light in all directions, tossing a shards of light on everything in the vicinity. She looks asleep at the moment. if you check back in a little while, perhaps she will be awake. ', 'clothing': [m('Agatha','him_her'), ' is wearing ', m('dazzling necklace','noun_phrase'), ', ', m('midnight blue cloak','noun_phrase'), ', ', 'and ', m('pair of brown leather boots','noun_phrase'), '.']}),
	OBSOLETE_super=t('Class_Human'),
	gender='f'
)

Room("Agatha's Lighthouse")(
	exits={'west': t('Lonely Expanse of Beach')},
	description="The fieldstone light tower stretches toward the sky, standing proud against the assault of the sea and decades of neglect. The beacon  stands cold and unusable. A cascade of vines and yellow lichen hides the west face of the tower. Copper drainpipes and rooftops are a riot of green oxide trails. The light keeper's cottage looks as if it's been recently occupied after years of vacancy.  A few of the dangling shutters have been removed and neatly stacked, the oak front door reattached and the sand swept away from the smooth stones forming the path.\012A simple oil lamp burns in the window. "
)

twisted.author.Author('Agent Moore')(
	oldlocation=t('Obscure Corner of Bookstore'),
	OBSOLETE_super=t('Class_Human'),
	description='He is non-descript.  He is wearing a suit.  There is nothing more.'
)

Thing('agility dial')(
	component=1,
	place=t('Genetic Laboratory'),
	synonyms=['agility', 'dial'],
	value='0.25',
	OBSOLETE_super=t('Class_Player Creation Dial'),
	description='A white box.'
)

Thing('aging leather tome')(
	place=t('great bookshelf'),
	synonyms=['leather tome', 'tome'],
	page_1='The sucessful sourcerer needs many things to accomplish his task, but primarily, an open mind is required, as well as a soul willing to experiment, and a heart willing to believe.',
	page_number=1,
	page_3="Required ingredients\012\012-   a sprig of sage\012-   one vial of moonshine\012-   a spider's web\012-   the eye of a newt",
	page_2="The cauldron is the most important part of any spellcaster's posessions.",
	OBSOLETE_super=t('Class_Book'),
	description='The aging leather tome is open to page 1. It reads:\012"The sucessful sourcerer needs many things to accomplish his task, but primarily, an open mind is required, as well as a soul willing to experiment, and a heart willing to believe."'
)

Room('Aisle 1.')(
	theme='paper',
	description=observable.Hash({'__MAIN__': 'An array of important-looking tomes of different shapes and sizes are displayed on the shelves here. Each is titled with the name of a geographical location - the smaller ones, cities and towns, the larger ones, provinces and countries. You can exit the aisle to the south and there is a marble arch in the wall at the north end of the aisle, holding a stainless steel door.', 'stainless steel door closeDesc': 'A large steel door blocks the northern exit.'}),
	exits={'south': t('Main Aisle, East End'), 'north': t('Grand History Book Room')}
)

Room('Aisle 2.')(
	theme='paper',
	description="A series of short, squat books sit on the shelves here. All the books look the same. The aisle ends abruptly to the north, almost in the middle of a shelf, in a wall. The wall isn't quite straight, and this place looks poorly maintained. You can exit the aisle to your south.",
	exits={'south': t('Main Aisle, Center')}
)

Room('Aisle 3.')(
	theme='paper',
	description='You are in an aisle filled with miscelleneous types of books, all stacked together on shelves with no apparent organization. You can exit into a wider aisle to the south, or continue on to an unusual curve to the north.',
	exits={'south': t('Main Aisle, West End'), 'north': t('Odd Curve')}
)

Room("Anah's Room")(
	exits={'north': t('Cylindrical Mansion Hallway')},
	description='This room is very white - and depicts an interesting dichotomy.  On the west wall, there is a bed, sheeted completely in white linen, covered with an huge group of stuffed animals which spill over onto the floor.  On the wall to the east, there is a rack for edged weapons of all sorts.  The dominant feature of the room, however, is the southern wall, which is a huge, wide window overlooking a pine forest immediately after a snow storm.  The boughs of the trees are heavily laden with snow, and they glisten in the late sunlight.'
)

Thing('analog clock')(
	component=1,
	place=t("Damien's Cubicle"),
	synonyms=['clock'],
	description='On the wall is a small, white analog clock. It is round, with thick black hands. It appears to be three minutes fast, but there is no readily obvious way to set it to the correct time.\012\012The minute hand is silver underneath the black paint, a few flakes of paint have begun to flake off. A few centimeters below the center of the clock the word Seiko is written, and underneat it, Quartz.\012\012The clock has a small silver border.'
)

Thing('ancient tome')(
	place=t('Rikyu'),
	synonyms=['tome', 'spellbook'],
	spell_2='posess',
	spell_1='zorft',
	spell_0='frotz',
	OBSOLETE_super=t('Class_Spell Book'),
	description='A small black book, covered in a sort of fake-leather. A loop on the side looks like it might hold a pen of some sort.'
)

Thing('apple')(
	place=t('Tsiale'),
	OBSOLETE_super=t('class_apple'),
	description="A juicy red apple, with smooth lush curves to make any man's mouth water.\012"
)

Chair('armchair')(
	maximum_occupancy=1,
	place=t('Smoking Room'),
	synonyms=['chair'],
	preposition='in',
	player_preposition='sitting in',
	description='An rather nondescript armchair.'
)

Room('Armory')(
	theme='greystone',
	description='This room still contains numerous rusted sets of armor, but all the lances, bows, arrows, and rifles have been taken from the racks that once contained them.  There is a large archway leading southwest, and a short and narrow door leading to the north.',
	exits={'southwest': t('Great Dome'), 'north': t('Small Arched Tunnel')}
)

Room('Art Gallery')(
	theme='paper',
	description='This is an interesting art gallery. There is a painting on the north wall of a mansion toppled on its front door, with its roof pointing towards the viewer, and to the west there is a hole in the wall framed as if it were a picture. Through the hole you can see a winding rock path sloping up over a field of clouds to an architecturally impossible castle. There is a metal spiral staircase downward.',
	exits={'west': t('Portrait in the Sky')}
)

Room('Art Room')(
	exits={'southwest': t('More Mansion Hallway')},
	description='This room is heavily spattered with paint, graphite dust, papers, eraser-residue, and various other side-effects of artistic endeavor.  A lone easel stands in the center of the room, on a pedestal.'
)

Thing('attic staircase')(
	obstructed='true',
	component=1,
	place=t('Mansion Upper Hall'),
	synonyms=['stairs', 'staircase'],
	description='A white box.'
)

Room('Autumn Chamber')(
	exits={'west': t('Cylindrical Mansion Hallway')},
	description='The ground here is a bed of slightly crisp leaves.  The walls are covered with a tapestry of rich browns and reds, abstract, but nevertheless reminiscent of the season.  The air is cool and clean, and smells of the forest. On the east wall, a large rectangular window overlooks a forest of pine trees, whose needles have turned an interesting array of bright colors.  '
)


Thing('bamboo teascoop')(
	place=t('Rikyu'),
	synonyms=['teascoop', 'scoop', 'bamboo scoop'],
	OBSOLETE_super=t('Reality Pencil'),
	description='A rather nondescript bamboo teascoop.'
)

Thing('Battered Document')(
	place=t('Damien'),
	synonyms=['document', 'battered', 'social', 'social contract', 'contract', 'pencil'],
	OBSOLETE_super=t('Reality Pencil'),
	description='You quickly skim the battered parchment. Apart from an introduction that goes on for great length about life being "nasty, brutish and short" the document appears to contain clause after clause of  complex jargon. The initial section, headed "Social Contract" mostly deals with ettiquette and the moral justification (and lack thereof, see article 32, page 247) of killing and eating one\'s neighbors. A later section, entitled "S.C. Adendum" has a series of handwritten clauses. A sample clause reads, "Clause 49a, sub-section R28: Small Velvet Cushion: And hithertofore with such legalities and commisions as stated in the above acts and legeslative derivatives, there shall be created a small cushion constructed of... of pillow stuff and covered in velvet".'
)

Thing('battered gray door')(
	thereOpenDesc='The east door is open.',
	openDesc='The west door is clearly open.',
	obstructed='false',
	component=1,
	place=t("Michelle's Dorm Room"),
	synonyms=['door'],
	closeDesc='The west door is closed.',
	OBSOLETE_super=t('Class_Door'),
	description='A rather nondescript battered gray door.',
	thereCloseDesc='The east door is clearly closed.'
)

Thing('bauble')(
	frotzed='true',
	place=t('demo cash register'),
	isLit='true',
	description=observable.Hash({'__MAIN__': 'A small, shiny object, that catches the light and gleams in a rather valuable looking sort of way. ', 'lighting': ['A pure white glow eminates from ', m('bauble','noun_phrase'), ', bathing ', m('bauble','him_her'), ' in light.']})
)

Room('Behind House')(
	exits={'southwest': t('South of House'), 'northwest': t('North of House'), 'east': t('Clearing 2'), 'west': t('Kitchen(1)')},
	description='You are behind the white house. A path leads into the forest to the east. In one corner of the house there is a small window which has had the shutters pulled off of it, ruined beyond repair.'
)

Room('Between the Cliffs')(
	theme='water',
	description='This is a path between two very high cliffs.  The path is lit by bright moonlight shining through and reflected from the clouds above.  To the south the path becomes sandier and widens into a beach, and to the north, it becomes a dirt path through a pine grove.',
	exits={'south': t('Moonlit Beach'), 'north': t('Pine Grove')}
)

Room('Between the Rubble')(
	theme='leaf',
	description="You are between the pieces of rubble which probably once comprised the western wall of a large castle.  The castle's walls are about fifty or sixty feet thick, making this rubble a fairly long expanse to plod through, but there is a path between the debris.  This wall has been in a state of disrepair for some time now, judging by the age and size of the trees growing here -- some of the well-trimmed shrubs visible in the courtyard appear to have taken root and flourished here.  The rest of the castle is off to the east, where the path between the rubble leads into the small courtyard.  To the west, the rubble thins out, and you can see more trees.  The castle's wall seems unusual.",
	exits={'east': t('Castle Courtyard'), 'west': t('Clearing in Small Forest')}
)

Thing('billboard')(
	component=1,
	place=t('Twisted Reality Corporate Demo Center'),
	synonyms=['board'],
	description='This is a ten-foot-tall gleaming white billboard, with clear, black, sans-serif writing that begins in huge three-foot-tall letters and proceeds down to a small ten-point font.  It reads:\012\012"Welcome to the Twisted Reality Demo Center!  A few basic commands that will guide you through this magical land of corporation fun are:\012\012LOOK: this lets you look at stuff.  Try it on objects both in the room\'s description and in the object-list in the upper right hand corner.\012\012SAY: This command is macro-bound to your \' key.  You can use this to interact with other players.\012\012GO: This lets you move.  You can also use the numeric keypad (with NUM-LOCK on) to move in the cardinal and secondary compass directions - also, 0 is \'up\' and 5 is \'down\'.\012\012SMILE: it\'s polite.  You can just SMILE or SMILE AT someone.\012\012These are not all of the verbs you can use, by any stretch of the imagination.  Some situations may also call for OPEN, CLOSE, TURN or SIT.  If the game says something snide to you, it\'s likely that the verb you\'re looking for doesn\'t work in that context.  Another good rule to keep in mind is that the parser will understand you in the form: "verb [direct-object] [preposition indirect-object] so sentences like "slowly use the tongs to give bob the fish", "north, please" or "I\'d sure like to go north right now, wouldn\'t you?" are not going to work quite right.  Try instead "give fish to bob with tongs" or "go north".\012\012Thanks for playing, and we hope you enjoy the demo!'
)

Container('bin')(
	component=1,
	place=t('Mansion Entrance Hall'),
	theme='wood',
	synonyms=['metal bin'],
	OBSOLETE_super=t('Class_Container'),
	description='A hollow black metal cylinder about three feet high.'
)

Thing('black and red postcard')(
	place=t('Other New Jersey Apartment Bedroom'),
	synonyms=['card', 'postcard'],
	description='A small, worn, glossy postcard. The front side is a photograph of Colonial Williamsburg at night, lit by the time-lapsed glow of reddish yellow fireworks, and the back is covered in small, neat handwriting, and a cute drawing of a knight standing at attention.'
)

Room('Black Hallway')(
	theme='greystone',
	description='This is a solid onyx hallway with an arched ceiling.  It continues north into the distance for a long while, and south into another, brighter hallway.',
	exits={'south': t('Jewel Bedecked Hallway 2'), 'north': t('Black Hallway')}
)

Thing('black plastic cable')(
	component=1,
	place=t('Mansion Main Hall'),
	theme='wood',
	synonyms=['plastic cable', 'cable'],
	description='A long, thin cable, coated with a glossy black plastic.'
)

twisted.author.Author('Blake')(
	oldlocation=t('A Crumbling Stairway'),
	description=observable.Hash({'__MAIN__': 'A man of average height and medium build, with deep green eyes and cropped blond hair. He carries himself casually, but with an air of continual alertness. ', 'clothing': 'He is wearing a dark green shirt, a pair of tan cargo pants, and a pair of sturdy leather boots.'}),
	OBSOLETE_super=t('Class_Human'),
	gender='m'
)

Room("Blake's Sphere")(
	theme='default',
	description='You are inside of a hollow brushed steel sphere that is approximately 10 feet in diameter. The sphere is lit by a ring of glowing material set into its horizontal circumference. There is a small brass plaque set into the base of the sphere. There is also a sphere chair here.'
)

Container("Blake's Sphere of Stuff")(
	place=t('Blake'),
	synonyms=['box', 'sphere'],
	description='About one foot across, this steel sphere looks as if it is meant to hold things. Part of the sphere is hinged, to open and close. The words "Blake\'s Sphere of Stuff" are stenciled on it.'
)

Thing('blank wall')(
	component=1,
	place=t('Natural Alcove'),
	synonyms=['wall', 'right wall'],
	description='The wall feels very solid and slightly damp. It is covered in moss, and there is a fairly large crack at its base. It also has, much to your surprise, an oil painting hanging from a small nail.'
)

Thing('blue box')(
	component=1,
	place=t('Ivy Garden'),
	description='A rather nondescript blue box.'
)

Thing('Blue Charting Pencil')(
	place=t('Agatha'),
	OBSOLETE_super=t('Reality Pencil'),
	description='A rather nondescript Blue Charting Pencil.'
)

twisted.library.clothing.Tunic('blue-grey vest')(
	place=t('Jedin'),
	synonyms=['vest'],
	clothing_appearance='a medium-grey vest',
	description='A sturdy, medium-grey fabric on the back and sides meets a darker leather on the front of the garment.  The blue tinge is so slight as to make its effect seem more of an impression than something directly perceived.  Three midnight-blue buttons adorn the front of the vest.  '
)

Thing('blueprints')(
	component=1,
	place=t('Mansion Maintenance Closet'),
	synonyms=['blueprint'],
	description='A disordered pile of blue drafting paper covered in unintelligible handwriting and illustrations. Most of the text seems to be in an odd scientific notation, while the illustrations focus on a complex, interconnected system of gears and clockwork. A few pages are devoted to listing the dimensions of various gears, wheels, and rods, and one particularly long sheet is covered in a fantastically complicated set of tables and boxes, all filled with strange three-character sequences of letters and numbers.'
)

Player('Bob')(
	oldlocation=t('Demo Center East Wing'),
	stamina_time=943948804325L,
	health='1.0',
	stamina='-0.58383834',
	isLit='false',
	health_time=943948804325L,
	gender='m',
	OBSOLETE_super=t('Class_Player'),
	description='Bob is an incredible specimen of virile manhood, as powerful as he is senual, all at once the most beautiful and terrifying thing you have ever seen. If you are a woman, you are struck instantly by his obvious sexual potency and skill, and if you are a man, you cower as his cold and powerful gaze passes over you.'
)

Container('Book Box')(
	place=t('Class Room'),
	synonyms=['box'],
	description='A perfectly white box labeled "Book Classes" in neat black letters.'
)

Thing('Book of Patchwork')(
	place=t('Twin'),
	synonyms=['book'],
	page_1='Book of Patchwork (1:1) Dear reader, within these pages are fragments of the collective destiny of the twin books (the books of Patchwork - this is the main tome, Dingo, Clouds, Ivy, Rings, Nymphs, Euphoria, Lions, Tigers, and Labrinths). Be warned that improper use of their teachings can and will lead to spread of the glitch. As volumes of new readers misuse and fall prey... new books shall arrive. Take care... reader.',
	page_number=1,
	page_2='Book of Euphoria (174:312) [Systematic proposal on the obliteration of frantic warfare in the <removed> together with numbers 1, 2, 4, and 9] On one three-dimentional afternoon, I decided to take a walk in the form of a nearby algorhythm. Little did i know, a glitch hid just around the corner....',
	OBSOLETE_super=t('Class_Book'),
	description='The Book of Patchwork is open to page 1. It reads:\012"Book of Patchwork (1:1) Dear reader, within these pages are fragments of the collective destiny of the twin books (the books of Patchwork - this is the main tome, Dingo, Clouds, Ivy, Rings, Nymphs, Euphoria, Lions, Tigers, and Labrinths). Be warned that improper use of their teachings can and will lead to spread of the glitch. As volumes of new readers misuse and fall prey... new books shall arrive. Take care... reader."'
)

Thing('bookshelf')(
	component=1,
	place=t("Damien's Study"),
	description='A simple, metal bookshelf, held together by screws and a sticky, web-like substance. All of the edges are carefully covered, perhaps someone was child-proofing here?'
)

Thing('bookshelf door')(
	yellow_pushed='false',
	obstructed='true',
	exit_message='You squeeze between the bookshelves through the door.',
	component=1,
	place=t('Science Fiction Room'),
	theme='wood',
	steam_source=t('Mansion Steam Engine'),
	steam_off=926639534319L,
	description='A blue box.',
	obstructed_message="You can't go that way."
)

Room('Bookstore Stairwell, Level 10')(
	exits={'north': t('Science Fiction Room'), 'up': t('Bookstore Stairwell, Level 11'), 'down': t('Bookstore Stairwell, Level 9')},
	description='This is a plain marble spiral staircase, leading both up and down. There is a door here in the north wall that leads to this floor of the bookstore, that has the number "10" written on it.'
)

Room('Bookstore Stairwell, Level 11')(
	exits={'northwest': t('Empty Hallway'), 'down': t('Bookstore Stairwell, Level 10')},
	description='This is a plain marble spiral staircase, leading both up and down. There is a door here to the northeast that leads to this floor of the bookstore, that has the number "10" written on it.'
)

Room('Bookstore Stairwell, Level 4')(
	exits={'up': t('Bookstore Stairwell, Level 5')},
	description='This is a plain marble spiral staircase, leading only up. There is a chalk drawing of a door here that has the number "4" written on it.  Strangely, the stairs end in a wall here, with no purpose for their continuation this low.'
)

Room('Bookstore Stairwell, Level 5')(
	exits={'up': t('Bookstore Stairwell, Level 6'), 'southeast': t('Granite Reception Room'), 'down': t('Bookstore Stairwell, Level 4')},
	description='This is a plain marble spiral staircase, leading both up and down. There is a door here that leads southeast to this floor of the bookstore, that has the number "5" written on it.'
)

Room('Bookstore Stairwell, Level 6')(
	exits={'northeast': t('Rare Book Room, Upper Level'), 'up': t('Bookstore Stairwell, Level 7'), 'down': t('Bookstore Stairwell, Level 5')},
	description='This is a plain marble spiral staircase, leading both up and down. There is a door here that leads northeast to this floor of the bookstore, that has the number "6" written on it.'
)

Room('Bookstore Stairwell, Level 7')(
	exits={'southwest': t('Odd Curve'), 'up': t('Bookstore Stairwell, Level 8'), 'down': t('Bookstore Stairwell, Level 6')},
	description='This is a plain marble spiral staircase, leading both up and down. There is a door here to the southwest that leads to this floor of the bookstore, that has the number "7" written on it.'
)

Room('Bookstore Stairwell, Level 8')(
	exits={'up': t('Bookstore Stairwell, Level 9'), 'northwest': t('Nondescript Section'), 'down': t('Bookstore Stairwell, Level 7')},
	description='This is a plain marble spiral staircase, leading both up and down. There is a door here to the northwest that leads to this floor of the bookstore, that has the number "8" written on it.'
)

Room('Bookstore Stairwell, Level 9')(
	exits={'south': t('Myth Section'), 'up': t('Bookstore Stairwell, Level 10'), 'down': t('Bookstore Stairwell, Level 8')},
	description='This is a plain marble spiral staircase, leading both up and down. There is a door here in the southern wall that leads to this floor of the bookstore, that has the number "9" written on it.'
)

Thing('brass cockroach')(
	winds=0,
	place=t('Greenhouse Entrance'),
	synonyms=['cockroach', 'roach'],
	windable='true',
	repop=t('Greenhouse Entrance'),
	description='A small mechanical cockroach, intricately designed with all of the parts and details of a real insect, made entirely of polished brass. There is a small hexagonal keyhole between two of the plates of its thorax.'
)

Thing('brass label')(
	component=1,
	place=t('Twisted Reality Corporate Demo Center'),
	synonyms=['brass labels', 'labels', 'label'],
	description='A tiny, engraved brass plaque, identical to all of the other tiny engraved brass plaques attached to their respective potted plants, bearing the legend:\012\012     "Artificial Potted Plant (Model 86003)"\012  \011     "Copywright 1793 GUE"\012"Frobozz Magic Artificial Potted Plant Company"\012\011'
)

Thing('brass lantern')(
	place=t('Genetic Laboratory'),
	synonyms=['light', 'lantern', 'lamp', 'brass'],
	isLit='true',
	description="This lamp is so battered and bruised, having survived so many adventures, that it's a wonder it survives at all. It is currently on and the switch is stuck, so you can't turn it off!"
)

Thing('brass paperweight')(
	place=t('Tenth'),
	synonyms=['pager', 'paperweight'],
	description='A short brass dome about the size of a coffee cup, with a small glass lens set into its center.'
)

Thing('brass pocketwatch')(
	place=t('Tenth'),
	synonyms=['watch', 'pocketwatch'],
	OBSOLETE_super=t('Reality Pencil'),
	description='divunal.tenth.WatchDisplay',
	base_description='A large, well-polished brass pocketwatch, fitted with a number of extra dials, buttons and controls, and attached to a thin metal chain.'
)

Player('Brasswheel')(
	synonyms=['gyro', 'gyroscope'],
	painting_looks=-3,
	oldlocation=t('Science and Technology Vehicle Area(2)'),
	OBSOLETE_super=t('Class_Human'),
	description=observable.Hash({'__MAIN__': "Several concentric hoops of polished brass, each spinning rapidly on it's own independant axis and surrounded by a more stationary spherical framework of the same material.", 'floating': 'It is suspended in the air at about chest level by some incomprehensible force.'}),
	display_name='brass gyroscope'
)

Thing('brightly colored manual')(
	place=t('Proper English Library'),
	synonyms=['manual'],
	description='35 Quick Steps to Mastering the X57:\012An Introduction to the New Generation \012of Foreign Residual Income Distribution.\012\012It looks friendly and quite easy to read... for a CPA.'
)

Thing('Brita Water Filter')(
	place=t('New Jersey Apartment Refrigerator'),
	synonyms=['filter', 'water filter', 'brita filter'],
	description='A sleek transparent pitcher filled with clear water, with a white plastic filter assembly and handle.'
)

Thing('broken handmirror')(
	place=t('Guyute'),
	synonyms=['handmirror', 'mirror'],
	description='The mirror glass has been broken into a slew of tiny glass fragments. It appears to have been thrown in a fit of rage (or fear?)'
)

Room('Broken Office')(
	exits={'north': t('Reception Area')},
	description='This is an office, most likely that of someone in a relatively low position.  Bits of twisted metal lie about the floor, indicating that there may have once been some furniture here.  The walls are undecorated but for a few small, burnt holes, and the space is small.  The smashed remains of a computer terminal litter the floor.'
)

twisted.library.clothing.Shoes('brown expedition boots')(
	place=t('Jedin'),
	synonyms=['leather boots', 'boots'],
	clothing_appearance='a pair of all-purpose brown leather boots',
	description="Despite the obviously thick sides and soles, the hide's soft texture gives these boots a comfortable appearance."
)

twisted.library.clothing.Tunic('brown kimono')(
	place=t('Rikyu'),
	synonyms=['kimono'],
	description='A rather nondescript brown kimono.'
)

twisted.library.clothing.Belt('brown leather belt')(
	place=t('Jedin'),
	synonyms=['leather belt', 'brown belt', 'belt'],
	clothing_appearance='a well-worn brown leather belt',
	description='The complete absence of cracks in the thick leather indicate that this belt has been well-broken in.  Still, the dust-brown hide shows no stains, nor does the rounded gold buckle suffer any marks to mar its smooth, matte finish.'
)

Thing('BummCo Toys ownership guide')(
	place=t('demo gift shop shelves'),
	synonyms=['ownership guide', 'guide'],
	repop=t('demo gift shop shelves'),
	description='A folded piece of white paper, covered in poorly printed lettering. It reads:\012\012"BummCo Toys Proudly Presents the "John Romero: Master of Daikatana" promotional semi-posable talking action figure! Just yank his crank and hear him say any one of 18 colorful phrases."\012\012"WARNING: Highly Flammable. Do not immerse in liquids. Explodes Under Pressure. Not a Food. Rated Grade F (Human Inedible) by the Artifical Food Standards committee. May contain bullshit."\012\012"Thank you for your purchase. BummCo Toys is a trademark and fully owned subsidiary of General Firms (tm)."'
)

Thing('Bun-Bun squeaky toy')(
	place=t('Large Glass Box'),
	synonyms=['squeaky toy', 'toy', 'bun', 'bun-bun', 'bunbun'],
	repop=t('Large Glass Box'),
	description='A grey, white, and vaguely rabbit shaped rubber figurine with long floppy ears and dark, vicious eyes.'
)

Thing('BusinessMind for Jewelers poster')(
	component=1,
	place=t('Messy New Jersey Office'),
	synonyms=['red and white poster', 'poster'],
	description='A large poster of Rodin\'s "The Thinker" sculpture, surrounded by a red and yellow background. It is covered with information about a piece of database software called BusinessMind for Jewelers, and invites you to www.businessmind.com, where you can find more information on "Business Software that thinks the way you do".'
)

Thing('button')(
	component=1,
	place=t('Science Fiction Room'),
	synonyms=['green button', 'yellow button', 'red button', 'red', 'green', 'yellow'],
	steam_source=t('Mansion Steam Engine'),
	steam_off=917227965847L,
	description='A small, round button mounted at eye level on the bookshelf.'
)

Thing('buttons')(
	component=1,
	place=t('Science Fiction Room'),
	theme='default',
	description='Each of the 3 middlemost shelves has a small button attached to it at eye level; From left to right, there is a small green button, a rather ominous red button, and a somewhat less threatening yellow button.'
)

Container('cabinets')(
	component=1,
	place=t('Mansion Study'),
	theme='wood',
	synonyms=['cabinet'],
	description='A set of glass cabinets with dark, polished wooden frames.'
)

Thing('candelabra')(
	component=1,
	place=t('Crumbling Hallway'),
	synonyms=['candles', 'candelabraas', 'candelabras'],
	description='This is an ancient candelabra which appears to have been brushed completely free of cobwebs. You can see fingerprints on its surface, which looks to be brass.'
)

Room('Canyon Bottom')(
	exits={'up': t('Rocky Ledge'), 'north': t('End of Rainbow')},
	description='You are beneath the walls of the river canyon which may be climbable here. The lesser part of the runoff of Aragain Falls flows by below. To the north is a narrow path.'
)

Room('Canyon View')(
	exits={'west': t('Forest 2'), 'down': t('Rocky Ledge')},
	description='You are at the top of the Great Canyon on its west wall. From here there is a marvelous view of the canyon and parts of the Frigid River upstream. Across the canyon, the walls of the White Cliffs join the mighty ramparts of the Flathead Mountains to the east. Following the Canyon upstream to the north, Aragain Fallsmay be seen, complete with rainbow. The mighty Frigid River flows out from a great dark cavern. To the west and south can be seen an immense forest, stretching for miles around. A path leads northwest. It is possible to climb down into the canyon from here.'
)

Thing('carvings')(
	component=1,
	place=t('Small Platform on the Rock'),
	description='The carvings are scrawled in an unusual handwriting, and are shaky, as if they were written by a weak and dying hand.  They read, "hello sailor".'
)

Room('Castle Beach')(
	theme='leaf',
	description='You see a very rocky beach, with a sea to the west, north, and south. To the east, you can see a very small forest, walled by cliffs on either side.  The air is clean and clear here.  There is a tunnel in the rocks leading downward into a stairwell.',
	exits={'east': t('Clearing in Small Forest'), 'down': t('Crumbling Entranceway')}
)

Room('Castle Courtyard')(
	theme='leaf',
	exits={'south': t('Castle Entrance'), 'west': t('Between the Rubble'), 'north': t('Castle Entrance Archway')},
	description="This is the courtyard of a large, white stone castle.  The castle's four towers reach high above here.  The eastern wall is flawless marble, although it exhibits a much better resistance to the elements than actual marble would.  The west wall, on the other hand, while having a similiar texture, is crumbled down in a V shape, as if it had been struck with something from above.  You could easily walk through the chasm formed in the wall, and there appears to be a misty forest that way.  To the south, you can enter the castle proper through a small doorway, and to the north, you can exit through the huge northern gate.",
	display_name='Courtyard'
)

Room('Castle Entrance')(
	theme='default',
	description="This is a minimalistically decorated entrance hall with alabaster-white walls.  Black squares at uneven distances down the left wall punctuate an otherwise featureless room.  A soft, sourceless light illuminates the whole room.  A low doorway to the north leads out into a courtyard, and a small archway southward continues further into the palace's depths.",
	exits={'south': t('Castle Foyer'), 'north': t('Castle Courtyard')}
)

Room('Castle Entrance Archway')(
	display_name='Entrance Archway',
	description='You stand under a very large white stone archway in the walls of a castle.  You notice that the western wall seems a bit ashen and grey, while the eastern one is bright and gleaming.  To the south, you can continue further into the castle, where there is a small courtyard.  You can exit the castle to the north, onto a set of steps.',
	exits={'south': t('Castle Courtyard'), 'north': t('Castle Steps')}
)

Room('Castle Foyer')(
	theme='default',
	description='The polished white floor here is carpeted with a T of red carpet running from archways in the northern, eastern, and western ends of the room.  The southern wall is completely blank.',
	exits={'east': t('Sitting Room'), 'north': t('Castle Entrance')}
)

Room('Castle Greysen Fountain Room')(
	display_name='Fountain Room',
	description='The floor here is made of a black glossy material, but the center of the floor is dominated by a huge inlaid compass.  The arms of the compass are all silver, except the eastern one, which is a shining gold.  The western arm is very slightly tarnished. A large circle in the center of the compass is depressed into the floor, and a fountain is in the center of the depression.',
	exits={'west': t('Sitting Room'), 'southeast': t('East Wing Spiral Staircase Bottom')}
)

Room('Castle Steps')(
	exits={'south': t('Castle Entrance Archway'), 'down': t('Ledge in front of Castle in the Clouds')},
	description='You are standing on a set of beautiful white stone palace steps.  The steps are too stonelike to be ivory, yet too muted to be marble.  They are almost soft as you walk on them.  To your south lies the castle, through a very large stone archway, and down the stairs to the north there is a ledge on which you think you might be able to stand.  A portcullis is visible at the top of the archway: it is wide open.'
)

Thing("Castle's Wall")(
	component=1,
	place=t('Between the Rubble'),
	synonyms=['walls', 'wall'],
	description='The wall of the castle, rather than being hollow to accomodate rooms, is completely solid stone!  From what you can see, this portion of the castle is just a huge smashed block of marble, and it is not now, nor ever was, designed for any purpose but to keep stray animals out of the courtyard.  As it has been split asunder, it no longer serves even that purpose.'
)

Room('Catwalk')(
	exits={'southwest': t('Even More Office Hallway'), 'north': t('End of Catwalk')},
	description='This is a catwalk overlooking a long-abandoned factory from far above.  The shape of this room is interesting.  It is almost completely cubical, except that the southern wall is concave.  This wall has windows at its top, overlooking the work area, and a line of doors along the bottom.  Aside from the equipment on the floor and this one irregular wall, the room is completely featureless.  There is a door to your southwest, leading into the southern wall of the factory.  There was probably once a portal to the east, there is a large rock lodged in the wall where the door may have been.'
)

Container('cement urn')(
	component=1,
	place=t('Ivy Garden'),
	synonyms=['urn'],
	OBSOLETE_super=t('Class_Container'),
	description='Along the rim of the urn there are several Taoist images. The urn itself seems to be very well built, in all...'
)

Thing('chair')(
	component=1,
	place=t("Damien's Cubicle"),
	description='Your eye slides over this object, just another bit of office junk.\012\012You look again, but there are no interesting features.\012\012You force yourself to look hard at this simple chair, and notice that you cannot quite determine the number of wheels. There are definately more than three, but there seem to be less than four... The color is hard to determine, as well... grey? Perhaps a steel blue?'
)

Room('Chasm Bottom')(
	exits={'east': t('Continued Chasm'), 'up': t('More Office Hallway')},
	description='This chasm is very irregular.  The floor is not level here, or even regularly sloping.  You struggle for you balance as you notice that the floor seems to ameliorate slightly to the east.'
)

twisted.author.Author('Chenai')(
	oldlocation=t("Michelle's Dorm Room"),
	description=observable.Hash({'__MAIN__': 'No Description.', 'clothing': [m('Chenai','him_her'), ' is wearing ', m('tupperware lunchbox','noun_phrase'), '.']}),
	OBSOLETE_super=t('Class_Human'),
	gender='f'
)

Room('Class Room')(
	theme='default',
	description='A room with lots of generic, basic looking objects lying about.  The walls are whitewashed and it is entirely nondescript.',
	exits={'southwest': t('Small Gray Dome'), 'south': t('Test Bed'), 'up': t('Small Book Room'), 'north': t('Genetic Laboratory'), 'west': t('Grey Cube Room')}
)

Thing('class_45 ACP bullet')(
	bullet_type='.45 ACP',
	place=t("Tenth's Chamber"),
	OBSOLETE_super=t('class_bullet'),
	description='It appears to be a class_45 ACP bullet, but it is vague, indistinct, and little more than a blurry smear on reality.'
)

Thing('class_apple')(
	eat_text_1='You eat ',
	eat_text_2='. It is juicy and crisp, and quite tasty.',
	place=t('Food Box'),
	OBSOLETE_super=t('class_food'),
	description='It appears to be a class_apple, but it is vague, indistinct, and little more than a blurry smear on reality.'
)

Container('Class_Boat')(
	component=1,
	place=t('Underground Grotto'),
	description='A rather non-descript Class_Boat.'
)

Thing('Class_Book')(
	place=t('Book Box'),
	description='A white box.'
)

Thing('Class_Bookshelf')(
	place=t('Book Box'),
	description='A white box.'
)

Thing('class_bullet')(
	bullet_type='insert bullet type/caliber here',
	place=t("Tenth's Chamber"),
	description='It appears to be a class_bullet, but it is vague, indistinct, and little more than a blurry smear on reality.'
)

Container('Class_Closeable Container')(
	place=t('General Box'),
	OBSOLETE_super=t('Class_Container'),
	description='A blue box.'
)

Container('Class_Container')(
	place=t('General Box'),
	description='A generic container.'
)

Thing('Class_Cube')(
	place=t('Other Box'),
	description='A grey box.'
)

Thing('Class_Dark Room')(
	darkDescription="It's too dark in here to see!",
	place=t('Room Box'),
	isLit='divunal.common.IsLit',
	description='A small black box.'
)

Thing('Class_Dial')(
	place=t('Other Box'),
	description='A white box.'
)

Thing('Class_Door')(
	obstructed='true',
	place=t('General Box'),
	synonyms=['doorway', 'door'],
	obstructed_message="The door is closed.  You can't walk through it.",
	description='This is a regular doorway.  You can OPEN and CLOSE it.'
)

Thing('class_food')(
	place=t('Food Box'),
	description='It appears to be a class_food, but it is vague, indistinct, and little more than a blurry smear on reality.'
)

Thing('Class_Forbidden Exit')(
	obstructed='true',
	component=1,
	place=t('Underground Grotto'),
	description='A rather nondescript Class_ForbiddenExit.'
)


Thing('class_gun trigger')(
	place=t("Tenth's Chamber"),
	description='A blue box.'
)

Player('Class_Human')(
	oldlocation=t('Class Room'),
	OBSOLETE_super=t('Class_Player'),
	description='This player is as-yet undescribed.'
)

Thing('Class_Linking Book')(
	place=t('Book Box'),
	description='A rather nondescript Class_Linking Book.',
	OBSOLETE_super=t('Class_Book'),
	linkTo=t('Obscure Corner of Bookstore')
)

Container('class_pistol')(
	clip_type='insert clip type/caliber here',
	place=t("Tenth's Chamber"),
	slide=t('class_pistol slide'),
	description='A blue box.'
)

Container('class_pistol chamber')(
	place=t("Tenth's Chamber"),
	description='A blue box.'
)

Container('class_pistol clip')(
	clip_type='insert clip type/caliber here',
	place=t("Tenth's Chamber"),
	description='A blue box.',
	bullet_capacity=8
)

Thing('class_pistol clip release')(
	place=t("Tenth's Chamber"),
	description='It appears to be a class_pistol clip release, but it is vague, indistinct, and little more than a blurry smear on reality.'
)

Thing('class_pistol slide')(
	place=t("Tenth's Chamber"),
	description='A blue box.'
)

Player('Class_Player')(
	place=t('Class Room'),
	description='This player is as-yet undescribed.'
)

Thing('Class_Player Creation Dial')(
	minval='-1.0',
	maxval='1.0',
	place=t('Other Box'),
	machine=t('player creation machine'),
	OBSOLETE_super=t('Class_Dial'),
	description='A black dial.  Look at the machine for a clearer description...'
)

Thing('class_simple book')(
	place=t('Book Box'),
	description='It appears to be a class_simple book, but it is vague, indistinct, and little more than a blurry smear on reality.'
)

Thing('Class_Small Book')(
	book_text="The book is mostly in a language you can't understand, and is very uninteresting to you.",
	place=t('Book Box'),
	description='Set the property "book text" to what you want the player to see when they read it.'
)

Thing('Class_Spell Book')(
	place=t('Book Box'),
	description='A rather nondescript Class_Spell Book.'
)

Thing('class_translator book')(
	place=t('Book Box'),
	OBSOLETE_super=t('class_simple book'),
	description='It appears to be a class_translator book, but it is vague, indistinct, and little more than a blurry smear on reality.'
)

Thing('clean book')(
	place=t('Small Book Room'),
	synonyms=['book'],
	OBSOLETE_super=t('Class_Small Book'),
	description='This is an oblong, linoleum-bound book with a shining and clean surface, entitled (according to its cover) "The Tall Kitchen".'
)

Room('Clearing')(
	exits={'east': t('Forest 2'), 'south': t('Forest Path'), 'north': t('Forest 2')},
	description='You are in a clearing, with a forest surrounding you on all sides. A path leads south.\012There is a grating securely fastened into the ground.'
)

Room('Clearing 2')(
	display_name='Clearing',
	description='You are in a small clearing in a well marked forest path that extends to the east and west.',
	exits={'south': t('Forest 2'), 'west': t('Behind House'), 'north': t('Forest 2')}
)

Room('Clearing in Small Forest')(
	theme='leaf',
	description='This is a clearing in a small forest.  You can see high, rocky cliffs in the distance to the north and south, and a castle with a crumbled wall to the east.  The trees seem to thin on a path to the west.',
	exits={'south': t('Southern End of Small Forest'), 'north': t('Northern End of Small Forest'), 'east': t('Between the Rubble'), 'west': t('Castle Beach')}
)

Thing('Cliffs of Insanity')(
	component=1,
	place=t('Northern End of Small Forest'),
	synonyms=['rock wall', 'wall', 'rock', 'writing', 'cliff', 'cliffs'],
	description='This is a very high, very wide rock wall, blocking your passage further north.  Someone has scrawled a passage on the wall in a very thin line of white paint:\012\012\011"The profession of book-writing makes horse racing seem like a solid, stable business.\012\011\011-- John Steinbeck"\012\012The word "John" is underlined several times.'
)


Room('Closed Junction')(
	exits={'east': t('Very Cold Room'), 'north': t('Dent in Tube')},
	description='This is a huge hemi-spherical metal room.  The room is well illuminated, seemingly from nowhere.  There are tunnels branching off in several directions, but most of them look as if they were pinched shut by rocks.  One remains open to the north, and there is a tunnel larger than all the rest leading east.'
)

Container('Clothing Box')(
	place=t('Demo'),
	synonyms=['box'],
	description='A perfectly white box labeled "Clothing Classes" in neat black letters.'
)

Cloudscape('Cloud Scene Balcony')(
	cloudiness=-0.03485268,
	theme='water',
	fling_place=t('Moonlit Beach'),
	exits={'east': t('West End')},
	description=observable.Hash({'__MAIN__': 'You are standing on a semicircular slab of marble, with steps leading outward in all directions... into a layer of clouds! The castle looms high above you, but all you can see into the distance is an unbroken layer of clouds and the moon.  Within a few steps, the stairs in all directions are completely obscured by clouds.  ', 'clouds': "The clouds are as tranquil as a lake on a cool summer's night."})
)

Thing('clue apple tree')(
	component=1,
	place=t('Garden Maze(5)'),
	synonyms=['tree'],
	description='The few apples that remain on this tree are rotten and putrid-looking. In fact, this whole tree looks sickly, including its scrawny trunk.',
	display_name='apple tree'
)

Thing('clue chair')(
	component=1,
	place=t('Garden Maze(4)'),
	description='This chair is rickety and weathered. It might be a good resting place for a weary maze-dweller, but that could be misleading. Painted on the seat is the phrase "A.M. Furniture Co."',
	display_name='chair'
)

Chair('clue first chair')(
	component=1,
	place=t('Garden Maze(12)'),
	synonyms=['chair'],
	display_name='first chair',
	description='A rather nondescript clue first chair.'
)

Chair('clue fourth chair')(
	component=1,
	place=t('Garden Maze(12)'),
	synonyms=['chair'],
	display_name='fourth chair',
	description='A rather nondescript clue fourth chair.'
)

Thing('clue hammer')(
	component=1,
	place=t('Garden Maze(1)'),
	description='A rather new-looking hammer. Etched into the wooden handle are the words: "A.M. Hammer Co."',
	display_name='hammer'
)

Thing('clue leaves')(
	component=1,
	place=t('Garden Maze(7)'),
	synonyms=['leaves', 'pile'],
	description="Where did these come from?!?! There aren't any trees around, though judging by the mold on them they've probably been here a long time. Strangely enough, the mold seems to have grown in the shape of two letters, an A and a M.",
	display_name='pile of leaves'
)

Thing('clue oak tree')(
	component=1,
	place=t('Garden Maze(5)'),
	synonyms=['tree'],
	description='This tree must have been here for hundreds of years, judging by its great girth. Strangely enough, it seems that the trunk has been wrapped with barbed wire, making a climb impossible.',
	display_name='oak tree'
)

Thing('clue paddle')(
	component=1,
	place=t('Garden Maze(4)'),
	description='Row, row, row your boat. The paddle has the letters N and Z etched into the blade.',
	display_name='paddle'
)

Thing('clue rake')(
	component=1,
	place=t('Garden Maze(7)'),
	description='This rake looks like it\'s been here for a really long time. The blades are so rusted, it probably wouldn\'t be of any use, but carved into the pole are someone\'s initials: "N.Z."',
	display_name='rake'
)

Thing('clue scissors')(
	component=1,
	place=t('Garden Maze(1)'),
	description='A pair of stainless steel scissors. The blades bear the words "BookeNZ Scissor Factories."',
	display_name='scissors'
)

Chair('clue second chair')(
	component=1,
	place=t('Garden Maze(12)'),
	synonyms=['chair'],
	display_name='second chair',
	description='A rather nondescript clue second chair.'
)

Thing('clue table')(
	component=1,
	place=t('Garden Maze(12)'),
	description='A rather nondescript clue table.',
	display_name='table'
)

Chair('clue third chair')(
	component=1,
	place=t('Garden Maze(12)'),
	synonyms=['chair'],
	display_name='third chair',
	description='A rather nondescript clue third chair.'
)

Room('coat closet')(
	exits={'south': t("Jedin's Foyer")},
	description='A coat closet looking as if it needs to be described.'
)

Thing('coat rack')(
	component=1,
	place=t('Mansion Entrance Hall'),
	theme='wood',
	synonyms=['rack'],
	description='A rather intimidating six foot high wrought iron structure, balanced on four pointed legs and bearing a number of less dangerous looking metal arms.'
)

Thing('coffee mug')(
	place=t('Proper English Library'),
	synonyms=['mug'],
	description='A slightly cracked white mug with the legend, "Rx-2500--Simple, Fast and Easy" across on side in bold, black letters. There is a dark brown coffee stain inside.'
)

Room('Cold Floor')(
	inhibit_exits='true',
	theme='greystone',
	inhibit_items='true',
	display_name='A Dark Place',
	OBSOLETE_super=t('Class_Dark Room'),
	exits={'southwest': t('Uneven Floor'), 'north': t('Rough Floor'), 'east': t('Plain Room'), 'west': t('Wet Floor')},
	description="It's too dark in here to see!"
)

Room('Cold Room')(
	theme='greystone',
	description="This room looks as if it's simply used to store old junk.",
	exits={'east': t("Guyute's Laboratory"), 'south': t('Western End of Grotto')}
)

Thing('colorful book')(
	place=t('Small Book Room'),
	synonyms=['book'],
	OBSOLETE_super=t('Class_Small Book'),
	description='This is a colorful book with an outrageous pattern on it that looks reminiscent of a cloudy day, except the clouds are all rainbows and the sky is a bizarre gradient.  The title is in large black block letters on the front: "Dropping Acid with Doctor Seuss"'
)

Chair('comfortable sofa')(
	component=1,
	maximum_occupancy=3,
	place=t("Guyute's Laboratory"),
	synonyms=['couch'],
	display_name='sofa',
	description="This fine piece of furniture is upholstered in fine velvet. The legs are carved out of fine mahogany; it certainly seems sturdy, and has room for three. It's obvious that it was crafted by someone who cared an awful lot about sitting."
)

Thing('computer')(
	component=1,
	place=t('Mansion Main Hall'),
	theme='wood',
	synonyms=['terminal'],
	description='A rectangular grey plastic box, labeled "VA RESEARCH VArStation 28", just above the word "Linux" and the icon of a small flightless bird. The box is sitting underneath a small wooden table, on top of which is a grey plastic keyboard and a monitor. Both are attached to the computer by a number of small plastic cables. A larger, black plastic cable attached to the computer leads along the floor of the hall until it rounds the corner through the western archway.'
)

Container('construction frame')(
	component=1,
	place=t('Mansion Laboratory'),
	synonyms=['frame'],
	description='A large interconnected framework of metal scaffolding, reaching up to the ceiling of the room.'
)

Room('Continued Chasm')(
	exits={'up': t('Even More Office Hallway'), 'west': t('Chasm Bottom')},
	description='The chasm is somewhat regular here.  It gets dirtier and more ragged to the south.  Hewn into the wall of the chasm is what looks like a makeshift stairwell leading upwards, and though it is a bit rough and uneven, it appears to be quite serviceable.'
)

Thing('corner')(
	component=1,
	place=t("Damien's Bedroom"),
	description="There aren't any."
)

Thing('cot')(
	place=t("Damien's Bedroom"),
	description='A white rectangular mattress with rounded corners. It looks comfy but hardly luxorious.'
)


Room('Cramped Transporter Booth')(
	exits={'east': t('Reception Area')},
	description='This is a transporter booth - though somewhat cramped.  It looks as though it was once spacious, but one half of the room has been compressed by what look like metal girders that have collapsed, blocking what may have once been an exit to the north.  There is a doorway to the east, beyond which you can see a hallway.'
)

Container('crate')(
	place=t('Mansion Maintenance Closet'),
	description='Several roughly shaped pieces of wood that have been nailed together in a cruel mockery of a box.'
)

Room('Crater Edge North')(
	theme='crack',
	description='You stand at the edge of a large hole.  Its sides slope steeply down, too sheer to scale with ease.  You cannot see any indication of what created this crater; the bottom of the pit looks to be filled with a thick, grey liquid.',
	exits={'east': t('Wrecked Street, north')}
)

Room('Crater Edge South')(
	theme='crack',
	description='DESCRIBE ME!',
	exits={'east': t('Wrecked Street, south')}
)


Room('Crumbling Entranceway')(
	theme='greystone',
	description='This is an old and decrepit hallway. There are stairs here, covered at the top in sand, at the bottom in dust. Candles are mounted high on the walls, providing a feeble yellow light. There is an arched iron sign hanging down from the high ceiling here, reading "Welcome to the West Wing". Rust almost obscures the last word.',
	exits={'west': t('Crumbling Hallway'), 'up': t('Castle Beach')}
)

Room('Crumbling Hallway')(
	theme='greystone',
	description='This is a bit further into the west wing of the castle.  The hall is in a complete state of disrepair. Instead of candles high on the walls, there are candelabras here, almost low enough to reach. In fact, there is one you can reach, about waist level, on the southern wall.  The hallway continues to the east and west.',
	exits={'east': t('Crumbling Entranceway'), 'west': t('Less Crumbling Hallway')}
)

Room('Crumbling Library')(
	theme='greystone',
	description='This relatively small (but still immense) room must once have been a library, judging from the expanse of empty shelf-space and the few remaining books, crumbled to pieces.  The one remaining vestige of the appearance of a true library is the huge dias in the center of the room (which looks as though it may have once held a book), boldly emblazoned "The Encyclopedia".',
	exits={'south': t('Great Dome')}
)

Thing('crumbling piece of papyrus')(
	place=t('Mystic Field'),
	synonyms=['paper', 'piece of papyrus', 'map', 'piece of paper', 'papyrus'],
	description="This ancient item looks as if it's about to disintegrate right in your hands, but you can faintly make out a diagram of some sort:\012\012     +-----------------------||---+\012     X   12   =    13   =    14   |\012     +---||---+----xx---+---------+\012     X   10   |    11        6    \012+----+---||---+----xx---+----xx---+\012| 9  X   8    =    7    =    5    |\012+-xx-+--------+---------+----||---+\012                   3    X    4    |\012              +----xx---+----||---+\012              |    1    =    2    |\012     +--------+----||---+---------+\012     |                            |\012     +----------------------------+"
)

Room('Cube Room')(
	inhibit_exits='true',
	theme='greystone',
	inhibit_items='true',
	display_name='A Dark Place',
	OBSOLETE_super=t('Class_Dark Room'),
	exits={'down': t('Secret Cave')},
	description="It's too dark in here to see!"
)

Thing('curves')(
	component=1,
	place=t('Mansion Upper Hall'),
	synonyms=['pattern', 'intersecting lines', 'lines'],
	description='The curves and lines woven into the carpet create a sinuous, elaborate pattern. It is difficult to focus on any one part of the design, and it almost seems to be shifting and changing as you watch. The effect is hypnotic, looking almost as if the lines were waving in a slow, repeating motion.'
)

Room('Cylindrical Mansion Hallway')(
	exits={'south': t("Anah's Room"), 'west': t('Spring Chamber'), 'north': t('Summer Chamber'), 'east': t('Autumn Chamber'), 'southeast': t('Slanted Mansion Hallway')},
	description='This is a small octagonal room with a domed ceiling, with four large doors in the cardinal directions, and one smaller one to the southeast.  The walls here are completely white, and a soft light eminates from the ceiling.'
)

twisted.author.Author('Damien')(
	oldlocation=t('Obscure Corner of Bookstore'),
	theme='default',
	isLit='false',
	gender='m',
	OBSOLETE_super=t('Class_Human'),
	description="Few would mistake Damien Jones for a chartered accountant. His physique suggests the Undead, and his wardrobe suggests a failed lion-tamer.\012He wears an accountant-style white button-down shirt, but half of it is missing. His skin underneath is criss-crossed with what might almost be claw marks, and bizarre patterns have been burned into the skin around his back. He wears a stylish pince-nez, but the left lens has shattered. Bits of organic matter hang from his finger tips, but he doesn't seem to mind.\012\012He seems entirely determined to accomplish one goal and one goal only -- to ignore it all, and pray everything returns to nromal."
)

Room("Damien's Bedroom")(
	exits={'east': t("Damien's Office,leaving"), 'west': t("Damien's Study")},
	description='You feel as though you have stepped into a giant metal ping-pong ball. Everything is gun metal grey, the room is spherical and there are no hard edges in sight. It looks as though someone has hollowed out a metal ball bearing and made it his home. In the center of the room is a white cot with a few blankets on it. You see nothing else here.\012\012In what looks like another new addition, there is a round pathway made of the same organic threads leading off to the west.'
)

Room("Damien's Cubicle")(
	exits={'south': t("Damien's Office,leaving")},
	description='A few objects come to your attention when you first enter the cubicle: a snazzy black laptop, an executive toy, an analog clock, and a small framed photograph. Everything else here is difficult to make out -- instead of catching your eye most of the items in this room do the opposite. There is some sort of chair here, a notice or calendar on the cubical wall, and a pile of things on the floor. None of them look very important.\012\012The cubicle walls have also been filled in at the corners. There is no trace of plaster here, instead the corners are filled with the smooth, sticky substance.'
)

Room("Damien's Cubicle(1)")(
	exits={'south': t("Damien's Office,entering")},
	description='null'
)

Room("Damien's Office,entering")(
	display_name="Damien's Office",
	description="You see a typical office cubicle littered with common-place office junk. The office looks to be some sort of banking or accountancy house, but it is difficult to make out any details. Maybe it's the lighting, but everything except the one cubicle seems dull and almost out of focus. In fact, the only detail that you can easily make out aside from the cubicle is that all of the corners to this room have been filled in with plaster. Now none of the walls meets at a right angle. This plaster has recently been augmented by an organic, sticky substance. The strands completely round out the edges, and seem to be incredibly strong.\012\012You can go east, into a stack of books; or you can enter the cubicle to the north.",
	exits={'east': t('Musty Section'), 'north': t("Damien's Cubicle")}
)

Room("Damien's Office,leaving")(
	display_name="Damien's Office",
	description="You see a typical office cubicle littered with common-place office junk. The office looks to be some sort of banking or accountancy house, but it is difficult to make out any details. Maybe it's the lighting, but everything except the one cubicle seems dull and almost out of focus. In fact, the only detail that you can easily make out aside from the cubicle is that all of the corners to this room have been filled in with plaster. Now none of the walls meets at a right angle. This plaster has recently been augmented by an organic, sticky substance. The strands completely round out the edges, and seem to be incredibly strong.\012\012You can go east, into a stack of books; you can exit through a steel grey door to the west; or you can enter  the cubicle to the north.",
	exits={'east': t('Musty Section'), 'west': t("Damien's Bedroom"), 'north': t("Damien's Cubicle")}
)

Room("Damien's Study")(
	exits={'east': t("Damien's Bedroom")},
	description='     This is looks like a traditional (20th century, Earth-type) room in a large city apartment. The decoration is modern, and it is full of sturdy metal bookshelves.  The reference manuals are still fairly neat in rows on the shelf, but everything else has been removed.\012     There are several piles of half-read occult lore around the room, apparently someone was searching for something -- a bit frantically, too.\012     Organic stuff covers every surface, and every edge. Maybe someone was in a hurry to redecorate?\012     There is an exit to the east, and there was an exit to the north. This exit has been nailed shut, and completely sealed with about two feet of the bizarre thread.'
)

twisted.library.clothing.Cape('dark black cloak')(
	place=t('Guyute'),
	synonyms=['cloak', 'black cloak'],
	description='A rather nondescript dark black cloak.'
)

Thing('dark blue loose silk shirt')(
	place=t('Agatha'),
	synonyms=['silk shirt', 'shirt'],
	description='A white box.'
)

Thing('dark green carpet')(
	component=1,
	place=t('Mansion Upper Hall'),
	synonyms=['carpet', 'green carpet'],
	description='The carpet is a murky, dark green color, and woven with intersecting lines and curves of black thread. The lines are difficult to discern against their dark background, and almost seem to be moving, in an indistinct sort of way.'
)

twisted.library.clothing.Coat('dark green overcoat')(
	place=t('Tenth'),
	synonyms=['green overcoat', 'overcoat', 'coat'],
	clothing_appearance='a dark green overcoat',
	description='A long, dark green overcoat with gold stitching along the cuffs and around the buttonholes and pockets. '
)

twisted.library.clothing.Shirt('dark green shirt')(
	component=1,
	place=t('Blake'),
	synonyms=['shirt'],
	description='A hunter green button-down shirt.',
	clothing_worn='true'
)

twisted.library.clothing.Cape('dark grey cape')(
	place=t('Maxwell'),
	synonyms=['cape'],
	description='This is a dark grey cape.'
)

Room('Dark River Tunnel')(
	theme='water',
	exits={'east': t('Underground Grotto'), 'west': t('Western End of Grotto'), 'north': t('Dark River Tunnel(1)')},
	description='A Dark River Tunnel looking as if it needs to be described.',
	needsBoat='true'
)

Room('Dark River Tunnel(1)')(
	theme='water',
	exits={'south': t('Dark River Tunnel'), 'north': t('Dark River Tunnel(2)')},
	description='A Dark River Tunnel looking as if it needs to be described.',
	display_name='Dark River Tunnel',
	needsBoat='true'
)

Room('Dark River Tunnel(2)')(
	theme='water',
	exits={'south': t('Dark River Tunnel(1)')},
	description='A Dark River Tunnel looking as if it needs to be described.',
	display_name='Dark River Tunnel',
	needsBoat='true'
)

Room('Darkness')(
	inhibit_exits='true',
	theme='paper',
	inhibit_items='true',
	display_name='A Dark Place',
	OBSOLETE_super=t('Class_Dark Room'),
	exits={'east': t('Precarious Ledge'), 'west': t('Cold Floor')},
	description="It's too dark in here to see!"
)

twisted.library.clothing.Necklace('dazzling necklace')(
	place=t('Agatha'),
	synonyms=["agatha's necklace"],
	description='The necklace dazzles the eye, even white walls bear witness to its light.',
	display_name='necklace'
)

Room('Deeper In The Rock')(
	theme='greystone',
	OBSOLETE_super=t('Class_Dark Room'),
	exits={'south': t('A Small Dark Crevice'), 'north': t('Secret Cave')},
	description="It's too dark in here to see!",
	display_name='A Dark Place'
)

Room('Demo')(
	description='A funny box.'
)

Thing('demo book')(
	place=t('great bookshelf'),
	synonyms=['book'],
	description='A rather nondescript demo book.',
	OBSOLETE_super=t('Class_Linking Book'),
	linkTo=t('Twisted Reality Corporate Demo Center')
)

Container('demo cash register')(
	locked='true',
	component=1,
	place=t('Demo Center Gift Shop'),
	synonyms=['drawer', 'pad', 'small numeric keypad', 'keypad', 'register', 'numeric keypad'],
	closed_description='The lower portion of the register bears a vaguely rectangular seam which you guess must be the cash drawer.',
	description=observable.Hash({'__MAIN__': 'A smooth, sleek, ergonomic grey plastic lump, with a small green lcd display reading "Out of Service" at the top, and a small numeric keypad at the bottom.', 'open/close': 'The lower portion of the register bears a vaguely rectangular seam which you guess must be the cash drawer.'}),
	display_name='cash register',
	open_description='The cash drawer is open, unfolded from an origami-like section of the register that normally contains it.'
)

Thing('demo center bathroom door')(
	component=1,
	place=t('Demo Center East Wing'),
	synonyms=['blue door', 'swinging door', 'door'],
	description='A blue metal door, designed to be pushed open easily from either side. It is labeled "Players" just above the icon of a gender-neutral stick figure.',
	display_name='blue swinging door'
)

Thing('demo center bathroom graffiti')(
	component=1,
	place=t('Demo Center Bathroom Stall'),
	synonyms=['tiles', 'bathroom graffiti', 'occasional graffiti'],
	description='Someone has scrawled "zork4ever" on the tiles in an idelible black magic marker, probably due to the average guest\'s inherent desire to deface and destroy online demos through any means possible. Then again, it is possible that it was left here by someone who just liked zork a lot.',
	display_name='graffiti'
)

Thing('demo center bathroom mirror')(
	component=1,
	place=t('Demo Center Lavatory'),
	synonyms=['mirror'],
	description='demo.MirrorDesc',
	display_name='Lavatory mirror',
	base_description='A large, rectangular mirror built into the wall over the sink. Reflected in the mirror, you see:\012\012'
)

Thing('demo center bathroom notice')(
	component=1,
	place=t('Demo Center Bathroom Stall'),
	synonyms=['notice', 'note'],
	description='A large, white, laminated piece of paper, topped with the large heading "NOTICE:" followed by the text:\012\012     "This bathroom is equipped with a High Pressure Zero Gravity Toilet for your convenience and safety. Twisted Matrix Enterprises Inc. is in no way responsible for the misuse, intentional or otherwise, of the abovementioned High Pressure Zero Gravity Toilet, and is not responsible for any injuries, damages, psychological trauma, and/or destruction and/or loss of any parts, extremities, organs, possessions, or attributes inflicted during the operation of the toilet in question."',
	display_name='large notice'
)

Thing('demo center bathroom sink')(
	component=1,
	place=t('Demo Center Lavatory'),
	synonyms=['white sink', 'small white sink', 'knob', 'knob left', 'knob right', 'unlabeled knob'],
	display_name='sink',
	degree=0,
	description='A small white ceramic basin, topped with a single unlabled knob and a polished metal faucet.'
)

Room('Demo Center Bathroom Stall')(
	place=t('Demo'),
	description=observable.Hash({'__MAIN__': 'A small bathroom stall, lined with light grey tiles, immaculately clean except for the occasional graffiti. A large, gleamingly white and unnecessarily futuristic looking toilet is set into the center of the floor, next to a toilet paper dispenser that has been attached to the wall.', 'demo center bathroom stall door closeDesc': 'The stall door is closed, and there is a large notice posted on the wall just to the right of it.'}),
	exits={'west': t('Demo Center Lavatory')}
)

Thing('demo center bathroom stall door')(
	thereOpenDesc='The stall door stands open, leading out into the bathroom.',
	openDesc='To the east, the door to the single bathroom stall stands open.',
	obstructed='true',
	component=1,
	place=t('Demo Center Lavatory'),
	synonyms=['door', 'stall', 'stall door'],
	closeDesc='To the east, a single bathroom stall is separated from the rest of the room by a black metal door and a similar set of dividers.',
	display_name='bathroom stall door',
	OBSOLETE_super=t('Class_Door'),
	description='It appears to be a demo center bathroom stall door, but it is vague, indistinct, and little more than a blurry smear on reality.',
	thereCloseDesc='The stall door is closed, and there is a large notice posted on the wall just to the right of it.'
)

Thing('demo center bell')(
	reciever=t('brass paperweight'),
	place=t('demo center obelisk'),
	synonyms=['brass button', 'button', 'bell', 'brass bell'],
	repop=t('demo center obelisk'),
	description='A small brass bell on a wooden stand, with a prominent brass button emerging from the top. Engraved in the stand is the phrase "Ring For Service".',
	display_name='small brass bell'
)

Container('demo center coffee table')(
	component=1,
	maximum_occupancy=2,
	place=t('Demo Center Waiting Room'),
	synonyms=['table'],
	preposition='on',
	player_preposition='sitting on',
	display_name='coffee table',
	description='A dark, polished wooden table, made of what appears to be solid oak.  A thin line of gold inlay traces a complicated, yet elegant, pattern around the edge of the table.  It is set between the high backed chairs.'
)

Thing('demo center computer')(
	component=1,
	place=t('Messy New Jersey Office'),
	description='A large grey box labeled "VA Research", attached to a similarly colored keyboard. The monitor attached appears to have been originally intended for a Macintosh workstation, and is currently showing a very trippy screensaver of some kind.',
	display_name='computer'
)

Thing('demo center computer equipment')(
	component=1,
	place=t('Messy New Jersey Office'),
	synonyms=['equipment', 'computer equipment'],
	description='Various and sundry items, including a set of headphones, a cheap plastic General Electric telephone, several Linux Manuals, an extra Universal Mac Monitor Plug Adapter, several outdated RedHat Linux install CDs, and a lot of other fairly uninteresting and useless items.'
)

Thing('demo center counter')(
	component=1,
	place=t('Demo Center Gift Shop'),
	synonyms=['counter', 'behind counter'],
	description='A curved, grey wooden barrier, about waist high. A cash register is built into the end near the doorway, and there is also a small sign standing on the middle of it.',
	display_name='check out counter'
)

Container('demo center drinking fountain')(
	spouting_water='false',
	component=1,
	place=t('Demo Center West Wing'),
	synonyms=['push button', 'square button', 'button', 'fount', 'fountain'],
	display_name='drinking fountain',
	description='A cylindrical drinking fountain, with a brightly polished steel spigot, and a rectangular "PUSH" button set into one side.'
)

Room('Demo Center East Wing')(
	place=t('Demo'),
	theme='default',
	exits={'east': t('Demo Center Lavatory'), 'west': t('Demo Information Center'), 'north': t('Messy New Jersey Office')},
	description=observable.Hash({'__MAIN__': 'An immaculately white hallway, with a tall, arched ceiling and a polished black marble floor. A framed painting has been hung on the south wall, and to the east, the hallway ends in a blue swinging door labeled "Players" just above the icon of a gender-neutral stick figure.', 'development door openDesc': 'A small, battered wooden door stands open to the north.'})
)

Room('Demo Center Gift Shop')(
	place=t('Demo'),
	description='A small but brightly colored room, aside from the rather drab white walls and polished black marble floor. It is filled with shelves and racks where merchandise would go, but they stand almost empty, except for a few things no one would want. There is a check out counter along the south end of the room, with a built in cash register. A small white sign stands on the counter by the register. To the south, a doorway leads out into a larger room.',
	exits={'south': t('Demo Center West Wing Lobby')}
)

Container('demo center gift shop racks')(
	component=1,
	place=t('Demo Center Gift Shop'),
	synonyms=['racks'],
	description='There are several large standing racks here, built from black metal wire and designed to rotate freely when spun.',
	display_name='rack'
)

twisted.library.clothing.Shirt('demo center guest t-shirt')(
	place=t('demo center gift shop racks'),
	synonyms=['shirt', 't-shirt', 't', 'tshirt', 'guest t-shirt', 'demo center', 'demo'],
	clothing_appearance='a "guest" t-shirt',
	repop=t('demo center gift shop racks'),
	description='A cheap white cotton shirt with short sleeves. It is emblazoned with the word "Guest" in large, friendly letters.'
)

Container('demo center high backed chair')(
	component=1,
	maximum_occupancy=2,
	place=t('Demo Center Waiting Room'),
	synonyms=['high backed chair', 'chair'],
	preposition='on',
	player_preposition='sitting on',
	display_name='high-backed chair',
	description='A blue box.'
)

Thing('demo center jar-jar')(
	component=1,
	place=t('Demo Center Gift Shop'),
	synonyms=['jar-jar binks pez dispenser', 'jar-jar binks', 'pez dispenser', 'dispenser', 'jar-jar', 'jar'],
	description='For christ\'s sake, it\'s a Jar-jar binks "Official" pez dispenser... Why are you even trying to looking at it?',
	display_name='Jar-jar Binks pez dispenser'
)

Thing('demo center keyboard')(
	password='zork4ever',
	entry='',
	component=1,
	place=t('Messy New Jersey Office'),
	display_name='keyboard',
	description='A KB101 Plus keyboard. It contains a wide variety of keys, including the ever popular "Enter". Like all KeyTronic keyboards, it looks as though it was designed in the \'50s and made to withstand a direct nuclear attack.',
	monitor=t('demo center monitor')
)

Room('Demo Center Lavatory')(
	place=t('Demo'),
	theme='default',
	exits={'east': t('Demo Center Bathroom Stall'), 'west': t('Demo Center East Wing')},
	description=observable.Hash({'__MAIN__': 'A square, more modestly sized room lined entirely in light grey tiles. A black plastic wastebasket stands against the south wall, opposite a small white sink and the much larger mirror hanging above it. A blue swinging door leads out of the bathroom to the west.', 'demo center bathroom stall door closeDesc': 'To the east, a single bathroom stall is separated from the rest of the room by a black metal door and a similar set of dividers.'})
)

Thing('demo center monitor')(
	component=1,
	place=t('Messy New Jersey Office'),
	synonyms=['screen', 'trippy screensaver', 'screensaver'],
	description=observable.Hash({'__MAIN__': 'A large Macintosh monitor with a Winny The Pooh sticker attached to the case just above the power button. Someone has covered Winny\'s head with a semitransparent "Powered By RedHat" sticker, giving him a dark, brooding, and disproportionately large white head.', 'screen': 'In the background, a screensaver is tracing out some trippy mathematical figures, and an "Enter Password:" window is open in the center of the screen, displaying an empty password field.'}),
	display_name='monitor'
)

Container('demo center obelisk')(
	component=1,
	maximum_occupancy=3,
	place=t('Demo Information Center'),
	synonyms=['brightly colored map', 'map', 'obelisk'],
	preposition='on',
	player_preposition='sitting on',
	display_name='Obsidian Obelisk',
	description='The obelisk is a polished, glossy black, and set with a large, colorful map and various pieces of Twisted Reality propoganda. At the top is a familiar looking black line-art "Twisted Reality 1.2.1" logo, and a large piece of text welcoming you to the demo center. Below that is a bright yellow polygon, very similar to the shape of the room you\'re currently standing in, labeled "YOU ARE HERE!". The hallway leading east from the main room connects to a large blue area labeled "Restrooms" to the east, and a much smaller, brown room to the north, labeled "development". The west hallway branches off into a Lobby, with a Gift Shop to it\'s north, and two "Staging Areas" further west.'
)

Thing('demo center office trash')(
	component=1,
	place=t('Messy New Jersey Office'),
	synonyms=['trash', 'bottles', 'bags', 'empty bottles', 'paper bags'],
	description="The desk is scattered with empty bottles of Dr. Pepper, discarded Arizona Iced Tea cans, and a few crumpled paper bags. You get the impression that whoever works here probably eats most of their meals at the desk and doesn't get around to cleaning up until much later in the day, if ever."
)

Thing('demo center painting of tenth')(
	reciever=t('Tenth'),
	component=1,
	place=t('Demo Center East Wing'),
	synonyms=['black button', 'small button', 'small black button', 'page button', 'button', 'painting of tenth', 'painting', 'picture', 'portrait'],
	display_name='Painting of Tenth',
	description='demo.PaintingDescription'
)

Container('demo center paper dispenser')(
	component=1,
	place=t('Demo Center Bathroom Stall'),
	synonyms=['paper dispenser lever', 'toilet paper dispenser lever', 'dispenser lever', 'lever', 'paper dispenser', 'dispenser'],
	target_room=t('Science and Technology Demo Center'),
	display_name='toilet paper dispenser',
	description='A small, glossy black box, with a polished chrome sliding lever attached to the side.'
)

Thing('demo center scattered paper')(
	component=1,
	place=t('science and technology demo center table'),
	synonyms=['set of papers', 'papers', 'scattered paper', 'pieces', 'pieces of paper', 'paper'],
	description='A pile of scattered papers, including some assembly diagrams, unused warranty cards, and other refuse associated with equipment-heavy labs, but nothing of any particular interest.',
	display_name='scattered set of papers'
)

Container('demo center swivel chair')(
	component=1,
	maximum_occupancy=1,
	place=t('Messy New Jersey Office'),
	synonyms=['chair', 'swivel chair'],
	preposition='on',
	player_preposition='sitting on',
	display_name='black swivel chair',
	description='An adjustable black plastic chair with a padded seat and backrest, ending in five jointed wheels.'
)

Thing('demo center things no one would want')(
	component=1,
	place=t('Demo Center Gift Shop'),
	synonyms=['things', 'things no one wants', 'stuff'],
	description="There are a few really worthless things no one would want on the shelves... But really, you don't want them. Would you really want a jar-jar binks pez dispenser? Honestly, now.",
	display_name='things no one would want'
)

Container('demo center toilet')(
	component=1,
	maximum_occupancy=2,
	place=t('Demo Center Bathroom Stall'),
	preposition='in',
	player_preposition='sitting on',
	description='A sleek, elegant form of lines and curves, gleaming white and perfectly symmetrical... A geometrical work of art, but also a toilet. There is no visible handle, leaving it perfectly unmarred, except for a small white placard on top of the back rest.',
	display_name='toilet',
	fountain=t('demo center drinking fountain')
)

Thing('demo center toilet placard')(
	component=1,
	place=t('Demo Center Bathroom Stall'),
	synonyms=['toilet placard', 'placard', 'card'],
	description='A tiny white cardboard square, propped up for easy reference and covered in flowing black script which reads:\012\012    "Motion Sensitive Zero Gravity Toilet"\012\011   "Copywright 1798 GUE"\012"Frobozz Magic Zero Gravity Toilet Company"\012\012    "The staff of the Frobozz Magic Zero Gravity Toilet company thanks you for your purchase. The Model Zero HPZGT is truly superior to the standard Magic Toilet line, and, as the name implies, is designed for ease of use and can operate in many conditions that would render a normal toilet useless... We pride ourselves on catering to the distinguishing toilet owner, and we hope to enjoy your patronage in the future."',
	display_name='small white placard'
)

Container('demo center vehicle frame')(
	component=1,
	maximum_occupancy=1,
	place=t('Science and Technology Vehicle Area(2)'),
	synonyms=['framework', 'frame'],
	preposition='on',
	player_preposition='sitting on',
	display_name='metal framework',
	description='It appears to be a demo center vehicle frame, but it is vague, indistinct, and little more than a blurry smear on reality.'
)

Room('Demo Center Waiting Room')(
	place=t('Demo'),
	theme='wood',
	exits={'northeast': t('Demo Center West Wing')},
	description='This is a comfortable waiting room with high-backed leather chairs and wooden-paneled walls. There is a solid oak coffee table here, with a tasteful gold inlay.  To the northeast, there is a gold-lined archway leading into a room with white walls and a black floor.'
)

Container('demo center wastebasket')(
	component=1,
	place=t('Demo Center Lavatory'),
	synonyms=['wastebasket', 'basket', 'plastic wastebasket'],
	description='A black plastic wastebasket, with a small swinging door labeled "TRASH".',
	display_name='black plastic wastebasket'
)

Room('Demo Center West Wing')(
	place=t('Demo'),
	description='This is the west wing of the demo center. The walls are a polished, gleaming, white substance, and the floor is perfectly smooth black marble. This particular room is triangular, with an arched doorway set into each of the three walls. A sign reading "Back To Main Demo Center" is hung over the eastern arch, while the southwest and northwest arches are unlabeled. A small drinking fountain stands alone in the center of the floor.',
	exits={'southwest': t('Demo Center Waiting Room'), 'northwest': t('Greenhouse Entrance'), 'east': t('Demo Center West Wing Lobby')}
)

Room('Demo Center West Wing Lobby')(
	place=t('Demo'),
	description=observable.Hash({'__MAIN__': 'A circular room, with bright, white walls and a polished black marble floor. The lobby joins a pair of hallways to the east and west, and has a rectangular doorway cut into the north wall, labeled "Gift Shop". Several grey plastic chairs are built into the floor around the edges of the room, but they don\'t look particularly comfortable.', 'sliding glass doors closeDesc': 'A pair of sliding glass doors stand shut in the southern wall.'}),
	exits={'south': t('Science and Technology Demo Center'), 'north': t('Demo Center Gift Shop'), 'east': t('Demo Information Center'), 'west': t('Demo Center West Wing')}
)

Container('demo gift shop shelves')(
	component=1,
	place=t('Demo Center Gift Shop'),
	synonyms=['shelves'],
	preposition='on',
	display_name='shelf',
	description='The shelves are geometrically perfect arrangements of wooden boards, forming large, rectangular... shelves. Collectively, there is enough space to hold quite a few gifts, but they are strangely bare, except for the few things no one would want.'
)

Thing('demo gift shop sign')(
	component=1,
	place=t('Demo Center Gift Shop'),
	synonyms=['white sign', 'small sign', 'sign'],
	description='A small white cardboard sign, with black letters. It reads:\012\012\011"TME Gift Shop Customers:"\012\012"Due to the increasing number of increasingly rude and inconsiderate guest users running off with our merchandise and using it to jam the plumbing, we have been forced to shut down the Gift Shop. We may re-open in the future, but only if some degree of civility on the parts of the visitors can be established."\012\012Thank you,\012\012The Management"',
	display_name='small white sign'
)

Container('demo guymelef')(
	open_descriptor='The chest plates have separated and slid open to reveal a small compartment inside, where there a few controls and an uncomfortably cramped looking chair.',
	foo='(null)',
	closed_descriptor='A large green gem is set into either shoulder, and a single reddish stone is embedded in the left side of its chest.',
	is_guymelef='true',
	place=t('Mansion Laboratory'),
	synonyms=['giant armor', 'giant suit', 'suit', 'suit of armor', 'armor', 'white guymelef', 'guymelef'],
	display_name='giant suit of armor',
	description=observable.Hash({'__MAIN__': "A massive suit of white armor, easily five times the height of a man. It is formed from smooth, oddly shaped sections of silvery white metal, and bears a dark red cloak from it's broad shoulderpads.", 'open/close descriptor': 'The chest plates have separated and slid open to reveal a small compartment inside, where there a few controls and an uncomfortably cramped looking chair.'})
)

Room('Demo Information Center')(
	place=t('Demo'),
	theme='default',
	exits={'east': t('Demo Center East Wing'), 'south': t('Twisted Reality Corporate Demo Center'), 'west': t('Demo Center West Wing Lobby')},
	description='A large, circular room, with immaculately white walls and a polished, black marble floor. A large black obsidian obelisk stands in the center of the room, emblazoned with a brightly colored map. The room becomes more of a hallway as it continues off to the south.'
)

Room('Dent in Tube')(
	exits={'south': t('Closed Junction'), 'northwest': t('Metal Tube')},
	description='This is a continuation of the gleaming metal tube. There is a huge dent in the ceiling here, which nearly forces you to crawl as you pass it.  The dent looks as though a huge, jagged rock were slammed into the side of the tube by a giant, yet it did not break through.  The tube continues to the south, and bends around to the northwest.'
)

Thing('development door')(
	thereOpenDesc='A battered wooden doorway in the south wall leads out into the hall.',
	openDesc='A small, battered wooden door stands open to the north.',
	obstructed='false',
	component=1,
	place=t('Demo Center East Wing'),
	synonyms=['door'],
	closeDesc='A piece of graph paper scrawled with the word "Development" is taped to a smaller, battered wooden door set into the north wall.',
	display_name='wooden door',
	OBSOLETE_super=t('Class_Door'),
	description='A worn, splintered wooden door with a dented copper handle. A piece of graph paper has been taped to it, scrawled with the word "development".',
	thereCloseDesc='A battered wooden door is set into the south wall.'
)

Thing('dexterity dial')(
	component=1,
	place=t('Genetic Laboratory'),
	synonyms=['dexterity', 'dial'],
	value='0.05',
	OBSOLETE_super=t('Class_Player Creation Dial'),
	description='It appears to be a dexterity dial, but it is vague, indistinct, and little more than a blurry smear on reality.'
)

Thing('diagrams')(
	component=1,
	place=t('Mansion Maintenance Closet'),
	synonyms=['technical diagrams', 'diagram'],
	description='Large sheets of white paper, covered with dense and intricate patterns of black lines. While some of the diagrams are difficult to identify, several of them appear to be drawings of a large, cubic system of clockwork. There is also a drawing of what looks like a massive suit of armor, filled with gears, pulleys, and tubing, but its exact design and purpose is somewhat unclear.'
)

Room("Divu'en School Entranceway")(
	theme='crack',
	exits={'southwest': t('Wrecked Street, wall')},
	description='The hallway of an old school-building.  The ceiling is caved in, and none of the rest of the building is accessible, but you can get out to the southwest where you can see a street.',
	display_name='School Entranceway'
)

Room('Divunal Room')(
	theme='greystone',
	description='This room is a series of gateways to different places in the Age of Divunal.  Now, there is only one which has been uncovered.  To the north, there is a gateway with a crude drawing of a sideways oval with five lines drawn upwards from various points on it.  Through this gateway, you can see a small room that is littered with rubble.',
	exits={'north': t('Cramped Transporter Booth')}
)

twisted.library.clothing.Shirt('Divunal t-shirt')(
	place=t('demo center gift shop racks'),
	synonyms=['t-shirt', 'shirt', 'divunal shirt', 't shirt', 't', 'divunal'],
	clothing_appearance='a Divunal t-shirt',
	repop=t('demo center gift shop racks'),
	description='A white t-shirt, almost exactly the right size for a generic guest person. It is emblazoned with the image of a yellowed piece of parchment, upon which the word "Divunal" has been written in flowing script. Below the image, in much smaller letters, is the phrase "Less graphics, more game" and a small blue Twisted Reality logo.'
)

Thing('door')(
	place=t("Jedin's Foyer"),
	description='A rather nondescript door.'
)

Thing('door in oak tree')(
	thereOpenDesc='To the south, here is a door leading to a green-looking garden.',
	openDesc='There seems to be a door leading north into the tree.',
	obstructed='false',
	component=1,
	place=t('Ivy Garden'),
	synonyms=['door'],
	OBSOLETE_super=t('Class_Door'),
	description='Yes, if you look closely it seems there IS a door in the tree. It has been very well concealed, and the edges match almost perfectly.',
	thereCloseDesc='The secret door to the south seems to be closed.'
)

Room('Doorway Room')(
	exits={'south': t('Small Arched Tunnel'), 'north': t('very small round room')},
	description='This room seems entirely dedicated to a door in the north wall. The entire north wall is decorated with rays extending from the ceiling, floor, and two other walls to the door at the center.  There are no other decorations here. To the south there is a much smaller door.'
)

Thing('dried white rose')(
	place=t('Other New Jersey Apartment Bedroom'),
	synonyms=['rose', 'white rose', 'dried rose'],
	description='The blossom, stem, and first leaf of a white rose, carefully dried out and preserved.'
)


Thing('easel')(
	place=t('Art Room'),
	description='A lone, half-finished picture lies on the easel.  It looks like it could easily be finished, but the artist left it intentionally not so.  It is a picture of a book.'
)

Room('East Wing Spiral Staircase Bottom')(
	display_name='Spiral Staircase',
	description='This is the bottom of a walled white marble spiral staircase.  There is a small open archway here to the northwest, with the word "Lobby" engraved above it.',
	exits={'northwest': t('Castle Greysen Fountain Room'), 'up': t('East Wing Spiral Staircase Top')}
)

Room('East Wing Spiral Staircase Top')(
	display_name='Spiral Staircase',
	description='This is the top of a walled white marble spiral staircase.  There is a small open archway here to the northwest, with the word "Offices" engraved above it.',
	exits={'northwest': t('Observation Hallway'), 'down': t('East Wing Spiral Staircase Bottom')}
)

Thing('eastern tapestry')(
	component=1,
	place=t("Guyute's Bedroom"),
	synonyms=['tapestry', 'east'],
	description='The images here form a stark contrast to the ones in the rest of the room. Instead of a scene full of battle and violent imagery, there is a picture of a library. Though it seems run-down and slightly decrepit, it seems to emit a feeling of hope and good fortune.'
)

Thing('egyptology manual')(
	read_text="The manual's innumerable pages are covered in illustrations and notes regarding the strange symbolic language of the egyptians. While some of the illustrations are interesting, this book makes for fairly dry and uninteresting reading, although it would probably be very useful in an attempt to translate hieroglyphics.",
	place=t('Maxwell'),
	synonyms=['egyptology', 'manual', 'book'],
	translates='egyptian hieroglyphics',
	OBSOLETE_super=t('class_translator book'),
	description='A large and extremely thick leather bound book, entitled "A Practical Guide to Egyptian Hieroglyphs, by Lord Rutherford P. Beaucavage, Esquire". While one of the more massive and unwieldy books you\'ve ever had tthe misfortune to encounter, it appears to be nothing if not comprehensive.'
)

Chair('elegant straight-backed chair')(
	maximum_occupancy=1,
	place=t('Smoking Room'),
	synonyms=['straight chair', 'straight-backed chair', 'elegant chair'],
	preposition='in',
	player_preposition='sitting in',
	description='A rather nondescript Chippendale chair.'
)

Thing('elvish sword of great antiquity')(
	frotzed='true',
	place=t('Maxwell'),
	synonyms=['sword', 'elvish sword'],
	isLit='true',
	description=observable.Hash({'__MAIN__': 'This sword is elvish.  You can tell by the runes carved into the blade and hilt.  It is made of a perfectly mirrored metal, which, although you can guess that it is old by the quality craftsmanship and baroque style to the curves of the hilt, is completely undamaged by age.', 'lighting': ['A pure white glow eminates from ', m('elvish sword of great antiquity','noun_phrase'), ', bathing ', m('elvish sword of great antiquity','him_her'), ' in light.']})
)

Thing('Emerald Cube')(
	component=1,
	place=t('Emerald Room'),
	synonyms=['cube'],
	OBSOLETE_super=t('Class_Cube'),
	description='A white box.'
)

Room('Emerald Room')(
	exits={'west': t('Jewel Bedecked Hallway')},
	description="This room is a study in green.  While you can make out no light source, light must be filtering in through the emerald ceiling to get down here, where it reflects off of the myriad facets of the room's walls and floor.  There are no markings anywhere, and the only real feature of the room is a cube, which appears to be part of the floor, made of the same emerald substance that composes the rest of the room, but glittering more brightly."
)

Room('Empty Bakery')(
	theme='crack',
	description='A small and burnt-out bakery.  It looks as though there has been a fire here.  Shattered glass windows to the northwest look out upon a destroyed street, and a door leads out onto it.  There is a small wooden door to the northwest.',
	exits={'northeast': t('Wrecked Street, wall'), 'northwest': t('Wrecked Alleyway')}
)

Room('Empty Hallway')(
	exits={'southeast': t('Bookstore Stairwell, Level 11'), 'north': t('Empty Hallway North')},
	description='This is an empty north/south hallway.  There are no doors here save one in the southeastern corner, only wooden floor and white-painted walls.  The southeastern door is labeled "11".'
)

Room('Empty Hallway North')(
	display_name='Empty Hallway',
	description='This is an empty north/south hallway.  There are no doors here, only wooden floor and white-painted walls.  The northern wall appears to have been slightly singed by a circular fire.  The hallway continues some distance to the south.',
	exits={'south': t('Empty Hallway')}
)

Thing('Encyclopedia Divunalia')(
	enc_define_tenth='Tenth: a Human brought from Earth to fill the role of the Architect or Artificer Archetype.  He has a penchant for a Victorian style of design and dress.  He is rather nondescript for the purposes of this example, although he should not be.',
	enc_define_foo='Foo: an interesting metasyntactic variable whose origins have been lost in the mists of time.  This foo is rather nondescript for the purposes of this example.  See also: the Great Plague of Foos (GPF) in 2 BF.',
	enc_define_anah='Anah: The Human brought from Earth to fulfill the Dreamer archetype.  This archetype is dissatified in the real world, and finds comfort and satisfaction in a world of dreams.',
	enc_define_huntyre='Huntyre: A manifestation of the Dark Angel.',
	enc_define_maxwells_castle="Maxwell's Castle: A palace in the clouds, created as a home for the Teller of the Tale.  It is somewhere in the heart of the library.",
	place=t('Pedestal'),
	synonyms=['book', 'encyclopedia'],
	enc_define_jedin='Jedin: A Human archaeologist sent from Earth to fulfill the "Historian" archetype.  His type is most interested in the past.',
	enc_define_kalev='Kalev: A Human sent from Earth to fulfill the "Mystery" archetype.  This archetype takes herself very seriously, she has an alluring and mysterious personality which inspires curiosity (and perhaps desire).',
	enc_define_maxwell='Maxwell: the first of the human archetypes to arrive in Divunal.  He is an ex-writer.',
	description='A beautiful book, elegantly bound in what appears to be platinum, with the engraved title "Encyclopedia Divunalia" on the front cover.  You are sure that it contains lots of useful information about the world that you are currently residing in, and that much of that information is reserved only for gods.  A pen is attached for defining your own words, and there is a bookmark at each letter for doing lookups.  You could also index the volume by looking in the back.',
	enc_define_skystone='Skystone: A "magical" mineral that was previously in a ring orbiting Divunal, which allows Humans (and to some extent, those with Divuthan heritage) to change the rules that bind Reality.  While it can theoretically take on any form, it is usually fullbright blue, and translucent.'
)

Room('End of Catwalk')(
	exits={'east': t('Metal Tube'), 'south': t('Catwalk')},
	description="This is a wire mesh catwalk overlooking a huge factory assembly from high above.  From this height, it would be impossible to discern what it is that was produced below.  There is a hole punched in the catwalk to the north, and it looks unsafe to tread further on.  There is a door to your east leading away from the factory floor.  The door is labeled with some strange letters that you don't understand."
)

Room('End of Rainbow')(
	exits={'southwest': t('Canyon Bottom')},
	description='You are on a small, rocky beach on the continuation of the Frigid River past the Falls. The beach is narrow due to the presence of the White Cliffs. The river canyon opens here and sunlight shines in from above. A rainbow crosses over the falls to the east and a narrow path continues to the southwest.'
)

Thing('endurance dial')(
	component=1,
	place=t('Genetic Laboratory'),
	synonyms=['endurance', 'dial'],
	value='0.0',
	OBSOLETE_super=t('Class_Player Creation Dial'),
	description='A white box.'
)

Thing('ethereal staff')(
	isLit='false',
	place=t('Guyute'),
	synonyms=['staff'],
	teleport_phrase_learn_me=t('Class Room'),
	teleport_phrase_take_me_home=t("Guyute's Laboratory"),
	teleport_message='The ethereal staff begins to glow an unearthly color.',
	description='This staff is quite ornate, and stands at over six feet tall. The shaft is made from carved kemlar wood, straight out of the Great Forest.  At the top there is a large orb made of fine crystal. ',
	teleport_phrase_my_its_musty_in_here=t('Musty Section')
)

Room('Even More Office Hallway')(
	exits={'northeast': t('Catwalk'), 'southeast': t('Supply Closet'), 'down': t('Continued Chasm')},
	description='This hall is undamaged except for a huge chasm which seems to be carved straight out of the floor to the west.  Other than that, it is a clean, white hallway which ends to your east.  There is a spiral staircase leading upwards, as well as an open archway to a metal catwalk to the northeast and a door to a large closet to the southeast.'
)

Thing('executive toy')(
	component=1,
	place=t("Damien's Cubicle"),
	synonyms=['toy'],
	description="This is a physical demonstration of Conservation of Momentum and classic Newtonian physics. There is a small base of a shiny black marble, from which stand four silver poles. These, in turn, support a brass crossbar.\012\012Hanging from the crossbar are five shiny chrome bearings, suspended by wire. If you were to lift one and let it fall, it would smack into it's neighbor and come to an abrupt stop. The neighboring ball, however, would shudder as it passed the momentum on to the next in line, until the opposite ball would swing out.\012\012Currently the executive toy is motionless, but there are enough fingerprint smears on the shiny chrome to imply tat it gets frequent use."
)

Thing('eye of a newt')(
	place=t('glass jar'),
	synonyms=['eye'],
	description='An rather nondescript eye of newt.'
)

twisted.library.clothing.Coat('faded brown coat')(
	component=1,
	place=t('Aaron'),
	synonyms=['coat', 'brown coat', 'jacket', 'brown jacket', 'faded jacket', 'faded brown jacket', 'faded coat'],
	clothing_appearance='faded brown coat',
	description='A careworn old coat, faded from the sun.'
)

Container('faded coat pocket')(
	component=1,
	place=t('faded brown coat'),
	synonyms=['pocket'],
	description='A blue box.',
	display_name='coat pocket'
)


Thing('fifth knob')(
	component=1,
	place=t('qin'),
	synonyms=['knob5', 'knob'],
	description='Fifth knob from the top of the qin with which to tune the instrument.'
)

Thing('first knob')(
	component=1,
	place=t('qin'),
	synonyms=['knob1', 'knob'],
	description='The first knob from the top of the qin.'
)

Room('Flat Ledge')(
	exits={'east': t('Twisty Cloud Path'), 'west': t('Ledge in front of Castle in the Clouds')},
	description='This is a ledge into the cliff surrounding a tall castle in the clouds.  You can see clouds everywhere below you.  To your west, you can walk around the rock to where there is an entrance to the palace, or you can follow a rock path which is seemingly suspended in the clouds to your east.'
)

Thing('floozle')(
	place=t('Jedin'),
	description='This appears to be a sort of musical instrument.  It has 14 different horns on it, each of which is vibrating slightly.  It is cycling slowly through the colors of the rainbow.  Touching it is slightly painful.'
)

Container('Food Box')(
	place=t('Class Room'),
	synonyms=['box'],
	OBSOLETE_super=t('Class_Container'),
	description='A blue box.'
)

Room('Forest')(
	exits={'east': t('Forest Path'), 'north': t('Clearing')},
	description='This is a forest, with trees in all directions.  To the east, there appears to be sunlight.'
)

Room('Forest 2')(
	display_name='Forest',
	description='This is a dimly lit forest, with large trees all around.',
	exits={'south': t('Clearing'), 'north': t('Clearing 2'), 'east': t('Forest 3'), 'west': t('Forest Path')}
)

Room('Forest 3')(
	display_name='Forest',
	description='The forest thins out, revealing impassable mountains.',
	exits={'south': t('Forest 2'), 'west': t('Forest 2'), 'north': t('Forest 2')}
)

Room('Forest Path')(
	exits={'south': t('North of House'), 'north': t('Clearing'), 'east': t('Forest 2'), 'west': t('Forest')},
	description='This is a path winding through a dimly lit forest. The path heads north-south here. One particularly large tree with some low branches stands at the edge of the path.'
)

Thing('foundation')(
	component=1,
	place=t('Wrecked Street, curve'),
	description='The foundation of the building looks as if it has barely survived the test of time.'
)

Thing('fourth knob')(
	component=1,
	place=t('qin'),
	synonyms=['knob4', 'knob'],
	description='Fourth knob from the top of the qin with which to tune the instrument.'
)

Thing('frobozz magic reality altering appliance')(
	place=t('Guyute'),
	synonyms=['appliance'],
	OBSOLETE_super=t('Reality Pencil'),
	description='This generic reality altering appliance bears a striking resemblance to a pencil.  It bears the Frobozz Magic Reality Company logo.'
)

Room('Front Step of Darkness')(
	theme='paper',
	description='You stand upon the front stoop of a mansion perched upon an infinite void.  There is no ground except where you are standing, no light except that coming from the door behind you.  You can only go back into the house to the south.',
	exits={'south': t('Hallway')}
)

Room('Garden Maze')(
	theme='leaf',
	description='You are in a medium-sized clearing. To the north, there is a tall hedge with a single opening in it. A sign has been placed in the ground near the hedge, next to which is a large red button.',
	exits={'east': t('Outer Tea Garden'), 'north': t('Garden Maze(1)')}
)

Room('Garden Maze(1)')(
	theme='leaf',
	exits={'east': t('Garden Maze(2)'), 'south': t('Garden Maze'), 'north': t('Garden Maze(3)')},
	description="The hedges in here are very high--seven or eight feet tall. There's little to look at, so two items easily stick out. There is a hammer on the ground to the north, and to the east there is a pair of scissors.",
	display_name='Garden Maze'
)

Room('Garden Maze(10)')(
	theme='leaf',
	exits={'south': t('Garden Maze(8)'), 'north': t('Garden Maze(12)'), 'east': t('Garden Maze(11)'), 'west': t('Garden Maze(9)')},
	description='This part of the maze narrows so much, you can barely squeeze through, but it does feature a large trellis at the northern end. The eastern and western exits are ensconced by large stone arches.',
	display_name='Garden Maze'
)

Room('Garden Maze(11)')(
	theme='leaf',
	exits={'south': t('Garden Maze'), 'north': t('Garden Maze(6)'), 'east': t('Garden Maze(9)'), 'west': t('Garden Maze')},
	description='This part of the maze feels *very* strange, almost as if its a dead end...but there are exits all around!',
	display_name='Garden Maze'
)

Room('Garden Maze(12)')(
	theme='leaf',
	exits={'east': t('Garden Maze(13)'), 'south': t('Garden Maze(10)'), 'west': t('Garden Maze(9)')},
	description="This part of the maze looks as if it's been set up especially for the weary traveller to take a break. There's a nice table near the eastern exit and four chairs suspiciously positioned to the west.",
	display_name='Garden Maze'
)

Room('Garden Maze(13)')(
	theme='leaf',
	exits={'east': t('Garden Maze(14)'), 'south': t('Garden Maze(11)'), 'west': t('Garden Maze(12)')},
	description='A wind blows through this area, and small rivulets swirl about on the ground near the eastern exit. To the south, a large gate is open, and apparently uncloseable, judging by the rusty hinge that squeaks in the wind.',
	display_name='Garden Maze'
)

Room('Garden Maze(14)')(
	theme='leaf',
	exits={'west': t('Garden Maze(13)'), 'north': t('Mystic Field')},
	description='This portion of the maze seems nicer and more well kept than the rest. You can barely make out a tune gently playing, although the source is unknown.',
	display_name='Garden Maze'
)

Room('Garden Maze(2)')(
	theme='leaf',
	exits={'west': t('Garden Maze(1)'), 'north': t('Garden Maze(4)')},
	description="You might need some help, or you could have the knack, but as long as you're here, you're on the right track. The ground is covered by a thick fog, but there's just grass on the ground anyways.",
	display_name='Garden Maze'
)

Room('Garden Maze(3)')(
	theme='leaf',
	exits={'east': t('Garden Maze'), 'south': t('Garden Maze'), 'north': t('Garden Maze(9)')},
	description="A unsettling feeling seems to be a resident of this area; you can't escape it. The hedge seems to be turning brown in patches around here.",
	display_name='Garden Maze'
)

Room('Garden Maze(4)')(
	theme='leaf',
	exits={'south': t('Garden Maze(2)'), 'west': t('Garden Maze(3)'), 'north': t('Garden Maze(5)')},
	description='The hedges must be of a different kind here; now there seems to be flowers blooming in places on the walls. To the west there is a wooden chair, while to the north, leaning against the hedge is a paddle from a rowboat of some sort.',
	display_name='Garden Maze'
)

Room('Garden Maze(5)')(
	theme='leaf',
	exits={'south': t('Garden Maze(4)'), 'west': t('Garden Maze(7)'), 'north': t('Garden Maze(6)')},
	description='The maze continues in several directions here. A large pine tree stands to the west, while to the north is an apple tree.',
	display_name='Garden Maze'
)

Room('Garden Maze(6)')(
	theme='leaf',
	OBSOLETE_super=t('Class_Dark Room'),
	exits={'south': t('Garden Maze')},
	description="It's too dark in here to see!",
	display_name='A Dark Place'
)

Room('Garden Maze(7)')(
	theme='leaf',
	exits={'east': t('Garden Maze(5)'), 'west': t('Garden Maze(8)'), 'north': t('Garden Maze(11)')},
	description='There is a sense of peace and tranquility that fills the air here. There is a great pile of leaves on the ground to the north, which is quite strange, given the fact that there are no trees in the area. To the west there is a rake leaning against the hedge.',
	display_name='Garden Maze'
)

Room('Garden Maze(8)')(
	theme='leaf',
	exits={'east': t('Garden Maze(7)'), 'west': t('Garden Maze(9)'), 'north': t('Garden Maze(10)')},
	description="Sometimes it's easy to lose faith in yourself, especially when on a long journey. Just remember,\012\012YOU HAVE ALWAYS BEEN HERE.\012\012Take a leap of faith.",
	display_name='Garden Maze'
)

Room('Garden Maze(9)')(
	theme='leaf',
	exits={'east': t('Garden Maze'), 'south': t('Garden Maze')},
	description='The last person to come here must not have been feeling too well...judging by the skeleton in the corner.',
	display_name='Garden Maze'
)

Thing('gate(1)')(
	component=1,
	place=t('Castle Entrance Archway'),
	description='A cast-iron heavy gate which bears the inscription, "Abandon all hope, ye who enter here."'
)

Thing('GenderMatic')(
	place=t('science and technology demo center table'),
	synonyms=['matic', 'gender', 'button', 'changer', 'red button'],
	repop=t('science and technology demo center table'),
	description='A small, grey, rectangular piece of plastic, with 32 pin connectors on either end and a large red button on the top.',
	gender='f'
)

Thing('GenderMatic instruction booklet')(
	read_text='    "Thank you for your purchase of our Type 232 Ronco Pocket GenderMatic. To to the somewhat touchy nature of human sexuality, this device is not precisely calibrated; However, the simple control system makes working out your desired settings a simple game of chance. In other words, if at first you don\'t succeed, try, try again."\012\012     "(Ronco Pocket Body Alterations, Inc. can be held in no way liable for any effects, desired or otherwise, produced by this non-UL-Listed device, or any concequences thereof.)"',
	place=t('science and technology demo center table'),
	synonyms=['instructions', 'gendermatic instructions', 'gendermatic instruction', 'gendermatic booklet', 'instruction booklet', 'booklet'],
	repop=t('science and technology demo center table'),
	description='A folded paper booklet, entitled "Improving your life with the Ronco Pocket GenderMatic". It seems to be little more than a few pages of instructions and legal notices, but would probably be very useful if you wanted to read about the functions of the Type 232 Gender Changer.'
)

Container('General Box')(
	place=t('Demo'),
	OBSOLETE_super=t('Class_Container'),
	description='A blue box.'
)

Room('Genetic Laboratory')(
	theme='default',
	description='A perfectly square room with immaculately white walls and floors. The northern end of the room is filled with a large, complex machine, consisting of a bank of controls connected to a large transparent tube large enough for a person to stand comfortably inside, labeled "Sterilized For Your Protection".',
	exits={'south': t('Class Room')}
)

Container('glass jar')(
	place=t('Cold Room'),
	synonyms=['jar'],
	OBSOLETE_super=t('Class_Container'),
	description='An ordinary class jar.'
)

Container('glasses case')(
	place=t('Rikyu'),
	synonyms=['case'],
	OBSOLETE_super=t('Class_Container'),
	description='A rather nondescript glasses case.'
)

Thing('glock semi-automatic pistol')(
	place=t('Agent Moore'),
	synonyms=['glock', 'gun'],
	OBSOLETE_super=t('Reality Pencil'),
	description='A white box.'
)

Room('God Authoring Room')(
	exits={'down': t('Science Fiction Room')},
	description='This room holds dangerous equipment. DO NOT MODIFY ANYTHING HERE UNLESS YOU KNOW EXACTLY WHAT YOU ARE DOING, IS THAT CLEAR!??!'
)

Thing('Gold Cube')(
	component=1,
	place=t('Gold Room'),
	synonyms=['cube'],
	OBSOLETE_super=t('Class_Cube'),
	description='A white box.'
)

Room('Gold Room')(
	exits={'east': t('Jewel Bedecked Hallway 2')},
	description="This room is a study in gold.  While you can make out no light source, light must be filtering in through the golden, translucent ceiling to get down here, where it shines off of the curved surfaces of the room's walls and floor.  There are no markings anywhere, and the only real feature of the room is a cube, which appears to be part of the floor, made of the same golden substance that composes the rest of the room, but glittering more brightly."
)

Container('gondola')(
	place=t('Western End of Grotto'),
	synonyms=['boat'],
	OBSOLETE_super=t('Class_Boat'),
	description='This gondola has a canopy cover like that of a horse drawn carriage. It is painted ebony black with deep rich mahogany wood decks, inlaid roses and glove leather seats.'
)

Thing('gondola pager')(
	place=t('teakwood podium'),
	synonyms=['pager', 'bell'],
	description='This bell is crafted out of some silver material. It looks perfectly balanced, and one can imagine how sweet it sounds.',
	display_name='small bell'
)

Thing('gondola pager(1)')(
	place=t('Western End of Grotto'),
	synonyms=['bell', 'pager'],
	description='This bell is crafted out of some silver material. It looks perfectly balanced, and one can imagine how sweet it sounds.',
	display_name='small bell'
)

Room('Grand History Book Room')(
	exits={'east': t("Jedin's Foyer"), 'south': t('Aisle 1.')},
	description=observable.Hash({'__MAIN__': 'This room is a hemisphere carved from solid marble. The only feature of the room is a giant book which is chained and bolted into a huge pedestal at the dead center of the room, and the plaque at the floor in front of the pedestal which reads, "#1, History Of Divunal" in immense letters.  A small sign bearing the legend "Prehistory" stands over a wooden archway to the north.', 'stainless steel door closeDesc': 'A large archway with a steel door stands to the south.', 'solid oak door openDesc': 'To the east, you see a well-lit, polished wood foyer.'})
)

Room('Granite Reception Room')(
	exits={'south': t('Grey Cube Room'), 'northwest': t('Bookstore Stairwell, Level 5')},
	description='This is a dark grey granite room with a section of the floor raised to form a semicircular reception desk.  No one is seated behind it.  On the southern wall, there is a door leading further into the office.  The west wall is entirely filled with bookshelves, and the east wall is solid, unbroken granite.  You can exit to a stairwell to the northwest.'
)

Container('great bookshelf')(
	component=1,
	place=t("Guyute's Laboratory"),
	synonyms=['bookshelf'],
	OBSOLETE_super=t('Class_Container'),
	description='This bookshelf is filled with all sorts of mysterious-looking books. Each shelf seems to have its own category, indicated by a dirty brass plaque. "Spells and Hexes", "Astrology", "Myths and Legends" and "Ancient Mystical Ceremony" are all packed with aging tomes. The section marked "General Magic" catches your eye.'
)

Room('Great Dome')(
	theme='greystone',
	description='Upon entering this room, you might mistake it for the out-of doors - except for the marble flooring and the walls. Those walls and that floor are cracked in many places, and were it not for the sturdy marble pillars holding the walls up, it would seem a very unstable structure indeed.  Far, far above where you stand you can see a dome, partially obscured by the clouds beneath it.  The dome is a crystal blue color, and though one would assume the sky must lie beyond it, it is impossible to see.  Two exits, northeast and southwest, are completely blocked by rubble, and there are doors to the west, east, and northeast.',
	exits={'northeast': t('Armory'), 'east': t('Less Crumbling Hallway'), 'west': t('West End'), 'north': t('Crumbling Library')}
)

Thing('great oak tree')(
	component=1,
	place=t('Ivy Garden'),
	synonyms=['tree branch', 'oak tree', 'tree'],
	description="This great tree is several armspans around. Given it's immense size, it must have been here for at least a century. "
)

Room('Great Underground Lake')(
	theme='greystone',
	description='The shallow end of a great underground lake that extends into dark and deeper waters to the north. A small cave, partially filled with water, leads south.',
	exits={'south': t('Mansion Basement Well')}
)

Container('green leather book')(
	place=t('demo center coffee table'),
	synonyms=['book', 'green book', 'leather book'],
	repop=t('demo center coffee table'),
	description=observable.Hash({'__MAIN__': 'A green, leather bound book, entitled "Simulacra And Simulation" in gold embossed letters.', 'opened': 'It is open, revealing that the center of each page has been removed, making it useless as a book but quite functional as a container.'})
)

twisted.library.clothing.Shirt('green silk shirt')(
	place=t('Tsiale'),
	synonyms=['green shirt', 'shirt', 'silk shirt'],
	description='A loose fitting, collarless green silk shirt, with its sleeves rolled up to the elbow. '
)

Room('Greenhouse Entrance')(
	place=t('Demo'),
	theme='leaf',
	exits={'southeast': t('Demo Center West Wing')},
	description='An engraved marble plaque in the center of the floor proclaims this to be the "Twisted Matrix Enterprises Twisted Reality Demonstration Center Greenhouse". A small forest of plants are strewn haphazardly about the room, as if they were put there to meet a deadline. They all look remarkably similiar.'
)

Thing('grenade')(
	place=t('Agent Moore'),
	description="It is a pretty typical looking grenade.  If you don't know what that is, well too bad!"
)

twisted.library.clothing.Shirt('grey cotton shirt')(
	place=t('Maxwell'),
	synonyms=['shirt', 'grey shirt'],
	description='A very plain, neatly pressed, grey cotton shirt.'
)

Room('Grey Cube Room')(
	theme='default',
	description='This is a grey cubical room, about sixteen feet on each side, which appears to have been out of use for a very long time.  A thin layer of dust on the floor is scuffled from the center of the room to the northern door, but other than that untouched.',
	exits={'north': t('Granite Reception Room')}
)

Container('grey plastic chairs')(
	component=1,
	maximum_occupancy=6,
	place=t('Demo Center West Wing Lobby'),
	synonyms=['plastic chairs', 'plastic chair', 'chairs', 'chair'],
	preposition='on',
	player_preposition='sitting on',
	display_name='grey plastic chair',
	description='A blue box.'
)

twisted.library.clothing.Blindfold('greyish cloth')(
	place=t('Yumeika'),
	synonyms=['cloth'],
	clothing_appearance='a greyish cloth bound tightly across her eyes',
	description='A greyish cloth of thick, finely-woven linen.'
)


Room('Guest Chamber')(
	exits={'east': t('Observation Hallway')},
	description='A small, comfortable guest room.'
)

twisted.author.Author('Guyute')(
	dexterity='0.0',
	memory='1.0',
	aura='0.1',
	health='1.0',
	stamina='0.0',
	health_time=934396549868L,
	mindspeak='0.1',
	endurance='0.0',
	oldlocation=t('Garden Maze'),
	learned_frotz=1,
	strength='-0.2',
	stamina_time=934396549868L,
	spells_learned=1,
	gender='m',
	learned_posess=-1,
	psyche='1.0',
	learned_zorft=-1,
	OBSOLETE_super=t('Class_Human'),
	description=observable.Hash({'__MAIN__': "A tall and thin man, most of Guyute's appearance is shrouded. ", 'clothing': [m('Guyute','him_her'), ' is wearing ', m('dark black cloak','noun_phrase'), '.']}),
	agility='0.0'
)

Room("Guyute's Bedroom")(
	theme='wood',
	exits={'northwest': t('Smoking Room'), 'north': t('Secret Chamber')},
	description=observable.Hash({'__MAIN__': 'The walls here are covered with ancient tapestries depicting battle scenes. In the southwest corner is a king-sized bed, next to which is a small nightstand. Near the east wall is a wood-burning stove, whose chimmney rises into the ceiling.', 'northern tapestry closeDesc': ''}),
	display_name='Master Bedroom'
)

Room("Guyute's Laboratory")(
	theme='greystone',
	description='A large stone-walled room. It looks as if someone has been hard at work here. Over on the north wall is a stone workbench, while on the south wall is a large bookshelf. In the southeast corner, surprisingly, is a sofa. The most prominent item in the room, however, is a great black cauldron;  each burp and bubble releases a fine mist, which fills the room. A set of rickety metal stairs leads up. To the west is a stone doorway.',
	exits={'up': t('Smoking Room'), 'west': t('Cold Room')}
)

Room("Guyute's Laboratory(1)")(
	theme='greystone',
	description="It's too dark in here to see!",
	display_name='A Dark Place'
)

Room('Hallway')(
	theme='paper',
	description='This is a rather short wood paneled hallway. The floor is covered buy a thin persian rug, and the walls are covered by thick hangings. To the north is a heavy wooden door, and to the east is a comfortable looking study.',
	exits={'east': t('Proper English Library'), 'north': t('Front Step of Darkness')}
)

Thing('hazardous materials crate')(
	place=t('Science and Technology Vehicle Area(1)'),
	synonyms=['hazardous materials', 'materials crate', 'materials', 'crate'],
	repop=t('Science and Technology Vehicle Area(1)'),
	weight='2.0',
	description='A large, yellow box built from high impact plastic. It is fitted with oversized handles on each side, and stenciled with a number of warning symbols. A label painted onto one side reads: \012\012    WARNING: WILD WILD WEST FANFIC ARCHIVE  (EXPOSURE MAY RESULT IN SEVERE BRAIN DAMAGE)'
)

Room('Help Desk')(
	theme='paper',
	description='This is a customer service and help desk in a bookstore. There are a few racks which look like they could accomodate paperbacks here which are currently empty. There is also a rickety metal spiral staircase which ascends to the entrance hallway. A passageway to the southwest affords you access to the greater body of this level, where most books are stored.',
	exits={'southwest': t('Main Aisle, East End'), 'up': t('Small Bookstore Entrance')}
)

Thing('huge cylindrical pressure tank')(
	component=1,
	place=t('Mansion Basement Engine Room'),
	synonyms=['cylindrical pressure tank', 'pressure tank', 'tank'],
	description='A huge, cylindrical tank, built out of metal and set with strengthening bands and braces. A small brass plaque is attached to the front side, embossed with the phrase "WARNING: Contents may be under high pressure" in flowing script.'
)

Container('humidor')(
	place=t('ornate wooden table'),
	OBSOLETE_super=t('Class_Closeable Container'),
	description="A humidor made out of expensive-looking teak wood. There's a glass window in the top through which many fine cigars can be seen."
)

Thing('Important Note')(
	place=t('Darkness'),
	synonyms=['maxwell note', 'note'],
	description='I wanted to write a section that was entirely dark, pitch black like tar. It could be a magical darkness, if necessary, to extinguish torches and the like. To do so, however, I\'d need to disable certain verbs, such as "look at" because there isn\'t anything to see. Can I write my own verb "look" for these rooms?\012\012I suppose I should also disable turn page, or can we just suspend disbelief on that score?\012\012//Damien'
)

Container('inflatable mattress')(
	component=1,
	maximum_occupancy=2,
	place=t('Mansion Laboratory'),
	synonyms=['mattress', 'bed'],
	preposition='on',
	player_preposition='lying on',
	description='A blue box.'
)

Room('Inner Garden')(
	theme='leaf',
	exits={'south': t('Outer Tea Garden')},
	description='The paths leading northeast and south here are laid with small, flat stones. Over to the east is a stone lantern, in front of which is a stone basin, filled with water. To the north is a tea house, surrounded by small trees and bushes. All around this area is a tall bamboo fence.',
	display_name='Uchi-rojj'
)

Room('Inside Oak Tree')(
	theme='leaf',
	description=observable.Hash({'__MAIN__': "Though the tree is big, it's still a little cramped in here. However, there's a ladder leading down into the darkness.", 'door in oak tree openDesc': 'To the south, here is a door leading to a green-looking garden.'}),
	exits={'south': t('Ivy Garden'), 'down': t('Underground Grotto')}
)

Thing('instruction manual')(
	book_text='\012"Hello, Guest! And welcome to the Twisted Reality Demo Center. Here, you can experience some of the many interesting features that make TR the Ergonomic Power Tool of interactive text development that it is."\012\012"Twisted Reality, like Infocom\'s classic text based games, allows for a wide range of interaction with the environment. Feel free to experiment; Entering commands like "close door", "pull lever", or "turn dial to liquefy" can produce many interesting effects."\012\012"The Demo Center, while small, has a lot of objects in it. When you look at room descriptions and visible objects, try looking at some of the other things their descriptions mention; A fairly complex Zork-like puzzle is here if you can find it."',
	place=t('Maxwell'),
	synonyms=['manual'],
	repop=t('grey plastic chairs'),
	description='A small folded booklet of white paper, with a blue spherical logo and the title "Twisted Reality Demo Center Instruction Manual".'
)

Thing('Irlae Rod')(
	place=t('Tsiale'),
	synonyms=['rod'],
	OBSOLETE_super=t('Reality Pencil'),
	description="A rod of delicate craftsmenship about one's arm length. It combines a jade-colored stone which glitters as if lit from within, and a ruby crystal which makes it warm to the touch.  These two materials are set in opposing spirals to one and other. One end of the rod is pointed, and there is a translucent pearlescent bulb adorning the other."
)

Thing('iron door')(
	obstructed='false',
	component=1,
	place=t('Cold Room'),
	OBSOLETE_super=t('Class_Door'),
	description='An rather nondescript iron door.'
)

Thing('ishi-doro')(
	frotzed='true',
	place=t('Inner Garden'),
	synonyms=['lantern'],
	isLit='true',
	display_name='stone lantern',
	description=observable.Hash({'__MAIN__': 'A very nice lantern. ', 'lighting': ['A pure white glow eminates from ', m('ishi-doro','noun_phrase'), ', bathing ', m('ishi-doro','him_her'), ' in light.']})
)

Room('Ivy Garden')(
	theme='leaf',
	description=observable.Hash({'__MAIN__': "This garden provides an extremely peaceful place to sit and meditate. A great oak tree is present in the northern part of this garden. To the southwest is a aisle of stone benches, at whose southwesternmost point is a large cement urn. The ground here is covered with ivy; only the walkways to and from the urn are clear enough to pass. It's also possible to climb the tree.", 'door in oak tree openDesc': 'There seems to be a door leading north into the tree.'}),
	exits={'up': t('Woodem Platform in Oak Tree'), 'west': t('Outer Tea Garden'), 'north': t('Inside Oak Tree')}
)

twisted.author.Author('James')(
	oldlocation=t('Jewel Bedecked Hallway 2'),
	dexterity='0.0',
	agility='0.0',
	memory='0.0',
	psyche='-0.05',
	endurance='0.0',
	gender='m',
	OBSOLETE_super=t('Class_Human'),
	description=observable.Hash({'__MAIN__': 'A lean, solemn looking young man with bright yellow eyes, flowing bright red hair, and a pale complexion. ', 'clothing': [m('James','him_her'), ' is wearing ', m('shirt with an owl insignia','noun_phrase'), ', ', m('pair of dark blue shorts','noun_phrase'), ', ', 'and ', m('pair of sandles','noun_phrase'), '.']}),
	strength='0.65'
)

twisted.author.Author('Jedin')(
	oldlocation=t('The Doorway of the Obsidian Tower'),
	description=observable.Hash({'__MAIN__': "This man, about two meters in height, complements his gymnastic musculature with the poise of a high-ranking aristocrat--or a military leader.  His thick, straight hair parts easily to his left; it appears slightly mussed, as if he runs his hands through it often.  The obsidian-toned locks frame a face of planes and angles, striking in its resemblance to that of an almost-finished statue--even the ears are slightly pointier than a normal man's, the lips fuller.  Jedin's emerald-green eyes sparkle beneath his black eyebrows, their intensity matched by a startling degree of softness and understanding, traits that flow through the rest of his demeanor and belie his body's youth.", 'clothing': [m('Jedin','him_her'), ' is wearing ', 'a white, button-down shirt and collar of a soft, durable fabric with the sleeves rolled up to just below his elbows', ', ', 'a well-worn brown leather belt', ', ', 'a pair of rugged, dust-brown chinos', ', ', 'and ', 'a pair of all-purpose brown leather boots', '.']}),
	OBSOLETE_super=t('Class_Human'),
	gender='m'
)

Room("Jedin's Foyer")(
	exits={'west': t('Grand History Book Room'), 'north': t('coat closet')},
	description=observable.Hash({'__MAIN__': "A Jedin's Foyer looking as if it needs to be described.", 'solid oak door openDesc': 'To the east, you see a large, marble room with a pedestal in its center, to which is chained a large book.'})
)

Room('Jewel Bedecked Hallway')(
	theme='default',
	description='This is a hallway lined with hundreds of different colors of jewels.  Upon closer inspection, the walls are inlaid with them, so they appear both smooth and jeweled at once.  An emerald arch leads west, a marble one south, a ruby one east and an onyx one north.',
	exits={'south': t('Observation Hallway'), 'north': t('Jewel Bedecked Hallway 2'), 'east': t('Emerald Room'), 'west': t('Ruby Room')}
)

Room('Jewel Bedecked Hallway 2')(
	theme='default',
	exits={'south': t('Jewel Bedecked Hallway'), 'north': t('Black Hallway'), 'east': t('Silver Room'), 'west': t('Gold Room')},
	description='This is a hallway lined with hundreds of different colors of jewels.  Upon closer inspection, the walls are inlaid with them, so they appear both smooth and jeweled at once.  A gold arch leads west, a silver one east, and onyx ones north and south.',
	display_name='Jewel Bedecked Hallway'
)

Thing('jeweled sword')(
	place=t('Rikyu'),
	synonyms=['sword'],
	description='A rather nondescript jeweled sword.'
)

Thing('John Romero action figure')(
	place=t('demo gift shop shelves'),
	synonyms=['action figure', 'figure', 'john', 'romero', 'ring', 'string'],
	repop=t('demo gift shop shelves'),
	description='The semi-posable plastic figure of a chunky little man with long black hair tied back in a ponytail. He is wearing a tiny Ion Storm t-shirt, and there is a length of string protruding from his back, ending in a small plastic ring.',
	romero='true'
)

Thing('journal')(
	place=t("Damien's Cubicle"),
	description='A typical diary, in a typical journal book. It is a well made book, with a leather exterior and very nice paper inside. The only thing that speerates it from a normal day planner are the large, we-mean-business combination locks along the edge.'
)

Thing('Kakemono')(
	component=1,
	book_text='The scroll is covered with strange characters. However, you find yourself magically able to understand them...',
	place=t('Tea House'),
	synonyms=['scroll'],
	spell_1='Posess',
	description='The scroll is covered with strange characters.'
)

twisted.library.clothing.Pants('khaki pants')(
	place=t('Jedin'),
	synonyms=['pants'],
	clothing_appearance='a pair of rugged, dust-brown chinos',
	description='Though a crease runs down the front and back of each leg of these pleated chinos, the strong, supple fabric makes it plain that this piece of clothing functions equally well for both work and leisure.  The pants have two pockets on both the front and back and are the color of dark brown dust.'
)

Container('king-sized bed')(
	place=t("Guyute's Bedroom"),
	synonyms=['bed'],
	description='This bed looks very soft, and its velvet comforter make it look all the more luxorious.'
)

Room('Kitchen(1)')(
	exits={'east': t('Behind House'), 'west': t('Living Room')},
	description='You are in the kitchen of the white house. A table seems to have been used recently for the preparation of food. A passage leads to the west and a dark staircase can be seen leading upward. A dark chimney leads down and to the east is a small window which is open.'
)

Chair('koshikake-machiai')(
	component=1,
	maximum_occupancy=5,
	place=t('Inner Garden'),
	synonyms=['bench'],
	display_name='small bench',
	description='This bench, called koshikake-machiai, is where guests await the invitation of the tea ceremony host.'
)

Thing('laptop')(
	place=t('Maxwell'),
	description='They say that you can tell how powerful a laptop is by how big it isn\'t. A large, heavy machine isn\'t likely to be very fast, or very exspensive. If that is a good standard, then this must be a fast mahcine indeed because if you were to turn it sideways it would almost disappear. Currently there is a screensaver running. It repeats the words:\012\012   "Damien Jones,  CPA -- Tax Law and Import Export Residuals"'
)

Container('Large Black Box')(
	component=1,
	place=t('Science and Technology Demo Center(1)'),
	synonyms=['black metal box', 'black', 'box'],
	closed_description='It is currently closed.',
	description=observable.Hash({'__MAIN__': 'A large, black metal box with a hinged top.', 'open/close': 'It is currently closed.'}),
	open_description='It is currently open.',
	display_name='black box'
)

Container('large black cauldron')(
	component=1,
	place=t("Guyute's Laboratory"),
	synonyms=['cauldron'],
	OBSOLETE_super=t('Class_Container'),
	description='This cauldron is filled with a strange phosphorescent liquid. Some other objects can be seen floating in the goo.'
)

Thing('large blue crayon')(
	place=t('Chenai'),
	synonyms=['blue crayon', 'crayon'],
	OBSOLETE_super=t('Reality Pencil'),
	description='It appears to be a blue crayon, but it is vague, indistinct, and little more than a blurry smear on reality.'
)

Thing('large gear')(
	place=t('Mansion Maintenance Closet'),
	synonyms=['gear'],
	description='A thin metal disc about the size of a dinner plate, edged with evenly spaced protrusions.'
)

Container('Large Glass Box')(
	transparent='true',
	component=1,
	place=t('Science and Technology Demo Center(1)'),
	synonyms=['transparent glass box', 'glass', 'box'],
	closed_description='It is currently closed.',
	description=observable.Hash({'__MAIN__': 'A large, transparent glass box with a hinged top.', 'open/close': 'It is currently open.'}),
	open_description='It is currently open.',
	display_name='glass box'
)

Container('large glass jar')(
	place=t('plastic swivel chair'),
	synonyms=['glass jar', 'jar'],
	description='A large glass jar with a rubber seal clamped onto the top.'
)

Thing('large predaceous diving beetle')(
	place=t('large glass jar'),
	synonyms=['diving beetle', 'large diving beetle', 'large beetle', 'beetle'],
	description="A large, glossy black beetle with powerful gripping forelegs, sharp, glistening, piercing mouthparts, and a homicidal gleam in it's compound eyes. Its numerous legs seem to be designed for swimming rapidly through water, but its large wings suggest that it is capable of wreaking havoc on land and in the air as well."
)

Thing('leather book')(
	place=t("Damien's Study"),
	synonyms=['leather', 'book'],
	description='An ancient, ancient tome. The ink (old faded, and red) is cracked, and the huge brass locks (??) have almost fallen off the edges. The binding is odd, it looks like leather, but feels slightly different.\012\012It is not possible to read; the handwriting is so old that it almost looks liks alien gibberish.'
)

Room('Ledge in front of Castle in the Clouds')(
	exits={'east': t('Flat Ledge'), 'up': t('Castle Steps'), 'west': t('Rocky Ledge, further west')},
	description='This is a rocky ledge.  Above, you can see a very large, imposing building, which looks like a smooth stone castle.  To your east and west lie further outcroppings of this ledge.  Beneath you, to the north, you see nothing but occasional clouds and a near-infinite drop.'
)

Room('Less Crumbling Hallway')(
	theme='greystone',
	description='This hallway is in slightly better condition than those that preceeded it.  The archaic mode of lighting here has reverted to candles near to the high ceiling.  The hallway continues to the east and to the west there is a door leading outside.',
	exits={'east': t('Crumbling Hallway'), 'west': t('Great Dome')}
)

Thing('lever')(
	component=1,
	place=t('Steam-Powered Library'),
	theme='wood',
	target_door=t('bookshelf door'),
	steam_source=t('Mansion Steam Engine'),
	description='A polished brass rod with a wooden handle, protruding from a similarly crafted socket set into the wall.'
)

Thing('light')(
	component=1,
	place=t("Damien's Office,entering"),
	description='A long, harsh flourescent tube. It emits a loud buzzing and an unforgiving glare.'
)

Thing('little black book')(
	place=t('Guyute'),
	synonyms=['spellbook'],
	spell_2='posess',
	spell_1='zorft',
	spell_0='frotz',
	OBSOLETE_super=t('Class_Spell Book'),
	description='A small black book, covered in a sort of fake-leather. A loop on the side looks like it might hold a pen of some sort.'
)

Room('Living Room')(
	exits={'east': t('Kitchen(1)')},
	description='You are in the living room. There is a doorway to the east, a wooden door with strange gothic lettering to the west, which appears to be nailed shut, a trophy case, and a large oriental rug in the center of the room.'
)

Room('Lonely Expanse of Beach')(
	exits={'east': t("Agatha's Lighthouse"), 'west': t('Sea Shore'), 'north': t('The Doorway of the Obsidian Tower')},
	description='A stream of icy water cuts a narrow, brackish ribbon in the sand. The water tumbles over rough, black rocks and mingles with the rolling sea.   A mixture of weather-ravaged conifers and deciduous trees border the sand.\012To the east, a lighthouse and an aged copper roof are visible above the trees tops.\012'
)

Thing('long glass tube')(
	component=1,
	place=t('Genetic Laboratory'),
	synonyms=['tube'],
	description=observable.Hash({'__MAIN__': 'A large, vertical glass tube, capable of holding a standing humanoid person comfortably within it. ', 'my person': 'There appears to be a person floating in some fluid inside the tube.'})
)

Thing('loose-leaf document')(
	place=t("Damien's Study"),
	synonyms=['loose', 'loose-leaf', 'loose leaf', 'document'],
	description='A loose collection of pages printed out on a dot matrix printer with a fading ink cartridge. The pages are held together by a series of clips, and appear to deal with tax law, especially unilateral trade assertions in multi-national businesses.'
)

Thing('lower ladder')(
	component=1,
	place=t('Small Platform on the Rock'),
	synonyms=['ladder'],
	description='This is the lower half of a wooden ladder which leads upwards to a higher, more narrow ledge.'
)

Thing('mailbox')(
	component=1,
	place=t('Front Step of Darkness'),
	description='The mailbox is painted white to match the house. It is closed.'
)

Room('Main Aisle, Center')(
	theme='paper',
	description='This is the main aisle of the floor of a bookstore. There are three aisles branching from it, spaced at regular intervals along the floor - the aisles are almost separate rooms because the bookshelves touch the ceilings and the floors and there is a wide separation between one aisle and the next because the shelves are so deep.  You are standing at the front of the second sub-aisle, at the middle of the main one. A plaque on the floor here reads "52.6-100, Important Financial Books". You can continue northward to into the Financial aisle, or east to another section.',
	exits={'east': t('Main Aisle, East End'), 'west': t('Main Aisle, West End'), 'north': t('Aisle 2.')}
)

Room('Main Aisle, East End')(
	theme='paper',
	description='This is the main aisle of the floor of a bookstore. There are three aisles branching from it, spaced at regular intervals along the floor - the aisles are almost separate rooms because the bookshelves touch the ceilings and the floors and there is a wide separation between one aisle and the next because the shelves are so deep.  You are standing at the front of the first sub-aisle, at the east end of the main one. A plaque on the floor here reads "1-52.5, The History Of Everything Really Worth Knowing About". You can continue northward to into the History aisle, or east to another section.',
	exits={'northeast': t('Help Desk'), 'west': t('Main Aisle, Center'), 'north': t('Aisle 1.')}
)

Room('Main Aisle, West End')(
	theme='paper',
	description='This is the main aisle of the floor of a bookstore. There are three aisles branching from it, spaced at regular intervals along the floor - the aisles are almost separate rooms because the bookshelves touch the ceilings and the floors and there is a wide separation between one aisle and the next because the shelves are so deep.  You are standing at the front of the third sub-aisle, at the western end of the main one. A plaque on the floor here reads "101-707, Miscelleneous Reading, Fiction, and Other Books". You can continue northward to into the Miscelleneous Reading aisle, or east to another section.',
	exits={'east': t('Main Aisle, Center'), 'north': t('Aisle 3.')}
)

Thing('mainspring')(
	place=t('Mansion Maintenance Closet'),
	description='A thick metal disc, composed of a long strip of metal wrapped into a tight spiral shape. The spiral begins with a small metal ring in the center, and ends in a small fastening bracket on its outside edge.'
)

Room('Mansion Attic')(
	exits={'down': t('Mansion Upper Hall')},
	description='null'
)

Room('Mansion Balcony')(
	theme='wood',
	description=observable.Hash({'__MAIN__': 'This is a balcony overlooking a war-torn industrial city.  Blimps are flying overhead, and you can see occasional explosions and flashes of light from the city streets.  French doors lead back into a large victorian mansion to the south.', 'balcony double doors openDesc': ''}),
	exits={'south': t("Tenth's Chamber")}
)

Room('Mansion Basement')(
	theme='greystone',
	description='A dimly lit chamber with greyish stone walls. In the center of the room, a massive wrought iron spiral staircase descends from the ceiling, leading upwards to a much brighter area. Crude doorways cut into the east and west walls lead into darkness. ',
	exits={'east': t('Mansion Basement Engine Room'), 'up': t('Mansion Stairwell'), 'west': t('Mansion Basement Storeroom')}
)

Room('Mansion Basement Engine Room')(
	theme='greystone',
	description='A dark, humid place, pervaded by a strange musty smell. The floor is little more than well packed earth, and the dark greyish brick of the walls is damp with condensation. A bare glass bulb provides a dim, flickering light to the room, hanging by its cord from the uncovered wooden beams that form the ceiling. A large brass and iron steam engine stands against the northern wall, laden with controls and gauges, next to a huge cylindrical tank which leaves just enough space to squeeze past to the eastern end of the room.',
	exits={'east': t('Mansion Basement Pump Area'), 'west': t('Mansion Basement')}
)

Thing('Mansion Basement Pump')(
	obstructed='true',
	component=1,
	place=t('Mansion Basement Pump Area'),
	synonyms=['pump', 'basement pump'],
	description=observable.Hash({'__MAIN__': 'A large metal box, bolted to a set of stone blocks that suspend it over the well dug into the floor. A cylindrical object extends from the bottom of the pump into the water, and it is connected to the machinery on the west side of the room by a number of large tubes and hoses.', 'pump action': ' It is producing a rhythmic humming sound, and causing the water in the well below it to churn violently.'})
)

Room('Mansion Basement Pump Area')(
	theme='greystone',
	description=observable.Hash({'__MAIN__': 'A small area, mostly walled off from the western half of the room by a large brass and metal machine. A large circular well has been dug into the dirt floor, and a small pump is suspended over it on stone blocks.', 'pump sound': ' A rhythmic, almost mechanical humming sound echoes throughout the room.'}),
	exits={'west': t('Mansion Basement Engine Room'), 'down': t('Mansion Basement Well')}
)

Room('Mansion Basement Storeroom')(
	theme='greystone',
	description='A dark, roughly built brick room, with an uncovered dirt floor. A broken glass bulb hangs from the ceiling by its cord, and several empty crates are scattered on the floor. Several of the crates are stacked up against an old wooden door in the west wall, which has also been boarded over. To the east, a roughly rectangular hole in the wall leads into a smaller room.',
	exits={'east': t('Mansion Basement')}
)

Room('Mansion Basement Well')(
	theme='greystone',
	description='A dark, cramped, narrow tunnel carved out of greyish stone, knee deep in running water. The tunnel continues to the north, and a rough vertical shaft leads upwards to a brighter area, where a cylindrical object is hanging.',
	exits={'up': t('Mansion Basement Pump Area'), 'north': t('Great Underground Lake')}
)

Container('Mansion Bedroom Bureau')(
	component=1,
	place=t("Tenth's Chamber"),
	synonyms=['drawer', 'drawers', 'wooden bureau'],
	display_name='bureau',
	OBSOLETE_super=t('Class_Container'),
	description='A dark, polished wooden bureau, with six drawers. The top of the bureau is blends seamlessly into the frame of a large, ovular mirror. '
)

Thing('Mansion Bedroom Mirror')(
	component=1,
	place=t("Tenth's Chamber"),
	synonyms=['large mirror', 'mirror'],
	description='divunal.tenth.MirrorDesc',
	display_name='ovular mirror',
	base_description='A large, ovular mirror, set in a polished wooden frame. Reflected in the mirror is:\012     '
)

Container('Mansion Bedroom Writing Desk')(
	component=1,
	maximum_occupancy=1,
	place=t("Tenth's Chamber"),
	synonyms=['desk'],
	preposition='on',
	player_preposition='sitting at',
	display_name='writing desk',
	description='A dark, polished wooden desk, set with bookshelves and an inkwell.'
)

Room('Mansion Coat Room')(
	theme='wood',
	description='A spacious walk-in closet which seems somewhat bigger than it does when observed from the outside. There are a number of wrought iron coathooks set into the walls at shoulder level, and a series of boot racks along the edges of the floor.',
	exits={'east': t('Mansion Entrance Hall')}
)

Room('Mansion Doorstep')(
	theme='leaf',
	description='You are standing on the southern doorstep of a large, stately mansion which is remarkably in contrast to the vast expanse of pine trees that surround it.  It appears completely undamaged by the decay and destruction that are evident to the sides of the forest.',
	exits={'east': t('Pine Grove'), 'north': t('Mansion Foyer')}
)

Room('Mansion East Ballroom')(
	theme='wood',
	description='A massive ballroom, empty and silent. A single candle is flickering in the giant crystal chandelier hanging over the room, casting an uneven, wavering glow over the polished floor and pale, greyish walls. A huge pair of archways are set into the east and west walls, leading into smaller and more brightly lit areas.',
	exits={'east': t('Mansion Grand Stair Landing'), 'west': t('Mansion Main Hall')}
)

Room('Mansion Entrance Hall')(
	theme='wood',
	description='An open, rectangular room with a slightly arched ceiling and a tiled floor. A large grey wooden door with a polished brass knob is set into the north wall, flanked by a coat rack and a small metal bin.  There is a nondescript wooden door on the west wall that leads to the coat room, and an archway in the rear wall leads south into a much larger room.',
	exits={'south': t('Mansion Main Hall'), 'west': t('Mansion Coat Room')}
)

Container('Mansion Four Poster Bed')(
	component=1,
	maximum_occupancy=2,
	place=t("Tenth's Chamber"),
	synonyms=['large bed'],
	preposition='on',
	player_preposition='lying on',
	display_name='bed',
	description='A large four poster bed, with a polished wooden frame, dark green hanging curtains, and matching sheets and pillows.'
)

Room('Mansion Foyer')(
	exits={'south': t('Mansion Doorstep'), 'up': t('Spiral Landing'), 'west': t('Mansion Hallway')},
	description='This is the entrance hallway of a large and tastefully decorated, if somewhat eccentric, mansion.  A large, sweeping half-spiral staircase leads upstairs, and a hallway continues eastward.'
)

Room('Mansion Grand Stair Balcony')(
	theme='wood',
	description='A spacious platform, bordered by a wrought iron railing. On either side, a pair of staircases lead downwards, eventually reaching a landing where they combine and change direction before continuing their descent. An arched doorway is set in the west wall, leading into a long hallway.',
	exits={'west': t('Mansion Upper Hall'), 'down': t('Mansion Grand Stair Landing')}
)

Room('Mansion Grand Stair Landing')(
	theme='wood',
	description='The room leads up into a vast, broad staircase, set with a deep red carpet. The stairs lead up for some way, narrowing as they go, until they divide into two separate sets and change direction, continuing upwards. A massive archway in the west wall leads into a larger, darker room.',
	exits={'up': t('Mansion Grand Stair Balcony'), 'west': t('Mansion East Ballroom')}
)

Room('Mansion Guest Room')(
	theme='wood',
	description='A workroom.  Describe me?',
	exits={'north': t('Mansion Upper Hallway')}
)

Room('Mansion Hallway')(
	exits={'east': t('Mansion Foyer'), 'west': t('More Mansion Hallway'), 'north': t('Psychadelic Room')},
	description='You are standing in a narrow, well-lit hallway with doors on the northern side, and windows on the southern.  The hall continues on to the west, and finishes to the east at the entrance of the building.'
)

Room('Mansion Laboratory')(
	theme='wood',
	description='A large room, cluttered with tables, shelves, and large racks of machinery. A massive metal frame occupies the center of the room, attached to a number of smaller machines. The closest thing to furniture in the room is a blue mattress laying on the floor in one corner.',
	exits={'south': t('Mansion Upper Hall')}
)

Room('Mansion Main Hall')(
	theme='wood',
	description='A broad, massive hallway with an arched ceiling that rises some thirty feet above you. The walls are a muted and featureless white, contrasting sharply against the dark wooden floor. There is a modest pair of doorways at the north and south ends of the hall,  but they are dwarfed by the massive arches set into the east and west walls. The eastern archway leads into darkness, while the western one is nearly obscured by a mass of gears and rods in the room behind it. A black plastic cable runs along the floor, emerging from the western arch and leading to a computer terminal standing in the southwest corner of the hall. Across from the computer, there is a small wooden door in the southeast corner labeled "Maintenance".',
	exits={'south': t('Mansion Study'), 'north': t('Mansion Entrance Hall'), 'east': t('Mansion East Ballroom'), 'southeast': t('Mansion Maintenance Closet'), 'west': t('Mansion West Ballroom')}
)

Room('Mansion Maintenance Closet')(
	theme='wood',
	description='A small, cubical, unfinished wooden room, roughly ten feet on each side. The walls are postered with obscure technical diagrams, and there are a number of wooden crates scattered randomly across the floor. A simple wooden table is set against the wall opposite the door, covered with random stacks of blueprints.',
	exits={'northwest': t('Mansion Main Hall')}
)

Room('Mansion Staging Room')(
	theme='wood',
	description='A wide, open room, with a polished wooden floor and plain white plaster walls. In the center of the room, a large pyramidal arrangement of steps leads up to a circular platform. Three identical, brass-cased cylindrical machines stand against the east, south, and west walls, connected to the base of the stairs by thick black cables.',
	exits={'north': t('Mansion Upper Hall')}
)

Room('Mansion Stairwell')(
	theme='wood',
	description='A tall, cylindrical room with a polished marble floor.  A massive wrought iron spiral staircase runs through the center of the room, leading both up and down for quite some distance. Simple arched doorways are set into the east and west walls, leading out of the room.',
	exits={'up': t('Upper Mansion Stairwell'), 'east': t('Mansion Upper Hall'), 'west': t('Mansion Upper Hallway'), 'down': t('Mansion Basement')}
)

Thing('Mansion Steam Engine')(
	magic='More Magic',
	pump_source=t('Mansion Basement Pump'),
	component=1,
	place=t('Mansion Basement Engine Room'),
	synonyms=['steam engine', 'engine', 'dials', 'controls'],
	steam_pressure=550,
	description=observable.Hash({'__MAIN__': 'A large, blocky, metal and brass contraption, with a number of strange attachments. Several hoses and pipes lead out through the wall, floor, and ceiling, and it is also connected to the nearby pressure tank in a number of places. A large brass lever with a red handle is set into the side of the engine, labeled "DANGER: RELEASE VALVE".', 'steam descriptor': ' A circular, glass covered gauge protrudes from the front of the engine, its needle hovering near the 550 PSI mark.', 'magic descriptor': ' There is a rather ominous looking throw-switch labeled "Magic" and "More Magic" attached to the base of the engine, currently set to the "More Magic" position.'})
)

Room('Mansion Study')(
	theme='wood',
	description='A spacious, open room with a high ceiling. A pair of high backed victorian chairs stand near the center of the floor, facing each other over a small, ornately carved wooden table. Glass windowed cabinets line the east and west walls, while arched doorways lead out of the room to the north and south.',
	exits={'south': t('Steam-Powered Library'), 'north': t('Mansion Main Hall')}
)

Room('Mansion Upper Hall')(
	theme='wood',
	attic_staircase=t('attic staircase'),
	exits={'south': t('Mansion Staging Room'), 'up': t('Mansion Attic'), 'north': t('Mansion Laboratory'), 'east': t('Mansion Grand Stair Balcony'), 'west': t('Mansion Stairwell')},
	description=observable.Hash({'__MAIN__': 'A long, wide hallway, ending in arched doorways to the east and west. A dark green carpet runs the entire length of the floor, woven with a complex pattern of intersecting curves.  A pair of doorways are set into the side walls, leading north and south, respectively.', 'attic door state': 'A small wooden ring is hanging from the center of the ceiling by a piece of string.'})
)

Room('Mansion Upper Hallway')(
	theme='wood',
	description=observable.Hash({'__MAIN__': 'A long, wide hallway, ending in an arched doorway to the east. A pair of smaller doors are set halfway along the length of the hall, leading north and south, respectively. A dark green carpet runs along the entire length of the floor, inscribed with a black, twisting pattern of lines and angles.', 'tenths bedroom doors openDesc': 'A pair of double doors stand open at the west end of the hallway.'}),
	exits={'south': t('Mansion Guest Room'), 'north': t('Parlor'), 'east': t('Mansion Stairwell'), 'west': t("Tenth's Chamber")}
)

Room('Mansion West Ballroom')(
	theme='wood',
	description='This ballroom appears to be quite spacious, but it is almost entirely occupied by a massive framework of metal rods, gears, and wheels, leaving only the eastmost edge of the room accessible. Every single piece of the machinery seems to be in motion, whether spinning rapidly or clicking along in slow, measured progression, producing a soft, metallic symphony of ambient sound. A black plastic cable runs along the floor, emerging from deep within the machine and continuing out of the room through the massive archway in the east wall.',
	exits={'east': t('Mansion Main Hall')}
)

Thing('manual')(
	place=t("Damien's Cubicle"),
	description='and can in fact be considred mid-strata evocations, provided of course that the wage para-disclosure is handled via proxy. Also of interest is the government\'s new attempt to garner worker re-compensation allowance dividends in the high yield market. Following the pattern the established for private / cottage income two years ago with 78-Z224, the latest attempt is also prone to flaw. Pro-Dis 6900A, or PD6A as those "in the know" call it, has taken on somewhat of a life of its own of late...\012\012The manual continues in this vein for countless pages.'
)

twisted.author.Author('Maxwell')(
	psyche='0.1',
	health='1.0',
	learned_zorft=1,
	stamina='-0.6537466',
	health_time=930513195556L,
	washed='true',
	oldlocation=t('Demo Center East Wing'),
	learned_frotz=2,
	antecedent=t('development door'),
	spells_learned=5,
	gender='m',
	place=t('Demo Center East Wing'),
	stamina_time=930513195556L,
	password='UkgBvNg9H42Ak',
	synonyms=['max'],
	isLit='false',
	visit_color='ghostly white',
	OBSOLETE_super=t('Class_Human'),
	description=observable.Hash({'__MAIN__': 'A wiry, short man, with grey hair and eyes. His skin tone appears rosy when you look straight at him, but gives you an impression of colorlessness when you see him from the corner of your eye.  His left hand has a clear, black line drawing of a circle on it.', 'clothing': [m('Maxwell','him_her'), ' is wearing ', m('dark grey cape','noun_phrase'), ', ', m('neat grey tunic','noun_phrase'), ', ', m('grey cotton shirt','noun_phrase'), ', ', m('pair of grey jeans','noun_phrase'), ', ', 'and ', m('pair of grey soft leather boots','noun_phrase'), '.']})
)

Thing('maze entrance sign')(
	component=1,
	place=t('Garden Maze'),
	description='This sign has weathered rather poorly, but you can make out the instructions, "HIT BUTTON TO START TIMER."',
	display_name='sign'
)

Thing('maze timer')(
	component=1,
	place=t('Garden Maze'),
	synonyms=['button', 'red button'],
	description="There's not really much to say about this. It's just a red spring-loaded button on some sort of pedestal.",
	display_name='large red button'
)

Thing('Mechanical Pencil')(
	place=t('Blake'),
	synonyms=['pencil'],
	OBSOLETE_super=t('Reality Pencil'),
	description='This pencil is one cool thingie. It has a fancy grip and a brushed steel look to it. Wow. It belongs to Blake. Push off.'
)

Thing('memory dial')(
	component=1,
	place=t('Genetic Laboratory'),
	synonyms=['memory', 'dial'],
	value='0.4',
	OBSOLETE_super=t('Class_Player Creation Dial'),
	description='A black dial.  Look at the machine for a clearer description...'
)

Thing("Meredith's east wall")(
	component=1,
	place=t("Meredith's Hell Hole"),
	synonyms=['wall', 'ewall'],
	description='A collage of random pictures, postcards, and other nonesense hangs on the east wall.'
)

Room("Meredith's Hell Hole")(
	exits={'east': t("Michelle's Dorm Room")},
	description=observable.Hash({'__MAIN__': 'A horribly messy room, whose very walls seem to ooze the stench of hampster feces and vodka.', 'battered gray door openDesc': 'The east door is open.'})
)

Thing("Meredith's north wall")(
	component=1,
	place=t("Meredith's Hell Hole"),
	synonyms=['nwall'],
	description="A rather nondescript Meredith's north wall."
)

Thing("Meredith's south wall")(
	component=1,
	place=t("Meredith's Hell Hole"),
	synonyms=['swall'],
	description="A rather nondescript Meredith's south wall."
)

Thing("Meredith's west wall")(
	component=1,
	place=t("Meredith's Hell Hole"),
	synonyms=['wall', 'wwall'],
	description='A haphazard collection of random stupid pictures hang on the west wall.',
	display_name='west wall'
)

Thing('Message')(
	component=1,
	place=t('A Small Dark Crevice'),
	description='Greetings all... The chambers further on are in midst of construction... Please refrain from entering. THANK YOU FOR LISTENING....Only the foolish continue.'
)

Thing('message post')(
	component=1,
	place=t('Silver Shadowed Glade'),
	description='A crystal clear screen is before you, and shimmering ethereally, written in dark, dripping blood is:    Come follow me into my eternal realm, where the shadows of dusk and dawn are perpetual.  Dare ye dig in my sanctuary...watch well yer back fer ye will find me personally hunting ye down...'
)

Room('Messy New Jersey Office')(
	place=t('Demo'),
	description=observable.Hash({'__MAIN__': 'A strikingly mundane office, with peeling off-white plaster walls and a dirty old gray carpet. The room is lined with desks, all of which are heavily laden with computer equipment, manuals, paper bags, empty bottles, and other trash. A large red and yellow poster has been tacked to the northern wall, above a rather snazzy looking computer, and a black swivel chair is positioned in front of it.', 'development door openDesc': 'A battered wooden doorway in the south wall leads out into the hall.'}),
	exits={'south': t('Demo Center East Wing')}
)

Room('Metal Tube')(
	exits={'southeast': t('Dent in Tube'), 'west': t('End of Catwalk')},
	description='This huge metal tube is spacious and the air is especially clean here.  The edges of the tube gleam with a soft, sourceless illumination.  There is a door out of the tube to the west, and the tube bends around to the southeast and continues.'
)

Thing('meteorite')(
	place=t('recycle bin'),
	description='A scorched piece of rock which, by the pockmarks on its surface and the uneven way that it is shaped, appears to have fallen from the sky.  It is dark grey and smells of scorched iron.'
)

Room("Michelle's Dorm Room")(
	exits={'west': t("Meredith's Hell Hole")},
	description=observable.Hash({'__MAIN__': 'A small, neat room.  You get the impression that whoever lives here has a weakness for Arizona Green Tea.', 'battered gray door openDesc': 'The west door is clearly open.'})
)


twisted.library.clothing.Cloak('midnight blue cloak')(
	place=t('Agatha'),
	synonyms=["agatha's cloak"],
	description='A rather nondescript midnight blue cloak.',
	display_name='cloak'
)

Thing('Mirrored Pencil')(
	place=t('Twin'),
	synonyms=['pencil'],
	OBSOLETE_super=t('Reality Pencil'),
	description='A white box.'
)

Cloudscape('Moonlit Beach')(
	cloudiness='0.08658715',
	theme='water',
	fling_place=t('Cloud Scene Balcony'),
	exits={'east': t('West End'), 'north': t('Between the Cliffs')},
	description=observable.Hash({'__MAIN__': 'This beach is a small alcove in the high walls of cliffs to the east and west.  The sea is smooth, calm, and flat - catching the moonlight as a mirrow would.  A narrow crevice between the cliffs has had a path paved on it through the cliffs to the north.  The moon is shining through a break in the almost overcast cloud-cover above.', 'clouds': "The clouds are as tranquil as a lake on a cool summer's night."})
)

Thing('Mop of Bob')(
	place=t('Tenth'),
	synonyms=['mop'],
	description='A long wooden pole with a soft fabric brush at one end. The words "BOB\'S FUNKY MOP" are painted along the handle, and for some reason unknown to all but Bob himself, it looks totally unfit for mopping or cleaning. However, for a similar reason, it does seem like it would make a good dance partner.'
)

Room('More Mansion Hallway')(
	exits={'east': t('Mansion Hallway'), 'north': t('Music Room'), 'northeast': t('Art Room')},
	description='This is a continuation of the hallway.  The hallway simply ends in a flat wall to the west.  Doors line the northern wall, and through the windows to the south you can see a large pine forest.'
)

Room('More Office Hallway')(
	exits={'west': t('Office Hallway'), 'down': t('Chasm Bottom')},
	description='There is a streak of blackened and burnt area down the center of this hall, terminating in a deep chasm stretching from one side of the hall to the other.  The chasm looks to be rather deep, and dark, though it is lit from the panel lights on the ceiling here.  Far across the chasm you can see this hall continuing.  Looking down into the chasm, you can see footholds that you think will hold your weight.'
)


Room('Music Room')(
	exits={'south': t('More Mansion Hallway')},
	description='Strains of music float through this acoustically perfect room.  The walls are made of a white plaster-like material which seems to reflect sound extremely well.'
)

Room('Musty Section')(
	theme='paper',
	description='This section of the library seems, if possible, even mustier and older than the rest of the books. Glancing casually at a few titles, the books seem to be mostly occult, mostly very old, and mostly bound in human flesh. The library gets rapidly more twisty towards the south, and to the west it opens out into a larger room.',
	exits={'south': t('The Twisty Bit'), 'west': t("Damien's Office,entering")}
)

Room('Mystic Field')(
	theme='leaf',
	description='',
	exits={'south': t('Garden Maze(14)')}
)

Room('Myth Section')(
	theme='paper',
	description='This is a room dedicated to the preservation of myths. Stone statues punctuate the shelves occasionally, and all of the books look ancient and very important. They are in as good a condition as could be expected for their great age and apparently frequent use. There is a pillar in the center of the room here with nothing on it, and a door to the north. A shadowy corner to the southwest has a small sign hanging over it that says "Occult Myths". An unmarked corrider wanders off westward.',
	exits={'southwest': t('The Twisty Bit'), 'west': t('Unmarked Corridor'), 'north': t('Bookstore Stairwell, Level 9')}
)

Thing('naka-mon')(
	obstructed='false',
	exit_message='You stoop down and humbly step through the central gate.',
	component=1,
	place=t('Outer Tea Garden'),
	synonyms=['central gate'],
	obstructed_message='You must open the gate before you can enter.',
	OBSOLETE_super=t('Class_Door'),
	description='The low gate forces even highly-ranked guests to stoop low, reminding them to discard all thoughts of their worldly status upon entering the tea garden.'
)

Thing('name changing machine')(
	component=1,
	place=t('Science and Technology Demo Center'),
	synonyms=['keyboard', 'machine', 'key', 'booth', 'nominator', 'monitor'],
	description=observable.Hash({'__MAIN__': 'A large stainless steel structure vaguely reminiscent of a phone booth, with an embedded monitor and keyboard, featuring a prominent "Execute" key.', 'screen': 'The screen is black, except for "Effeminate Sailor" in large green letters.'}),
	new_name='Effeminate Sailor'
)

Room('Natural Alcove')(
	theme='paper',
	exits={'west': t('Precarious Ledge'), 'up': t('Under the Bookshelf')},
	description='The floor slopes gradually downward, forming a natural alcove under the floorboards. The air is damp down here, and what little light there is filters in from above. There is a rough pathway leading off to the left, and the alcove ends in a blank wall to the right. In front of you the floor begins to slope downward rather drastically. You can crawl back up as well.'
)

twisted.library.clothing.Tunic('neat grey tunic')(
	place=t('Maxwell'),
	synonyms=['tunic'],
	description='A clean and well-pressed light grey tunic made from high-quality fabric.'
)

Room('New Jersey Apartment Bathroom')(
	theme='default',
	description='A small, entirely off-white and beige bathroom. The sink is a tall, vaguely flower-shaped work of ceramics, but despite its graceful appearance, it looks rather unsteady, swaying slightly in tune to the unusual sounds of the plumbing. A toilet is set alongside it, considerably more steady, and the opposite side of the room is dominated by a combination shower/bathtub. The shower head is dripping at a slow, measured pace, producing a metallic clinking noise as each drop hits the temperature dials below it. A plastic towel rack and shampoo basket stands by the tub, laden with shampoos, conditioners, and soap.\012',
	exits={'north': t('New Jersey Apartment Hallway')}
)

Room('New Jersey Apartment Bedroom')(
	theme='default',
	description='A long, rectangular room, with a dark brownish carpet, and windows set into the corners of the north and east walls. The floor is dotted with clothes, books, and software instruction manuals, forming somewhat of a trail between a bare matress, a pile of sheets, and the closet set into the west wall.\012',
	exits={'southwest': t('New Jersey Apartment Hallway')}
)

Room('New Jersey Apartment Entrance Hall')(
	theme='default',
	description='A small room with a mirror and end table against one wall, and four different doors. Two of them are white and identically paneled, leading west and presumably out into New Jersey itself. The other two are made of dark brown wood, one closed and firmly locked, and the other standing open, to a flight of stairs leading upwards\012',
	exits={'up': t('New Jersey Apartment Living Room')}
)

Room('New Jersey Apartment Guest Room')(
	theme='default',
	description='A bare, empty room, with a hardwood floor, and two unshaded windows, in the east and south walls, respectively. A pile of boxes are stacked against the east wall, filled with books and computer paraphenalia, but they do little to add a sense of presence to the room.\012',
	exits={'west': t('New Jersey Apartment Hallway')}
)

Room('New Jersey Apartment Hallway')(
	theme='default',
	description='A dimly lit, narrow hallway, with an ugly reddish pink carpet. To the south, a door is open into what looks like a bathroom, and there are additional doors crammed into the hall to the east, northeast, and north. \012',
	exits={'south': t('New Jersey Apartment Bathroom'), 'north': t('Other New Jersey Apartment Bedroom'), 'east': t('New Jersey Apartment Guest Room'), 'northeast': t('New Jersey Apartment Bedroom'), 'west': t('New Jersey Apartment Kitchen')}
)

Room('New Jersey Apartment Kitchen')(
	theme='default',
	description='The ugly pinkish shag carpeting of the floor gives way to white plastic tiles along the northern half of the room, where a small kitchen area is formed by a wall of old wooden cabinets, a sink, an ancient looking gas stove, and a refrigerator, all an almost identical shade of brown. A rickety looking table and two folding chairs sit on the kitchen floor, below a telephone attached precariously to the wall. There are windows over the sink and in the opposite wall, but each only provides a view of the walls of other nearby buildings. A combination ceiling fan and light fixture is buzzing away overhead, in contrast to the low, echoing burbles from the air conditioner.\012',
	exits={'east': t('New Jersey Apartment Hallway'), 'west': t('New Jersey Apartment Living Room')}
)

Room('New Jersey Apartment Living Room')(
	theme='default',
	description="A large, square room with ugly reddish pink carpeting, and a large picture window shaded by hanging blinds. A pitifully small grey monitor is set up in the far corner of the room, on top of a small black VCR, next to a sony playstation which is lying upside down on the carpet, apparently held together with duct tape. A staircase leads down to the front door, with a smaller wooden door attached between its railing and the wall of the living room, probably to keep the previous tenant's children out of trouble. The room and its ugly carpet continue to the east.\012",
	exits={'east': t('New Jersey Apartment Kitchen'), 'down': t('New Jersey Apartment Entrance Hall')}
)

Container('New Jersey Apartment Refrigerator')(
	component=1,
	place=t('New Jersey Apartment Kitchen'),
	synonyms=['frige', 'fridge', 'refrigerator'],
	OBSOLETE_super=t('Class_Container'),
	description="A large, brown metal box, with a blue and white interior. It's sort of cold inside, but not remarkably so. There are a few stray packets of jello pudding lurking in the back, but nothing substantially like food."
)

Room('Nice Office')(
	exits={'south': t('Reception Area'), 'north': t('Small Grey Room')},
	description="This is a plush office, well-decorated and hardly damaged at all. There are a few minor dents and cracks in the ceiling, but other than that there's not much wrong here.  A large desk and wheeled chair (both bolted to the floor) adorn the western end of the room."
)

Container('nightstand')(
	component=1,
	place=t("Guyute's Bedroom"),
	OBSOLETE_super=t('Class_Closeable Container'),
	description='This nightstand is made of mahogany. It has a small drawer in the front, upon which is a small brass handle.'
)

Thing('Nominator Manual')(
	read_text='     "Personalize your visit to our demo center with the Nominator 5000! Simply type your desired name on the supplied ergonomic keypad, and press the execute key when the name on the screen meets with your approval! A fun and easy way to increase your self worth and make your stay here a somewhat more memorable one.\012\012     (WARNING: SEVERE EYE DAMAGE: The Twisted Matrix Enterprises Nominator Model 5000 may contain near-unpronouncable quantum effects. Do not look directly into the singularity.)"',
	place=t('science and technology demo center table'),
	synonyms=['manual'],
	repop=t('science and technology demo center table'),
	description='A large grey plastic binder, titled "Nominator 5000: A Reference Manual". It only seems to contain a few pieces of paper, but would probably be very useful if you wanted to read about the functions of the Nominator.'
)

Room('Nondescript Section')(
	theme='paper',
	description='This is a rather nondescript area.',
	exits={'southeast': t('Bookstore Stairwell, Level 8')}
)

Room('North of House')(
	exits={'southwest': t('West of House'), 'southeast': t('Behind House')},
	description='You are facing the north side of a white house. There is no door here, and all the windows are boarded up. To the north a narrow path winds through the trees.'
)

Room('Northern End of Small Forest')(
	theme='leaf',
	description='This is the northern end of a small forest, where your way is blocked by a huge rock wall.  Looking upward, you can see the cliff extending up far into the clouds.  Someone has scrawled something in white paint at about eye-level on the cliff.',
	exits={'south': t('Clearing in Small Forest')}
)

Thing('northern tapestry')(
	obstructed='true',
	exit_message='You go north through the hidden doorway.',
	component=1,
	place=t("Guyute's Bedroom"),
	synonyms=['tapestry', 'north'],
	obstructed_message="You can't go that way",
	OBSOLETE_super=t('Class_Door'),
	description='This tapestry depicts a disasterous scene, with people and other creatures running in vain. It appears that some sort of meteor shower is occurring; at least, large, flaming rocks are flying down out of the sky.'
)

Thing('note')(
	place=t('Supply Closet'),
	description='This is a yellow sticky note.  It reads,"Tenth: you might want to hide one of your vacuum tubes in here."'
)

Thing('notebook')(
	warp_here_as_moo=t('A Dark Narrow Passage'),
	warp_default=t('Genetic Laboratory'),
	place=t('James'),
	warp_demo=t('Twisted Reality Corporate Demo Center'),
	description='This notebook has a table of names and places scrawled on it.'
)

Thing('notice')(
	component=1,
	place=t("Damien's Cubicle"),
	synonyms=['calender'],
	description='Some office junk.\012\012\012You look again, but all you learn is that there is some paper stuck to the wall here.\012\012You look closely, but you still cannot tell if it is a calender, a memo, or possibly a list of phone numbers.'
)

Thing('obelisk welcoming text')(
	component=1,
	place=t('Demo Information Center'),
	synonyms=['welcoming text', 'text', 'piece of text', 'large piece of text'],
	description='Despite being in a large, white Times Roman font on a black background, you can\'t quite seem to make out what it says. Something along the lines of "Welcome to our demonstration center, home of Twisted Matrix Enterprises..." but after that, your eyes begin to glaze over. Jumbled, run-on sentences are twined with phrases like "Enterprise Wide", "Networked Scalability", and "Multithreaded Dynamic Architecture", which, while compelling, destroy any meaning the text may have had.'
)

Room('Obscure Corner of Bookstore')(
	theme='paper',
	exits={'southwest': t('Rare Book Room, Lower Level')},
	description='This is an obscure corner of a bookstore.  Though the books are worn with age, they are nontheless in surprisingly good condition. The room has a sense of tiredness but it is kept well. There are few books here, and the place seems deserted, but footprints lie in the accumulated dust which signify that this place was not always as neglected. There is an exit to the southwest to a slightly brighter and more spacious room.',
	special_thing=t('small brown book')
)

Room('Observation Hallway')(
	exits={'west': t('Guest Chamber'), 'southeast': t('East Wing Spiral Staircase Top'), 'north': t('Jewel Bedecked Hallway')},
	description='This is an oblong rectangular room with a set of windows built into the southern wall.  The walls are all built from a pure, white marble.  The windows overlook a rocky plain from far above.  Far in the distance, you can make out a large stone altar with large black scorch-marks on and surrounding it.  A large marble archway leads north, into a multi-colored glittering hallway, and a modest doorway in the southeastern corner bears the legend "stairs".  Another, perhaps even more modest, door is set into the western wall, with the legend "Guest Room".'
)

Room('Odd Curve')(
	theme='paper',
	description='You stand in an odd curve in an aisle of books.  The hallway twists as if it were curving about a large mass to the southeast. There is a door at the end of the aisle to the northeast labled "stairs" and to the south, the passage straightens out and continues.',
	exits={'northeast': t('Bookstore Stairwell, Level 7'), 'south': t('Aisle 3.')}
)

Container('oddly built brass and metal chair')(
	maximum_occupancy=1,
	place=t('Mansion Staging Room'),
	synonyms=['chair', 'metal chair', 'brass and metal chair', 'brass chair', 'oddly built chair'],
	preposition='on',
	player_preposition='sitting on',
	description='A wooden chair set into a large metal contraption, covered with tubes and wires and ending in a large brass dome over the head of the person unfortunate enough to be sitting in it.'
)

Room('Office Hallway')(
	exits={'east': t('More Office Hallway'), 'west': t('Reception Area')},
	description='This hallway exhibits a peculiar pattern of decay.  Down the center of the hallway, there is an area that looks badly damaged, and blackened, as by an electrical storm.  This swath of destruction extends down the hallway to the east and west, and to the doors leading north and south.'
)

Thing('oil can')(
	place=t('Mansion Maintenance Closet'),
	synonyms=['can'],
	description='A small brass can fitted with a long, thin nozzle, and a crudely bent piece of metal which was probably intended to be used as a handle.'
)

Thing('oil painting')(
	component=1,
	place=t('Natural Alcove'),
	synonyms=['painting'],
	description='An unfinished masterwork. The composition is brilliant and the colours are so vibrant that they tremble with life. The subject is pastoral, showing a forest pool with satyrs at play, but the bottom corner has not been finished. A few lines of charcoal sketch out the rest of the scene, but the artist apparently changed his mind about it. Instead of finishing the satyr, the unknown painter covered over that corner with two words in bright carmine: "Help Me".'
)

Thing('old book')(
	place=t("Damien's Study"),
	synonyms=['old', 'book'],
	description='A book written in an indescribable language, discussing unmentionable things in an ineffable style.'
)

Thing('old sandal')(
	place=t('large black cauldron'),
	description='An rather nondescript old sandal.'
)

Thing('old wooden door')(
	place=t('Mansion Study'),
	theme='default',
	target_door=t('old wooden doorframe'),
	synonyms=['wooden door', 'door', 'knob', 'brass knob'],
	description='An old, weathered looking door made of dark, greyish wood, mounted in a doorframe of the same material. A brass knob is set into the door at waist level, worn and dented in a few places but still appearing to have been polished recently.'
)

Thing('old wooden doorframe')(
	component=1,
	place=t('Mansion Entrance Hall'),
	synonyms=['wooden doorframe', 'wooden door', 'doorframe', 'door', 'knob', 'brass knob', 'doorknob'],
	target_door=t('old wooden door'),
	description='An old, weathered looking door made of dark greyish wood, mounted in a doorframe of the same material. A brass knob is set into the door at waist level, worn and dented in a few places but still appearing to have been polished recently.'
)

Thing('orange')(
	eat_text_1='You peel the ',
	eat_text_2=" and eat it... It's a little chewy, but juicy and delicious.",
	place=t('Tsiale'),
	description='It appears to be a orange, but it is vague, indistinct, and little more than a blurry smear on reality.'
)

Thing('orange cube')(
	teleport_phrase_I_leave_now=t('Myth Section'),
	place=t('Cold Floor'),
	synonyms=['cube'],
	description='A white box.'
)

Thing('organic stuff')(
	component=1,
	place=t("Damien's Study"),
	synonyms=['organic', 'stuff', 'thread', 'goop'],
	description="A bit of organic... stuff. Some of this goop looks like a spider's thread, while in other places it seems more like carpenter's plaster. In all cases it is smooth, slightly sticky, and strong as hell."
)

Container('ornate wooden table')(
	place=t('Smoking Room'),
	theme='wood',
	synonyms=['table', 'wooden table', 'ornate table'],
	OBSOLETE_super=t('Class_Container'),
	description='The wooden legs of this table curve at the ends into what seem like paws of some animal. The surface is polished and bright, showing a beautiful grain.'
)

Container('Other Box')(
	place=t('Class Room'),
	synonyms=['box'],
	description='A perfectly white box labeled "Other Classes" in neat black letters.'
)

Room('Other New Jersey Apartment Bedroom')(
	theme='default',
	description='A fair sized room, with bluish wallpaper and a darker, brownish shag carpet. The two windows are set with dark brown shades, and a small closet is built into the east wall, with sliding wooden doors that seem a bit too large for it. A number of boxes are stacked up in the corners of the room, and a set of blankets are folded up on the floor in semblance of a bed, next to a suitcase strewn with brushes, hair ties, and an electric razor.\012',
	exits={'south': t('New Jersey Apartment Hallway')}
)

Room("Other Underling's Office")(
	exits={'northwest': t('Reception Area')},
	description='This is an office, most likely that of someone in a relatively low position.  There is a desk here, and also a chair, both of which are bolted to the floor.  The place is clean, but the walls are undecorated, and the space is small.  The smashed remains of a computer terminal litter the desk and floor.'
)

Room('Outer Tea Garden')(
	theme='leaf',
	exits={'east': t('Ivy Garden'), 'west': t('Garden Maze'), 'north': t('Inner Garden')},
	description='You are in a traditional tea garden. A central gate separates this outer garden from the inner garden. The low gate forces even highly-ranked guests to stoop low, reminding them to discard all thoughts of their worldly status upon entering the tea garden. This area is surrounded by a wrought-iron fence.',
	display_name='Soto-rojj'
)

Thing('painting')(
	place=t("Tenth's Chamber"),
	painting_realm=t('A Swirling Mass Of Colors'),
	description='divunal.random.PaintingDescription',
	description_1='It appears to be a painting of a scenery of some sort, vague and indistict.  The whole painting is covered with soft colors, swirling and undulating in patterns that tease the mind. They almost seem to be moving...',
	description_2='It appears to be a painting of a scenery of some sort, vague and indistict.  The whole painting is covered with soft colors, swirling and undulating in patterns that tease the mind. They are definitely moving.'
)

Thing('pair of black dockers')(
	place=t('Test Bed'),
	synonyms=['black dockers', 'dockers'],
	description='A white box.'
)

twisted.library.clothing.Shoes('pair of black leather boots')(
	component=1,
	place=t('Tenth'),
	synonyms=['black leather boots', 'leather boots', 'boots'],
	clothing_appearance='knee high black leather boots',
	description='A pair of tall black leather riding boots, the tops of which have been folded down to knee length to make them less restrictive.'
)

twisted.library.clothing.Shoes('pair of black leather shoes')(
	place=t('Tsiale'),
	synonyms=['shoes', 'leather shoes'],
	description='It appears to be a pair of black leather shoes, but it is vague, indistinct, and little more than a blurry smear on reality.'
)

twisted.library.clothing.Pants('pair of black pants')(
	place=t('Tsiale'),
	synonyms=['leggings', 'pants'],
	clothing_appearance='black leggings',
	description='A pair of close-fitting black pants, apparently made from a single, seamless piece of fabric.'
)

twisted.library.clothing.Spectacles('pair of brass framed spectacles')(
	place=t('Tenth'),
	synonyms=['brass framed spectacles', 'spectacles', 'lenses', 'lens', 'glasses'],
	color='green',
	description='A pair of brass framed spectacles with green colored lenses, each of which is set in some sort of odd mechanism which apparently allows them to be rotated.',
	display_name='pair of green-tinted spectacles'
)

twisted.library.clothing.Shoes('pair of brown leather boots')(
	place=t('Agatha'),
	synonyms=['boots', 'brown boots'],
	clothing_appearance='leather boots',
	description='A rather nondescript pair of brown leather boots.'
)

twisted.library.clothing.Shorts('pair of dark blue shorts')(
	place=t('James'),
	synonyms=['shorts', 'blue shorts'],
	description='A white box.'
)

twisted.library.clothing.Shorts('pair of green boxer shorts')(
	place=t('Tenth'),
	synonyms=['shorts', 'boxer shorts'],
	description='A pair of dark green silk boxer shorts'
)

twisted.library.clothing.Socks('pair of green socks')(
	place=t('Tenth'),
	synonyms=['socks', 'green socks'],
	description='A pair of shin high green cotton socks.'
)

twisted.library.clothing.Pants('pair of grey jeans')(
	place=t('Maxwell'),
	synonyms=['jeans', 'slacks', 'pants'],
	description='A white box.'
)

twisted.library.clothing.Shoes('pair of grey soft leather boots')(
	place=t('Maxwell'),
	synonyms=['boots', 'grey boots'],
	description='A pair of suede boots in a muted grey color.'
)

twisted.library.clothing.Spectacles('pair of metal-rimmed spectacles')(
	place=t('Rikyu'),
	synonyms=['xray glasses', 'metal-rimmed glasses', 'glasses', 'spectacles'],
	description='A rather nondescript metal-rimmed spectacles.'
)

twisted.library.clothing.Shoes('pair of sandles')(
	place=t('James'),
	synonyms=['sandles'],
	description='A white box.'
)

twisted.library.clothing.Pants('pair of silk pants')(
	place=t('Rikyu'),
	synonyms=['pants', 'silk pants'],
	description='A rather nondescript silk pajamas.'
)

twisted.library.clothing.Shoes('pair of sturdy leather boots')(
	place=t('Blake'),
	synonyms=['boots'],
	description='These boots look as if they have had a lot of use. They are made of reinforced leather for strength and flexibility.'
)

twisted.library.clothing.Pants('pair of tan cargo pants')(
	place=t('Blake'),
	synonyms=['pants', 'jeans'],
	description='A rather nondescript pair of tan cargo pants.'
)

Container("pale blue robe's left sleeve")(
	component=1,
	place=t("Yumeiko's pale blue kimono-like robe"),
	synonyms=['lsleeve'],
	description="The pale blue robe's left sleeve."
)

Container("pale blue robe's right sleeve")(
	component=1,
	place=t("Yumeiko's pale blue kimono-like robe"),
	synonyms=['rsleeve'],
	description="The pale blue robe's right sleeve."
)

Room('Parlor')(
	theme='wood',
	description='A parlor.  Describe me?',
	exits={'south': t('Mansion Upper Hallway')}
)

Room('Path in the Clouds')(
	exits={'east': t('Portrait in the Sky'), 'northwest': t('Twisty Cloud Path')},
	description='This is a wide, smooth stone path through a sea of clouds. The path curves around here. To your west you can see a tall castle in the clouds with many gravitationally impossible protrusions, and to your east you see what looks like a small square at the end of the path.'
)

Container('Pedestal')(
	maximum_occupancy=1,
	place=t("Tenth's Chamber"),
	preposition='on',
	description='A dark, polished wooden pedestal.'
)

Thing('phaser')(
	place=t('dark green overcoat'),
	synonyms=['device', 'plastic device'],
	description='A smooth grey device, shaped in such a way as to rest easily in the palm of your hand. It terminates in a small, glossy black protrusion, and has no visible controls or attachments.',
	display_name='oblong plastic device'
)

Thing('photograph')(
	place=t("Damien's Cubicle"),
	synonyms=['photo'],
	description='A small color photograph has been inserted somewhat unevenly into this black wooden frame. A small "leg" sticks out the back of the cheap, wooden, dyed-black frame, enabling the assemblage to stand upright on the desk.\012\012The photograph is of a large group of people, all of whom look related and poorly posed. Most of the men and a few of the women are wearing nice-looking suits, except for one guy in the back. He is dressed for a safari, in a photographer\'s jacket and headband. You can almost see the pith helmet he assuredly carries in his arms. The rest of the family seems to be avoiding him in the photo.'
)

Thing('piece of skystone')(
	morph_gender_jello='neutral',
	morph_gender_nymph='female',
	morph_gender_old='male',
	morph_name_jello='Gelatinous Cube',
	morph_name_old='Elderly man',
	synonyms=['skystone', 'stone'],
	morph_descr_old='A feeble looking creature, this man seems to have been through a lot in his long lifetime.',
	morph_name_nymph='Elven wood nymph',
	place=t('Secret Chamber'),
	description='This appears to be a fragment of a much larger piece of stone. It feels warm to the touch: almost as if it has some sort of internal power. One side of the stone glows a soft blue color, while the other is simply a beautiful deep blue.',
	morph_descr_nymph='An adorable-looking wood nymph.',
	morph_descr_jello='A rather squishy cube of an unknown substance.'
)

Thing('pig skull')(
	place=t('large black cauldron'),
	description='The poor creature!'
)

Thing('pile of leaves')(
	place=t('Forest 2'),
	synonyms=['leaves'],
	description='A white box.'
)

Thing('pile of things')(
	component=1,
	place=t("Damien's Cubicle"),
	synonyms=['pile', 'things'],
	description='A bunch of stuff is stacked along the wall.\012\012No matter how much effort you put into it, this is all you can tell. A bunch of stuff is stacked against the wall.'
)

Room('Pine Grove')(
	theme='leaf',
	description='South of this grove, you can two large cliffs flanking the small dirt path you are standing on. To your west, the path continues on its winding way through the trees. The trees are far too dense for you to proceed in any direction except along the path to the west, but they thin considerably to the south.',
	exits={'west': t('Mansion Doorstep')}
)

Room('Plain Room')(
	exits={'west': t('Cold Floor')},
	description='null'
)

Thing('plaque')(
	component=1,
	place=t("Blake's Sphere"),
	description='The plaque is made of bronze and is firmly affixed to the surface of the sphere. "Welcome to Blake\'s Sphere!" is emblazoned across it in stenciled lettering.'
)

Container('plastic swivel chair')(
	place=t('Genetic Laboratory'),
	synonyms=['swivel chair', 'chair'],
	description='It appears to be a ergonomic swivel chair, but it is vague, indistinct, and little more than a blurry smear on reality.'
)

Thing('player creation machine')(
	component=1,
	dexterity=t('dexterity dial'),
	agility=t('agility dial'),
	memory=t('memory dial'),
	place=t('Genetic Laboratory'),
	synonyms=['release', 'randomize', 'generate', 'machine', 'controls', 'control panel', 'panel'],
	psyche=t('psyche dial'),
	tube=t('long glass tube'),
	endurance=t('endurance dial'),
	description='The control panel of the machine has three buttons, labeled "GENERATE", "RELEASE", and "RANDOMIZE", and six dials, each labeled and marked on a range from -1.0 to 1.0.  There are two black rectangles above the control panel, each with an engraved label in the silver below, "Point Total" and "Name" respectively, and immediately below those, there is a silver keyboard. ',
	strength=t('strength dial')
)

Room('Portrait in the Sky')(
	exits={'east': t('Art Gallery'), 'west': t('Path in the Clouds')},
	description='To the east, the path you are standing on ends at a picture frame framing what looks to be a hole in the sky.  Through the frame you can see a library room, as if it were a window.  To the west you can see a path leading to a tall castle far in the distance.'
)

Thing('post-it')(
	place=t("Damien's Cubicle"),
	description='I suppose I could e-mail you, but this is better. I\'m sure.\012\012How do I check to see if the directObject() matches a particular object I have in mind? If the user uses my foo verb, and types "foo troll with sword" how can I check to see that it is fooing a troll, so that I can respond "You foo the troll hard and fast" or some such. Make sense?\012\012Thanks,\012Benjamin (currently still in control of Damine\'s motor functions, poor guy will be even MORE confused soon!)'
)

Thing('potted plant')(
	component=1,
	place=t('Twisted Reality Corporate Demo Center'),
	synonyms=['pot', 'plant', 'green potted plant', 'green potted plants', 'plants', 'potted plants', 'pots'],
	description="All of the plants bear a striking resemblance to one another, having the same number of leaves in approximately the same position, each set into an indentical grey marble pot with it's own tiny engraved brass label. Despite being an almost preternatural shade of green, the plants themselves bear a striking resemblance to palm trees, albeit ones that had been fitted with extra leaves and subjected to some sort of bonsai-like stunting process."
)

Room('Precarious Ledge')(
	theme='paper',
	description='The forces of erosion have conspired to eat away at the rock underneath your feet until the ledge you stand on is no more than a few feet thick. To the south and north is the comforting solidity of a rock wall, but to the west is a dizzying exspanse of nothing.\012The rock wall is covered in a phospherescent moss that provides enough light to see the ledge you are standing on, but not enough light to see anything to the west. For all you can tell, it is a void.  On the wall there is an sign with an arrow pointing west, reading "Do not go that way.  You probably won\'t be able to get out."  Below it, there is another, apparrently written in blood, that says "We\'re not even kidding. Really."',
	exits={'east': t('Natural Alcove'), 'west': t('Darkness')}
)

twisted.library.clothing.Pants('pressed pair of black slacks')(
	place=t('Agatha'),
	synonyms=['slacks', 'black slacks'],
	description='A rather nondescript pressed pair of black slacks.'
)

Room('Proper English Library')(
	theme='paper',
	description='This room has the works: wall to wall plush shag carpeting, leather clad chairs and oaken tables. Obviously the walls are paneled in bookcases. In the center is a huge wooden table. \012\012It looks as though someone has set up camp here: the room is covered in neatly stacked piles of paper, coffee mugs, and empty chinese food cartons.',
	exits={'east': t('Musty Section'), 'west': t('Hallway')}
)

Room('Psychadelic Room')(
	theme='weird',
	description='This room has no apparent purpose. The garish colors and pulsating, disorienting distortions of space in here would distort your orientation completely if it were not for the fact that there is only one door to the south.',
	exits={'south': t('Mansion Hallway')}
)

Thing('psyche dial')(
	component=1,
	place=t('Genetic Laboratory'),
	synonyms=['psyche', 'dial'],
	value='0.0',
	OBSOLETE_super=t('Class_Player Creation Dial'),
	description='A white box.'
)

Container('qin')(
	place=t("pale blue robe's right sleeve"),
	description='A kind of seven-stringed zither made of a rosy wood.  The strings seem iridescent, as if waves of color and light pass through them.  The base of the instrument is very delicately etched with almost imperceptible whorls and floral patterns.  There are seven very tiny, metal knobs with which to tune the instrument.'
)

Thing('quantum')(
	place=t('quantum singularity'),
	description='A rather nondescript quantum.'
)

Container('quantum singularity')(
	component=1,
	place=t('Messy New Jersey Office'),
	synonyms=['singularity'],
	description='A blue box.'
)

Room('Quiet Niche')(
	theme='paper',
	description='This small alcove is formed by the convergence of two large bookshelves. One shelf contains a number a books about anthropology and ancient civilizations, the other is stacked with volumes and volumes of poetry.\012There is a much wider area to the southeast, and perhaps you could squeeze under the western shelf.',
	exits={'west': t('Under the Bookshelf'), 'northwest': t('Wider Area')}
)

Thing('rainbow trout')(
	place=t('recycle bin'),
	synonyms=['fish'],
	description='Looks like a rainbow trout. About seven inches long, way too small. It would probably be best to find a body of water to put it in.'
)

Room('Rare Book Room, Lower Level')(
	theme='paper',
	description='This is the lower level of the Rare Book room of a bookstore, as a sign hanging from the ceiling indicates.  There are many books here and they all appear well cared-for. There is a passageway to the northeast leading to a slightly less-used corner of the room. A rickety metal spiral staircase leads upward.',
	exits={'northeast': t('Obscure Corner of Bookstore'), 'up': t('Rare Book Room, Upper Level')}
)

Room('Rare Book Room, Upper Level')(
	theme='paper',
	description='This is the upper level of a Rare Book room, as a sign hanging from the ceiling says.  There is a staircase leading down to the lower level in the corner of the room, and a wooden door with a frosted glass window to the west.',
	exits={'southwest': t('Bookstore Stairwell, Level 6'), 'down': t('Rare Book Room, Lower Level')}
)

Thing('Reality Brush')(
	place=t("pale blue robe's left sleeve"),
	synonyms=['brush'],
	OBSOLETE_super=t('Reality Pencil'),
	description='A white box.'
)

Thing('Reality Pencil')(
	place=t('Maxwell'),
	synonyms=['pencil'],
	isLit='false',
	description='This is a regular Number Two pencil, brought here from the real world.  It holds the power of ultimate creation and destruction.'
)

Room('Reception Area')(
	exits={'south': t('Broken Office'), 'north': t('Nice Office'), 'east': t('Office Hallway'), 'southeast': t("Other Underling's Office"), 'west': t('Cramped Transporter Booth')},
	description='This area, though quiet, looks as if it were once bustling with activity.  It also looks as if it were rather heavily abused in its last few days of usefulness.  Most of the room is relatively undamaged, but there is a visible swath of destruction leading from the western door to the southern and eastern edges of the room.  There is a large granite desk here with many devices that look as if they might be used for communication bolted to it.'
)

Container('recycle bin')(
	place=t('Class Room'),
	synonyms=['bin'],
	description='A light green plastic bin of seemingly infinite proportions, yet still small enough to fit conveniently under a desk. It is emblazoned with a triangular pattern of arrows, and looks like just the sort of place where unwanted or innappropriate objects would be put, to be rescued by their owners, or, failing that, periodically erased.'
)

Thing('Red marker')(
	place=t('James'),
	synonyms=['marker'],
	OBSOLETE_super=t('Reality Pencil'),
	description='A red marker, suitable for making corrections to works of other people.'
)

Thing('reference book')(
	place=t('Proper English Library'),
	synonyms=['book'],
	description='An Overview of the DR-127 Departure/Withdrawal Forms and Their Application in Income-Based RCFs.\012\012It seems quite thick.'
)

Thing('reference manual')(
	place=t("Damien's Study"),
	synonyms=['manual', 'reference'],
	description='A Friendly Guide to Form 6900A.\012\012Dept. Clarification and Simplification\012Bureau 923100-A6, Section 23\012Internal Revenue Service'
)

Thing('registry')(
	place=t('great bookshelf'),
	synonyms=['book', 'phonebook', 'yellow book', 'paperback book', 'paperback'],
	replace=t('great bookshelf'),
	description='A very informative piece of work.',
	display_name='yellow paperback book'
)

twisted.author.Author('Rikyu')(
	psyche='1.0',
	dexterity='1.0',
	memory='1.0',
	health='1.0',
	stamina='-0.1',
	health_time=947253784314L,
	washed='true',
	mindspeak='0.1',
	teleport_in='seems to step through a great tear in the fabric of reality, which then closes behind him.',
	oldlocation=t('Mansion Basement Engine Room'),
	learned_frotz=1,
	strength='0.3',
	stamina_time=947253784314L,
	spy='0.1',
	spells_learned=4,
	gender='m',
	learned_posess=2,
	synonyms=['sen rikyu'],
	teleport_out='begins to spin at a great speed, then disappears in a brilliant flash of light.',
	learned_zorft=1,
	endurance='0.0',
	OBSOLETE_super=t('Class_Human'),
	description=observable.Hash({'__MAIN__': 'A life of seventy years,\012Strength spent to the very last,\012With this, my jeweled sword,\012I kill both patriarchs and Buddhas.\012I yet carry\012One article I had gained,\012The long sword\012That now at this moment\012I hurl to the heavens. \012\012', 'clothing': [m('Rikyu','him_her'), ' is wearing ', m('brown kimono','noun_phrase'), ', ', 'and ', m('pair of silk pants','noun_phrase'), '.']}),
	agility='0.0'
)

Thing('ring bell sign')(
	component=1,
	place=t('teakwood podium'),
	synonyms=['small sign', 'sign', 'white sign'],
	description='The sign reads:\012\012"RING BELL FOR SERVICE."',
	display_name='small white sign'
)

Room('Rocky Ledge')(
	exits={'up': t('Canyon View'), 'down': t('Canyon Bottom')},
	description='You are on a ledge about halfway up the wall of the river canyon. You can see from here that the main flow from Aragain Falls twists along a passage which it is impossible for you to enter. Below you is the canyon bottom. Above you is more cliff, which appears climbable.'
)

Room('Rocky Ledge, further west')(
	exits={'east': t('Ledge in front of Castle in the Clouds'), 'west': t('Very Narrow Rocky Ledge')},
	description='To your east, there appear to be some steps where you can ascend to the looming palace above.  To the west there lies more of a ledge.'
)

Thing('room')(
	place=t('Wrecked Street'),
	description='A blue box.'
)

Container('Room Box')(
	place=t('Class Room'),
	synonyms=['box'],
	description='A perfectly white box labeled "Room Classes" in neat black letters.'
)

Room('Rough Corridor')(
	exits={'back': t('Rough Floor')},
	description='null'
)

Room('Rough Floor')(
	inhibit_exits='true',
	theme='greystone',
	inhibit_items='true',
	display_name='A Dark Place',
	OBSOLETE_super=t('Class_Dark Room'),
	exits={'south': t('Cold Floor'), 'north': t('Rough Passage')},
	description="It's too dark in here to see!"
)

Room('Rough Passage')(
	theme='greystone',
	description='For the first time in a while you can feel walls. There are two of them, in fact, on on either side of you. Both feel like normal rock walls: slightly damp, slightly cold and very solid. The floor beneath your feet continues to be quite rough and strewn with rubble. The walls continue on for at least a few more feet to the north, so it must be safe to follow them.',
	exits={'south': t('Rough Floor')}
)

Thing('Ruby Cube')(
	component=1,
	place=t('Ruby Room'),
	synonyms=['cube'],
	OBSOLETE_super=t('Class_Cube'),
	description='A cube composed from something quite like ruby.  Through its translucent surface, though, you can see lights like stars, slowly growing and diminishing and intensity.'
)

Room('Ruby Room')(
	exits={'east': t('Jewel Bedecked Hallway')},
	description="This room is a study in red.  While you can make out no light source, light must be filtering in through the ruby ceiling to get down here, where it reflects off of the myriad facets of the room's walls and floor.  There are no markings anywhere, and the only real feature of the room is a cube, which appears to be part of the floor, made of the same ruby substance that composes the rest of the room, but glittering more brightly."
)

Thing('rug')(
	component=1,
	place=t('Hallway'),
	description='The design on this rug is extremely intricate; it must have cost a lot of money. The rug itself is very heavy and thick.'
)

Chair('rustic loveseat')(
	maximum_occupancy=2,
	place=t('Smoking Room'),
	synonyms=['loveseat'],
	preposition='on',
	player_preposition='sitting on',
	description='A wonderfully soft leather chair.'
)

Thing('rusting silver inkwell')(
	place=t('Twin'),
	description='A white box.'
)


Room('Science and Technology Demo Center')(
	place=t('Demo'),
	description=observable.Hash({'__MAIN__': 'A spacious, high ceilinged room, with quite a few more stainless steel pipes and mechanical paraphenalia showing through the walls than would normally be tasteful. A large metal booth is built into the east wall, next to a table strewn with technical papers.', 'sliding glass doors closeDesc': 'A pair of sliding glass doors stand shut in the northern wall.'}),
	exits={'south': t('Science and Technology Demo Center(1)'), 'north': t('Demo Center West Wing Lobby')}
)

Container('science and technology demo center table')(
	component=1,
	maximum_occupancy=3,
	place=t('Science and Technology Demo Center'),
	preposition='on',
	player_preposition='sitting on',
	display_name='table',
	description='A long, rectangular table built of polished stainless steel. A few pieces of paper are scattered carelessly across it.'
)

Room('Science and Technology Demo Center(1)')(
	place=t('Demo'),
	exits={'south': t('Science and Technology Vehicle Area(1)'), 'north': t('Science and Technology Demo Center')},
	description='A large, perfectly cubical, empty room. It looks suspiciously unfinished, as though the person or persons responsible for designing the demo center had taken a coffee break before completing it. A small doorway leads north, while a much larger one leads south into a more spacious room. A large black box is set against one wall, and a large glass box stands across from it.',
	display_name='Science and Technology Demo Center'
)

Room('Science and Technology Vehicle Area(1)')(
	place=t('Demo'),
	exits={'south': t('Science and Technology Vehicle Area(2)'), 'west': t('Science and Technology Waste Disposal Area'), 'north': t('Science and Technology Demo Center(1)')},
	description='A large, empty, L-shaped room, with a dirty concrete floor and a high, arched ceiling supported by metal girders. There also appears to be square hole in the ceiling, leading up into darkness. A large open doorway in the north wall leads into a smaller room, while this area continues to the south and west.',
	display_name='Science and Technology Vehicle Area'
)

Room('Science and Technology Vehicle Area(2)')(
	place=t('Demo'),
	exits={'north': t('Science and Technology Vehicle Area(1)')},
	description='A large, empty room, with a dirty concrete floor and a high, arched ceiling supported by metal girders. A complex metal framework is attached to the south wall, almost resembling a giant chair, with a number of strange tubes and connectors. The room continues on to the north, where it seems to turn a corner.',
	display_name='Science and Technology Vehicle Area'
)

Room('Science and Technology Waste Disposal Area')(
	place=t('Demo'),
	description='A large, empty room, with a dirty concrete floor and a high, arched ceiling supported by metal girders. The room continues on to the west, where it seems to turn a corner.',
	exits={'east': t('Science and Technology Vehicle Area(1)')}
)

Room('Science Fiction Room')(
	bookshelf_door=t('bookshelf door'),
	theme='paper',
	exits={'south': t('Bookstore Stairwell, Level 10'), 'north': t('Steam-Powered Library')},
	description='This is a room filled with books about strange worlds, fantastic technology, giant robots, and space travel.  While the books themselves are of the standard text-on-paper variety, the shelves are made of black, gleaming metal, and are mounted on a diabolically complicated system of tracks and sliders. There is also a series of small, tempting buttons mounted at eye level along the shelves. A simple wooden door leads southward back to more mundane surroundings. '
)

Thing('scrap of parchment')(
	place=t('Maxwell'),
	synonyms=['parchment', 'scrap'],
	description='A small scrap of parchment with some words written in an archaic hand on it.  It reads:\012"Always--I tell you this they learned--\012Always at night when they returned\012To the lonely house from far away\012To lamps unlighted and fire gone gray,\012They learned to rattle the lock and key\012To give whatever might chance to be\012Warning and time to be off in flight:\012And preferring the out- to the in-door night,\012They learned to leave the house-door wide\012Until they had lit the lamp inside."\012\012In a messier hand, below, it reads:\012"Leave the keys for other guests.  The lock isn\'t loud enough."'
)

Room('Sea Shore')(
	exits={'east': t('Lonely Expanse of Beach'), 'south': t('Windy Section')},
	description='As you turn the corner you are blinded by a bright blast of sunlight. When you recover your vision you can see that you are standing in the middle of a vast stretch of beach, with pure white sand stretching off in all directions. \012To the east the sand meets a vast, dark-green sea. Immense waves are crashing, spraying you with flecks of foam. The water looks very cold and very powerful.\012The breeze is quite strong here, as is the smell of salt. The sky is a flat slate blue.'
)

Thing('second knob')(
	component=1,
	place=t('qin'),
	synonyms=['knob2', 'knob'],
	description='The second knob from the top of the qin with which to tune the instrument.'
)

Room('Secret Cave')(
	theme='greystone',
	isLit='divunal.common.IsLit',
	OBSOLETE_super=t('Class_Dark Room'),
	exits={'south': t('Deeper In The Rock'), 'up': t('Cube Room'), 'north': t('Very Narrow Rocky Ledge')},
	description="It's too dark in here to see!",
	display_name='A Dark Place'
)

Room('Secret Chamber')(
	theme='greystone',
	description=observable.Hash({'__MAIN__': 'This stone-walled room feels very cool and dank, as if it were once some kind of dugeon chamber. The carpeted floor indicates, however, that it now must have some finer purpose.', 'northern tapestry closeDesc': ''}),
	exits={'south': t("Guyute's Bedroom")}
)

Thing('seventh knob')(
	component=1,
	place=t('qin'),
	synonyms=['knob7', 'knob'],
	description='Seventh knob from the top of the qin with which to tune the instrument.'
)

Room('Shadow Glade')(
	exits={'southwest': t('Silver Shadowed Glade(7)')},
	description='A wide circle of flowers in full bloom surround you.  The air is thick and heavy with their sweet cloying scent, making it hard to breathe.  Shadows dance here and there, weaving in and out among the dark silvery  petals...   Looking more closely you see that they are stained dark with blood.  In a circle around you, seven dark gleaming portals stand shimmering darkly, each beckoning to you.   There is one for each direction except the south.  To the south lies a sheer wall of black void.'
)

Thing('shelves')(
	component=1,
	place=t('Science Fiction Room'),
	synonyms=['middle shelves', 'middle shelf', 'rightmost shelf', 'rightmost shelves', 'leftmost shelf', 'leftmost shelves'],
	description="Large, heavy looking bookshelves made of glossy black metal. They are laden with various works of science fiction, but you don't see anything paticularly of interest to you."
)

twisted.library.clothing.Shirt('shirt with an owl insignia')(
	component=1,
	place=t('James'),
	synonyms=['shirt', 'owl shirt'],
	description='This is a grey T-shirt with the insignia of an owl on it.'
)

Thing('shroom')(
	place=t('Psychadelic Room'),
	theme='weird',
	description='Your vision wavers as you stare at the shroom. It has an aura of blue haze that surrounds it. The more you concentrate on it, the woozier you feel.'
)


Thing('Silver Cube')(
	component=1,
	place=t('Silver Room'),
	synonyms=['cube'],
	OBSOLETE_super=t('Class_Cube'),
	description='A white box.'
)

Room('Silver Room')(
	exits={'west': t('Jewel Bedecked Hallway 2')},
	description="This room is a study in silver.  While you can make out no light source, light must be filtering in through the silvered, translucent ceiling to get down here, where it shines off of the curved surfaces of the room's walls and floor.  There are no markings anywhere, and the only real feature of the room is a cube, which appears to be part of the floor, made of the same silvery substance that composes the rest of the room, but glittering more brightly."
)

Room('Silver Shadowed Clearing')(
	theme='leaf',
	description='This is the side of a mountain, a small clearing in a forest.  You can see a path stretching into the forest to your east and west.',
	exits={'east': t('Silver Shadowed Glade'), 'west': t('Sylvan Sanctuary')}
)

Room('Silver Shadowed Fields')(
	theme='leaf',
	description='Endless fields of flowers and silverbladed grass.  The perfumed scent haning in the air is stronger here, making you feel slighlty dizzy.  ',
	exits={'southwest': t('Silver Shadowed Glade'), 'northwest': t('Silver Shadowed Clearing'), 'north': t('Silver Shadowed Clearing')}
)

Room('Silver Shadowed Flowers')(
	theme='leaf',
	description='Endless fields of flowers and silverbladed grass spread out all around you.  The perfumed scent haning in the air is stronger here, making you feel slighlty dizzy.  ',
	exits={'northeast': t('Silver Shadowed Flowers'), 'southeast': t('Silver Shadowed Flowers'), 'north': t('Silver Shadowed Plain')}
)

Room('Silver Shadowed Glade')(
	theme='leaf',
	description=' A sylvan glade stretches out before you bathed in soft, silver moonlight.  As far as the eye can see, there are soft, silver-bladed grass, and fields of flowers in full bloom.  Dew glistens crystal clear upon the delicate, velvety petals and blades of grass. The air is heavily suffused with scents, sweet and cloying.  ',
	exits={'southwest': t('Silver Shadowed Clearing'), 'south': t('Trans-Dimensional Time Warp'), 'east': t('Silver Shadowed Plain'), 'west': t('Silver Shadowed Flowers'), 'northwest': t('Silver Shadowed Glade'), 'north': t('Silver Shadowed Glade'), 'northeast': t('Silver Shadowed Glade'), 'southeast': t('Silver Shadowed Fields')}
)

Room('Silver Shadowed Glade(7)')(
	theme='leaf',
	description='Tall grass surrounds you tightly, pushing at you, and disorienting you.  Everything you look at has a strange silvery haze over it. ',
	exits={'southwest': t('Silver Shadowed Fields'), 'northwest': t('Silver Shadowed Glade(7)'), 'north': t('Silver Shadowed Glade'), 'southeast': t('Silver Shadowed Plain')}
)

Room('Silver Shadowed Plain')(
	theme='leaf',
	description="The grass is so thick here that you can barely see where you are going.  You can't imagine how the grass has gotten so thick or so tall.",
	exits={'southeast': t('Silver Shadowed Glade(7)'), 'north': t('Silver Shadowed Plain'), 'east': t('Silver Shadowed Glade'), 'west': t('Silver Shadowed Fields')}
)

Room('Silver Shadowed Wood')(
	theme='leaf',
	description='The woods at the edge of the clearing here glow with an erie shade.  The trees whisper among themselves, their bare branches swaying, almost beckoning you towards them.',
	exits={'south': t('Silver Shadowed Glade')}
)

Room('Sitting Room')(
	theme='default',
	description='A Sitting Room looking as if it needs to be described.',
	exits={'east': t('Castle Greysen Fountain Room'), 'west': t('Castle Foyer')}
)

Thing('sixth knob')(
	component=1,
	place=t('qin'),
	synonyms=['knob6', 'knob'],
	description='Sixth knob from the top of the qin with which to tune the instrument.'
)

Thing('skeleton')(
	component=1,
	place=t('Garden Maze(9)'),
	description='Ugh! Though little can be determined by this pile of bones, a sense of dread is eminent. This poor creature must have just given up hope on finding a way out of this maze.'
)

Room('Slanted Mansion Hallway')(
	exits={'northwest': t('Cylindrical Mansion Hallway'), 'down': t('Spiral Landing')},
	description='This narrow hallway is at a 45 degree angle to the corner of the house.  It leads straight into the center of the mansion, where there is a doorway.  You are at the top of a spiral staircase which leads downward.'
)

Thing('sliding glass doors')(
	openDesc='An open, black framed doorway leads south.',
	place=t('Demo Center West Wing Lobby'),
	obstructed='true',
	thereOpenDesc='An open, black framed doorway leads north.',
	openDescription='An open doorway set into the wall.',
	close_message='The doors slide shut.',
	synonyms=['north', 'south', 'door', 'doors', 'glass doors'],
	closeDesc='A pair of sliding glass doors stand shut in the southern wall.',
	component=1,
	OBSOLETE_super=t('Class_Door'),
	description='A pair of sliding glass doors set into the wall.',
	closedDescription='A pair of sliding glass doors set into the wall.',
	thereCloseDesc='A pair of sliding glass doors stand shut in the northern wall.'
)

Room('Small Arched Tunnel')(
	theme='greystone',
	description='This tunnel is carved in the shape of a perfect arch. The walls are solid granite.  It continues north and south.',
	exits={'south': t('Armory'), 'north': t('Doorway Room')}
)

Room('Small Book Room')(
	exits={'down': t('Class Room')},
	description='This is a room full of small books'
)

Room('Small Bookstore Entrance')(
	theme='paper',
	description='You are in the entrance to a small bookstore, which appears to have been out of use for quite some time. Empty shelves line the walls. There is a small counter here with a cash register on it and a sign hanging above it which reads "Borrow and Purchase Here". A rickety metal spiral stairwell leads down to another level of the store. A doorway leads east out onto the street.',
	exits={'east': t('Wrecked Street, bookstore'), 'down': t('Help Desk')}
)

Thing('small brown book')(
	place=t('Obscure Corner of Bookstore'),
	synonyms=['book', 'brown book', 'small book'],
	description='A small, leather-bound book of indeterminate age.  It bears a coat-of-arms crest on its cover, a checkered shield.  It is closed.',
	OBSOLETE_super=t('Class_Linking Book'),
	linkTo=t('Ledge in front of Castle in the Clouds')
)

Thing('small bucket of plaster')(
	place=t("Damien's Bedroom"),
	synonyms=['plaster', 'bucket'],
	description='A small tin can full of plaster of paris. It looks like the same stuff that someone has been using to make the corners of this room smoother.'
)

Thing('small gear')(
	place=t('Mansion Maintenance Closet'),
	synonyms=['gear'],
	description='A thin metal disc, about as big around as the palm of your hand, edged with evenly spaced protrusions.'
)

Room('Small Gray Dome')(
	exits={'down': t('Obscure Corner of Bookstore')},
	description='You are in the center of a small grey dome.  It is perfectly smooth except for the crease where the dome meets the ground, and the perfectly circular hole in the floor.  The hole leading downward appears to have a dark gauze stretched over it.'
)

Room('Small Grey Room')(
	exits={'south': t('Nice Office')},
	description='This is a small grey room with a safe in the corner.  It has no windows, only one door, and no ventilation.  The walls look to be made out of something extremely hard and very thick.'
)

Thing('small heart shaped box')(
	place=t('Other New Jersey Apartment Bedroom'),
	synonyms=['box', 'heart shaped box'],
	description='A small, heart shaped cardboard box, covered in a swirl of reddish colors.'
)

Thing('small mailbox')(
	place=t('West of House'),
	synonyms=['mailbox', 'box'],
	weight='0.9',
	description='A white box.'
)

Room('Small Platform on the Rock')(
	exits={'up': t('Very Narrow Rocky Ledge')},
	description='This is a small platform on the rock.  A ladder is leaned up against the side of the cliff here, which leads up to a higher ledge.  There are some carvings here.'
)

Room('Small Section')(
	theme='paper',
	description="The bookshelves get closer and closer the more you walk in this direction, and the titles get increasingly bizarre. Here sits a book cataloging the World's Great Cataclysms, there lies a novel about fisheries. The floor is very dusty here.\012The passage gets wider to the north, and to the west you can just barely squeeze through between two shelves.",
	exits={'west': t('Tight Squeeze'), 'north': t('Unmarked Corridor')}
)

Room('Smoking Room')(
	theme='wood',
	description='This is a very luxorious room, obiously meant to be a nice place to talk, visit, or even just sit and enjoy a pipe or two. The floor is covered with a vibrant, finely detailed carpet. There are several chairs arranged in a circle, all equally fine. They are all oriented to view the fireplace that graces the east wall. In the center of the circle of chairs is a table with some books and other objects on it. A aging metal staircase leads down into the darkness, and a small passageway leads off to the southeast.',
	exits={'southeast': t("Guyute's Bedroom"), 'down': t("Guyute's Laboratory")}
)

Thing('smoking room fireplace')(
	component=1,
	place=t('Smoking Room'),
	synonyms=['fireplace'],
	description='A rather nondescript smoking room fireplace.'
)

Thing('solid oak door')(
	locked='false',
	thereOpenDesc='To the east, you see a large, marble room with a pedestal in its center, to which is chained a large book.',
	openDesc='To the east, you see a well-lit, polished wood foyer.',
	obstructed='false',
	component=1,
	place=t('Grand History Book Room'),
	synonyms=['door', 'oak door'],
	closeDesc='You see a solid oak door to the east.',
	OBSOLETE_super=t('Class_Door'),
	description='A rather nondescript Solid Oak Door.',
	thereCloseDesc='You see a solid oak door to the east.'
)

Room('South of House')(
	exits={'northeast': t('Behind House'), 'northwest': t('West of House')},
	description='You are facing the south side of a white house. There is no door here, and all the windows are boarded.'
)

Room('Southern End of Small Forest')(
	theme='leaf',
	description='This is the southern end of a small forest, where your way is blocked by a huge rock wall.  Looking upward, you can see the cliff extending up far into the clouds.',
	exits={'north': t('Clearing in Small Forest')}
)

Thing('southern tapestry')(
	component=1,
	place=t("Guyute's Bedroom"),
	synonyms=['tapestry', 'south'],
	description='Though this tapestry is partially obscured, you can see several images of large winged creatures carrying people away. Though it\'s hard to understand precisely what is going on, it seems these "angels" victims are in much pain.'
)

Thing('sparkly book')(
	place=t('Small Book Room'),
	synonyms=['book'],
	OBSOLETE_super=t('Class_Small Book'),
	description='This is a sparkling, shiny book with the words "Collecting Pixies for Fun and Profit" emblazoned on its spine.'
)

Thing('spatula poetry collection')(
	place=t('tupperware lunchbox'),
	page_number=8,
	page_5="\012\011me beacuse when i was little\012\011there was a circus that came to town every summer\012\011the fact that i'm still frightend of clowns \012\011is \012\011odd\012\011though\012\011i'd have to admitt\012\012\012\012\011\011\011-=5=-",
	page_4="\012\011so i took the bus home\012\011to a place that had bare walls\012\011and doors with no knobs\012\011i like being able to look in on people\012\011despite the fact that i'm the only one home\012\011that\012\011doesn't \012\011bother\012\012\012\011\011\011-=4=-",
	page_7='\012\011over me\012\011but whatever it is\012\011i always end up tossing and turning\012\011looking at the clock hoping that\012\011it\012\011would\012\011end\012\012\012\012\011\011\011-=7=-',
	page_6="\011\012\011when ever i go over to your house\012\011and we snuggle up to watch your dads old dirty films\012\011i can't ever get to sleep afterwards\012\011maybe it's the fact that there are no knobs on my doors\012\011or maybe it's because i secertly think\012\011that you prefer the swedish school girls form the films\012\012\012\012\012\011\011\011-=6=-",
	page_1='\012\012\011        \011The Spatula and Other Poems\012\012\011\011\011     by\012\012\011\011           Mistress of Pain',
	page_3="\012\011mutual understanding of individualism\012\011the fact that their goal of\012\011making us one and blurring the edges\012\011so much \012\011you couldn't tell where you ended and i began\012\011made\012\011me\012\011sick\012\012\011\011\011-=3=-",
	page_2=" \011                        The Spatula\012\012\011our journey i'd hoped\011\012\011would have been longer\012\011but the incidences of pronouns and peragotives\012\011was too high\012\011there\012\011was\012\011no\012\012\012\011\011\011-=2=-",
	page_8="\012\011so maybe i could hit the restart button\012\011and begin over with a new player\012\011then maybe i wouldn't have to clean the fridge\012\011or burn so many pictures\012\012\012\012\011\011\011\011\011--End\012\012\012\011\011\011-=8=-",
	synonyms=['poetry', 'book', 'the spatula', 'poetry book'],
	OBSOLETE_super=t('Class_Book'),
	description='The spatula poetry collection is open to page 8. It reads:\012"\012\011so maybe i could hit the restart button\012\011and begin over with a new player\012\011then maybe i wouldn\'t have to clean the fridge\012\011or burn so many pictures\012\012\012\012\011\011\011\011\011--End\012\012\012\011\011\011-=8=-"'
)

Container('sphere chair')(
	maximum_occupancy=1,
	place=t("Blake's Sphere"),
	synonyms=['chair'],
	preposition='on',
	player_preposition='sitting on',
	description='A lovely sphere to sit on.'
)

Thing('spider web')(
	place=t('Cold Room'),
	synonyms=['web'],
	description='A rather nondescript spider web.'
)

Room('Spiral Landing')(
	exits={'up': t('Slanted Mansion Hallway'), 'down': t('Mansion Foyer')},
	description='This is a landing on the spiral staircase, with large windows in the southeastern corner.  Through the windows you can see a pine forest, and a large plateau, which you are slightly above at this height.  In the distance, on top of one of the cliffs you can see a square stone with lightening flickering around it, and black scorchmarks littering the rocky plateau around it.'
)

Thing('sprig of sage')(
	place=t('stone workbench'),
	synonyms=['sage'],
	description='A rather nondescript sprig of sage.'
)

Room('Spring Chamber')(
	exits={'east': t('Cylindrical Mansion Hallway')},
	description='The ground here is a springy bed of grass, which is slightly damp with dew.  The walls are almost the same color of the grass, and the room feels practically alive itself.  On the west wall, there is a huge window looking out over a forest of pine trees during a rainstorm.  The sound of rain falling has a mildly soporific effect, and the ground is soft - you feel like going to sleep.'
)

Thing('stainless steel door')(
	thereOpenDesc='To the north, you see a large, marble room.  A large book is chained to a pedestal in the center of that chamber.',
	openDesc='You see a row of bookshelves through the steel doorway in the south wall.',
	obstructed='true',
	component=1,
	place=t('Grand History Book Room'),
	synonyms=['door', 'steel door'],
	closeDesc='A large archway with a steel door stands to the south.',
	OBSOLETE_super=t('Class_Door'),
	description='This solid, featureless, stainless steel door stands at least half again as high as you within an archway of smooth, white marble accented with dark red veins. ',
	thereCloseDesc='A large steel door blocks the northern exit.'
)

Thing('stairway')(
	component=1,
	place=t('Wrecked Street, curve'),
	synonyms=['stairs'],
	description='This crumbling stairway seems to be all that of this building that has survived.'
)

Thing('staple gun')(
	place=t('Mansion Laboratory'),
	description='A standard staple gun, painted red and wieldable with one hand.  It has the monogram "10" inlaid on its handle in gold.'
)

Thing('steam engine lever')(
	component=1,
	place=t('Mansion Basement Engine Room'),
	synonyms=['lever'],
	description='A brass lever with a red handle set into the side of the steam engine, labled "DANGER: RELEASE VALVE".',
	steam_source=t('Mansion Steam Engine')
)

Thing('steam engine magic switch')(
	component=1,
	place=t('Mansion Basement Engine Room'),
	synonyms=['throw-switch', 'switch', 'steam engine switch'],
	description='A large, y-shaped metal switch with a black handle. It can be switched to either of two positions, labeled "Magic" and "More Magic", respectively.',
	steam_source=t('Mansion Steam Engine')
)

Thing('steam meter')(
	place=t('dark green overcoat'),
	synonyms=['meter'],
	description='divunal.tenth.SteamMeter',
	steam_source=t('Mansion Steam Engine')
)

Room('Steam-Powered Library')(
	theme='wood',
	description=observable.Hash({'__MAIN__': 'A small, cozy room, lined with bookshelves and softly lit by a brass chandelier hanging from the ceiling. An ornately carved sofa with dark green upholstery is set opposite a small reading table, and an Oriental rug of roughly the same color is spread out across the polished wooden floor. An archway leads north into a larger room, while the door to the south is a large metal contraption, held in place between two bookcases by a complicated system of pistons and hydraulics. On the left side of the door, there is a lever.', 'bookshelf door': 'The southern door is closed.'}),
	exits={'south': t('Science Fiction Room'), 'north': t('Mansion Study')}
)

Thing('sticky note')(
	place=t("Damien's Cubicle"),
	synonyms=['sticky', 'note'],
	description='Login: djones\012Password: "nemesis"'
)

Chair('stone prayer bench')(
	component=1,
	maximum_occupancy=5,
	place=t('Ivy Garden'),
	synonyms=['bench'],
	description='Though carved out of stone, this bench seems surprisingly smooth and comfortable to sit on.'
)

Container('stone workbench')(
	component=1,
	place=t("Guyute's Laboratory"),
	synonyms=['workbench'],
	preposition='on',
	OBSOLETE_super=t('Class_Container'),
	description="This workbench looks like it's been through the Great War. Even in the hard granite that composes its top surface there are deep gouges. The surface of the workbench is covered with clutter and refuse of every kind."
)

Thing('stones')(
	component=1,
	place=t('Inner Garden'),
	description='These small stones form the pathways that go through the garden. You should only walk on these, not the finely cared-for grass.'
)

Thing('strange device')(
	place=t('Aaron'),
	synonyms=['device'],
	OBSOLETE_super=t('Reality Pencil'),
	description='It appears to be a generic reality altering device, but aside from being vaguely pencil-shaped, it is vague and indistinct.'
)

Thing('strength dial')(
	component=1,
	place=t('Genetic Laboratory'),
	synonyms=['strength', 'dial'],
	value='-0.15',
	OBSOLETE_super=t('Class_Player Creation Dial'),
	description='A white box.'
)

Thing('stuffed Tux the Penguin')(
	place=t('dark green overcoat'),
	synonyms=['penguin', 'tux', 'tux the penguin'],
	description='A soft, stuffed figurine of a flightless bird with black and white plumage, proudly wearing a "Linux Power" pin on it\'s chest.'
)

Room('Summer Chamber')(
	exits={'south': t('Cylindrical Mansion Hallway')},
	description='This room is warm, with the scent of flowers in the air.  A bed is aligned with the west wall, a half circle, in a sort of crude line-drawing of the sun.  The ground is a soft bed of flower petals, and the walls are a muted white.  On the north wall is a large panel window overlooking a pine forest in full bloom.  '
)

Room('Supply Closet')(
	exits={'northwest': t('Even More Office Hallway')},
	description='This is an empty closet, filled with many shelves.  There is a fuse box here, long fused shut.  The only exit is a door to the northwest.'
)

Thing('Swank Pencil')(
	place=t('Jedin'),
	synonyms=['pencil'],
	OBSOLETE_super=t('Reality Pencil'),
	description='A white box.'
)

Thing('sword +1')(
	frotzed='true',
	place=t('James'),
	synonyms=['sword'],
	isLit='true',
	description=observable.Hash({'__MAIN__': 'This is a sword of slightly above-average quality.  You notice that the craftsmanship, while not excellent, is good enough to be impressive.  It appears to have been carefully honed to do just a little bit more damage than another, similar, but less above-average sword would do.  Its blade has a flat, pseudo-silvery texture, and the hilt is made of what appears to be a low-grade stainless steel.', 'lighting': ['A pure white glow eminates from ', m('sword +1','noun_phrase'), ', bathing ', m('sword +1','him_her'), ' in light.']})
)

Room('Sylvan Sanctuary')(
	theme='leaf',
	description='A peaceful, tranquil, and silent glade in a silver forest at night.  You can make out a rock wall with a door in it to the south, which is painted to look as though it is a part of the night sky, and to the north, you can enter the forest.',
	exits={'north': t('Silver Shadowed Wood')}
)

Thing('take-out carton')(
	place=t('Proper English Library'),
	synonyms=['carton', 'chinese food', 'food'],
	description='Aside from a few grains of pork fried rice and a splash of grease, this carton is completely empty.'
)

Thing('tapestry')(
	component=1,
	place=t('Hallway'),
	description='This hanging covers the western wall. It has a beautiful pattern in the shape of a stylized serpent winding around itself in ever-tightening circles. It is very heavy, and hangs flush against the wall.'
)

Thing('tattered book')(
	place=t('Musty Section'),
	synonyms=['book'],
	description='The cover reads "Mad Science"',
	linkTo=t('Cold Room')
)

Thing('Tax Guide')(
	place=t("Damien's Cubicle"),
	synonyms=['guide', 'tax'],
	description='Pro-Dis Form 6900A -- the Easy Way\012\012If you are a wage-gaining corporation, and you may have high-end yield bonus in the 1 to 2 million ranges, then things are going to change for you! As of March, the government has released Form 6900A, which is mandatory under certain conditions...\012\012It continues on in this fashion for some time.'
)

Thing('tea bowl')(
	place=t('Tea House'),
	synonyms=['teabowl', 'bowl'],
	description='A rather nondescript tea bowl.'
)

Room('Tea House')(
	theme='paper',
	description='Wabi is the avoidance of anything showy or sensuous. It is the pursuit of simplicity and abstraction. It is the discovery of the true beauty that things possess when stripped of superficial characteristics and reduced to their essence. Even the tea-ceremony room itself is shorn of all superfluity, and a limitless universe is created in an unadorned room with an area of a mere 5 meters. In a small alcove to the north, there is a scroll hanging on the wall.',
	exits={'south': t('Inner Garden')}
)

Thing('tea house helper')(
	component=1,
	place=t('Inner Garden'),
	synonyms=['house'],
	description='A delightful little tea house. The walls are made of very thin paper, yet the house looks as if it might be difficult to enter.',
	display_name='tea house'
)

Container('teakwood podium')(
	component=1,
	place=t('Underground Grotto'),
	synonyms=['podium'],
	preposition='on',
	description="An elegant teakwood podium. There's a small sign here."
)

Room('Temple Bottom Floor')(
	theme='default',
	exits={'up': t('Temple Middle Floor'), 'north': t('Temple Northern Hallway')},
	description='This room is a very large octagonal room, whose ceiling is supported at intervals by pilliars.  At the center of the room, a wide, octagonal, metal staircase is framed by eight such pilliars, at the points of the octagon.  Arches are placed at equal intervals in the centers of the outer walls, each leading into its own hallway.  Each arch is decorated in a unique manner.',
	display_name='Bottom Floor'
)

Room('Temple Entrance Room')(
	theme='default',
	exits={'south': t('Temple Northern Hallway'), 'north': t("Tower's Base")},
	description="This is a large, light stone room.  A statue of a tall, strong looking man adorns the northwestern corner of the room, facing diagonally inward, as if to monitor those who enter from the north without being seen itself.  Another, smaller archway leads south, into the center of the tower's base.",
	display_name='Entrance Room'
)

Room('Temple Middle Floor')(
	theme='default',
	exits={'south': t('Temple Middle Hallway South'), 'up': t('Temple Triangle Room'), 'north': t('Temple Middle Hallway North'), 'east': t('Temple Middle Hallway East'), 'west': t('Temple Middle Hallway West'), 'down': t('Temple Bottom Floor')},
	description='This is a large cylindrical chamber supported at eight points by pilliars.  In the center of the room, a wide octagonal octagonal stairway leads both up and down.  Wooden doorframes adorn the four cardinal directions of the room, leading off into hallways.  The floor is made of a light stone here, except for four black, glossy squares in front of each doorway.',
	display_name='Middle Floor'
)

Room('Temple Middle Hallway East')(
	theme='default',
	description='A Temple Middle Hallway East looking as if it needs to be described.',
	exits={'west': t('Temple Middle Floor')}
)

Room('Temple Middle Hallway North')(
	theme='default',
	description='A Temple Middle Hallway North looking as if it needs to be described.',
	exits={'south': t('Temple Middle Floor')}
)

Room('Temple Middle Hallway South')(
	theme='default',
	description='A Temple Middle Hallway South looking as if it needs to be described.',
	exits={'north': t('Temple Middle Floor')}
)

Room('Temple Middle Hallway West')(
	theme='default',
	description='A Temple Middle Hallway West looking as if it needs to be described.',
	exits={'east': t('Temple Middle Floor')}
)

Room('Temple Northern Hallway')(
	theme='default',
	exits={'south': t('Temple Bottom Floor'), 'north': t('Temple Entrance Room')},
	description='This is a well-lit hallway with an arched ceiling. Illumination comes from an unknown source behind the walls and reflects downward off of the light stone ceiling. Two doors to your left and right are boarded over, and the hallway opens up to the north and south.',
	display_name='Northern Hallway'
)

Room('Temple Triangle Room')(
	theme='default',
	exits={'down': t('Temple Middle Floor')},
	description="This room is spacious, but low ceilinged.  It is cylindrical, but the main focus of the room's geometry seems to be a triangle.  Three statues, each slightly larger than life, are placed near the edges of the room, facing inward.  The statues are all composed of a gleaming, smooth white material.  There is a tall statue of a man holding a hemisphere, a short statue of a man holding a book, and a strong statue of a man holding a bone.",
	display_name='Triangle Room'
)

twisted.author.Author('Tenth')(
	foo='(null)',
	health='1.0',
	theme='default',
	stamina='-0.8790683',
	health_time=942018677035L,
	mindspeak='0.1',
	endurance='-0.5',
	oldlocation=t('Science and Technology Vehicle Area(2)'),
	stamina_time=942018677034L,
	teleport_destination=t('Demo Center Lavatory'),
	gender='m',
	pageable='true',
	glance='0.2',
	psyche='1.0',
	painting_looks=-3,
	visit_color='greenish',
	OBSOLETE_super=t('Class_Human'),
	description=observable.Hash({'__MAIN__': 'A tall, slender young man, with bright green eyes and a calm, thoughtful face. His hair is an odd, coppery shade of blonde, and falls nearly to his waist in gentle waves.', 'clothing': [m('Tenth','him_her'), ' is wearing ', 'a pair of green-tinted spectacles', ', ', 'a neatly tied white silk cravat', ', ', 'a white silk shirt', ', ', 'a dark green overcoat', ', ', 'black slacks', ', ', 'and ', 'knee high black leather boots', '.']}),
	dexterity='0.2'
)

Room("Tenth's Chamber")(
	theme='wood',
	description=observable.Hash({'__MAIN__': 'A spacious bedroom, lit by a pair of identical brass lanterns on the north and south walls. A large four poster bed stands against the west wall, surrounded by hanging curtains. A dark wooden writing desk sits under the lantern against the south wall, and a wooden bureau stands across from it, set with a large mirror.', 'tenths folding balcony doors openDesc': 'A light breeze wafts in from the north, where a pair of folding double doors lead out onto a balcony.', 'tenths bedroom doors openDesc': 'To the east, a long hallway is visible through a pair of open doors.'}),
	exits={'east': t('Mansion Upper Hallway'), 'north': t('Mansion Balcony')}
)

Thing('tenths bedroom doors')(
	thereOpenDesc='To the east, a long hallway is visible through a pair of open doors.',
	openDesc='A pair of double doors stand open at the west end of the hallway.',
	obstructed='false',
	component=1,
	place=t('Mansion Upper Hallway'),
	synonyms=['east door', 'doors', 'west doors', 'west door', 'east doors'],
	closeDesc='To the west, the hallway ends in a large set of double doors.',
	display_name='double doors',
	OBSOLETE_super=t('Class_Door'),
	description='A pair of large, dark brown wooden doors, each set with a polished brass handle.',
	thereCloseDesc='A large set of double doors is set into the east wall.'
)

Thing('tenths folding balcony doors')(
	openDesc='A light breeze wafts in from the north, where a pair of folding double doors lead out onto a balcony.',
	obstructed='false',
	component=1,
	place=t("Tenth's Chamber"),
	synonyms=['doors', 'folding doors', 'north door', 'north doors', 'south door', 'south doors', 'south', 'door'],
	closeDesc='To the north, a pair of folding doors are set into the wall.',
	display_name='folding balcony doors',
	OBSOLETE_super=t('Class_Door'),
	description='A set of folding double doors made of dark, polished wood, set with simple wooden handles.'
)

Room('Test Bed')(
	theme='water',
	description='This is a big comfy mattress where you can test stuff. There is also a large, comfortable sofa here.',
	exits={'north': t('Class Room')}
)

Room('The Beginning')(
	exits={'down': t('Obscure Corner of Bookstore')},
	description='Hello, and welcome to the first universe constructed with Reality Pencil v0.99. We try hard to keep the universe in good working order here, so: if anything seems out of place to you, please make a note of it to a Human or send some email to reality@tinaa.com.'
)

Room('The Doorway of the Obsidian Tower')(
	exits={'south': t('Lonely Expanse of Beach')},
	description="This edifice stretches into the sky; to try and see its top would surely strain one's spine.  Regular sets of rectangular protrusions and indentations tile the faces of the tower--in fact, it looks not so much that the glistening rock has been carved, but that someone molded it around a building, blocking it off from the outside world.  Sickly, thorny vines fight for purchase in the sparse cracks encroaching on the building's base, though their flowers' white, bell-shaped bulbs grow thick and plentiful.  You glimpse a hand-shaped indentation to the right of the black stone door, the small slit above it almost obscured by delicate petals."
)

Room('The Twisty Bit')(
	theme='paper',
	description='The library becomes more narrow here;  the bookshelves are getting closer together, pressing in on both sides. It also seems to be twisting around, almost doubling back on itself.',
	exits={'northeast': t('Myth Section'), 'north': t('Musty Section')}
)

Chair('thin bamboo mat')(
	component=1,
	place=t('Tea House'),
	synonyms=['thin mat', 'bamboo mat', 'mat'],
	description='A rather nondescript thin bamboo mat.'
)

Thing('third knob')(
	component=1,
	place=t('qin'),
	synonyms=['knob3', 'knob'],
	description='Third knob from the top of the qin with which to tune the instrument.'
)

Thing('tied stone')(
	place=t('Rikyu'),
	synonyms=['stone'],
	description='This small stone has a rope tied around it.',
	display_name='small stone'
)

Room('Tight Squeeze')(
	theme='paper',
	description='You can just barely fit into this section. Fortunately it seems to get a little wider to the south and to the east. \012There is so much dust on the floor here that you can barely even see the stones under your feet.',
	exits={'east': t('Small Section'), 'south': t('Wider Area')}
)

Thing('timer stop button')(
	place=t('Mystic Field'),
	synonyms=['button', 'blue button'],
	description="This button is mounted on a sort of platform. It's fairly ordinary, or at least, as ordinary as any other button placed in the middle of nowhere.",
	display_name='large blue button'
)

Thing('TME Greenhouse Plants')(
	component=1,
	place=t('Greenhouse Entrance'),
	synonyms=['plants', 'greenhouse plants'],
	description='Upon closer examination, the plants, although strewn about the room with no sense of organization, are all exactly the same.  They have fairly geometric leaves and stems, as well as all being rooted in mounds of dirt which look strangely glossy and pot-shaped.'
)

Thing('Tome of History')(
	place=t('Grand History Book Room'),
	theme='paper',
	page_number=1,
	page_5='\012\012\012\012\011One day, the people looked up.',
	page_4='Once, there was a city.  The city was a small and quiet place, where many eccentric but amiable people dwelt.  This city was a part of a country, which in turn was part of a planet.  That planet was surrounded by a ring -- an irridescent ring which was visible from everywhere in the city, high in the center of the sky.  The ring was made of a beautiful blue stone which cast its light as an arced, brilliant blue streak down the center of the night sky.  It was said that this ring was one of the most beautiful sights in all of the world.  Although the world was not one of travellers, many made a pilgrimage at least once in their lives to this city, to see the Light of the Line (as it was called, looking like a line in the sky) and thank the sky for the inspiring painting which it had hung upon itself.',
	page_7='There was much chaos.  The stones in the sky came hailing down upon the residents of the city.  Those who had known of the impending disaster had prepared a dwelling place below the streets -- but that place was more slavery than salvation.\012\012',
	page_6='\012\012\012\012\011The next,\012\011\011the sky fell down.',
	page_1='INTRODUCTION\012An unimagineably long time ago, before the Great Fall, things were much different than they are now. The title of "scribe" inspired no awe, books were merely paper and ink, and all life was mundane.\012To remind us what these books were like, we still have the Second Aisle, which, though it does not grow, is an important part of the history of our world. Take a book from that place sometime - you will notice that they are not attached to the shelves. Open it, and note that the pages are dry and brittle (this is because it is dead) and the words stay the same even after you read them.',
	page_3='\012\012\012\011Chapter One\012\012\011\011Times Before Now',
	page_2='This very book, in fact, is that same sort of book with very few of our modern enhancements. It will not dry up and rot like those in Aisle 2, but it will also never change or grow. It is meant to preserve the past faithfully - and so we call such books, with double meaning, History Books. Each of the books in the First Aisle is such a book. You can rest assured that they will never change, to faithfully preserve the past. ',
	synonyms=['tome', 'book'],
	component=1,
	OBSOLETE_super=t('Class_Book'),
	description='The Tome of History is open to page 1. It reads:\012"INTRODUCTION\012An unimagineably long time ago, before the Great Fall, things were much different than they are now. The title of "scribe" inspired no awe, books were merely paper and ink, and all life was mundane.\012To remind us what these books were like, we still have the Second Aisle, which, though it does not grow, is an important part of the history of our world. Take a book from that place sometime - you will notice that they are not attached to the shelves. Open it, and note that the pages are dry and brittle (this is because it is dead) and the words stay the same even after you scrutinize them."'
)

Thing('torch')(
	true='false',
	place=t('James'),
	isLit='true',
	description='A white box.'
)

Room("Tower's Base")(
	theme='crack',
	exits={'south': t('Temple Entrance Room'), 'north': t('Wrecked Avenue')},
	description='This avenue goes between rows of buildings that have been completely reduced to rubble.  The road has fared better than the buildings though, it appears to be in fairly good condition, as does the tall tower standing to the south.  An open archway leads into the tower.',
	display_name='Wrecked Street'
)

Room('Trans-Dimensional Time Warp')(
	theme='weird',
	description='You are in a void.  This room is thermodynamically impossible - and yet it exists.   I wonder why?  You cannot see any direction clearly, but nothing blocks your path.',
	exits={'southwest': t('Trans-Dimensional Time Warp'), 'south': t('Silver Shadowed Flowers'), 'up': t('Trans-Dimensional Time Warp'), 'east': t('Trans-Dimensional Time Warp'), 'west': t('Trans-Dimensional Time Warp'), 'northwest': t('Silver Shadowed Glade'), 'north': t('Trans-Dimensional Time Warp'), 'northeast': t('Trans-Dimensional Time Warp'), 'southeast': t('Trans-Dimensional Time Warp'), 'down': t('Trans-Dimensional Time Warp')}
)

twisted.author.Author('Tsiale')(
	painting_looks=4,
	oldlocation=t('Mansion Four Poster Bed'),
	description=observable.Hash({'__MAIN__': '', 'clothing': [m('Tsiale','him_her'), ' is wearing ', m('green silk shirt','noun_phrase'), ', ', 'black leggings', ', ', 'and ', m('pair of black leather shoes','noun_phrase'), '.']}),
	OBSOLETE_super=t('Class_Human'),
	gender='f'
)

Room("Tsiale's House")(
	theme='crack',
	exits={'west': t('Wrecked Street, bookstore')},
	description='This is the entrance hall of a small wrecked house.  You can see that there is an upper floor and a few other rooms, but the staircase is collapsed, and the other rooms (and most of this one) are all caved in.  There is a wooden doorframe to the west.',
	display_name='Small Wrecked House'
)

Thing('tsukubai')(
	component=1,
	place=t('Inner Garden'),
	synonyms=['basin'],
	description='This stone basin, or tsukubai, is continuously filled by some hidden pump. The water is clear and cold, suitable for drinking, though the designs indicate some holier purpose as well.',
	display_name='stone basin'
)

Thing('tunnelX1')(
	component=1,
	wateryExit='true',
	place=t('Underground Grotto'),
	OBSOLETE_super=t('Class_Forbidden Exit'),
	description='A rather nondescript tunnel opening helper.'
)

Thing('tunnelX2')(
	component=1,
	wateryExit='true',
	place=t('Dark River Tunnel'),
	OBSOLETE_super=t('Class_Forbidden Exit'),
	description='A rather nondescript tunnelX2.'
)

Thing('tunnelX3')(
	component=1,
	place=t('Dark River Tunnel'),
	OBSOLETE_super=t('tunnelX2'),
	description='A rather nondescript tunnelX3.'
)

Thing('tunnelX4')(
	component=1,
	place=t('Dark River Tunnel(1)'),
	OBSOLETE_super=t('tunnelX2'),
	description='A rather nondescript tunnelX4.'
)

twisted.library.clothing.Hat('tupperware lunchbox')(
	component=1,
	place=t('Chenai'),
	synonyms=['tupperware', 'lunch box', 'lunchbox', 'box'],
	description='A blue tupperware lunchbox with a cartoon Tux on the front.'
)

twisted.author.Author('Twin')(
	oldlocation=t('Mansion West Ballroom'),
	description="Although Twin's figure looks human, his presense feels somewhat supernatural. Only two things stand out about this otherwise shady character: a set of glowing eyes in the hood of his black cloak, and the sparkling silver rings ornamenting his fingers...",
	OBSOLETE_super=t('Class_Human'),
	gender='m'
)

Room('Twisted Reality Corporate Demo Center')(
	place=t('Demo'),
	description='A spacious, open room with a high, arched ceiling. The walls are an almost gleaming, immaculate white, contrasting sharply with the polished black marble floor. The room becomes wider as it continues on to the north, and is dotted with bright green potted plants at regular intervals.  The southern wall is covered by a ten-foot-tall billboard labeled with the legend: "\'look at board\' for help!\'"',
	exits={'north': t('Demo Information Center')}
)

Room('Twisty Cloud Path')(
	exits={'southeast': t('Path in the Clouds'), 'west': t('Flat Ledge')},
	description='You are walking on a twisty path made of smooth rock, floating upon a sea of clouds.  There is a twist in it here as it curves gracefully around.'
)

Room('Under the Bookshelf')(
	theme='paper',
	description='There is more room under this bookshelf than you thought. In fact, then floor slopes quickly downward quickly here; a few paces down and you could probably stand up.',
	exits={'east': t('Quiet Niche'), 'down': t('Natural Alcove')}
)

Room('Underground Grotto')(
	theme='water',
	exits={'west': t('Dark River Tunnel'), 'up': t('Inside Oak Tree')},
	description="There is a great underground river here, which comes in over a waterfall at the east end of the cave. Despite the turbulent waterfall, the rest of the river's mirrorlike surface is incredibly serene. These caverns have been carved by nature through the centuries, resulting in the beautiful scene you see before you. There is a ladder leading up here, and to the west, the river continues to flow into a tunnel. It looks to be passable by boat. Near you, on the bank, is a elegant teakwood podium, upon which is a bell and a small white sign.",
	display_name='Riverbank in Underground Grotto'
)

Room('Uneven Floor')(
	inhibit_exits='true',
	theme='greystone',
	inhibit_items='true',
	display_name='A Dark Place',
	OBSOLETE_super=t('Class_Dark Room'),
	exits={'northeast': t('Cold Floor')},
	description="It's too dark in here to see!"
)

Room('Unmarked Corridor')(
	theme='paper',
	description='As you wander down this twisty section of the store, you try in vain to guess what topic unites the books here. Choosing books at random you notice some on astrology, some on tidal cycles, and quite a few that are too ancient to make out the titles of. Not a few are printed in languages that you do not understand. This section continues to the south, although it becomes very narrow in that direction.',
	exits={'east': t('Myth Section'), 'south': t('Small Section')}
)

Thing('upper ladder')(
	component=1,
	place=t('Very Narrow Rocky Ledge'),
	synonyms=['ladder'],
	description='This is the upper half of a wooden ladder which leads downward to a lower and wider ledge.'
)

Room('Upper Mansion Stairwell')(
	theme='wood',
	description='A tall, cylindrical room, with a wrought iron spiral staircase descending down through the center of the floor. The domed ceiling is built from triangular panes of tinted glass set in a metal frame, and the sunlight filtering through it provides a gentle illumination to the room.',
	exits={'down': t('Mansion Stairwell')}
)

Thing('Vehicle Area ceiling hatch')(
	component=1,
	place=t('Science and Technology Vehicle Area(1)'),
	synonyms=['hatch', 'square hole', 'hole'],
	description='An ominous square hole in the ceiling. While it seems to be lined with metal sheeting, it leads up into an inky darkness, and there is no other indication of what it does or where it goes.',
	display_name='hole in the ceiling'
)

Room('Very Cold Room')(
	exits={'west': t('Closed Junction')},
	description='This room is very, very cold.  The metallic walls, floor and ceiling gleam harshly, and ice covers all the surfaces.  A mist covers the floor.  A metallic tube leads westward to somewhat warmer climes.'
)

Room('Very Narrow Rocky Ledge')(
	exits={'east': t('Rocky Ledge, further west'), 'south': t('Secret Cave'), 'down': t('Small Platform on the Rock')},
	description='This ledge overlooks the very edge of death itself.  You can almost feel the rock giving way under your feet as you look downwards into the seemingly bottomless clouds that do not even begin until hundreds of feet away.  A ladder leans over the edge here, and you think you could climb down to a lower ledge.'
)

Room('very small round room')(
	exits={'south': t('Doorway Room')},
	description="This room is a circular grey room. It is utterly plain except for the door to the south, and the word 'null' crudely chiseled in the front wall."
)

Thing('vial of moonshine')(
	place=t('nightstand'),
	synonyms=['vial'],
	description="What's the use of only a vial's worth?"
)

Thing('wall')(
	component=1,
	place=t("Damien's Cubicle"),
	synonyms=['walls'],
	description='Grey. Or perhaps blue? Greyish-blue, maybe. Hard plastic cubicle dividers... possibly made of cloth and not plastic.'
)

Thing('Weirwood Cube')(
	place=t('Maxwell'),
	teleport_phrase_Ohm=t('Underground Grotto'),
	teleport_phrase_Hello_Sailor=t('West of House'),
	teleport_phrase_Away_away=t('Ledge in front of Castle in the Clouds'),
	teleport_phrase_Theres_no_place_like_home=t('Ruby Room'),
	teleport_phrase_Go_Elsewhere=t('Class Room'),
	teleport_phrase_Obscurity=t('Obscure Corner of Bookstore'),
	synonyms=['cube'],
	teleport_phrase_genome=t('Genetic Laboratory'),
	OBSOLETE_super=t('Class_Cube'),
	description='This is a small cube made out of a deep red wood, polished until it gleams. Its corners are rounded.  In places it appears slightly translucent, and you can see pulsating points of light, like stars, under its surface.',
	teleport_phrase_magritte=t('Portrait in the Sky'),
	teleport_phrase_Gyre_and_gimble_in_the_wabe=t('Observation Hallway'),
	teleport_phrase_go_go_gadget_archetype=t('Tenth'),
	teleport_message='The Weirwood Cube vibrates visibly, as if something had struck a harmonic with it.'
)

Room('West End')(
	theme='greystone',
	description='This is the westmost point on the castle.  The room seems useless except to indicate that the place ends here.  To the west, there are a set of french doors, long since shattered, leading onto a terrace.  Eastward there is a large archway.',
	exits={'east': t('Great Dome'), 'west': t('Cloud Scene Balcony')}
)

Room('West of House')(
	exits={'northeast': t('North of House'), 'west': t('Forest'), 'southeast': t('South of House')},
	description='You are standing in an open field west of a white house, with a boarded front door.'
)

Room('Western End of Grotto')(
	theme='water',
	description='An Eastern Grotto End looking as if it needs to be described.',
	exits={'east': t('Dark River Tunnel'), 'north': t('Cold Room')}
)

Thing('western tapestry')(
	component=1,
	place=t("Guyute's Bedroom"),
	synonyms=['tapestry', 'west'],
	description="This tapestry is mostly covered by the bed, but an image of a large machine is peeking out. One can't be sure the purpose of this machine, but from the gears and pistons placed all around it, it can't be good."
)

Room('Wet Floor')(
	inhibit_exits='true',
	theme='greystone',
	inhibit_items='true',
	display_name='A Dark Place',
	OBSOLETE_super=t('Class_Dark Room'),
	exits={'east': t('Cold Floor')},
	description="It's too dark in here to see!"
)

twisted.library.clothing.Shirt('white button-down shirt')(
	place=t('Jedin'),
	synonyms=['white shirt', 'shirt'],
	clothing_appearance='a white, button-down shirt and collar of a soft, durable fabric with the sleeves rolled up to just below his elbows',
	description="An evenly-spaced row of small, white buttons fashioned from a semi-precious stone run down the front of this garment; two are placed higher for fastening the collar as well.   The buttons' matte finish blends smoothly with the soft, strong fabric.  You see no wrinkles on the shirt."
)

Container('white guymelf')(
	place=t('Mansion Laboratory'),
	synonyms=['guymelf', 'armor', 'suit'],
	description="A massive suit of white armor, easily four times the height of a man. It is formed from smooth, oddly shaped sections of silvery white metal, and bears a dark red cloak from it's shoulders. A large green gem is set into either shoulder, and a single reddish stone is embedded in the left side of the chest."
)

twisted.library.clothing.Tie('white silk cravat')(
	component=1,
	untied_descriptor='It is untied, so as to be simply hung over the neck.',
	place=t('Tenth'),
	tied_appearance='a neatly tied white silk cravat',
	synonyms=['silk cravat', 'cravat', 'scarf'],
	clothing_appearance='a neatly tied white silk cravat',
	tied_descriptor='It is worn around the neck like a scarf, but tied in front, with the remainder of the embroidered silk hanging somewhat like a tie. ',
	description=observable.Hash({'__MAIN__': 'A long, thin piece of white silk, like a very light scarf.', 'tie descriptor': 'It is worn around the neck like a scarf, but tied in front, with the remainder of the embroidered silk hanging somewhat like a tie. '}),
	untied_appearance='a white silk scarf'
)

twisted.library.clothing.Shirt('white silk shirt')(
	component=1,
	place=t('Tenth'),
	synonyms=['white shirt', 'silk shirt', 'shirt'],
	clothing_appearance='a white silk shirt',
	description='a loose fitting white silk shirt, gathered into cuffs at the wrist and fitted with a white cravat at the collar.'
)

twisted.library.clothing.Belt('wide sash')(
	place=t('Yumeika'),
	synonyms=['sash'],
	clothing_appearance='a wide sash around her waist',
	description='A wide sash.'
)

Room('Wider Area')(
	theme='paper',
	description='This area is still a mere two or three arm-spans wide, but it seems huge compared to the claustrophobic closeness of the passage to the north.\012The dust which completely covers the floor here is very grainy. It looks more like sand than dust, and it is everywhere. There is a very slight glow from the eastern end of this section, and to the southeast two bookshelves form a quiet niche.',
	exits={'east': t('Windy Section'), 'southeast': t('Quiet Niche'), 'north': t('Tight Squeeze')}
)

Room('Windy Section')(
	exits={'west': t('Wider Area'), 'north': t('Sea Shore')},
	description='The dust-- or sand -- is so deep here that the floor is completely gone. There is a fairly strong breeze blowing northward, and it carries a faint salty tang with it. To the west the passage continues, but it seems darker in that direction.'
)

Container('wood-burning stove')(
	place=t("Guyute's Bedroom"),
	synonyms=['stove', 'wood stove'],
	OBSOLETE_super=t('Class_Container'),
	description='A cast-iron wood stove.'
)

Room('Woodem Platform in Oak Tree')(
	theme='leaf',
	description="From here you can see the ivy and tea gardens. Careful you don't fall!",
	exits={'down': t('Ivy Garden')}
)

Thing('Wooden Pencil')(
	place=t('Tsiale'),
	synonyms=['pencil'],
	OBSOLETE_super=t('Reality Pencil'),
	description='A delicate faery wand.'
)

Thing('wooden ring')(
	component=1,
	place=t('Mansion Upper Hall'),
	synonyms=['piece of string', 'string', 'rin', 'small wooden ring', 'ring'],
	description='A small polished wooden ring, hanging from a ceiling panel by a white piece of string.'
)

Thing('wooden table')(
	component=1,
	place=t('Proper English Library'),
	synonyms=['table', 'wooden'],
	OBSOLETE_super=t('Class_Container'),
	description="The first thing you notice is  the oppulence of this table -- it is constructed of solid oak and polished to a high degree. It's the sort of table that makes you want to sit down (in one of the plush leather arm chairs) and read a scholarly tome. Nevertheless, someone has managed to turn this comfortable work space into a surprisingly anal computer desk. The table top is covered in manuals and books on tax law, drawing an ironic contrast to the ancient texts on every wall."
)

Thing('worn grey leather book')(
	place=t('Maxwell'),
	synonyms=['grey leather book', 'leather book', 'grey book', 'book'],
	isLit='false',
	spells=['frotz','zorft'],
	OBSOLETE_super=t('Class_Spell Book'),
	description='A worn, palm-sized leather book that is in good condition despite the destroyed appearance of its cover.  Some words used to be etched into the cover, but they are long since illegible.'
)

Thing('wrapper')(
	place=t('Proper English Library'),
	description='Thank you for choosing nice Chinese Restaurant. To use chopstick:\012\0121) Grasp frimly in fingers\012\0122) Move back and forthly with hands.\012\0123) Now you can pick up anything!'
)

Room('Wrecked Alleyway')(
	theme='crack',
	description='This is the end of an alley.  You can enter a building to the southeast, where a wooden doorframe leads into a building, or you can continue north out to the street.',
	exits={'southeast': t('Empty Bakery'), 'north': t('Wrecked Street, postwall')}
)

Room('Wrecked Avenue')(
	theme='crack',
	exits={'south': t("Tower's Base"), 'north': t('Wrecked Street')},
	description='This avenue goes between rows of buildings that have been completely reduced to rubble.  The road has fared better than the buildings though, it appears to be in fairly good condition. The avenue continues north to an intersection, and south to the base of what appears to be a very tall tower.',
	display_name='Wrecked Street'
)

Room('Wrecked House Foundation')(
	theme='crack',
	description='This was probably once the foundation of a house, but the house has long since been destroyed.  Sharp rubble surrounds the foundation, but there are the remnants of a road to the west.',
	exits={'west': t('Wrecked Street, south')}
)

Room('Wrecked Street')(
	theme='crack',
	description='This is an intersection, which looks as if thousands of small rocks had bombarded it at high velocity, leaving pockmarks.  To the north and west, the pockmarks become larger, and the road is unwalkable within 30 or 40 steps.  To the southwest, the road is damaged but still useful.  Southward, however, the road is curiously undamaged, although buildings lie in rubble to both sides of it.',
	exits={'south': t('Wrecked Avenue'), 'southeast': t('Wrecked Street, postwall')}
)

Room('Wrecked Street, bookstore')(
	theme='crack',
	exits={'south': t('Wrecked Street, south'), 'north': t('Wrecked Street, north'), 'east': t("Tsiale's House"), 'west': t('Small Bookstore Entrance')},
	description='A wrecked paved street.  It continues to the north and south, and to the west you see the familiar sight of the Bookstore.',
	display_name='Wrecked Street'
)

Room('Wrecked Street, corner')(
	theme='crack',
	exits={'south': t('Wrecked Street, north'), 'northwest': t('Wrecked Street, curve')},
	description='This is a nondescript cuved street, which looks as if thousands of small rocks had bombarded it at high velocity, leaving pockmarks.',
	display_name='Wrecked Street'
)

Room('Wrecked Street, curve')(
	theme='crack',
	exits={'northwest': t('Wrecked Street, wall'), 'southeast': t('Wrecked Street, corner'), 'down': t('A Crumbling Stairway')},
	description="This is a nondescript cuved street, which looks as if thousands of small rocks had bombarded it at high velocity, leaving pockmarks. To the east of you lies a foundation for what must have been one of the area's larger buildings. There is a stairway leading downward at the edge of the foundation, which looks as if it was once covered by a bulkhead door.",
	display_name='Wrecked Street'
)

Room('Wrecked Street, north')(
	theme='crack',
	exits={'south': t('Wrecked Street, bookstore'), 'west': t('Crater Edge North'), 'north': t('Wrecked Street, corner')},
	description='This is a nondescript cuved street, which looks as if thousands of small rocks had bombarded it at high velocity, leaving pockmarks.',
	display_name='Wrecked Street'
)

Room('Wrecked Street, postwall')(
	theme='crack',
	exits={'south': t('Wrecked Alleyway'), 'northwest': t('Wrecked Street')},
	description='This is a nondescript cuved street, which looks as if thousands of small rocks had bombarded it at high velocity, leaving pockmarks.',
	display_name='Wrecked Street'
)

Room('Wrecked Street, south')(
	theme='crack',
	exits={'east': t('Wrecked House Foundation'), 'west': t('Crater Edge South'), 'north': t('Wrecked Street, bookstore')},
	description="This is a nondescript cuved street, which looks as if thousands of small rocks had bombarded it at high velocity, leaving pockmarks.  A narrow path leads off to the west into the southern edge of the crater which holds the bookstore, and to the east is a pile of rubble which may once have been a house.  To the south there is a very steep, large crater which doesn't appear navigable.",
	display_name='Wrecked Street'
)

Room('Wrecked Street, wall')(
	theme='crack',
	exits={'southwest': t('Empty Bakery'), 'southeast': t('Wrecked Street, curve'), 'northeast': t("Divu'en School Entranceway")},
	description='This is a nondescript cuved street, which looks as if thousands of small rocks had bombarded it at high velocity, leaving pockmarks.  There is a huge grey stone wall in the middle of the road to the northwest, as well as what looks like the ruins of a school-building to the northeast.  A sign that says "bakery" overhangs the building to the southwest.',
	display_name='Wrecked Street'
)

twisted.author.Author('Yumeika')(
	spells_learned=0,
	gender='f',
	gender_pronoun='woman',
	learned_frotz=-1,
	synonyms=['yume'],
	learned_zorft=-1,
	visit_color='silver',
	oldlocation=t('Science and Technology Demo Center(1)'),
	OBSOLETE_super=t('Class_Human'),
	description=observable.Hash({'__MAIN__': 'A young woman of average height and build.  There is nothing particularly noteworthy about her except for the raven-black hair, tied back loosely with a white ribbon.', 'clothing': [m('Yumeika','him_her'), ' is wearing ', 'a greyish cloth bound tightly across her eyes', ', ', 'a well-worn knapsack', ', ', 'a pale blue, almost kimono-like robe with wide, open sleeves', ', ', 'and ', 'a wide sash around her waist', '.']})
)

twisted.library.clothing.Robe("Yumeiko's pale blue kimono-like robe")(
	place=t('Yumeika'),
	synonyms=['robe', 'blue robe', 'pale robe'],
	clothing_appearance='a pale blue, almost kimono-like robe with wide, open sleeves',
	description='A kimono-like, pale blue robe with wide, open sleeves.',
	display_name='pale blue robe'
)

default_reality.resolve_all()
from cPickle import dump
dump(default_reality,open('divunal.rpl','wb'))
