Location
{
	name "wide sash"
	describe "A wide sash."
	place "Yumeika"
	feature "twisted.reality.plugin.Put"
	string "clothing appearance" "a wide sash around her waist"
	boolean "clothing worn" true
	extends "class_belt"
	component
	syn "sash"
}

Room
{
	name "Rough Floor"
	describe "In contrast to the room to the south, the floor is very rough here. You realize now that the other floor was almost polished in its smoothness, whereas this floor is jagged and covered in bits of loose stone. It also feels a little bit warmer than the room to the south, although the breeze blowing through to the north is a bit chilly."
	theme "greystone"
	string "name" "A Dark Place"
	string "description" "It's too dark in here to see!"
	boolean "inhibit_exits" true
	boolean "inhibit_items" true
	extends "Class_Dark Room"
	opaque
	shut
	exit "north" to "Rough Passage"
	exit "south" to "Cold Floor"
	claustrophobic
}

Room
{
	name "Nice Office"
	describe "This is a plush office, well-decorated and hardly damaged at all. There are a few minor dents and cracks in the ceiling, but other than that there's not much wrong here.  A large desk and wheeled chair (both bolted to the floor) adorn the western end of the room."
	exit "north" to "Small Grey Room"
	exit "south" to "Reception Area"
}

Location
{
	name "science and technology demo center table"
	describe "A long, rectangular table built of polished stainless steel."
	place "Science And Technology Demo Center"
	feature "twisted.reality.plugin.furniture.Sit"
	feature "twisted.reality.plugin.furniture.Stand"
	feature "twisted.reality.plugin.Put"
	int "maximum occupancy" 3
	string "preposition" "on"
	string "player preposition" "sitting on"
	string "name" "table"
	component
	syn "table"
	broadcast
}

Room
{
	name "Underground Grotto"
	describe "There is a great underground river here, which comes in over a waterfall at the east end of the cave. Despite the turbulent waterfall, the rest of the river's mirrorlike surface is incredibly serene. These caverns have been carved by nature through the centuries, resulting in the beautiful scene you see before you. There is a ladder leading up here, and to the west, the river continues to flow into a tunnel. It looks to be passable by boat. Near you, on the bank, is a elegant teakwood podium, upon which is a bell and a small white sign."
	theme "water"
	string "name" "Riverbank in Underground Grotto"
	exit "west" to "Dark River Tunnel" with "tunnelX1"
	exit "up" to "Inside Oak Tree"
}

Thing
{
	name "Message"
	describe "Greetings all... The chambers further on are in midst of construction... Please refrain from entering. THANK YOU FOR LISTENING....Only the foolish continue."
	place "A Small Dark Crevice"
	component
}

Thing
{
	name "strength dial"
	describe "A white box."
	place "Genetic Laboratory"
	float "value" "-0.15"
	extends "Class_Player Creation Dial"
	component
	syn "strength"
	syn "dial"
}

Room
{
	name "Sitting Room"
	describe "A Sitting Room looking as if it needs to be described."
	theme "default"
	exit "east" to "Castle Greysen Fountain Room"
	exit "west" to "Castle Foyer"
}

Room
{
	name "New Jersey Apartment Entrance Hall"
	describe "A small room with a mirror and end table against one wall, and four different doors. Two of them are white and identically paneled, leading west and presumably out into New Jersey itself. The other two are made of dark brown wood, one closed and firmly locked, and the other standing open, to a flight of stairs leading upwards\n"
	theme "default"
	exit "up" to "New Jersey Apartment Living Room"
}

Room
{
	name "Main Aisle, West End"
	describe "This is the main aisle of the floor of a bookstore. There are three aisles branching from it, spaced at regular intervals along the floor - the aisles are almost separate rooms because the bookshelves touch the ceilings and the floors and there is a wide separation between one aisle and the next because the shelves are so deep.  You are standing at the front of the third sub-aisle, at the western end of the main one. A plaque on the floor here reads \"101-707, Miscelleneous Reading, Fiction, and Other Books\". You can continue northward to into the Miscelleneous Reading aisle, or east to another section."
	theme "paper"
	exit "east" to "Main Aisle, Center"
	exit "north" to "Aisle 3."
}

Location
{
	name "Colt 1911 pistol clip"
	describe "A blue box."
	place "Colt 1911 Semi-Auto"
	string "clip type" "colt 1911"
	string "bullet type" ".45 ACP"
	string "name" "clip"
	
	persistable "bullets" "twisted.reality.Stack" val "thing dirty bullet\nthing dirty bullet\nthing dented bullet\n" key "twisted.reality.Stack@58512fa"
	extends "class_pistol clip"
	component
	syn "clip"
}

Room
{
	name "Boring East-West Path"
	describe "This is a relatively boring east-west path."
	exit "west" to "Interesting East-West Path"
	exit "east" to "Another Junction"
}

Location
{
	name "cement urn"
	describe "Along the rim of the urn there are several Taoist images. The urn itself seems to be very well built, in all..."
	place "Ivy Garden"
	extends "Class_Container"
	component
	syn "urn"
}

Room
{
	name "Demo Center Lavatory"
	describe "A square, more modestly sized room lined entirely in light grey tiles. A black plastic wastebasket stands against the south wall, opposite a small white sink and the much larger mirror hanging above it. A blue swinging door leads out of the bathroom to the west."
	place "Demo"
	theme "default"
	descript "demo center bathroom stall door openDesc" "To the east, the door to the single bathroom stall stands open."
	exit "east" to "Demo Center Bathroom Stall" with "demo center bathroom stall door"
	exit "west" to "Demo Center East Wing" with "demo center bathroom door"
}

Thing
{
	name "colt 1911 pistol slide"
	describe "It appears to be a colt 1911 pistol slide, but it is vague, indistinct, and little more than a blurry smear on reality."
	place "Colt 1911 Semi-Auto"
	string "name" "slide"
	extends "class_pistol slide"
	component
	syn "action"
	syn "slide"
}

Thing
{
	name "scrap of parchment"
	describe "A small scrap of parchment with some words written in an archaic hand on it.  It reads:\n\"Always--I tell you this they learned--\nAlways at night when they returned\nTo the lonely house from far away\nTo lamps unlighted and fire gone gray,\nThey learned to rattle the lock and key\nTo give whatever might chance to be\nWarning and time to be off in flight:\nAnd preferring the out- to the in-door night,\nThey learned to leave the house-door wide\nUntil they had lit the lamp inside.\"\n\nIn a messier hand, below, it reads:\n\"Leave the keys for other guests.  The lock isn't loud enough.\""
	place "Maxwell"
	syn "parchment"
	syn "scrap"
}

Location
{
	name "cabinets"
	describe "A set of glass cabinets with dark, polished wooden frames."
	place "Mansion Study"
	theme "wood"
	component
	syn "cabinet"
}

Thing
{
	name "science and technology manuals"
	describe "There are several manuals on the counter, each of which seems to be firmly attached. Of particular note are the manuals titled \"Nominator\" and \"Gender Changer\"."
	place "Science And Technology Demo Center"
	string "name" "technical manuals"
	component
	syn "manuals"
	syn "technical manuals"
}

Room
{
	name "Cold Floor"
	describe "It is still dark here -- if anything it is more dark in this place than it was on the ledge. Your pupils stretch to their limits but detect nothing.\nFortunately, your other senses begin to work overtime, and you quickly notice the icy coldness of the stone(?) floor beneath you. The air smells fresh, and you sense a slight breeze from above. It might be blowing to the west, or perhaps it is getting sucked northward."
	theme "greystone"
	string "name" "A Dark Place"
	string "description" "It's too dark in here to see!"
	boolean "inhibit_exits" true
	boolean "inhibit_items" true
	extends "Class_Dark Room"
	opaque
	shut
	exit "east" to "Plain Room"
	exit "southwest" to "Uneven Floor"
	exit "west" to "Wet Floor"
	exit "north" to "Rough Floor"
	claustrophobic
}

Room
{
	name "RCC Rec Area East"
	describe "This is a recreation area with a bunch of table gaming equipment such as air-hockey and pool.  Nothing seems interesting here as all of the equipment looks mostly broken.  This area continues for a while to the west, and there is a room to the south.  This place overlooks a middle-sized gym with some basketball hoops."
	exit "south" to "RCC South Lounge"
	exit "west" to "RCC Rec Area West"
}

Room
{
	name "Silver Shadowed Glade(7)"
	describe "Tall grass surrounds you tightly, pushing at you, and disorienting you.  Everything you look at has a strange silvery haze over it. "
	theme "leaf"
	exit "northwest" to "Silver Shadowed Glade(7)"
	exit "north" to "Silver Shadowed Glade"
	exit "southeast" to "Silver Shadowed Plain"
	exit "southwest" to "Silver Shadowed Fields"
}

Thing
{
	name "fifth knob"
	describe "Fifth knob from the top of the qin with which to tune the instrument."
	place "qin"
	component
	syn "knob5"
	syn "knob"
}

Location
{
	name "Ford Runabout"
	describe "A rather beat up looking specimen of the Ford Model T Runabout series. It is a blocky, ungainly little car, standing a few feet off the ground on its large spoked wheels, and painted a uniform black like every other motor car Ford has produced in the last ten years. It is an older design, lacking the electric ignition and headlights of more modern vehicles, and has a large socket in the hood for the starter crank. The rear end consists mostly of a rounded trunk hanging over the back wheels, where the driver can store their personal effects. "
	mood "parked on the edge of the driveway"
	place "Chateau courtyard"
	feature "inheritance.car.CarEnterLeave"
	float "weight" "100.0"
	
	property "description" "inheritance.car.CarLook"
	string "interior description" "The interior of the runabout isn't much more pleasant than the outside, and is similarly colored. Two stiffly upholstered chairs are bolted to the floorboards, sheltered somewhat from the outside by a black canvas roof and a thin, slanted windshield. The brake and gas pedals are located conveniently for the driver, but the steering wheel is mounted quite a bit higher than you'd like, from the end of a long metal rod extending up from deep under the engine."
	syn "ford"
	syn "motor car"
	syn "automobile"
	syn "car"
	syn "runabout"
	broadcast
}

Location
{
	name "large black cauldron"
	describe "This cauldron is filled with a strange phosphorescent liquid. Some other objects can be seen floating in the goo."
	place "Guyute's Laboratory"
	extends "Class_Container"
	component
	syn "cauldron"
}

Room
{
	name "Side Lawn(3)"
	describe "You are at the western corner of an old, neglected mansion. The surrounding forest has begun to spread over the lawn, and the branches of the nearest trees are beginning to brush the mansion's walls, leaving only a narrow path between them to the north. The lawn continues along the front of the mansion to the east, towards the front door, and to the south, where it gives way to a long forgotten cornfield.\n"
	place "Inheritance"
	theme "leaf"
	string "name" "Front Lawn"
	exit "east" to "Front Lawn(3)"
	exit "north" to "Side Lawn(4)"
	exit "south" to "Front Lawn(5)"
}

Room
{
	name "Chateau Kitchen"
	describe "A Chateau Kitchen looking as if it needs to be described."
	place "Inheritance"
	theme "greystone"
	exit "east" to "Chateau Pantry"
	exit "south" to "Kitchen Closet"
	exit "west" to "Chateau Hallway(1)"
}

Location
{
	name "demo center obelisk"
	describe "The obelisk is a polished, glossy black, and set with a large, colorful map and various pieces of Twisted Reality propoganda. At the top is a familiar looking black line-art \"Twisted Reality 1.2.1\" logo, and a large piece of text welcoming you to the demo center. Below that is a bright yellow polygon, very similar to the shape of the room you're currently standing in, labeled \"YOU ARE HERE!\". The hallway leading east from the main room connects to a large blue area labeled \"Restrooms\" to the east, and a much smaller, brown room to the north, labeled \"development\". The west hallway branches off into a Lobby, with a Gift Shop to it's north, and two \"Staging Areas\" further west."
	place "Demo Information Center"
	feature "twisted.reality.plugin.ReadLook"
	feature "twisted.reality.plugin.furniture.Stand"
	feature "twisted.reality.plugin.furniture.Sit"
	feature "twisted.reality.plugin.Put"
	string "name" "Obsidian Obelisk"
	string "player preposition" "sitting on"
	string "preposition" "on"
	int "maximum occupancy" 3
	component
	syn "brightly colored map"
	syn "map"
	syn "obelisk"
	broadcast
}

Thing
{
	name "Class_Gloves"
	describe "A white box."
	place "Clothing Box"
	extends "Class_Clothing"
}

Thing
{
	name "Class_Bookshelf"
	describe "A white box."
	place "Book Box"
}

Room
{
	name "A Swirling Mass Of Colors"
	describe "A swirling, chaotic mass of colors... Or whatever else Tsiale wants it to be."
}

Room
{
	name "Uridians Dimension"
	describe "This is a mysterious place unlike the area you travelled from. The area around you is totally dark except for the center of the room, which seems to be lit by a circle of light whose orgin is indeterminable."
	theme "default"
}

Thing
{
	name "orange cube"
	describe "A white box."
	place "Cold Floor"
	thing "teleport phrase I leave now" "Myth Section"
	handler "say" "divunal.common.author.VoiceTeleport"
	syn "cube"
}

Thing
{
	name "class_belt"
	describe "A rather nondescript class_belt."
	place "Clothing Box"
	string "clothing location" "waist"
	extends "Class_Clothing"
}

Location
{
	name "faded brown coat"
	describe "A careworn old coat, faded from the sun."
	place "Aaron"
	feature "twisted.reality.plugin.Put"
	boolean "clothing worn" true
	string "clothing appearance" "faded brown coat"
	extends "Class_Shirt"
	component
	syn "coat"
	syn "brown coat"
	syn "jacket"
	syn "brown jacket"
	syn "faded jacket"
	syn "faded brown jacket"
	syn "faded coat"
}

Location
{
	name "clue fourth chair"
	describe "A rather nondescript clue fourth chair."
	place "Garden Maze(12)"
	string "name" "fourth chair"
	extends "Class_Sittable"
	component
	syn "chair"
	syn "fourth chair"
	broadcast
}

Thing
{
	name "maze timer"
	describe "There's not really much to say about this. It's just a red spring-loaded button on some sort of pedestal."
	place "Garden Maze"
	string "name" "large red button"
	component
	syn "large red button"
	syn "button"
	syn "red button"
}

Thing
{
	name "brown leather belt"
	describe "The complete absence of cracks in the thick leather indicate that this belt has been well-broken in.  Still, the dust-brown hide shows no stains, nor does the rounded gold buckle suffer any marks to mar its smooth, matte finish."
	place "Jedin"
	string "clothing appearance" "a well-worn brown leather belt"
	boolean "clothing worn" true
	extends "class_belt"
	component
	syn "leather belt"
	syn "brown belt"
	syn "belt"
}

Thing
{
	name "Castle's Wall"
	describe "The wall of the castle, rather than being hollow to accomodate rooms, is completely solid stone!  From what you can see, this portion of the castle is just a huge smashed block of marble, and it is not now, nor ever was, designed for any purpose but to keep stray animals out of the courtyard.  As it has been split asunder, it no longer serves even that purpose."
	place "Between the Rubble"
	component
	syn "walls"
	syn "wall"
}

Player
{
	name "Tsiale"
	describe ""
	gender f
	thing "oldlocation" "Mansion Four Poster Bed"
	int "painting looks" 4
	
	persistable "clothing left foot" "twisted.reality.Stack" val "thing pair of black leather shoes\n" key "twisted.reality.Stack@5852154"
	
	persistable "clothing right foot" "twisted.reality.Stack" val "thing pair of black leather shoes\n" key "twisted.reality.Stack@585211e"
	
	persistable "clothing left leg" "twisted.reality.Stack" val "thing pair of black pants\n" key "twisted.reality.Stack@58520e3"
	
	persistable "clothing right leg" "twisted.reality.Stack" val "thing pair of black pants\n" key "twisted.reality.Stack@5852102"
	
	persistable "clothing chest" "twisted.reality.Stack" val "thing green silk shirt\n" key "twisted.reality.Stack@58520c7"
	
	persistable "clothing left arm" "twisted.reality.Stack" val "thing green silk shirt\n" key "twisted.reality.Stack@585208c"
	
	persistable "clothing right arm" "twisted.reality.Stack" val "thing green silk shirt\n" key "twisted.reality.Stack@58520ac"
	descript "clothing" {Pronoun Of("Tsiale"), " is wearing ", Name of("green silk shirt"), ", ", "black leggings", ", ", "and ", Name of("pair of black leather shoes"), "."}
	extends "Class_Human"
	architect
	passwd "TsqtVb4bTXUxs"
}

Room
{
	name "Back Lawn(1)"
	describe "A Back Lawn looking as if it needs to be described."
	place "Inheritance"
	theme "leaf"
	exit "east" to "Back Lawn(7)"
	exit "west" to "Back Lawn(3)"
	exit "south" to "Back Lawn"
}

Room
{
	name "Catwalk"
	describe "This is a catwalk overlooking a long-abandoned factory from far above.  The shape of this room is interesting.  It is almost completely cubical, except that the southern wall is concave.  This wall has windows at its top, overlooking the work area, and a line of doors along the bottom.  Aside from the equipment on the floor and this one irregular wall, the room is completely featureless.  There is a door to your southwest, leading into the southern wall of the factory.  There was probably once a portal to the east, there is a large rock lodged in the wall where the door may have been."
	exit "north" to "End of Catwalk"
	exit "southwest" to "Even More Office Hallway"
}

Room
{
	name "New Jersey Apartment Guest Room"
	describe "A bare, empty room, with a hardwood floor, and two unshaded windows, in the east and south walls, respectively. A pile of boxes are stacked against the east wall, filled with books and computer paraphenalia, but they do little to add a sense of presence to the room.\n"
	theme "default"
	exit "west" to "New Jersey Apartment Hallway"
}

Location
{
	name "Blake's Sphere of Stuff"
	describe "About one foot across, this steel sphere looks as if it is meant to hold things. Part of the sphere is hinged, to open and close. The words \"Blake's Sphere of Stuff\" are stenciled on it."
	place "Blake"
	feature "twisted.reality.plugin.Put"
	syn "box"
	syn "sphere"
}

Room
{
	name "Temple Northern Hallway"
	describe "This is a well-lit hallway with an arched ceiling. Illumination comes from an unknown source behind the walls and reflects downward off of the light stone ceiling. Two doors to your left and right are boarded over, and the hallway opens up to the north and south."
	theme "default"
	string "name" "Northern Hallway"
	exit "south" to "Temple Bottom Floor"
	exit "north" to "Temple Entrance Room"
}

Thing
{
	name "brass label"
	describe "A tiny, engraved brass plaque, identical to all of the other tiny engraved brass plaques attached to their respective potted plants, bearing the legend:\n\n     \"Artificial Potted Plant (Model 86003)\"\n  \t     \"Copywright 1793 GUE\"\n\"Frobozz Magic Artificial Potted Plant Company\"\n\t"
	place "Twisted Reality Corporate Demo Center"
	feature "twisted.reality.plugin.ReadLook"
	component
	syn "brass labels"
	syn "labels"
	syn "label"
}

Room
{
	name "Demo"
	describe "A funny box."
}

Room
{
	name "Science and Technology Vehicle Area"
	describe "A large, perfectly cubical, empty room. It looks suspiciously unfinished, as though the person or persons responsible for designing the demo center had taken a coffee break before completing it. A large black box is set against one wall, and a large glass box stands across from it."
	place "Demo"
	exit "north" to "Science And Technology Demo Center"
}

Room
{
	name "Side Lawn(2)"
	describe "You are at the eastern corner of a darkened old mansion. The nearby forest has begun to grow in over the lawn, and the branches of the closest trees almost touch the eastern wall, leaving a narrow path along the side of the mansion to the north. The lawn continues along the front of the mansion to the east, towards the front door, and to the south, where it gives way to the yellowed remains of a cornfield."
	place "Inheritance"
	theme "leaf"
	string "name" "Front Lawn"
	exit "west" to "Front Lawn(1)"
	exit "south" to "Front Lawn"
	exit "north" to "Side Lawn(1)"
}

Location
{
	name "demo center gift shop racks"
	describe "There are several large standing racks here, built from black metal wire and designed to rotate freely when spun."
	place "Demo Center Gift Shop"
	feature "twisted.reality.plugin.Put"
	string "name" "rack"
	component
	syn "racks"
	syn "rack"
	broadcast
}

Thing
{
	name "fountain water"
	describe "A jet of vool, clear, refreshing water. Ah, water, bringer of life..."
	place "demo center drinking fountain"
	feature "demo.WaterDrink"
	component
	syn "spurt"
	syn "jet"
	syn "water"
}

Thing
{
	name "Silver Cube"
	describe "A white box."
	place "Silver Room"
	extends "Class_Cube"
	component
	syn "cube"
}

Thing
{
	name "small brass key"
	describe "A small brass key with a delicately polished hexagonal tip. "
	place "green leather book"
	feature "demo.BrassWind"
	thing "repop" "green leather book"
	syn "brass key"
	syn "key"
}

Thing
{
	name "Class_Clothing"
	describe "A white box."
	place "Clothing Box"
	feature "twisted.reality.plugin.clothes.WearRemove"
}

Thing
{
	name "clue paddle"
	describe "Row, row, row your boat. The paddle has the letters N and Z etched into the blade."
	place "Garden Maze(4)"
	string "name" "paddle"
	component
	syn "paddle"
}

Location
{
	name "wood-buring stove"
	describe "A blue box."
	syn "wood stove"
	syn "stove"
}

Room
{
	name "North of House"
	describe "You are facing the north side of a white house. There is no door here, and all the windows are boarded up. To the north a narrow path winds through the trees."
	exit "southeast" to "Behind House"
	exit "southwest" to "West of House"
}

Thing
{
	name "Wooden Pencil"
	describe "A delicate faery wand."
	place "Tsiale"
	extends "Reality Pencil"
	syn "pencil"
}

Thing
{
	name "ring bell sign"
	describe "The sign reads:\n\n\"RING BELL FOR SERVICE.\""
	place "teakwood podium"
	string "name" "small white sign"
	component
	syn "small sign"
	syn "sign"
	syn "white sign"
	syn "small white sign"
}

Thing
{
	name "rusting silver inkwell"
	describe "A white box."
	place "Twin"
}

Room
{
	name "Demo Center Bathroom Stall"
	describe "A small bathroom stall, lined with light grey tiles. A large, gleamingly white and unnecessarily complicated-looking toilet is set into the center of the floor, next to a toilet paper dispenser that has been attached to the wall."
	place "Demo"
	descript "demo center bathroom stall door openDesc" "The stall door stands open, leading out into the bathroom."
	exit "west" to "Demo Center Lavatory" with "demo center bathroom stall door"
}

Thing
{
	name "demo center bathroom sink"
	describe "A small white ceramic basin, topped with a single unlabled knob and a polished metal faucet."
	place "Demo Center Lavatory"
	feature "demo.DemoKnobTurn"
	string "name" "sink"
	int "degree" 0
	component
	syn "sink"
	syn "white sink"
	syn "small white sink"
	syn "knob"
	syn "knob left"
	syn "knob right"
	syn "unlabeled knob"
}

Room
{
	name "Jedin's Foyer"
	describe "A Jedin's Foyer looking as if it needs to be described."
	descript "solid oak door openDesc" "To the east, you see a large, marble room with a pedestal in its center, to which is chained a large book."
	exit "north" to "coat closet"
	exit "west" to "Grand History Book Room" with "solid oak door"
}

Room
{
	name "HC Magic Board Landing"
	describe "This is a landing on which there is a large black screen upon which are displayed three anouncements. They are illegible, although one seems to allude to an event called \"build your own hippie\". To your west there is the libary, to the east the airport lounge. There are stairs downward from here, to the south."
	exit "down" to "HC Library Landing"
	exit "east" to "Airport Lounge"
	exit "west" to "HC Library"
}

Thing
{
	name "oil can"
	describe "A small brass can fitted with a long, thin nozzle, and a crudely bent piece of metal which was probably intended to be used as a handle."
	place "Mansion Maintenance Closet"
	syn "can"
}

Thing
{
	name "loose-leaf document"
	describe "A loose collection of pages printed out on a dot matrix printer with a fading ink cartridge. The pages are held together by a series of clips, and appear to deal with tax law, especially unilateral trade assertions in multi-national businesses."
	place "Damien's Study"
	syn "loose"
	syn "loose-leaf"
	syn "loose leaf"
	syn "document"
}

Room
{
	name "East Wing Spiral Staircase Top"
	describe "This is the top of a walled white marble spiral staircase.  There is a small open archway here to the northwest, with the word \"Offices\" engraved above it."
	string "name" "Spiral Staircase"
	exit "down" to "East Wing Spiral Staircase Bottom"
	exit "northwest" to "Observation Hallway"
}

Thing
{
	name "old wooden door"
	describe "An old, weathered looking door made of dark, greyish wood, mounted in a doorframe of the same material. A brass knob is set into the door at waist level, worn and dented in a few places but still appearing to have been polished recently."
	place "Mansion Study"
	theme "default"
	feature "divunal.tenth.OldWoodenDoorEnter"
	thing "target door" "old wooden doorframe"
	syn "wooden door"
	syn "door"
	syn "knob"
	syn "brass knob"
}

Location
{
	name "demo center drinking fountain"
	describe "It appears to be a demo center drinking fountain, but it is vague, indistinct, and little more than a blurry smear on reality. A small \"Out of Order\" sign has been hung haphazardly off one side."
	place "Demo Center West Wing"
	feature "demo.FountainDrink"
	feature "demo.FountainPush"
	thing "water" "fountain water"
	string "name" "drinking fountain"
	handler "startup" "demo.WaterOff"
	component
	syn "fount"
	syn "drinking fountain"
	syn "fountain"
	broadcast
}

Room
{
	name "Side Lawn(1)"
	describe "A narrow path between the thick overgrowth  of the forest and the rotting wooden walls of the mansion. It leads south to the front lawn, and continues towards a similar clearing to the north."
	place "Inheritance"
	theme "leaf"
	string "name" "Side Lawn"
	exit "south" to "Side Lawn(2)"
	exit "north" to "Side Lawn"
}

Thing
{
	name "Wooden Archway"
	describe "A simple wooden archway.  This appears to be a magical gate of some kind, as no tunnel is visible behind it, but you can see a forest setting clearly though it."
	component
	syn "archway"
}

Room
{
	name "Outer Tea Garden"
	describe "You are in a traditional tea garden. A central gate separates this outer garden from the inner garden. The low gate forces even highly-ranked guests to stoop low, reminding them to discard all thoughts of their worldly status upon entering the tea garden. This area is surrounded by a wrought-iron fence."
	theme "leaf"
	string "name" "Soto-rojj"
	exit "west" to "Garden Maze"
	exit "east" to "Ivy Garden"
	exit "north" to "Inner Garden" with "naka-mon"
}

Room
{
	name "Living Room"
	describe "You are in the living room. There is a doorway to the east, a wooden door with strange gothic lettering to the west, which appears to be nailed shut, a trophy case, and a large oriental rug in the center of the room."
	exit "east" to "Kitchen(1)"
}

Room
{
	name "Wrecked Street, wall"
	describe "This is a nondescript cuved street, which looks as if thousands of small rocks had bombarded it at high velocity, leaving pockmarks.  There is a huge grey stone wall in the middle of the road to the northwest, as well as what looks like the ruins of a school-building to the northeast.  A sign that says \"bakery\" overhangs the building to the southwest."
	theme "crack"
	string "name" "Wrecked Street"
	exit "southwest" to "Empty Bakery"
	exit "northeast" to "Divu'en School Entranceway"
	exit "southeast" to "Wrecked Street, curve"
}

Thing
{
	name "stones"
	describe "These small stones form the pathways that go through the garden. You should only walk on these, not the finely cared-for grass."
	place "Inner Garden"
	component
}

Thing
{
	name "bauble"
	describe "A small, shiny object, that catches the light and gleams in a rather valuable looking sort of way. "
	mood "providing light"
	place "demo register drawer"
	boolean "frotzed" true
	boolean "isLit" true
	descript "lighting" {"A pure white glow eminates from ", Name of("bauble"), ", bathing ", Pronoun of("bauble"), " in light."}
}

Thing
{
	name "blueprints"
	describe "A disordered pile of blue drafting paper covered in unintelligible handwriting and illustrations. Most of the text seems to be in an odd scientific notation, while the illustrations focus on a complex, interconnected system of gears and clockwork. A few pages are devoted to listing the dimensions of various gears, wheels, and rods, and one particularly long sheet is covered in a fantastically complicated set of tables and boxes, all filled with strange three-character sequences of letters and numbers."
	place "Mansion Maintenance Closet"
	component
	syn "blueprint"
}

Room
{
	name "Guyute's Laboratory"
	describe "A large stone-walled room. It looks as if someone has been hard at work here. Over on the north wall is a stone workbench, while on the south wall is a large bookshelf. In the southeast corner, surprisingly, is a sofa. The most prominent item in the room, however, is a great black cauldron;  each burp and bubble releases a fine mist, which fills the room. A set of rickety metal stairs leads up. To the west is a stone doorway."
	theme "greystone"
	exit "up" to "Smoking Room"
	exit "west" to "Cold Room"
}

Thing
{
	name "gate"
	describe "Apparently, this was an attempt to ensure that no law-abiding car-driver should drive to the Library. Between two sturdy wooden posts rests a flimsy, plastic chain. IT is attached to the post with a large padlock, but would be easy enough to break. Especially with a car."
	place "Intersection"
	component
}

Thing
{
	name "stairway"
	describe "This crumbling stairway seems to be all that of this building that has survived."
	place "Wrecked Street, curve"
	component
	syn "stairs"
}

Room
{
	name "Small Arched Tunnel"
	describe "This tunnel is carved in the shape of a perfect arch. The walls are solid granite.  It continues north and south."
	theme "greystone"
	exit "north" to "Doorway Room"
	exit "south" to "Armory"
}

Location
{
	name "Other Box"
	describe "A perfectly white box labeled \"Other Classes\" in neat black letters."
	place "Class Room"
	feature "twisted.reality.plugin.Put"
	syn "box"
	broadcast
}

Thing
{
	name "dented bullet"
	describe "It appears to be a dented bullet, but it is vague, indistinct, and little more than a blurry smear on reality."
	place "Colt 1911 pistol clip"
	string "bullet type" ".45 ACP"
	syn "bullet"
}

Location
{
	name "quantum singularity"
	describe "A blue box."
	place "Messy New Jersey Office"
	feature "twisted.reality.plugin.Put"
	component
	syn "singularity"
	shut
}

Thing
{
	name "clue apple tree"
	describe "The few apples that remain on this tree are rotten and putrid-looking. In fact, this whole tree looks sickly, including its scrawny trunk."
	place "Garden Maze(5)"
	string "name" "apple tree"
	component
	syn "apple tree"
	syn "tree"
}

Location
{
	name "great bookshelf"
	describe "This bookshelf is filled with all sorts of mysterious-looking books. Each shelf seems to have its own category, indicated by a dirty brass plaque. \"Spells and Hexes\", \"Astrology\", \"Myths and Legends\" and \"Ancient Mystical Ceremony\" are all packed with aging tomes. The section marked \"General Magic\" catches your eye."
	place "Guyute's Laboratory"
	extends "Class_Container"
	component
	syn "bookshelf"
}

Thing
{
	name "dark blue loose silk shirt"
	describe "A white box."
	place "Agatha"
	syn "silk shirt"
	syn "shirt"
}

Room
{
	name "Open Space"
	describe "null"
	exit "south" to "Cold Floor"
}

Thing
{
	name "flower"
	describe "This is a rose, it has not been watered recently and is close to dying.\n"
	component
}

Player
{
	name "Brasswheel"
	describe "Several concentric hoops of polished brass, each spinning rapidly on it's own independant axis and surrounded by a more stationary spherical framework of the same material."
	mood "floating in the air"
	thing "oldlocation" "Demo Information Center"
	int "painting looks" -3
	string "name" "brass gyroscope"
	descript "floating" "It is suspended in the air at about chest level by some incomprehensible force."
	extends "Class_Human"
	syn "brass gyroscope"
	syn "gyro"
	syn "gyroscope"
	ability "divunal.common.author.Twin"
	passwd "brIZWIEEUJfbg"
}

Room
{
	name "Intersection"
	describe "The pathway intersects a road here, although there is very little traffic to worry about. To the north the path continues into the forrest, and the road goes both east and west from here. There is a large field to the west, on the other side of the road, and the markings of many feet have cut a path through it, to the northwest. There is a gate here."
	exit "northwest" to "The Middle of the Field"
	exit "south" to "Path beside the RCC"
}

Room
{
	name "A Small Dark Crevice"
	describe "It is dark and damp in this crevice, with barely enough room to stand straight.  Some strange material glistens on the walls... looking further on you see the narrow passageway continue into the shadows.  Along the wall is a message nailed to it."
	theme "greystone"
	string "name" "A Dark Place"
	string "description" "It's too dark in here to see!"
	boolean "inhibit_exits" true
	boolean "inhibit_items" true
	extends "Class_Dark Room"
	opaque
	shut
	exit "south" to "A Dark Narrow Passage"
	exit "north" to "Deeper In The Rock"
	claustrophobic
}

Thing
{
	name "demo center monitor"
	describe "A large Macintosh monitor with a Winny The Pooh sticker attached to the case just above the power button. Someone has covered Winny's head with a semitransparent \"Powered By RedHat\" sticker, giving him a dark, brooding, and disproportionately large white head. In the background, a screensaver is tracing out some trippy mathematical figures, and"
	place "Messy New Jersey Office"
	string "name" "monitor"
	descript "screen" "an \"Enter Password:\" window is open in the center of the screen, displaying an empty password field."
	component
	syn "screen"
	syn "trippy screensaver"
	syn "screensaver"
	syn "monitor"
}

Thing
{
	name "Ornate Grandfather Clock"
	describe "A tall, intricately carved grandfather clock, embossed with unusual carvings and symbols. The base of the clock is framed in glass, where three brass weights hang motionlessly behind a large circular pendulum. The face of the clock is a white marble disk set with gilded roman numerals, and a surrounded by a narrow ring painted with the various phases of the moon. Judging from the position of the hands and the position of the ring, it is about "
	place "Chateau Antechamber"
	long "init time" 946431235335
	string "after time string" ", and a new moon as well."
	
	property "description" "inheritance.clock.ClockLook"
	handler "startup" "inheritance.clock.ClockStart"
	syn "clock"
	syn "grandfather clock"
}

Room
{
	name "RCC Entrance Hall"
	describe "You're standing in a glass entranceway surrounded on three sides by doors."
	exit "south" to "Front of RCC"
	exit "west" to "Under Walkway"
	exit "north" to "RCC Reception Desk"
}

Thing
{
	name "demo cash register"
	describe "A smooth, sleek, ergonomic grey plastic lump, with a small green lcd display reading \"Out of Service\" at the top, and a small keypad at the bottom."
	place "Demo Center Gift Shop"
	feature "demo.DemoRegisterType"
	thing "drawer" "demo register drawer"
	string "name" "cash register"
	component
	syn "cash register"
	syn "register"
	syn "keypad"
	syn "small numeric keypad"
	syn "pad"
}

Location
{
	name "teakwood podium"
	describe "An elegant teakwood podium. There's a small sign here."
	place "Underground Grotto"
	feature "twisted.reality.plugin.Put"
	string "preposition" "on"
	component
	syn "podium"
	broadcast
}

Room
{
	name "Rare Book Room, Lower Level"
	describe "This is the lower level of the Rare Book room of a bookstore, as a sign hanging from the ceiling indicates.  There are many books here and they all appear well cared-for. There is a passageway to the northeast leading to a slightly less-used corner of the room. A rickety metal spiral staircase leads upward."
	theme "paper"
	exit "up" to "Rare Book Room, Upper Level"
	exit "northeast" to "Obscure Corner of Bookstore"
}

Thing
{
	name "colt 1911 pistol trigger"
	describe "It appears to be a colt 1911 pistol trigger, but it is vague, indistinct, and little more than a blurry smear on reality."
	place "Colt 1911 Semi-Auto"
	string "name" "trigger"
	component
	syn "trigger"
}

Room
{
	name "another test room"
	describe "Another room full of jello."
}

Room
{
	name "Damien's Bedroom"
	describe "You feel as though you have stepped into a giant metal ping-pong ball. Everything is gun metal grey, the room is spherical and there are no hard edges in sight. It looks as though someone has hollowed out a metal ball bearing and made it his home. In the center of the room is a white cot with a few blankets on it. You see nothing else here.\n\nIn what looks like another new addition, there is a round pathway made of the same organic threads leading off to the west."
	exit "west" to "Damien's Study"
	exit "east" to "Damien's Office,leaving"
}

Room
{
	name "Trans-Dimensional Time Warp"
	describe "You are in a void.  This room is thermodynamically impossible - and yet it exists.   I wonder why?  You cannot see any direction clearly, but nothing blocks your path."
	theme "weird"
	exit "south" to "Silver Shadowed Flowers"
	exit "down" to "Trans-Dimensional Time Warp"
	exit "up" to "Trans-Dimensional Time Warp"
	exit "east" to "Trans-Dimensional Time Warp"
	exit "southeast" to "Trans-Dimensional Time Warp"
	exit "southwest" to "Trans-Dimensional Time Warp"
	exit "west" to "Trans-Dimensional Time Warp"
	exit "northeast" to "Trans-Dimensional Time Warp"
	exit "north" to "Trans-Dimensional Time Warp"
	exit "northwest" to "Silver Shadowed Glade"
}

Room
{
	name "Another Junction"
	describe "Here is another multidirectional fork in the concrete path snaking through the hampshire lawns.  You can continue south to an ivy-covered building, or west toward the edge of a forest."
	exit "west" to "Boring East-West Path"
	exit "northwest" to "Scenic Junction"
}

Room
{
	name "Rough Corridor"
	describe "null"
	exit "back" to "Rough Floor"
}

Thing
{
	name "Divunal t-shirt"
	describe "A white t-shirt, almost exactly the right size for a generic guest person. It is emblazoned with the image of a yellowed piece of parchment, upon which the word \"Divunal\" has been written in flowing script. Below the image, in much smaller letters, is the phrase \"Less graphics, more game\" and a small blue Twisted Reality logo."
	place "demo center gift shop racks"
	thing "repop" "demo center gift shop racks"
	string "clothing appearance" "a Divunal t-shirt"
	extends "Class_Shirt"
	syn "t-shirt"
	syn "shirt"
	syn "divunal shirt"
	syn "t shirt"
	syn "t"
	syn "divunal"
}

Room
{
	name "Closed Junction"
	describe "This is a huge hemi-spherical metal room.  The room is well illuminated, seemingly from nowhere.  There are tunnels branching off in several directions, but most of them look as if they were pinched shut by rocks.  One remains open to the north, and there is a tunnel larger than all the rest leading east."
	exit "east" to "Very Cold Room"
	exit "north" to "Dent in Tube"
}

Thing
{
	name "analog clock"
	describe "On the wall is a small, white analog clock. It is round, with thick black hands. It appears to be three minutes fast, but there is no readily obvious way to set it to the correct time.\n\nThe minute hand is silver underneath the black paint, a few flakes of paint have begun to flake off. A few centimeters below the center of the clock the word Seiko is written, and underneat it, Quartz.\n\nThe clock has a small silver border."
	place "Damien's Cubicle"
	component
	syn "clock"
}

Thing
{
	name "candelabra"
	describe "This is an ancient candelabra which appears to have been brushed completely free of cobwebs. You can see fingerprints on its surface, which looks to be brass."
	place "Crumbling Hallway"
	component
	syn "candles"
	syn "candelabraas"
	syn "candelabras"
}

Thing
{
	name "Ruby Cube"
	describe "A cube composed from something quite like ruby.  Through its translucent surface, though, you can see lights like stars, slowly growing and diminishing and intensity."
	place "Ruby Room"
	extends "Class_Cube"
	component
	syn "cube"
}

Room
{
	name "Deeper In The Rock"
	describe "This room is unusually dark and silent."
	theme "greystone"
	string "name" "A Dark Place"
	string "description" "It's too dark in here to see!"
	extends "Class_Dark Room"
	opaque
	shut
	exit "south" to "A Small Dark Crevice"
	exit "north" to "Secret Cave"
	claustrophobic
}

Thing
{
	name "upper ladder"
	describe "This is the upper half of a wooden ladder which leads downward to a lower and wider ledge."
	place "Very Narrow Rocky Ledge"
	component
	syn "ladder"
}

Thing
{
	name "small gear"
	describe "A thin metal disc, about as big around as the palm of your hand, edged with evenly spaced protrusions."
	place "Mansion Maintenance Closet"
	syn "gear"
}

Location
{
	name "demo center coffee table"
	describe "A dark, polished wooden table, made of what appears to be solid oak.  A thin line of gold inlay traces a complicated, yet elegant, pattern around the edge of the table.  It is set between the high backed chairs."
	place "Demo Center Waiting Room"
	feature "twisted.reality.plugin.furniture.Stand"
	feature "twisted.reality.plugin.furniture.Sit"
	feature "twisted.reality.plugin.Put"
	string "name" "coffee table"
	string "player preposition" "sitting on"
	string "preposition" "on"
	int "maximum occupancy" 2
	component
	syn "coffee table"
	syn "table"
	broadcast
}

Thing
{
	name "verb list"
	describe "Verbs that were just allowed: Hug, Grin, Bite, Cackle, Fly, Grimace, Laugh, Frown, Gate, Chuckle, Poke, Sigh, Smirk"
}

Thing
{
	name "white silk cravat"
	describe "A long, thin piece of white silk, like a very light scarf."
	place "Tenth"
	string "tied descriptor" "It is worn around the neck like a scarf, but tied in front, with the remainder of the embroidered silk hanging somewhat like a tie. "
	string "untied descriptor" "It is untied, so as to be simply hung over the neck."
	string "tied appearance" "a neatly tied white silk cravat"
	string "untied appearance" "a white silk scarf"
	boolean "clothing worn" true
	boolean "tied" true
	string "clothing appearance" "a neatly tied white silk cravat"
	descript "tie descriptor" "It is worn around the neck like a scarf, but tied in front, with the remainder of the embroidered silk hanging somewhat like a tie. "
	extends "class_tie"
	component
	syn "silk cravat"
	syn "cravat"
	syn "scarf"
}

Room
{
	name "Great Underground Lake"
	describe "The shallow end of a great underground lake that extends into dark and deeper waters to the north. A small cave, partially filled with water, leads south."
	theme "greystone"
	exit "south" to "Mansion Basement Well"
}

Thing
{
	name "white button-down shirt"
	describe "An evenly-spaced row of small, white buttons fashioned from a semi-precious stone run down the front of this garment; two are placed higher for fastening the collar as well.   The buttons' matte finish blends smoothly with the soft, strong fabric.  You see no wrinkles on the shirt."
	place "Jedin"
	string "clothing appearance" "a white, button-down shirt and collar of a soft, durable fabric with the sleeves rolled up to just below his elbows"
	boolean "clothing worn" true
	extends "Class_Shirt"
	component
	syn "white shirt"
	syn "shirt"
}

Thing
{
	name "mailbox"
	describe "The mailbox is painted white to match the house. It is closed."
	place "Front Step of Darkness"
	component
}

Player
{
	name "Twin"
	describe "Although Twin's figure looks human, his presense feels somewhat supernatural. Only two things stand out about this otherwise shady character: a set of glowing eyes in the hood of his black cloak, and the sparkling silver rings ornamenting his fingers..."
	gender m
	thing "oldlocation" "Mansion West Ballroom"
	extends "Class_Human"
	architect
	passwd "TwmZOKhqj8jCg"
}

Room
{
	name "Guest Room"
	describe "A Guest Room looking as if it needs to be described."
	place "Inheritance"
	theme "dark"
	exit "south" to "Guest Bathroom"
	exit "east" to "Chateau Hallway(13)"
}

Thing
{
	name "skeleton"
	describe "Ugh! Though little can be determined by this pile of bones, a sense of dread is eminent. This poor creature must have just given up hope on finding a way out of this maze."
	place "Garden Maze(9)"
	component
}

Thing
{
	name "tenths bedroom doors"
	describe "A pair of large, dark brown wooden doors, each set with a polished brass handle."
	place "Mansion Upper Hallway"
	boolean "obstructed" false
	string "openDesc" "A pair of double doors stand open at the west end of the hallway."
	string "closeDesc" "To the west, the hallway ends in a large set of double doors."
	string "thereOpenDesc" "To the east, a long hallway is visible through a pair of open doors."
	string "thereCloseDesc" "A large set of double doors is set into the east wall."
	string "name" "double doors"
	extends "Class_Door"
	component
	syn "east door"
	syn "doors"
	syn "double doors"
	syn "west doors"
	syn "west door"
	syn "east doors"
}

Thing
{
	name "Class_Socks"
	describe "A white box."
	place "Clothing Box"
	extends "Class_Clothing"
}

Thing
{
	name "lower ladder"
	describe "This is the lower half of a wooden ladder which leads upwards to a higher, more narrow ledge."
	place "Small Platform on the Rock"
	component
	syn "ladder"
}

Room
{
	name "Anah's Room"
	describe "This room is very white - and depicts an interesting dichotomy.  On the west wall, there is a bed, sheeted completely in white linen, covered with an huge group of stuffed animals which spill over onto the floor.  On the wall to the east, there is a rack for edged weapons of all sorts.  The dominant feature of the room, however, is the southern wall, which is a huge, wide window overlooking a pine forest immediately after a snow storm.  The boughs of the trees are heavily laden with snow, and they glisten in the late sunlight."
	exit "north" to "Cylindrical Mansion Hallway"
}

Room
{
	name "Sylvan Sanctuary"
	describe "A peaceful, tranquil, and silent glade in a silver forest at night.  You can make out a rock wall with a door in it to the south, which is painted to look as though it is a part of the night sky, and to the north, you can enter the forest."
	theme "leaf"
	exit "north" to "Silver Shadowed Wood"
}

Room
{
	name "Science Fiction Room"
	describe "This is a room filled with books about strange worlds, fantastic technology, giant robots, and space travel.  While the books themselves are of the standard text-on-paper variety, the shelves are made of black, gleaming metal, and are mounted on a diabolically complicated system of tracks and sliders. There is also a series of small, tempting buttons mounted at eye level along the shelves. A simple wooden door leads southward back to more mundane surroundings. "
	theme "paper"
	thing "bookshelf door" "bookshelf door"
	exit "south" to "Bookstore Stairwell, Level 10"
	exit "north" notTo "Steam-Powered Library" with "bookshelf door"
}

Thing
{
	name "BusinessMind for Jewelers poster"
	describe "A large poster of Rodin's \"The Thinker\" sculpture, surrounded by a red and yellow background. It is covered with information about a piece of database software called BusinessMind for Jewelers, and invites you to www.businessmind.com, where you can find more information on \"Business Software that thinks the way you do\"."
	place "Messy New Jersey Office"
	component
	syn "red and white poster"
	syn "poster"
}

Room
{
	name "Mod Lawn"
	describe "This is the combined lawn of the two large, round buildings on either side of it. There is a door to the east, but it is closed. There is also a glass door to the west."
	exit "west" to "Mod Seven"
	exit "south" to "Pathway"
}

Thing
{
	name "demo center toilet placard"
	describe "A tiny white cardboard square, propped up for easy reference and covered in flowing black script which reads:\n\n    \"Motion Sensitive Zero Gravity Toilet\"\n\t   \"Copywright 1798 GUE\"\n\"Frobozz Magic Zero Gravity Toilet Company\"\n\n    \"The staff of the Frobozz Magic Zero Gravity Toilet company thanks you for your purchase. The Model Zero HPZGT is truly superior to the standard Magic Toilet line, and, as the name implies, is designed for ease of use and can operate in many conditions that would render a normal toilet useless... We pride ourselves on catering to the distinguishing toilet owner, and we hope to enjoy your patronage in the future.\""
	place "Demo Center Bathroom Stall"
	feature "twisted.reality.plugin.ReadLook"
	string "name" "small white placard"
	component
	syn "toilet placard"
	syn "placard"
	syn "card"
}

Room
{
	name "Mansion Maintenance Closet"
	describe "A small, cubical, unfinished wooden room, roughly ten feet on each side. The walls are postered with obscure technical diagrams, and there are a number of wooden crates scattered randomly across the floor. A simple wooden table is set against the wall opposite the door, covered with random stacks of blueprints."
	theme "wood"
	exit "northwest" to "Mansion Main Hall"
}

Room
{
	name "Chateau Sitting Room"
	describe "A Chateau Sitting Room looking as if it needs to be described."
	place "Inheritance"
	theme "greystone"
	exit "south" to "Chateau Hallway(16)"
	exit "north" to "Chateau Hallway(3)"
}

Room
{
	name "Mansion Basement"
	describe "A dimly lit chamber with greyish stone walls. In the center of the room, a massive wrought iron spiral staircase descends from the ceiling, leading upwards to a much brighter area. Crude doorways cut into the east and west walls lead into darkness. "
	theme "greystone"
	exit "east" to "Mansion Basement Engine Room"
	exit "west" to "Mansion Basement Storeroom"
	exit "up" to "Mansion Stairwell"
}

Thing
{
	name "brown kimono"
	describe "A rather nondescript brown kimono."
	place "Rikyu"
	boolean "clothing worn" true
	extends "Class_Tunic"
	component
	syn "kimono"
}

Location
{
	name "Large Black Box"
	describe "A large, black metal box with a hinged top."
	place "Science and Technology Vehicle Area"
	feature "twisted.reality.plugin.OpenCloseContainer"
	feature "twisted.reality.plugin.Put"
	string "open description" "It is currently open."
	string "closed description" "It is currently closed."
	string "name" "black box"
	descript "open/close" "It is currently open."
	component
	syn "black metal box"
	syn "black"
	syn "black box"
	syn "box"
}

Location
{
	name "Book Box"
	describe "A perfectly white box labeled \"Book Classes\" in neat black letters."
	place "Class Room"
	feature "twisted.reality.plugin.Put"
	syn "box"
}

Thing
{
	name "seventh knob"
	describe "Seventh knob from the top of the qin with which to tune the instrument."
	place "qin"
	component
	syn "knob7"
	syn "knob"
}

Thing
{
	name "rainbow trout"
	describe "Looks like a rainbow trout. About seven inches long, way too small. It would probably be best to find a body of water to put it in."
	place "recycle bin"
	syn "fish"
}

Room
{
	name "Chateau Basement(5)"
	describe "A Chateau Basement looking as if it needs to be described."
	place "Inheritance"
	theme "greystone"
	string "name" "Chateau Basement"
	exit "up" to "Chateau Stairwell"
	exit "south" to "Chateau Basement"
}

Room
{
	name "Chateau Basement(4)"
	describe "A Chateau Basement looking as if it needs to be described."
	place "Inheritance"
	theme "greystone"
	string "name" "Chateau Basement"
	exit "south" to "Chateau Basement(3)"
}

Room
{
	name "Chateau Basement(3)"
	describe "A Chateau Basement looking as if it needs to be described."
	place "Inheritance"
	theme "greystone"
	string "name" "Chateau Basement"
	exit "north" to "Chateau Basement(4)"
	exit "east" to "Chateau Basement"
}

Room
{
	name "Chateau Basement(2)"
	describe "A Chateau Basement looking as if it needs to be described."
	place "Inheritance"
	theme "greystone"
	string "name" "Chateau Basement"
	exit "south" to "Chateau Basement(1)"
}

Room
{
	name "Chateau Basement(1)"
	describe "A Chateau Basement looking as if it needs to be described."
	place "Inheritance"
	theme "greystone"
	string "name" "Chateau Basement"
	exit "north" to "Chateau Basement(2)"
	exit "west" to "Chateau Basement"
}

Thing
{
	name "carved bit pipe"
	describe "A rather nondescript carved bit pipe."
	place "Rikyu"
	extends "Class_Smokeable"
	syn "bit pipe"
	syn "carved pipe"
	syn "pipe"
}

Room
{
	name "Emerald Room"
	describe "This room is a study in green.  While you can make out no light source, light must be filtering in through the emerald ceiling to get down here, where it reflects off of the myriad facets of the room's walls and floor.  There are no markings anywhere, and the only real feature of the room is a cube, which appears to be part of the floor, made of the same emerald substance that composes the rest of the room, but glittering more brightly."
	exit "west" to "Jewel Bedecked Hallway"
}

Thing
{
	name "clue chair"
	describe "This chair is rickety and weathered. It might be a good resting place for a weary maze-dweller, but that could be misleading. Painted on the seat is the phrase \"A.M. Furniture Co.\""
	place "Garden Maze(4)"
	string "name" "chair"
	component
	syn "chair"
}

Thing
{
	name "stuffed Tux the Penguin"
	describe "A soft, stuffed figurine of a flightless bird with black and white plumage, proudly wearing a \"Linux Power\" pin on it's chest."
	place "dark green overcoat"
	syn "penguin"
	syn "tux"
	syn "tux the penguin"
}

Thing
{
	name "Class_Dark Room"
	describe "A small black box."
	place "Room Box"
	string "darkDescription" "It's too dark in here to see!"
	
	property "isLit" "divunal.common.IsLit"
	handler "toss" "divunal.common.DarkCheck"
	handler "grab" "divunal.common.DarkCheck"
	handler "leave" "divunal.common.DarkCheck"
	handler "enter" "divunal.common.DarkCheck"
	handler "darkcheck" "divunal.common.DarkCheck"
}

Thing
{
	name "sword +1"
	describe "This is a sword of slightly above-average quality.  You notice that the craftsmanship, while not excellent, is good enough to be impressive.  It appears to have been carefully honed to do just a little bit more damage than another, similar, but less above-average sword would do.  Its blade has a flat, pseudo-silvery texture, and the hilt is made of what appears to be a low-grade stainless steel."
	mood "providing light"
	place "James"
	boolean "isLit" true
	boolean "frotzed" true
	descript "lighting" {"A pure white glow eminates from ", Name of("sword +1"), ", bathing ", Pronoun of("sword +1"), " in light."}
	syn "sword"
}

Room
{
	name "End of Rainbow"
	describe "You are on a small, rocky beach on the continuation of the Frigid River past the Falls. The beach is narrow due to the presence of the White Cliffs. The river canyon opens here and sunlight shines in from above. A rainbow crosses over the falls to the east and a narrow path continues to the southwest."
	exit "southwest" to "Canyon Bottom"
}

Room
{
	name "Forest 3"
	describe "The forest thins out, revealing impassable mountains."
	string "name" "Forest"
	exit "south" to "Forest 2"
	exit "north" to "Forest 2"
	exit "west" to "Forest 2"
}

Room
{
	name "Forest 2"
	describe "This is a dimly lit forest, with large trees all around."
	string "name" "Forest"
	exit "north" to "Clearing 2"
	exit "east" to "Forest 3"
	exit "south" to "Clearing"
	exit "west" to "Forest Path"
}

Room
{
	name "Class Room"
	describe "A room with lots of generic, basic looking objects lying about.  The walls are whitewashed and it is entirely nondescript."
	theme "default"
	exit "southwest" to "Small Gray Dome"
	exit "south" to "Test Bed"
	exit "north" to "Genetic Laboratory"
	exit "up" to "Small Book Room"
	exit "west" to "Grey Cube Room"
}

Room
{
	name "Front Lawn"
	describe "The mansion's unkempt lawn surrenders to the yellowed remains of a cornfield to the south, and a dense bordering forest to the east. The tall grass of the lawn continues to the west, towards the mansion's gravel drive, and north, towards the mansion itself."
	place "Inheritance"
	theme "leaf"
	string "name" "Front Lawn"
	exit "west" to "Front Lawn(2)"
	exit "north" to "Side Lawn(2)"
}

Room
{
	name "Help Desk"
	describe "This is a customer service and help desk in a bookstore. There are a few racks which look like they could accomodate paperbacks here which are currently empty. There is also a rickety metal spiral staircase which ascends to the entrance hallway. A passageway to the southwest affords you access to the greater body of this level, where most books are stored."
	theme "paper"
	exit "up" to "Small Bookstore Entrance"
	exit "southwest" to "Main Aisle, East End"
}

Thing
{
	name "Mansion Basement Pump"
	describe "A large metal box, bolted to a set of stone blocks that suspend it over the well dug into the floor. A cylindrical object extends from the bottom of the pump into the water, and it is connected to the machinery on the west side of the room by a number of large tubes and hoses."
	place "Mansion Basement Pump Area"
	feature "twisted.reality.author.Obstruct"
	boolean "obstructed" true
	descript "pump action" " It is producing a rhythmic humming sound, and causing the water in the well below it to churn violently."
	component
	syn "pump"
	syn "basement pump"
}

Room
{
	name "Reception Area"
	describe "This area, though quiet, looks as if it were once bustling with activity.  It also looks as if it were rather heavily abused in its last few days of usefulness.  Most of the room is relatively undamaged, but there is a visible swath of destruction leading from the western door to the southern and eastern edges of the room.  There is a large granite desk here with many devices that look as if they might be used for communication bolted to it."
	exit "east" to "Office Hallway"
	exit "southeast" to "Other Underling's Office"
	exit "south" to "Broken Office"
	exit "north" to "Nice Office"
	exit "west" to "Cramped Transporter Booth"
}

Room
{
	name "Wrecked Street, curve"
	describe "This is a nondescript cuved street, which looks as if thousands of small rocks had bombarded it at high velocity, leaving pockmarks. To the east of you lies a foundation for what must have been one of the area's larger buildings. There is a stairway leading downward at the edge of the foundation, which looks as if it was once covered by a bulkhead door."
	theme "crack"
	string "name" "Wrecked Street"
	exit "down" to "A Crumbling Stairway"
	exit "northwest" to "Wrecked Street, wall"
	exit "southeast" to "Wrecked Street, corner"
}

Room
{
	name "Wrecked Street, corner"
	describe "This is a nondescript cuved street, which looks as if thousands of small rocks had bombarded it at high velocity, leaving pockmarks."
	theme "crack"
	string "name" "Wrecked Street"
	exit "northwest" to "Wrecked Street, curve"
	exit "south" to "Wrecked Street, north"
}

Thing
{
	name "first knob"
	describe "The first knob from the top of the qin."
	place "qin"
	component
	syn "knob1"
	syn "knob"
}

Thing
{
	name "clue table"
	describe "A rather nondescript clue table."
	place "Garden Maze(12)"
	string "name" "table"
	component
	syn "table"
}

Player
{
	name "Bob"
	describe "Bob is an incredible specimen of virile manhood, as powerful as he is senual, all at once the most beautiful and terrifying thing you have ever seen. If you are a woman, you are struck instantly by his obvious sexual potency and skill, and if you are a man, you cower as his cold and powerful gaze passes over you."
	gender m
	thing "oldlocation" "Demo Center East Wing"
	long "stamina time" 943948804325
	float "stamina" "-0.58383834"
	long "health time" 943948804325
	float "health" "1.0"
	boolean "isLit" false
	extends "Class_Player"
	passwd "Bo8AKlsFnZk/c"
}

Room
{
	name "Genetic Laboratory"
	describe "A perfectly square room with immaculately white walls and floors. The northern end of the room is filled with a large, complex machine, consisting of a bank of controls connected to a large transparent tube large enough for a person to stand comfortably inside, labeled \"Sterilized For Your Protection\"."
	theme "default"
	exit "south" to "Class Room"
}

Location
{
	name "Pedestal"
	describe "A dark, polished wooden pedestal."
	place "Tenth's Chamber"
	feature "twisted.reality.plugin.Put"
	string "preposition" "on"
	int "maximum occupancy" 1
	broadcast
}

Room
{
	name "Wrecked Street, south"
	describe "This is a nondescript cuved street, which looks as if thousands of small rocks had bombarded it at high velocity, leaving pockmarks.  A narrow path leads off to the west into the southern edge of the crater which holds the bookstore, and to the east is a pile of rubble which may once have been a house.  To the south there is a very steep, large crater which doesn't appear navigable."
	theme "crack"
	string "name" "Wrecked Street"
	exit "west" to "Crater Edge South"
	exit "east" to "Wrecked House Foundation"
	exit "north" to "Wrecked Street, bookstore"
}

Location
{
	name "construction frame"
	describe "A large interconnected framework of metal scaffolding, reaching up to the ceiling of the room."
	place "Mansion Laboratory"
	feature "twisted.reality.plugin.Put"
	component
	syn "frame"
	broadcast
}

Thing
{
	name "black and red postcard"
	describe "A small, worn, glossy postcard. The front side is a photograph of Colonial Williamsburg at night, lit by the time-lapsed glow of reddish yellow fireworks, and the back is covered in small, neat handwriting, and a cute drawing of a knight standing at attention."
	place "Other New Jersey Apartment Bedroom"
	syn "card"
	syn "postcard"
}

Room
{
	name "Ivy Garden"
	describe "This garden provides an extremely peaceful place to sit and meditate. A great oak tree is present in the northern part of this garden. To the southwest is a aisle of stone benches, at whose southwesternmost point is a large cement urn. The ground here is covered with ivy; only the walkways to and from the urn are clear enough to pass. It's also possible to climb the tree."
	theme "leaf"
	descript "door in oak tree openDesc" "There seems to be a door leading north into the tree."
	exit "north" to "Inside Oak Tree" with "door in oak tree"
	exit "up" to "Woodem Platform in Oak Tree"
	exit "west" to "Outer Tea Garden"
}

Room
{
	name "Mansion Grand Stair Balcony"
	describe "A spacious platform, bordered by a wrought iron railing. On either side, a pair of staircases lead downwards, eventually reaching a landing where they combine and change direction before continuing their descent. An arched doorway is set in the west wall, leading into a long hallway."
	theme "wood"
	exit "west" to "Mansion Upper Hall"
	exit "down" to "Mansion Grand Stair Landing"
}

Player
{
	name "Michael"
	describe "No Description."
	gender m
	thing "oldlocation" "Genetic Laboratory"
	extends "Class_Human"
	syn "mike"
	architect
	passwd "MipLxiM71e08c"
}

Room
{
	name "Mansion Grand Stair Landing"
	describe "The room leads up into a vast, broad staircase, set with a deep red carpet. The stairs lead up for some way, narrowing as they go, until they divide into two separate sets and change direction, continuing upwards. A massive archway in the west wall leads into a larger, darker room."
	theme "wood"
	exit "up" to "Mansion Grand Stair Balcony"
	exit "west" to "Mansion East Ballroom"
}

Thing
{
	name "can of Punt-B-Gone"
	describe "A white box."
}

Thing
{
	name "obelisk welcoming text"
	describe "Despite being in a large, white Times Roman font on a black background, you can't quite seem to make out what it says. Something along the lines of \"Welcome to our demonstration center, home of Twisted Matrix Enterprises...\" but after that, your eyes begin to glaze over. Jumbled, run-on sentences are twined with phrases like \"Enterprise Wide\", \"Networked Scalability\", and \"Multithreaded Dynamic Architecture\", which, while compelling, destroy any meaning the text may have had."
	place "Demo Information Center"
	feature "twisted.reality.plugin.ReadLook"
	component
	syn "welcoming text"
	syn "text"
	syn "piece of text"
	syn "large piece of text"
}

Room
{
	name "Castle Entrance"
	describe "This is a minimalistically decorated entrance hall with alabaster-white walls.  Black squares at uneven distances down the left wall punctuate an otherwise featureless room.  A soft, sourceless light illuminates the whole room.  A low doorway to the north leads out into a courtyard, and a small archway southward continues further into the palace's depths."
	theme "default"
	exit "south" to "Castle Foyer"
	exit "north" to "Castle Courtyard"
}

Room
{
	name "Country Road"
	describe "An old dirt road, leading off into the darkness to the east and west. It is bordered on the south side by a crumbling stone wall, while an opening in the trees to the north leads downhill to a gravel driveway."
	place "Inheritance"
	theme "leaf"
	exit "west" to "Country Road(3)"
	exit "east" to "Country Road(1)"
	exit "north" to "Driveway"
}

Location
{
	name "elegant straight-backed chair"
	describe "A rather nondescript Chippendale chair."
	place "Smoking Room"
	string "player preposition" "sitting in"
	string "preposition" "in"
	int "maximum occupancy" 1
	extends "Class_Sittable"
	syn "straight chair"
	syn "straight-backed chair"
	syn "elegant chair"
	broadcast
}

Room
{
	name "Chateau Pantry"
	describe "A Chateau Pantry looking as if it needs to be described."
	place "Inheritance"
	theme "greystone"
	exit "south" to "Chateau Stairwell"
	exit "north" to "Back Lawn"
	exit "east" to "Chateau Hallway(2)"
	exit "west" to "Chateau Kitchen"
}

Player
{
	name "Tenth"
	describe "A tall, slender young man, with bright green eyes and a calm, thoughtful face. His hair is an odd, coppery shade of blonde, and falls nearly to his waist in gentle waves."
	place "Demo Center West Wing"
	gender m
	theme "default"
	int "drinking problem" 6
	thing "oldlocation" "Demo Center Waiting Room"
	thing "teleport destination" "Demo Center Lavatory"
	boolean "pageable" true
	int "painting looks" -3
	
	persistable "clothing left eye" "twisted.reality.Stack" val "thing pair of brass framed spectacles\n" key "twisted.reality.Stack@5853fc8"
	
	persistable "clothing right eye" "twisted.reality.Stack" val "thing pair of brass framed spectacles\n" key "twisted.reality.Stack@5854038"
	
	persistable "clothing right ear" "twisted.reality.Stack" val "thing pair of brass framed spectacles\n" key "twisted.reality.Stack@58540ad"
	
	persistable "clothing left ear" "twisted.reality.Stack" val "thing pair of brass framed spectacles\n" key "twisted.reality.Stack@585406d"
	long "stamina time" 942018677034
	float "stamina" "-0.8790683"
	long "health time" 942018677035
	float "health" "1.0"
	float "dexterity" "0.2"
	float "glance" "0.2"
	
	persistable "clothing left leg" "twisted.reality.Stack" val "thing pair of green boxer shorts\nthing a pair of black slacks\n" key "twisted.reality.Stack@58541df"
	
	persistable "clothing right leg" "twisted.reality.Stack" val "thing pair of green boxer shorts\nthing a pair of black slacks\n" key "twisted.reality.Stack@585424a"
	float "endurance" "-0.5"
	float "mindspeak" "0.1"
	
	persistable "clothing right foot" "twisted.reality.Stack" val "thing pair of green socks\nthing pair of black leather boots\n" key "twisted.reality.Stack@5854260"
	
	persistable "clothing left foot" "twisted.reality.Stack" val "thing pair of green socks\nthing pair of black leather boots\n" key "twisted.reality.Stack@58542ad"
	float "psyche" "1.0"
	
	persistable "clothing right arm" "twisted.reality.Stack" val "thing white silk shirt\nthing dark green overcoat\n" key "twisted.reality.Stack@5854391"
	
	persistable "clothing left arm" "twisted.reality.Stack" val "thing white silk shirt\nthing dark green overcoat\n" key "twisted.reality.Stack@58543f9"
	
	persistable "clothing chest" "twisted.reality.Stack" val "thing white silk shirt\n" key "twisted.reality.Stack@58543c1"
	
	persistable "clothing neck" "twisted.reality.Stack" val "thing white silk cravat\n" key "twisted.reality.Stack@5854437"
	
	persistable "updatedSkills" "twisted.reality.Stack" val "string mindspeak\n" key "twisted.reality.Stack@585449b"
	string "visit color" "greenish"
	descript "clothing" {Pronoun Of("Tenth"), " is wearing ", "a pair of green-tinted spectacles", ", ", "a neatly tied white silk cravat", ", ", "a white silk shirt", ", ", "a dark green overcoat", ", ", "black slacks", ", ", "and ", "knee high black leather boots", "."}
	extends "Class_Human"
	ability "divunal.magic.spells.Frotz"
	ability "divunal.magic.spells.Zorft"
	ability "divunal.common.skills.Glance"
	ability "divunal.tenth.Rube"
	ability "divunal.tenth.TiringVerb"
	architect
	passwd "Te9J2beMbV1yU"
}

Thing
{
	name "demo center bathroom notice"
	describe "A large, white, laminated piece of paper, topped with the large heading \"NOTICE:\" followed by the text:\n\n     \"This bathroom is equipped with a High Pressure Zero Gravity Toilet for your convenience and safety. Twisted Matrix Enterprises Inc. is in no way responsible for the misuse, intentional or otherwise, of the abovementioned High Pressure Zero Gravity Toilet, and is not responsible for any injuries, damages, psychological trauma, and/or destruction and/or loss of any parts, extremities, organs, possessions, or attributes inflicted during the operation of the toilet in question.\""
	place "Demo Center Bathroom Stall"
	feature "twisted.reality.plugin.ReadLook"
	string "name" "large notice"
	component
	syn "large notice"
	syn "notice"
	syn "note"
}

Thing
{
	name "small bucket of plaster"
	describe "A small tin can full of plaster of paris. It looks like the same stuff that someone has been using to make the corners of this room smoother."
	place "Damien's Bedroom"
	syn "plaster"
	syn "bucket"
}

Room
{
	name "Other New Jersey Apartment Bedroom"
	describe "A fair sized room, with bluish wallpaper and a darker, brownish shag carpet. The two windows are set with dark brown shades, and a small closet is built into the east wall, with sliding wooden doors that seem a bit too large for it. A number of boxes are stacked up in the corners of the room, and a set of blankets are folded up on the floor in semblance of a bed, next to a suitcase strewn with brushes, hair ties, and an electric razor.\n"
	theme "default"
	exit "south" to "New Jersey Apartment Hallway"
}

Room
{
	name "Back Lawn"
	describe "You are near the... aw, fuck it.\n"
	place "Inheritance"
	theme "leaf"
	exit "west" to "Back Lawn(9)"
	exit "east" to "Back Lawn(8)"
	exit "north" to "Back Lawn(1)"
	exit "south" to "Chateau Pantry"
}

Thing
{
	name "pig skull"
	describe "The poor creature!"
	place "large black cauldron"
}

Room
{
	name "Silver Shadowed Wood"
	describe "The woods at the edge of the clearing here glow with an erie shade.  The trees whisper among themselves, their bare branches swaying, almost beckoning you towards them."
	theme "leaf"
	exit "south" to "Silver Shadowed Glade"
}

Thing
{
	name "maze entrance sign"
	describe "This sign has weathered rather poorly, but you can make out the instructions, \"HIT BUTTON TO START TIMER.\""
	place "Garden Maze"
	string "name" "sign"
	component
	syn "sign"
}

Room
{
	name "Wrecked House Foundation"
	describe "This was probably once the foundation of a house, but the house has long since been destroyed.  Sharp rubble surrounds the foundation, but there are the remnants of a road to the west."
	theme "crack"
	exit "west" to "Wrecked Street, south"
}

Thing
{
	name "post-it"
	describe "I suppose I could e-mail you, but this is better. I'm sure.\n\nHow do I check to see if the directObject() matches a particular object I have in mind? If the user uses my foo verb, and types \"foo troll with sword\" how can I check to see that it is fooing a troll, so that I can respond \"You foo the troll hard and fast\" or some such. Make sense?\n\nThanks,\nBenjamin (currently still in control of Damine's motor functions, poor guy will be even MORE confused soon!)"
	place "Damien's Cubicle"
}

Thing
{
	name "demo center bathroom mirror"
	describe "It appears to be a demo center bathroom window, but it is vague, indistinct, and little more than a blurry smear on reality."
	place "Demo Center Lavatory"
	string "base description" "A large, rectangular mirror built into the wall over the sink. Reflected in the mirror, you see:\n\n"
	string "name" "Lavatory mirror"
	
	property "description" "demo.MirrorDesc"
	component
	syn "mirror"
}

Room
{
	name "Hall"
	describe "null"
	exit "south" to "Mod Seven"
}

Thing
{
	name "dark green carpet"
	describe "The carpet is a murky, dark green color, and woven with intersecting lines and curves of black thread. The lines are difficult to discern against their dark background, and almost seem to be moving, in an indistinct sort of way."
	place "Mansion Upper Hall"
	component
	syn "carpet"
	syn "green carpet"
}

Location
{
	name "Mansion Bedroom Bureau"
	describe "A dark, polished wooden bureau, with six drawers. The top of the bureau is blends seamlessly into the frame of a large, ovular mirror. "
	place "Tenth's Chamber"
	feature "twisted.reality.plugin.OpenCloseContainer"
	string "name" "bureau"
	extends "Class_Container"
	component
	syn "drawer"
	syn "drawers"
	syn "wooden bureau"
	syn "bureau"
	opaque
	shut
}

Thing
{
	name "pair of grey soft leather boots"
	describe "A pair of suede boots in a muted grey color."
	place "Maxwell"
	boolean "clothing worn" true
	boolean "isLit" false
	extends "Class_Shoes"
	component
	syn "boots"
	syn "grey boots"
}

Thing
{
	name "Reality Pencil"
	describe "This is a regular Number Two pencil, brought here from the real world.  It holds the power of ultimate creation and destruction."
	place "Maxwell"
	feature "twisted.reality.author.Visible"
	feature "twisted.reality.author.She"
	feature "twisted.reality.author.He"
	feature "twisted.reality.author.Locate"
	feature "twisted.reality.author.Draw"
	feature "twisted.reality.author.CVS"
	feature "twisted.reality.author.FloatSet"
	feature "twisted.reality.author.IntSet"
	feature "twisted.reality.author.Sketch"
	feature "twisted.reality.author.Theme"
	feature "twisted.reality.author.Nail"
	feature "twisted.reality.author.Name"
	feature "twisted.reality.author.Erase"
	feature "twisted.reality.author.Describe"
	feature "twisted.reality.author.Persist"
	feature "twisted.reality.author.Yank"
	feature "twisted.reality.author.Enable"
	feature "twisted.reality.Godhood"
	feature "twisted.reality.author.Dig"
	feature "twisted.reality.author.Barricade"
	feature "twisted.reality.author.Allow"
	feature "twisted.reality.author.Grab"
	feature "twisted.reality.author.AddUser"
	feature "twisted.reality.author.Extend"
	feature "twisted.reality.author.Reference"
	feature "twisted.reality.author.Tunnel"
	feature "twisted.reality.author.Banish"
	feature "divunal.common.Activate"
	feature "twisted.reality.author.BoolSet"
	feature "twisted.reality.author.Compile"
	feature "twisted.reality.author.Operable"
	feature "twisted.reality.author.Broadcast"
	feature "twisted.reality.author.MoodSet"
	feature "twisted.reality.author.It"
	feature "demo.Repop"
	boolean "isLit" false
	syn "pencil"
}

Location
{
	name "ornate wooden table"
	describe "The wooden legs of this table curve at the ends into what seem like paws of some animal. The surface is polished and bright, showing a beautiful grain."
	place "Smoking Room"
	theme "wood"
	extends "Class_Container"
	component
	syn "table"
	syn "wooden table"
	syn "ornate table"
}

Thing
{
	name "photograph"
	describe "A small color photograph has been inserted somewhat unevenly into this black wooden frame. A small \"leg\" sticks out the back of the cheap, wooden, dyed-black frame, enabling the assemblage to stand upright on the desk.\n\nThe photograph is of a large group of people, all of whom look related and poorly posed. Most of the men and a few of the women are wearing nice-looking suits, except for one guy in the back. He is dressed for a safari, in a photographer's jacket and headband. You can almost see the pith helmet he assuredly carries in his arms. The rest of the family seems to be avoiding him in the photo."
	place "Damien's Cubicle"
	syn "photo"
}

Room
{
	name "Armory"
	describe "This room still contains numerous rusted sets of armor, but all the lances, bows, arrows, and rifles have been taken from the racks that once contained them.  There is a large archway leading southwest, and a short and narrow door leading to the north."
	theme "greystone"
	exit "north" to "Small Arched Tunnel"
	exit "southwest" to "Great Dome"
}

Thing
{
	name "button"
	describe "A small, round button mounted at eye level on the bookshelf."
	place "Science Fiction Room"
	feature "divunal.tenth.LibraryPush"
	thing "steam source" "Mansion Steam Engine"
	long "steam off" 917227965847
	component
	syn "green button"
	syn "yellow button"
	syn "red button"
	syn "red"
	syn "green"
	syn "yellow"
}

Room
{
	name "Cramped Transporter Booth"
	describe "This is a transporter booth - though somewhat cramped.  It looks as though it was once spacious, but one half of the room has been compressed by what look like metal girders that have collapsed, blocking what may have once been an exit to the north.  There is a doorway to the east, beyond which you can see a hallway."
	exit "east" to "Reception Area"
}

Room
{
	name "Under Walkway"
	describe "You are underneath a glass walkway.  To your west, there is an entrance to the post office, and to your east there is the Robert Crown sports center."
	exit "north" to "Path beside the RCC"
	exit "south" to "HC Library Slab"
	exit "east" to "RCC Entrance Hall"
}

Room
{
	name "Mansion Upper Hallway"
	describe "A long, wide hallway, ending in an arched doorway to the east. A pair of smaller doors are set halfway along the length of the hall, leading north and south, respectively. A dark green carpet runs along the entire length of the floor, inscribed with a black, twisting pattern of lines and angles."
	theme "wood"
	descript "tenths bedroom doors openDesc" "A pair of double doors stand open at the west end of the hallway."
	exit "south" to "Mansion Guest Room"
	exit "north" to "Parlor"
	exit "west" to "Tenth's Chamber" with "tenths bedroom doors"
	exit "east" to "Mansion Stairwell"
}

Room
{
	name "Silver Shadowed Plain"
	describe "The grass is so thick here that you can barely see where you are going.  You can't imagine how the grass has gotten so thick or so tall."
	theme "leaf"
	exit "east" to "Silver Shadowed Glade"
	exit "west" to "Silver Shadowed Fields"
	exit "southeast" to "Silver Shadowed Glade(7)"
	exit "north" to "Silver Shadowed Plain"
}

Thing
{
	name "steam meter"
	describe "It appears to be a steam meter, but it is vague, indistinct, and little more than a blurry smear on reality."
	place "dark green overcoat"
	thing "steam source" "Mansion Steam Engine"
	
	property "description" "divunal.tenth.SteamMeter"
	syn "meter"
}

Location
{
	name "pipe rack"
	describe "A rather nondescript pipe rack."
	place "Smoking Room"
	extends "Class_Container"
	syn "rack"
}

Room
{
	name "Slanted Mansion Hallway"
	describe "This narrow hallway is at a 45 degree angle to the corner of the house.  It leads straight into the center of the mansion, where there is a doorway.  You are at the top of a spiral staircase which leads downward."
	exit "northwest" to "Cylindrical Mansion Hallway"
	exit "down" to "Spiral Landing"
}

Room
{
	name "Mansion Basement Storeroom"
	describe "A dark, roughly built brick room, with an uncovered dirt floor. A broken glass bulb hangs from the ceiling by its cord, and several empty crates are scattered on the floor. Several of the crates are stacked up against an old wooden door in the west wall, which has also been boarded over. To the east, a roughly rectangular hole in the wall leads into a smaller room."
	theme "greystone"
	exit "east" to "Mansion Basement"
}

Thing
{
	name "demo gift shop sign"
	describe "A small white cardboard sign, with black letters. It reads:\n\n\t\"TME Gift Shop Customers:\"\n\n\"Due to the increasing number of increasingly rude and inconsiderate guest users running off with our merchandise and using it to jam the plumbing, we have been forced to shut down the Gift Shop. We may re-open in the future, but only if some degree of civility on the parts of the visitors can be established.\"\n\nThank you,\n\nThe Management\""
	place "Demo Center Gift Shop"
	feature "twisted.reality.plugin.ReadLook"
	string "name" "small white sign"
	component
	syn "small white sign"
	syn "white sign"
	syn "small sign"
	syn "sign"
}

Thing
{
	name "dexterity dial"
	describe "It appears to be a dexterity dial, but it is vague, indistinct, and little more than a blurry smear on reality."
	place "Genetic Laboratory"
	float "value" "0.05"
	extends "Class_Player Creation Dial"
	component
	syn "dexterity"
	syn "dial"
}

Room
{
	name "Sea Shore"
	describe "As you turn the corner you are blinded by a bright blast of sunlight. When you recover your vision you can see that you are standing in the middle of a vast stretch of beach, with pure white sand stretching off in all directions. \nTo the east the sand meets a vast, dark-green sea. Immense waves are crashing, spraying you with flecks of foam. The water looks very cold and very powerful.\nThe breeze is quite strong here, as is the smell of salt. The sky is a flat slate blue."
	exit "east" to "Lonely Expanse of Beach"
	exit "south" to "Windy Section"
}

Thing
{
	name "class_gun trigger"
	describe "A blue box."
	place "Tenth's Chamber"
}

Room
{
	name "A Crumbling Stairway"
	describe "Nothing special."
	theme "crack"
	exit "up" to "Wrecked Street, curve"
}

Location
{
	name "clue second chair"
	describe "A rather nondescript clue second chair."
	place "Garden Maze(12)"
	string "name" "second chair"
	extends "Class_Sittable"
	component
	syn "second chair"
	syn "chair"
	broadcast
}

Thing
{
	name "carvings"
	describe "The carvings are scrawled in an unusual handwriting, and are shaky, as if they were written by a weak and dying hand.  They read, \"hello sailor\"."
	place "Small Platform on the Rock"
	component
}

Room
{
	name "New Jersey Apartment Bathroom"
	describe "A small, entirely off-white and beige bathroom. The sink is a tall, vaguely flower-shaped work of ceramics, but despite its graceful appearance, it looks rather unsteady, swaying slightly in tune to the unusual sounds of the plumbing. A toilet is set alongside it, considerably more steady, and the opposite side of the room is dominated by a combination shower/bathtub. The shower head is dripping at a slow, measured pace, producing a metallic clinking noise as each drop hits the temperature dials below it. A plastic towel rack and shampoo basket stands by the tub, laden with shampoos, conditioners, and soap.\n"
	theme "default"
	exit "north" to "New Jersey Apartment Hallway"
}

Room
{
	name "Lounge Walkway"
	describe "This is a long glass walkway along the south side of which are a set of chairs and tables and lamps. It continues east-west, to the west is the library building and to the east is the Robert Crown Center."
	exit "east" to "Robert Crown Center Cafe"
	exit "west" to "Airport Lounge"
}

Room
{
	name "More Office Hallway"
	describe "There is a streak of blackened and burnt area down the center of this hall, terminating in a deep chasm stretching from one side of the hall to the other.  The chasm looks to be rather deep, and dark, though it is lit from the panel lights on the ceiling here.  Far across the chasm you can see this hall continuing.  Looking down into the chasm, you can see footholds that you think will hold your weight."
	exit "down" to "Chasm Bottom"
	exit "west" to "Office Hallway"
}

Thing
{
	name "huge cylindrical pressure tank"
	describe "A huge, cylindrical tank, built out of metal and set with strengthening bands and braces. A small brass plaque is attached to the front side, embossed with the phrase \"WARNING: Contents may be under high pressure\" in flowing script."
	place "Mansion Basement Engine Room"
	component
	syn "cylindrical pressure tank"
	syn "pressure tank"
	syn "tank"
}

Location
{
	name "green leather book"
	describe "A green, leather bound book, entitled \"Simulacra And Simulation\" in gold embossed letters."
	place "Maxwell"
	feature "twisted.reality.plugin.Put"
	feature "demo.OpenBookBox"
	thing "repop" "demo center coffee table"
	descript "opened" "It is open, revealing that the center of each page has been removed, making it useless as a book but quite functional as a container."
	syn "book"
	syn "green book"
	syn "leather book"
}

Room
{
	name "Art Room"
	describe "This room is heavily spattered with paint, graphite dust, papers, eraser-residue, and various other side-effects of artistic endeavor.  A lone easel stands in the center of the room, on a pedestal."
	exit "southwest" to "More Mansion Hallway"
}

Thing
{
	name "sixth knob"
	describe "Sixth knob from the top of the qin with which to tune the instrument."
	place "qin"
	component
	syn "knob6"
	syn "knob"
}

Thing
{
	name "piece of skystone"
	describe "This appears to be a fragment of a much larger piece of stone. It feels warm to the touch: almost as if it has some sort of internal power. One side of the stone glows a soft blue color, while the other is simply a beautiful deep blue."
	place "Secret Chamber"
	feature "divunal.rikyu.Morph"
	string "morph name old" "Elderly man"
	string "morph descr old" "A feeble looking creature, this man seems to have been through a lot in his long lifetime."
	string "morph gender old" "male"
	string "morph name nymph" "Elven wood nymph"
	string "morph descr nymph" "An adorable-looking wood nymph."
	string "morph gender nymph" "female"
	string "morph descr jello" "A rather squishy cube of an unknown substance."
	string "morph name jello" "Gelatinous Cube"
	string "morph gender jello" "neutral"
	syn "skystone"
	syn "stone"
}

Thing
{
	name "player creation machine"
	describe "The control panel of the machine has three buttons, labeled \"GENERATE\", \"RELEASE\", and \"RANDOMIZE\", and six dials, each labeled and marked on a range from -1.0 to 1.0.  There are two black rectangles above the control panel, each with an engraved label in the silver below, \"Point Total\" and \"Name\" respectively, and immediately below those, there is a silver keyboard. "
	place "Genetic Laboratory"
	feature "divunal.common.author.PCMachinePush"
	feature "divunal.common.author.PCMachineType"
	thing "tube" "long glass tube"
	thing "strength" "strength dial"
	thing "agility" "agility dial"
	thing "dexterity" "dexterity dial"
	thing "endurance" "endurance dial"
	thing "psyche" "psyche dial"
	thing "memory" "memory dial"
	handler "update" "divunal.common.author.PCMachineUpdate"
	component
	syn "release"
	syn "randomize"
	syn "generate"
	syn "machine"
	syn "controls"
	syn "control panel"
	syn "panel"
}

Room
{
	name "Quiet Niche"
	describe "This small alcove is formed by the convergence of two large bookshelves. One shelf contains a number a books about anthropology and ancient civilizations, the other is stacked with volumes and volumes of poetry.\nThere is a much wider area to the southeast, and perhaps you could squeeze under the western shelf."
	theme "paper"
	exit "west" to "Under the Bookshelf"
	exit "northwest" to "Wider Area"
}

Room
{
	name "Wider Area"
	describe "This area is still a mere two or three arm-spans wide, but it seems huge compared to the claustrophobic closeness of the passage to the north.\nThe dust which completely covers the floor here is very grainy. It looks more like sand than dust, and it is everywhere. There is a very slight glow from the eastern end of this section, and to the southeast two bookshelves form a quiet niche."
	theme "paper"
	exit "southeast" to "Quiet Niche"
	exit "east" to "Windy Section"
	exit "north" to "Tight Squeeze"
}

Room
{
	name "Musty Section"
	describe "This section of the library seems, if possible, even mustier and older than the rest of the books. Glancing casually at a few titles, the books seem to be mostly occult, mostly very old, and mostly bound in human flesh. The library gets rapidly more twisty towards the south, and to the west it opens out into a larger room."
	theme "paper"
	exit "west" to "Damien's Office,entering"
	exit "south" to "The Twisty Bit"
}

Thing
{
	name "ancient artifact"
	describe "A totem of an owl, obviously of some great antiquity.  It appears to be glaring straight at you from whatever angle you see it."
	syn "artifact"
}

Room
{
	name "Small Grey Room"
	describe "This is a small grey room with a safe in the corner.  It has no windows, only one door, and no ventilation.  The walls look to be made out of something extremely hard and very thick."
	exit "south" to "Nice Office"
}

Thing
{
	name "shelves"
	describe "Large, heavy looking bookshelves made of glossy black metal. They are laden with various works of science fiction, but you don't see anything paticularly of interest to you."
	place "Science Fiction Room"
	component
	syn "middle shelves"
	syn "middle shelf"
	syn "rightmost shelf"
	syn "rightmost shelves"
	syn "leftmost shelf"
	syn "leftmost shelves"
}

Room
{
	name "Less Crumbling Hallway"
	describe "This hallway is in slightly better condition than those that preceeded it.  The archaic mode of lighting here has reverted to candles near to the high ceiling.  The hallway continues to the east and to the west there is a door leading outside."
	theme "greystone"
	exit "west" to "Great Dome"
	exit "east" to "Crumbling Hallway"
}

Room
{
	name "Spring Chamber"
	describe "The ground here is a springy bed of grass, which is slightly damp with dew.  The walls are almost the same color of the grass, and the room feels practically alive itself.  On the west wall, there is a huge window looking out over a forest of pine trees during a rainstorm.  The sound of rain falling has a mildly soporific effect, and the ground is soft - you feel like going to sleep."
	exit "east" to "Cylindrical Mansion Hallway"
}

Thing
{
	name "Class_Cape"
	describe "A white box."
	place "Clothing Box"
	string "clothing location" "neck"
	extends "Class_Clothing"
}

Room
{
	name "Damien's Cubicle(1)"
	describe "null"
	exit "south" to "Damien's Office,entering"
}

Room
{
	name "Chateau Staircase Landing"
	describe "A Chateau Staircase Landing looking as if it needs to be described."
	place "Inheritance"
	theme "greystone"
	exit "north" to "Chateau Library(1)"
	exit "west" to "Chateau Hallway(6)"
	exit "east" to "Chateau Hallway(4)"
	exit "down" to "Chateau Staircase"
}

Thing
{
	name "glock semi-automatic pistol"
	describe "A white box."
	place "Agent Moore"
	extends "Reality Pencil"
	syn "glock"
	syn "gun"
}

Location
{
	name "demo center high backed chair"
	describe "A blue box."
	place "Demo Center Waiting Room"
	feature "twisted.reality.plugin.furniture.Stand"
	feature "twisted.reality.plugin.furniture.Sit"
	string "name" "high-backed chair"
	string "player preposition" "sitting on"
	string "preposition" "on"
	int "maximum occupancy" 2
	component
	syn "high backed chair"
	syn "chair"
	broadcast
}

Thing
{
	name "name changing machine"
	describe "A large stainless steel structure vaguely reminiscent of a phone booth, with an embedded monitor and keyboard, featuring a prominent \"Execute\" key."
	place "Science And Technology Demo Center"
	feature "demo.DemoNamerType"
	string "new name" "Effeminate Sailor"
	descript "screen" "The screen is black, except for \"Effeminate Sailor\" in large green letters."
	component
	syn "keyboard"
	syn "machine"
	syn "key"
	syn "booth"
	syn "nominator"
	syn "monitor"
}

Thing
{
	name "Emerald Cube"
	describe "A white box."
	place "Emerald Room"
	extends "Class_Cube"
	component
	syn "cube"
}

Thing
{
	name "Ford Model T Runabout brochure"
	describe "A folded piece of posterboard, emblazoned with a brightly colored drawing of a well dressed young couple speeding along a country road in a Runabout of their own. The slogan \"Better than Ever Before\" is sprawled across the top of the page in bright red flowing script.\n\n\"Greatly improved with one man top and slanting windshield, more room in carrying compartment at the rear and with many improvements in chassis construction, the Ford Runabout is a more attractive purchase than ever before, at the lowest price in motor car history.\"\n\nIt's not exactly new anymore, but it certainly was cheaper than ever when your uncle sold it to you for $45 last year."
	place "Chateau courtyard"
	syn "paper"
	syn "brochure"
}

Room
{
	name "Clearing 2"
	describe "You are in a small clearing in a well marked forest path that extends to the east and west."
	string "name" "Clearing"
	exit "south" to "Forest 2"
	exit "north" to "Forest 2"
	exit "west" to "Behind House"
}

Location
{
	name "rustic loveseat"
	describe "A wonderfully soft leather chair."
	place "Smoking Room"
	int "maximum occupancy" 2
	string "preposition" "on"
	string "player preposition" "sitting on"
	extends "Class_Sittable"
	syn "loveseat"
	broadcast
}

Thing
{
	name "notebook"
	describe "This notebook has a table of names and places scrawled on it."
	place "James"
	feature "divunal.james.Mark"
	feature "divunal.james.Recall"
	thing "warp demo" "Twisted Reality Corporate Demo Center"
	thing "warp here as moo" "A Dark Narrow Passage"
	thing "warp default" "Genetic Laboratory"
}

Room
{
	name "Rocky Ledge, further west"
	describe "To your east, there appear to be some steps where you can ascend to the looming palace above.  To the west there lies more of a ledge."
	exit "east" to "Ledge in front of Castle in the Clouds"
	exit "west" to "Very Narrow Rocky Ledge"
}

Room
{
	name "Crumbling Library"
	describe "This relatively small (but still immense) room must once have been a library, judging from the expanse of empty shelf-space and the few remaining books, crumbled to pieces.  The one remaining vestige of the appearance of a true library is the huge dias in the center of the room (which looks as though it may have once held a book), boldly emblazoned \"The Encyclopedia\"."
	theme "greystone"
	exit "south" to "Great Dome"
}

Thing
{
	name "large predaceous diving beetle"
	describe "A large, glossy black beetle with powerful gripping forelegs, sharp, glistening, piercing mouthparts, and a homicidal gleam in it's compound eyes. Its numerous legs seem to be designed for swimming rapidly through water, but its large wings suggest that it is capable of wreaking havoc on land and in the air as well."
	place "large glass jar"
	syn "diving beetle"
	syn "large diving beetle"
	syn "large beetle"
	syn "beetle"
}

Room
{
	name "Science And Technology Demo Center"
	describe "A spacious, high ceilinged room, with quite a few more stainless steel pipes and mechanical paraphenalia showing through the walls than would normally be tasteful. A large metal booth is built into the east wall, next to a table strewn with technical manuals."
	place "Demo"
	descript "sliding glass doors closeDesc" "A pair of sliding glass doors stand shut in the northern wall."
	exit "south" to "Science and Technology Vehicle Area"
	exit "north" notTo "Demo Center West Wing Lobby" with "sliding glass doors"
}

Thing
{
	name "demo center counter"
	describe "A curved, grey wooden barrier, about waist high. A cash register is built into the end near the doorway, and there is also a small sign standing on the middle of it."
	place "Demo Center Gift Shop"
	string "name" "check out counter"
	component
	syn "check out counter"
	syn "counter"
	syn "behind counter"
}

Thing
{
	name "large gear"
	describe "A thin metal disc about the size of a dinner plate, edged with evenly spaced protrusions."
	place "Mansion Maintenance Closet"
	syn "gear"
}

Room
{
	name "South of House"
	describe "You are facing the south side of a white house. There is no door here, and all the windows are boarded."
	exit "northeast" to "Behind House"
	exit "northwest" to "West of House"
}

Room
{
	name "Tenth's Chamber"
	describe "A spacious bedroom, lit by a pair of identical brass lanterns on the north and south walls. A large four poster bed stands against the west wall, surrounded by hanging curtains. A dark wooden writing desk sits under the lantern against the south wall, and a wooden bureau stands across from it, set with a large mirror."
	theme "wood"
	descript "tenths folding balcony doors openDesc" "A light breeze wafts in from the north, where a pair of folding double doors lead out onto a balcony."
	descript "tenths bedroom doors openDesc" "To the east, a long hallway is visible through a pair of open doors."
	exit "north" to "Mansion Balcony" with "tenths folding balcony doors"
	exit "east" to "Mansion Upper Hallway" with "tenths bedroom doors"
}

Thing
{
	name "dark green shirt"
	describe "A hunter green button-down shirt."
	place "Blake"
	boolean "clothing worn" true
	extends "Class_Shirt"
	component
	syn "shirt"
}

Thing
{
	name "Important Note"
	describe "I wanted to write a section that was entirely dark, pitch black like tar. It could be a magical darkness, if necessary, to extinguish torches and the like. To do so, however, I'd need to disable certain verbs, such as \"look at\" because there isn't anything to see. Can I write my own verb \"look\" for these rooms?\n\nI suppose I should also disable turn page, or can we just suspend disbelief on that score?\n\n//Damien"
	place "Darkness"
	syn "maxwell note"
	syn "note"
}

Location
{
	name "demo center swivel chair"
	describe "An adjustable black plastic chair with a padded seat and backrest, ending in five jointed wheels."
	place "Messy New Jersey Office"
	feature "twisted.reality.plugin.furniture.Stand"
	feature "twisted.reality.plugin.furniture.Sit"
	int "maximum occupancy" 1
	string "preposition" "on"
	string "player preposition" "sitting on"
	string "name" "black swivel chair"
	component
	syn "chair"
	syn "swivel chair"
	syn "black swivel chair"
	broadcast
}

Room
{
	name "HC Library Steps"
	describe "You stand on a bunch of steps in front of the library.  To your south there is a large angry lawn. East, you can descend onto the large concrete slab which is in front of the library for no apparent reason."
	exit "east" to "HC Library Slab"
	exit "north" to "HC Library Landing"
}

Thing
{
	name "billboard"
	describe "This is a ten-foot-tall gleaming white billboard, with clear, black, sans-serif writing that begins in huge three-foot-tall letters and proceeds down to a small ten-point font.  It reads:\n\n\"Welcome to the Twisted Reality Demo Center!  A few basic commands that will guide you through this magical land of corporation fun are:\n\nLOOK: this lets you look at stuff.  Try it on objects both in the room's description and in the object-list in the upper right hand corner.\n\nSAY: This command is macro-bound to your ' key.  You can use this to interact with other players.\n\nGO: This lets you move.  You can also use the numeric keypad (with NUM-LOCK on) to move in the cardinal and secondary compass directions - also, 0 is 'up' and 5 is 'down'.\n\nSMILE: it's polite.  You can just SMILE or SMILE AT someone.\n\nThese are not all of the verbs you can use, by any stretch of the imagination.  Some situations may also call for OPEN, CLOSE, TURN or SIT.  If the game says something snide to you, it's likely that the verb you're looking for doesn't work in that context.  Another good rule to keep in mind is that the parser will understand you in the form: \"verb [direct-object] [preposition indirect-object] so sentences like \"slowly use the tongs to give bob the fish\", \"north, please\" or \"I'd sure like to go north right now, wouldn't you?\" are not going to work quite right.  Try instead \"give fish to bob with tongs\" or \"go north\".\n\nThanks for playing, and we hope you enjoy the demo!"
	place "Twisted Reality Corporate Demo Center"
	feature "twisted.reality.plugin.ReadLook"
	component
	syn "board"
}

Thing
{
	name "Meredith's east wall"
	describe "A collage of random pictures, postcards, and other nonesense hangs on the east wall."
	place "Meredith's Hell Hole"
	component
	syn "wall"
	syn "ewall"
}

Room
{
	name "Side Lawn"
	describe "You are near the rear corner of the mansion, where a thick field of tall grass and weeds that was once the back yard extends outwards to the west. Further north, towards the back of the lawn, you can make out the shape of a small shed against the trees, and there is a narrow path leading south between the wall of the mansion and the forest that has grown up against it."
	place "Inheritance"
	theme "leaf"
	string "name" "Side Lawn"
	exit "south" to "Side Lawn(1)"
	exit "west" to "Back Lawn(8)"
}

Thing
{
	name "Swank Pencil"
	describe "A white box."
	place "Jedin"
	extends "Reality Pencil"
	syn "pencil"
}

Thing
{
	name "ghastly specter"
	describe "A rather nondescript ghastly specter."
	syn "specter"
	syn "ghost"
}

Room
{
	name "class_outdoors_room"
	describe "The superclass of outdoor rooms in Inheritance. HIDE ME! The fruit of knowledge has left me ashamed of my nakedness, and I do not wish to be seen."
	place "Side Lawn"
}

Thing
{
	name "tied stone"
	describe "This small stone has a rope tied around it."
	place "Inner Garden"
	string "name" "small stone"
	syn "small stone"
	syn "stone"
}

Room
{
	name "New Jersey Apartment Living Room"
	describe "A large, square room with ugly reddish pink carpeting, and a large picture window shaded by hanging blinds. A pitifully small grey monitor is set up in the far corner of the room, on top of a small black VCR, next to a sony playstation which is lying upside down on the carpet, apparently held together with duct tape. A staircase leads down to the front door, with a smaller wooden door attached between its railing and the wall of the living room, probably to keep the previous tenant's children out of trouble. The room and its ugly carpet continue to the east.\n"
	theme "default"
	exit "down" to "New Jersey Apartment Entrance Hall"
	exit "east" to "New Jersey Apartment Kitchen"
}

Thing
{
	name "computer"
	describe "A rectangular grey plastic box, labeled \"VA RESEARCH VArStation 28\", just above the word \"Linux\" and the icon of a small flightless bird. The box is sitting underneath a small wooden table, on top of which is a grey plastic keyboard and a monitor. Both are attached to the computer by a number of small plastic cables. A larger, black plastic cable attached to the computer leads along the floor of the hall until it rounds the corner through the western archway."
	place "Mansion Main Hall"
	theme "wood"
	component
	syn "terminal"
}

Thing
{
	name "white silk shirt"
	describe "a loose fitting white silk shirt, gathered into cuffs at the wrist and fitted with a white cravat at the collar."
	place "Tenth"
	string "clothing appearance" "a white silk shirt"
	boolean "clothing worn" true
	extends "Class_Shirt"
	component
	syn "white shirt"
	syn "silk shirt"
	syn "shirt"
}

Room
{
	name "Western End of Grotto"
	describe "An Eastern Grotto End looking as if it needs to be described."
	theme "water"
	exit "north" to "Cold Room"
	exit "east" to "Dark River Tunnel" with "tunnelX2"
}

Thing
{
	name "Battered Document"
	describe "You quickly skim the battered parchment. Apart from an introduction that goes on for great length about life being \"nasty, brutish and short\" the document appears to contain clause after clause of  complex jargon. The initial section, headed \"Social Contract\" mostly deals with ettiquette and the moral justification (and lack thereof, see article 32, page 247) of killing and eating one's neighbors. A later section, entitled \"S.C. Adendum\" has a series of handwritten clauses. A sample clause reads, \"Clause 49a, sub-section R28: Small Velvet Cushion: And hithertofore with such legalities and commisions as stated in the above acts and legeslative derivatives, there shall be created a small cushion constructed of... of pillow stuff and covered in velvet\"."
	place "Damien"
	feature "divunal.damien.Draw"
	feature "divunal.damien.Erase"
	feature "divunal.damien.Gate"
	extends "Reality Pencil"
	syn "document"
	syn "battered"
	syn "social"
	syn "social contract"
	syn "contract"
	syn "pencil"
}

Location
{
	name "bin"
	describe "A hollow black metal cylinder about three feet high."
	place "Mansion Entrance Hall"
	theme "wood"
	extends "Class_Container"
	component
	syn "metal bin"
}

Room
{
	name "The Doorway of the Obsidian Tower"
	describe "This edifice stretches into the sky; to try and see its top would surely strain one's spine.  Regular sets of rectangular protrusions and indentations tile the faces of the tower--in fact, it looks not so much that the glistening rock has been carved, but that someone molded it around a building, blocking it off from the outside world.  Sickly, thorny vines fight for purchase in the sparse cracks encroaching on the building's base, though their flowers' white, bell-shaped bulbs grow thick and plentiful.  You glimpse a hand-shaped indentation to the right of the black stone door, the small slit above it almost obscured by delicate petals."
	exit "south" to "Lonely Expanse of Beach"
}

Room
{
	name "Darkened Room"
	describe "A Darkened Room looking as if it needs to be described."
	place "Inheritance"
	theme "dark"
	exit "east" to "Study"
}

Room
{
	name "Demo Center Gift Shop"
	describe "A small but brightly colored room, aside from the rather drab white walls and polished black marble floor. It is filled with shelves and racks where merchandise would go, but they stand almost empty, except for a few things no one would want. There is a check out counter along the south end of the room, with a built in cash register. A small white sign stands on the counter by the register. To the south, a doorway leads out into a larger room."
	place "Demo"
	exit "south" to "Demo Center West Wing Lobby"
}

Room
{
	name "Garden Maze(14)"
	describe "This portion of the maze seems nicer and more well kept than the rest. You can barely make out a tune gently playing, although the source is unknown."
	theme "leaf"
	string "name" "Garden Maze"
	exit "north" to "Mystic Field"
	exit "west" to "Garden Maze(13)"
}

Player
{
	name "Class_Player"
	describe "This player is as-yet undescribed."
	place "Demo"
	feature "twisted.reality.plugin.Give"
	handler "say" "twisted.reality.plugin.PlayerSayHandler"
	handler "login" "twisted.reality.plugin.Login"
	handler "logout" "twisted.reality.plugin.Logout"
	ability "twisted.reality.plugin.Socials"
	ability "twisted.reality.plugin.Quit"
	ability "twisted.reality.plugin.Take"
	ability "twisted.reality.plugin.Insult"
	ability "twisted.reality.plugin.Inventory"
	ability "twisted.reality.plugin.Go"
	ability "twisted.reality.plugin.Say"
	ability "twisted.reality.plugin.Drop"
	ability "twisted.reality.plugin.Emote"
	ability "twisted.reality.plugin.Give"
	ability "twisted.reality.plugin.Look"
	passwd "--"
}

Room
{
	name "Smoking Room"
	describe "This is a very luxorious room, obiously meant to be a nice place to talk, visit, or even just sit and enjoy a pipe or two. The floor is covered with a vibrant, finely detailed carpet. There are several chairs arranged in a circle, all equally fine. They are all oriented to view the fireplace that graces the east wall. In the center of the circle of chairs is a table with some books and other objects on it. A aging metal staircase leads down into the darkness, and a small passageway leads off to the southeast."
	theme "wood"
	descript "roaring fireplace closeDesc" ""
	exit "east" notTo "Narrow Passageway" with "roaring fireplace"
	exit "southeast" to "Guyute's Bedroom"
	exit "down" to "Guyute's Laboratory"
}

Thing
{
	name "naka-mon"
	describe "The low gate forces even highly-ranked guests to stoop low, reminding them to discard all thoughts of their worldly status upon entering the tea garden."
	place "Outer Tea Garden"
	boolean "obstructed" false
	string "exit message" "You stoop down and humbly step through the central gate."
	string "obstructed message" "You must open the gate before you can enter."
	extends "Class_Door"
	component
	syn "central gate"
}

Thing
{
	name "stainless steel door"
	describe "This solid, featureless, stainless steel door stands at least half again as high as you within an archway of smooth, white marble accented with dark red veins. "
	place "Grand History Book Room"
	boolean "obstructed" true
	string "openDesc" "You see a row of bookshelves through the steel doorway in the south wall."
	string "closeDesc" "A large archway with a steel door stands to the south."
	string "thereOpenDesc" "To the north, you see a large, marble room.  A large book is chained to a pedestal in the center of that chamber."
	string "thereCloseDesc" "A large steel door blocks the northern exit."
	extends "Class_Door"
	component
	syn "door"
	syn "steel door"
}

Room
{
	name "Front of RCC"
	describe "null"
	exit "north" to "RCC Entrance Hall"
}

Room
{
	name "Natural Alcove"
	describe "The floor slopes gradually downward, forming a natural alcove under the floorboards. The air is damp down here, and what little light there is filters in from above. There is a rough pathway leading off to the left, and the alcove ends in a blank wall to the right. In front of you the floor begins to slope downward rather drastically. You can crawl back up as well."
	theme "paper"
	feature "divunal.maxwell.AutoReturnGo"
	thing "special thing" "dirty-looking book"
	exit "west" to "Precarious Ledge"
	exit "up" to "Under the Bookshelf"
}

Thing
{
	name "buttons"
	describe "Each of the 3 middlemost shelves has a small button attached to it at eye level; From left to right, there is a small green button, a rather ominous red button, and a somewhat less threatening yellow button."
	place "Science Fiction Room"
	theme "default"
	component
}

Room
{
	name "Ledge in front of Castle in the Clouds"
	describe "This is a rocky ledge.  Above, you can see a very large, imposing building, which looks like a smooth stone castle.  To your east and west lie further outcroppings of this ledge.  Beneath you, to the north, you see nothing but occasional clouds and a near-infinite drop."
	exit "east" to "Flat Ledge"
	exit "west" to "Rocky Ledge, further west"
	exit "up" to "Castle Steps"
}

Thing
{
	name "Glowing fruit"
	describe "A small piece of fruit that has been sitting in jello so long that it is glowing.  Who'da thunk it."
	place "Aaron's test room"
	boolean "isLit" true
	string "name" "Strange Fruit"
	syn "fruit"
	syn "strange fruit"
}

Room
{
	name "Yurt"
	describe "You are in the Yurt."
	exit "north" to "Yurt Entrance"
}

Room
{
	name "Garden Maze(11)(1)"
	describe "A Garden Maze(11) looking as if it needs to be described."
	theme "leaf"
	exit "back" to "Garden Maze(13)"
}

Thing
{
	name "cot"
	describe "A white rectangular mattress with rounded corners. It looks comfy but hardly luxorious."
	place "Damien's Bedroom"
}

Room
{
	name "Demo Center East Wing"
	describe "An immaculately white hallway, with a tall, arched ceiling and a polished black marble floor. A framed painting has been hung on the south wall, and to the east, the hallway ends in a blue swinging door labeled \"Players\" just above the icon of a gender-neutral stick figure."
	place "Demo"
	theme "default"
	descript "development door openDesc" "A small, battered wooden door stands open to the north."
	exit "north" to "Messy New Jersey Office" with "development door"
	exit "east" to "Demo Center Lavatory" with "demo center bathroom door"
	exit "west" to "Demo Information Center"
}

Thing
{
	name "Mirrored Pencil"
	describe "A white box."
	place "Twin"
	extends "Reality Pencil"
	syn "pencil"
}

Thing
{
	name "sticky note"
	describe "Login: djones\nPassword: \"nemesis\""
	place "Damien's Cubicle"
	syn "sticky"
	syn "note"
}

Thing
{
	name "class_45 ACP bullet"
	describe "It appears to be a class_45 ACP bullet, but it is vague, indistinct, and little more than a blurry smear on reality."
	place "Tenth's Chamber"
	string "bullet type" ".45 ACP"
	extends "class_bullet"
}

Player
{
	name "Chenai"
	describe "No Description."
	gender f
	thing "oldlocation" "Michelle's Dorm Room"
	
	persistable "clothing crown" "twisted.reality.Stack" val "thing tupperware lunchbox\n" key "twisted.reality.Stack@585327b"
	descript "clothing" {Pronoun Of("Chenai"), " is wearing ", Name of("tupperware lunchbox"), "."}
	extends "Class_Human"
	architect
	passwd "Ch11CNUuPElC2"
}

Room
{
	name "Windy Section"
	describe "The dust-- or sand -- is so deep here that the floor is completely gone. There is a fairly strong breeze blowing northward, and it carries a faint salty tang with it. To the west the passage continues, but it seems darker in that direction."
	exit "north" to "Sea Shore"
	exit "west" to "Wider Area"
}

Room
{
	name "Dent in Tube"
	describe "This is a continuation of the gleaming metal tube. There is a huge dent in the ceiling here, which nearly forces you to crawl as you pass it.  The dent looks as though a huge, jagged rock were slammed into the side of the tube by a giant, yet it did not break through.  The tube continues to the south, and bends around to the northwest."
	exit "south" to "Closed Junction"
	exit "northwest" to "Metal Tube"
}

Room
{
	name "Southern End of Small Forest"
	describe "This is the southern end of a small forest, where your way is blocked by a huge rock wall.  Looking upward, you can see the cliff extending up far into the clouds."
	theme "leaf"
	exit "north" to "Clearing in Small Forest"
}

Room
{
	name "Garden Maze(13)"
	describe "A wind blows through this area, and small rivulets swirl about on the ground near the eastern exit. To the south, a large gate is open, and apparently uncloseable, judging by the rusty hinge that squeaks in the wind."
	theme "leaf"
	string "name" "Garden Maze"
	exit "south" to "Garden Maze(11)"
	exit "east" to "Garden Maze(14)"
	exit "west" to "Garden Maze(12)"
}

Location
{
	name "large glass jar"
	describe "A large glass jar with a rubber seal clamped onto the top."
	place "plastic swivel chair"
	feature "twisted.reality.plugin.Put"
	syn "glass jar"
	syn "jar"
}

Thing
{
	name "Class_Shirt"
	describe "A white box."
	place "Clothing Box"
	string "clothing location" "chest"
	string "clothing location 2" "left arm"
	string "clothing location 3" "right arm"
	extends "Class_Clothing"
}

Thing
{
	name "blue box"
	describe "A rather nondescript blue box."
	place "Ivy Garden"
	component
}

Thing
{
	name "metal spike"
	describe "Heavy, metal, pointy. This spike could do some serious damage to one's skull."
	syn "spike"
}

Room
{
	name "Old Wooden Shed"
	describe "An Old Wooden Shed looking as if it needs to be described."
	place "Inheritance"
	theme "wood"
	exit "north" to "Back Lawn(5)"
}

Location
{
	name "gondola"
	describe "This gondola has a canopy cover like that of a horse drawn carriage. It is painted ebony black with deep rich mahogany wood decks, inlaid roses and glove leather seats."
	place "Western End of Grotto"
	feature "divunal.rikyu.UseGondola"
	extends "Class_Boat"
	syn "boat"
	broadcast
}

Thing
{
	name "manual"
	describe "and can in fact be considred mid-strata evocations, provided of course that the wage para-disclosure is handled via proxy. Also of interest is the government's new attempt to garner worker re-compensation allowance dividends in the high yield market. Following the pattern the established for private / cottage income two years ago with 78-Z224, the latest attempt is also prone to flaw. Pro-Dis 6900A, or PD6A as those \"in the know\" call it, has taken on somewhat of a life of its own of late...\n\nThe manual continues in this vein for countless pages."
	place "Damien's Cubicle"
}

Room
{
	name "Black Hallway"
	describe "This is a solid onyx hallway with an arched ceiling.  It continues north into the distance for a long while, and south into another, brighter hallway."
	theme "greystone"
	exit "north" to "Black Hallway"
	exit "south" to "Jewel Bedecked Hallway 2"
}

Thing
{
	name "steam engine lever"
	describe "A brass lever with a red handle set into the side of the steam engine, labled \"DANGER: RELEASE VALVE\"."
	place "Mansion Basement Engine Room"
	feature "divunal.tenth.SteamEnginePull"
	thing "steam source" "Mansion Steam Engine"
	component
	syn "lever"
}

Thing
{
	name "Obsidian Pencil"
	describe "A sharpened crystal of obsidian which looks as if it were modified for writing.  A small triangle of graphite emerges from its tip and a rubber ball is on its end."
	extends "Reality Pencil"
	syn "pencil"
}

Thing
{
	name "gondola pager"
	describe "This bell is crafted out of some silver material. It looks perfectly balanced, and one can imagine how sweet it sounds."
	place "teakwood podium"
	feature "divunal.rikyu.SummonGondola"
	string "name" "small bell"
	syn "small bell"
	syn "pager"
	syn "bell"
}

Room
{
	name "Temple Bottom Floor"
	describe "This room is a very large octagonal room, whose ceiling is supported at intervals by pilliars.  At the center of the room, a wide, octagonal, metal staircase is framed by eight such pilliars, at the points of the octagon.  Arches are placed at equal intervals in the centers of the outer walls, each leading into its own hallway.  Each arch is decorated in a unique manner."
	theme "default"
	string "name" "Bottom Floor"
	exit "up" to "Temple Middle Floor"
	exit "north" to "Temple Northern Hallway"
}

Location
{
	name "Clothing Box"
	describe "A perfectly white box labeled \"Clothing Classes\" in neat black letters."
	place "Demo"
	feature "twisted.reality.plugin.Put"
	syn "box"
}

Room
{
	name "Chateau Library(2)"
	describe "A Chateau Library looking as if it needs to be described."
	place "Inheritance"
	theme "greystone"
	string "name" "Chateau Library"
	exit "east" to "Chateau Hallway(14)"
	exit "west" to "Chateau Library(1)"
}

Room
{
	name "Chateau Library(1)"
	describe "A Chateau Library looking as if it needs to be described."
	place "Inheritance"
	theme "greystone"
	string "name" "Chateau Library"
	exit "south" to "Chateau Staircase Landing"
	exit "east" to "Chateau Library(2)"
	exit "west" to "Chateau Library"
}

Thing
{
	name "memory dial"
	describe "A black dial.  Look at the machine for a clearer description..."
	place "Genetic Laboratory"
	float "value" "0.4"
	extends "Class_Player Creation Dial"
	component
	syn "memory"
	syn "dial"
}

Thing
{
	name "a small piece of plaster"
	describe "A white box."
	place "Damien's Cubicle"
}

Room
{
	name "Hallway"
	describe "This is a rather short wood paneled hallway. The floor is covered buy a thin persian rug, and the walls are covered by thick hangings. To the north is a heavy wooden door, and to the east is a comfortable looking study."
	theme "paper"
	exit "north" to "Front Step of Darkness"
	exit "east" to "Proper English Library"
}

Location
{
	name "oddly built brass and metal chair"
	describe "A wooden chair set into a large metal contraption, covered with tubes and wires and ending in a large brass dome over the head of the person unfortunate enough to be sitting in it."
	place "Mansion Staging Room"
	feature "twisted.reality.plugin.furniture.Stand"
	feature "twisted.reality.plugin.furniture.Sit"
	feature "divunal.common.skills.MindSpeak"
	string "player preposition" "sitting on"
	string "preposition" "on"
	int "maximum occupancy" 1
	syn "chair"
	syn "metal chair"
	syn "brass and metal chair"
	syn "brass chair"
	syn "oddly built chair"
	broadcast
}

Room
{
	name "Forest Path"
	describe "This is a path winding through a dimly lit forest. The path heads north-south here. One particularly large tree with some low branches stands at the edge of the path."
	exit "east" to "Forest 2"
	exit "west" to "Forest"
	exit "south" to "North of House"
	exit "north" to "Clearing"
}

Room
{
	name "Temple Middle Hallway South"
	describe "A Temple Middle Hallway South looking as if it needs to be described."
	theme "default"
	exit "north" to "Temple Middle Floor"
}

Room
{
	name "Crater Edge North"
	describe "You stand at the edge of a large hole.  Its sides slope steeply down, too sheer to scale with ease.  You cannot see any indication of what created this crater; the bottom of the pit looks to be filled with a thick, grey liquid."
	theme "crack"
	exit "east" to "Wrecked Street, north"
}

Room
{
	name "Temple Middle Hallway West"
	describe "A Temple Middle Hallway West looking as if it needs to be described."
	theme "default"
	exit "east" to "Temple Middle Floor"
}

Room
{
	name "Temple Middle Hallway East"
	describe "A Temple Middle Hallway East looking as if it needs to be described."
	theme "default"
	exit "west" to "Temple Middle Floor"
}

Room
{
	name "Garden Maze(12)"
	describe "This part of the maze looks as if it's been set up especially for the weary traveller to take a break. There's a nice table near the eastern exit and four chairs suspiciously positioned to the west."
	theme "leaf"
	string "name" "Garden Maze"
	exit "east" to "Garden Maze(13)"
	exit "west" to "Garden Maze(9)"
	exit "south" to "Garden Maze(10)"
}

Room
{
	name "RCC South Lounge"
	describe "This is a large empty room where the fencing team sometimes practices."
	exit "north" to "RCC Rec Area East"
}

Room
{
	name "Temple Middle Hallway North"
	describe "A Temple Middle Hallway North looking as if it needs to be described."
	theme "default"
	exit "south" to "Temple Middle Floor"
}

Thing
{
	name "great oak tree"
	describe "This great tree is several armspans around. Given it's immense size, it must have been here for at least a century. "
	place "Ivy Garden"
	component
	syn "tree branch"
	syn "oak tree"
	syn "tree"
}

Thing
{
	name "plaque"
	describe "The plaque is made of bronze and is firmly affixed to the surface of the sphere. \"Welcome to Blake's Sphere!\" is emblazoned across it in stenciled lettering."
	place "Blake's Sphere"
	component
}

Thing
{
	name "Cara"
	describe "A white box."
}

Thing
{
	name "Nominator Manual"
	describe "A large grey plastic binder, titled \"Nominator 5000: A Reference Manual\". It only seems to contain a few pieces of paper, but would probably be very useful if you wanted to read about the functions of the Nominator."
	place "science and technology demo center table"
	feature "twisted.reality.plugin.Read"
	string "read text" "     \"Personalize your visit to our demo center with the Nominator 5000! Simply type your desired name on the supplied ergonomic keypad, and press the execute key when the name on the screen meets with your approval! A fun and easy way to increase your self worth and make your stay here a somewhat more memorable one.\n\n     (WARNING: SEVERE EYE DAMAGE: The Twisted Matrix Enterprises Nominator Model 5000 may contain near-unpronouncable quantum effects. Do not look directly into the singularity.)\""
	syn "manual"
}

Thing
{
	name "class_food"
	describe "It appears to be a class_food, but it is vague, indistinct, and little more than a blurry smear on reality."
	place "Food Box"
	feature "divunal.common.Eat"
}

Thing
{
	name "wall"
	describe "Grey. Or perhaps blue? Greyish-blue, maybe. Hard plastic cubicle dividers... possibly made of cloth and not plastic."
	place "Damien's Cubicle"
	component
	syn "walls"
}

Room
{
	name "Test Bed"
	describe "This is a big comfy mattress where you can test stuff. There is also a large, comfortable sofa here."
	theme "water"
	exit "north" to "Class Room"
}

Player
{
	name "Damien"
	describe "Few would mistake Damien Jones for a chartered accountant. His physique suggests the Undead, and his wardrobe suggests a failed lion-tamer.\nHe wears an accountant-style white button-down shirt, but half of it is missing. His skin underneath is criss-crossed with what might almost be claw marks, and bizarre patterns have been burned into the skin around his back. He wears a stylish pince-nez, but the left lens has shattered. Bits of organic matter hang from his finger tips, but he doesn't seem to mind.\n\nHe seems entirely determined to accomplish one goal and one goal only -- to ignore it all, and pray everything returns to nromal."
	gender m
	theme "default"
	feature "divunal.damien.Gate"
	thing "oldlocation" "Obscure Corner of Bookstore"
	boolean "isLit" false
	extends "Class_Human"
	ability "divunal.damien.Gate"
	ability "divunal.common.author.DarkDescribe"
	architect
	passwd "DaO16XBrpjVDo"
}

Room
{
	name "Chateau Attic(4)"
	describe "A Chateau Attic looking as if it needs to be described."
	place "Inheritance"
	theme "dark"
	exit "north" to "Chateau Attic(3)"
}

Room
{
	name "Chateau Attic(3)"
	describe "A Chateau Attic looking as if it needs to be described."
	place "Inheritance"
	theme "dark"
	exit "south" to "Chateau Attic(4)"
	exit "east" to "Chateau Attic"
}

Room
{
	name "Chateau Attic(2)"
	describe "A Chateau Attic looking as if it needs to be described."
	place "Inheritance"
	theme "dark"
	exit "south" to "Chateau Attic(1)"
}

Room
{
	name "Chateau Attic(1)"
	describe "A Chateau Attic looking as if it needs to be described."
	place "Inheritance"
	theme "dark"
	exit "north" to "Chateau Attic(2)"
	exit "west" to "Chateau Attic"
}

Room
{
	name "Chateau Stairwell"
	describe "A Chateau Stairwell looking as if it needs to be described."
	place "Inheritance"
	theme "greystone"
	exit "down" to "Chateau Basement"
	exit "north" to "Chateau Pantry"
}

Thing
{
	name "dirty bullet"
	describe "It appears to be a dirty bullet, but it is vague, indistinct, and little more than a blurry smear on reality."
	place "Colt 1911 pistol clip"
	string "bullet type" ".45 ACP"
	syn "bullet"
}

Thing
{
	name "class_simple book"
	describe "It appears to be a class_simple book, but it is vague, indistinct, and little more than a blurry smear on reality."
	place "Book Box"
	feature "twisted.reality.plugin.Read"
}

Room
{
	name "Forest Clearing"
	describe "A Forest Clearing looking as if it needs to be described."
	place "Inheritance"
	theme "leaf"
	exit "south" to "Wooded Grove"
}

Room
{
	name "Garden Maze(11)"
	describe "This part of the maze feels *very* strange, almost as if its a dead end...but there are exits all around!"
	theme "leaf"
	string "name" "Garden Maze"
	exit "north" to "Garden Maze(6)"
	exit "east" to "Garden Maze(9)"
	exit "south" to "Garden Maze"
	exit "west" to "Garden Maze"
}

Thing
{
	name "pair of brown leather boots"
	describe "A rather nondescript pair of brown leather boots."
	place "Agatha"
	boolean "clothing worn" true
	string "clothing appearance" "leather boots"
	extends "Class_Shoes"
	component
	syn "boots"
	syn "brown boots"
}

Location
{
	name "class_pistol chamber"
	describe "A blue box."
	place "Tenth's Chamber"
}

Thing
{
	name "phaser"
	describe "A smooth grey device, shaped in such a way as to rest easily in the palm of your hand. It terminates in a small, glossy black protrusion, and has no visible controls or attachments."
	place "dark green overcoat"
	feature "divunal.tenth.TiringVerb"
	string "name" "oblong plastic device"
	syn "device"
	syn "plastic device"
}

Room
{
	name "Mansion Coat Room"
	describe "A spacious walk-in closet which seems somewhat bigger than it does when observed from the outside. There are a number of wrought iron coathooks set into the walls at shoulder level, and a series of boot racks along the edges of the floor."
	theme "wood"
	exit "east" to "Mansion Entrance Hall"
}

Room
{
	name "Great Dome"
	describe "Upon entering this room, you might mistake it for the out-of doors - except for the marble flooring and the walls. Those walls and that floor are cracked in many places, and were it not for the sturdy marble pillars holding the walls up, it would seem a very unstable structure indeed.  Far, far above where you stand you can see a dome, partially obscured by the clouds beneath it.  The dome is a crystal blue color, and though one would assume the sky must lie beyond it, it is impossible to see.  Two exits, northeast and southwest, are completely blocked by rubble, and there are doors to the west, east, and northeast."
	theme "greystone"
	exit "northeast" to "Armory"
	exit "west" to "West End"
	exit "north" to "Crumbling Library"
	exit "east" to "Less Crumbling Hallway"
}

Thing
{
	name "iron door"
	describe "An rather nondescript iron door."
	place "Cold Room"
	boolean "obstructed" false
	extends "Class_Door"
	component
}

Room
{
	name "Temple Triangle Room"
	describe "This room is spacious, but low ceilinged.  It is cylindrical, but the main focus of the room's geometry seems to be a triangle.  Three statues, each slightly larger than life, are placed near the edges of the room, facing inward.  The statues are all composed of a gleaming, smooth white material.  There is a tall statue of a man holding a hemisphere, a short statue of a man holding a book, and a strong statue of a man holding a bone."
	theme "default"
	string "name" "Triangle Room"
	exit "down" to "Temple Middle Floor"
}

Thing
{
	name "floozle"
	describe "This appears to be a sort of musical instrument.  It has 14 different horns on it, each of which is vibrating slightly.  It is cycling slowly through the colors of the rainbow.  Touching it is slightly painful."
	place "Jedin"
}

Room
{
	name "Wet Floor"
	describe "You gasp in shock as your foot enters a very cold pool of water. The pool is not very deep here, but it is certainly cold. There is a breeze here, too, but it seems to be moving eastward."
	theme "greystone"
	string "name" "A Dark Place"
	string "description" "It's too dark in here to see!"
	boolean "inhibit_exits" true
	boolean "inhibit_items" true
	extends "Class_Dark Room"
	opaque
	shut
	exit "east" to "Cold Floor"
	claustrophobic
}

Thing
{
	name "gondola pager(1)"
	describe "This bell is crafted out of some silver material. It looks perfectly balanced, and one can imagine how sweet it sounds."
	place "Western End of Grotto"
	feature "divunal.rikyu.SummonGondola"
	string "name" "small bell"
	syn "bell"
	syn "pager"
	syn "small bell"
}

Thing
{
	name "fourth knob"
	describe "Fourth knob from the top of the qin with which to tune the instrument."
	place "qin"
	component
	syn "knob4"
	syn "knob"
}

Thing
{
	name "Class_Spell Book"
	describe "A rather nondescript Class_Spell Book."
	place "Book Box"
	feature "divunal.magic.SpellRead"
	feature "divunal.magic.SpellLearn"
}

Room
{
	name "Darkened Road(3)"
	describe "The road has given way to a narrow, forgotten path through the trees, overgrown with ferns and dark, waving grass. The trees seem to have grown together into a single, writhing mass above the road."
	place "Inheritance"
	theme "leaf"
	string "name" "Darkened Road"
	exit "east" to "Darkened Road(2)"
}

Room
{
	name "Darkened Road(2)"
	describe "A faint trail through the woods that may once have been a dirt road, leading off into darkness to the east and west. It is bordered by a steep ridge to the north, and the crumbling remains of a stone wall to the south, overgrown with ferns and odd looking plants. The trees form an almost solid wall of leaves and clawlike branches above the road, shutting out the sky."
	place "Inheritance"
	theme "leaf"
	string "name" "Darkened Road"
	exit "west" to "Darkened Road(3)"
	exit "east" to "Country Road(4)"
}

Thing
{
	name "registry"
	describe "A very informative piece of work."
	place "Maxwell"
	feature "divunal.rikyu.WhoWhere"
	feature "divunal.rikyu.Replace"
	thing "replace" "great bookshelf"
	string "name" "yellow paperback book"
	syn "book"
	syn "phonebook"
	syn "yellow book"
	syn "paperback book"
	syn "paperback"
	syn "yellow paperback book"
}

Thing
{
	name "take-out carton"
	describe "Aside from a few grains of pork fried rice and a splash of grease, this carton is completely empty."
	place "Proper English Library"
	syn "carton"
	syn "chinese food"
	syn "food"
}

Room
{
	name "Darkened Road(1)"
	describe "The road twists and turns through the narrow space allotted by the trees, which have grown even closer together overhead, shutting out the light from the sky. The stone wall is only a scattered pile of stones at this point, leaving the road open to the darkness of the forest to the south."
	place "Inheritance"
	theme "leaf"
	string "name" "Darkened Road"
	exit "west" to "Darkened Road"
}

Thing
{
	name "Cliffs of Insanity"
	describe "This is a very high, very wide rock wall, blocking your passage further north.  Someone has scrawled a passage on the wall in a very thin line of white paint:\n\n\t\"The profession of book-writing makes horse racing seem like a solid, stable business.\n\t\t-- John Steinbeck\"\n\nThe word \"John\" is underlined several times."
	place "Northern End of Small Forest"
	component
	syn "rock wall"
	syn "wall"
	syn "rock"
	syn "writing"
	syn "cliff"
	syn "cliffs"
}

Player
{
	name "Intuitive Guest"
	describe ""
	boolean "score init" true
	int "score max" 1024
	int "score" 0
	string "adjective" "Intuitive"
	extends "Class_Guest"
	syn "guest"
	passwd ""
}

Room
{
	name "Aisle 3."
	describe "You are in an aisle filled with miscelleneous types of books, all stacked together on shelves with no apparent organization. You can exit into a wider aisle to the south, or continue on to an unusual curve to the north."
	theme "paper"
	exit "south" to "Main Aisle, West End"
	exit "north" to "Odd Curve"
}

Room
{
	name "Wooded Grove"
	describe "A Wooded Grove looking as if it needs to be described."
	place "Inheritance"
	theme "leaf"
	exit "north" to "Forest Clearing"
	exit "south" to "Back Lawn(5)"
}

Room
{
	name "Tight Squeeze"
	describe "You can just barely fit into this section. Fortunately it seems to get a little wider to the south and to the east. \nThere is so much dust on the floor here that you can barely even see the stones under your feet."
	theme "paper"
	exit "south" to "Wider Area"
	exit "east" to "Small Section"
}

Room
{
	name "Myth Section"
	describe "This is a room dedicated to the preservation of myths. Stone statues punctuate the shelves occasionally, and all of the books look ancient and very important. They are in as good a condition as could be expected for their great age and apparently frequent use. There is a pillar in the center of the room here with nothing on it, and a door to the north. A shadowy corner to the southwest has a small sign hanging over it that says \"Occult Myths\". An unmarked corrider wanders off westward."
	theme "paper"
	exit "north" to "Bookstore Stairwell, Level 9"
	exit "west" to "Unmarked Corridor"
	exit "southwest" to "The Twisty Bit"
}

Location
{
	name "Ford Runabout Trunk"
	describe "The Runabout's trunk is open, revealing a bare, dirty steel compartment."
	place "Ford Runabout"
	feature "inheritance.car.OpenCloseTrunk"
	feature "inheritance.car.TrunkBlock"
	string "closed description" "The back end of the Runabout consists primarily of a lumpy metal trunk suspended over the back wheels. It is currently closed."
	string "open description" "The Runabout's trunk is open, revealing a bare, dirty steel compartment."
	component
	syn "rounded trunk"
	syn "ford trunk"
	syn "runabout trunk"
	syn "trunk"
}

Room
{
	name "Garden Maze(10)"
	describe "This part of the maze narrows so much, you can barely squeeze through, but it does feature a large trellis at the northern end. The eastern and western exits are ensconced by large stone arches."
	theme "leaf"
	string "name" "Garden Maze"
	exit "west" to "Garden Maze(9)"
	exit "north" to "Garden Maze(12)"
	exit "east" to "Garden Maze(11)"
	exit "south" to "Garden Maze(8)"
}

Thing
{
	name "Rock Especially for MAXWELL"
	describe "A rather nondescript rock.\nYET..... There is writing on it!!!\n\"MAXWELL!!! WHY DO I HAVE WOODEN PENCIL?!!!!\""
	place "Main Aisle, Center"
	syn "maxwell's rock"
	syn "rock"
}

Room
{
	name "Unfinished Room"
	describe "An Unfinished Room, looking like some kind of crazy Tool video or something."
	place "Inheritance"
	theme "dark"
	exit "west" to "Antiques Room"
}

Thing
{
	name "Kakemono"
	describe "The scroll is covered with strange characters."
	place "Tea House"
	feature "divunal.magic.SpellLearn"
	feature "divunal.rikyu.Posess"
	feature "divunal.bookstore.TrivialRead"
	string "spell 1" "Posess"
	string "book text" "The scroll is covered with strange characters. However, you find yourself magically able to understand them..."
	component
	syn "scroll"
}

Room
{
	name "Aaron's test room"
	describe "A large bowl of Green Jello(tm)"
	extends "Class_Dark Room"
	exit "up" to "another test room(1)"
}

Thing
{
	name "dazzling necklace"
	describe "The necklace dazzles the eye, even wihte walls bear witness to its light."
	place "Agatha"
	string "name" "necklace"
	boolean "clothing worn" true
	extends "Class_Necklace"
	component
	syn "agatha's necklace"
}

Room
{
	name "Rock Pile"
	describe "This is a cramped cave under a huge pile of boulders. The boulders are supported by wooden posts, much like those you would expect to see in a mine shaft. There is a hole in the ground here. A rope ladder hangs down the hole."
	theme "crack"
}

Location
{
	name "armchair"
	describe "An rather nondescript armchair."
	place "Smoking Room"
	int "maximum occupancy" 1
	string "preposition" "in"
	string "player preposition" "sitting in"
	extends "Class_Sittable"
	syn "chair"
	broadcast
}

Thing
{
	name "psyche dial"
	describe "A white box."
	place "Genetic Laboratory"
	float "value" "0.0"
	extends "Class_Player Creation Dial"
	component
	syn "psyche"
	syn "dial"
}

Thing
{
	name "steam engine magic switch"
	describe "A large, y-shaped metal switch with a black handle. It can be switched to either of two positions, labeled \"Magic\" and \"More Magic\", respectively."
	place "Mansion Basement Engine Room"
	feature "divunal.tenth.SteamEngineFlip"
	thing "steam source" "Mansion Steam Engine"
	component
	syn "throw-switch"
	syn "switch"
	syn "steam engine switch"
}

Location
{
	name "Class_Closeable Container"
	describe "A blue box."
	place "General Box"
	feature "twisted.reality.plugin.OpenCloseContainer"
	extends "Class_Container"
}

Thing
{
	name "demo center painting of tenth"
	describe "A framed portrait of a slender young man with bright green eyes and a calm, thoughtful face. His hair is an odd, coppery shade of blonde, and falls nearly to his waist in gentle waves. He is dressed in a dark green victorian style frock coat, and the painting has caught him in the act of studying a large brass pocketwatch."
	place "Demo Center East Wing"
	feature "demo.PagerPress"
	thing "reciever" "Tenth"
	
	property "description" "demo.PaintingDescription"
	string "name" "Painting of Tenth"
	component
	syn "black button"
	syn "small button"
	syn "small black button"
	syn "page button"
	syn "button"
	syn "painting of tenth"
	syn "painting"
	syn "picture"
	syn "portrait"
}

Thing
{
	name "elvish sword of great antiquity"
	describe "This sword is elvish.  You can tell by the runes carved into the blade and hilt.  It is made of a perfectly mirrored metal, which, although you can guess that it is old by the quality craftsmanship and baroque style to the curves of the hilt, is completely undamaged by age."
	mood "providing light"
	place "Maxwell"
	boolean "frotzed" true
	boolean "isLit" true
	descript "lighting" {"A pure white glow eminates from ", Name of("elvish sword of great antiquity"), ", bathing ", Pronoun of("elvish sword of great antiquity"), " in light."}
	syn "sword"
	syn "elvish sword"
}

Room
{
	name "Damien's Cubicle"
	describe "A few objects come to your attention when you first enter the cubicle: a snazzy black laptop, an executive toy, an analog clock, and a small framed photograph. Everything else here is difficult to make out -- instead of catching your eye most of the items in this room do the opposite. There is some sort of chair here, a notice or calendar on the cubical wall, and a pile of things on the floor. None of them look very important.\n\nThe cubicle walls have also been filled in at the corners. There is no trace of plaster here, instead the corners are filled with the smooth, sticky substance."
	exit "south" to "Damien's Office,leaving"
}

Thing
{
	name "sliding glass doors"
	describe "A pair of sliding glass doors set into the wall."
	place "Demo Center West Wing Lobby"
	feature "demo.AutomaticDoor"
	boolean "obstructed" true
	string "thereCloseDesc" "A pair of sliding glass doors stand shut in the northern wall."
	string "closeDesc" "A pair of sliding glass doors stand shut in the southern wall."
	string "thereOpenDesc" "An open, black framed doorway leads north."
	string "openDesc" "An open, black framed doorway leads south."
	string "close message" "The doors slide shut."
	string "openDescription" "An open doorway set into the wall."
	string "closedDescription" "A pair of sliding glass doors set into the wall."
	handler "startup" "demo.AutomaticDoorCloser"
	handler "door close" "demo.AutomaticDoorCloser"
	extends "Class_Door"
	component
	syn "north"
	syn "south"
	syn "door"
	syn "doors"
	syn "glass doors"
}

Location
{
	name "sphere chair"
	describe "A lovely sphere to sit on."
	place "Blake's Sphere"
	feature "twisted.reality.plugin.furniture.Stand"
	feature "twisted.reality.plugin.furniture.Sit"
	string "player preposition" "sitting on"
	string "preposition" "on"
	int "maximum occupancy" 1
	syn "chair"
	broadcast
}

Thing
{
	name "message post"
	describe "A crystal clear screen is before you, and shimmering ethereally, written in dark, dripping blood is:    Come follow me into my eternal realm, where the shadows of dusk and dawn are perpetual.  Dare ye dig in my sanctuary...watch well yer back fer ye will find me personally hunting ye down..."
	place "Silver Shadowed Glade"
	component
}

Location
{
	name "Class_Container"
	describe "A generic container."
	place "General Box"
	feature "twisted.reality.plugin.Put"
}

Location
{
	name "demo gift shop shelves"
	describe "The shelves are geometrically perfect arrangements of wooden boards, forming large, rectangular... shelves. Collectively, there is enough space to hold quite a few gifts, but they are strangely bare, except for the few things no one would want."
	place "Demo Center Gift Shop"
	feature "twisted.reality.plugin.Put"
	string "preposition" "on"
	string "name" "shelf"
	component
	syn "shelves"
	syn "shelf"
	broadcast
}

Thing
{
	name "Class_Smokeable"
	describe "A rather nondescript Class_Smokable."
	place "Smoking Room"
	feature "divunal.rikyu.SmokePipe"
	string "othersHearPrepare" "$m fills up the $t with fine tobacco."
	string "subjectHearsSmoke" "You puff away on the $t ."
	string "othersHearSmoke" "$m puffs away on the $t ."
	string "unlitPipe" "The $t isn't lit!"
	string "emptyPipe" "The $t is empty. You need to prepare it."
	string "alreadyPrepared" "The $t is already prepared."
	string "subjectHearsPrepare" "You fill up the $t with fine tobacco."
	string "alreadyLit" "The $t is already lit."
	string "othersHearLight" "$m lights the $t ."
	string "subjectHearsLight" "You light the $t ."
	handler "extinguish" "divunal.rikyu.ExtinguishHandler"
	component
}

Room
{
	name "Aisle 2."
	describe "A series of short, squat books sit on the shelves here. All the books look the same. The aisle ends abruptly to the north, almost in the middle of a shelf, in a wall. The wall isn't quite straight, and this place looks poorly maintained. You can exit the aisle to your south."
	theme "paper"
	exit "south" to "Main Aisle, Center"
}

Thing
{
	name "demo center bathroom door"
	describe "A blue metal door, designed to be pushed open easily from either side. It is labeled \"Players\" just above the icon of a gender-neutral stick figure."
	place "Demo Center East Wing"
	feature "twisted.reality.author.Obstruct"
	feature "twisted.reality.plugin.door.OpenCloseSwingingDoor"
	string "name" "blue swinging door"
	component
	syn "blue swinging door"
	syn "blue door"
	syn "swinging door"
	syn "door"
}

Room
{
	name "Demo Center West Wing Lobby"
	describe "A circular room, with bright, white walls and a polished black marble floor. The lobby joins a pair of hallways to the east and west, and has a rectangular doorway cut into the north wall, labeled \"Gift Shop\". Several grey plastic chairs are built into the floor around the edges of the room, but they don't look particularly comfortable."
	place "Demo"
	descript "sliding glass doors closeDesc" "A pair of sliding glass doors stand shut in the southern wall."
	exit "south" notTo "Science And Technology Demo Center" with "sliding glass doors"
	exit "north" to "Demo Center Gift Shop"
	exit "west" to "Demo Center West Wing"
	exit "east" to "Demo Information Center"
}

Room
{
	name "Castle Entrance Archway"
	describe "You stand under a very large white stone archway in the walls of a castle.  You notice that the western wall seems a bit ashen and grey, while the eastern one is bright and gleaming.  To the south, you can continue further into the castle, where there is a small courtyard.  You can exit the castle to the north, onto a set of steps."
	string "name" "Entrance Archway"
	exit "north" to "Castle Steps"
	exit "south" to "Castle Courtyard"
}

Room
{
	name "Garden Maze"
	describe "You are in a medium-sized clearing. To the north, there is a tall hedge with a single opening in it. A sign has been placed in the ground near the hedge, next to which is a large red button."
	theme "leaf"
	exit "east" to "Outer Tea Garden"
	exit "north" to "Garden Maze(1)"
}

Room
{
	name "chasm"
	describe "This is the bottom of a deep chasm.  There is not much light, but you can tell that there is no way to climb back up. Maybe you shouldn't have jumped down here?\n\nObvious Exits:\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
}

Room
{
	name "Wrecked Street, postwall"
	describe "This is a nondescript cuved street, which looks as if thousands of small rocks had bombarded it at high velocity, leaving pockmarks."
	theme "crack"
	string "name" "Wrecked Street"
	exit "northwest" to "Wrecked Street"
	exit "south" to "Wrecked Alleyway"
}

Thing
{
	name "frobozz magic reality altering appliance"
	describe "This generic reality altering appliance bears a striking resemblance to a pencil.  It bears the Frobozz Magic Reality Company logo."
	place "Guyute"
	feature "twisted.reality.author.FloatSet"
	feature "divunal.common.author.CreateBox"
	extends "Reality Pencil"
	syn "appliance"
}

Thing
{
	name "demo center things no one would want"
	describe "There are a few really worthless things no one would want on the shelves... But really, you don't want them. Would you really want a jar-jar binks pez dispenser? Honestly, now."
	place "Demo Center Gift Shop"
	string "name" "things no one would want"
	component
	syn "things"
	syn "things no one would want"
	syn "things no one wants"
	syn "stuff"
}

Thing
{
	name "Class_Forbidden Exit"
	describe "A rather nondescript Class_ForbiddenExit."
	place "Underground Grotto"
	feature "twisted.reality.author.Obstruct"
	boolean "obstructed" true
	component
}

Thing
{
	name "Tax Guide"
	describe "Pro-Dis Form 6900A -- the Easy Way\n\nIf you are a wage-gaining corporation, and you may have high-end yield bonus in the 1 to 2 million ranges, then things are going to change for you! As of March, the government has released Form 6900A, which is mandatory under certain conditions...\n\nIt continues on in this fashion for some time."
	place "Damien's Cubicle"
	syn "guide"
	syn "tax"
}

Thing
{
	name "organic stuff"
	describe "A bit of organic... stuff. Some of this goop looks like a spider's thread, while in other places it seems more like carpenter's plaster. In all cases it is smooth, slightly sticky, and strong as hell."
	place "Damien's Study"
	component
	syn "organic"
	syn "stuff"
	syn "thread"
	syn "goop"
}

Room
{
	name "Behind House"
	describe "You are behind the white house. A path leads into the forest to the east. In one corner of the house there is a small window which has had the shutters pulled off of it, ruined beyond repair."
	exit "west" to "Kitchen(1)"
	exit "east" to "Clearing 2"
	exit "southwest" to "South of House"
	exit "northwest" to "North of House"
}

Thing
{
	name "pair of metal-rimmed spectacles"
	describe "A rather nondescript metal-rimmed spectacles."
	place "glasses case"
	feature "divunal.rikyu.XRayVision"
	boolean "clothing worn" false
	string "clothing location" "face"
	extends "Class_Clothing"
	syn "xray glasses"
	syn "metal-rimmed glasses"
	syn "glasses"
	syn "spectacles"
}

Thing
{
	name "greyish cloth"
	describe "A greyish cloth of thick, finely-woven linen."
	place "Yumeika"
	string "clothing location" "left eye"
	string "clothing location 2" "right eye"
	string "clothing appearance" "a greyish cloth bound tightly across her eyes"
	boolean "clothing worn" true
	extends "Class_Clothing"
	component
	syn "cloth"
}

Location
{
	name "beastly fido"
	describe "The beastly fido is a medium sized dog who scavenges wherever it goes. It is harmless, but sometimes annoying."
	place "Cold Room"
	gender m
	boolean "wandering" false
	handler "wander" "divunal.rikyu.WanderHandler"
	syn "fido"
}

Room
{
	name "Jewel Bedecked Hallway 2"
	describe "This is a hallway lined with hundreds of different colors of jewels.  Upon closer inspection, the walls are inlaid with them, so they appear both smooth and jeweled at once.  A gold arch leads west, a silver one east, and onyx ones north and south."
	theme "default"
	string "name" "Jewel Bedecked Hallway"
	exit "north" to "Black Hallway"
	exit "east" to "Silver Room"
	exit "west" to "Gold Room"
	exit "south" to "Jewel Bedecked Hallway"
}

Thing
{
	name "brass lantern"
	describe "This lamp is so battered and bruised, having survived so many adventures, that it's a wonder it survives at all. It is currently on and the switch is stuck, so you can't turn it off!"
	place "Genetic Laboratory"
	boolean "isLit" true
	syn "light"
	syn "lantern"
	syn "lamp"
	syn "brass"
}

Thing
{
	name "display"
	describe "There is a photograph of a man breathing fire -- quite an impressive shot, really. Underneath it are the remains of a keyboard draped artistically across the door."
	place "Mod Seven Short Hallway"
	component
}

Thing
{
	name "agility dial"
	describe "A white box."
	place "Genetic Laboratory"
	float "value" "0.25"
	extends "Class_Player Creation Dial"
	component
	syn "agility"
	syn "dial"
}

Thing
{
	name "hat"
	describe "A rather nondescript hat."
	place "demo center wastebasket"
	boolean "clothing worn" false
	extends "class_hat"
}

Thing
{
	name "pair of silk pants"
	describe "A rather nondescript silk pajamas."
	place "Rikyu"
	boolean "clothing worn" true
	extends "Class_Pants"
	component
	syn "pants"
	syn "silk pants"
}

Room
{
	name "Aisle 1."
	describe "An array of important-looking tomes of different shapes and sizes are displayed on the shelves here. Each is titled with the name of a geographical location - the smaller ones, cities and towns, the larger ones, provinces and countries. You can exit the aisle to the south and there is a marble arch in the wall at the north end of the aisle, holding a stainless steel door."
	theme "paper"
	descript "stainless steel door closeDesc" "A large steel door blocks the northern exit."
	exit "north" notTo "Grand History Book Room" with "stainless steel door"
	exit "south" to "Main Aisle, East End"
}

Room
{
	name "Outside the Mods"
	describe "You are standing in a break in the line of trees. To the north it is forrest, to the south an open plane. Far to the south you can make out the Library Building, and in the north there are a few round buildings with multiple doors."
	exit "north" to "Pathway"
	exit "south" to "The Middle of the Field"
}

Thing
{
	name "clue scissors"
	describe "A pair of stainless steel scissors. The blades bear the words \"BookeNZ Scissor Factories.\""
	place "Garden Maze(1)"
	string "name" "scissors"
	component
	syn "scissors"
}

Room
{
	name "Gravel Driveway"
	describe "The bottom end of a long gravel driveway, leading towards a dark, imposing mansion. Vast fields of corn rise up on either side, brittle and yellow with age. Further to the north, the driveway splits into a circular parth in the courtyard of the mansion, while to the south, it continues uphill towards a distant forest."
	place "Inheritance"
	theme "leaf"
	exit "south" to "Gravel Driveway(1)"
	exit "north" to "Circular Driveway"
}

Thing
{
	name "demo center bathroom stall door"
	describe "It appears to be a demo center bathroom stall door, but it is vague, indistinct, and little more than a blurry smear on reality."
	place "Demo Center Lavatory"
	feature "twisted.reality.author.Obstruct"
	boolean "obstructed" false
	string "closeDesc" "To the east, a single bathroom stall is separated from the rest of the room by a black metal door and a similar set of dividers."
	string "openDesc" "To the east, the door to the single bathroom stall stands open."
	string "name" "bathroom stall door"
	string "thereOpenDesc" "The stall door stands open, leading out into the bathroom."
	string "thereCloseDesc" "The stall door is closed, and there is a large notice posted on the wall just to the right of it."
	extends "Class_Door"
	component
	syn "door"
	syn "stall"
	syn "stall door"
	syn "bathroom stall door"
}

Thing
{
	name "dark black cloak"
	describe "A rather nondescript dark black cloak."
	place "Guyute"
	boolean "clothing worn" true
	extends "Class_Cape"
	component
	syn "cloak"
	syn "black cloak"
}

Thing
{
	name "shiny clasp for right front pocket"
	describe "A shiny clasp that closes the right front pocket."
	component
	syn "right clasp"
	syn "clasp"
}

Room
{
	name "Empty Hallway North"
	describe "This is an empty north/south hallway.  There are no doors here, only wooden floor and white-painted walls.  The northern wall appears to have been slightly singed by a circular fire.  The hallway continues some distance to the south."
	string "name" "Empty Hallway"
	exit "south" to "Empty Hallway"
}

Room
{
	name "Mansion Stairwell"
	describe "A tall, cylindrical room with a polished marble floor.  A massive wrought iron spiral staircase runs through the center of the room, leading both up and down for quite some distance. Simple arched doorways are set into the east and west walls, leading out of the room."
	theme "wood"
	exit "down" to "Mansion Basement"
	exit "up" to "Upper Mansion Stairwell"
	exit "west" to "Mansion Upper Hallway"
	exit "east" to "Mansion Upper Hall"
}

Thing
{
	name "green thing"
	describe "You're not exactly sure, but this stuff looks a lot like Green Jello.  But that would be copyright infringement, so that just can't be.  It looks kind of jiggly."
	place "Aaron's test room"
	syn "jello"
	syn "stuff"
	syn "green jello"
	syn "thing"
}

Room
{
	name "Silver Shadowed Fields"
	describe "Endless fields of flowers and silverbladed grass.  The perfumed scent haning in the air is stronger here, making you feel slighlty dizzy.  "
	theme "leaf"
	exit "north" to "Silver Shadowed Clearing"
	exit "northwest" to "Silver Shadowed Clearing"
	exit "southwest" to "Silver Shadowed Glade"
}

Thing
{
	name "reference manual"
	describe "A Friendly Guide to Form 6900A.\n\nDept. Clarification and Simplification\nBureau 923100-A6, Section 23\nInternal Revenue Service"
	place "Damien's Study"
	syn "manual"
	syn "reference"
}

Room
{
	name "Chateau Antechamber"
	describe "A dark, poorly described place. There should also be a table or something, with your Great-Uncle's Letter on it."
	place "Inheritance"
	theme "greystone"
	exit "east" to "Chateau Hallway(16)"
	exit "up" to "Chateau Staircase"
	exit "west" to "Chateau Hallway"
	exit "south" to "Chateau courtyard"
}

Player
{
	name "James"
	describe "A lean, solemn looking young man with bright yellow eyes, flowing bright red hair, and a pale complexion. "
	place "Class Room"
	gender m
	thing "oldlocation" "Class Room"
	
	persistable "clothing right leg" "twisted.reality.Stack" val "thing pair of dark blue shorts\n" key "twisted.reality.Stack@5855432"
	
	persistable "clothing left leg" "twisted.reality.Stack" val "thing pair of dark blue shorts\n" key "twisted.reality.Stack@5855450"
	
	persistable "clothing right foot" "twisted.reality.Stack" val "thing pair of sandles\n" key "twisted.reality.Stack@5855414"
	
	persistable "clothing left foot" "twisted.reality.Stack" val "thing pair of sandles\n" key "twisted.reality.Stack@58553dd"
	
	persistable "clothing right arm" "twisted.reality.Stack" val "thing shirt with an owl insignia\n" key "twisted.reality.Stack@58553f6"
	
	persistable "clothing left arm" "twisted.reality.Stack" val "thing shirt with an owl insignia\n" key "twisted.reality.Stack@58553ba"
	
	persistable "clothing chest" "twisted.reality.Stack" val "thing shirt with an owl insignia\n" key "twisted.reality.Stack@5855383"
	float "dexterity" "0.0"
	float "endurance" "0.0"
	float "agility" "0.0"
	float "strength" "0.65"
	float "memory" "0.0"
	float "psyche" "-0.05"
	descript "clothing" {Pronoun of("James"), " is wearing ", Name of("shirt with an owl insignia"), ", ", Name of("pair of dark blue shorts"), ", ", "and ", Name of("pair of sandles"), "."}
	extends "Class_Human"
	ability "divunal.common.author.Visit"
	ability "divunal.james.Who"
	ability "divunal.james.Recall"
	architect
	passwd "Ja3HyQwS9J.XQ"
}

Room
{
	name "RCC Reception Desk"
	describe "A disgruntled receptionist sits here at a desk, undoubtedly waiting to check your I.D. and make sure that you don't get in without one. There are stairs that you could probably ascend without incurring any wrath, but the path to the north looks closed to all but bona-fide students."
	exit "south" to "RCC Entrance Hall"
	exit "up" to "RCC Rec Area West"
}

Room
{
	name "Dark River Tunnel(2)"
	describe "A Dark River Tunnel looking as if it needs to be described."
	theme "water"
	string "name" "Dark River Tunnel"
	boolean "needsBoat" true
	exit "south" to "Dark River Tunnel(1)" with "tunnelX4"
}

Room
{
	name "Dark River Tunnel(1)"
	describe "A Dark River Tunnel looking as if it needs to be described."
	theme "water"
	string "name" "Dark River Tunnel"
	boolean "needsBoat" true
	exit "north" to "Dark River Tunnel(2)" with "tunnelX4"
	exit "south" to "Dark River Tunnel" with "tunnelX3"
}

Room
{
	name "Autumn Chamber"
	describe "The ground here is a bed of slightly crisp leaves.  The walls are covered with a tapestry of rich browns and reds, abstract, but nevertheless reminiscent of the season.  The air is cool and clean, and smells of the forest. On the east wall, a large rectangular window overlooks a forest of pine trees, whose needles have turned an interesting array of bright colors.  "
	exit "west" to "Cylindrical Mansion Hallway"
}

Room
{
	name "Castle Greysen Fountain Room"
	describe "The floor here is made of a black glossy material, but the center of the floor is dominated by a huge inlaid compass.  The arms of the compass are all silver, except the eastern one, which is a shining gold.  The western arm is very slightly tarnished. A large circle in the center of the compass is depressed into the floor, and a fountain is in the center of the depression."
	string "name" "Fountain Room"
	exit "west" to "Sitting Room"
	exit "southeast" to "East Wing Spiral Staircase Bottom"
}

Room
{
	name "Canyon Bottom"
	describe "You are beneath the walls of the river canyon which may be climbable here. The lesser part of the runoff of Aragain Falls flows by below. To the north is a narrow path."
	exit "north" to "End of Rainbow"
	exit "up" to "Rocky Ledge"
}

Room
{
	name "Odd Curve"
	describe "You stand in an odd curve in an aisle of books.  The hallway twists as if it were curving about a large mass to the southeast. There is a door at the end of the aisle to the northeast labled \"stairs\" and to the south, the passage straightens out and continues."
	theme "paper"
	exit "south" to "Aisle 3."
	exit "northeast" to "Bookstore Stairwell, Level 7"
}

Room
{
	name "Forest"
	describe "This is a forest, with trees in all directions.  To the east, there appears to be sunlight."
	exit "north" to "Clearing"
	exit "east" to "Forest Path"
}

Thing
{
	name "pressed pair of black slacks"
	describe "A rather nondescript pressed pair of black slacks."
	place "Agatha"
	boolean "clothing worn" false
	extends "Class_Pants"
	syn "slacks"
	syn "black slacks"
}

Thing
{
	name "Class_Door"
	describe "This is a regular doorway.  You can OPEN and CLOSE it."
	place "General Box"
	feature "twisted.reality.author.Obstruct"
	feature "twisted.reality.plugin.door.Open"
	feature "twisted.reality.plugin.door.Close"
	boolean "obstructed" true
	string "obstructed message" "The door is closed.  You can't walk through it."
	syn "doorway"
	syn "door"
}

Room
{
	name "Mansion Study"
	describe "A spacious, open room with a high ceiling. A pair of high backed victorian chairs stand near the center of the floor, facing each other over a small, ornately carved wooden table. Glass windowed cabinets line the east and west walls, while arched doorways lead out of the room to the north and south."
	theme "wood"
	exit "north" to "Mansion Main Hall"
	exit "south" to "Steam-Powered Library"
}

Room
{
	name "Granite Reception Room"
	describe "This is a dark grey granite room with a section of the floor raised to form a semicircular reception desk.  No one is seated behind it.  On the southern wall, there is a door leading further into the office.  The west wall is entirely filled with bookshelves, and the east wall is solid, unbroken granite.  You can exit to a stairwell to the northwest."
	exit "south" to "Grey Cube Room"
	exit "northwest" to "Bookstore Stairwell, Level 5"
}

Thing
{
	name "Book of Patchwork"
	describe "The Book of Patchwork is open to page 1. It reads:\n\"Book of Patchwork (1:1) Dear reader, within these pages are fragments of the collective destiny of the twin books (the books of Patchwork - this is the main tome, Dingo, Clouds, Ivy, Rings, Nymphs, Euphoria, Lions, Tigers, and Labrinths). Be warned that improper use of their teachings can and will lead to spread of the glitch. As volumes of new readers misuse and fall prey... new books shall arrive. Take care... reader.\""
	place "Twin"
	string "page_#1" "Book of Patchwork (1:1) Dear reader, within these pages are fragments of the collective destiny of the twin books (the books of Patchwork - this is the main tome, Dingo, Clouds, Ivy, Rings, Nymphs, Euphoria, Lions, Tigers, and Labrinths). Be warned that improper use of their teachings can and will lead to spread of the glitch. As volumes of new readers misuse and fall prey... new books shall arrive. Take care... reader."
	string "page_#2" "Book of Euphoria (174:312) [Systematic proposal on the obliteration of frantic warfare in the <removed> together with numbers 1, 2, 4, and 9] On one three-dimentional afternoon, I decided to take a walk in the form of a nearby algorhythm. Little did i know, a glitch hid just around the corner...."
	int "page_number" 1
	extends "Class_Book"
	syn "book"
}

Thing
{
	name "titanium white table"
	describe "A white box."
	component
	syn "table"
}

Room
{
	name "Chateau Staircase"
	describe "A Chateau Staircase looking as if it needs to be described."
	place "Inheritance"
	theme "greystone"
	exit "up" to "Chateau Staircase Landing"
	exit "down" to "Chateau Antechamber"
}

Player
{
	name "Class_God"
	describe "This player is as-yet undescribed."
	place "Demo"
	extends "Class_Player"
	ability "twisted.reality.author.Refrump"
	ability "twisted.reality.author.Scrutinize"
	ability "twisted.reality.author.Gate"
	ability "twisted.reality.Armageddon"
	ability "twisted.reality.author.StringSet"
	ability "twisted.reality.author.Locate"
	ability "twisted.reality.Passwd"
	ability "twisted.reality.author.Property"
	ability "twisted.reality.author.DescriptSet"
	ability "twisted.reality.author.KillProp"
	ability "twisted.reality.author.Grab"
	ability "twisted.reality.author.ThingSet"
	ability "twisted.reality.author.Handle"
	ability "twisted.reality.author.Pause"
	ability "twisted.reality.author.Toss"
	ability "twisted.reality.author.MoodSet"
	passwd "--"
}

Thing
{
	name "solid oak door"
	describe "A rather nondescript Solid Oak Door."
	place "Grand History Book Room"
	string "closeDesc" "You see a solid oak door to the east."
	boolean "locked" false
	string "openDesc" "To the east, you see a well-lit, polished wood foyer."
	string "thereOpenDesc" "To the east, you see a large, marble room with a pedestal in its center, to which is chained a large book."
	string "thereCloseDesc" "You see a solid oak door to the east."
	boolean "obstructed" false
	extends "Class_Door"
	component
	syn "door"
	syn "oak door"
}

Player
{
	name "Blake"
	describe "A man of average height and medium build, with deep green eyes and cropped blond hair. He carries himself casually, but with an air of continual alertness. "
	gender m
	thing "oldlocation" "A Crumbling Stairway"
	
	persistable "clothing left leg" "twisted.reality.Stack" val "thing pair of tan cargo pants\n" key "twisted.reality.Stack@5855087"
	
	persistable "clothing right leg" "twisted.reality.Stack" val "thing pair of tan cargo pants\n" key "twisted.reality.Stack@585505d"
	
	persistable "clothing chest" "twisted.reality.Stack" val "thing dark green shirt\n" key "twisted.reality.Stack@58550b2"
	
	persistable "clothing left arm" "twisted.reality.Stack" val "thing dark green shirt\n" key "twisted.reality.Stack@585510a"
	
	persistable "clothing right arm" "twisted.reality.Stack" val "thing dark green shirt\n" key "twisted.reality.Stack@58550e4"
	
	persistable "clothing left foot" "twisted.reality.Stack" val "thing pair of sturdy leather boots\n" key "twisted.reality.Stack@585513f"
	
	persistable "clothing right foot" "twisted.reality.Stack" val "thing pair of sturdy leather boots\n" key "twisted.reality.Stack@585510f"
	descript "clothing" "He is wearing a dark green shirt, a pair of tan cargo pants, and a pair of sturdy leather boots."
	extends "Class_Human"
	architect
	passwd "BlRZcxZsyFPsA"
}

Room
{
	name "Broken Office"
	describe "This is an office, most likely that of someone in a relatively low position.  Bits of twisted metal lie about the floor, indicating that there may have once been some furniture here.  The walls are undecorated but for a few small, burnt holes, and the space is small.  The smashed remains of a computer terminal litter the floor."
	exit "north" to "Reception Area"
}

Room
{
	name "East Wing Spiral Staircase Bottom"
	describe "This is the bottom of a walled white marble spiral staircase.  There is a small open archway here to the northwest, with the word \"Lobby\" engraved above it."
	string "name" "Spiral Staircase"
	exit "northwest" to "Castle Greysen Fountain Room"
	exit "up" to "East Wing Spiral Staircase Top"
}

Thing
{
	name "pair of black dockers"
	describe "A white box."
	place "Test Bed"
	syn "black dockers"
	syn "dockers"
}

Thing
{
	name "Class_Necklace"
	describe "It appears to be a Class_Necklace, but it is vague, indistinct, and little more than a blurry smear on reality."
	place "Clothing Box"
	string "clothing location" "neck"
	extends "Class_Clothing"
}

Thing
{
	name "battered gray door"
	describe "A rather nondescript battered gray door."
	place "Michelle's Dorm Room"
	boolean "obstructed" false
	string "thereCloseDesc" "The east door is clearly closed."
	string "thereOpenDesc" "The east door is open."
	string "closeDesc" "The west door is closed."
	string "openDesc" "The west door is clearly open."
	extends "Class_Door"
	component
	syn "door"
}

Room
{
	name "Path beside the RCC"
	describe "A small asphalt pathway leads northward. To the east is the blank wall of the Robert Crown Center, and to the west is a small parking lot. To the north the pathway appraoches a road, and further in the distance there is what seems to be a fairly extensive forest."
	exit "north" to "Intersection"
	exit "south" to "Under Walkway"
}

Room
{
	name "Damien's Office,leaving"
	describe "You see a typical office cubicle littered with common-place office junk. The office looks to be some sort of banking or accountancy house, but it is difficult to make out any details. Maybe it's the lighting, but everything except the one cubicle seems dull and almost out of focus. In fact, the only detail that you can easily make out aside from the cubicle is that all of the corners to this room have been filled in with plaster. Now none of the walls meets at a right angle. This plaster has recently been augmented by an organic, sticky substance. The strands completely round out the edges, and seem to be incredibly strong.\n\nYou can go east, into a stack of books; you can exit through a steel grey door to the west; or you can enter  the cubicle to the north."
	string "name" "Damien's Office"
	exit "west" to "Damien's Bedroom"
	exit "east" to "Musty Section"
	exit "north" to "Damien's Cubicle"
}

Thing
{
	name "rickety spiral staircase"
	describe "The staircase is old and rusting.  It doesn't look very safe.  In fact it look outright dangerous.  You think to yourself \"Do I dare use those stairs!\". "
	component
	syn "staircase"
}

Thing
{
	name "Meredith's south wall"
	describe "A rather nondescript Meredith's south wall."
	place "Meredith's Hell Hole"
	component
	syn "swall"
}

Thing
{
	name "Meredith's north wall"
	describe "A rather nondescript Meredith's north wall."
	place "Meredith's Hell Hole"
	component
	syn "nwall"
}

Thing
{
	name "tea house helper"
	describe "A delightful little tea house. The walls are made of very thin paper, yet the house looks as if it might be difficult to enter."
	place "Inner Garden"
	feature "divunal.rikyu.TeaHouseOpen"
	string "name" "tea house"
	component
	syn "house"
	syn "tea house"
}

Thing
{
	name "staple gun"
	describe "A standard staple gun, painted red and wieldable with one hand.  It has the monogram \"10\" inlaid on its handle in gold."
	place "Mansion Laboratory"
}

Room
{
	name "Castle Foyer"
	describe "The polished white floor here is carpeted with a T of red carpet running from archways in the northern, eastern, and western ends of the room.  The southern wall is completely blank."
	theme "default"
	exit "east" to "Sitting Room"
	exit "north" to "Castle Entrance"
}

Room
{
	name "Robert Crown Center Cafe"
	describe "You stand next to a snack bar with a few tables. There is a railing here, which opens up into a stairwell to the north, where there is a recreational area with a few gaming tables like air-hockey and pool. To your west you can exit onto a glass walkway."
	exit "north" to "RCC Rec Area West"
	exit "west" to "Lounge Walkway"
}

Location
{
	name "humidor"
	describe "A humidor made out of expensive-looking teak wood. There's a glass window in the top through which many fine cigars can be seen."
	place "ornate wooden table"
	extends "Class_Closeable Container"
	opaque
	shut
}

Room
{
	name "Northern End of Small Forest"
	describe "This is the northern end of a small forest, where your way is blocked by a huge rock wall.  Looking upward, you can see the cliff extending up far into the clouds.  Someone has scrawled something in white paint at about eye-level on the cliff."
	theme "leaf"
	exit "south" to "Clearing in Small Forest"
}

Thing
{
	name "demo center guest t-shirt"
	describe "A cheap white cotton shirt with short sleeves. It is emblazoned with the word \"Guest\" in large, friendly letters."
	place "demo center gift shop racks"
	thing "repop" "demo center gift shop racks"
	string "clothing appearance" "a \"guest\" t-shirt"
	extends "Class_Shirt"
	syn "shirt"
	syn "t-shirt"
	syn "t"
	syn "tshirt"
	syn "guest t-shirt"
	syn "demo center"
	syn "demo"
}

Thing
{
	name "ethereal staff"
	describe "This staff is quite ornate, and stands at over six feet tall. The shaft is made from carved kemlar wood, straight out of the Great Forest.  At the top there is a large orb made of fine crystal. "
	place "Guyute"
	thing "teleport phrase my, it's musty in here" "Musty Section"
	thing "teleport phrase mind if I smoke?" "Smoking Room"
	thing "teleport phrase take me home" "Guyute's Laboratory"
	thing "teleport phrase learn me" "Class Room"
	string "teleport message" "The ethereal staff begins to glow an unearthly color."
	boolean "isLit" false
	handler "say" "divunal.maxwell.VoiceTeleport"
	syn "staff"
}

Thing
{
	name "lever"
	describe "A polished brass rod with a wooden handle, protruding from a similarly crafted socket set into the wall."
	place "Steam-Powered Library"
	theme "wood"
	feature "divunal.tenth.LibraryPull"
	thing "steam source" "Mansion Steam Engine"
	thing "target door" "bookshelf door"
	component
}

Room
{
	name "Agatha's Lighthouse"
	describe "The fieldstone light tower stretches toward the sky, standing proud against the assault of the sea and decades of neglect. The beacon  stands cold and unusable. A cascade of vines and yellow lichen hides the west face of the tower. Copper drainpipes and rooftops are a riot of green oxide trails. The light keeper's cottage looks as if it's been recently occupied after years of vacancy.  A few of the dangling shutters have been removed and neatly stacked, the oak front door reattached and the sand swept away from the smooth stones forming the path.\nA simple oil lamp burns in the window. "
	exit "west" to "Lonely Expanse of Beach"
}

Room
{
	name "Mansion Foyer"
	describe "This is the entrance hallway of a large and tastefully decorated, if somewhat eccentric, mansion.  A large, sweeping half-spiral staircase leads upstairs, and a hallway continues eastward."
	exit "west" to "Mansion Hallway"
	exit "up" to "Spiral Landing"
	exit "south" to "Mansion Doorstep"
}

Thing
{
	name "eye of a newt"
	describe "An rather nondescript eye of newt."
	place "glass jar"
	syn "eye"
}

Thing
{
	name "Tome of History"
	describe "The Tome of History is open to page 1. It reads:\n\"INTRODUCTION\nAn unimagineably long time ago, before the Great Fall, things were much different than they are now. The title of \"scribe\" inspired no awe, books were merely paper and ink, and all life was mundane.\nTo remind us what these books were like, we still have the Second Aisle, which, though it does not grow, is an important part of the history of our world. Take a book from that place sometime - you will notice that they are not attached to the shelves. Open it, and note that the pages are dry and brittle (this is because it is dead) and the words stay the same even after you scrutinize them.\""
	place "Grand History Book Room"
	theme "paper"
	feature "divunal.bookstore.TomePage"
	feature "divunal.bookstore.TomeWrite"
	string "page_#7" "There was much chaos.  The stones in the sky came hailing down upon the residents of the city.  Those who had known of the impending disaster had prepared a dwelling place below the streets -- but that place was more slavery than salvation.\n\n"
	string "page_#6" "\n\n\n\n\tThe next,\n\t\tthe sky fell down."
	string "page_#5" "\n\n\n\n\tOne day, the people looked up."
	string "page_#4" "Once, there was a city.  The city was a small and quiet place, where many eccentric but amiable people dwelt.  This city was a part of a country, which in turn was part of a planet.  That planet was surrounded by a ring -- an irridescent ring which was visible from everywhere in the city, high in the center of the sky.  The ring was made of a beautiful blue stone which cast its light as an arced, brilliant blue streak down the center of the night sky.  It was said that this ring was one of the most beautiful sights in all of the world.  Although the world was not one of travellers, many made a pilgrimage at least once in their lives to this city, to see the Light of the Line (as it was called, looking like a line in the sky) and thank the sky for the inspiring painting which it had hung upon itself."
	string "page_#3" "\n\n\n\tChapter One\n\n\t\tTimes Before Now"
	string "page_#2" "This very book, in fact, is that same sort of book with very few of our modern enhancements. It will not dry up and rot like those in Aisle 2, but it will also never change or grow. It is meant to preserve the past faithfully - and so we call such books, with double meaning, History Books. Each of the books in the First Aisle is such a book. You can rest assured that they will never change, to faithfully preserve the past. "
	int "page_number" 1
	string "page_#1" "INTRODUCTION\nAn unimagineably long time ago, before the Great Fall, things were much different than they are now. The title of \"scribe\" inspired no awe, books were merely paper and ink, and all life was mundane.\nTo remind us what these books were like, we still have the Second Aisle, which, though it does not grow, is an important part of the history of our world. Take a book from that place sometime - you will notice that they are not attached to the shelves. Open it, and note that the pages are dry and brittle (this is because it is dead) and the words stay the same even after you read them."
	extends "Class_Book"
	component
	syn "tome"
	syn "book"
}

Location
{
	name "red chair"
	describe "A white box."
	place "Furniture Box"
	feature "twisted.reality.plugin.furniture.Stand"
	feature "twisted.reality.plugin.furniture.Sit"
	string "player preposition" "sitting on"
	string "preposition" "on"
	int "maximum occupancy" 1
	boolean "isLit" false
	syn "chair"
	broadcast
}

Thing
{
	name "clue oak tree"
	describe "This tree must have been here for hundreds of years, judging by its great girth. Strangely enough, it seems that the trunk has been wrapped with barbed wire, making a climb impossible."
	place "Garden Maze(5)"
	string "name" "oak tree"
	component
	syn "oak tree"
	syn "tree"
}

Thing
{
	name "Mechanical Pencil"
	describe "This pencil is one cool thingie. It has a fancy grip and a brushed steel look to it. Wow. It belongs to Blake. Push off."
	place "Blake"
	extends "Reality Pencil"
	syn "pencil"
}

Location
{
	name "leather chair"
	describe "A wonderfully soft leather chair."
	place "Chateau Sitting Room"
	float "weildiness" "0.8"
	float "weight" "0.8"
	string "player preposition" "sitting in"
	string "preposition" "in"
	int "maximum occupancy" 1
	extends "Class_Sittable"
	syn "chair"
	broadcast
}

Thing
{
	name "eastern tapestry"
	describe "The images here form a stark contrast to the ones in the rest of the room. Instead of a scene full of battle and violent imagery, there is a picture of a library. Though it seems run-down and slightly decrepit, it seems to emit a feeling of hope and good fortune."
	place "Guyute's Bedroom"
	component
	syn "tapestry"
	syn "east"
}

Thing
{
	name "tattered book"
	describe "The cover reads \"Mad Science\""
	place "Musty Section"
	feature "divunal.rikyu.LinkingBookOpen"
	thing "linkTo" "Cold Room"
	syn "book"
}

Room
{
	name "Empty Bakery"
	describe "A small and burnt-out bakery.  It looks as though there has been a fire here.  Shattered glass windows to the northwest look out upon a destroyed street, and a door leads out onto it.  There is a small wooden door to the northwest."
	theme "crack"
	exit "northwest" to "Wrecked Alleyway"
	exit "northeast" to "Wrecked Street, wall"
}

Thing
{
	name "development door"
	describe "A worn, splintered wooden door with a dented copper handle. A piece of graph paper has been taped to it, scrawled with the word \"development\"."
	place "Demo Center East Wing"
	feature "twisted.reality.author.Obstruct"
	boolean "obstructed" false
	string "openDesc" "A small, battered wooden door stands open to the north."
	string "closeDesc" "A piece of graph paper scrawled with the word \"Development\" is taped to a smaller, battered wooden door set into the north wall."
	string "thereOpenDesc" "A battered wooden doorway in the south wall leads out into the hall."
	string "thereCloseDesc" "A battered wooden door is set into the south wall."
	string "name" "wooden door"
	extends "Class_Door"
	component
	syn "wooden door"
	syn "door"
}

Room
{
	name "Grand History Book Room"
	describe "This room is a hemisphere carved from solid marble. The only feature of the room is a giant book which is chained and bolted into a huge pedestal at the dead center of the room, and the plaque at the floor in front of the pedestal which reads, \"#1, History Of Divunal\" in immense letters.  A small sign bearing the legend \"Prehistory\" stands over a wooden archway to the north."
	descript "stainless steel door closeDesc" "A large archway with a steel door stands to the south."
	descript "solid oak door openDesc" "To the east, you see a well-lit, polished wood foyer."
	exit "east" to "Jedin's Foyer" with "solid oak door"
	exit "south" notTo "Aisle 1." with "stainless steel door"
}

Player
{
	name "Dynamic Guest"
	describe ""
	boolean "score init" true
	int "score max" 1024
	int "score" 0
	string "adjective" "Dynamic"
	extends "Class_Guest"
	syn "guest"
	passwd ""
}

Thing
{
	name "endurance dial"
	describe "A white box."
	place "Genetic Laboratory"
	float "value" "0.0"
	extends "Class_Player Creation Dial"
	component
	syn "endurance"
	syn "dial"
}

Room
{
	name "Plain Room(1)"
	describe "A Plain Room looking as if it needs to be described."
	theme "dark"
	exit "back" to "Guest Room"
}

Thing
{
	name "pair of tan cargo pants"
	describe "A rather nondescript pair of tan cargo pants."
	place "Blake"
	boolean "clothing worn" true
	extends "Class_Pants"
	component
	syn "pants"
	syn "jeans"
}

Player
{
	name "Rikyu"
	describe "A life of seventy years,\nStrength spent to the very last,\nWith this, my jeweled sword,\nI kill both patriarchs and Buddhas.\nI yet carry\nOne article I had gained,\nThe long sword\nThat now at this moment\nI hurl to the heavens. \n\n"
	gender m
	feature "twisted.reality.Godhood"
	feature "twisted.reality.author.MoodSet"
	thing "oldlocation" "Garden Maze"
	float "spy" "0.1"
	float "stamina time" "9.3439656E11"
	float "health time" "9.3439656E11"
	float "strength" "0.3"
	float "dexterity" "1.0"
	float "agility" "0.0"
	float "endurance" "0.0"
	float "memory" "1.0"
	float "psyche" "1.0"
	
	persistable "clothing right leg" "twisted.reality.Stack" val "thing pair of silk pants\n" key "twisted.reality.Stack@5855ec5"
	
	persistable "clothing left leg" "twisted.reality.Stack" val "thing pair of silk pants\n" key "twisted.reality.Stack@5855e89"
	float "mindspeak" "0.1"
	
	persistable "updatedSkills" "twisted.reality.Stack" val "string mindspeak\n" key "twisted.reality.Stack@5855e62"
	int "learned frotz" -1
	int "learned zorft" -1
	
	persistable "clothing chest" "twisted.reality.Stack" val "thing brown kimono\n" key "twisted.reality.Stack@5855e4a"
	float "health" "1.0"
	float "stamina" "1.0"
	int "learned posess" 2
	int "spells learned" 2
	descript "clothing" {Pronoun Of("Rikyu"), " is wearing ", Name of("brown kimono"), ", ", "and ", Name of("pair of silk pants"), "."}
	extends "Class_Human"
	syn "sen rikyu"
	ability "divunal.rikyu.Posess"
	ability "divunal.magic.spells.Zorft"
	ability "divunal.magic.spells.Frotz"
	ability "divunal.rikyu.Spy"
	ability "twisted.reality.author.FloatSet"
	ability "divunal.rikyu.Drift"
	ability "divunal.magic.Cast"
	ability "divunal.rikyu.Teleport"
	ability "divunal.common.author.Visit"
	ability "divunal.common.skills.MindSpeak"
	architect
	passwd "Ri7zz2f3rUVfA"
}

Thing
{
	name "Class_Tunic"
	describe "A white box."
	place "Clothing Box"
	string "clothing location" "chest"
	extends "Class_Clothing"
}

Location
{
	name "class_pistol"
	describe "A blue box."
	place "Tenth's Chamber"
	feature "inheritance.gun.UnLoad"
	feature "inheritance.gun.GunPut"
	thing "slide" "class_pistol slide"
	string "clip type" "insert clip type/caliber here"
}

Room
{
	name "Michelle's Dorm Room"
	describe "A small, neat room.  You get the impression that whoever lives here has a weakness for Arizona Green Tea."
	descript "battered gray door openDesc" "The west door is clearly open."
	exit "west" to "Meredith's Hell Hole" with "battered gray door"
}

Room
{
	name "Woodem Platform in Oak Tree"
	describe "From here you can see the ivy and tea gardens. Careful you don't fall!"
	theme "leaf"
	exit "down" to "Ivy Garden"
}

Room
{
	name "Greenhouse Entrance"
	describe "An engraved marble plaque in the center of the floor proclaims this to be the \"Twisted Matrix Enterprises Twisted Reality Demonstration Center Greenhouse\". A small forest of plants are strewn haphazardly about the room, as if they were put there to meet a deadline. They all look remarkably similiar."
	place "Demo"
	theme "leaf"
	exit "southeast" to "Demo Center West Wing"
}

Room
{
	name "Even More Office Hallway"
	describe "This hall is undamaged except for a huge chasm which seems to be carved straight out of the floor to the west.  Other than that, it is a clean, white hallway which ends to your east.  There is a spiral staircase leading upwards, as well as an open archway to a metal catwalk to the northeast and a door to a large closet to the southeast."
	exit "northeast" to "Catwalk"
	exit "southeast" to "Supply Closet"
	exit "down" to "Continued Chasm"
}

Thing
{
	name "potted plant"
	describe "All of the plants bear a striking resemblance to one another, having the same number of leaves in approximately the same position, each set into an indentical grey marble pot with it's own tiny engraved brass label. Despite being an almost preternatural shade of green, the plants themselves bear a striking resemblance to palm trees, albeit ones that had been fitted with extra leaves and subjected to some sort of bonsai-like stunting process."
	place "Twisted Reality Corporate Demo Center"
	component
	syn "pot"
	syn "plant"
	syn "green potted plant"
	syn "green potted plants"
	syn "plants"
	syn "potted plants"
	syn "pots"
}

Room
{
	name "Between the Cliffs"
	describe "This is a path between two very high cliffs.  The path is lit by bright moonlight shining through and reflected from the clouds above.  To the south the path becomes sandier and widens into a beach, and to the north, it becomes a dirt path through a pine grove."
	theme "water"
	exit "north" to "Pine Grove"
	exit "south" to "Moonlit Beach"
}

Location
{
	name "koshikake-machiai"
	describe "This bench, called koshikake-machiai, is where guests await the invitation of the tea ceremony host."
	place "Inner Garden"
	string "name" "small bench"
	int "maximum occupancy" 5
	extends "Class_Sittable"
	component
	syn "small bench"
	syn "bench"
	broadcast
}

Room
{
	name "New Jersey Apartment Hallway"
	describe "A dimly lit, narrow hallway, with an ugly reddish pink carpet. To the south, a door is open into what looks like a bathroom, and there are additional doors crammed into the hall to the east, northeast, and north. \n"
	theme "default"
	exit "north" to "Other New Jersey Apartment Bedroom"
	exit "northeast" to "New Jersey Apartment Bedroom"
	exit "east" to "New Jersey Apartment Guest Room"
	exit "south" to "New Jersey Apartment Bathroom"
	exit "west" to "New Jersey Apartment Kitchen"
}

Thing
{
	name "brightly colored manual"
	describe "35 Quick Steps to Mastering the X57:\nAn Introduction to the New Generation \nof Foreign Residual Income Distribution.\n\nIt looks friendly and quite easy to read... for a CPA."
	place "Proper English Library"
	syn "manual"
}

Room
{
	name "Blake's Sphere"
	describe "You are inside of a hollow brushed steel sphere that is approximately 10 feet in diameter. The sphere is lit by a ring of glowing material set into its horizontal circumference. There is a small brass plaque set into the base of the sphere. There is also a sphere chair here."
	theme "default"
}

Thing
{
	name "pile of leaves"
	describe "A white box."
	place "Forest 2"
	syn "leaves"
}

Room
{
	name "coat closet"
	describe "A coat closet looking as if it needs to be described."
	exit "south" to "Jedin's Foyer"
}

Room
{
	name "Chateau Dining Hall"
	describe "A Chateau Dining Hall looking as if it needs to be described."
	place "Inheritance"
	theme "greystone"
	exit "south" to "Chateau Hallway"
	exit "north" to "Chateau Dining Hall(1)"
}

Thing
{
	name "second knob"
	describe "The second knob from the top of the qin with which to tune the instrument."
	place "qin"
	component
	syn "knob2"
	syn "knob"
}

Room
{
	name "Small Gray Dome"
	describe "You are in the center of a small grey dome.  It is perfectly smooth except for the crease where the dome meets the ground, and the perfectly circular hole in the floor.  The hole leading downward appears to have a dark gauze stretched over it."
	exit "down" to "Obscure Corner of Bookstore"
}

Room
{
	name "Supply Closet"
	describe "This is an empty closet, filled with many shelves.  There is a fuse box here, long fused shut.  The only exit is a door to the northwest."
	exit "northwest" to "Even More Office Hallway"
}

Thing
{
	name "door in oak tree"
	describe "Yes, if you look closely it seems there IS a door in the tree. It has been very well concealed, and the edges match almost perfectly."
	place "Ivy Garden"
	boolean "obstructed" false
	string "thereCloseDesc" "The secret door to the south seems to be closed."
	string "thereOpenDesc" "To the south, here is a door leading to a green-looking garden."
	string "openDesc" "There seems to be a door leading north into the tree."
	extends "Class_Door"
	component
	syn "door"
}

Room
{
	name "Mansion Basement Well"
	describe "A dark, cramped, narrow tunnel carved out of greyish stone, knee deep in running water. The tunnel continues to the north, and a rough vertical shaft leads upwards to a brighter area, where a cylindrical object is hanging."
	theme "greystone"
	exit "north" to "Great Underground Lake"
	exit "up" notTo "Mansion Basement Pump Area" with "Mansion Basement Pump"
}

Room
{
	name "Interesting East-West Path"
	describe "This is an east-west path with a junction to the south leading to a small conical building."
	exit "south" to "Yurt Entrance"
	exit "west" to "Start of Forest Path"
	exit "east" to "Boring East-West Path"
}

Location
{
	name "Room Box"
	describe "A perfectly white box labeled \"Room Classes\" in neat black letters."
	place "Class Room"
	feature "twisted.reality.plugin.Put"
	syn "box"
}

Location
{
	name "grey plastic chairs"
	describe "A blue box."
	place "Demo Center West Wing Lobby"
	feature "twisted.reality.plugin.Put"
	feature "twisted.reality.plugin.furniture.Stand"
	feature "twisted.reality.plugin.furniture.Sit"
	string "name" "grey plastic chair"
	string "player preposition" "sitting on"
	string "preposition" "on"
	int "maximum occupancy" 6
	component
	syn "grey plastic chair"
	syn "plastic chairs"
	syn "plastic chair"
	syn "chairs"
	syn "chair"
	broadcast
}

Location
{
	name "king-sized bed"
	describe "This bed looks very soft, and its velvet comforter make it look all the more luxorious."
	place "Guyute's Bedroom"
	syn "bed"
}

Thing
{
	name "ishi-doro"
	describe "A very nice lantern. "
	mood "providing light"
	place "Inner Garden"
	string "name" "stone lantern"
	boolean "isLit" true
	boolean "frotzed" true
	descript "lighting" {"A pure white glow eminates from ", Name of("ishi-doro"), ", bathing ", Pronoun of("ishi-doro"), " in light."}
	syn "stone lantern"
	syn "lantern"
}

Room
{
	name "Garden Maze(9)"
	describe "The last person to come here must not have been feeling too well...judging by the skeleton in the corner."
	theme "leaf"
	string "name" "Garden Maze"
	exit "south" to "Garden Maze"
	exit "east" to "Garden Maze"
}

Thing
{
	name "vial of moonshine"
	describe "What's the use of only a vial's worth?"
	place "nightstand"
	syn "vial"
}

Room
{
	name "A Small Opening"
	describe "The walls leave barely enough room for you to move on.  A soft iradescent light shines at you filling the opening with a soft erie glow. You feel the jelly material all around you now, getting into you hair, and on your clothes as you rub up against the wall as you pass. The subtle scent you smelled before is stronger here, making you reel slightly.  You can almost taste it in the air...sweet and alluring...yet somehow repelling."
	theme "greystone"
	boolean "inhibit_exits" true
	boolean "inhibit_items" true
	string "description" "It's too dark in here to see!"
	string "name" "A Dark Place"
	extends "Class_Dark Room"
	opaque
	shut
	exit "south" to "Silver Shadowed Glade"
	exit "north" to "A Dark Narrow Passage"
	claustrophobic
}

Room
{
	name "Grey Cube Room"
	describe "This is a grey cubical room, about sixteen feet on each side, which appears to have been out of use for a very long time.  A thin layer of dust on the floor is scuffled from the center of the room to the northern door, but other than that untouched."
	theme "default"
	exit "north" to "Granite Reception Room"
}

Location
{
	name "Furniture Box"
	describe "A blue box."
	place "Class Room"
	extends "Class_Container"
}

Thing
{
	name "small brown book"
	describe "A small, leather-bound book of indeterminate age.  It bears a coat-of-arms crest on its cover, a checkered shield.  It is closed."
	place "Obscure Corner of Bookstore"
	thing "linkTo" "Ledge in front of Castle in the Clouds"
	extends "Class_Linking Book"
	syn "book"
	syn "brown book"
	syn "small book"
}

Room
{
	name "Secret Chamber"
	describe "This stone-walled room feels very cool and dank, as if it were once some kind of dugeon chamber. The carpeted floor indicates, however, that it now must have some finer purpose."
	theme "greystone"
	descript "northern tapestry closeDesc" ""
	exit "south" to "Guyute's Bedroom" with "northern tapestry"
}

Thing
{
	name "spider web"
	describe "A rather nondescript spider web."
	place "Cold Room"
	syn "web"
}

Thing
{
	name "starter crank"
	describe "A vaguely Z shaped steel rod, with a hard rubber handle on one end, and a grooved rectangular plug on the other. "
	place "Chateau courtyard"
	feature "inheritance.car.CrankTurn"
	string "type" "Ford Runabout Starter"
	syn "starter"
	syn "crank"
}

Location
{
	name "thin bamboo mat"
	describe "A rather nondescript thin bamboo mat."
	place "Tea House"
	extends "Class_Sittable"
	component
	syn "thin mat"
	syn "bamboo mat"
	syn "mat"
	broadcast
}

Thing
{
	name "pair of sandles"
	describe "A white box."
	place "James"
	boolean "clothing worn" true
	extends "Class_Shoes"
	component
	syn "sandles"
}

Room
{
	name "Rocky Ledge"
	describe "You are on a ledge about halfway up the wall of the river canyon. You can see from here that the main flow from Aragain Falls twists along a passage which it is impossible for you to enter. Below you is the canyon bottom. Above you is more cliff, which appears climbable."
	exit "down" to "Canyon Bottom"
	exit "up" to "Canyon View"
}

Room
{
	name "Mansion Main Hall"
	describe "A broad, massive hallway with an arched ceiling that rises some thirty feet above you. The walls are a muted and featureless white, contrasting sharply against the dark wooden floor. There is a modest pair of doorways at the north and south ends of the hall,  but they are dwarfed by the massive arches set into the east and west walls. The eastern archway leads into darkness, while the western one is nearly obscured by a mass of gears and rods in the room behind it. A black plastic cable runs along the floor, emerging from the western arch and leading to a computer terminal standing in the southwest corner of the hall. Across from the computer, there is a small wooden door in the southeast corner labeled \"Maintenance\"."
	theme "wood"
	exit "west" to "Mansion West Ballroom"
	exit "southeast" to "Mansion Maintenance Closet"
	exit "east" to "Mansion East Ballroom"
	exit "north" to "Mansion Entrance Hall"
	exit "south" to "Mansion Study"
}

Location
{
	name "faded coat pocket"
	describe "A blue box."
	place "faded brown coat"
	feature "twisted.reality.plugin.Put"
	string "name" "coat pocket"
	component
	syn "coat pocket"
	syn "pocket"
}

Thing
{
	name "attic staircase"
	describe "A white box."
	place "Mansion Upper Hall"
	boolean "obstructed" true
	handler "attic door close" "divunal.tenth.AtticCloseHandler"
	component
	syn "stairs"
	syn "staircase"
}

Room
{
	name "Garden Maze(8)"
	describe "Sometimes it's easy to lose faith in yourself, especially when on a long journey. Just remember,\n\nYOU HAVE ALWAYS BEEN HERE.\n\nTake a leap of faith."
	theme "leaf"
	string "name" "Garden Maze"
	exit "north" to "Garden Maze(10)"
	exit "west" to "Garden Maze(9)"
	exit "east" to "Garden Maze(7)"
}

Thing
{
	name "Class_Book"
	describe "A white box."
	place "Book Box"
	feature "divunal.bookstore.TomeWrite"
	feature "divunal.bookstore.TomePage"
}

Room
{
	name "Twisted Reality Corporate Demo Center"
	describe "A spacious, open room with a high, arched ceiling. The walls are an almost gleaming, immaculate white, contrasting sharply with the polished black marble floor. The room becomes wider as it continues on to the north, and is dotted with bright green potted plants at regular intervals.  The southern wall is covered by a ten-foot-tall billboard labeled with the legend: \"'look at board' for help!'\""
	place "Demo"
	exit "north" to "Demo Information Center"
}

Thing
{
	name "Floogle Horn"
	describe "A rather nondescript Floogle Horn."
	extends "Reality Pencil"
	syn "horn"
}

Location
{
	name "Mansion Four Poster Bed"
	describe "A large four poster bed, with a polished wooden frame, dark green hanging curtains, and matching sheets and pillows."
	place "Tenth's Chamber"
	feature "twisted.reality.plugin.furniture.Stand"
	feature "twisted.reality.plugin.furniture.Lie"
	feature "twisted.reality.plugin.furniture.Sit"
	string "name" "bed"
	int "maximum occupancy" 2
	string "preposition" "on"
	string "player preposition" "lying on"
	component
	syn "large bed"
	syn "bed"
	broadcast
}

Room
{
	name "Start of Forest Path"
	describe "This is an east-west path very close to a forest. There are branches overhanging the path here. You may continue east or west or proceed into the small stand of trees to the south."
	exit "east" to "Interesting East-West Path"
}

Thing
{
	name "quantum"
	describe "A rather nondescript quantum."
	place "quantum singularity"
}

Room
{
	name "Psychadelic Room"
	describe "This room has no apparent purpose. The garish colors and pulsating, disorienting distortions of space in here would distort your orientation completely if it were not for the fact that there is only one door to the south."
	theme "weird"
	exit "south" to "Mansion Hallway"
}

Player
{
	name "Class_Human"
	describe "This player is as-yet undescribed."
	thing "oldlocation" "Class Room"
	extends "Class_Player"
	ability "divunal.common.author.ShadowStep"
	ability "divunal.common.author.Twin"
	ability "twisted.reality.author.MoodSet"
	ability "divunal.common.author.Listen"
	ability "twisted.reality.author.Toss"
	ability "divunal.common.author.Visit"
	ability "twisted.reality.author.Pause"
	ability "twisted.reality.author.Handle"
	ability "twisted.reality.author.ThingSet"
	ability "twisted.reality.author.Grab"
	ability "twisted.reality.author.KillProp"
	ability "twisted.reality.author.DescriptSet"
	ability "divunal.jedin.Discover"
	ability "twisted.reality.author.Property"
	ability "twisted.reality.Passwd"
	ability "twisted.reality.author.Locate"
	ability "twisted.reality.author.StringSet"
	ability "twisted.reality.Armageddon"
	ability "twisted.reality.author.Gate"
	ability "twisted.reality.author.Scrutinize"
	ability "twisted.reality.author.Refrump"
	ability "divunal.common.author.TweakRandom"
	ability "divunal.common.skills.MindSpeak"
	passwd "--"
}

Thing
{
	name "notice"
	describe "Some office junk.\n\n\nYou look again, but all you learn is that there is some paper stuck to the wall here.\n\nYou look closely, but you still cannot tell if it is a calender, a memo, or possibly a list of phone numbers."
	place "Damien's Cubicle"
	component
	syn "calender"
}

Room
{
	name "very small round room"
	describe "This room is a circular grey room. It is utterly plain except for the door to the south, and the word 'null' crudely chiseled in the front wall."
	exit "south" to "Doorway Room"
}

Thing
{
	name "pair of sturdy leather boots"
	describe "These boots look as if they have had a lot of use. They are made of reinforced leather for strength and flexibility."
	place "Blake"
	boolean "clothing worn" true
	extends "Class_Shoes"
	component
	syn "boots"
}

Thing
{
	name "Class_Shoes"
	describe "A white box."
	place "Clothing Box"
	string "clothing location" "left foot"
	string "clothing location 2" "right foot"
	extends "Class_Clothing"
}

Thing
{
	name "sprig of sage"
	describe "A rather nondescript sprig of sage."
	place "stone workbench"
	syn "sage"
}

Room
{
	name "Dark River Tunnel"
	describe "A Dark River Tunnel looking as if it needs to be described."
	theme "water"
	boolean "needsBoat" true
	exit "north" to "Dark River Tunnel(1)" with "tunnelX3"
	exit "west" to "Western End of Grotto" with "tunnelX2"
	exit "east" to "Underground Grotto" with "tunnelX1"
}

Thing
{
	name "roaring fireplace"
	describe "The border of the fireplace is constructed out of brick, with a thick mantlepiece across the top. A prominent figure on the front of the mantle is a large lion's head."
	place "Smoking Room"
	feature "divunal.rikyu.FireplacePassage"
	boolean "obstructed" true
	descript "fireplace closed" " Though the fire roars, there seems to be a small draft coming from...somewhere."
	extends "Class_Door"
	component
	syn "fireplace"
	syn "lion's head"
}

Location
{
	name "blue chair"
	describe "A white box."
	feature "twisted.reality.plugin.furniture.Stand"
	feature "twisted.reality.plugin.furniture.Sit"
	int "maximum occupancy" 1
	string "preposition" "on"
	string "player preposition" "sitting on"
	syn "chair"
	broadcast
}

Room
{
	name "Small Bookstore Entrance"
	describe "You are in the entrance to a small bookstore, which appears to have been out of use for quite some time. Empty shelves line the walls. There is a small counter here with a cash register on it and a sign hanging above it which reads \"Borrow and Purchase Here\". A rickety metal spiral stairwell leads down to another level of the store. A doorway leads east out onto the street."
	theme "paper"
	exit "east" to "Wrecked Street, bookstore"
	exit "down" to "Help Desk"
}

Room
{
	name "Guyute's Bedroom"
	describe "The walls here are covered with ancient tapestries depicting battle scenes. In the southwest corner is a king-sized bed, next to which is a small nightstand. Near the east wall is a wood-burning stove, whose chimmney rises into the ceiling."
	theme "wood"
	string "name" "Master Bedroom"
	descript "northern tapestry closeDesc" ""
	descript "tapestry moved" " The northern tapestry has been moved to show a small doorway."
	exit "north" to "Secret Chamber" with "northern tapestry"
	exit "northwest" to "Smoking Room"
}

Location
{
	name "Colt 1911 Semi-Auto"
	describe "It appears to be a Colt 1911, but it is vague, indistinct, and little more than a blurry smear on reality."
	place "Tenth"
	feature "inheritance.gun.UnLoad"
	feature "inheritance.gun.GunPut"
	thing "loaded with" "Colt 1911 pistol clip"
	thing "chamber" "colt 1911 chamber"
	string "clip type" "colt 1911"
	boolean "slide lock" false
	extends "class_pistol"
	syn "gun"
	syn "auto"
	syn "semi-auto"
	syn "colt"
	syn "automatic pistol"
	syn "pistol"
	broadcast
}

Room
{
	name "Divu'en School Entranceway"
	describe "The hallway of an old school-building.  The ceiling is caved in, and none of the rest of the building is accessible, but you can get out to the southwest where you can see a street."
	theme "crack"
	string "name" "School Entranceway"
	exit "southwest" to "Wrecked Street, wall"
}

Thing
{
	name "Temporary Pencil"
	describe "A rather nondescript Temporary Pencil."
	extends "Reality Pencil"
	syn "pencil"
}

Player
{
	name "Yumeika"
	describe "  A young woman of average height and build.  There is nothing particularly noteworthy about her except for the raven-black hair, tied back loosely with a white ribbon."
	gender f
	thing "oldlocation" "Science and Technology Vehicle Area"
	string "visit color" "silver"
	int "learned frotz" -1
	int "learned zorft" -1
	int "spells learned" 0
	string "gender pronoun" "woman"
	
	persistable "clothing right eye" "twisted.reality.Stack" val "thing greyish cloth\n" key "twisted.reality.Stack@5856aab"
	
	persistable "clothing left eye" "twisted.reality.Stack" val "thing greyish cloth\n" key "twisted.reality.Stack@5856ac4"
	
	persistable "clothing back" "twisted.reality.Stack" val "" key "twisted.reality.Stack@5856a83"
	
	persistable "clothing right leg" "twisted.reality.Stack" val "thing Yumeiko's pale blue kimono-like robe\n" key "twisted.reality.Stack@5856a9c"
	
	persistable "clothing left leg" "twisted.reality.Stack" val "thing Yumeiko's pale blue kimono-like robe\n" key "twisted.reality.Stack@5856a5f"
	
	persistable "clothing waist" "twisted.reality.Stack" val "thing Yumeiko's pale blue kimono-like robe\nthing wide sash\n" key "twisted.reality.Stack@5856a2a"
	
	persistable "clothing left arm" "twisted.reality.Stack" val "thing Yumeiko's pale blue kimono-like robe\n" key "twisted.reality.Stack@5856a43"
	
	persistable "clothing right arm" "twisted.reality.Stack" val "thing Yumeiko's pale blue kimono-like robe\n" key "twisted.reality.Stack@5856a07"
	
	persistable "clothing chest" "twisted.reality.Stack" val "thing Yumeiko's pale blue kimono-like robe\n" key "twisted.reality.Stack@5856a26"
	descript "clothing" {Pronoun Of("Yumeika"), " is wearing ", "a greyish cloth bound tightly across her eyes", ", ", "a well-worn knapsack", ", ", "a pale blue, almost kimono-like robe with wide, open sleeves", ", ", "and ", "a wide sash around her waist", "."}
	extends "Class_Human"
	syn "yume"
	syn "dumbname"
	ability "divunal.common.author.Visit"
	ability "divunal.magic.spells.Zorft"
	ability "divunal.magic.spells.Frotz"
	architect
	passwd "AnRMSrekM/MSU"
}

Room
{
	name "Chateau Bathroom"
	describe "A Bathroom looking as if it needs to be described."
	place "Inheritance"
	theme "greystone"
	exit "north" to "Chateau Bedroom"
}

Thing
{
	name "rug"
	describe "The design on this rug is extremely intricate; it must have cost a lot of money. The rug itself is very heavy and thick."
	place "Hallway"
	component
}

Room
{
	name "Castle Beach"
	describe "You see a very rocky beach, with a sea to the west, north, and south. To the east, you can see a very small forest, walled by cliffs on either side.  The air is clean and clear here.  There is a tunnel in the rocks leading downward into a stairwell."
	theme "leaf"
	exit "east" to "Clearing in Small Forest"
	exit "down" to "Crumbling Entranceway"
}

Room
{
	name "Garden Maze(7)"
	describe "There is a sense of peace and tranquility that fills the air here. There is a great pile of leaves on the ground to the north, which is quite strange, given the fact that there are no trees in the area. To the west there is a rake leaning against the hedge."
	theme "leaf"
	string "name" "Garden Maze"
	exit "north" to "Garden Maze(11)"
	exit "west" to "Garden Maze(8)"
	exit "east" to "Garden Maze(5)"
}

Thing
{
	name "tunnelX4"
	describe "A rather nondescript tunnelX4."
	place "Dark River Tunnel(1)"
	extends "tunnelX2"
	component
}

Room
{
	name "Very Cold Room"
	describe "This room is very, very cold.  The metallic walls, floor and ceiling gleam harshly, and ice covers all the surfaces.  A mist covers the floor.  A metallic tube leads westward to somewhat warmer climes."
	exit "west" to "Closed Junction"
}

Thing
{
	name "diagrams"
	describe "Large sheets of white paper, covered with dense and intricate patterns of black lines. While some of the diagrams are difficult to identify, several of them appear to be drawings of a large, cubic system of clockwork. There is also a drawing of what looks like a massive suit of armor, filled with gears, pulleys, and tubing, but its exact design and purpose is somewhat unclear."
	place "Mansion Maintenance Closet"
	component
	syn "technical diagrams"
	syn "diagram"
}

Thing
{
	name "tunnelX3"
	describe "A rather nondescript tunnelX3."
	place "Dark River Tunnel"
	extends "tunnelX2"
	component
}

Thing
{
	name "tunnelX2"
	describe "A rather nondescript tunnelX2."
	place "Dark River Tunnel"
	boolean "wateryExit" true
	extends "Class_Forbidden Exit"
	component
}

Thing
{
	name "tunnelX1"
	describe "A rather nondescript tunnel opening helper."
	place "Underground Grotto"
	boolean "wateryExit" true
	extends "Class_Forbidden Exit"
	component
}

Thing
{
	name "green silk shirt"
	describe "A loose fitting, collarless green silk shirt, with it's sleeves rolled up to the elbow. "
	place "Tsiale"
	boolean "clothing worn" true
	extends "Class_Shirt"
	component
	syn "green shirt"
	syn "shirt"
	syn "silk shirt"
}

Thing
{
	name "door"
	describe "A rather nondescript door."
	place "Jedin's Foyer"
}

Room
{
	name "Chateau Bedroom"
	describe "A Bedroom looking as if it needs to be described."
	place "Inheritance"
	theme "greystone"
	exit "south" to "Chateau Bathroom"
	exit "west" to "Chateau Hallway(14)"
}

Player
{
	name "Fault-Tolerant Guest"
	describe ""
	boolean "score init" true
	int "score max" 1024
	int "score" 0
	string "adjective" "Fault-Tolerant"
	extends "Class_Guest"
	syn "guest"
	passwd ""
}

Thing
{
	name "small mailbox"
	describe "A white box."
	place "West of House"
	float "weight" "0.9"
	syn "mailbox"
	syn "box"
}

Room
{
	name "Chateau Hallway"
	describe "A Chateau Hallway looking as if it needs to be described."
	place "Inheritance"
	theme "greystone"
	exit "east" to "Chateau Antechamber"
	exit "north" to "Chateau Dining Hall"
}

Room
{
	name "Cold Room"
	describe "This room looks as if it's simply used to store old junk."
	theme "greystone"
	exit "south" to "Western End of Grotto"
	exit "east" to "Guyute's Laboratory"
}

Room
{
	name "Proper English Library"
	describe "This room has the works: wall to wall plush shag carpeting, leather clad chairs and oaken tables. Obviously the walls are paneled in bookcases. In the center is a huge wooden table. \n\nIt looks as though someone has set up camp here: the room is covered in neatly stacked piles of paper, coffee mugs, and empty chinese food cartons."
	theme "paper"
	exit "west" to "Hallway"
	exit "east" to "Musty Section"
}

Room
{
	name "Silver Shadowed Glade"
	describe " A sylvan glade stretches out before you bathed in soft, silver moonlight.  As far as the eye can see, there are soft, silver-bladed grass, and fields of flowers in full bloom.  Dew glistens crystal clear upon the delicate, velvety petals and blades of grass. The air is heavily suffused with scents, sweet and cloying.  "
	theme "leaf"
	exit "north" to "Silver Shadowed Glade"
	exit "southwest" to "Silver Shadowed Clearing"
	exit "southeast" to "Silver Shadowed Fields"
	exit "east" to "Silver Shadowed Plain"
	exit "west" to "Silver Shadowed Flowers"
	exit "northwest" to "Silver Shadowed Glade"
	exit "northeast" to "Silver Shadowed Glade"
	exit "south" to "Trans-Dimensional Time Warp"
}

Room
{
	name "Circular Driveway"
	describe "The far side of a circular gravel drive, both ends of which lead north towards a tall, imposing mansion. To the south, the two sides converge into a single driveway and lead uphill through the middle of a vast, yellowish white field of dead corn."
	place "Inheritance"
	theme "leaf"
	exit "west" to "Front Lawn(4)"
	exit "east" to "Front Lawn(2)"
	exit "south" to "Gravel Driveway"
	exit "north" to "Chateau courtyard"
}

Location
{
	name "Yumeiko's pale blue kimono-like robe"
	describe "A kimono-like, pale blue robe with wide, open sleeves."
	place "Yumeika"
	string "clothing appearance" "a pale blue, almost kimono-like robe with wide, open sleeves"
	string "name" "pale blue robe"
	boolean "clothing worn" true
	extends "class_robe"
	component
	syn "robe"
	syn "blue robe"
	syn "pale robe"
	syn "pale blue robe"
	broadcast
}

Room
{
	name "Castle Steps"
	describe "You are standing on a set of beautiful white stone palace steps.  The steps are too stonelike to be ivory, yet too muted to be marble.  They are almost soft as you walk on them.  To your south lies the castle, through a very large stone archway, and down the stairs to the north there is a ledge on which you think you might be able to stand.  A portcullis is visible at the top of the archway: it is wide open."
	exit "down" to "Ledge in front of Castle in the Clouds"
	exit "south" to "Castle Entrance Archway"
}

Room
{
	name "Crater Edge South"
	describe "DESCRIBE ME!"
	theme "crack"
	exit "east" to "Wrecked Street, south"
}

Room
{
	name "The Middle of the Field"
	describe "To the north you can see a rather imposing forrest, while to the south is a road and, further on, the library building. This field continues on to the west, and a pathway cuts through it to the east."
	exit "north" to "Outside the Mods"
	exit "southeast" to "Intersection"
}

Room
{
	name "Bus Stop Junction"
	describe "This is a junction in the path which leads either to a bus stop to the east or another, smaller junction to the south."
	exit "south" to "Scenic Junction"
	exit "east" to "Bus Stop"
	exit "west" to "HC Library Slab"
}

Thing
{
	name "Class_Linking Book"
	describe "A rather nondescript Class_Linking Book."
	place "Book Box"
	feature "divunal.rikyu.LinkingBookOpen"
	thing "linkTo" "Obscure Corner of Bookstore"
	extends "Class_Book"
}

Room
{
	name "Garden Maze(6)"
	describe "You can barely make out a thing in here. Any sources of light, no matter how bright, do little to fix the darkness."
	theme "leaf"
	string "description" "It's too dark in here to see!"
	string "name" "A Dark Place"
	extends "Class_Dark Room"
	opaque
	shut
	exit "south" to "Garden Maze"
	claustrophobic
}

Room
{
	name "Jewel Bedecked Hallway"
	describe "This is a hallway lined with hundreds of different colors of jewels.  Upon closer inspection, the walls are inlaid with them, so they appear both smooth and jeweled at once.  An emerald arch leads west, a marble one south, a ruby one east and an onyx one north."
	theme "default"
	exit "north" to "Jewel Bedecked Hallway 2"
	exit "west" to "Ruby Room"
	exit "east" to "Emerald Room"
	exit "south" to "Observation Hallway"
}

Thing
{
	name "painting"
	describe "It appears to be a painting of a scenery of some sort, vague and indistict.  The whole painting is covered with alternations of soft and vivid colors, swirling and undulating in patterns that tease the mind.  "
	place "Tenth's Chamber"
	thing "painting realm" "A Swirling Mass Of Colors"
	string "description 2" "It appears to be a painting of a scenery of some sort, vague and indistict.  The whole painting is covered with soft colors, swirling and undulating in patterns that tease the mind. They are definitely moving."
	string "description 1" "It appears to be a painting of a scenery of some sort, vague and indistict.  The whole painting is covered with soft colors, swirling and undulating in patterns that tease the mind. They almost seem to be moving..."
	
	property "description" "divunal.random.PaintingDescription"
	string "xyzzy" ""
}

Thing
{
	name "gender changer"
	describe "A small, grey, rectangular piece of plastic, with 32 pin connectors on either end and a large red button on the top."
	place "science and technology demo center table"
	gender m
	feature "demo.GenderChanger"
	thing "repop" "Science And Technology Demo Center"
	syn "button"
	syn "changer"
	syn "red button"
}

Room
{
	name "Meredith's Hell Hole"
	describe "A horribly messy room, whose very walls seem to ooze the stench of hampster feces and vodka."
	descript "battered gray door openDesc" "The east door is open."
	exit "east" to "Michelle's Dorm Room" with "battered gray door"
}

Room
{
	name "Darkened Road"
	describe "An old dirt road, leading off into darkness to the east and west. It is bordered by a steep ridge to the north, and the crumbling remains of a stone wall to the south. The trees form an almost solid wall of leaves and branches above the road, blotting out the sky."
	place "Inheritance"
	theme "leaf"
	exit "east" to "Darkened Road(1)"
	exit "west" to "Country Road(2)"
}

Location
{
	name "comfortable sofa"
	describe "This fine piece of furniture is upholstered in fine velvet. The legs are carved out of fine mahogany; it certainly seems sturdy, and has room for three. It's obvious that it was crafted by someone who cared an awful lot about sitting."
	place "Guyute's Laboratory"
	string "name" "sofa"
	int "maximum occupancy" 3
	extends "Class_Sittable"
	component
	syn "sofa"
	broadcast
}

Location
{
	name "colt 1911 chamber"
	describe "A blue box."
	place "Colt 1911 Semi-Auto"
	string "name" "chamber"
	extends "class_pistol chamber"
	component
	syn "chamber"
}

Room
{
	name "Landing"
	describe "null"
	exit "down" to "Mod Seven"
}

Thing
{
	name "pair of green boxer shorts"
	describe "A pair of dark green silk boxer shorts"
	place "Tenth"
	boolean "clothing worn" true
	extends "Class_Pants"
	component
	syn "shorts"
	syn "boxer shorts"
}

Room
{
	name "Gold Room"
	describe "This room is a study in gold.  While you can make out no light source, light must be filtering in through the golden, translucent ceiling to get down here, where it shines off of the curved surfaces of the room's walls and floor.  There are no markings anywhere, and the only real feature of the room is a cube, which appears to be part of the floor, made of the same golden substance that composes the rest of the room, but glittering more brightly."
	exit "east" to "Jewel Bedecked Hallway 2"
}

Room
{
	name "Mod Seven"
	describe "This place is a mess! Empty cereal bowls litter the floor, the tables and every other surface. The carpet is full of crumbs, and papers litter the ground. There is an extraordinarily ugly couch here, facing the television set. The carpet is green.\nThere is a tiny little kitchen space to the north, stairs lead upowards, and a sign marked, \"Science Fiction/Fantasy\" hangs over the door to the west. To the north is a door. The sign over it says, \"Fiction\"."
	exit "up" to "Landing"
	exit "north" to "Hall"
	exit "west" to "Mod Seven Short Hallway"
	exit "east" to "Mod Lawn"
}

Location
{
	name "demo center paper dispenser"
	describe "A small, glossy black box, with a polished chrome sliding lever attached to the side."
	place "Demo Center Bathroom Stall"
	string "name" "toilet paper dispenser"
	component
	syn "paper dispenser lever"
	syn "toilet paper dispenser lever"
	syn "dispenser lever"
	syn "lever"
	syn "paper dispenser"
	syn "dispenser"
	syn "toilet paper dispenser"
}

Room
{
	name "Rare Book Room, Upper Level"
	describe "This is the upper level of a Rare Book room, as a sign hanging from the ceiling says.  There is a staircase leading down to the lower level in the corner of the room, and a wooden door with a frosted glass window to the west."
	theme "paper"
	exit "southwest" to "Bookstore Stairwell, Level 6"
	exit "down" to "Rare Book Room, Lower Level"
}

Room
{
	name "Office Hallway"
	describe "This hallway exhibits a peculiar pattern of decay.  Down the center of the hallway, there is an area that looks badly damaged, and blackened, as by an electrical storm.  This swath of destruction extends down the hallway to the east and west, and to the doors leading north and south."
	exit "east" to "More Office Hallway"
	exit "west" to "Reception Area"
}

Thing
{
	name "Red marker"
	describe "A red marker, suitable for making corrections to works of other people."
	place "James"
	feature "twisted.reality.author.BoolSet"
	extends "Reality Pencil"
	syn "marker"
}

Room
{
	name "Precarious Ledge"
	describe "The forces of erosion have conspired to eat away at the rock underneath your feet until the ledge you stand on is no more than a few feet thick. To the south and north is the comforting solidity of a rock wall, but to the west is a dizzying exspanse of nothing.\nThe rock wall is covered in a phospherescent moss that provides enough light to see the ledge you are standing on, but not enough light to see anything to the west. For all you can tell, it is a void.  On the wall there is an sign with an arrow pointing west, reading \"Do not go that way.  You probably won't be able to get out.\"  Below it, there is another, apparrently written in blood, that says \"We're not even kidding. Really.\""
	theme "paper"
	exit "west" to "Darkness"
	exit "east" to "Natural Alcove"
}

Room
{
	name "Unmarked Corridor"
	describe "As you wander down this twisty section of the store, you try in vain to guess what topic unites the books here. Choosing books at random you notice some on astrology, some on tidal cycles, and quite a few that are too ancient to make out the titles of. Not a few are printed in languages that you do not understand. This section continues to the south, although it becomes very narrow in that direction."
	theme "paper"
	exit "south" to "Small Section"
	exit "east" to "Myth Section"
}

Thing
{
	name "crumbling piece of papyrus"
	describe "This ancient item looks as if it's about to disintegrate right in your hands, but you can faintly make out a diagram of some sort:\n\n     +-----------------------||---+\n     X   12   =    13   =    14   |\n     +---||---+----xx---+---------+\n     X   10   |    11        6    \n+----+---||---+----xx---+----xx---+\n| 9  X   8    =    7    =    5    |\n+-xx-+--------+---------+----||---+\n                   3    X    4    |\n              +----xx---+----||---+\n              |    1    =    2    |\n     +--------+----||---+---------+\n     |                            |\n     +----------------------------+"
	place "Mystic Field"
	syn "paper"
	syn "piece of papyrus"
	syn "map"
	syn "piece of paper"
	syn "papyrus"
}

Thing
{
	name "third knob"
	describe "Third knob from the top of the qin with which to tune the instrument."
	place "qin"
	component
	syn "knob3"
	syn "knob"
}

Room
{
	name "Wrecked Street, bookstore"
	describe "A wrecked paved street.  It continues to the north and south, and to the west you see the familiar sight of the Bookstore."
	theme "crack"
	string "name" "Wrecked Street"
	exit "south" to "Wrecked Street, south"
	exit "north" to "Wrecked Street, north"
	exit "east" to "Tsiale's House"
	exit "west" to "Small Bookstore Entrance"
}

Room
{
	name "Garden Maze(5)"
	describe "The maze continues in several directions here. A large pine tree stands to the west, while to the north is an apple tree."
	theme "leaf"
	string "name" "Garden Maze"
	exit "west" to "Garden Maze(7)"
	exit "north" to "Garden Maze(6)"
	exit "south" to "Garden Maze(4)"
}

Thing
{
	name "torch"
	describe "A white box."
	place "James"
	boolean "true" false
	boolean "isLit" true
}

Thing
{
	name "curves"
	describe "The curves and lines woven into the carpet create a sinuous, elaborate pattern. It is difficult to focus on any one part of the design, and it almost seems to be shifting and changing as you watch. The effect is hypnotic, looking almost as if the lines were waving in a slow, repeating motion."
	place "Mansion Upper Hall"
	component
	syn "pattern"
	syn "intersecting lines"
	syn "lines"
}

Room
{
	name "Guest Bathroom"
	describe "A Guest Bathroom looking as if it needs to be described."
	place "Inheritance"
	theme "dark"
	exit "north" to "Guest Room"
}

Room
{
	name "Music Room"
	describe "Strains of music float through this acoustically perfect room.  The walls are made of a white plaster-like material which seems to reflect sound extremely well."
	exit "south" to "More Mansion Hallway"
}

Thing
{
	name "chair"
	describe "Your eye slides over this object, just another bit of office junk.\n\nYou look again, but there are no interesting features.\n\nYou force yourself to look hard at this simple chair, and notice that you cannot quite determine the number of wheels. There are definately more than three, but there seem to be less than four... The color is hard to determine, as well... grey? Perhaps a steel blue?"
	place "Damien's Cubicle"
	component
}

Location
{
	name "wood-burning stove"
	describe "A cast-iron wood stove."
	place "Guyute's Bedroom"
	extends "Class_Container"
	syn "stove"
	syn "wood stove"
}

Room
{
	name "Mansion Laboratory"
	describe "A large room, cluttered with tables, shelves, and large racks of machinery. A massive metal frame occupies the center of the room, attached to a number of smaller machines. The closest thing to furniture in the room is a blue mattress laying on the floor in one corner."
	theme "wood"
	exit "south" to "Mansion Upper Hall"
}

Thing
{
	name "oil painting"
	describe "An unfinished masterwork. The composition is brilliant and the colours are so vibrant that they tremble with life. The subject is pastoral, showing a forest pool with satyrs at play, but the bottom corner has not been finished. A few lines of charcoal sketch out the rest of the scene, but the artist apparently changed his mind about it. Instead of finishing the satyr, the unknown painter covered over that corner with two words in bright carmine: \"Help Me\"."
	place "Natural Alcove"
	component
	syn "painting"
}

Room
{
	name "Rough Passage"
	describe "For the first time in a while you can feel walls. There are two of them, in fact, on on either side of you. Both feel like normal rock walls: slightly damp, slightly cold and very solid. The floor beneath your feet continues to be quite rough and strewn with rubble. The walls continue on for at least a few more feet to the north, so it must be safe to follow them."
	theme "greystone"
	exit "south" to "Rough Floor"
}

Thing
{
	name "frobozz magic reality altering sextant"
	describe "This is an exciting sparkly and new sextant, with the \"FROBOZZ MAGIC REALITY ALTERING SEXTANT AND FLOOR WAX REMOVER COMPANY\" logo proudly emblazoned on its side.  Below that, in slightly smaller text, reads the Frobozz International slogan: \"You Name It, We Own It\"."
	extends "Reality Pencil"
	syn "sextant"
}

Thing
{
	name "sparkly book"
	describe "This is a sparkling, shiny book with the words \"Collecting Pixies for Fun and Profit\" emblazoned on its spine."
	place "Small Book Room"
	extends "Class_Small Book"
	syn "book"
}

Player
{
	name "Agent Moore"
	describe "He is non-descript.  He is wearing a suit.  There is nothing more."
	thing "oldlocation" "Obscure Corner of Bookstore"
	extends "Class_Human"
	ability "divunal.jedin.Discover"
	architect
	passwd "Ag8VCxnj7Xndg"
}

Thing
{
	name "chain"
	describe "A long, white plastic chain. A child could snap it in half, but why would it want to?"
	place "Intersection"
	component
}

Room
{
	name "Chateau Basement"
	describe "A Chateau Basement looking as if it needs to be described."
	place "Inheritance"
	theme "greystone"
	exit "north" to "Chateau Basement(5)"
	exit "west" to "Chateau Basement(3)"
	exit "east" to "Chateau Basement(1)"
}

Room
{
	name "Small Book Room"
	describe "This is a room full of small books"
	exit "down" to "Class Room"
}

Location
{
	name "clue third chair"
	describe "A rather nondescript clue third chair."
	place "Garden Maze(12)"
	string "name" "third chair"
	extends "Class_Sittable"
	component
	syn "third chair"
	syn "chair"
	broadcast
}

Room
{
	name "Damien's Office,entering"
	describe "You see a typical office cubicle littered with common-place office junk. The office looks to be some sort of banking or accountancy house, but it is difficult to make out any details. Maybe it's the lighting, but everything except the one cubicle seems dull and almost out of focus. In fact, the only detail that you can easily make out aside from the cubicle is that all of the corners to this room have been filled in with plaster. Now none of the walls meets at a right angle. This plaster has recently been augmented by an organic, sticky substance. The strands completely round out the edges, and seem to be incredibly strong.\n\nYou can go east, into a stack of books; or you can enter the cubicle to the north."
	string "name" "Damien's Office"
	exit "north" to "Damien's Cubicle"
	exit "east" to "Musty Section"
}

Location
{
	name "Ford Runabout starter socket"
	describe "A raised, circular socket embedded in the hood of the runabout, where the crank used to start the engine is normally inserted."
	place "Ford Runabout"
	feature "inheritance.car.SocketPut"
	string "type" "Ford Runabout Starter"
	component
	syn "socket"
	syn "starter socket"
	broadcast
}

Room
{
	name "Kitchen Closet"
	describe "A Kitchen Closet looking as if it needs to be described."
	place "Inheritance"
	theme "greystone"
	exit "north" to "Chateau Kitchen"
}

Room
{
	name "another test room(1)"
	describe "A test room that is being taken over by jello"
	exit "down" to "Aaron's test room"
}

Room
{
	name "Wrecked Avenue"
	describe "This avenue goes between rows of buildings that have been completely reduced to rubble.  The road has fared better than the buildings though, it appears to be in fairly good condition. The avenue continues north to an intersection, and south to the base of what appears to be a very tall tower."
	theme "crack"
	string "name" "Wrecked Street"
	exit "south" to "Tower's Base"
	exit "north" to "Wrecked Street"
}

Thing
{
	name "demo center bell"
	describe "A small brass bell on a wooden stand, with a prominent brass button emerging from the top. Engraved in the stand is the phrase \"Ring For Service\"."
	place "demo center obelisk"
	feature "demo.RingForService"
	thing "repop" "demo center obelisk"
	thing "reciever" "brass paperweight"
	string "name" "small brass bell"
	syn "brass button"
	syn "button"
	syn "bell"
	syn "brass bell"
	syn "small brass bell"
}

Room
{
	name "Tea House"
	describe "Wabi is the avoidance of anything showy or sensuous. It is the pursuit of simplicity and abstraction. It is the discovery of the true beauty that things possess when stripped of superficial characteristics and reduced to their essence. Even the tea-ceremony room itself is shorn of all superfluity, and a limitless universe is created in an unadorned room with an area of a mere 5 meters. In a small alcove to the north, there is a scroll hanging on the wall."
	theme "paper"
	exit "south" to "Inner Garden"
}

Room
{
	name "Narrow Passageway"
	describe "A Narrow Passageway looking as if it needs to be described."
	theme "wood"
	descript "roaring fireplace closeDesc" ""
	exit "west" to "Smoking Room" with "roaring fireplace"
}

Room
{
	name "Small Section"
	describe "The bookshelves get closer and closer the more you walk in this direction, and the titles get increasingly bizarre. Here sits a book cataloging the World's Great Cataclysms, there lies a novel about fisheries. The floor is very dusty here.\nThe passage gets wider to the north, and to the west you can just barely squeeze through between two shelves."
	theme "paper"
	exit "west" to "Tight Squeeze"
	exit "north" to "Unmarked Corridor"
}

Room
{
	name "Main Aisle, East End"
	describe "This is the main aisle of the floor of a bookstore. There are three aisles branching from it, spaced at regular intervals along the floor - the aisles are almost separate rooms because the bookshelves touch the ceilings and the floors and there is a wide separation between one aisle and the next because the shelves are so deep.  You are standing at the front of the first sub-aisle, at the east end of the main one. A plaque on the floor here reads \"1-52.5, The History Of Everything Really Worth Knowing About\". You can continue northward to into the History aisle, or east to another section."
	theme "paper"
	exit "northeast" to "Help Desk"
	exit "north" to "Aisle 1."
	exit "west" to "Main Aisle, Center"
}

Room
{
	name "Garden Maze(4)"
	describe "The hedges must be of a different kind here; now there seems to be flowers blooming in places on the walls. To the west there is a wooden chair, while to the north, leaning against the hedge is a paddle from a rowboat of some sort."
	theme "leaf"
	string "name" "Garden Maze"
	exit "west" to "Garden Maze(3)"
	exit "north" to "Garden Maze(5)"
	exit "south" to "Garden Maze(2)"
}

Room
{
	name "Inheritance"
	describe "A silent box."
	place "Mansion Laboratory"
}

Thing
{
	name "dried white rose"
	describe "The blossom, stem, and first leaf of a white rose, carefully dried out and preserved."
	place "Other New Jersey Apartment Bedroom"
	syn "rose"
	syn "white rose"
	syn "dried rose"
}

Room
{
	name "Parlor"
	describe "A parlor.  Describe me?"
	theme "wood"
	exit "south" to "Mansion Upper Hallway"
}

Thing
{
	name "Encyclopedia Divunalia"
	describe "A beautiful book, elegantly bound in what appears to be platinum, with the engraved title \"Encyclopedia Divunalia\" on the front cover.  You are sure that it contains lots of useful information about the world that you are currently residing in, and that much of that information is reserved only for gods.  A pen is attached for defining your own words, and there is a bookmark at each letter for doing lookups.  You could also index the volume by looking in the back."
	place "Pedestal"
	feature "divunal.bookstore.Define"
	feature "divunal.bookstore.Lookup"
	string "enc define skystone" "Skystone: A \"magical\" mineral that was previously in a ring orbiting Divunal, which allows Humans (and to some extent, those with Divuthan heritage) to change the rules that bind Reality.  While it can theoretically take on any form, it is usually fullbright blue, and translucent."
	string "enc define huntyre" "Huntyre: A manifestation of the Dark Angel."
	string "enc define maxwell's castle" "Maxwell's Castle: A palace in the clouds, created as a home for the Teller of the Tale.  It is somewhere in the heart of the library."
	string "enc define anah" "Anah: The Human brought from Earth to fulfill the Dreamer archetype.  This archetype is dissatified in the real world, and finds comfort and satisfaction in a world of dreams."
	string "enc define kalev" "Kalev: A Human sent from Earth to fulfill the \"Mystery\" archetype.  This archetype takes herself very seriously, she has an alluring and mysterious personality which inspires curiosity (and perhaps desire)."
	string "enc define jedin" "Jedin: A Human archaeologist sent from Earth to fulfill the \"Historian\" archetype.  His type is most interested in the past."
	string "enc define foo" "Foo: an interesting metasyntactic variable whose origins have been lost in the mists of time.  This foo is rather nondescript for the purposes of this example.  See also: the Great Plague of Foos (GPF) in 2 BF."
	string "enc define maxwell" "Maxwell: the first of the human archetypes to arrive in Divunal.  He is an ex-writer."
	
	persistable "enc index" "twisted.reality.Stack" val "string Foo\nstring Maxwell\nstring Tenth\nstring Jedin\nstring Kalev\nstring Anah\nstring Maxwell's Castle\nstring Huntyre\nstring Skystone\n" key "twisted.reality.Stack@5857083"
	string "enc define tenth" "Tenth: a Human brought from Earth to fill the role of the Architect or Artificer Archetype.  He has a penchant for a Victorian style of design and dress.  He is rather nondescript for the purposes of this example, although he should not be."
	syn "book"
	syn "encyclopedia"
}

Room
{
	name "Guyute's Laboratory(1)"
	describe "This room is dank and moist. On the east wall is a long workbench, on which lies all sorts of junk. The north wall is mostly covered by a large bookshelf. In the middle of the room is a large black cauldron, which emits billows of smoke and steam. The southeast corner features a soft, squishy sofa."
	theme "greystone"
	string "name" "A Dark Place"
	string "description" "It's too dark in here to see!"
}

Location
{
	name "right front pocket"
	describe "The front right pocket of the battered black backpack.  It can be closed with a shiny clasp."
	feature "twisted.reality.plugin.clothes.ClothingPut"
	feature "twisted.reality.plugin.OpenCloseContainer"
	component
	syn "right pocket"
	syn "pocket"
}

Room
{
	name "More Mansion Hallway"
	describe "This is a continuation of the hallway.  The hallway simply ends in a flat wall to the west.  Doors line the northern wall, and through the windows to the south you can see a large pine forest."
	exit "east" to "Mansion Hallway"
	exit "northeast" to "Art Room"
	exit "north" to "Music Room"
}

Thing
{
	name "broken handmirror"
	describe "The mirror glass has been broken into a slew of tiny glass fragments. It appears to have been thrown in a fit of rage (or fear?)"
	place "Guyute"
	syn "handmirror"
	syn "mirror"
}

Thing
{
	name "tapestry"
	describe "This hanging covers the western wall. It has a beautiful pattern in the shape of a stylized serpent winding around itself in ever-tightening circles. It is very heavy, and hangs flush against the wall."
	place "Hallway"
	component
}

Room
{
	name "Garden Maze(3)"
	describe "A unsettling feeling seems to be a resident of this area; you can't escape it. The hedge seems to be turning brown in patches around here."
	theme "leaf"
	string "name" "Garden Maze"
	exit "east" to "Garden Maze"
	exit "north" to "Garden Maze(9)"
	exit "south" to "Garden Maze"
}

Thing
{
	name "clue rake"
	describe "This rake looks like it's been here for a really long time. The blades are so rusted, it probably wouldn't be of any use, but carved into the pole are someone's initials: \"N.Z.\""
	place "Garden Maze(7)"
	string "name" "rake"
	component
	syn "rake"
}

Player
{
	name "Jedin"
	describe "This man, about two meters in height, complements his gymnastic musculature with the poise of a high-ranking aristocrat--or a military leader.  His thick, straight hair parts easily to his left; it appears slightly mussed, as if he runs his hands through it often.  The obsidian-toned locks frame a face of planes and angles, striking in its resemblance to that of an almost-finished statue--even the ears are slightly pointier than a normal man's, the lips fuller.  Jedin's emerald-green eyes sparkle beneath his black eyebrows, their intensity matched by a startling degree of softness and understanding, traits that flow through the rest of his demeanor and belie his body's youth."
	gender m
	thing "oldlocation" "The Doorway of the Obsidian Tower"
	
	persistable "clothing left foot" "twisted.reality.Stack" val "thing brown Expedition boots\n" key "twisted.reality.Stack@5857510"
	
	persistable "clothing right foot" "twisted.reality.Stack" val "thing brown Expedition boots\n" key "twisted.reality.Stack@58574da"
	
	persistable "clothing waist" "twisted.reality.Stack" val "thing brown leather belt\n" key "twisted.reality.Stack@58574f3"
	
	persistable "clothing right leg" "twisted.reality.Stack" val "thing khaki pants\n" key "twisted.reality.Stack@58574b7"
	
	persistable "clothing left leg" "twisted.reality.Stack" val "thing khaki pants\n" key "twisted.reality.Stack@5857480"
	
	persistable "clothing right arm" "twisted.reality.Stack" val "thing white button-down shirt\n" key "twisted.reality.Stack@5857499"
	
	persistable "clothing left arm" "twisted.reality.Stack" val "thing white button-down shirt\n" key "twisted.reality.Stack@585745d"
	
	persistable "clothing chest" "twisted.reality.Stack" val "thing white button-down shirt\n" key "twisted.reality.Stack@5857420"
	descript "clothing" {Pronoun Of("Jedin"), " is wearing ", "a white, button-down shirt and collar of a soft, durable fabric with the sleeves rolled up to just below his elbows", ", ", "a well-worn brown leather belt", ", ", "a pair of rugged, dust-brown chinos", ", ", "and ", "a pair of all-purpose brown leather boots", "."}
	extends "Class_Human"
	architect
	passwd "Jeu5g0d1RMBPo"
}

Thing
{
	name "class_tie"
	describe "It appears to be a class_tie, but it is vague, indistinct, and little more than a blurry smear on reality."
	feature "divunal.tenth.TieUntie"
	feature "divunal.tenth.WearRemoveTie"
	string "clothing location" "neck"
	extends "Class_Clothing"
}

Location
{
	name "glass jar"
	describe "An ordinary class jar."
	place "Cold Room"
	extends "Class_Container"
	syn "jar"
}

Room
{
	name "Mansion Hallway"
	describe "You are standing in a narrow, well-lit hallway with doors on the northern side, and windows on the southern.  The hall continues on to the west, and finishes to the east at the entrance of the building."
	exit "north" to "Psychadelic Room"
	exit "west" to "More Mansion Hallway"
	exit "east" to "Mansion Foyer"
}

Thing
{
	name "blank wall"
	describe "The wall feels very solid and slightly damp. It is covered in moss, and there is a fairly large crack at its base. It also has, much to your surprise, an oil painting hanging from a small nail."
	place "Natural Alcove"
	component
	syn "wall"
	syn "right wall"
}

Room
{
	name "Castle Courtyard"
	describe "This is the courtyard of a large, white stone castle.  The castle's four towers reach high above here.  The eastern wall is flawless marble, although it exhibits a much better resistance to the elements than actual marble would.  The west wall, on the other hand, while having a similiar texture, is crumbled down in a V shape, as if it had been struck with something from above.  You could easily walk through the chasm formed in the wall, and there appears to be a misty forest that way.  To the south, you can enter the castle proper through a small doorway, and to the north, you can exit through the huge northern gate."
	theme "leaf"
	string "name" "Courtyard"
	exit "south" to "Castle Entrance"
	exit "north" to "Castle Entrance Archway"
	exit "west" to "Between the Rubble"
}

Location
{
	name "New Jersey Apartment Refrigerator"
	describe "A large, brown metal box, with a blue and white interior. It's sort of cold inside, but not remarkably so. There are a few stray packets of jello pudding lurking in the back, but nothing substantially like food."
	place "New Jersey Apartment Kitchen"
	feature "twisted.reality.plugin.OpenCloseContainer"
	extends "Class_Container"
	component
	syn "frige"
	syn "fridge"
	syn "refrigerator"
	opaque
	shut
}

Room
{
	name "Small Platform on the Rock"
	describe "This is a small platform on the rock.  A ladder is leaned up against the side of the cliff here, which leads up to a higher ledge.  There are some carvings here."
	exit "up" to "Very Narrow Rocky Ledge"
}

Room
{
	name "Shadow Glade"
	describe "A wide circle of flowers in full bloom surround you.  The air is thick and heavy with their sweet cloying scent, making it hard to breathe.  Shadows dance here and there, weaving in and out among the dark silvery  petals...   Looking more closely you see that they are stained dark with blood.  In a circle around you, seven dark gleaming portals stand shimmering darkly, each beckoning to you.   There is one for each direction except the south.  To the south lies a sheer wall of black void."
	exit "southwest" to "Silver Shadowed Glade(7)"
}

Room
{
	name "Flat Ledge"
	describe "This is a ledge into the cliff surrounding a tall castle in the clouds.  You can see clouds everywhere below you.  To your west, you can walk around the rock to where there is an entrance to the palace, or you can follow a rock path which is seemingly suspended in the clouds to your east."
	exit "east" to "Twisty Cloud Path"
	exit "west" to "Ledge in front of Castle in the Clouds"
}

Room
{
	name "Yurt Entrance"
	describe "This is the Entrance to the Yurt. The towering edifice of Yurtness stands proudly to your south, radiating whatever it is that Yurts radiate."
	exit "south" to "Yurt"
	exit "southwest" to "Forest Path"
	exit "northeast" to "Interesting East-West Path"
}

Room
{
	name "Cube Room"
	describe "A darkened, cubical room that's obviously some sort of geological mistake... the umarked walls and seamless floor make it seem rather incongruous with the rock below."
	theme "greystone"
	string "description" "It's too dark in here to see!"
	boolean "inhibit_exits" true
	string "name" "A Dark Place"
	boolean "inhibit_items" true
	extends "Class_Dark Room"
	exit "down" to "Secret Cave"
}

Thing
{
	name "little black book"
	describe "A small black book, covered in a sort of fake-leather. A loop on the side looks like it might hold a pen of some sort."
	place "Guyute"
	feature "divunal.magic.spells.Zorft"
	feature "divunal.magic.spells.Frotz"
	feature "divunal.rikyu.Posess"
	string "spell 0" "frotz"
	string "spell 1" "zorft"
	string "spell 2" "posess"
	extends "Class_Spell Book"
	syn "spellbook"
}

Room
{
	name "Clearing"
	describe "You are in a clearing, with a forest surrounding you on all sides. A path leads south.\nThere is a grating securely fastened into the ground."
	exit "east" to "Forest 2"
	exit "north" to "Forest 2"
	exit "south" to "Forest Path"
}

Room
{
	name "Between the Rubble"
	describe "You are between the pieces of rubble which probably once comprised the western wall of a large castle.  The castle's walls are about fifty or sixty feet thick, making this rubble a fairly long expanse to plod through, but there is a path between the debris.  This wall has been in a state of disrepair for some time now, judging by the age and size of the trees growing here -- some of the well-trimmed shrubs visible in the courtyard appear to have taken root and flourished here.  The rest of the castle is off to the east, where the path between the rubble leads into the small courtyard.  To the west, the rubble thins out, and you can see more trees.  The castle's wall seems unusual."
	theme "leaf"
	exit "west" to "Clearing in Small Forest"
	exit "east" to "Castle Courtyard"
}

Location
{
	name "qin"
	describe "A kind of seven-stringed zither made of a rosy wood.  The strings seem iridescent, as if waves of color and light pass through them.  The base of the instrument is very delicately etched with almost imperceptible whorls and floral patterns.  There are seven very tiny, metal knobs with which to tune the instrument."
	place "pale blue robe's right sleeve"
	broadcast
}

Thing
{
	name "demo center keyboard"
	describe "A KB101 Plus keyboard. It contains a wide variety of keys, including the ever popular \"Enter\". Like all KeyTronic keyboards, it looks as though it was designed in the '50s and made to withstand a direct nuclear attack, although the left Control key seems to be slightly crooked."
	place "Messy New Jersey Office"
	feature "demo.DemoComputerType"
	int "stars" 0
	thing "monitor" "demo center monitor"
	string "name" "keyboard"
	component
	syn "keyboard"
}

Location
{
	name "dark green overcoat"
	describe "A long, dark green overcoat with gold stitching along the cuffs and around the buttonholes and pockets. "
	place "Tenth"
	feature "twisted.reality.plugin.OpenCloseContainer"
	feature "twisted.reality.plugin.Put"
	boolean "clothing worn" true
	string "clothing location 2" "left arm"
	string "clothing location" "right arm"
	string "clothing appearance" "a dark green overcoat"
	extends "Class_Clothing"
	component
	syn "green overcoat"
	syn "overcoat"
	syn "coat"
}

Thing
{
	name "timer stop button"
	describe "This button is mounted on a sort of platform. It's fairly ordinary, or at least, as ordinary as any other button placed in the middle of nowhere."
	place "Mystic Field"
	string "name" "large blue button"
	syn "button"
	syn "blue button"
	syn "large blue button"
}

Thing
{
	name "Irlae Rod"
	describe "A rod of delicate craftsmenship about one's arm length. It combines a jade-colored stone which glitters as if lit from within, and a ruby crystal which makes it warm to the touch.  These two materials are set in opposing spirals to one and other. One end of the rod is pointed, and there is a translucent pearlescent bulb adorning the other."
	place "Tsiale"
	extends "Reality Pencil"
	syn "rod"
}

Room
{
	name "Other Underling's Office"
	describe "This is an office, most likely that of someone in a relatively low position.  There is a desk here, and also a chair, both of which are bolted to the floor.  The place is clean, but the walls are undecorated, and the space is small.  The smashed remains of a computer terminal litter the desk and floor."
	exit "northwest" to "Reception Area"
}

Room
{
	name "Moonlit Beach"
	describe "This beach is a small alcove in the high walls of cliffs to the east and west.  The sea is smooth, calm, and flat - catching the moonlight as a mirrow would.  A narrow crevice between the cliffs has had a path paved on it through the cliffs to the north.  The moon is shining through a break in the almost overcast cloud-cover above."
	theme "water"
	float "cloudiness" "0.4169256"
	thing "fling place" "Cloud Scene Balcony"
	handler "startup" "divunal.dream.FlingHandler"
	descript "cloudd" "The clouds are very turbulent.  They are swirling and thundering quite a bit."
	exit "north" to "Between the Cliffs"
	exit "east" to "West End"
}

Room
{
	name "Steam-Powered Library"
	describe "A small, cozy room, lined with bookshelves and softly lit by a brass chandelier hanging from the ceiling. An ornately carved sofa with dark green upholstery is set opposite a small reading table, and an Oriental rug of roughly the same color is spread out across the polished wooden floor. An archway leads north into a larger room, while the door to the south is a large metal contraption, held in place between two bookcases by a complicated system of pistons and hydraulics. On the left side of the door, there is a lever."
	theme "wood"
	descript "bookshelf door" "The southern door is closed."
	exit "north" to "Mansion Study"
	exit "south" notTo "Science Fiction Room" with "bookshelf door"
}

Room
{
	name "Obscure Corner of Bookstore"
	describe "This is an obscure corner of a bookstore.  Though the books are worn with age, they are nontheless in surprisingly good condition. The room has a sense of tiredness but it is kept well. There are few books here, and the place seems deserted, but footprints lie in the accumulated dust which signify that this place was not always as neglected. There is an exit to the southwest to a slightly brighter and more spacious room."
	theme "paper"
	feature "divunal.maxwell.AutoReturnGo"
	thing "special thing" "small brown book"
	exit "southwest" to "Rare Book Room, Lower Level"
}

Room
{
	name "Garden Maze(2)"
	describe "You might need some help, or you could have the knack, but as long as you're here, you're on the right track. The ground is covered by a thick fog, but there's just grass on the ground anyways."
	theme "leaf"
	string "name" "Garden Maze"
	exit "north" to "Garden Maze(4)"
	exit "west" to "Garden Maze(1)"
}

Thing
{
	name "Weirwood Cube"
	describe "This is a small cube made out of a deep red wood, polished until it gleams. Its corners are rounded.  In places it appears slightly translucent, and you can see pulsating points of light, like stars, under its surface."
	place "Maxwell"
	thing "teleport phrase Gyre and gimble in the wabe." "Observation Hallway"
	thing "teleport phrase There's no place like home." "Ruby Room"
	thing "teleport phrase Away, away..." "Ledge in front of Castle in the Clouds"
	thing "teleport phrase Ohm" "Underground Grotto"
	thing "teleport phrase Obscurity!" "Obscure Corner of Bookstore"
	thing "teleport phrase genome" "Genetic Laboratory"
	thing "teleport phrase magritte" "Portrait in the Sky"
	thing "teleport phrase Go Elsewhere" "Class Room"
	thing "teleport phrase go go gadget archetype" "Tenth"
	thing "teleport phrase Hello, Sailor!" "West of House"
	string "teleport message" "The Weirwood Cube vibrates visibly, as if something had struck a harmonic with it."
	handler "say" "divunal.maxwell.VoiceTeleport"
	extends "Class_Cube"
	syn "cube"
}

Player
{
	name "Mission-Critical Guest"
	describe ""
	boolean "score init" true
	int "score max" 1024
	int "score" 0
	string "adjective" "Mission-Critical"
	extends "Class_Guest"
	syn "guest"
	passwd ""
}

Thing
{
	name "bamboo teascoop"
	describe "A rather nondescript bamboo teascoop."
	place "Rikyu"
	feature "twisted.reality.author.MoodSet"
	extends "Reality Pencil"
	syn "teascoop"
	syn "scoop"
	syn "bamboo scoop"
}

Thing
{
	name "class_apple"
	describe "It appears to be a class_apple, but it is vague, indistinct, and little more than a blurry smear on reality."
	place "Food Box"
	string "eat text 1" "You eat "
	string "eat text 2" ". It is juicy and crisp, and quite tasty."
	extends "class_food"
}

Thing
{
	name "blue-grey vest"
	describe "A sturdy, medium-grey fabric on the back and sides meets a darker leather on the front of the garment.  The blue tinge is so slight as to make its effect seem more of an impression than something directly perceived.  Three midnight-blue buttons adorn the front of the vest.  "
	place "Jedin"
	string "clothing appearance" "a medium-grey vest"
	extends "Class_Tunic"
	syn "vest"
}

Room
{
	name "Messy New Jersey Office"
	describe "A strikingly mundane office, with peeling off-white plaster walls and a dirty old gray carpet. The room is lined with desks, all of which are heavily laden with computer equipment, manuals, paper bags, empty bottles, and other trash. A large red and yellow poster has been tacked to the northern wall, above a rather snazzy looking computer, and a black swivel chair is positioned in front of it."
	place "Demo"
	descript "development door openDesc" "A battered wooden doorway in the south wall leads out into the hall."
	exit "south" to "Demo Center East Wing" with "development door"
}

Thing
{
	name "demo center computer"
	describe "A large grey box labeled \"VA Research\", attached to a similarly colored keyboard. The monitor attached appears to have been originally intended for a Macintosh workstation, and is currently showing a very trippy screensaver of some kind."
	place "Messy New Jersey Office"
	string "name" "computer"
	component
	syn "computer"
}

Thing
{
	name "apple"
	describe "A juicy red apple, with smooth lush curves to make any man's mouth water.\n"
	place "Tsiale"
	feature "divunal.common.Eat"
	extends "class_apple"
}

Room
{
	name "Pine Grove"
	describe "South of this grove, you can two large cliffs flanking the small dirt path you are standing on. To your west, the path continues on its winding way through the trees. The trees are far too dense for you to proceed in any direction except along the path to the west, but they thin considerably to the south."
	theme "leaf"
	exit "west" to "Mansion Doorstep"
}

Thing
{
	name "executive toy"
	describe "This is a physical demonstration of Conservation of Momentum and classic Newtonian physics. There is a small base of a shiny black marble, from which stand four silver poles. These, in turn, support a brass crossbar.\n\nHanging from the crossbar are five shiny chrome bearings, suspended by wire. If you were to lift one and let it fall, it would smack into it's neighbor and come to an abrupt stop. The neighboring ball, however, would shudder as it passed the momentum on to the next in line, until the opposite ball would swing out.\n\nCurrently the executive toy is motionless, but there are enough fingerprint smears on the shiny chrome to imply tat it gets frequent use."
	place "Damien's Cubicle"
	component
	syn "toy"
}

Thing
{
	name "demo center jar-jar"
	describe "For christ's sake, it's a Jar-jar binks \"Official\" pez dispenser... Why are you even trying to looking at it?"
	place "Demo Center Gift Shop"
	feature "demo.DontGoThereGet"
	string "name" "Jar-jar Binks pez dispenser"
	component
	syn "jar-jar binks pez dispenser"
	syn "jar-jar binks"
	syn "pez dispenser"
	syn "dispenser"
	syn "jar-jar"
	syn "jar"
}

Location
{
	name "Large Glass Box"
	describe "A large, transparent glass box with a hinged top."
	place "Science and Technology Vehicle Area"
	feature "twisted.reality.plugin.Put"
	feature "twisted.reality.plugin.OpenCloseContainer"
	boolean "transparent" true
	string "open description" "It is currently open."
	string "closed description" "It is currently closed."
	string "name" "glass box"
	descript "open/close" "It is currently open."
	component
	syn "transparent glass box"
	syn "glass"
	syn "glass box"
	syn "box"
	broadcast
}

Thing
{
	name "pile of things"
	describe "A bunch of stuff is stacked along the wall.\n\nNo matter how much effort you put into it, this is all you can tell. A bunch of stuff is stacked against the wall."
	place "Damien's Cubicle"
	component
	syn "pile"
	syn "things"
}

Room
{
	name "Portrait in the Sky"
	describe "To the east, the path you are standing on ends at a picture frame framing what looks to be a hole in the sky.  Through the frame you can see a library room, as if it were a window.  To the west you can see a path leading to a tall castle far in the distance."
	exit "east" to "Art Gallery"
	exit "west" to "Path in the Clouds"
}

Thing
{
	name "meteorite"
	describe "A scorched piece of rock which, by the pockmarks on its surface and the uneven way that it is shaped, appears to have fallen from the sky.  It is dark grey and smells of scorched iron."
	place "recycle bin"
}

Location
{
	name "Mansion Bedroom Writing Desk"
	describe "A dark, polished wooden desk, set with bookshelves and an inkwell."
	place "Tenth's Chamber"
	feature "twisted.reality.plugin.Put"
	feature "twisted.reality.plugin.furniture.Stand"
	feature "divunal.common.SitAt"
	string "name" "writing desk"
	int "maximum occupancy" 1
	string "preposition" "on"
	string "player preposition" "sitting at"
	component
	syn "desk"
	syn "writing desk"
	broadcast
}

Room
{
	name "Mod Seven Short Hallway"
	describe "The hallway behind the \"Science Fiction/Fantasy\" sign leads to two rooms. You wonder which contains \"Fantasy\".\nTo the north is a rather squalid bathroom, to the southeast is a room with a bunch of text on the door, and to the southwest there is a door with an interesting display. The door to the southwest is slightly open."
	exit "east" to "Mod Seven"
}

Thing
{
	name "wrapper"
	describe "Thank you for choosing nice Chinese Restaurant. To use chopstick:\n\n1) Grasp frimly in fingers\n\n2) Move back and forthly with hands.\n\n3) Now you can pick up anything!"
	place "Proper English Library"
}

Room
{
	name "Metal Tube"
	describe "This huge metal tube is spacious and the air is especially clean here.  The edges of the tube gleam with a soft, sourceless illumination.  There is a door out of the tube to the west, and the tube bends around to the southeast and continues."
	exit "southeast" to "Dent in Tube"
	exit "west" to "End of Catwalk"
}

Room
{
	name "Garden Maze(1)"
	describe "The hedges in here are very high--seven or eight feet tall. There's little to look at, so two items easily stick out. There is a hammer on the ground to the north, and to the east there is a pair of scissors."
	theme "leaf"
	string "name" "Garden Maze"
	exit "north" to "Garden Maze(3)"
	exit "east" to "Garden Maze(2)"
	exit "south" to "Garden Maze"
}

Room
{
	name "Divunal Room"
	describe "This room is a series of gateways to different places in the Age of Divunal.  Now, there is only one which has been uncovered.  To the north, there is a gateway with a crude drawing of a sideways oval with five lines drawn upwards from various points on it.  Through this gateway, you can see a small room that is littered with rubble."
	theme "greystone"
	exit "north" to "Cramped Transporter Booth"
}

Room
{
	name "Spiral Landing"
	describe "This is a landing on the spiral staircase, with large windows in the southeastern corner.  Through the windows you can see a pine forest, and a large plateau, which you are slightly above at this height.  In the distance, on top of one of the cliffs you can see a square stone with lightening flickering around it, and black scorchmarks littering the rocky plateau around it."
	exit "up" to "Slanted Mansion Hallway"
	exit "down" to "Mansion Foyer"
}

Location
{
	name "sarcophagus"
	describe "An ornately carved stone coffin, lined with small hieroglyphics and symbols."
	place "Chateau Library(1)"
}

Room
{
	name "HC Library"
	describe "A bright room, slightly colder than the rest of the library, to your south there is a desk with a receptionist sitting at it.  To your north you see a short hallway with a water fountain and elevators.  Ahead of you, to the west, is an open lounge area with several bookshelves, a few iMacs, some terminals, and some bus schedules."
	theme "paper"
	exit "east" to "HC Magic Board Landing"
	exit "south" to "Nondescript Section"
}

Thing
{
	name "Gold Cube"
	describe "A white box."
	place "Gold Room"
	extends "Class_Cube"
	component
	syn "cube"
}

Room
{
	name "Mansion Balcony"
	describe "This is a balcony overlooking a war-torn industrial city.  Blimps are flying overhead, and you can see occasional explosions and flashes of light from the city streets.  French doors lead back into a large victorian mansion to the south."
	theme "wood"
	descript "balcony double doors openDesc" ""
	exit "south" to "Tenth's Chamber" with "tenths folding balcony doors"
}

Room
{
	name "Chateau Parlor"
	describe "A Chateau Parlor looking as if it needs to be described."
	place "Inheritance"
	theme "greystone"
	exit "north" to "Chateau Hallway(2)"
	exit "south" to "Chateau Hallway(3)"
}

Thing
{
	name "aging leather tome"
	describe "The aging leather tome is open to page 1. It reads:\n\"The sucessful sourcerer needs many things to accomplish his task, but primarily, an open mind is required, as well as a soul willing to experiment, and a heart willing to believe.\""
	place "great bookshelf"
	string "page_#3" "Required ingredients\n\n-   a sprig of sage\n-   one vial of moonshine\n-   a spider's web\n-   the eye of a newt"
	string "page_#2" "The cauldron is the most important part of any spellcaster's posessions."
	string "page_#1" "The sucessful sourcerer needs many things to accomplish his task, but primarily, an open mind is required, as well as a soul willing to experiment, and a heart willing to believe."
	int "page_number" 1
	extends "Class_Book"
	syn "leather tome"
	syn "tome"
}

Thing
{
	name "Class_Pants"
	describe "A white box."
	place "Clothing Box"
	string "clothing location" "left leg"
	string "clothing location 2" "right leg"
	extends "Class_Clothing"
}

Thing
{
	name "mainspring"
	describe "A thick metal disc, composed of a long strip of metal wrapped into a tight spiral shape. The spiral begins with a small metal ring in the center, and ends in a small fastening bracket on its outside edge."
	place "Mansion Maintenance Closet"
}

Thing
{
	name "tea bowl"
	describe "A rather nondescript tea bowl."
	place "Tea House"
	feature "divunal.rikyu.DrinkSpecialTea"
	syn "teabowl"
	syn "bowl"
}

Thing
{
	name "Bun-Bun squeaky toy"
	describe "A grey, white, and vaguely rabbit shaped rubber figurine with long floppy ears and dark, vicious eyes."
	place "Large Glass Box"
	feature "demo.ToySqueeze"
	feature "demo.ToyDrop"
	thing "repop" "Large Glass Box"
	syn "squeaky toy"
	syn "toy"
	syn "bun"
	syn "bun-bun"
	syn "bunbun"
}

Location
{
	name "knapsack"
	describe "A well-worn, and very spacious"
}

Thing
{
	name "bookshelf door"
	describe "A blue box."
	place "Science Fiction Room"
	theme "wood"
	feature "twisted.reality.author.Obstruct"
	feature "divunal.tenth.LibraryDoorOpen"
	feature "divunal.tenth.LibraryDoorLook"
	thing "steam source" "Mansion Steam Engine"
	boolean "obstructed" true
	boolean "yellow pushed" false
	string "exit message" "You squeeze between the bookshelves through the door."
	string "obstructed message" "You can't go that way."
	long "steam off" 926639534319
	handler "shelf close" "divunal.tenth.LibraryCloseHandler"
	component
}

Room
{
	name "Continued Chasm"
	describe "The chasm is somewhat regular here.  It gets dirtier and more ragged to the south.  Hewn into the wall of the chasm is what looks like a makeshift stairwell leading upwards, and though it is a bit rough and uneven, it appears to be quite serviceable."
	exit "up" to "Even More Office Hallway"
	exit "west" to "Chasm Bottom"
}

Room
{
	name "Secret Cave"
	describe "This is a super-secret cave in the side of the rock..."
	theme "greystone"
	string "name" "A Dark Place"
	string "description" "It's too dark in here to see!"
	
	property "isLit" "divunal.common.IsLit"
	extends "Class_Dark Room"
	opaque
	shut
	exit "north" to "Very Narrow Rocky Ledge"
	exit "south" to "Deeper In The Rock"
	exit "up" to "Cube Room"
	claustrophobic
}

Thing
{
	name "old book"
	describe "A book written in an indescribable language, discussing unmentionable things in an ineffable style."
	place "Damien's Study"
	syn "old"
	syn "book"
}

Player
{
	name "Maxwell"
	describe "A wiry, short man, with grey hair and eyes. His skin tone appears rosy when you look straight at him, but gives you an impression of colorlessness when you see him from the corner of your eye.  His left hand has a clear, black line drawing of a circle on it."
	place "Demo Center Bathroom Stall"
	gender m
	thing "oldlocation" "Messy New Jersey Office"
	string "visit color" "ghostly white"
	
	persistable "clothing left leg" "twisted.reality.Stack" val "thing pair of grey jeans\n" key "twisted.reality.Stack@584e2e4"
	
	persistable "clothing right leg" "twisted.reality.Stack" val "thing pair of grey jeans\n" key "twisted.reality.Stack@584e302"
	long "stamina time" 930513195556
	float "stamina" "-0.6537466"
	long "health time" 930513195556
	float "health" "1.0"
	float "psyche" "0.1"
	
	persistable "clothing right arm" "twisted.reality.Stack" val "thing grey cotton shirt\n" key "twisted.reality.Stack@584e279"
	
	persistable "clothing left arm" "twisted.reality.Stack" val "thing grey cotton shirt\n" key "twisted.reality.Stack@584e23d"
	
	persistable "clothing chest" "twisted.reality.Stack" val "thing grey cotton shirt\nthing neat grey tunic\n" key "twisted.reality.Stack@584e211"
	
	persistable "clothing neck" "twisted.reality.Stack" val "thing dark grey cape\n" key "twisted.reality.Stack@58579e1"
	
	persistable "clothing right foot" "twisted.reality.Stack" val "thing pair of grey soft leather boots\n" key "twisted.reality.Stack@58579fa"
	
	persistable "clothing left foot" "twisted.reality.Stack" val "thing pair of grey soft leather boots\n" key "twisted.reality.Stack@58579c5"
	boolean "washed" true
	int "learned frotz" 2
	int "learned zorft" 1
	int "spells learned" 5
	boolean "isLit" false
	descript "clothing" {Pronoun Of("Maxwell"), " is wearing ", Name of("dark grey cape"), ", ", Name of("neat grey tunic"), ", ", Name of("grey cotton shirt"), ", ", Name of("pair of grey jeans"), ", ", "and ", Name of("pair of grey soft leather boots"), "."}
	extends "Class_Human"
	syn "max"
	ability "twisted.reality.author.Pause"
	ability "divunal.magic.Cast"
	ability "twisted.reality.author.FloatSet"
	ability "twisted.reality.author.GC"
	ability "twisted.reality.author.Refrump"
	ability "divunal.magic.spells.Zorft"
	ability "divunal.magic.spells.Frotz"
	architect
	passwd "Mam6MEtmnRUpk"
}

Room
{
	name "Canyon View"
	describe "You are at the top of the Great Canyon on its west wall. From here there is a marvelous view of the canyon and parts of the Frigid River upstream. Across the canyon, the walls of the White Cliffs join the mighty ramparts of the Flathead Mountains to the east. Following the Canyon upstream to the north, Aragain Fallsmay be seen, complete with rainbow. The mighty Frigid River flows out from a great dark cavern. To the west and south can be seen an immense forest, stretching for miles around. A path leads northwest. It is possible to climb down into the canyon from here."
	exit "west" to "Forest 2"
	exit "down" to "Rocky Ledge"
}

Location
{
	name "demo center black swivel chair(1)"
	describe "It appears to be a demo center swivel chair, but it is vague, indistinct, and little more than a blurry smear on reality."
	feature "twisted.reality.plugin.furniture.Stand"
	feature "twisted.reality.plugin.furniture.Sit"
	string "name" "black swivel chair"
	string "player preposition" "sitting on"
	string "preposition" "on"
	int "maximum occupancy" 1
}

Location
{
	name "pale blue robe's left sleeve"
	describe "The pale blue robe's left sleeve."
	place "Yumeiko's pale blue kimono-like robe"
	feature "twisted.reality.plugin.clothes.ClothingPut"
	component
	syn "lsleeve"
}

Room
{
	name "Mansion Basement Engine Room"
	describe "A dark, humid place, pervaded by a strange musty smell. The floor is little more than well packed earth, and the dark greyish brick of the walls is damp with condensation. A bare glass bulb provides a dim, flickering light to the room, hanging by its cord from the uncovered wooden beams that form the ceiling. A large brass and iron steam engine stands against the northern wall, laden with controls and gauges, next to a huge cylindrical tank which leaves just enough space to squeeze past to the eastern end of the room."
	theme "greystone"
	exit "east" to "Mansion Basement Pump Area"
	exit "west" to "Mansion Basement"
}

Thing
{
	name "pair of black leather boots"
	describe "A pair of tall black leather riding boots, the tops of which have been folded down to knee length to make them less restrictive."
	place "Tenth"
	boolean "clothing worn" true
	string "clothing appearance" "knee high black leather boots"
	extends "Class_Shoes"
	component
	syn "black leather boots"
	syn "leather boots"
	syn "boots"
}

Thing
{
	name "pair of black leather shoes"
	describe "It appears to be a pair of black leather shoes, but it is vague, indistinct, and little more than a blurry smear on reality."
	place "Tsiale"
	boolean "clothing worn" true
	extends "Class_Shoes"
	component
	syn "shoes"
	syn "leather shoes"
}

Thing
{
	name "pair of black pants"
	describe "A pair of close-fitting black pants, apparently made from a single, seamless piece of fabric."
	place "Tsiale"
	boolean "clothing worn" true
	string "clothing appearance" "black leggings"
	extends "Class_Pants"
	component
	syn "leggings"
	syn "pants"
}

Room
{
	name "Mansion Attic"
	describe "null"
	exit "down" to "Mansion Upper Hall" with "attic staircase"
}

Room
{
	name "Inner Garden"
	describe "The paths leading northeast and south here are laid with small, flat stones. Over to the east is a stone lantern, in front of which is a stone basin, filled with water. To the north is a tea house, surrounded by small trees and bushes. All around this area is a tall bamboo fence."
	theme "leaf"
	string "name" "Uchi-rojj"
	exit "south" to "Outer Tea Garden" with "naka-mon"
}

Location
{
	name "pale blue robe's right sleeve"
	describe "The pale blue robe's right sleeve."
	place "Yumeiko's pale blue kimono-like robe"
	feature "twisted.reality.plugin.clothes.ClothingPut"
	component
	syn "rsleeve"
}

Thing
{
	name "neat grey tunic"
	describe "A clean and well-pressed light grey tunic made from high-quality fabric."
	place "Maxwell"
	boolean "clothing worn" true
	extends "Class_Tunic"
	component
	syn "tunic"
}

Room
{
	name "Storage Room"
	describe "This room looks as if it's simply used to store old junk."
	mood "providing light"
	theme "greystone"
	boolean "inhibit_items" true
	boolean "inhibit_exits" true
	boolean "isLit" true
	boolean "frotzed" true
	descript "lighting" "A pure white glow eminates from the A Dark Place, bathing it in light."
	extends "Class_Dark Room"
	shut
}

Thing
{
	name "brass paperweight"
	describe "A short brass dome about the size of a coffee cup, with a small glass lens set into its center."
	place "Tenth"
	syn "pager"
	syn "paperweight"
}

Thing
{
	name "clean book"
	describe "This is an oblong, linoleum-bound book with a shining and clean surface, entitled (according to its cover) \"The Tall Kitchen\"."
	place "Small Book Room"
	extends "Class_Small Book"
	syn "book"
}

Room
{
	name "Chateau Hallway(16)"
	describe "A Chateau Hallway looking as if it needs to be described."
	place "Inheritance"
	theme "greystone"
	string "name" "Chateau Hallway"
	exit "north" to "Chateau Sitting Room"
	exit "west" to "Chateau Antechamber"
}

Room
{
	name "Chateau Attic"
	describe "A Chateau Attic looking as if it needs to be described."
	place "Inheritance"
	theme "dark"
	exit "west" to "Chateau Attic(3)"
	exit "east" to "Chateau Attic(1)"
	exit "down" to "Chateau Hallway(4)"
}

Room
{
	name "Chateau Hallway(15)"
	describe "A Chateau Hallway looking as if it needs to be described."
	place "Inheritance"
	theme "dark"
	exit "west" to "Chateau Hallway(5)"
}

Room
{
	name "Chateau Hallway(14)"
	describe "A Chateau Hallway looking as if it needs to be described."
	place "Inheritance"
	theme "greystone"
	string "name" "Chateau Hallway"
	exit "south" to "Chateau Hallway(5)"
	exit "east" to "Chateau Bedroom"
	exit "west" to "Chateau Library(2)"
}

Room
{
	name "Chateau Hallway(13)"
	describe "A Chateau Hallway looking as if it needs to be described."
	place "Inheritance"
	theme "dark"
	string "name" "Chateau Hallway"
	exit "east" to "Chateau Library"
	exit "west" to "Guest Room"
	exit "south" to "Chateau Hallway(6)"
}

Room
{
	name "Chateau Hallway(12)"
	describe "A Chateau Hallway looking as if it needs to be described."
	place "Inheritance"
	theme "dark"
	string "name" "Chateau Hallway"
	exit "north" to "Study"
	exit "west" to "Chateau Hallway(11)"
}

Room
{
	name "Chateau Hallway(11)"
	describe "A Chateau Hallway looking as if it needs to be described."
	place "Inheritance"
	theme "dark"
	exit "east" to "Chateau Hallway(12)"
	exit "west" to "Chateau Hallway(10)"
}

Room
{
	name "Chateau Hallway(10)"
	describe "A Chateau Hallway looking as if it needs to be described. It should have a couch or something, pointed out at the picture window."
	place "Inheritance"
	theme "dark"
	exit "east" to "Chateau Hallway(11)"
	exit "west" to "Chateau Hallway(9)"
}

Room
{
	name "Demo Center West Wing"
	describe "This is the west wing of the demo center. The walls are a polished, gleaming, white substance, and the floor is perfectly smooth black marble. This particular room is triangular, with an arched doorway set into each of the three walls. A sign reading \"Back To Main Demo Center\" is hung over the eastern arch, while the southwest and northwest arches are unlabeled. A small drinking fountain stands alone in the center of the floor."
	place "Demo"
	exit "east" to "Demo Center West Wing Lobby"
	exit "southwest" to "Demo Center Waiting Room"
	exit "northwest" to "Greenhouse Entrance"
}

Room
{
	name "Observation Hallway"
	describe "This is an oblong rectangular room with a set of windows built into the southern wall.  The walls are all built from a pure, white marble.  The windows overlook a rocky plain from far above.  Far in the distance, you can make out a large stone altar with large black scorch-marks on and surrounding it.  A large marble archway leads north, into a multi-colored glittering hallway, and a modest doorway in the southeastern corner bears the legend \"stairs\".  Another, perhaps even more modest, door is set into the western wall, with the legend \"Guest Room\"."
	exit "west" to "Guest Chamber"
	exit "southeast" to "East Wing Spiral Staircase Top"
	exit "north" to "Jewel Bedecked Hallway"
}

Thing
{
	name "wooden table"
	describe "The first thing you notice is  the oppulence of this table -- it is constructed of solid oak and polished to a high degree. It's the sort of table that makes you want to sit down (in one of the plush leather arm chairs) and read a scholarly tome. Nevertheless, someone has managed to turn this comfortable work space into a surprisingly anal computer desk. The table top is covered in manuals and books on tax law, drawing an ironic contrast to the ancient texts on every wall."
	place "Proper English Library"
	extends "Class_Container"
	component
	syn "table"
	syn "wooden"
}

Thing
{
	name "Class_Cube"
	describe "A grey box."
	place "Other Box"
	handler "say" "divunal.maxwell.VoiceTeleport"
}

Thing
{
	name "very very small rocks"
	describe "These rocks are very small.  They are barely visible to the naked eye."
	component
	syn "rocks"
}

Location
{
	name "tupperware lunchbox"
	describe "A blue tupperware lunchbox with a cartoon Tux on the front."
	place "Chenai"
	feature "twisted.reality.plugin.OpenCloseContainer"
	feature "twisted.reality.plugin.Put"
	boolean "clothing worn" true
	extends "class_hat"
	component
	syn "tupperware"
	syn "lunch box"
	syn "lunchbox"
	syn "box"
	opaque
	shut
}

Room
{
	name "Under the Bookshelf"
	describe "There is more room under this bookshelf than you thought. In fact, then floor slopes quickly downward quickly here; a few paces down and you could probably stand up."
	theme "paper"
	exit "down" to "Natural Alcove"
	exit "east" to "Quiet Niche"
}

Thing
{
	name "leather book"
	describe "An ancient, ancient tome. The ink (old faded, and red) is cracked, and the huge brass locks (??) have almost fallen off the edges. The binding is odd, it looks like leather, but feels slightly different.\n\nIt is not possible to read; the handwriting is so old that it almost looks liks alien gibberish."
	place "Damien's Study"
	syn "leather"
	syn "book"
}

Thing
{
	name "old sandal"
	describe "An rather nondescript old sandal."
	place "large black cauldron"
}

Thing
{
	name "pair of green socks"
	describe "A pair of shin high green cotton socks."
	place "Tenth"
	boolean "clothing worn" true
	extends "Class_Shoes"
	component
	syn "socks"
	syn "green socks"
}

Thing
{
	name "light"
	describe "A long, harsh flourescent tube. It emits a loud buzzing and an unforgiving glare."
	place "Damien's Office,entering"
	component
}

Location
{
	name "demo center wastebasket"
	describe "A black plastic wastebasket, with a small swinging door labeled \"TRASH\"."
	place "Demo Center Lavatory"
	feature "twisted.reality.plugin.Put"
	string "name" "black plastic wastebasket"
	component
	syn "wastebasket"
	syn "basket"
	syn "plastic wastebasket"
}

Thing
{
	name "instruction manual"
	describe "A small folded booklet of white paper, with a blue spherical logo and the title \"Twisted Reality Demo Center Instruction Manual\"."
	place "Maxwell"
	feature "divunal.bookstore.TrivialOpenRead"
	thing "repop" "grey plastic chairs"
	string "book text" "\n\"Hello, Guest! And welcome to the Twisted Reality Demo Center. Here, you can experience some of the many interesting features that make TR the Ergonomic Power Tool of interactive text development that it is.\"\n\n\"Twisted Reality, like Infocom's classic text based games, allows for a wide range of interaction with the environment. Feel free to experiment; Entering commands like \"close door\", \"pull lever\", or \"turn dial to liquefy\" can produce many interesting effects.\"\n\n\"The Demo Center, while small, has a lot of objects in it. When you look at room descriptions and visible objects, try looking at some of the other things their descriptions mention; A fairly complex Zork-like puzzle is here if you can find it.\""
	syn "manual"
}

Thing
{
	name "spatula poetry collection"
	describe "The spatula poetry collection is open to page 8. It reads:\n\"\n\tso maybe i could hit the restart button\n\tand begin over with a new player\n\tthen maybe i wouldn't have to clean the fridge\n\tor burn so many pictures\n\n\n\n\t\t\t\t\t--End\n\n\n\t\t\t-=8=-\""
	place "tupperware lunchbox"
	string "page_#3" "\n\tmutual understanding of individualism\n\tthe fact that their goal of\n\tmaking us one and blurring the edges\n\tso much \n\tyou couldn't tell where you ended and i began\n\tmade\n\tme\n\tsick\n\n\t\t\t-=3=-"
	string "page_#2" " \t                        The Spatula\n\n\tour journey i'd hoped\t\n\twould have been longer\n\tbut the incidences of pronouns and peragotives\n\twas too high\n\tthere\n\twas\n\tno\n\n\n\t\t\t-=2=-"
	string "page_#1" "\n\n\t        \tThe Spatula and Other Poems\n\n\t\t\t     by\n\n\t\t           Mistress of Pain"
	string "page_#8" "\n\tso maybe i could hit the restart button\n\tand begin over with a new player\n\tthen maybe i wouldn't have to clean the fridge\n\tor burn so many pictures\n\n\n\n\t\t\t\t\t--End\n\n\n\t\t\t-=8=-"
	string "page_#7" "\n\tover me\n\tbut whatever it is\n\ti always end up tossing and turning\n\tlooking at the clock hoping that\n\tit\n\twould\n\tend\n\n\n\n\t\t\t-=7=-"
	string "page_#6" "\t\n\twhen ever i go over to your house\n\tand we snuggle up to watch your dads old dirty films\n\ti can't ever get to sleep afterwards\n\tmaybe it's the fact that there are no knobs on my doors\n\tor maybe it's because i secertly think\n\tthat you prefer the swedish school girls form the films\n\n\n\n\n\t\t\t-=6=-"
	string "page_#5" "\n\tme beacuse when i was little\n\tthere was a circus that came to town every summer\n\tthe fact that i'm still frightend of clowns \n\tis \n\todd\n\tthough\n\ti'd have to admitt\n\n\n\n\t\t\t-=5=-"
	string "page_#4" "\n\tso i took the bus home\n\tto a place that had bare walls\n\tand doors with no knobs\n\ti like being able to look in on people\n\tdespite the fact that i'm the only one home\n\tthat\n\tdoesn't \n\tbother\n\n\n\t\t\t-=4=-"
	int "page_number" 8
	extends "Class_Book"
	syn "poetry"
	syn "book"
	syn "the spatula"
	syn "poetry book"
}

Thing
{
	name "reference book"
	describe "An Overview of the DR-127 Departure/Withdrawal Forms and Their Application in Income-Based RCFs.\n\nIt seems quite thick."
	place "Proper English Library"
	syn "book"
}

Room
{
	name "Path in the Clouds"
	describe "This is a wide, smooth stone path through a sea of clouds. The path curves around here. To your west you can see a tall castle in the clouds with many gravitationally impossible protrusions, and to your east you see what looks like a small square at the end of the path."
	exit "east" to "Portrait in the Sky"
	exit "northwest" to "Twisty Cloud Path"
}

Room
{
	name "Chateau Hallway(9)"
	describe "A Chateau Hallway looking as if it needs to be described."
	place "Inheritance"
	theme "dark"
	string "name" "Chateau Hallway"
	exit "east" to "Chateau Hallway(10)"
	exit "west" to "Chateau Hallway(8)"
}

Room
{
	name "Chateau Hallway(8)"
	describe "A Chateau Hallway looking as if it needs to be described."
	place "Inheritance"
	theme "dark"
	string "name" "Chateau Hallway"
	exit "east" to "Chateau Hallway(9)"
	exit "north" to "Antiques Room"
}

Thing
{
	name "long glass tube"
	describe "A large, vertical glass tube, capable of holding a standing humanoid person comfortably within it. "
	place "Genetic Laboratory"
	descript "my person" "There appears to be a person floating in some fluid inside the tube."
	component
	syn "tube"
}

Thing
{
	name "wooden ring"
	describe "A small polished wooden ring, hanging from a ceiling panel by a white piece of string."
	place "Mansion Upper Hall"
	feature "divunal.tenth.AtticPull"
	handler "attic door close" "divunal.tenth.AtticCloseHandler"
	component
	syn "piece of string"
	syn "string"
	syn "rin"
	syn "small wooden ring"
	syn "ring"
}

Room
{
	name "Chateau Hallway(7)"
	describe "A Chateau Hallway looking as if it needs to be described."
	place "Inheritance"
	theme "dark"
	string "name" "Chateau Hallway"
	exit "south" to "Antiques Room"
	exit "east" to "Chateau Hallway(6)"
}

Room
{
	name "Chateau Hallway(6)"
	describe "A Chateau Hallway looking as if it needs to be described."
	place "Inheritance"
	theme "dark"
	string "name" "Chateau Hallway"
	exit "north" to "Chateau Hallway(13)"
	exit "west" to "Chateau Hallway(7)"
	exit "east" to "Chateau Staircase Landing"
}

Thing
{
	name "padlock"
	describe "The padlock looks like it can do the job. It is emblazoned with the legend, \"Master\" along the front."
	place "Intersection"
	component
	syn "lock"
}

Thing
{
	name "bookshelf"
	describe "A simple, metal bookshelf, held together by screws and a sticky, web-like substance. All of the edges are carefully covered, perhaps someone was child-proofing here?"
	place "Damien's Study"
	component
}

Room
{
	name "Chateau Hallway(5)"
	describe "A Chateau Hallway looking as if it needs to be described."
	place "Inheritance"
	theme "dark"
	exit "north" to "Chateau Hallway(14)"
	exit "east" to "Chateau Hallway(15)"
	exit "west" to "Chateau Hallway(4)"
}

Room
{
	name "Chateau Hallway(4)"
	describe "A Chateau Hallway looking as if it needs to be described."
	place "Inheritance"
	theme "dark"
	exit "up" to "Chateau Attic"
	exit "east" to "Chateau Hallway(5)"
	exit "west" to "Chateau Staircase Landing"
}

Thing
{
	name "clay chillum"
	describe "A totally irae chillum, mon."
	place "pipe rack"
	string "subjectHearsPrepare" "You pack up a phatty bowl in the $t"
	string "alreadyLit" "Duuude, the $t is already blazin'!"
	string "othersHearLight" "$m sparks up the $t"
	string "subjectHearsLight" "You spark up the $t"
	string "othersHearPrepare" "$m packs up a phatty bowl in the $t"
	string "subjectHearsSmoke" "You pull a monster cloud off the $t ."
	string "othersHearSmoke" "$m pulls a monster cloud off the $t ."
	string "unlitPipe" "Aw, duuude, the $t isn't lit!"
	string "emptyPipe" "The $t is empty. Packy-pack it up!"
	string "alreadyPrepared" "The $t is already packed full, maan!"
	boolean "lit" true
	int "litTime" 9
	extends "Class_Smokeable"
	syn "chillum"
	syn "clay pipe"
}

Room
{
	name "Chateau Hallway(3)"
	describe "A Chateau Hallway looking as if it needs to be described."
	place "Inheritance"
	theme "greystone"
	string "name" "Chateau Hallway"
	exit "south" to "Chateau Sitting Room"
	exit "west" to "Chateau Lavatory"
	exit "north" to "Chateau Parlor"
}

Thing
{
	name "worn grey leather book"
	describe "A worn, palm-sized leather book that is in good condition despite the destroyed appearance of its cover.  Some words used to be etched into the cover, but they are long since illegible."
	place "Maxwell"
	feature "divunal.magic.spells.Zorft"
	feature "divunal.magic.spells.Frotz"
	string "spell 0" "zorft"
	string "spell 1" "frotz"
	boolean "isLit" false
	extends "Class_Spell Book"
	syn "grey leather book"
	syn "leather book"
	syn "grey book"
	syn "book"
}

Thing
{
	name "foo"
	describe "A rather nondescript foo."
	place "Garden Maze"
}

Room
{
	name "Chateau Hallway(2)"
	describe "A Chateau Hallway looking as if it needs to be described."
	place "Inheritance"
	theme "greystone"
	string "name" "Chateau Hallway"
	exit "south" to "Chateau Parlor"
	exit "west" to "Chateau Pantry"
}

Room
{
	name "Chateau Hallway(1)"
	describe "A Chateau Hallway looking as if it needs to be described."
	place "Inheritance"
	theme "greystone"
	string "name" "Chateau Hallway"
	exit "south" to "Chateau Dining Hall(1)"
	exit "east" to "Chateau Kitchen"
}

Thing
{
	name "southern tapestry"
	describe "Though this tapestry is partially obscured, you can see several images of large winged creatures carrying people away. Though it's hard to understand precisely what is going on, it seems these \"angels\" victims are in much pain."
	place "Guyute's Bedroom"
	component
	syn "tapestry"
	syn "south"
}

Thing
{
	name "Meredith's west wall"
	describe "A haphazard collection of random stupid pictures hang on the west wall."
	place "Meredith's Hell Hole"
	string "name" "west wall"
	component
	syn "wall"
	syn "wwall"
}

Room
{
	name "Scenic Junction"
	describe "Concrete paths lead four ways away from this junction, to the north where you can see a bus stop in the distance, to the northwest in the direction of the library, to the southeast towards some other buildings, or to the west or east, which haven't been finished yet."
	exit "northwest" to "Middle of Path"
	exit "southeast" to "Another Junction"
	exit "north" to "Bus Stop Junction"
}

Thing
{
	name "clue leaves"
	describe "Where did these come from?!?! There aren't any trees around, though judging by the mold on them they've probably been here a long time. Strangely enough, the mold seems to have grown in the shape of two letters, an A and a M."
	place "Garden Maze(7)"
	string "name" "pile of leaves"
	component
	syn "leaves"
	syn "pile of leaves"
	syn "pile"
}

Thing
{
	name "Brita Water Filter"
	describe "A sleek transparent pitcher filled with clear water, with a white plastic filter assembly and handle."
	place "New Jersey Apartment Refrigerator"
	syn "filter"
	syn "water filter"
	syn "brita filter"
}

Room
{
	name "Driveway"
	describe "The far end of a long gravel driveway leading downhill to the north, where the dark outlines of a house loom above the horizon. To the south, an old dirt road is visible through an opening in the trees, and to the east and west are endless yellow fields of neglected corn."
	place "Inheritance"
	theme "leaf"
	exit "south" to "Country Road"
	exit "north" to "Gravel Driveway(2)"
}

Room
{
	name "Inside Oak Tree"
	describe "Though the tree is big, it's still a little cramped in here. However, there's a ladder leading down into the darkness."
	theme "leaf"
	descript "door in oak tree openDesc" "To the south, here is a door leading to a green-looking garden."
	exit "down" to "Underground Grotto"
	exit "south" to "Ivy Garden" with "door in oak tree"
}

Thing
{
	name "shirt with an owl insignia"
	describe "This is a grey T-shirt with the insignia of an owl on it."
	place "James"
	boolean "clothing worn" true
	extends "Class_Shirt"
	component
	syn "shirt"
	syn "owl shirt"
}

Thing
{
	name "Xian action figure"
	describe "A white box."
	syn "figure"
}

Player
{
	name "Aaron"
	describe "A tall young man with blond hair.\n"
	gender m
	thing "oldlocation" "Aaron's test room"
	
	persistable "clothing right arm" "twisted.reality.Stack" val "thing faded brown coat\n" key "twisted.reality.Stack@5857269"
	
	persistable "clothing left arm" "twisted.reality.Stack" val "thing faded brown coat\n" key "twisted.reality.Stack@58572df"
	
	persistable "clothing chest" "twisted.reality.Stack" val "thing faded brown coat\n" key "twisted.reality.Stack@5857352"
	float "health" "1.0"
	long "health time" 938212952099
	float "stamina" "0.0"
	long "stamina time" 938212952099
	descript "clothing" {Pronoun Of("Aaron"), " is wearing ", "Faded brown coat", "."}
	extends "Class_Human"
	architect
	passwd "AahPWY1x6MDFI"
}

Location
{
	name "class_pistol clip"
	describe "A blue box."
	place "Tenth's Chamber"
	feature "inheritance.gun.ReleaseClip"
	feature "inheritance.gun.ClipLook"
	feature "inheritance.gun.BulletPut"
	feature "inheritance.gun.BulletGet"
	int "bullet capacity" 8
	string "clip type" "insert clip type/caliber here"
}

Thing
{
	name "western tapestry"
	describe "This tapestry is mostly covered by the bed, but an image of a large machine is peeking out. One can't be sure the purpose of this machine, but from the gears and pistons placed all around it, it can't be good."
	place "Guyute's Bedroom"
	component
	syn "tapestry"
	syn "west"
}

Location
{
	name "glasses case"
	describe "A rather nondescript glasses case."
	place "Rikyu"
	extends "Class_Container"
	syn "case"
}

Room
{
	name "West of House"
	describe "You are standing in an open field west of a white house, with a boarded front door."
	exit "west" to "Forest"
	exit "southeast" to "South of House"
	exit "northeast" to "North of House"
}

Room
{
	name "Country Road(4)"
	describe "A poorly maintained dirt road, leading off into darkness to the east and west. It is bordered by a steep ridge to the north, and a crumbling stone wall to the south. The trees along the road form a thick canopy overhead, lacing together like skeletal fingers to block out the faint light from the sky."
	place "Inheritance"
	theme "leaf"
	string "name" "Country Road"
	exit "west" to "Darkened Road(2)"
	exit "east" to "Country Road(3)"
}

Room
{
	name "Mansion Guest Room"
	describe "A workroom.  Describe me?"
	theme "wood"
	exit "north" to "Mansion Upper Hallway"
}

Thing
{
	name "Class_Dial"
	describe "A white box."
	place "Other Box"
	feature "divunal.common.author.DialTurn"
}

Thing
{
	name "room"
	describe "A blue box."
	place "Wrecked Street"
}

Thing
{
	name "grenade"
	describe "It is a pretty typical looking grenade.  If you don't know what that is, well too bad!"
	place "Agent Moore"
}

Thing
{
	name "gender changer instruction booklet"
	describe "A folded paper booklet, entitled \"Improving your life with the Ronco Pocket Gender Changer\". It seems to be little more than a few pages of instructions and legal notices, but would probably be very useful if you wanted to read about the functions of the Type 232 Gender Changer."
	place "science and technology demo center table"
	feature "twisted.reality.plugin.Read"
	string "read text" "    \"Thank you for your purchase of our Type 232 Ronco Pocket Gender Changer. To to the somewhat touchy nature of human sexuality, this device is not precisely calibrated; However, the simple control system makes working out your desired settings a simple game of chance. In other words, if at first you don't succeed, try, try again.\"\n\n     \"(Ronco Pocket Body Alterations, Inc. can be held in no way liable for any effects, desired or otherwise, produced by this non-UL-Listed device, or any concequences thereof.)\""
	syn "changer instruction"
	syn "changer instruction booklet"
	syn "instruction booklet"
	syn "booklet"
}

Thing
{
	name "gate(1)"
	describe "A cast-iron heavy gate which bears the inscription, \"Abandon all hope, ye who enter here.\""
	place "Castle Entrance Archway"
	component
}

Thing
{
	name "class_pistol slide"
	describe "A blue box."
	place "Tenth's Chamber"
	feature "inheritance.gun.RackSlide"
}

Thing
{
	name "khaki pants"
	describe "Though a crease runs down the front and back of each leg of these pleated chinos, the strong, supple fabric makes it plain that this piece of clothing functions equally well for both work and leisure.  The pants have two pockets on both the front and back and are the color of dark brown dust."
	place "Jedin"
	string "clothing appearance" "a pair of rugged, dust-brown chinos"
	boolean "clothing worn" true
	extends "Class_Pants"
	component
	syn "pants"
}

Room
{
	name "Summer Chamber"
	describe "This room is warm, with the scent of flowers in the air.  A bed is aligned with the west wall, a half circle, in a sort of crude line-drawing of the sun.  The ground is a soft bed of flower petals, and the walls are a muted white.  On the north wall is a large panel window overlooking a pine forest in full bloom.  "
	exit "south" to "Cylindrical Mansion Hallway"
}

Player
{
	name "Cross-platform Guest"
	describe ""
	boolean "score init" true
	int "score max" 1024
	int "score" 0
	string "adjective" "Cross-platform"
	extends "Class_Guest"
	syn "guest"
	passwd ""
}

Room
{
	name "Kitchen(1)"
	describe "You are in the kitchen of the white house. A table seems to have been used recently for the preparation of food. A passage leads to the west and a dark staircase can be seen leading upward. A dark chimney leads down and to the east is a small window which is open."
	exit "west" to "Living Room"
	exit "east" to "Behind House"
}

Room
{
	name "Bookstore Stairwell, Level 9"
	describe "This is a plain marble spiral staircase, leading both up and down. There is a door here in the southern wall that leads to this floor of the bookstore, that has the number \"9\" written on it."
	exit "up" to "Bookstore Stairwell, Level 10"
	exit "south" to "Myth Section"
	exit "down" to "Bookstore Stairwell, Level 8"
}

Room
{
	name "Bookstore Stairwell, Level 8"
	describe "This is a plain marble spiral staircase, leading both up and down. There is a door here to the northwest that leads to this floor of the bookstore, that has the number \"8\" written on it."
	exit "northwest" to "Nondescript Section"
	exit "up" to "Bookstore Stairwell, Level 9"
	exit "down" to "Bookstore Stairwell, Level 7"
}

Room
{
	name "Damien's Study"
	describe "     This is looks like a traditional (20th century, Earth-type) room in a large city apartment. The decoration is modern, and it is full of sturdy metal bookshelves.  The reference manuals are still fairly neat in rows on the shelf, but everything else has been removed.\n     There are several piles of half-read occult lore around the room, apparently someone was searching for something -- a bit frantically, too.\n     Organic stuff covers every surface, and every edge. Maybe someone was in a hurry to redecorate?\n     There is an exit to the east, and there was an exit to the north. This exit has been nailed shut, and completely sealed with about two feet of the bizarre thread."
	exit "east" to "Damien's Bedroom"
}

Room
{
	name "Bookstore Stairwell, Level 7"
	describe "This is a plain marble spiral staircase, leading both up and down. There is a door here to the southwest that leads to this floor of the bookstore, that has the number \"7\" written on it."
	exit "southwest" to "Odd Curve"
	exit "up" to "Bookstore Stairwell, Level 8"
	exit "down" to "Bookstore Stairwell, Level 6"
}

Location
{
	name "Class_Sittable"
	describe "A nice place to sit."
	place "Furniture Box"
	feature "twisted.reality.plugin.furniture.Stand"
	feature "twisted.reality.plugin.furniture.Sit"
	int "maximum occupancy" 1
	string "preposition" "on"
	string "player preposition" "sitting on"
	broadcast
}

Room
{
	name "Bookstore Stairwell, Level 6"
	describe "This is a plain marble spiral staircase, leading both up and down. There is a door here that leads northeast to this floor of the bookstore, that has the number \"6\" written on it."
	exit "northeast" to "Rare Book Room, Upper Level"
	exit "down" to "Bookstore Stairwell, Level 5"
	exit "up" to "Bookstore Stairwell, Level 7"
}

Room
{
	name "Bookstore Stairwell, Level 5"
	describe "This is a plain marble spiral staircase, leading both up and down. There is a door here that leads southeast to this floor of the bookstore, that has the number \"5\" written on it."
	exit "southeast" to "Granite Reception Room"
	exit "down" to "Bookstore Stairwell, Level 4"
	exit "up" to "Bookstore Stairwell, Level 6"
}

Room
{
	name "Bookstore Stairwell, Level 4"
	describe "This is a plain marble spiral staircase, leading only up. There is a chalk drawing of a door here that has the number \"4\" written on it.  Strangely, the stairs end in a wall here, with no purpose for their continuation this low."
	exit "up" to "Bookstore Stairwell, Level 5"
}

Room
{
	name "Bookstore Stairwell, Level 10"
	describe "This is a plain marble spiral staircase, leading both up and down. There is a door here in the north wall that leads to this floor of the bookstore, that has the number \"10\" written on it."
	exit "up" to "Bookstore Stairwell, Level 11"
	exit "north" to "Science Fiction Room"
	exit "down" to "Bookstore Stairwell, Level 9"
}

Room
{
	name "Bookstore Stairwell, Level 11"
	describe "This is a plain marble spiral staircase, leading both up and down. There is a door here to the northeast that leads to this floor of the bookstore, that has the number \"10\" written on it."
	exit "northwest" to "Empty Hallway"
	exit "down" to "Bookstore Stairwell, Level 10"
}

Room
{
	name "Antiques Room"
	describe "An Antiques Room looking as if it needs to be described."
	place "Inheritance"
	theme "dark"
	exit "south" to "Chateau Hallway(8)"
	exit "east" to "Unfinished Room"
	exit "north" to "Chateau Hallway(7)"
}

Thing
{
	name "sarcophagus hieroglyphics"
	describe "It appears to be a sarcophagus hieroglyphics, but it is vague, indistinct, and little more than a blurry smear on reality."
	place "Chateau Library(1)"
	string "egyptian hieroglyphics" "These runes seem to mean something to the effect of \"The god-accursed translation verb is finally working\"."
	component
	syn "hieroglyphics"
	syn "symbols"
	syn "runes"
	syn "glyphs"
}

Room
{
	name "Country Road(3)"
	describe "A poorly maintained dirt road, leading off into darkness to the east and west. It is bordered by a steep ridge to the north, and an old stone wall to the south. The branches of the trees along the edge of the road nearly touch overhead, covering the ground with dancing shadows and faint patches of light"
	place "Inheritance"
	theme "leaf"
	string "name" "Country Road"
	exit "west" to "Country Road(4)"
	exit "east" to "Country Road"
}

Thing
{
	name "Class_Player Creation Dial"
	describe "A white box."
	place "Other Box"
	thing "machine" "player creation machine"
	string "description" "A black dial.  Look at the machine for a clearer description..."
	float "minval" "-1.0"
	float "maxval" "1.0"
	extends "Class_Dial"
}

Thing
{
	name "demo book"
	describe "A rather nondescript demo book."
	place "great bookshelf"
	thing "linkTo" "Twisted Reality Corporate Demo Center"
	extends "Class_Linking Book"
	syn "book"
}

Location
{
	name "crate"
	describe "Several roughly shaped pieces of wood that have been nailed together in a cruel mockery of a box."
	place "Mansion Maintenance Closet"
}

Room
{
	name "Tsiale's House"
	describe "This is the entrance hall of a small wrecked house.  You can see that there is an upper floor and a few other rooms, but the staircase is collapsed, and the other rooms (and most of this one) are all caved in.  There is a wooden doorframe to the west."
	theme "crack"
	string "name" "Small Wrecked House"
	exit "west" to "Wrecked Street, bookstore"
}

Room
{
	name "God Authoring Room"
	describe "This room holds dangerous equipment. DO NOT MODIFY ANYTHING HERE UNLESS YOU KNOW EXACTLY WHAT YOU ARE DOING, IS THAT CLEAR!??!"
	exit "down" to "Science Fiction Room"
}

Location
{
	name "left front pocket"
	describe "The front left pocket of the battered black backpack."
	feature "twisted.reality.plugin.clothes.ClothingPut"
	feature "twisted.reality.plugin.OpenCloseContainer"
	component
	syn "left pocket"
	syn "pocket"
}

Thing
{
	name "foundation"
	describe "The foundation of the building looks as if it has barely survived the test of time."
	place "Wrecked Street, curve"
	component
}

Room
{
	name "Cylindrical Mansion Hallway"
	describe "This is a small octagonal room with a domed ceiling, with four large doors in the cardinal directions, and one smaller one to the southeast.  The walls here are completely white, and a soft light eminates from the ceiling."
	exit "south" to "Anah's Room"
	exit "east" to "Autumn Chamber"
	exit "west" to "Spring Chamber"
	exit "north" to "Summer Chamber"
	exit "southeast" to "Slanted Mansion Hallway"
}

Thing
{
	name "small heart shaped box"
	describe "A small, heart shaped cardboard box, covered in a swirl of reddish colors."
	place "Other New Jersey Apartment Bedroom"
	syn "box"
	syn "heart shaped box"
}

Thing
{
	name "Class_Cloak"
	describe "A white box."
	place "Clothing Box"
	string "clothing location" "chest"
	string "clothing location 2" "right arm"
	string "clothing location 3" "left arm"
	string "clothing location 4" "left leg"
	string "clothing location 5" "right leg"
	extends "Class_Clothing"
}

Location
{
	name "stone prayer bench"
	describe "Though carved out of stone, this bench seems surprisingly smooth and comfortable to sit on."
	place "Ivy Garden"
	int "maximum occupancy" 5
	extends "Class_Sittable"
	component
	syn "bench"
	broadcast
}

Room
{
	name "Airport Lounge"
	describe "This is a large lounge, with a large plush couch and several booths surrounding tables. There are several doors along the north wall - to the northwest, the textbook store, which is never open. To the north, there is the \"Community Council Office\", and to the northeast, there is an Internet office for Academic computing. Directly to the east, there is a long hallway leading to the Robert Crown Center."
	exit "east" to "Lounge Walkway"
	exit "west" to "HC Magic Board Landing"
}

Thing
{
	name "easel"
	describe "A lone, half-finished picture lies on the easel.  It looks like it could easily be finished, but the artist left it intentionally not so.  It is a picture of a book."
	place "Art Room"
}

Location
{
	name "white guymelf"
	describe "A massive suit of white armor, easily four times the height of a man. It is formed from smooth, oddly shaped sections of silvery white metal, and bears a dark red cloak from it's shoulders. A large green gem is set into either shoulder, and a single reddish stone is embedded in the left side of the chest."
	place "Mansion Laboratory"
	feature "divunal.common.vehicles.VehicleGo"
	feature "divunal.tenth.EnterGuymelf"
	feature "divunal.tenth.OpenGuymelf"
	syn "guymelf"
	syn "armor"
	syn "suit"
	broadcast
}

Location
{
	name "demo register drawer"
	describe "A grey plastic drawer, of the sort fitted into grey plastic cash registers and used to store money."
	place "Demo Center Gift Shop"
	feature "demo.DrawerOpenClose"
	feature "twisted.reality.plugin.Put"
	string "name" "cash register drawer"
	component
	syn "drawer"
	syn "cash register drawer"
	opaque
	shut
}

Room
{
	name "Plain Room"
	describe "null"
	exit "west" to "Cold Floor"
}

Location
{
	name "inflatable mattress"
	describe "A blue box."
	place "Mansion Laboratory"
	feature "twisted.reality.plugin.furniture.Lie"
	string "player preposition" "lying on"
	string "preposition" "on"
	int "maximum occupancy" 2
	component
	syn "mattress"
	syn "bed"
	broadcast
}

Thing
{
	name "pair of brass framed spectacles"
	describe "A pair of brass framed spectacles with green colored lenses, each of which is set in some sort of odd mechanism which apparently allows them to be rotated."
	place "Tenth"
	feature "divunal.tenth.SpectacleRotate"
	feature "divunal.tenth.SpectacleSet"
	string "clothing appearance" "a pair of green-tinted spectacles"
	string "name" "pair of green-tinted spectacles"
	string "color" "green"
	boolean "clothing worn" true
	string "clothing location" "left eye"
	string "clothing location 2" "right eye"
	string "clothing location 3" "right ear"
	string "clothing location 4" "left ear"
	extends "Class_Clothing"
	component
	syn "brass framed spectacles"
	syn "spectacles"
	syn "lenses"
	syn "lens"
	syn "glasses"
}

Room
{
	name "Back Lawn(9)"
	describe "You are near the back end of the mansion, by the large field of overgrown grass and weeds that forms the back yard. The rear wall of the mansion continues on for quite some way to the east, to the back door, and the lawn continues out to the north for quite a ways, where a dark, blocky shape is silhouetted against the trees."
	place "Inheritance"
	theme "leaf"
	string "name" "Back Lawn"
	exit "north" to "Back Lawn(3)"
	exit "east" to "Back Lawn"
	exit "west" to "Side Lawn(5)"
}

Room
{
	name "Country Road(2)"
	describe "A poorly maintained dirt road, leading off into darkness to the east and west. It is bordered by a steep ridge to the north, and a crumbling stone wall to the south. The trees along the road form a thick canopy overhead, blocking out even the faint light from the sky."
	place "Inheritance"
	theme "leaf"
	string "name" "Country Road"
	exit "east" to "Darkened Road"
	exit "west" to "Country Road(1)"
}

Room
{
	name "Lonely Expanse of Beach"
	describe "A stream of icy water cuts a narrow, brackish ribbon in the sand. The water tumbles over rough, black rocks and mingles with the rolling sea.   A mixture of weather-ravaged conifers and deciduous trees border the sand.\nTo the east, a lighthouse and an aged copper roof are visible above the trees tops.\n"
	exit "north" to "The Doorway of the Obsidian Tower"
	exit "east" to "Agatha's Lighthouse"
	exit "west" to "Sea Shore"
}

Location
{
	name "Food Box"
	describe "A blue box."
	place "Class Room"
	extends "Class_Container"
	syn "box"
}

Thing
{
	name "Class_Small Book"
	describe "Set the property \"book text\" to what you want the player to see when they read it."
	place "Book Box"
	feature "divunal.bookstore.TrivialRead"
	string "book text" "The book is mostly in a language you can't understand, and is very uninteresting to you."
}

Thing
{
	name "black plastic cable"
	describe "A long, thin cable, coated with a glossy black plastic."
	place "Mansion Main Hall"
	theme "wood"
	component
	syn "plastic cable"
	syn "cable"
}

Location
{
	name "clue first chair"
	describe "A rather nondescript clue first chair."
	place "Garden Maze(12)"
	string "name" "first chair"
	extends "Class_Sittable"
	component
	syn "first chair"
	syn "chair"
	broadcast
}

Thing
{
	name "TME Greenhouse Plants"
	describe "Upon closer examination, the plants, although strewn about the room with no sense of organization, are all exactly the same.  They have fairly geometric leaves and stems, as well as all being rooted in mounds of dirt which look strangely glossy and pot-shaped."
	place "Greenhouse Entrance"
	component
	syn "plants"
	syn "greenhouse plants"
}

Location
{
	name "demo center toilet"
	describe "A sleek, elegant form of lines and curves, gleaming white and perfectly symmetrical... A geometrical work of art, but also a toilet. There is no visible handle, leaving it perfectly unmarred, except for a small white placard on top of the back rest."
	place "Demo Center Bathroom Stall"
	feature "demo.ToiletStand"
	feature "twisted.reality.plugin.furniture.Sit"
	int "maximum occupancy" 1
	string "preposition" "on"
	string "player preposition" "sitting on"
	string "name" "toilet"
	component
	syn "toilet"
	broadcast
}

Player
{
	name "Guyute"
	describe "A tall and thin man, most of Guyute's appearance is shrouded. "
	gender m
	feature "divunal.magic.Cast"
	thing "oldlocation" "Underground Grotto"
	int "learned zorft" -1
	int "learned frotz" 1
	float "aura" "0.1"
	
	persistable "updatedSkills" "twisted.reality.Stack" val "string mindspeak\n" key "twisted.reality.Stack@5856c9a"
	float "mindspeak" "0.1"
	long "stamina time" 934396549868
	float "stamina" "0.0"
	long "health time" 934396549868
	float "health" "1.0"
	float "strength" "-0.2"
	float "dexterity" "0.0"
	float "agility" "0.0"
	float "endurance" "0.0"
	float "psyche" "1.0"
	float "memory" "1.0"
	
	persistable "clothing neck" "twisted.reality.Stack" val "thing dark black cloak\n" key "twisted.reality.Stack@5856e7c"
	int "learned posess" -1
	int "spells learned" 1
	descript "clothing" {Pronoun of("Guyute"), " is wearing ", Name of("dark black cloak"), "."}
	extends "Class_Human"
	ability "divunal.common.skills.ReadAura"
	ability "twisted.reality.author.FloatSet"
	ability "divunal.common.skills.MindSpeak"
	ability "divunal.rikyu.Teleport"
	ability "twisted.reality.Godhood"
	ability "twisted.reality.author.MoodSet"
	ability "divunal.magic.spells.Frotz"
	ability "divunal.magic.spells.Zorft"
	ability "divunal.rikyu.Posess"
	ability "divunal.rikyu.WhoWhere"
	architect
	passwd "Guf1Y1JBI7sZQ"
}

Room
{
	name "Silver Shadowed Flowers"
	describe "Endless fields of flowers and silverbladed grass spread out all around you.  The perfumed scent haning in the air is stronger here, making you feel slighlty dizzy.  "
	theme "leaf"
	exit "north" to "Silver Shadowed Plain"
	exit "southeast" to "Silver Shadowed Flowers"
	exit "northeast" to "Silver Shadowed Flowers"
}

Room
{
	name "Tower's Base"
	describe "This avenue goes between rows of buildings that have been completely reduced to rubble.  The road has fared better than the buildings though, it appears to be in fairly good condition, as does the tall tower standing to the south.  An open archway leads into the tower."
	theme "crack"
	string "name" "Wrecked Street"
	exit "south" to "Temple Entrance Room"
	exit "north" to "Wrecked Avenue"
}

Thing
{
	name "BummCo Toys ownership guide"
	describe "A folded piece of white paper, covered in poorly printed lettering. It reads:\n\n\"BummCo Toys Proudly Presents the \"John Romero: Master of Daikatana\" promotional semi-posable talking action figure! Just yank his crank and hear him say any one of 18 colorful phrases.\"\n\n\"WARNING: Highly Flammable. Do not immerse in liquids. Explodes Under Pressure. Not a Food. Rated Grade F (Human Inedible) by the Artifical Food Standards committee. May contain bullshit.\"\n\n\"Thank you for your purchase. BummCo Toys is a trademark and fully owned subsidiary of General Firms (tm).\""
	place "demo gift shop shelves"
	feature "twisted.reality.plugin.ReadLook"
	thing "repop" "demo gift shop shelves"
	syn "ownership guide"
	syn "guide"
}

Location
{
	name "Mummy"
	describe "A blue box."
	place "Chateau Library(1)"
}

Location
{
	name "stone workbench"
	describe "This workbench looks like it's been through the Great War. Even in the hard granite that composes its top surface there are deep gouges. The surface of the workbench is covered with clutter and refuse of every kind."
	place "Guyute's Laboratory"
	string "preposition" "on"
	extends "Class_Container"
	component
	syn "workbench"
}

Room
{
	name "Wrecked Street"
	describe "This is an intersection, which looks as if thousands of small rocks had bombarded it at high velocity, leaving pockmarks.  To the north and west, the pockmarks become larger, and the road is unwalkable within 30 or 40 steps.  To the southwest, the road is damaged but still useful.  Southward, however, the road is curiously undamaged, although buildings lie in rubble to both sides of it."
	theme "crack"
	exit "south" to "Wrecked Avenue"
	exit "southeast" to "Wrecked Street, postwall"
}

Thing
{
	name "demo center office trash"
	describe "The desk is scattered with empty bottles of Dr. Pepper, discarded Arizona Iced Tea cans, and a few crumpled paper bags. You get the impression that whoever works here probably eats most of their meals at the desk and doesn't get around to cleaning up until much later in the day, if ever."
	place "Messy New Jersey Office"
	feature "demo.DontGoThereGet"
	component
	syn "trash"
	syn "bottles"
	syn "bags"
	syn "empty bottles"
	syn "paper bags"
}

Room
{
	name "Back Lawn(8)"
	describe "You are near the back end of the mansion, by the large field of overgrown grass and weeds that forms the back yard. The rear wall of the mansion continues on for quite some way to the west, towards the back door, and the lawn continues out to the north for quite a ways, where a dark, blocky shape is silhouetted against the trees."
	place "Inheritance"
	theme "leaf"
	string "name" "Back Lawn"
	exit "east" to "Side Lawn"
	exit "west" to "Back Lawn"
	exit "north" to "Back Lawn(7)"
}

Thing
{
	name "corner"
	describe "There aren't any."
	place "Damien's Bedroom"
	component
}

Room
{
	name "Bus Stop"
	describe "You could wait here for a bus, if somebody had managed to program that yet.  Unfortunately, there are some problems with living in a half-built universe."
	exit "west" to "Bus Stop Junction"
}

Room
{
	name "Country Road(1)"
	describe "A poorly maintained dirt road, leading off into darkness to the east and west. It is bordered by a steep ridge to the north, and an old stone wall to the south. The branches of the trees along the sides of the road nearly meet overhead, throwing a patchwork of shadows over the ground."
	place "Inheritance"
	theme "leaf"
	string "name" "Country Road"
	exit "east" to "Country Road(2)"
	exit "west" to "Country Road"
}

Room
{
	name "Middle of Path"
	describe "This is the middle of a long northwest/southeast path through a lawn."
	exit "northwest" to "HC Library Slab"
	exit "southeast" to "Scenic Junction"
}

Thing
{
	name "journal"
	describe "A typical diary, in a typical journal book. It is a well made book, with a leather exterior and very nice paper inside. The only thing that speerates it from a normal day planner are the large, we-mean-business combination locks along the edge."
	place "Damien's Cubicle"
}

Location
{
	name "General Box"
	describe "A blue box."
	place "Demo"
	extends "Class_Container"
}

Room
{
	name "Silver Shadowed Clearing"
	describe "This is the side of a mountain, a small clearing in a forest.  You can see a path stretching into the forest to your east and west."
	theme "leaf"
	exit "west" to "Sylvan Sanctuary"
	exit "east" to "Silver Shadowed Glade"
}

Thing
{
	name "orange"
	describe "It appears to be a orange, but it is vague, indistinct, and little more than a blurry smear on reality."
	place "Tsiale"
	feature "divunal.common.Eat"
	string "eat text 2" " and eat it... It's a little chewy, but juicy and delicious."
	string "eat text 1" "You peel the "
}

Player
{
	name "Agatha"
	describe "Shadows settle  all around Agatha. She seems at once bathed in a soft glow and obsured in darkness, with the exclusion of a string of clear faceted stones encircling her throat. The necklace reflects a source-less light in all directions, tossing a shards of light on everything in the vicinity. She looks asleep at the moment. if you check back in a little while, perhaps she will be awake. "
	gender f
	thing "oldlocation" "Agatha's Lighthouse"
	
	persistable "clothing neck" "twisted.reality.Stack" val "thing dazzling necklace\n" key "twisted.reality.Stack@585579b"
	
	persistable "clothing chest" "twisted.reality.Stack" val "thing midnight blue cloak\n" key "twisted.reality.Stack@58558ab"
	
	persistable "clothing right foot" "twisted.reality.Stack" val "thing pair of brown leather boots\n" key "twisted.reality.Stack@585583f"
	
	persistable "clothing left foot" "twisted.reality.Stack" val "thing pair of brown leather boots\n" key "twisted.reality.Stack@5855975"
	descript "clothing" {Pronoun Of("Agatha"), " is wearing ", Name of("dazzling necklace"), ", ", Name of("midnight blue cloak"), ", ", "and ", Name of("pair of brown leather boots"), "."}
	extends "Class_Human"
	architect
	passwd "Agi6UUdFlSqAE"
}

Room
{
	name "Empty Hallway"
	describe "This is an empty north/south hallway.  There are no doors here save one in the southeastern corner, only wooden floor and white-painted walls.  The southeastern door is labeled \"11\"."
	exit "north" to "Empty Hallway North"
	exit "southeast" to "Bookstore Stairwell, Level 11"
}

Thing
{
	name "shroom"
	describe "Your vision wavers as you stare at the shroom. It has an aura of blue haze that surrounds it. The more you concentrate on it, the woozier you feel."
	place "Psychadelic Room"
	theme "weird"
	feature "divunal.dream.TakeShroom"
}

Thing
{
	name "jeweled sword"
	describe "A rather nondescript jeweled sword."
	place "Rikyu"
	syn "sword"
}

Location
{
	name "Class_Boat"
	describe "A rather non-descript Class_Boat."
	place "Underground Grotto"
	feature "divunal.rikyu.UseGondola"
	component
	broadcast
}

Thing
{
	name "pair of dark blue shorts"
	describe "A white box."
	place "James"
	boolean "clothing worn" true
	extends "Class_Pants"
	component
	syn "shorts"
	syn "blue shorts"
}

Thing
{
	name "text"
	describe "Some rather confusing comic strips, and a quote from the X-Files. It is the \"Life is like a box of chocolates\" quote from the Smoking Man episode."
	place "Mod Seven Short Hallway"
	component
}

Thing
{
	name "dark grey cape"
	describe "This is a dark grey cape."
	place "Maxwell"
	boolean "clothing worn" true
	extends "Class_Cape"
	component
	syn "cape"
}

Thing
{
	name "bouquet"
	describe "This is a boquet of white roses, delicately rimmed with blue.  In the center of the arrangement, there is one very red rose which is almost glowing.  A note is attached to the bottom of the boquet which reads, \"To Anah, who is the one part of reality I don't want to change.\"  It is unsigned."
	feature "divunal.dream.FlowerSmell"
	syn "flowers"
}

Room
{
	name "Chateau Dining Hall(1)"
	describe "A Chateau Dining Hall looking as if it needs to be described."
	place "Inheritance"
	theme "greystone"
	string "name" "Chateau Dining Hall"
	exit "north" to "Chateau Hallway(1)"
	exit "south" to "Chateau Dining Hall"
}

Room
{
	name "Mansion Entrance Hall"
	describe "An open, rectangular room with a slightly arched ceiling and a tiled floor. A large grey wooden door with a polished brass knob is set into the north wall, flanked by a coat rack and a small metal bin.  There is a nondescript wooden door on the west wall that leads to the coat room, and an archway in the rear wall leads south into a much larger room."
	theme "wood"
	exit "west" to "Mansion Coat Room"
	exit "south" to "Mansion Main Hall"
}

Room
{
	name "Crumbling Hallway"
	describe "This is a bit further into the west wing of the castle.  The hall is in a complete state of disrepair. Instead of candles high on the walls, there are candelabras here, almost low enough to reach. In fact, there is one you can reach, about waist level, on the southern wall.  The hallway continues to the east and west."
	theme "greystone"
	exit "west" to "Less Crumbling Hallway"
	exit "east" to "Crumbling Entranceway"
}

Room
{
	name "Very Narrow Rocky Ledge"
	describe "This ledge overlooks the very edge of death itself.  You can almost feel the rock giving way under your feet as you look downwards into the seemingly bottomless clouds that do not even begin until hundreds of feet away.  A ladder leans over the edge here, and you think you could climb down to a lower ledge."
	exit "down" to "Small Platform on the Rock"
	exit "east" to "Rocky Ledge, further west"
	exit "south" to "Secret Cave"
}

Location
{
	name "recycle bin"
	describe "A light green plastic bin of seemingly infinite proportions, yet still small enough to fit conveniently under a desk. It is emblazoned with a triangular pattern of arrows, and looks like just the sort of place where unwanted or innappropriate objects would be put, to be rescued by their owners, or, failing that, periodically erased."
	place "Class Room"
	feature "twisted.reality.plugin.Put"
	syn "bin"
}

Room
{
	name "Study"
	describe "A Study looking as if it needs to be described."
	place "Inheritance"
	theme "dark"
	exit "west" to "Darkened Room"
	exit "south" to "Chateau Hallway(12)"
}

Room
{
	name "Front Lawn(5)"
	describe "The edge of the mansion's unkempt lawn, where it surrenders to the yellowed remains of a cornfield to the south and the dense bordering forest to the west. The lawn continues to the east, towards the mansion's gravel drive, and north, towards the mansion itself."
	place "Inheritance"
	theme "leaf"
	string "name" "Front Lawn"
	exit "east" to "Front Lawn(4)"
	exit "north" to "Side Lawn(3)"
}

Thing
{
	name "Guyute's Cloak"
	describe "A rather nondescript Guyute's Cloak."
	extends "Class_Cloak"
}

Room
{
	name "Wrecked Street, north"
	describe "This is a nondescript cuved street, which looks as if thousands of small rocks had bombarded it at high velocity, leaving pockmarks."
	theme "crack"
	string "name" "Wrecked Street"
	exit "north" to "Wrecked Street, corner"
	exit "west" to "Crater Edge North"
	exit "south" to "Wrecked Street, bookstore"
}

Thing
{
	name "hot poker"
	describe "A white box."
	extends "hot coal"
}

Room
{
	name "Back Lawn(7)"
	describe "A Back Lawn looking as if it needs to be described. A good old game of Croquet can be had here."
	place "Inheritance"
	theme "leaf"
	string "name" "Back Lawn"
	exit "west" to "Back Lawn(1)"
	exit "south" to "Back Lawn(8)"
	exit "north" to "Back Lawn(6)"
}

Room
{
	name "HC Library Landing"
	describe "This is a landing in the lobby of a small library. The library proper is upstairs, while you can see the school store and post-office downstairs. A row of glass doors to your south lead outside."
	exit "south" to "HC Library Steps"
	exit "up" to "HC Magic Board Landing"
}

Thing
{
	name "Reality Brush"
	describe "A white box."
	place "pale blue robe's left sleeve"
	feature "twisted.reality.plugin.clothes.WearRemove"
	extends "Reality Pencil"
	syn "brush"
}

Room
{
	name "Chateau courtyard"
	describe "You are standing in front of a large grey mansion. A circular gravel drive runs past the front steps, leading south to where it passes through the middle of a huge field of yellowed corn. The lawn continues to the east and west, as does the mansion itself, towards the forest that surrounds the property."
	place "Inheritance"
	theme "leaf"
	exit "west" to "Front Lawn(3)"
	exit "east" to "Front Lawn(1)"
	exit "south" to "Circular Driveway"
	exit "north" to "Chateau Antechamber"
}

Thing
{
	name "demo center swivel chair(1)"
	describe "It appears to be a demo center swivel chair, but it is vague, indistinct, and little more than a blurry smear on reality."
	feature "twisted.reality.plugin.furniture.Stand"
	feature "twisted.reality.plugin.furniture.Sit"
	string "name" "black swivel chair"
	string "player preposition" "sitting on"
	string "preposition" "on"
	int "maximum occupancy" 1
}

Room
{
	name "Mansion West Ballroom"
	describe "This ballroom appears to be quite spacious, but it is almost entirely occupied by a massive framework of metal rods, gears, and wheels, leaving only the eastmost edge of the room accessible. Every single piece of the machinery seems to be in motion, whether spinning rapidly or clicking along in slow, measured progression, producing a soft, metallic symphony of ambient sound. A black plastic cable runs along the floor, emerging from deep within the machine and continuing out of the room through the massive archway in the east wall."
	theme "wood"
	exit "east" to "Mansion Main Hall"
}

Location
{
	name "dasdsa"
	describe "A blue box."
}

Thing
{
	name "class_bullet"
	describe "It appears to be a class_bullet, but it is vague, indistinct, and little more than a blurry smear on reality."
	place "Tenth's Chamber"
	string "bullet type" "insert bullet type/caliber here"
}

Room
{
	name "field"
	describe "null"
	exit "back" to "Intersection"
}

Room
{
	name "Uneven Floor"
	describe "This floor is covered with hundereds of small square sheets of some hard material. As the room is still pitch dark it is impossible to determine what the squares are made of, but they are stacked everywhere here. A slight breeze is blowing in a northerly direction."
	theme "greystone"
	string "name" "A Dark Place"
	string "description" "It's too dark in here to see!"
	boolean "inhibit_exits" true
	boolean "inhibit_items" true
	extends "Class_Dark Room"
	opaque
	shut
	exit "northeast" to "Cold Floor"
	claustrophobic
}

Thing
{
	name "poster"
	describe "This is a poster advertising the movie \"Poodle with a mohawk\"."
}

Thing
{
	name "clue hammer"
	describe "A rather new-looking hammer. Etched into the wooden handle are the words: \"A.M. Hammer Co.\""
	place "Garden Maze(1)"
	string "name" "hammer"
	component
	syn "hammer"
}

Thing
{
	name "large blue crayon"
	describe "It appears to be a blue crayon, but it is vague, indistinct, and little more than a blurry smear on reality."
	place "Chenai"
	extends "Reality Pencil"
	syn "blue crayon"
	syn "crayon"
}

Room
{
	name "Twisty Cloud Path"
	describe "You are walking on a twisty path made of smooth rock, floating upon a sea of clouds.  There is a twist in it here as it curves gracefully around."
	exit "southeast" to "Path in the Clouds"
	exit "west" to "Flat Ledge"
}

Thing
{
	name "cushioned chair"
	describe "A rather nondescript cushioned chair."
	place "Furniture Box"
	extends "Class_Sittable"
}

Room
{
	name "Front Lawn(4)"
	describe "The unkempt lawn of the mansion stops just to the south, where the dried yellow ruin of the cornfield begins. The knee high grass continues west, towards the forest surrounding the property, and north, towards the mansion itself. A curved gravel drive passes by to the east, following an arc that leads up to the mansion's front steps."
	place "Inheritance"
	theme "leaf"
	string "name" "Front Lawn"
	exit "east" to "Circular Driveway"
	exit "west" to "Front Lawn(5)"
	exit "north" to "Front Lawn(3)"
}

Room
{
	name "Gravel Driveway(2)"
	describe "A long gravel driveway, surrounded by yellowed cornfields on either side. To the south, it leads uphill towards the forest at the edge of the property, and to the north, it runs downhill towards the dark shape of a house silhoutted against the horizon."
	place "Inheritance"
	theme "leaf"
	string "name" "Gravel Driveway"
	exit "south" to "Driveway"
	exit "north" to "Gravel Driveway(1)"
}

Room
{
	name "Gravel Driveway(1)"
	describe "A long gravel driveway surrounded by cornfields. It leads upwards to the south, towards where the fields give way to a vast expanse of forest, and downwards to the north, towards a dark, weathered old mansion."
	place "Inheritance"
	theme "leaf"
	string "name" "Gravel Driveway"
	exit "south" to "Gravel Driveway(2)"
	exit "north" to "Gravel Driveway"
}

Room
{
	name "The Beginning"
	describe "Hello, and welcome to the first universe constructed with Reality Pencil v0.99. We try hard to keep the universe in good working order here, so: if anything seems out of place to you, please make a note of it to a Human or send some email to reality@tinaa.com."
	exit "down" to "Obscure Corner of Bookstore"
}

Room
{
	name "RCC Rec Area West"
	describe "This is a recreation area with a bunch of table gaming equipment such as air-hockey and pool.  Nothing much seems interesting here as all of the equipment looks mostly broken.  This area continues on for a while to the east and there is a snackbar to the south as well as some stairs going down. This place overlooks a middle-sized gym with a climbing wall."
	exit "down" to "RCC Reception Desk"
	exit "east" to "RCC Rec Area East"
	exit "south" to "Robert Crown Center Cafe"
}

Room
{
	name "Demo Information Center"
	describe "A large, circular room, with immaculately white walls and a polished, black marble floor. A large black obsidian obelisk stands in the center of the room, emblazoned with a brightly colored map. The room becomes more of a hallway as it continues off to the south."
	place "Demo"
	theme "default"
	exit "west" to "Demo Center West Wing Lobby"
	exit "east" to "Demo Center East Wing"
	exit "south" to "Twisted Reality Corporate Demo Center"
}

Room
{
	name "Doorway Room"
	describe "This room seems entirely dedicated to a door in the north wall. The entire north wall is decorated with rays extending from the ceiling, floor, and two other walls to the door at the center.  There are no other decorations here. To the south there is a much smaller door."
	exit "north" to "very small round room"
	exit "south" to "Small Arched Tunnel"
}

Room
{
	name "Back Lawn(6)"
	describe "A Back Lawn looking as if it needs to be described."
	place "Inheritance"
	theme "leaf"
	string "name" "Back Lawn"
	exit "south" to "Back Lawn(7)"
	exit "west" to "Back Lawn(5)"
}

Room
{
	name "West End"
	describe "This is the westmost point on the castle.  The room seems useless except to indicate that the place ends here.  To the west, there are a set of french doors, long since shattered, leading onto a terrace.  Eastward there is a large archway."
	theme "greystone"
	exit "west" to "Cloud Scene Balcony"
	exit "east" to "Great Dome"
}

Thing
{
	name "class_translator book"
	describe "It appears to be a class_translator book, but it is vague, indistinct, and little more than a blurry smear on reality."
	place "Book Box"
	feature "inheritance.Translate"
	extends "class_simple book"
}

Thing
{
	name "dirty-looking book"
	describe "A broken binding and a cracked leather cover are the defining characteristics of this ancient book.  The title and author have long since been obscured.  Although the cover is in atrocious condition, the pages themselves seem curiously well preserved."
	place "Natural Alcove"
	thing "linkTo" "Chateau courtyard"
	extends "Class_Linking Book"
	syn "dirty book"
	syn "book"
}

Thing
{
	name "brass pocketwatch"
	describe ""
	place "Tenth"
	feature "divunal.tenth.WatchDraw"
	feature "divunal.tenth.WatchErase"
	
	property "description" "divunal.tenth.WatchDisplay"
	string "base description" "A large, well-polished brass pocketwatch, fitted with a number of extra dials, buttons and controls, and attached to a thin metal chain."
	extends "Reality Pencil"
	syn "watch"
	syn "pocketwatch"
}

Thing
{
	name "note"
	describe "This is a yellow sticky note.  It reads,\"Tenth: you might want to hide one of your vacuum tubes in here.\""
	place "Supply Closet"
}

Thing
{
	name "Mansion Bedroom Mirror"
	describe ""
	place "Tenth's Chamber"
	string "name" "ovular mirror"
	string "base description" "A large, ovular mirror, set in a polished wooden frame. Reflected in the mirror is:\n     "
	
	property "description" "divunal.tenth.MirrorDesc"
	component
	syn "large mirror"
	syn "mirror"
}

Thing
{
	name "hot coal"
	describe "This is a piece of hot coal, about half the size of your palm."
	syn "coal"
}

Thing
{
	name "class_hat"
	describe "A blue box."
	place "Clothing Box"
	string "clothing location" "crown"
	boolean "clothing worn" false
	extends "Class_Clothing"
}

Room
{
	name "Cloud Scene Balcony"
	describe "You are standing on a semicircular slab of marble, with steps leading outward in all directions... into a layer of clouds! The castle looms high above you, but all you can see into the distance is an unbroken layer of clouds and the moon.  Within a few steps, the stairs in all directions are completely obscured by clouds.  "
	theme "water"
	float "cloudiness" "0.08391655"
	thing "fling place" "Moonlit Beach"
	handler "startup" "divunal.dream.FlingHandler"
	descript "cloudd" "The clouds are as tranquil as a lake on a cool summer's night."
	exit "east" to "West End"
}

Room
{
	name "HC Library Slab"
	describe "You are standing on a large concrete slab in front of what appears to be a library. There are steps to your west and nearby to the east is a large sport center.  Eastward is a bus stop and to your southeast there is a path cutting through the lawn. A large sign says DO NOT STEP ON THE LAWN which is to your south."
	exit "southeast" to "Middle of Path"
	exit "east" to "Bus Stop Junction"
	exit "west" to "HC Library Steps"
	exit "north" to "Under Walkway"
}

Room
{
	name "Silver Room"
	describe "This room is a study in silver.  While you can make out no light source, light must be filtering in through the silvered, translucent ceiling to get down here, where it shines off of the curved surfaces of the room's walls and floor.  There are no markings anywhere, and the only real feature of the room is a cube, which appears to be part of the floor, made of the same silvery substance that composes the rest of the room, but glittering more brightly."
	exit "west" to "Jewel Bedecked Hallway 2"
}

Room
{
	name "Field(1)"
	describe "null"
	exit "southeast" to "Intersection"
}

Thing
{
	name "demo center computer equipment"
	describe "Various and sundry items, including a set of headphones, a cheap plastic General Electric telephone, several Linux Manuals, an extra Universal Mac Monitor Plug Adapter, several outdated RedHat Linux install CDs, and a lot of other fairly uninteresting and useless items."
	place "Messy New Jersey Office"
	component
	syn "equipment"
	syn "computer equipment"
}

Room
{
	name "Front Lawn(3)"
	describe "You are in front of the west wing of a darkened old mansion. It continues to the west, almost touching the dense forest that lines the property, and to the east, towards the gravel driveway leading to the front door. The unkempt grass of the front lawn continues to the south before giving way to a vast field of yellowed corn."
	place "Inheritance"
	theme "leaf"
	string "name" "Front Lawn"
	exit "west" to "Side Lawn(3)"
	exit "south" to "Front Lawn(4)"
	exit "east" to "Chateau courtyard"
}

Room
{
	name "Guest Chamber"
	describe "A small, comfortable guest room."
	exit "east" to "Observation Hallway"
}

Room
{
	name "Mansion Basement Pump Area"
	describe "A small area, mostly walled off from the western half of the room by a large brass and metal machine. A large circular well has been dug into the dirt floor, and a small pump is suspended over it on stone blocks."
	theme "greystone"
	descript "pump sound" " A rhythmic, almost mechanical humming sound echoes throughout the room."
	exit "down" notTo "Mansion Basement Well" with "Mansion Basement Pump"
	exit "west" to "Mansion Basement Engine Room"
}

Thing
{
	name "brass cockroach"
	describe "A small mechanical cockroach, intricately designed with all of the parts and details of a real insect, made entirely of polished brass. There is a small hexagonal keyhole between two of the plates of its thorax."
	mood "lying on its back"
	place "Greenhouse Entrance"
	thing "repop" "Greenhouse Entrance"
	boolean "windable" true
	int "winds" 0
	handler "roachmove" "demo.RoachMove"
	handler "startup" "demo.RoachMove"
	syn "cockroach"
	syn "roach"
}

Thing
{
	name "midnight blue cloak"
	describe "A rather nondescript midnight blue cloak."
	place "Agatha"
	string "name" "cloak"
	boolean "clothing worn" true
	extends "Class_Cloak"
	component
	syn "agatha's cloak"
}

Thing
{
	name "brown Expedition boots"
	describe "Despite the obviously thick sides and soles, the hide's soft texture gives these boots a comfortable appearance."
	place "Jedin"
	boolean "clothing worn" true
	string "clothing appearance" "a pair of all-purpose brown leather boots"
	extends "Class_Shoes"
	component
	syn "leather boots"
	syn "boots"
}

Thing
{
	name "Blue Charting Pencil"
	describe "A rather nondescript Blue Charting Pencil."
	place "Agatha"
	extends "Reality Pencil"
}

Thing
{
	name "tsukubai"
	describe "This stone basin, or tsukubai, is continuously filled by some hidden pump. The water is clear and cold, suitable for drinking, though the designs indicate some holier purpose as well."
	place "Inner Garden"
	feature "divunal.rikyu.TeaHouseDrink"
	feature "divunal.rikyu.TeaHouseWash"
	string "name" "stone basin"
	component
	syn "stone basin"
	syn "basin"
}

Room
{
	name "Back Lawn(5)"
	describe "A Back Lawn looking as if it needs to be described."
	place "Inheritance"
	theme "leaf"
	string "name" "Back Lawn"
	exit "south" to "Old Wooden Shed"
	exit "east" to "Back Lawn(6)"
	exit "north" to "Wooded Grove"
	exit "west" to "Back lawn(4)"
}

Room
{
	name "Pathway"
	describe "This asphalt pathway leads from one mod to another. It continues to the east, and it leads up to a door to the west. To the south there is a break in the line of trees, and there is a large lawn to the north."
	exit "north" to "Mod Lawn"
	exit "south" to "Outside the Mods"
}

Thing
{
	name "colorful book"
	describe "This is a colorful book with an outrageous pattern on it that looks reminiscent of a cloudy day, except the clouds are all rainbows and the sky is a bizarre gradient.  The title is in large black block letters on the front: \"Dropping Acid with Doctor Seuss\""
	place "Small Book Room"
	extends "Class_Small Book"
	syn "book"
}

Thing
{
	name "northern tapestry"
	describe "This tapestry depicts a disasterous scene, with people and other creatures running in vain. It appears that some sort of meteor shower is occurring; at least, large, flaming rocks are flying down out of the sky."
	place "Guyute's Bedroom"
	feature "divunal.rikyu.TapestryMove"
	string "obstructed message" "You can't go that way"
	string "exit message" "You go north through the hidden doorway."
	boolean "obstructed" false
	descript "tapestry moved" " The northern tapestry has been moved to show a small doorway."
	extends "Class_Door"
	component
	syn "tapestry"
	syn "north"
}

Thing
{
	name "clip release switch"
	describe "It appears to be a clip release switch, but it is vague, indistinct, and little more than a blurry smear on reality."
	place "Colt 1911 Semi-Auto"
	feature "inheritance.gun.ReleasePress"
	component
	syn "release switch"
	syn "switch"
}

Thing
{
	name "John Romero action figure"
	describe "The semi-posable plastic figure of a chunky little man with long black hair tied back in a ponytail. He is wearing a tiny Ion Storm t-shirt, and there is a length of string protruding from his back, ending in a small plastic ring."
	place "demo gift shop shelves"
	feature "demo.DollPull"
	thing "repop" "demo gift shop shelves"
	syn "action figure"
	syn "figure"
	syn "john"
	syn "romero"
	syn "ring"
	syn "string"
}

Room
{
	name "Crumbling Entranceway"
	describe "This is an old and decrepit hallway. There are stairs here, covered at the top in sand, at the bottom in dust. Candles are mounted high on the walls, providing a feeble yellow light. There is an arched iron sign hanging down from the high ceiling here, reading \"Welcome to the West Wing\". Rust almost obscures the last word."
	theme "greystone"
	exit "west" to "Crumbling Hallway"
	exit "up" to "Castle Beach"
}

Room
{
	name "New Jersey Apartment Kitchen"
	describe "The ugly pinkish shag carpeting of the floor gives way to white plastic tiles along the northern half of the room, where a small kitchen area is formed by a wall of old wooden cabinets, a sink, an ancient looking gas stove, and a refrigerator, all an almost identical shade of brown. A rickety looking table and two folding chairs sit on the kitchen floor, below a telephone attached precariously to the wall. There are windows over the sink and in the opposite wall, but each only provides a view of the walls of other nearby buildings. A combination ceiling fan and light fixture is buzzing away overhead, in contrast to the low, echoing burbles from the air conditioner.\n"
	theme "default"
	exit "east" to "New Jersey Apartment Hallway"
	exit "west" to "New Jersey Apartment Living Room"
}

Thing
{
	name "pair of grey jeans"
	describe "A white box."
	place "Maxwell"
	boolean "clothing worn" true
	extends "Class_Pants"
	component
	syn "jeans"
	syn "slacks"
	syn "pants"
}

Thing
{
	name "flower(1)"
	describe "A delicate rose of velvety purple petals, and delicately jutting leaves.  There are dewdrops from the night myst alight its soft petals as if it were just picked one morning. A soft, subtle scent of perfume from its owner perpetually lingers about it, suffusing your senses with its delicate scent..."
}

Room
{
	name "Main Aisle, Center"
	describe "This is the main aisle of the floor of a bookstore. There are three aisles branching from it, spaced at regular intervals along the floor - the aisles are almost separate rooms because the bookshelves touch the ceilings and the floors and there is a wide separation between one aisle and the next because the shelves are so deep.  You are standing at the front of the second sub-aisle, at the middle of the main one. A plaque on the floor here reads \"52.6-100, Important Financial Books\". You can continue northward to into the Financial aisle, or east to another section."
	theme "paper"
	exit "east" to "Main Aisle, East End"
	exit "north" to "Aisle 2."
	exit "west" to "Main Aisle, West End"
}

Thing
{
	name "grey cotton shirt"
	describe "A very plain, neatly pressed, grey cotton shirt."
	place "Maxwell"
	boolean "clothing worn" true
	extends "Class_Shirt"
	component
	syn "shirt"
	syn "grey shirt"
}

Thing
{
	name "strange device"
	describe "It appears to be a generic reality altering device, but aside from being vaguely pencil-shaped, it is vague and indistinct."
	place "Aaron"
	extends "Reality Pencil"
	syn "device"
}

Room
{
	name "Demo Center Waiting Room"
	describe "This is a comfortable waiting room with high-backed leather chairs and wooden-paneled walls. There is a solid oak coffee table here, with a tasteful gold inlay.  To the northeast, there is a gold-lined archway leading into a room with white walls and a black floor."
	place "Demo"
	theme "wood"
	exit "northeast" to "Demo Center West Wing"
}

Thing
{
	name "laptop"
	describe "They say that you can tell how powerful a laptop is by how big it isn't. A large, heavy machine isn't likely to be very fast, or very exspensive. If that is a good standard, then this must be a fast mahcine indeed because if you were to turn it sideways it would almost disappear. Currently there is a screensaver running. It repeats the words:\n\n   \"Damien Jones,  CPA -- Tax Law and Import Export Residuals\""
	place "Maxwell"
	feature "divunal.damien.LaptopRead"
}

Thing
{
	name "shiny clasp for left front pocket"
	describe "A shiny clasp for the left front pocket."
	component
	syn "left clasp"
	syn "clasp"
}

Location
{
	name "plastic swivel chair"
	describe "It appears to be a ergonomic swivel chair, but it is vague, indistinct, and little more than a blurry smear on reality."
	place "Genetic Laboratory"
	syn "swivel chair"
	syn "chair"
}

Room
{
	name "Nondescript Section"
	describe "This is a rather nondescript area."
	theme "paper"
	exit "southeast" to "Bookstore Stairwell, Level 8"
}

Location
{
	name "nightstand"
	describe "This nightstand is made of mahogany. It has a small drawer in the front, upon which is a small brass handle."
	place "Guyute's Bedroom"
	extends "Class_Closeable Container"
	component
	opaque
	shut
}

Thing
{
	name "egyptology manual"
	describe "A large and extremely thick leather bound book, entitled \"A Practical Guide to Egyptian Hieroglyphs, by Lord Rutherford P. Beaucavage, Esquire\". While one of the more massive and unwieldy books you've ever had tthe misfortune to encounter, it appears to be nothing if not comprehensive."
	place "Maxwell"
	string "translates" "egyptian hieroglyphics"
	string "read text" "The manual's innumerable pages are covered in illustrations and notes regarding the strange symbolic language of the egyptians. While some of the illustrations are interesting, this book makes for fairly dry and uninteresting reading, although it would probably be very useful in an attempt to translate hieroglyphics."
	extends "class_translator book"
	syn "egyptology"
	syn "manual"
	syn "book"
}

Room
{
	name "Clearing in Small Forest"
	describe "This is a clearing in a small forest.  You can see high, rocky cliffs in the distance to the north and south, and a castle with a crumbled wall to the east.  The trees seem to thin on a path to the west."
	theme "leaf"
	exit "east" to "Between the Rubble"
	exit "south" to "Southern End of Small Forest"
	exit "north" to "Northern End of Small Forest"
	exit "west" to "Castle Beach"
}

Room
{
	name "Front Lawn(2)"
	describe "The knee high lawn of the mansion trails off a bit to the south, where the yellow husks of the cornfield begin. The lawn continues to the east, towards the forest surrounding the property, and north, towards the mansion itself. The mansion's  gravel drive is just to the west, leading up to the front steps."
	place "Inheritance"
	theme "leaf"
	string "name" "Front Lawn"
	exit "west" to "Circular Driveway"
	exit "east" to "Front Lawn"
	exit "north" to "Front Lawn(1)"
}

Room
{
	name "Art Gallery"
	describe "This is an interesting art gallery. There is a painting on the north wall of a mansion toppled on its front door, with its roof pointing towards the viewer, and to the west there is a hole in the wall framed as if it were a picture. Through the hole you can see a winding rock path sloping up over a field of clouds to an architecturally impossible castle. There is a metal spiral staircase downward."
	theme "paper"
	exit "west" to "Portrait in the Sky"
}

Thing
{
	name "Mansion Steam Engine"
	describe "A large, blocky, metal and brass contraption, with a number of strange attachments. Several hoses and pipes lead out through the wall, floor, and ceiling, and it is also connected to the nearby pressure tank in a number of places. A large brass lever with a red handle is set into the side of the engine, labeled \"DANGER: RELEASE VALVE\"."
	place "Mansion Basement Engine Room"
	int "steam pressure" 500
	thing "pump source" "Mansion Basement Pump"
	string "magic" "More Magic"
	handler "startup" "divunal.tenth.SteamEngineEvent"
	handler "SteamEngineEvent" "divunal.tenth.SteamEngineEvent"
	descript "steam descriptor" " A circular, glass covered gauge protrudes from the front of the engine, its needle hovering near the 500 PSI mark."
	descript "magic descriptor" " There is a rather ominous looking throw-switch labeled \"Magic\" and \"More Magic\" attached to the base of the engine, currently set to the \"More Magic\" position."
	component
	syn "steam engine"
	syn "engine"
	syn "dials"
	syn "controls"
}

Room
{
	name "Wrecked Alleyway"
	describe "This is the end of an alley.  You can enter a building to the southeast, where a wooden doorframe leads into a building, or you can continue north out to the street."
	theme "crack"
	exit "north" to "Wrecked Street, postwall"
	exit "southeast" to "Empty Bakery"
}

Thing
{
	name "tenths folding balcony doors"
	describe "A set of folding double doors made of dark, polished wood, set with simple wooden handles."
	place "Tenth's Chamber"
	boolean "obstructed" false
	string "openDesc" "A light breeze wafts in from the north, where a pair of folding double doors lead out onto a balcony."
	string "name" "folding balcony doors"
	string "closeDesc" "To the north, a pair of folding doors are set into the wall."
	extends "Class_Door"
	component
	syn "doors"
	syn "folding doors"
	syn "north door"
	syn "north doors"
	syn "south door"
	syn "south doors"
	syn "south"
	syn "door"
}

Thing
{
	name "class_robe"
	describe "A rather nondescript class_robe."
	place "Clothing Box"
	string "clothing location" "chest"
	string "clothing location 2" "right arm"
	string "clothing location 3" "left arm"
	string "clothing location 4" "waist"
	string "clothing location 5" "left leg"
	string "clothing location 6" "right leg"
	extends "Class_Clothing"
}

Room
{
	name "Mansion East Ballroom"
	describe "A massive ballroom, empty and silent. A single candle is flickering in the giant crystal chandelier hanging over the room, casting an uneven, wavering glow over the polished floor and pale, greyish walls. A huge pair of archways are set into the east and west walls, leading into smaller and more brightly lit areas."
	theme "wood"
	exit "east" to "Mansion Grand Stair Landing"
	exit "west" to "Mansion Main Hall"
}

Room
{
	name "Back lawn(4)"
	describe "A Back lawn looking as if it needs to be described."
	place "Inheritance"
	theme "leaf"
	string "name" "Back Lawn"
	exit "east" to "Back Lawn(5)"
	exit "south" to "Back Lawn(3)"
}

Room
{
	name "End of Catwalk"
	describe "This is a wire mesh catwalk overlooking a huge factory assembly from high above.  From this height, it would be impossible to discern what it is that was produced below.  There is a hole punched in the catwalk to the north, and it looks unsafe to tread further on.  There is a door to your east leading away from the factory floor.  The door is labeled with some strange letters that you don't understand."
	exit "east" to "Metal Tube"
	exit "south" to "Catwalk"
}

Thing
{
	name "class_pistol clip release"
	describe "It appears to be a class_pistol clip release, but it is vague, indistinct, and little more than a blurry smear on reality."
	place "Tenth's Chamber"
	feature "inheritance.gun.ReleaseClip"
}

Player
{
	name "Class_Guest"
	describe "A dummy class for guests."
	place "Demo"
	thing "default repop" "Demo Information Center"
	string "gender pronoun" "person"
	
	property "description" "demo.GuestDescription"
	handler "logout" "demo.GuestLogout"
	extends "Class_Player"
	passwd "null"
}

Room
{
	name "Chasm Bottom"
	describe "This chasm is very irregular.  The floor is not level here, or even regularly sloping.  You struggle for you balance as you notice that the floor seems to ameliorate slightly to the east."
	exit "east" to "Continued Chasm"
	exit "up" to "More Office Hallway"
}

Room
{
	name "Side Lawn(5)"
	describe "You are near the back side of the mansion, where an unkempt field of weeds and tall grass that was once the back lawn extends outwards to the east. Further north, towards the back of the yard, you can make out the shape of a small building against the trees, and there is a narrow path leading south between the western wall of the mansion and the forest that has grown up against it. "
	place "Inheritance"
	theme "leaf"
	string "name" "Side Lawn"
	exit "east" to "Back Lawn(9)"
	exit "south" to "Side Lawn(4)"
}

Player
{
	name "guest"
	describe "A blue box."
	place "Demo"
	int "guest number" 8
	thing "guest start" "Twisted Reality Corporate Demo Center"
	thing "playerclass" "Class_Guest"
	handler "login" "demo.GuestLogin"
	passwd "guVeRgi5kAY4k"
}

Thing
{
	name "old wooden doorframe"
	describe "An old, weathered looking door made of dark greyish wood, mounted in a doorframe of the same material. A brass knob is set into the door at waist level, worn and dented in a few places but still appearing to have been polished recently."
	place "Mansion Entrance Hall"
	feature "divunal.tenth.OldWoodenDoorEnter"
	thing "target door" "old wooden door"
	component
	syn "wooden doorframe"
	syn "wooden door"
	syn "doorframe"
	syn "door"
	syn "knob"
	syn "brass knob"
	syn "doorknob"
}

Thing
{
	name "a pair of black slacks"
	describe "A creased, loose fitting pair of black pants."
	place "Tenth"
	boolean "clothing worn" true
	string "clothing appearance" "black slacks"
	extends "Class_Pants"
	component
	syn "slacks"
}

Room
{
	name "Chateau Lavatory"
	describe "A Chateau Lavatory looking as if it needs to be described."
	place "Inheritance"
	theme "greystone"
	exit "east" to "Chateau Hallway(3)"
}

Room
{
	name "Upper Mansion Stairwell"
	describe "A tall, cylindrical room, with a wrought iron spiral staircase descending down through the center of the floor. The domed ceiling is built from triangular panes of tinted glass set in a metal frame, and the sunlight filtering through it provides a gentle illumination to the room."
	theme "wood"
	exit "down" to "Mansion Stairwell"
}

Room
{
	name "Temple Middle Floor"
	describe "This is a large cylindrical chamber supported at eight points by pilliars.  In the center of the room, a wide octagonal octagonal stairway leads both up and down.  Wooden doorframes adorn the four cardinal directions of the room, leading off into hallways.  The floor is made of a light stone here, except for four black, glossy squares in front of each doorway."
	theme "default"
	string "name" "Middle Floor"
	exit "up" to "Temple Triangle Room"
	exit "east" to "Temple Middle Hallway East"
	exit "south" to "Temple Middle Hallway South"
	exit "west" to "Temple Middle Hallway West"
	exit "north" to "Temple Middle Hallway North"
	exit "down" to "Temple Bottom Floor"
}

Room
{
	name "Front Lawn(1)"
	describe "You are in front of the east wing of a weathered old mansion. It continues to the east, almost touching the dense forest that lines the property, and to the west, towards the gravel driveway leading to the front door. The unkempt grass of the front lawn continues on to the south before giving way to a vast field of yellowed corn."
	place "Inheritance"
	theme "leaf"
	string "name" "Front Lawn"
	exit "west" to "Chateau courtyard"
	exit "south" to "Front Lawn(2)"
	exit "east" to "Side Lawn(2)"
}

Room
{
	name "Front Step of Darkness"
	describe "You stand upon the front stoop of a mansion perched upon an infinite void.  There is no ground except where you are standing, no light except that coming from the door behind you.  You can only go back into the house to the south."
	theme "paper"
	exit "south" to "Hallway"
}

Room
{
	name "Chateau Library"
	describe "A Chateau Library looking as if it needs to be described."
	place "Inheritance"
	theme "greystone"
	exit "east" to "Chateau Library(1)"
	exit "west" to "Chateau Hallway(13)"
}

Room
{
	name "New Jersey Apartment Bedroom"
	describe "A long, rectangular room, with a dark brownish carpet, and windows set into the corners of the north and east walls. The floor is dotted with clothes, books, and software instruction manuals, forming somewhat of a trail between a bare matress, a pile of sheets, and the closet set into the west wall.\n"
	theme "default"
	exit "southwest" to "New Jersey Apartment Hallway"
}

Room
{
	name "Mansion Staging Room"
	describe "A wide, open room, with a polished wooden floor and plain white plaster walls. In the center of the room, a large pyramidal arrangement of steps leads up to a circular platform. Three identical, brass-cased cylindrical machines stand against the east, south, and west walls, connected to the base of the stairs by thick black cables."
	theme "wood"
	exit "north" to "Mansion Upper Hall"
}

Room
{
	name "Mansion Upper Hall"
	describe "A long, wide hallway, ending in arched doorways to the east and west. A dark green carpet runs the entire length of the floor, woven with a complex pattern of intersecting curves.  A pair of doorways are set into the side walls, leading north and south, respectively."
	theme "wood"
	thing "attic staircase" "attic staircase"
	descript "attic door state" "A small wooden ring is hanging from the center of the ceiling by a piece of string."
	exit "south" to "Mansion Staging Room"
	exit "up" notTo "Mansion Attic" with "attic staircase"
	exit "north" to "Mansion Laboratory"
	exit "west" to "Mansion Stairwell"
	exit "east" to "Mansion Grand Stair Balcony"
}

Room
{
	name "Mystic Field"
	describe ""
	theme "leaf"
	exit "south" to "Garden Maze(14)"
}

Room
{
	name "Back Lawn(3)"
	describe "A Back Lawn looking as if it needs to be described."
	place "Inheritance"
	theme "leaf"
	string "name" "Back Lawn"
	exit "south" to "Back Lawn(9)"
	exit "north" to "Back lawn(4)"
	exit "east" to "Back Lawn(1)"
}

Room
{
	name "A Dark Narrow Passage"
	describe "A dark narrow passageway stretches before you.  The walls are covered with the strange jelly material you glimpsed earlier, and clumps of it are lying on the floor. The air is surprisingly clear, having a sweet taste to it.  Standing very still, you can feel a slight breeze of warm air carrying a strange perfume."
	theme "greystone"
	boolean "inhibit_exits" true
	boolean "inhibit_items" true
	string "description" "It's too dark in here to see!"
	string "name" "A Dark Place"
	extends "Class_Dark Room"
	opaque
	shut
	exit "south" to "A Small Opening"
	exit "north" to "A Small Dark Crevice"
	claustrophobic
}

Thing
{
	name "coffee mug"
	describe "A slightly cracked white mug with the legend, \"Rx-2500--Simple, Fast and Easy\" across on side in bold, black letters. There is a dark brown coffee stain inside."
	place "Proper English Library"
	syn "mug"
}

Room
{
	name "Mansion Doorstep"
	describe "You are standing on the southern doorstep of a large, stately mansion which is remarkably in contrast to the vast expanse of pine trees that surround it.  It appears completely undamaged by the decay and destruction that are evident to the sides of the forest."
	theme "leaf"
	exit "north" to "Mansion Foyer"
	exit "east" to "Pine Grove"
}

Room
{
	name "Darkness"
	describe "It's too dark in here to see anything."
	theme "paper"
	boolean "inhibit_items" true
	boolean "inhibit_exits" true
	string "description" "It's too dark in here to see!"
	string "name" "A Dark Place"
	extends "Class_Dark Room"
	opaque
	shut
	exit "west" to "Cold Floor"
	exit "east" to "Precarious Ledge"
	claustrophobic
}

Thing
{
	name "ancient tome"
	describe "A small black book, covered in a sort of fake-leather. A loop on the side looks like it might hold a pen of some sort."
	place "Rikyu"
	feature "divunal.rikyu.Posess"
	feature "divunal.magic.spells.Frotz"
	feature "divunal.magic.spells.Zorft"
	string "spell 2" "posess"
	string "spell 1" "zorft"
	string "spell 0" "frotz"
	extends "Class_Spell Book"
	syn "tome"
	syn "spellbook"
}

Room
{
	name "The Twisty Bit"
	describe "The library becomes more narrow here;  the bookshelves are getting closer together, pressing in on both sides. It also seems to be twisting around, almost doubling back on itself."
	theme "paper"
	exit "north" to "Musty Section"
	exit "northeast" to "Myth Section"
}

Thing
{
	name "Indistinct Pencil"
	describe "This is a cloudy, vague reference to a pencil. It can definitely be used for writing - but it seems rather insubstantial and you can't quite place its color. One moment it seems silver, then grey, then purple, and and then blue."
	extends "Reality Pencil"
	syn "pencil"
}

Room
{
	name "Temple Entrance Room"
	describe "This is a large, light stone room.  A statue of a tall, strong looking man adorns the northwestern corner of the room, facing diagonally inward, as if to monitor those who enter from the north without being seen itself.  Another, smaller archway leads south, into the center of the tower's base."
	theme "default"
	string "name" "Entrance Room"
	exit "south" to "Temple Northern Hallway"
	exit "north" to "Tower's Base"
}

Room
{
	name "Side Lawn(4)"
	describe "A narrow path between the dense trees and brush of the forest and the peeling grey wood of the mansion's western wall. It continues south to the front lawn, and meanders along into a similar clearing to the north."
	place "Inheritance"
	theme "leaf"
	string "name" "Side Lawn"
	exit "north" to "Side Lawn(5)"
	exit "south" to "Side Lawn(3)"
}

Thing
{
	name "stick"
	describe "A white stick of birch.  "
}

Room
{
	name "Ruby Room"
	describe "This room is a study in red.  While you can make out no light source, light must be filtering in through the ruby ceiling to get down here, where it reflects off of the myriad facets of the room's walls and floor.  There are no markings anywhere, and the only real feature of the room is a cube, which appears to be part of the floor, made of the same ruby substance that composes the rest of the room, but glittering more brightly."
	exit "east" to "Jewel Bedecked Hallway"
}

Thing
{
	name "coat rack"
	describe "A rather intimidating six foot high wrought iron structure, balanced on four pointed legs and bearing a number of less dangerous looking metal arms."
	place "Mansion Entrance Hall"
	theme "wood"
	component
	syn "rack"
}

