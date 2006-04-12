
from twisted.reality import *
from inherit import inheritance

t=reference.Reference
def d(**kw): return kw
r=inheritance.ThingFactory()
damien=inheritance.Claimant('Damien')(
	description='He looks pretty hassled.'
	)

front_lawn=Room("Front Lawn")(
	 description="The mansion's unkempt lawn surrenders to the yellowed remains of a cornfield to the south, and a dense bordering forest to the east. The tall grass of the lawn continues to the west, towards the mansion's gravel drive, and north, towards the mansion itself.",
	 exits={"west":t("Front Lawn(2)"),
			"north":t("Side Lawn(2)")}
	 )

front_lawn_1=Room("Front Lawn(1)")(
	description="You are in front of the east wing of a weathered old mansion. It continues to the east, almost touching the dense forest that lines the property, and to the west, towards the gravel driveway leading to the front door. The unkempt grass of the front lawn continues on to the south before giving way to a vast field of yellowed corn.",
	exits={'west':  t("Chateau Courtyard"),
		   'south': t("Front Lawn(2)"),
		   'east': t("Side Lawn(2)")}
	)

front_lawn_2=Room("Front Lawn(2)") (
	description="The knee high lawn of the mansion trails off a bit to the south, where the yellow husks of the cornfield begin. The lawn continues to the east, towards the forest surrounding the property, and north, towards the mansion itself. The mansion's  gravel drive is just to the west, leading up to the front steps.",
	exits={'west':t("Circular Driveway"),
		   'east':t("Front Lawn"),
		   'north':t("Front Lawn(1)")}
	)

front_lawn_3=Room("Front Lawn(3)")(
	description="You are in front of the west wing of a darkened old mansion. It continues to the west, almost touching the dense forest that lines the property, and to the east, towards the gravel driveway leading to the front door. The unkempt grass of the front lawn continues to the south before giving way to a vast field of yellowed corn.",
	exits={'west':t("Side Lawn(3)"),
		   'south':t("Front Lawn(4)"),
		   'east':t("Chateau Courtyard")}
	)

front_lawn_4=r.create("Front Lawn(4)","The unkempt lawn of the mansion stops just to the south, where the dried yellow ruin of the cornfield begins. The knee high grass continues west, towards the forest surrounding the property, and north, towards the mansion itself. A curved gravel drive passes by to the east, following an arc that leads up to the mansion's front steps.")

front_lawn_5=r.create("Front Lawn(5)","The edge of the mansion's unkempt lawn, where it surrenders to the yellowed remains of a cornfield to the south and the dense bordering forest to the west. The lawn continues to the east, towards the mansion's gravel drive, and north, towards the mansion itself.")

# side lawn

side_lawn=r.create("Side Lawn","You are near the rear corner of the mansion, where a thick field of tall grass and weeds that was once the back yard extends outwards to the west. Further north, towards the back of the lawn, you can make out the shape of a small shed against the trees, and there is a narrow path leading south between the wall of the mansion and the forest that has grown up against it.")

side_lawn_1=r.create("Side Lawn(1)","A narrow path between the thick overgrowth  of the forest and the rotting wooden walls of the mansion. It leads south to the front lawn, and continues towards a similar clearing to the north.")

side_lawn_2=r.create("Side Lawn(2)","You are at the eastern corner of a darkened old mansion. The nearby forest has begun to grow in over the lawn, and the branches of the closest trees almost touch the eastern wall, leaving a narrow path along the side of the mansion to the north. The lawn continues along the front of the mansion to the east, towards the front door, and to the south, where it gives way to the yellowed remains of a cornfield.")

side_lawn_3=r.create("Side Lawn(3)","You are at the western corner of an old, neglected mansion. The surrounding forest has begun to spread over the lawn, and the branches of the nearest trees are beginning to brush the mansion's walls, leaving only a narrow path between them to the north. The lawn continues along the front of the mansion to the east, towards the front door, and to the south, where it gives way to a long forgotten cornfield.")

