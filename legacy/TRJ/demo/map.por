Room
{
	name "Demo"
	describe "A funny box."
}

Room
{
	name "Demo Center Lavatory"
	describe "A square, more modestly sized room lined entirely in light grey tiles. A black plastic wastebasket stands against the south wall, opposite a small white sink and the much larger mirror hanging above it."
	place "Demo"
	descript "demo center bathroom stall door openDesc" "To the east, the door to the single bathroom stall stands open."
	exit "east" to "Demo Center Bathroom Stall" with "demo center bathroom stall door"
	exit "west" to "Demo Center East Wing" with "demo center bathroom door"
}

Thing
{
	name "demo center bathroom door"
	describe "A blue metal door, designed to be pushed open easily from either side. It is labeled \"Players\" just above the icon of a gender-neutral stick figure."
	place "Demo Center East Wing"
	feature "twisted.reality.plugin.door.OpenCloseSwingingDoor"
	feature "twisted.reality.author.Obstruct"
	string "name" "blue swinging door"
	component
	syn "door"
	syn "swinging door"
	syn "blue door"
	syn "blue swinging door"
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
	syn "knob right"
	syn "knob left"
	syn "knob"
	syn "small white sink"
	syn "white sink"
	syn "sink"
}

Thing
{
	name "demo center bathroom mirror"
	describe "It appears to be a demo center bathroom window, but it is vague, indistinct, and little more than a blurry smear on reality."
	place "Demo Center Lavatory"
	
	property "description" "demo.MirrorDesc"
	string "name" "Lavatory mirror"
	string "base description" "A large, rectangular mirror built into the wall over the sink. Reflected in the mirror, you see:\n\n"
	component
	syn "mirror"
}

Thing
{
	name "demo center bathroom stall door"
	describe "It appears to be a demo center bathroom stall door, but it is vague, indistinct, and little more than a blurry smear on reality."
	place "Demo Center Lavatory"
	feature "twisted.reality.author.Obstruct"
	boolean "obstructed" false
	string "thereCloseDesc" "The stall door is closed, and there is a large notice posted on the wall just to the right of it."
	string "thereOpenDesc" "The stall door stands open, leading out into the bathroom."
	string "name" "bathroom stall door"
	string "openDesc" "To the east, the door to the single bathroom stall stands open."
	string "closeDesc" "To the east, a single bathroom stall is separated from the rest of the room by a black metal door and a similar set of dividers."
	extends "Class_Door"
	component
	syn "bathroom stall door"
	syn "stall door"
	syn "stall"
	syn "door"
}

Location
{
	name "demo center wastebasket"
	describe "A black plastic wastebasket, with a small swinging door labeled \"TRASH\"."
	place "Demo Center Lavatory"
	feature "twisted.reality.plugin.Put"
	string "name" "black plastic wastebasket"
	component
	syn "plastic wastebasket"
	syn "basket"
	syn "wastebasket"
}

Room
{
	name "Science and Technology Vehicle Area"
	describe "A large, perfectly cubical, empty room. It looks suspiciously unfinished, as though the person or persons responsible for designing the demo center had taken a coffee break before completing it. A large black box is set against one wall, and a large glass box stands across from it."
	place "Demo"
	exit "north" to "Science And Technology Demo Center"
}

Location
{
	name "Large Black Box"
	describe "A large, black metal box with a hinged top."
	place "Science and Technology Vehicle Area"
	feature "twisted.reality.plugin.Put"
	feature "twisted.reality.plugin.OpenCloseContainer"
	string "name" "black box"
	string "closed description" "It is currently closed."
	string "open description" "It is currently open."
	descript "open/close" "It is currently open."
	component
	syn "box"
	syn "black box"
	syn "black"
	syn "black metal box"
}

Location
{
	name "Large Glass Box"
	describe "A large, transparent glass box with a hinged top."
	place "Science and Technology Vehicle Area"
	feature "twisted.reality.plugin.OpenCloseContainer"
	feature "twisted.reality.plugin.Put"
	string "name" "glass box"
	string "closed description" "It is currently closed."
	string "open description" "It is currently open."
	boolean "transparent" true
	descript "open/close" "It is currently open."
	component
	syn "box"
	syn "glass box"
	syn "glass"
	syn "transparent glass box"
	broadcast
}

Thing
{
	name "Bun-Bun squeaky toy"
	describe "A grey, white, and vaguely rabbit shaped rubber figurine with long floppy ears and dark, vicious eyes."
	place "Large Glass Box"
	feature "demo.ToyDrop"
	feature "demo.ToySqueeze"
	syn "bunbun"
	syn "bun-bun"
	syn "bun"
	syn "toy"
	syn "squeaky toy"
}

