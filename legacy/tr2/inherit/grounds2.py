from twisted.reality import *

t=reference.Reference
def d(**kw): return kw

Thing('Antechamber Table')(
	place=t('Chateau Antechamber'),
	description='This is a small table.',
	display_name="table"
)

Room('Antiques Room')(
	description='An Antiques Room looking as if it needs to be described.',
	exits={'east': t('Unfinished Room'), 'south': t('Chateau Hallway(8)'), 'north': t('Chateau Hallway(7)')}
)

Room('Back Lawn')(
	description='You are near the... aw, fuck it.',
	exits={'south': t('Chateau Pantry'), 'north': t('Back Lawn(1)'), 'east': t('Back Lawn(8)'), 'west': t('Back Lawn(9)')}
)

Room('Back Lawn(1)')(
	description='A Back Lawn looking as if it needs to be described.',
	exits={'east': t('Back Lawn(7)'), 'south': t('Back Lawn'), 'west': t('Back Lawn(3)')}
)

Room('Back Lawn(3)')(
	description='A Back Lawn looking as if it needs to be described.',
	exits={'east': t('Back Lawn(1)'), 'south': t('Back Lawn(9)'), 'north': t('Back lawn(4)')}
)

Room('Back lawn(4)')(
	description='A Back lawn looking as if it needs to be described.',
	exits={'east': t('Back Lawn(5)'), 'south': t('Back Lawn(3)')}
)

Room('Back Lawn(5)')(
	description='A Back Lawn looking as if it needs to be described.',
	exits={'south': t('Old Wooden Shed'), 'north': t('Wooded Grove'), 'east': t('Back Lawn(6)'), 'west': t('Back lawn(4)')}
)

Room('Back Lawn(6)')(
	description='A Back Lawn looking as if it needs to be described.',
	exits={'south': t('Back Lawn(7)'), 'west': t('Back Lawn(5)')}
)

Room('Back Lawn(7)')(
	description='A Back Lawn looking as if it needs to be described. A good old game of Croquet can be had here.',
	exits={'south': t('Back Lawn(8)'), 'west': t('Back Lawn(1)'), 'north': t('Back Lawn(6)')}
)

Room('Back Lawn(8)')(
	description='You are near the back end of the mansion, by the large field of overgrown grass and weeds that forms the back yard. The rear wall of the mansion continues on for quite some way to the west, towards the back door, and the lawn continues out to the north for quite a ways, where a dark, blocky shape is silhouetted against the trees.',
	exits={'east': t('Side Lawn'), 'west': t('Back Lawn'), 'north': t('Back Lawn(7)')}
)

Room('Back Lawn(9)')(
	description='You are near the back end of the mansion, by the large field of overgrown grass and weeds that forms the back yard. The rear wall of the mansion continues on for quite some way to the east, to the back door, and the lawn continues out to the north for quite a ways, where a dark, blocky shape is silhouetted against the trees.',
	exits={'east': t('Back Lawn'), 'west': t('Side Lawn(5)'), 'north': t('Back Lawn(3)')}
)

import inherit.monsters
inherit.monsters.BFNT('big nasty thing')(
	place=t('Side Lawn(1)'),
	description="This thing is big, and nasty, and horrible, and awful, and evil.  You really wish you weren't looking at it right now."
)

Room('Chateau Antechamber')(
	description="This is a dark, high-ceilinged room with a polished wooden floor.  Exits lead in all directions; you can go east or west through archways into the mansion's hallways, up to the second floor, or south through the front door.",
	exits={'south': t('Chateau Courtyard'), 'up': t('Chateau Staircase'), 'east': t('Chateau Hallway(16)'), 'west': t('Chateau Hallway')}
)

Room('Chateau Attic')(
	description='A Chateau Attic looking as if it needs to be described.',
	exits={'east': t('Chateau Attic(1)'), 'west': t('Chateau Attic(3)'), 'down': t('Chateau Hallway(4)')}
)