side_lawn_4=r.create("Side Lawn(4)","A narrow path between the dense trees and brush of the forest and the peeling grey wood of the mansion's western wall. It continues south to the front lawn, and meanders along into a similar clearing to the north.")

side_lawn_5=r.create("Side Lawn(5)","You are near the back side of the mansion, where an unkempt field of weeds and tall grass that was once the back lawn extends outwards to the east. Further north, towards the back of the yard, you can make out the shape of a small building against the trees, and there is a narrow path leading south between the western wall of the mansion and the forest that has grown up against it. ")

# back lawn

back_lawn=r.create("Back Lawn","You are near the... aw, fuck it.")

back_lawn_1=r.create("Back Lawn(1)","A Back Lawn looking as if it needs to be described.")

back_lawn_3=r.create("Back Lawn(3)","A Back Lawn looking as if it needs to be described.")

back_lawn_4=r.create("Back lawn(4)","A Back lawn looking as if it needs to be described.")

back_lawn_5=r.create("Back Lawn(5)","A Back Lawn looking as if it needs to be described.")

back_lawn_6=r.create("Back Lawn(6)","A Back Lawn looking as if it needs to be described.")

back_lawn_7=r.create("Back Lawn(7)","A Back Lawn looking as if it needs to be described. A good old game of Croquet can be had here.")

back_lawn_8=r.create("Back Lawn(8)","You are near the back end of the mansion, by the large field of overgrown grass and weeds that forms the back yard. The rear wall of the mansion continues on for quite some way to the west, towards the back door, and the lawn continues out to the north for quite a ways, where a dark, blocky shape is silhouetted against the trees.")

back_lawn_9=r.create("Back Lawn(9)","You are near the back end of the mansion, by the large field of overgrown grass and weeds that forms the back yard. The rear wall of the mansion continues on for quite some way to the east, to the back door, and the lawn continues out to the north for quite a ways, where a dark, blocky shape is silhouetted against the trees.")

wooded_grove=r.create("Wooded Grove","A Wooded Grove looking as if it needs to be described.")

forest_clearing=r.create("Forest Clearing","An undescribed forest clearing.")

# and let's not forget the shed

old_wooden_shed=r.create("Old Wooden Shed","An Old Wooden Shed looking as if it needs to be described.")

###
## Country Road
###

country_road=r.create("Country Road","An old dirt road, leading off into the darkness to the east and west. It is bordered on the south side by a crumbling stone wall, while an opening in the trees to the north leads downhill to a gravel driveway.")

country_road_1=r.create("Country Road(1)","A poorly maintained dirt road, leading off into darkness to the east and west. It is bordered by a steep ridge to the north, and an old stone wall to the south. The branches of the trees along the sides of the road nearly meet overhead, throwing a patchwork of shadows over the ground.")

country_road_2=r.create("Country Road(2)","A poorly maintained dirt road, leading off into darkness to the east and west. It is bordered by a steep ridge to the north, and a crumbling stone wall to the south. The trees along the road form a thick canopy overhead, blocking out even the faint light from the sky.")

country_road_3=r.create("Country Road(3)","A poorly maintained dirt road, leading off into darkness to the east and west. It is bordered by a steep ridge to the north, and an old stone wall to the south. The branches of the trees along the edge of the road nearly touch overhead, covering the ground with dancing shadows and faint patches of light")

country_road_4=r.create("Country Road(4)","A poorly maintained dirt road, leading off into darkness to the east and west. It is bordered by a steep ridge to the north, and a crumbling stone wall to the south. The trees along the road form a thick canopy overhead, lacing together like skeletal fingers to block out the faint light from the sky.")

# driveway

driveway=r.create("Driveway","The far end of a long gravel driveway leading downhill to the north, where the dark outlines of a house loom above the horizon. To the south, an old dirt road is visible through an opening in the trees, and to the east and west are endless yellow fields of neglected corn.")

circular_driveway=r.create("Circular Driveway", "The far side of a circular gravel drive, both ends of which lead north towards a tall, imposing mansion. To the south, the two sides converge into a single driveway and lead uphill through the middle of a vast, yellowish white field of dead corn.")