Thing
{
	name "Bun-Bun squeaky toy"
	describe "A grey, white, and vaguely rabbit shaped rubber figurine with long floppy ears and dark, vicious eyes."
	place "Large Glass Box"
	feature "demo.ToyDrop"
	feature "demo.ToySqueeze"
	syn "bunbun"
	syn "bun-bun"
	syn "bun"
	syn "toy"
	syn "squeaky toy"
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
	name "demo center bathroom stall door"
	describe "It appears to be a demo center bathroom stall door, but it is vague, indistinct, and little more than a blurry smear on reality."
	place "Demo Center Lavatory"
	feature "twisted.reality.author.Obstruct"
	boolean "obstructed" false
	string "thereCloseDesc" "The stall door is closed, and there is a large notice posted on the wall just to the right of it."
	string "thereOpenDesc" "The stall door stands open, leading out into the bathroom."
	string "name" "bathroom stall door"
	string "openDesc" "To the east, the door to the single bathroom stall stands open."
	string "closeDesc" "To the east, a single bathroom stall is separated from the rest of the room by a black metal door and a similar set of dividers."
	extends "Class_Door"
	component
	syn "bathroom stall door"
	syn "stall door"
	syn "stall"
	syn "door"
}

Thing
{
	name "demo center toilet placard"
	describe "A tiny white cardboard square, propped up for easy reference and covered in flowing black script which reads:\n\n    \"Motion Sensitive Zero Gravity Toilet\"\n\t   \"Copywright 1798 GUE\"\n\"Frobozz Magic Zero Gravity Toilet Company\"\n\n    \"The staff of the Frobozz Magic Zero Gravity Toilet company thanks you for your purchase. The Model Zero HPZGT is truly superior to the standard Magic Toilet line, and, as the name implies, is designed for ease of use and can operate in many conditions that would render a normal toilet useless... We pride ourselves on catering to the distinguishing toilet owner, and we hope to enjoy your patronage in the future.\""
	place "Demo Center Bathroom Stall"
	feature "twisted.reality.plugin.ReadLook"
	string "name" "small white placard"
	component
	syn "card"
	syn "placard"
	syn "toilet placard"
}

Thing
{
	name "demo center bathroom notice"
	describe "A large, white, laminated piece of paper, topped with the large heading \"NOTICE:\" followed by the text:\n\n     \"This bathroom is equipped with a High Pressure Zero Gravity Toilet for your convenience and safety. Twisted Matrix Enterprises Inc. is in no way responsible for the misuse, intentional or otherwise, of the abovementioned High Pressure Zero Gravity Toilet, and is not responsible for any injuries, damages, psychological trauma, and/or destruction and/or loss of any parts, extremities, organs, possessions, or attributes inflicted during the operation of the toilet in question.\""
	place "Demo Center Bathroom Stall"
	feature "twisted.reality.plugin.ReadLook"
	string "name" "large notice"
	component
	syn "note"
	syn "notice"
	syn "large notice"
}

Location
{
	name "demo center paper dispenser"
	describe "A small, glossy black box, with a polished chrome sliding lever attached to the side."
	place "Demo Center Bathroom Stall"
	string "name" "toilet paper dispenser"
	component
	syn "toilet paper dispenser"
	syn "dispenser"
	syn "paper dispenser"
	syn "lever"
	syn "dispenser lever"
	syn "toilet paper dispenser lever"
	syn "paper dispenser lever"
}

Location
{
	name "demo center toilet"
	describe "A sleek, elegant form of lines and curves, gleaming white and perfectly symmetrical... A geometrical work of art, but also a toilet. There is no visible handle, leaving it perfectly unmarred, except for a small white placard on top of the back rest."
	place "Demo Center Bathroom Stall"
	feature "demo.SitToilet"
	string "name" "toilet"
	string "player preposition" "sitting on"
	string "preposition" "on"
	int "maximum occupancy" 1
	component
	syn "toilet"
	broadcast
}

Room
{
	name "Science And Technology Demo Center"
	describe "A spacious, high ceilinged room, with quite a few more stainless steel pipes and mechanical paraphenalia showing through it's walls than it probably has a right to. A large metal booth is built into the east wall, next to a counter strewn with technical manuals."
	place "Demo"
	descript "sliding glass doors closeDesc" "A pair of sliding glass doors stand shut in the northern wall."
	exit "south" to "Science and Technology Vehicle Area"
	exit "north" notTo "Demo Center West Wing Lobby" with "sliding glass doors"
}

Thing
{
	name "science and technology demo center table"
	describe "A long, rectangular counter, set with a number of manuals which have been firmly attached to its surface."
	place "Science And Technology Demo Center"
	string "name" "science and technology center counter"
	component
	syn "counter"
	syn "table"
}

Thing
{
	name "science and technology manuals"
	describe "There are several manuals on the counter, each of which seems to be firmly attached. Of particular note are the manuals titled \"Nominator\" and \"Gender Changer\"."
	place "Science And Technology Demo Center"
	string "name" "technical manuals"
	component
	syn "technical manuals"
	syn "manuals"
}

Thing
{
	name "name changing machine"
	describe "A large stainless steel structure vaguely reminiscent of a phone booth, with an embedded monitor and keyboard, featuring a prominent \"Execute\" key."
	place "Science And Technology Demo Center"
	feature "demo.DemoNamerType"
	string "new name" "Execute"
	descript "screen" "The screen is black, except for \"Execute\" in large green letters."
	component
	syn "monitor"
	syn "nominator"
	syn "booth"
	syn "key"
	syn "machine"
	syn "keyboard"
}