Room('Chateau Attic(1)')(
	description='A Chateau Attic looking as if it needs to be described.',
	exits={'south': t('Chateau Attic'), 'north': t('Chateau Attic(2)')}
)

Room('Chateau Attic(2)')(
	description='A Chateau Attic looking as if it needs to be described.',
	exits={'south': t('Chateau Attic(1)')}
)

Room('Chateau Attic(3)')(
	description='A Chateau Attic looking as if it needs to be described.',
	exits={'east': t('Chateau Attic'), 'south': t('Chateau Attic(4)')}
)

Room('Chateau Attic(4)')(
	description='A Chateau Attic looking as if it needs to be described.',
	exits={'north': t('Chateau Attic(3)')}
)

Room('Chateau Basement')(
	description='A Chateau Basement looking as if it needs to be described.',
	exits={'east': t('Chateau Basement(1)'), 'west': t('Chateau Basement(3)'), 'up': t('Chateau Stairwell')}
)

Room('Chateau Basement(1)')(
	description='A Chateau Basement looking as if it needs to be described.',
	exits={'west': t('Chateau Basement'), 'north': t('Chateau Basement(2)')}
)

Room('Chateau Basement(2)')(
	description='A Chateau Basement looking as if it needs to be described.',
	exits={'south': t('Chateau Basement(1)')}
)

Room('Chateau Basement(3)')(
	description='A Chateau Basement looking as if it needs to be described.',
	exits={'east': t('Chateau Basement'), 'north': t('Chateau Basement(4)')}
)

Room('Chateau Basement(4)')(
	description='A Chateau Basement looking as if it needs to be described.',
	exits={'south': t('Chateau Basement(3)')}
)

Room('Chateau Bathroom')(
	description='A Bathroom looking as if it needs to be described.',
	exits={'north': t('Chateau Bedroom')}
)

Room('Chateau Bedroom')(
	description='A Bedroom looking as if it needs to be described.',
	exits={'south': t('Chateau Bathroom'), 'west': t('Chateau Hallway(14)')}
)

Room('Chateau Courtyard')(
	description='You are standing in front of a large grey mansion. A circular gravel drive runs past the front steps, leading south to where it passes through the middle of a huge field of yellowed corn. The lawn continues to the east and west, as does the mansion itself, towards the forest that surrounds the property.',
	exits={'south': t('Circular Driveway'), 'north': t('Chateau Antechamber'), 'east': t('Front Lawn(1)'), 'west': t('Front Lawn(3)')}
)

Room('Chateau Dining Hall')(
	description='A Chateau Dining Hall looking as if it needs to be described.',
	exits={'south': t('Chateau Hallway'), 'north': t('Chateau Dining Hall(1)')}
)

Room('Chateau Dining Hall(1)')(
	description='A Chateau Dining Hall looking as if it needs to be described.',
	exits={'south': t('Chateau Dining Hall'), 'north': t('Chateau Hallway(1)')}
)

Room('Chateau Hallway')(
	description='A Chateau Hallway looking as if it needs to be described.',
	exits={'east': t('Chateau Antechamber'), 'north': t('Chateau Dining Hall')}
)

Room('Chateau Hallway(1)')(
	description='A Chateau Hallway looking as if it needs to be described.',
	exits={'east': t('Chateau Kitchen'), 'south': t('Chateau Dining Hall(1)')}
)

Room('Chateau Hallway(10)')(
	description='A Chateau Hallway looking as if it needs to be described.  It should have a couch or something, pointed out the window.',
	exits={'east': t('Chateau Hallway(11)'), 'west': t('Chateau Hallway(9)')}
)

Room('Chateau Hallway(11)')(
	description='A Chateau Hallway looking as if it needs to be described.',
	exits={'east': t('Chateau Hallway(12)'), 'west': t('Chateau Hallway(10)')}
)

Room('Chateau Hallway(12)')(
	description='A Chateau Hallway looking as if it needs to be described.',
	exits={'west': t('Chateau Hallway(11)'), 'north': t('Study')}
)