gravel_driveway=r.create("Gravel Driveway","The bottom end of a long gravel driveway, leading towards a dark, imposing mansion. Vast fields of corn rise up on either side, brittle and yellow with age. Further to the north, the driveway splits into a circular parth in the courtyard of the mansion, while to the south, it continues uphill towards a distant forest.")

gravel_driveway_1=r.create("Gravel Driveway(1)","A long gravel driveway surrounded by cornfields. It leads upwards to the south, towards where the fields give way to a vast expanse of forest, and downwards to the north, towards a dark, weathered old mansion.")

gravel_driveway_2=r.create("Gravel Driveway(2)","A long gravel driveway, surrounded by yellowed cornfields on either side. To the south, it leads uphill towards the forest at the edge of the property, and to the north, it runs downhill towards the dark shape of a house silhoutted against the horizon.")

# darkened road

darkened_road=r.create("Darkened Road","An old dirt road, leading off into darkness to the east and west. It is bordered by a steep ridge to the north, and the crumbling remains of a stone wall to the south. The trees form an almost solid wall of leaves and branches above the road, blotting out the sky.")

darkened_road_1=r.create("Darkened Road(1)","The road twists and turns through the narrow space allotted by the trees, which have grown even closer together overhead, shutting out the light from the sky. The stone wall is only a scattered pile of stones at this point, leaving the road open to the darkness of the forest to the south.")

darkened_road_2=r.create("Darkened Road(2)","A faint trail through the woods that may once have been a dirt road, leading off into darkness to the east and west. It is bordered by a steep ridge to the north, and the crumbling remains of a stone wall to the south, overgrown with ferns and odd looking plants. The trees form an almost solid wall of leaves and clawlike branches above the road, shutting out the sky.")

darkened_road_3=r.create("Darkened Road(3)","The road has given way to a narrow, forgotten path through the trees, overgrown with ferns and dark, waving grass. The trees seem to have grown together into a single, writhing mass above the road.")

####
## Chateau
####

chateau_courtyard=r.create("Chateau Courtyard","You are standing in front of a large grey mansion. A circular gravel drive runs past the front steps, leading south to where it passes through the middle of a huge field of yellowed corn. The lawn continues to the east and west, as does the mansion itself, towards the forest that surrounds the property.")

chateau_lavatory=r.create("Chateau Lavatory","A Chateau Lavatory looking as if it needs to be described.")

chateau_bathroom=r.create("Chateau Bathroom", "A Bathroom looking as if it needs to be described.")

chateau_bedroom=r.create("Chateau Bedroom","A Bedroom looking as if it needs to be described.")

guest_bedroom=r.create("Guest Bedroom", "A Guest Bedroom looking as if it needs to be described.")

guest_bathroom=r.create("Guest Bathroom", "A Guest Bathroom looking as if it needs to be described.")

unfinished_room=r.create("Unfinished Room","An Unfinished Room, looking like some kind of crazy Tool video or something.")

antiques_room=r.create("Antiques Room","An Antiques Room looking as if it needs to be described.")

chateau_antechamber=r.create("Chateau Antechamber","This is a dark, high-ceilinged room with a polished wooden floor.  Exits lead in all directions; you can go east or west through archways into the mansion's hallways, up to the second floor, or south through the front door.")

antechamber_table=Thing("Antechamber Table")
antechamber_table.display_name="table"
antechamber_table.description="This is a small table."
antechamber_table.place=chateau_antechamber

study=r.create("Study","A Study looking as if it needs to be described.")

# hallway