Thing
{
	name "sliding glass doors"
	describe "A pair of sliding glass doors set into the wall."
	place "Demo Center West Wing Lobby"
	feature "demo.AutomaticDoor"
	boolean "obstructed" true
	string "closedDescription" "A pair of sliding glass doors set into the wall."
	string "openDescription" "An open doorway set into the wall."
	string "close message" "The doors slide shut."
	string "openDesc" "An open, black framed doorway leads south."
	string "thereOpenDesc" "An open, black framed doorway leads north."
	string "closeDesc" "A pair of sliding glass doors stand shut in the southern wall."
	string "thereCloseDesc" "A pair of sliding glass doors stand shut in the northern wall."
	handler "door close" "demo.AutomaticDoorCloser"
	handler "startup" "demo.AutomaticDoorCloser"
	extends "Class_Door"
	component
	syn "glass doors"
	syn "doors"
	syn "door"
	syn "south"
	syn "north"
}

Thing
{
	name "Nominator Manual"
	describe "A book bound by a sturdy plastic cover, and attached firmly to the table. It reads:\n\n     \"Personalize your visit to our demo center with the Nominator 5000! Simply type your desired name on the supplied ergonomic keypad, and press the execute key when the name on the screen meets with your approval! A fun and easy way to increase your self worth and make your stay here a somewhat more memorable one.\"\n\n     \"(WARNING: SEVERE EYE DAMAGE: The Twisted Matrix Enterprises Nominator Model 108 may contain near-unpronouncable quantum effects. Do not look directly into the singularity.)\""
	place "Science And Technology Demo Center"
	feature "twisted.reality.plugin.ReadLook"
	component
	syn "manual"
}

Thing
{
	name "gender changer"
	describe "A small, grey, rectangular piece of plastic, with 32 pin connectors on either end and a large red button on the top."
	place "Science And Technology Demo Center"
	feature "demo.GenderChanger"
	thing "repop" "Science And Technology Demo Center"
	syn "red button"
	syn "changer"
	syn "button"
}

Thing
{
	name "Gender Changer Manual"
	describe "A book bound by a sturdy plastic cover, and attached firmly to the table. It reads:\n\n     \"Thank you for your purchase of our Type 32 Ronco Pocket Gender Changer. To to the somewhat touchy nature of human sexuality, this device is not precisely calibrated; However, the simple control system makes working out your desired settings a simple game of chance. In other words, if at first you don't succeed, try, try again.\"\n\n     \"(Ronco Pocket Body Alterations, Inc. can be held in no way liable for any effects, desired or otherwise, produced by this non-UL-Listed device, or any concequences thereof.)"
	place "Science And Technology Demo Center"
	feature "twisted.reality.plugin.ReadLook"
	component
	syn "changer manual"
	syn "manual"
}

Room
{
	name "Demo Center Gift Shop"
	describe "A small but brightly colored room, aside from the rather drab white walls and polished black marble floor. It is filled with shelves and racks where merchandise would go, but they stand almost empty, except for a few things no one would want. There is a check out counter along the south end of the room, with a built in cash register. A small white sign stands on the counter by the register. To the south, a doorway leads out into a larger room."
	place "Demo"
	exit "south" to "Demo Center West Wing Lobby"
}

Location
{
	name "demo center gift shop racks"
	describe "There are several large standing racks here, built from black metal wire and designed to rotate freely when spun."
	place "Demo Center Gift Shop"
	feature "twisted.reality.plugin.Put"
	string "name" "rack"
	component
	syn "rack"
	syn "racks"
	broadcast
}

Thing
{
	name "Divunal t-shirt"
	describe "A white t-shirt, almost exactly the right size for a generic guest person. It is emblazoned with the image of a yellowed piece of parchment, upon which the word \"Divunal\" has been written in flowing script. Below the image, in much smaller letters, is the phrase \"Less graphics, more game\" and a small blue Twisted Reality logo."
	place "demo center gift shop racks"
	thing "repop" "demo center gift shop racks"
	string "clothing appearance" "a Divunal t-shirt"
	extends "Class_Shirt"
	syn "t"
	syn "t shirt"
	syn "divunal shirt"
	syn "shirt"
	syn "t-shirt"
}

Thing
{
	name "Divunal t-shirt"
	describe "A white t-shirt, almost exactly the right size for a generic guest person. It is emblazoned with the image of a yellowed piece of parchment, upon which the word \"Divunal\" has been written in flowing script. Below the image, in much smaller letters, is the phrase \"Less graphics, more game\" and a small blue Twisted Reality logo."
	place "demo center gift shop racks"
	thing "repop" "demo center gift shop racks"
	string "clothing appearance" "a Divunal t-shirt"
	extends "Class_Shirt"
	syn "t"
	syn "t shirt"
	syn "divunal shirt"
	syn "shirt"
	syn "t-shirt"
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
	syn "pad"
	syn "small numeric keypad"
	syn "keypad"
	syn "register"
	syn "cash register"
}