Room('Chateau Hallway(13)')(
	description='A Chateau Hallway looking as if it needs to be described.',
	exits={'east': t('Chateau Library'), 'south': t('Chateau Hallway(6)'), 'west': t('Guest Bedroom')}
)

Room('Chateau Hallway(14)')(
	description='A Chateau Hallway looking as if it needs to be described.',
	exits={'east': t('Chateau Bedroom'), 'south': t('Chateau Hallway(5)'), 'west': t('Chateau Library(2)')}
)

Room('Chateau Hallway(15)')(
	description='A Chateau Hallway looking as if it needs to be described.',
	exits={'west': t('Chateau Hallway(5)')}
)

Room('Chateau Hallway(16)')(
	description='A Chateau Hallway looking as if it needs to be described.',
	exits={'west': t('Chateau Antechamber'), 'north': t('Chateau Sitting Room')}
)

Room('Chateau Hallway(2)')(
	description='A Chateau Hallway looking as if it needs to be described.',
	exits={'south': t('Chateau Parlor'), 'west': t('Chateau Pantry')}
)

Room('Chateau Hallway(3)')(
	description='A Chateau Hallway looking as if it needs to be described.',
	exits={'south': t('Chateau Sitting Room'), 'west': t('Chateau Lavatory'), 'north': t('Chateau Parlor')}
)

Room('Chateau Hallway(4)')(
	description='A Chateau Hallway looking as if it needs to be described.',
	exits={'east': t('Chateau Staircase Landing')}
)

Room('Chateau Hallway(5)')(
	description='A Chateau Hallway looking as if it needs to be described.',
	exits={'east': t('Chateau Hallway(15)'), 'west': t('Chateau Hallway(4)'), 'north': t('Chateau Hallway(14)')}
)

Room('Chateau Hallway(6)')(
	description='A Chateau Hallway looking as if it needs to be described.',
	exits={'east': t('Chateau Staircase Landing'), 'west': t('Chateau Hallway(7)'), 'north': t('Chateau Hallway(13)')}
)

Room('Chateau Hallway(7)')(
	description='A Chateau Hallway looking as if it needs to be described.',
	exits={'east': t('Chateau Hallway(6)'), 'south': t('Antiques Room')}
)

Room('Chateau Hallway(8)')(
	description='A Chateau Hallway looking as if it needs to be described.',
	exits={'east': t('Chateau Hallway(9)'), 'north': t('Antiques Room')}
)

Room('Chateau Hallway(9)')(
	description='A Chateau Hallway looking as if it needs to be described.',
	exits={'east': t('Chateau Hallway(10)'), 'west': t('Chateau Hallway(8)')}
)

Room('Chateau Kitchen')(
	description='A Chateau Kitchen looking as if it needs to be described.',
	exits={'east': t('Chateau Pantry'), 'south': t('Kitchen Closet'), 'west': t('Chateau Hallway(1)')}
)

Room('Chateau Lavatory')(
	description='A Chateau Lavatory looking as if it needs to be described.',
	exits={'east': t('Chateau Hallway(3)')}
)

Room('Chateau Library')(
	description='A Chateau Library looking as if it needs to be described.',
	exits={'east': t('Chateau Library(1)'), 'west': t('Chateau Hallway(13)')}
)

Room('Chateau Library(1)')(
	description='A Chateau Library looking as if it needs to be described.',
	exits={'east': t('Chateau Library(2)'), 'south': t('Chateau Staircase Landing'), 'west': t('Chateau Library')}
)

Room('Chateau Library(2)')(
	description='A Chateau Library looking as if it needs to be described.',
	exits={'east': t('Chateau Hallway(14)'), 'west': t('Chateau Library(1)')}
)

Room('Chateau Pantry')(
	description='A Chateau Pantry looking as if it needs to be described.',
	exits={'south': t('Chateau Stairwell'), 'north': t('Back Lawn'), 'east': t('Chateau Hallway(2)'), 'west': t('Chateau Kitchen')}
)