chateau_hallway=r.create("Chateau Hallway","A Chateau Hallway looking as if it needs to be described.")
chateau_hallway_1=r.create("Chateau Hallway(1)","A Chateau Hallway looking as if it needs to be described.")
chateau_hallway_2=r.create("Chateau Hallway(2)","A Chateau Hallway looking as if it needs to be described.")
chateau_hallway_3=r.create("Chateau Hallway(3)","A Chateau Hallway looking as if it needs to be described.")
chateau_hallway_4=r.create("Chateau Hallway(4)","A Chateau Hallway looking as if it needs to be described.")
chateau_hallway_5=r.create("Chateau Hallway(5)","A Chateau Hallway looking as if it needs to be described.")
chateau_hallway_6=r.create("Chateau Hallway(6)","A Chateau Hallway looking as if it needs to be described.")
chateau_hallway_7=r.create("Chateau Hallway(7)","A Chateau Hallway looking as if it needs to be described.")
chateau_hallway_8=r.create("Chateau Hallway(8)","A Chateau Hallway looking as if it needs to be described.")
chateau_hallway_9=r.create("Chateau Hallway(9)","A Chateau Hallway looking as if it needs to be described.")
chateau_hallway_10=r.create("Chateau Hallway(10)","A Chateau Hallway looking as if it needs to be described.  It should have a couch or something, pointed out the window.")
chateau_hallway_11=r.create("Chateau Hallway(11)","A Chateau Hallway looking as if it needs to be described.")
chateau_hallway_12=r.create("Chateau Hallway(12)","A Chateau Hallway looking as if it needs to be described.")
chateau_hallway_13=r.create("Chateau Hallway(13)","A Chateau Hallway looking as if it needs to be described.")
chateau_hallway_14=r.create("Chateau Hallway(14)","A Chateau Hallway looking as if it needs to be described.")
chateau_hallway_15=r.create("Chateau Hallway(15)","A Chateau Hallway looking as if it needs to be described.")
chateau_hallway_16=r.create("Chateau Hallway(16)","A Chateau Hallway looking as if it needs to be described.")



# the library

chateau_library=r.create("Chateau Library","A Chateau Library looking as if it needs to be described.")

chateau_library_1=r.create("Chateau Library(1)","A Chateau Library looking as if it needs to be described.")

chateau_library_2=r.create("Chateau Library(2)","A Chateau Library looking as if it needs to be described.")

# the attic

chateau_attic=r.create("Chateau Attic","A Chateau Attic looking as if it needs to be described.")

chateau_attic_1=r.create("Chateau Attic(1)","A Chateau Attic looking as if it needs to be described.")

chateau_attic_2=r.create("Chateau Attic(2)","A Chateau Attic looking as if it needs to be described.")

chateau_attic_3=r.create("Chateau Attic(3)","A Chateau Attic looking as if it needs to be described.")

chateau_attic_4=r.create("Chateau Attic(4)","A Chateau Attic looking as if it needs to be described.")

chateau_kitchen=r.create("Chateau Kitchen", "A Chateau Kitchen looking as if it needs to be described.")

kitchen_closet=r.create("Kitchen Closet","A Kitchen Closet looking as if it needs to be described.")

chateau_pantry=r.create("Chateau Pantry","A Chateau Pantry looking as if it needs to be described.")

chateau_parlor=r.create("Chateau Parlor","A Chateau Parlor looking as if it needs to be described.")

# the staircase

chateau_stairwell=r.create("Chateau Stairwell","A Chateau Stairwell looking as if it needs to be described.")

chateau_staircase=r.create("Chateau Staircase", "A Chateau Staircase looking as if it needs to be described.")

chateau_staircase_landing=r.create("Chateau Staircase Landing","A Chateau Staircase Landing looking as if it needs to be described.")

# in the basement, the quiet basement, the evil lurks at night

chateau_basement=r.create("Chateau Basement","A Chateau Basement looking as if it needs to be described.")

chateau_basement_1=r.create("Chateau Basement(1)","A Chateau Basement looking as if it needs to be described.")

chateau_basement_2=r.create("Chateau Basement(2)","A Chateau Basement looking as if it needs to be described.")

chateau_basement_3=r.create("Chateau Basement(3)","A Chateau Basement looking as if it needs to be described.")

chateau_basement_4=r.create("Chateau Basement(4)","A Chateau Basement looking as if it needs to be described.")