Thing
{
	name "demo gift shop sign"
	describe "A small white cardboard sign, with black letters. It reads:\n\n\t\"TME Gift Shop Customers:\"\n\n\"Due to the increasing number of increasingly rude and inconsiderate guest users running off with our merchandise and using it to jam the plumbing, we have been forced to shut down the Gift Shop. We may re-open in the future, but only if some degree of civility on the parts of the visitors can be established.\"\n\nThank you,\n\nThe Management\""
	place "Demo Center Gift Shop"
	feature "twisted.reality.plugin.ReadLook"
	string "name" "small white sign"
	component
	syn "sign"
	syn "small sign"
	syn "white sign"
	syn "small white sign"
}

Thing
{
	name "demo center counter"
	describe "A curved, grey wooden barrier, about waist high. A cash register is built into the end near the doorway, and there is also a small sign standing on the middle of it."
	place "Demo Center Gift Shop"
	string "name" "check out counter"
	component
	syn "behind counter"
	syn "counter"
	syn "check out counter"
}

Location
{
	name "demo gift shop shelves"
	describe "The shelves are geometrically perfect arrangements of wooden boards, forming large, rectangular... shelves. Collectively, there is enough space to hold quite a few gifts, but they are strangely bare, except for the few things no one would want."
	place "Demo Center Gift Shop"
	feature "twisted.reality.plugin.Put"
	string "name" "shelf"
	string "preposition" "on"
	component
	syn "shelf"
	syn "shelves"
	broadcast
}

Thing
{
	name "John Romero action figure"
	describe "The semi-posable plastic figure of a chunky little man with long black hair tied back in a ponytail. He is wearing a tiny Ion Storm t-shirt, and there is a length of string protruding from his back, ending in a small plastic ring."
	place "demo gift shop shelves"
	feature "demo.DollPull"
	thing "repop" "demo gift shop shelves"
	syn "string"
	syn "ring"
	syn "romero"
	syn "john"
	syn "figure"
	syn "action figure"
}

Thing
{
	name "John Romero action figure"
	describe "The semi-posable plastic figure of a chunky little man with long black hair tied back in a ponytail. He is wearing a tiny Ion Storm t-shirt, and there is a length of string protruding from his back, ending in a small plastic ring."
	place "demo gift shop shelves"
	feature "demo.DollPull"
	thing "repop" "demo gift shop shelves"
	syn "string"
	syn "ring"
	syn "romero"
	syn "john"
	syn "figure"
	syn "action figure"
}

Thing
{
	name "demo center things no one would want"
	describe "There are a few really worthless things no one would want on the shelves... But really, you don't want them. Would you really want a jar-jar binks pez dispenser? Honestly, now."
	place "Demo Center Gift Shop"
	string "name" "things no one would want"
	component
	syn "stuff"
	syn "things no one wants"
	syn "things no one would want"
	syn "things"
}

Thing
{
	name "demo center jar-jar"
	describe "For christ's sake, it's a Jar-jar binks \"Official\" pez dispenser... Why are you even trying to looking at it?"
	place "Demo Center Gift Shop"
	feature "demo.DontGoThereGet"
	string "name" "Jar-jar Binks pez dispenser"
	component
	syn "jar"
	syn "jar-jar"
	syn "dispenser"
	syn "pez dispenser"
	syn "jar-jar binks"
	syn "jar-jar binks pez dispenser"
}

Location
{
	name "demo register drawer"
	describe "A grey plastic drawer, of the sort fitted into grey plastic cash registers and used to store money."
	place "Demo Center Gift Shop"
	feature "twisted.reality.plugin.Put"
	feature "demo.DrawerOpenClose"
	string "name" "cash register drawer"
	component
	syn "cash register drawer"
	syn "drawer"
	opaque
	shut
}

Thing
{
	name "bauble"
	describe "A small, shiny object, that catches the light and gleams in a rather valuable looking sort of way. "
	mood "providing light"
	place "demo register drawer"
	boolean "isLit" true
	boolean "frotzed" true
	descript "lighting" {"A pure white glow eminates from ", Name of("bauble"), ", bathing ", Pronoun of("bauble"), " in light."}
}

Player
{
	name "Class_Player"
	describe "This player is as-yet undescribed."
	place "Demo"
	feature "twisted.reality.plugin.Give"
	handler "logout" "twisted.reality.plugin.Logout"
	handler "login" "twisted.reality.plugin.Login"
	handler "say" "twisted.reality.plugin.PlayerSayHandler"
	ability "twisted.reality.plugin.Look"
	ability "twisted.reality.plugin.Give"
	ability "twisted.reality.plugin.Emote"
	ability "twisted.reality.plugin.Drop"
	ability "twisted.reality.plugin.Say"
	ability "twisted.reality.plugin.Go"
	ability "twisted.reality.plugin.Inventory"
	ability "twisted.reality.plugin.Insult"
	ability "twisted.reality.plugin.Take"
	ability "twisted.reality.plugin.Quit"
	ability "twisted.reality.plugin.Socials"
	passwd "--"
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
	name "demo center painting of tenth"
	describe "A framed portrait of a slender young man with bright green eyes and a calm, thoughtful face. His hair is an odd, coppery shade of blonde, and falls nearly to his waist in gentle waves. He is dressed in a dark green victorian style frock coat, and the painting has caught him in the act of studying a large brass pocketwatch."
	place "Demo Center East Wing"
	feature "demo.PagerPress"
	thing "reciever" "Tenth"
	string "name" "Painting of Tenth"
	
	property "description" "demo.PaintingDescription"
	component
	syn "portrait"
	syn "picture"
	syn "painting"
	syn "painting of tenth"
	syn "button"
	syn "page button"
	syn "small black button"
	syn "small button"
	syn "black button"
}