Room('Chateau Parlor')(
	description='A Chateau Parlor looking as if it needs to be described.',
	exits={'south': t('Chateau Hallway(3)'), 'north': t('Chateau Hallway(2)')}
)

Room('Chateau Sitting Room')(
	description='here is a place where you sit.  DESCRIBE ME',
	exits={'south': t('Chateau Hallway(16)'), 'north': t('Chateau Hallway(3)')}
)

Room('Chateau Staircase')(
	description='A Chateau Staircase looking as if it needs to be described.',
	exits={'up': t('Chateau Staircase Landing'), 'down': t('Chateau Antechamber')}
)

Room('Chateau Staircase Landing')(
	description='A Chateau Staircase Landing looking as if it needs to be described.',
	exits={'north': t('Chateau Library(1)'), 'east': t('Chateau Hallway(4)'), 'west': t('Chateau Hallway(6)'), 'down': t('Chateau Staircase')}
)

Room('Chateau Stairwell')(
	description='A Chateau Stairwell looking as if it needs to be described.',
	exits={'down': t('Chateau Basement'), 'north': t('Chateau Pantry')}
)

Room('Circular Driveway')(
	description='The far side of a circular gravel drive, both ends of which lead north towards a tall, imposing mansion. To the south, the two sides converge into a single driveway and lead uphill through the middle of a vast, yellowish white field of dead corn.',
	exits={'south': t('Gravel Driveway'), 'north': t('Chateau Courtyard'), 'east': t('Front Lawn(2)'), 'west': t('Front Lawn(4)')}
)

import inherit.tools
inherit.tools.Clip('Colt 1911 Clip')(
	place=t('Side Lawn'),
	synonyms=['clip']
)

inherit.tools.Gun('Colt 1911 Semi-Auto')(
	place=t('Side Lawn'),
	synonyms=['gun', 'auto', 'semi-auto', 'colt', 'pistol', 'automatic'],
	must_hit=0,
	misses=0,
	description='It appears to be a Colt 1911, but it is vague, indistinct, and little more than a blurry smear on reality.'
)

Room('Country Road')(
	description='An old dirt road, leading off into the darkness to the east and west. It is bordered on the south side by a crumbling stone wall, while an opening in the trees to the north leads downhill to a gravel driveway.',
	exits={'east': t('Country Road(1)'), 'west': t('Country Road(3)'), 'north': t('Driveway')}
)

Room('Country Road(1)')(
	description='A poorly maintained dirt road, leading off into darkness to the east and west. It is bordered by a steep ridge to the north, and an old stone wall to the south. The branches of the trees along the sides of the road nearly meet overhead, throwing a patchwork of shadows over the ground.',
	exits={'east': t('Country Road(2)'), 'west': t('Country Road')}
)

Room('Country Road(2)')(
	description='A poorly maintained dirt road, leading off into darkness to the east and west. It is bordered by a steep ridge to the north, and a crumbling stone wall to the south. The trees along the road form a thick canopy overhead, blocking out even the faint light from the sky.',
	exits={'east': t('Darkened Road'), 'west': t('Country Road(1)')}
)

Room('Country Road(3)')(
	description='A poorly maintained dirt road, leading off into darkness to the east and west. It is bordered by a steep ridge to the north, and an old stone wall to the south. The branches of the trees along the edge of the road nearly touch overhead, covering the ground with dancing shadows and faint patches of light',
	exits={'east': t('Country Road'), 'west': t('Country Road(4)')}
)

Room('Country Road(4)')(
	description='A poorly maintained dirt road, leading off into darkness to the east and west. It is bordered by a steep ridge to the north, and a crumbling stone wall to the south. The trees along the road form a thick canopy overhead, lacing together like skeletal fingers to block out the faint light from the sky.',
	exits={'east': t('Country Road(3)'), 'west': t('Darkened Road(2)')}
)

import inherit.claimant
damien=inherit.claimant.Claimant('Damien')(
	place=t('Side Lawn'),
	edible=1,
	description='He looks pretty hassled.',
	password='BvTJQWM0f2iHM'
)