# chateau_basement_5=r.create("Chateau Basement(5)","A Chateau Basement looking as if it needs to be described.")

# dining area

chateau_dining_hall=r.create("Chateau Dining Hall","A Chateau Dining Hall looking as if it needs to be described.")
chateau_dining_hall_1=r.create("Chateau Dining Hall(1)","A Chateau Dining Hall looking as if it needs to be described.")

chateau_sitting_room=r.create("Chateau Sitting Room","here is a place where you sit.  DESCRIBE ME")

# there is an exit here

side_lawn_3.add_exit('east',front_lawn_3)
side_lawn_3.add_exit('north',side_lawn_4)
side_lawn_3.add_exit('south',front_lawn_5)

chateau_kitchen.add_exit('east',chateau_pantry)
chateau_kitchen.add_exit('south',kitchen_closet)
chateau_kitchen.add_exit('west',chateau_hallway_1)

back_lawn_1.add_exit('east',back_lawn_7)
back_lawn_1.add_exit('west',back_lawn_3)
back_lawn_1.add_exit('south',back_lawn)

side_lawn_2.add_exit('west',front_lawn_1)
side_lawn_2.add_exit('south',front_lawn)
side_lawn_2.add_exit('north',side_lawn_1)

side_lawn_1.add_exit('south',side_lawn_2)
side_lawn_1.add_exit('north',side_lawn)

# chateau_basement_5.add_exit('south',chateau_basement)

chateau_basement_4.add_exit('south',chateau_basement_3)

chateau_basement_3.add_exit('north',chateau_basement_4)
chateau_basement_3.add_exit('east',chateau_basement)

chateau_basement_2.add_exit('south',chateau_basement_1)

chateau_basement_1.add_exit('north',chateau_basement_2)
chateau_basement_1.add_exit('west',chateau_basement)

chateau_basement.add_exit('east',chateau_basement_1)
chateau_basement.add_exit('west',chateau_basement_3)
chateau_basement.add_exit('up',chateau_stairwell)


country_road.add_exit('west',country_road_3)
country_road.add_exit('east',country_road_1)
country_road.add_exit('north',driveway)

chateau_pantry.add_exit('south',chateau_stairwell)
chateau_pantry.add_exit('north',back_lawn)
chateau_pantry.add_exit('east',chateau_hallway_2)
chateau_pantry.add_exit('west',chateau_kitchen)

back_lawn.add_exit('west',back_lawn_9)
back_lawn.add_exit('east',back_lawn_8)
back_lawn.add_exit('north',back_lawn_1)
back_lawn.add_exit('south',chateau_pantry)

chateau_staircase_landing.add_exit('north',chateau_library_1)
chateau_staircase_landing.add_exit('west',chateau_hallway_6)
chateau_staircase_landing.add_exit('east',chateau_hallway_4)
chateau_staircase_landing.add_exit('down',chateau_staircase)

side_lawn.add_exit('south',side_lawn_1)
side_lawn.add_exit('west',back_lawn_8)

old_wooden_shed.add_exit('north',back_lawn_5)

chateau_library_2.add_exit('east',chateau_hallway_14)
chateau_library_2.add_exit('west',chateau_library_1)

chateau_library_1.add_exit('south',chateau_staircase_landing)
chateau_library_1.add_exit('east',chateau_library_2)
chateau_library_1.add_exit('west',chateau_library)

chateau_attic_4.add_exit('north',chateau_attic_3)

chateau_attic_3.add_exit('south',chateau_attic_4)
chateau_attic_3.add_exit('east',chateau_attic)

chateau_attic_2.add_exit('south',chateau_attic_1)

chateau_attic_1.add_exit('north',chateau_attic_2)
chateau_attic_1.add_exit('south',chateau_attic)

chateau_stairwell.add_exit('down',chateau_basement)
chateau_stairwell.add_exit('north',chateau_pantry)

darkened_road_3.add_exit('east',darkened_road_2)

darkened_road_2.add_exit('west',darkened_road_3)
darkened_road_2.add_exit('east',country_road_4)