Thing
{
	name "demo center bathroom door"
	describe "A blue metal door, designed to be pushed open easily from either side. It is labeled \"Players\" just above the icon of a gender-neutral stick figure."
	place "Demo Center East Wing"
	feature "twisted.reality.plugin.door.OpenCloseSwingingDoor"
	feature "twisted.reality.author.Obstruct"
	string "name" "blue swinging door"
	component
	syn "door"
	syn "swinging door"
	syn "blue door"
	syn "blue swinging door"
}

Thing
{
	name "development door"
	describe "A worn, splintered wooden door with a dented copper handle. A piece of graph paper has been taped to it, scrawled with the word \"development\"."
	place "Demo Center East Wing"
	feature "twisted.reality.author.Obstruct"
	boolean "obstructed" false
	string "name" "wooden door"
	string "thereCloseDesc" "A battered wooden door is set into the south wall."
	string "thereOpenDesc" "A battered wooden doorway in the south wall leads out into the hall."
	string "closeDesc" "A piece of graph paper scrawled with the word \"Development\" is taped to a smaller, battered wooden door set into the north wall."
	string "openDesc" "A small, battered wooden door stands open to the north."
	extends "Class_Door"
	component
	syn "door"
	syn "wooden door"
}

Location
{
	name "Clothing Box"
	describe "A perfectly white box labeled \"Clothing Classes\" in neat black letters."
	place "Demo"
	feature "twisted.reality.plugin.Put"
	syn "box"
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
	name "class_belt"
	describe "A rather nondescript class_belt."
	place "Clothing Box"
	string "clothing location" "waist"
	extends "Class_Clothing"
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
	name "Class_Socks"
	describe "A white box."
	place "Clothing Box"
	extends "Class_Clothing"
}

Thing
{
	name "Class_Cape"
	describe "A white box."
	place "Clothing Box"
	string "clothing location" "neck"
	extends "Class_Clothing"
}

Thing
{
	name "Class_Shirt"
	describe "A white box."
	place "Clothing Box"
	string "clothing location 3" "right arm"
	string "clothing location 2" "left arm"
	string "clothing location" "chest"
	extends "Class_Clothing"
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
	name "Class_Tunic"
	describe "A white box."
	place "Clothing Box"
	string "clothing location" "chest"
	extends "Class_Clothing"
}

Thing
{
	name "Class_Shoes"
	describe "A white box."
	place "Clothing Box"
	string "clothing location 2" "right foot"
	string "clothing location" "left foot"
	extends "Class_Clothing"
}

Thing
{
	name "Class_Pants"
	describe "A white box."
	place "Clothing Box"
	string "clothing location 2" "right leg"
	string "clothing location" "left leg"
	extends "Class_Clothing"
}

Thing
{
	name "Class_Cloak"
	describe "A white box."
	place "Clothing Box"
	string "clothing location 5" "right leg"
	string "clothing location 4" "left leg"
	string "clothing location 3" "left arm"
	string "clothing location 2" "right arm"
	string "clothing location" "chest"
	extends "Class_Clothing"
}

Thing
{
	name "class_hat"
	describe "A blue box."
	place "Clothing Box"
	boolean "clothing worn" false
	string "clothing location" "crown"
	extends "Class_Clothing"
}