Room('Darkened Road')(
	description='An old dirt road, leading off into darkness to the east and west. It is bordered by a steep ridge to the north, and the crumbling remains of a stone wall to the south. The trees form an almost solid wall of leaves and branches above the road, blotting out the sky.',
	exits={'east': t('Darkened Road(1)'), 'west': t('Country Road(2)')}
)

Room('Darkened Road(1)')(
	description='The road twists and turns through the narrow space allotted by the trees, which have grown even closer together overhead, shutting out the light from the sky. The stone wall is only a scattered pile of stones at this point, leaving the road open to the darkness of the forest to the south.',
	exits={'west': t('Darkened Road')}
)

Room('Darkened Road(2)')(
	description='A faint trail through the woods that may once have been a dirt road, leading off into darkness to the east and west. It is bordered by a steep ridge to the north, and the crumbling remains of a stone wall to the south, overgrown with ferns and odd looking plants. The trees form an almost solid wall of leaves and clawlike branches above the road, shutting out the sky.',
	exits={'east': t('Country Road(4)'), 'west': t('Darkened Road(3)')}
)

Room('Darkened Road(3)')(
	description='The road has given way to a narrow, forgotten path through the trees, overgrown with ferns and dark, waving grass. The trees seem to have grown together into a single, writhing mass above the road.',
	exits={'east': t('Darkened Road(2)')}
)

inherit.tools.Bullet('dented bullet')(
	place=t('Side Lawn'),
	synonyms=['bullet', 'dented']
)

Room('Driveway')(
	description='The far end of a long gravel driveway leading downhill to the north, where the dark outlines of a house loom above the horizon. To the south, an old dirt road is visible through an opening in the trees, and to the east and west are endless yellow fields of neglected corn.',
	exits={'south': t('Country Road'), 'north': t('Gravel Driveway(2)')}
)

import inherit.car
inherit.car.Car('Ford Runabout')(
	interior="The interior of the runabout isn't much more pleasant than the outside, and is similarly colored. Two stiffly upholstered chairs are bolted to the floorboards, sheltered somewhat from the outside by a black canvas roof and a thin, slanted windshield. The brake and gas pedals are located conveniently for the driver, but the steering wheel is mounted quite a bit higher than you'd like, from the end of a long metal rod extending up from deep under the engine.",
	exterior='A rather beat up looking specimen of the Ford Model T Runabout series. It is a blocky, ungainly little car, standing a few feet off the ground on its large spoked wheels, and painted a uniform black like every other motor car Ford has produced in the last ten years. It is an older design, lacking the electric ignition and headlights of more modern vehicles, and has a large socket in the hood for the starter crank. The rear end consists mostly of a rounded trunk hanging over the back wheels, where the driver can store their personal effects. ',
	place=t('Side Lawn'),
	synonyms=['car'],
	description=inherit.car.Describer(t('Ford Runabout'))
)

inherit.car.Trunk('Ford Runabout Trunk')(
	closed='The back end of the Runabout consists primarily of a lumpy metal trunk suspended over the back wheels. It is currently closed.',
	place=t('Ford Runabout'),
	synonyms=['trunk', 'ford trunk'],
	opened="The Runabout's trunk is open, revealing a bare, dirty steel compartment."
)

Room('Forest Clearing')(
	description='An undescribed forest clearing.',
	exits={'south': t('Wooded Grove')}
)

Room('Front Lawn')(
	description="The mansion's unkempt lawn surrenders to the yellowed remains of a cornfield to the south, and a dense bordering forest to the east. The tall grass of the lawn continues to the west, towards the mansion's gravel drive, and north, towards the mansion itself.",
	exits={'west': t('Front Lawn(2)'), 'north': t('Side Lawn(2)')}
)

Room('Front Lawn(1)')(
	description='You are in front of the east wing of a weathered old mansion. It continues to the east, almost touching the dense forest that lines the property, and to the west, towards the gravel driveway leading to the front door. The unkempt grass of the front lawn continues on to the south before giving way to a vast field of yellowed corn.',
	exits={'east': t('Side Lawn(2)'), 'south': t('Front Lawn(2)'), 'west': t('Chateau Courtyard')}
)