darkened_road_1.add_exit('west',darkened_road)

forest_clearing.add_exit('south',wooded_grove)

wooded_grove.add_exit('north',forest_clearing)
wooded_grove.add_exit('south',back_lawn_5)

unfinished_room.add_exit('west',antiques_room)

gravel_driveway.add_exit('south',gravel_driveway_1)
gravel_driveway.add_exit('north',circular_driveway)

gravel_driveway_1.add_exit('south',gravel_driveway_2)
gravel_driveway_1.add_exit('north',gravel_driveway)

chateau_antechamber.add_exit('east',chateau_hallway_16)
chateau_antechamber.add_exit('up',chateau_staircase)
chateau_antechamber.add_exit('west',chateau_hallway)
chateau_antechamber.add_exit('south',chateau_courtyard)

chateau_staircase.add_exit('up',chateau_staircase_landing)
chateau_staircase.add_exit('down',chateau_antechamber)

chateau_dining_hall.add_exit('north',chateau_dining_hall_1)
chateau_dining_hall.add_exit('south',chateau_hallway)

chateau_dining_hall_1.add_exit('south',chateau_dining_hall)
chateau_dining_hall_1.add_exit('north',chateau_hallway_1)

chateau_bathroom.add_exit('north',chateau_bedroom)

chateau_bedroom.add_exit('south',chateau_bathroom)
chateau_bedroom.add_exit('west',chateau_hallway_14)

chateau_hallway.add_exit('east',chateau_antechamber)
chateau_hallway.add_exit('north',chateau_dining_hall)

circular_driveway.add_exit('west',front_lawn_4)
circular_driveway.add_exit('east',front_lawn_2)
circular_driveway.add_exit('south',gravel_driveway)
circular_driveway.add_exit('north',chateau_courtyard)

darkened_road.add_exit('east',darkened_road_1)
darkened_road.add_exit('west',country_road_2)

guest_bedroom.add_exit('east',chateau_hallway_13)
guest_bedroom.add_exit('south',guest_bathroom)
guest_bathroom.add_exit('north',guest_bedroom)

guest_bedroom.add_exit('south',guest_bathroom)
guest_bedroom.add_exit('east',chateau_hallway_13)

kitchen_closet.add_exit('north',chateau_kitchen)

chateau_parlor.add_exit('north',chateau_hallway_2)
chateau_parlor.add_exit('south',chateau_hallway_3)

chateau_hallway_16.add_exit('north',chateau_sitting_room)
chateau_hallway_16.add_exit('west',chateau_antechamber)

chateau_sitting_room.add_exit('south',chateau_hallway_16)
chateau_sitting_room.add_exit('north',chateau_hallway_3)

chateau_attic.add_exit('west',chateau_attic_3)
chateau_attic.add_exit('east',chateau_attic_1)
chateau_attic.add_exit('down',chateau_hallway_4)

chateau_hallway_15.add_exit('west',chateau_hallway_5)

chateau_hallway_14.add_exit('south',chateau_hallway_5)
chateau_hallway_14.add_exit('east',chateau_bedroom)
chateau_hallway_14.add_exit('west',chateau_library_2)

chateau_hallway_13.add_exit('east',chateau_library)
chateau_hallway_13.add_exit('west',guest_bedroom)
chateau_hallway_13.add_exit('south',chateau_hallway_6)

study.add_exit('south',chateau_hallway_12)

chateau_hallway_12.add_exit('north',study)
chateau_hallway_12.add_exit('west',chateau_hallway_11)

chateau_hallway_11.add_exit('east',chateau_hallway_12)
chateau_hallway_11.add_exit('west',chateau_hallway_10)

chateau_hallway_10.add_exit('east',chateau_hallway_11)
chateau_hallway_10.add_exit('west',chateau_hallway_9)

chateau_hallway_9.add_exit('east',chateau_hallway_10)
chateau_hallway_9.add_exit('west',chateau_hallway_8)