Thing
{
	name "class_robe"
	describe "A rather nondescript class_robe."
	place "Clothing Box"
	string "clothing location 6" "right leg"
	string "clothing location 5" "left leg"
	string "clothing location 4" "waist"
	string "clothing location 3" "left arm"
	string "clothing location 2" "right arm"
	string "clothing location" "chest"
	extends "Class_Clothing"
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

Thing
{
	name "sliding glass doors"
	describe "A pair of sliding glass doors set into the wall."
	place "Demo Center West Wing Lobby"
	feature "demo.AutomaticDoor"
	boolean "obstructed" true
	string "closedDescription" "A pair of sliding glass doors set into the wall."
	string "openDescription" "An open doorway set into the wall."
	string "close message" "The doors slide shut."
	string "openDesc" "An open, black framed doorway leads south."
	string "thereOpenDesc" "An open, black framed doorway leads north."
	string "closeDesc" "A pair of sliding glass doors stand shut in the southern wall."
	string "thereCloseDesc" "A pair of sliding glass doors stand shut in the northern wall."
	handler "door close" "demo.AutomaticDoorCloser"
	handler "startup" "demo.AutomaticDoorCloser"
	extends "Class_Door"
	component
	syn "glass doors"
	syn "doors"
	syn "door"
	syn "south"
	syn "north"
}

Location
{
	name "grey plastic chairs"
	describe "A blue box."
	place "Demo Center West Wing Lobby"
	feature "twisted.reality.plugin.furniture.Sit"
	feature "twisted.reality.plugin.furniture.Stand"
	feature "twisted.reality.plugin.Put"
	int "maximum occupancy" 6
	string "preposition" "on"
	string "player preposition" "sitting on"
	string "name" "grey plastic chair"
	component
	syn "chair"
	syn "chairs"
	syn "plastic chair"
	syn "plastic chairs"
	syn "grey plastic chair"
	broadcast
}

Player
{
	name "Class_God"
	describe "This player is as-yet undescribed."
	place "Demo"
	extends "Class_Player"
	ability "twisted.reality.author.MoodSet"
	ability "twisted.reality.author.Toss"
	ability "twisted.reality.author.Pause"
	ability "twisted.reality.author.Handle"
	ability "twisted.reality.author.ThingSet"
	ability "twisted.reality.author.Grab"
	ability "twisted.reality.author.KillProp"
	ability "twisted.reality.author.DescriptSet"
	ability "twisted.reality.author.Property"
	ability "twisted.reality.Passwd"
	ability "twisted.reality.author.Locate"
	ability "twisted.reality.author.StringSet"
	ability "twisted.reality.Armageddon"
	ability "twisted.reality.author.Gate"
	ability "twisted.reality.author.Scrutinize"
	ability "twisted.reality.author.Refrump"
	passwd "--"
}

Room
{
	name "Greenhouse Entrance"
	describe "An engraved marble plaque in the center of the floor proclaims this to be the \"Twisted Matrix Enterprises Twisted Reality Demonstration Center Greenhouse\". A small forest of plants are strewn haphazardly about the room, as if they were put there to meet a deadline. They all look remarkably similiar."
	place "Demo"
	theme "leaf"
	exit "southeast" to "Demo Center West Wing"
}

Thing
{
	name "brass cockroach"
	describe "A small mechanical cockroach, intricately designed with all of the parts and details of a real insect, made entirely of polished brass. There is a small hexagonal keyhole between two of the plates of its thorax."
	mood "lying on its back"
	place "Greenhouse Entrance"
	thing "repop" "Greenhouse Entrance"
	int "winds" 0
	boolean "windable" true
	handler "roachmove" "demo.RoachMove"
	handler "startup" "demo.RoachMove"
	syn "roach"
	syn "cockroach"
}

Thing
{
	name "TME Greenhouse Plants"
	describe "Upon closer examination, the plants, although strewn about the room with no sense of organization, are all exactly the same.  They have fairly geometric leaves and stems, as well as all being rooted in mounds of dirt which look strangely glossy and pot-shaped."
	place "Greenhouse Entrance"
	component
	syn "greenhouse plants"
	syn "plants"
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
	name "brass label"
	describe "A tiny, engraved brass plaque, identical to all of the other tiny engraved brass plaques attached to their respective potted plants, bearing the legend:\n\n     \"Artificial Potted Plant (Model 86003)\"\n  \t     \"Copywright 1793 GUE\"\n\"Frobozz Magic Artificial Potted Plant Company\"\n\t"
	place "Twisted Reality Corporate Demo Center"
	feature "twisted.reality.plugin.ReadLook"
	component
	syn "label"
	syn "labels"
	syn "brass labels"
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
	name "potted plant"
	describe "All of the plants bear a striking resemblance to one another, having the same number of leaves in approximately the same position, each set into an indentical grey marble pot with it's own tiny engraved brass label. Despite being an almost preternatural shade of green, the plants themselves bear a striking resemblance to palm trees, albeit ones that had been fitted with extra leaves and subjected to some sort of bonsai-like stunting process."
	place "Twisted Reality Corporate Demo Center"
	component
	syn "pots"
	syn "potted plants"
	syn "plants"
	syn "green potted plants"
	syn "green potted plant"
	syn "plant"
	syn "pot"
}

Room
{
	name "Messy New Jersey Office"
	describe "A strikingly mundane office, with peeling off-white plaster walls and a dirty old gray carpet. The room is lined with desks, all of which are heavily laden with computer equipment, manuals, paper bags, empty bottles, RedHat 6.1 install CDs, and chinese food containers. A large, red and yellow poster has been tacked to the northern wall, above a rather snazzy looking computer, and a black swivel chair is positioned in front of it."
	place "Demo"
	descript "development door openDesc" "A battered wooden doorway in the south wall leads out into the hall."
	exit "south" to "Demo Center East Wing" with "development door"
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
	name "quantum"
	describe "A rather nondescript quantum."
	place "quantum singularity"
}

Thing
{
	name "BusinessMind for Jewelers poster"
	describe "A large poster of Rodin's \"The Thinker\" sculpture, surrounded by a red background. It also has a great deal of information about a piece of database software called BusinessMind for Jewelers, and directs you to www.businessmind.com, where you can find more information on \"Business Software that thinks the way you do\"."
	place "Messy New Jersey Office"
	component
	syn "poster"
	syn "red and white poster"
}

Location
{
	name "demo center swivel chair"
	describe "An adjustable black plastic chair with a padded seat and backrest, ending in five jointed wheels."
	place "Messy New Jersey Office"
	feature "twisted.reality.plugin.furniture.Sit"
	feature "twisted.reality.plugin.furniture.Stand"
	string "name" "black swivel chair"
	string "player preposition" "sitting on"
	string "preposition" "on"
	int "maximum occupancy" 1
	component
	syn "black swivel chair"
	syn "swivel chair"
	syn "chair"
	broadcast
}

Thing
{
	name "demo center keyboard"
	describe "A standard grey US Standard keyboard. It would be described in more detail, but one would hope you'd recognize one by this point."
	place "Messy New Jersey Office"
	component
	syn "keyboard"
}

Thing
{
	name "development door"
	describe "A worn, splintered wooden door with a dented copper handle. A piece of graph paper has been taped to it, scrawled with the word \"development\"."
	place "Demo Center East Wing"
	feature "twisted.reality.author.Obstruct"
	boolean "obstructed" false
	string "name" "wooden door"
	string "thereCloseDesc" "A battered wooden door is set into the south wall."
	string "thereOpenDesc" "A battered wooden doorway in the south wall leads out into the hall."
	string "closeDesc" "A piece of graph paper scrawled with the word \"Development\" is taped to a smaller, battered wooden door set into the north wall."
	string "openDesc" "A small, battered wooden door stands open to the north."
	extends "Class_Door"
	component
	syn "door"
	syn "wooden door"
}

Thing
{
	name "demo center computer"
	describe "A large grey box labeled \"VA Research\", attached to a similarly colored keyboard and monitor."
	place "Messy New Jersey Office"
	component
	syn "computer"
}

Thing
{
	name "brass paperweight"
	describe "A short brass dome about the size of a coffee cup, with a small glass lens set into its center."
	place "Messy New Jersey Office"
	syn "paperweight"
	syn "pager"
}

Thing
{
	name "BummCo Toys ownership guide"
	describe "A folded piece of white paper, covered in poorly printed lettering. It reads:\n\n\"BummCo Toys Proudly Presents the \"John Romero: Master of Daikatana\" promotional semi-posable talking action figure! Just yank his crank and hear him say any one of 18 colorful phrases.\"\n\n\"WARNING: Highly Flammable. Do not immerse in liquids. Explodes Under Pressure. Not a Food. Rated Grade F (Human Inedible) by the Artifical Food Standards committee. May contain bullshit.\"\n\n\"Thank you for your purchase. BummCo Toys is a trademark and fully owned subsidiary of General Firms (tm).\""
	place "Messy New Jersey Office"
	feature "twisted.reality.plugin.ReadLook"
	thing "repop" "demo gift shop shelves"
	syn "guide"
	syn "ownership guide"
}

Room
{
	name "Demo Center West Wing"
	describe "This is the west wing of the demo center.  The walls are a polished, gleaming, white substance, and the floor is perfectly smooth black marble.  It is a triangluar room, with points at the northwestern, southwestern, and western ends.  The sides of the triangle each have an arch set into them.  Over the eastern arch, there is a sign that says \"Back To Main Demo Center\".  The southwest and northwest arches are unlabeled."
	place "Demo"
	exit "east" to "Demo Center West Wing Lobby"
	exit "southwest" to "Demo Center Waiting Room"
	exit "northwest" to "Greenhouse Entrance"
}

Location
{
	name "General Box"
	describe "A blue box."
	place "Demo"
	extends "Class_Container"
}

Location
{
	name "Class_Closeable Container"
	describe "A blue box."
	place "General Box"
	feature "twisted.reality.plugin.OpenCloseContainer"
	extends "Class_Container"
}

Location
{
	name "Class_Container"
	describe "A generic container."
	place "General Box"
	feature "twisted.reality.plugin.Put"
}

Thing
{
	name "Class_Door"
	describe "This is a regular doorway.  You can OPEN and CLOSE it."
	place "General Box"
	feature "twisted.reality.plugin.door.Close"
	feature "twisted.reality.plugin.door.Open"
	feature "twisted.reality.author.Obstruct"
	string "obstructed message" "The door is closed.  You can't walk through it."
	boolean "obstructed" true
	syn "door"
	syn "doorway"
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

Location
{
	name "demo center obelisk"
	describe "The obelisk is a polished, glossy black, and set with a large, colorful map and various pieces of Twisted Reality propoganda. At the top is a familiar looking black line-art \"Twisted Reality 1.2.1\" logo, and a large piece of text welcoming you to the demo center. Below that is a bright yellow polygon, very similar to the shape of the room you're currently standing in, labeled \"YOU ARE HERE!\". The hallway leading east from the main room connects to a large blue area labeled \"Restrooms\" to the east, and a much smaller, brown room to the north, labeled \"development\". The west hallway branches off into a Lobby, with a Gift Shop to it's north, and two \"Staging Areas\" further west."
	place "Demo Information Center"
	feature "twisted.reality.plugin.Put"
	feature "twisted.reality.plugin.furniture.Sit"
	feature "twisted.reality.plugin.furniture.Stand"
	feature "twisted.reality.plugin.ReadLook"
	int "maximum occupancy" 3
	string "preposition" "on"
	string "player preposition" "sitting on"
	string "name" "Obsidian Obelisk"
	component
	syn "obelisk"
	syn "map"
	syn "brightly colored map"
	broadcast
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
	syn "small brass bell"
	syn "brass bell"
	syn "bell"
	syn "button"
	syn "brass button"
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
	syn "small brass bell"
	syn "brass bell"
	syn "bell"
	syn "button"
	syn "brass button"
}

Thing
{
	name "obelisk welcoming text"
	describe "Despite being in a large, white Times Roman font on a black background, you can't quite seem to make out what it says. Something along the lines of \"Welcome to our demonstration center, home of Twisted Matrix Enterprises...\" but after that, your eyes begin to glaze over. Jumbled, run-on sentences are twined with phrases like \"Enterprise Wide\", \"Networked Scalability\", and \"Multithreaded Dynamic Architecture\", which, while compelling, destroy any meaning the text may have had."
	place "Demo Information Center"
	feature "twisted.reality.plugin.ReadLook"
	component
	syn "large piece of text"
	syn "piece of text"
	syn "text"
	syn "welcoming text"
}

Room
{
	name "Demo Center Waiting Room"
	describe "This is a comfortable waiting room with high-backed leather chairs and wooden-paneled walls. There is a solid oak coffee table here, with a tasteful gold inlay.  To the northeast, there is a gold-lined archway leading into a room with white walls and a black floor."
	place "Demo"
	theme "wood"
	exit "northeast" to "Demo Center West Wing"
}

Location
{
	name "demo center coffee table"
	describe "A dark, polished wooden table, made of what appears to be solid oak.  A thin line of gold inlay traces a complicated, yet elegant, pattern around the edge of the table.  It is set between the high backed chairs."
	place "Demo Center Waiting Room"
	feature "twisted.reality.plugin.Put"
	feature "twisted.reality.plugin.furniture.Sit"
	feature "twisted.reality.plugin.furniture.Stand"
	int "maximum occupancy" 2
	string "preposition" "on"
	string "player preposition" "sitting on"
	string "name" "coffee table"
	component
	syn "table"
	syn "coffee table"
	broadcast
}

Location
{
	name "green leather book"
	describe "A green, leather bound book, entitled \"Simulacra And Simulation\" in gold embossed letters."
	place "demo center coffee table"
	feature "demo.OpenBookBox"
	feature "twisted.reality.plugin.Put"
	thing "repop" "demo center coffee table"
	descript "opened" "It is open, revealing that the center of each page has been removed, making it useless as a book but quite functional as a container."
	syn "leather book"
	syn "green book"
	syn "book"
}

Thing
{
	name "small brass key"
	describe "A small brass key with a delicately polished hexagonal tip. "
	place "green leather book"
	feature "demo.BrassWind"
	thing "repop" "green leather book"
	syn "key"
	syn "brass key"
}

Location
{
	name "green leather book"
	describe "A green, leather bound book, entitled \"Simulacra And Simulation\" in gold embossed letters."
	place "demo center coffee table"
	feature "demo.OpenBookBox"
	feature "twisted.reality.plugin.Put"
	thing "repop" "demo center coffee table"
	descript "opened" "It is open, revealing that the center of each page has been removed, making it useless as a book but quite functional as a container."
	syn "leather book"
	syn "green book"
	syn "book"
}

Thing
{
	name "small brass key"
	describe "A small brass key with a delicately polished hexagonal tip. "
	place "green leather book"
	feature "demo.BrassWind"
	thing "repop" "green leather book"
	syn "key"
	syn "brass key"
}

Location
{
	name "demo center high backed chair"
	describe "A blue box."
	place "Demo Center Waiting Room"
	feature "twisted.reality.plugin.furniture.Sit"
	feature "twisted.reality.plugin.furniture.Stand"
	int "maximum occupancy" 2
	string "preposition" "on"
	string "player preposition" "sitting on"
	string "name" "high-backed chair"
	component
	syn "chair"
	syn "high backed chair"
	broadcast
}

Player
{
	name "Class_Guest"
	describe "A dummy class for guests."
	place "Demo"
	thing "default repop" "Demo Information Center"
	
	property "description" "demo.GuestDescription"
	string "gender pronoun" "person"
	handler "logout" "demo.GuestLogout"
	extends "Class_Player"
	passwd "null"
}

Player
{
	name "guest"
	describe "A blue box."
	place "Demo"
	thing "guest start" "Twisted Reality Corporate Demo Center"
	thing "playerclass" "Class_Guest"
	int "guest number" 6
	handler "login" "demo.GuestLogin"
	passwd "guVeRgi5kAY4k"
}