Room('Front Lawn(2)')(
	description="The knee high lawn of the mansion trails off a bit to the south, where the yellow husks of the cornfield begin. The lawn continues to the east, towards the forest surrounding the property, and north, towards the mansion itself. The mansion's  gravel drive is just to the west, leading up to the front steps.",
	exits={'east': t('Front Lawn'), 'west': t('Circular Driveway'), 'north': t('Front Lawn(1)')}
)

Room('Front Lawn(3)')(
	description='You are in front of the west wing of a darkened old mansion. It continues to the west, almost touching the dense forest that lines the property, and to the east, towards the gravel driveway leading to the front door. The unkempt grass of the front lawn continues to the south before giving way to a vast field of yellowed corn.',
	exits={'east': t('Chateau Courtyard'), 'south': t('Front Lawn(4)'), 'west': t('Side Lawn(3)')}
)

Room('Front Lawn(4)')(
	description="The unkempt lawn of the mansion stops just to the south, where the dried yellow ruin of the cornfield begins. The knee high grass continues west, towards the forest surrounding the property, and north, towards the mansion itself. A curved gravel drive passes by to the east, following an arc that leads up to the mansion's front steps.",
	exits={'east': t('Circular Driveway'), 'west': t('Front Lawn(5)'), 'north': t('Front Lawn(3)')}
)

Room('Front Lawn(5)')(
	description="The edge of the mansion's unkempt lawn, where it surrenders to the yellowed remains of a cornfield to the south and the dense bordering forest to the west. The lawn continues to the east, towards the mansion's gravel drive, and north, towards the mansion itself.",
	exits={'east': t('Front Lawn(4)'), 'north': t('Side Lawn(3)')}
)

Room('Gravel Driveway')(
	description='The bottom end of a long gravel driveway, leading towards a dark, imposing mansion. Vast fields of corn rise up on either side, brittle and yellow with age. Further to the north, the driveway splits into a circular parth in the courtyard of the mansion, while to the south, it continues uphill towards a distant forest.',
	exits={'south': t('Gravel Driveway(1)'), 'north': t('Circular Driveway')}
)

Room('Gravel Driveway(1)')(
	description='A long gravel driveway surrounded by cornfields. It leads upwards to the south, towards where the fields give way to a vast expanse of forest, and downwards to the north, towards a dark, weathered old mansion.',
	exits={'south': t('Gravel Driveway(2)'), 'north': t('Gravel Driveway')}
)

Room('Gravel Driveway(2)')(
	description='A long gravel driveway, surrounded by yellowed cornfields on either side. To the south, it leads uphill towards the forest at the edge of the property, and to the north, it runs downhill towards the dark shape of a house silhoutted against the horizon.',
	exits={'south': t('Driveway'), 'north': t('Gravel Driveway(1)')}
)

Room('Guest Bathroom')(
	description='A Guest Bathroom looking as if it needs to be described.',
	exits={'north': t('Guest Bedroom')}
)

Room('Guest Bedroom')(
	description='A Guest Bedroom looking as if it needs to be described.',
	exits={'east': t('Chateau Hallway(13)'), 'south': t('Guest Bathroom')}
)

Room('Kitchen Closet')(
	description='A Kitchen Closet looking as if it needs to be described.',
	exits={'north': t('Chateau Kitchen')}
)

import inherit.books
inherit.books.Translator('leather bound book')(
	place=t('Side Lawn'),
	synonyms=['book', 'leather book'],
	read_text="The manual's innumerable pages are covered in illustrations and notes regarding the strange symbolic language of the egyptians. While some of the illustrations are interesting, this book makes for fairly dry and uninteresting reading, although it would probably be very useful in an attempt to translate hieroglyphics.",
	description='A large and extremely thick leather bound book, entitled "A Practical Guide to Egyptian Hieroglyphs, by Lord Rutherford P. Beaucavage, Esquire". While one of the more massive and unwieldy books you\'ve ever had tthe misfortune to encounter, it appears to be nothing if not comprehensive.'
)