chateau_hallway_8.add_exit('east',chateau_hallway_9)
chateau_hallway_8.add_exit('north',antiques_room)

chateau_hallway_7.add_exit('south',antiques_room)
chateau_hallway_7.add_exit('east',chateau_hallway_6)

chateau_hallway_6.add_exit('north',chateau_hallway_13)
chateau_hallway_6.add_exit('west',chateau_hallway_7)
chateau_hallway_6.add_exit('east',chateau_staircase_landing)

chateau_hallway_5.add_exit('north',chateau_hallway_14)
chateau_hallway_5.add_exit('east',chateau_hallway_15)
chateau_hallway_5.add_exit('west',chateau_hallway_4)

chateau_hallway_4.add_exit('east',chateau_hallway_5)
chateau_hallway_4.add_exit('east',chateau_staircase_landing)

chateau_hallway_3.add_exit('south',chateau_sitting_room)
chateau_hallway_3.add_exit('west',chateau_lavatory)
chateau_hallway_3.add_exit('north',chateau_parlor)

chateau_hallway_2.add_exit('south',chateau_parlor)
chateau_hallway_2.add_exit('west',chateau_pantry)

chateau_hallway_1.add_exit('south',chateau_dining_hall_1)
chateau_hallway_1.add_exit('east',chateau_kitchen)

driveway.add_exit('south',country_road)
driveway.add_exit('north',gravel_driveway_2)

country_road_4.add_exit('west',darkened_road_2)
country_road_4.add_exit('east',country_road_3)

antiques_room.add_exit('south',chateau_hallway_8)
antiques_room.add_exit('east',unfinished_room)
antiques_room.add_exit('north',chateau_hallway_7)

country_road_3.add_exit('west',country_road_4)
country_road_3.add_exit('east',country_road)

back_lawn_9.add_exit('north',back_lawn_3)
back_lawn_9.add_exit('east',back_lawn)
back_lawn_9.add_exit('west',side_lawn_5)

country_road_2.add_exit('east',darkened_road)
country_road_2.add_exit('west',country_road_1)

back_lawn_8.add_exit('east',side_lawn)
back_lawn_8.add_exit('west',back_lawn)
back_lawn_8.add_exit('north',back_lawn_7)

country_road_1.add_exit('east',country_road_2)
country_road_1.add_exit('west',country_road)

front_lawn_5.add_exit('east',front_lawn_4)
front_lawn_5.add_exit('north',side_lawn_3)

back_lawn_7.add_exit('west',back_lawn_1)
back_lawn_7.add_exit('south',back_lawn_8)
back_lawn_7.add_exit('north',back_lawn_6)

chateau_courtyard.add_exit('west',front_lawn_3)
chateau_courtyard.add_exit('east',front_lawn_1)
chateau_courtyard.add_exit('south',circular_driveway)
chateau_courtyard.add_exit('north',chateau_antechamber)

front_lawn_4.add_exit('east',circular_driveway)
front_lawn_4.add_exit('west',front_lawn_5)
front_lawn_4.add_exit('north',front_lawn_3)

gravel_driveway_2.add_exit('south',driveway)
gravel_driveway_2.add_exit('north',gravel_driveway_1)

back_lawn_6.add_exit('south',back_lawn_7)
back_lawn_6.add_exit('west',back_lawn_5)

back_lawn_5.add_exit('south',old_wooden_shed)
back_lawn_5.add_exit('east',back_lawn_6)
back_lawn_5.add_exit('north',wooded_grove)
back_lawn_5.add_exit('west',back_lawn_4)

back_lawn_4.add_exit('east',back_lawn_5)
back_lawn_4.add_exit('south',back_lawn_3)

side_lawn_5.add_exit('east',back_lawn_9)
side_lawn_5.add_exit('south',side_lawn_4)

chateau_lavatory.add_exit('east',chateau_hallway_3)

chateau_library.add_exit('east',chateau_library_1)
chateau_library.add_exit('west',chateau_hallway_13)