inherit.tools.Leaflet('Letter')(
	place=t('Antechamber Table')
)

inherit.tools.Bullet('moldy bullet')(
	place=t('Side Lawn'),
	synonyms=['bullet', 'moldy']
)

inherit.monsters.Mummy('Mummy')(
	place=t('Side Lawn')
)

Room('Old Wooden Shed')(
	description='An Old Wooden Shed looking as if it needs to be described.',
	exits={'north': t('Back Lawn(5)')}
)

inherit.tools.Bullet('rusty bullet')(
	place=t('Side Lawn'),
	synonyms=['rusty', 'bullet']
)

inherit.monsters.Sarcophagus('Sarcophagus')(
	place=t('Side Lawn'),
	description='An ornately carved stone coffin, lined with small hieroglyphics and symbols.'
)

Room('Side Lawn')(
	description='You are near the rear corner of the mansion, where a thick field of tall grass and weeds that was once the back yard extends outwards to the west. Further north, towards the back of the lawn, you can make out the shape of a small shed against the trees, and there is a narrow path leading south between the wall of the mansion and the forest that has grown up against it.',
	exits={'south': t('Side Lawn(1)'), 'west': t('Back Lawn(8)')}
)

Room('Side Lawn(1)')(
	description='A narrow path between the thick overgrowth  of the forest and the rotting wooden walls of the mansion. It leads south to the front lawn, and continues towards a similar clearing to the north.',
	exits={'south': t('Side Lawn(2)'), 'north': t('Side Lawn')}
)

Room('Side Lawn(2)')(
	description='You are at the eastern corner of a darkened old mansion. The nearby forest has begun to grow in over the lawn, and the branches of the closest trees almost touch the eastern wall, leaving a narrow path along the side of the mansion to the north. The lawn continues along the front of the mansion to the east, towards the front door, and to the south, where it gives way to the yellowed remains of a cornfield.',
	exits={'south': t('Front Lawn'), 'west': t('Front Lawn(1)'), 'north': t('Side Lawn(1)')}
)

Room('Side Lawn(3)')(
	description="You are at the western corner of an old, neglected mansion. The surrounding forest has begun to spread over the lawn, and the branches of the nearest trees are beginning to brush the mansion's walls, leaving only a narrow path between them to the north. The lawn continues along the front of the mansion to the east, towards the front door, and to the south, where it gives way to a long forgotten cornfield.",
	exits={'east': t('Front Lawn(3)'), 'south': t('Front Lawn(5)'), 'north': t('Side Lawn(4)')}
)

Room('Side Lawn(4)')(
	description="A narrow path between the dense trees and brush of the forest and the peeling grey wood of the mansion's western wall. It continues south to the front lawn, and meanders along into a similar clearing to the north.",
	exits={'south': t('Side Lawn(3)'), 'north': t('Side Lawn(5)')}
)

Room('Side Lawn(5)')(
	description='You are near the back side of the mansion, where an unkempt field of weeds and tall grass that was once the back lawn extends outwards to the east. Further north, towards the back of the yard, you can make out the shape of a small building against the trees, and there is a narrow path leading south between the western wall of the mansion and the forest that has grown up against it. ',
	exits={'east': t('Back Lawn(9)'), 'south': t('Side Lawn(4)')}
)

Room('Study')(
	description='A Study looking as if it needs to be described.',
	exits={'south': t('Chateau Hallway(12)')}
)

Room('Unfinished Room')(
	description='An Unfinished Room, looking like some kind of crazy Tool video or something.',
	exits={'west': t('Antiques Room')}
)

Room('Wooded Grove')(
	description='A Wooded Grove looking as if it needs to be described.',
	exits={'south': t('Back Lawn(5)'), 'north': t('Forest Clearing')}
)

default_reality.resolve_all()