back_lawn_3.add_exit('south',back_lawn_9)
back_lawn_3.add_exit('north',back_lawn_4)
back_lawn_3.add_exit('east',back_lawn_1)

side_lawn_4.add_exit('north',side_lawn_5)
side_lawn_4.add_exit('south',side_lawn_3)

damien.place=side_lawn

damien.edible=1

bnt=inheritance.BFNT("big nasty thing")

bnt.description="This thing is big, and nasty, and horrible, and awful, and evil.  You really wish you weren't looking at it right now."

bnt.place=side_lawn_1


mummy=inheritance.Mummy("mummy")
mummy.place=damien.place

colt=inheritance.Gun("Colt 1911 Semi-Auto")

colt.description="It appears to be a Colt 1911, but it is vague, indistinct, and little more than a blurry smear on reality."

colt.add_synonym("gun")
colt.add_synonym("auto")
colt.add_synonym("semi-auto")
colt.add_synonym("colt")
colt.add_synonym("pistol")
colt.add_synonym("automatic")

bullet=inheritance.Bullet("moldy bullet")
bullet.add_synonym("bullet")
bullet.add_synonym("moldy")
bullet.place=damien.place

bullet=inheritance.Bullet("dented bullet")
bullet.add_synonym("bullet")
bullet.add_synonym("dented")
bullet.place=damien.place

bullet=inheritance.Bullet("rusty bullet")
bullet.add_synonym("rusty")
bullet.add_synonym("bullet")
bullet.place=damien.place

clip=inheritance.Clip("Colt 1911 Clip")
clip.add_synonym("clip")

colt.place=damien.place

clip.place=damien.place

sarcophagus=inheritance.Sarcophagus("Sarcophagus")

sarcophagus.description="An ornately carved stone coffin, lined with small hieroglyphics and symbols."

ford=inheritance.Car("Ford Runabout")

ford.exterior="A rather beat up looking specimen of the Ford Model T Runabout series. It is a blocky, ungainly little car, standing a few feet off the ground on its large spoked wheels, and painted a uniform black like every other motor car Ford has produced in the last ten years. It is an older design, lacking the electric ignition and headlights of more modern vehicles, and has a large socket in the hood for the starter crank. The rear end consists mostly of a rounded trunk hanging over the back wheels, where the driver can store their personal effects. "

ford.interior="The interior of the runabout isn't much more pleasant than the outside, and is similarly colored. Two stiffly upholstered chairs are bolted to the floorboards, sheltered somewhat from the outside by a black canvas roof and a thin, slanted windshield. The brake and gas pedals are located conveniently for the driver, but the steering wheel is mounted quite a bit higher than you'd like, from the end of a long metal rod extending up from deep under the engine."

ford.add_synonym("car")

trunk=inheritance.Trunk("Ford Runabout Trunk")
trunk.add_synonym("trunk")
trunk.add_synonym("ford trunk")

trunk.closed="The back end of the Runabout consists primarily of a lumpy metal trunk suspended over the back wheels. It is currently closed."

trunk.opened="The Runabout's trunk is open, revealing a bare, dirty steel compartment."

trunk.place=ford
ford.place=damien.place

sarcophagus.place=damien.place

translator=inheritance.Translator("leather bound book")

translator.add_synonym("book")
translator.add_synonym("leather book")

translator.description="A large and extremely thick leather bound book, entitled \"A Practical Guide to Egyptian Hieroglyphs, by Lord Rutherford P. Beaucavage, Esquire\". While one of the more massive and unwieldy books you've ever had tthe misfortune to encounter, it appears to be nothing if not comprehensive."

translator.read_text="The manual's innumerable pages are covered in illustrations and notes regarding the strange symbolic language of the egyptians. While some of the illustrations are interesting, this book makes for fairly dry and uninteresting reading, although it would probably be very useful in an attempt to translate hieroglyphics."

translator.place=damien.place

leaflet=inheritance.Leaflet("Letter")
leaflet.place=antechamber_table

leaflet.root.resolve_all()

# damien.place.add_exit('north',ford)
