#### we kickin' it old skool! anybody remember source persistence?
#### once datamatic works perfectly this may go away
#### in the meantime, consider it motivation
#### http://library.samford.edu/

from reality.things import Movable, Player
from reality.ambulation import Exit, Door, Room
from reality.conveyance import Portable
from reality.tools import addTodo, describe, simpleTRServer
from reality.text.common import IDescribeable

### first floor! http://library.samford.edu/kiosk/maps/firstfloor.htm

_ = antechamber = Room("Antechamber")
# http://library.samford.edu/images/welcome2.jpg
describe(_,"A wide room whose red granite floor is interrupted by a pair of steps midway between the three sets of double doors leading outside to the south and the matching six windowed doors leading inwards. Plaques line the east and west walls, and a bronze bust of the library's namesake occupies a prominent pedestal in the center of the room.")
addTodo(_,"get plaque text")
addTodo(_,"add special blocked-passage text for south")
addTodo(_,"add mechanism for blocked-passage text")

bust = Movable("Bust")
describe(bust, "A bronze likeness of the head of Maj. Harwell Goodwin Davis. The years have not been kind to him; his nose and forehead are a much shinier yellow, evidence of the idle hands of tne students that pass through here.")

bustInscription = "The inscription on the pedestal describes Maj. Davis' decoration for bravery in the campus uprisings of 1939, where with the assistance of Librarian Mabel Willoughby, he held off the enemy for nearly a week from their position in the BV shelves before being relieved by a team of cataloguers from Atlanta."

addTodo(_,"Make antechamber description-fragment for bust be attached to bust instead")
addTodo(_,"add 'read' verb")
bust.moveTo(antechamber)

# http://library.samford.edu/images/circ_desk2.jpg
_ = frontOfLibrary = Room("Front of Library")
describe(_,"Brass and frosted-glass domes hang low from the paneled ceiling to diffuse light upon a blue carpet covered with a bold white and red floral patten. Immediately to the north stands the Grand Staircase. Passages on either side of the stairs may be reached to the northeast and northwest. South lies the exit through the security doors; to either side are stairwells. East and west lead to other wings of the library.")
addTodo(_,"Make observable not always generate exits display, or rework descriptions to exits")
Exit("EXIT","south",frontOfLibrary,antechamber)

_ = landing = Room("Landing")
describe(_, "A black marble landing, with brass handrails. Stairs lead down to the first floor; upwards lies only a dense gray fog.")
Exit("EXIT","down",landing,frontOfLibrary)
Exit("EXIT","south",landing,frontOfLibrary)

_ = westWing = Room("West Wing")
describe(_,"Square pillars frame this burgundy-carpeted area between large windows to the south and the circulation desk to the north. The wing continues to the west. To the south is a stairwell, and east is the library entrance.")
addTodo(_,"Add couch/table group, pair of study tables")

_ = westWing2 = Room("West Wing")
describe(_,"Square pillars frame this burgundy-carpeted area between large windows to the south and the multimedia shelves to the north. A pair of TV rooms are to the west and northwest. The wing continues to the east.")
addTodo(_,"add 6 study tables")
addTodo(_,"make description less copy&paste?")
addTodo(_,"add TV rooms")
Exit("EXIT","east",westWing2,westWing)

_ = multimediaShelves = Room("Multimedia Shelves")
describe(_,"Nine low shelves full of VHS tapes fill this space between a TV room to the west and the circulation desk to the east. Study tables lie to the south.")
addTodo(_,"make shelves work")
Exit("EXIT","south",multimediaShelves,westWing2)

_ = microfilm = Room("Microfilm alcove")
describe(_,"Metal cabinets for microfilm and microfiche storage, and their attendant readers, line the walls in this area. The northwest corner is taken up by an electrical closet. A gate in the circulation desk lies to the east.")
Exit("EXIT","south",microfilm,multimediaShelves)

_ = electricalCloset = Room("Electrical Closet")
describe(_,"Grey cinder block and concrete floor limn this small closet space, lit by a single fluorescent bulb.")
addTodo(_,"Hey, radix - put cool stuff in here")
Exit("EXIT","northwest",microfilm,electricalCloset)

_ = circDesk = Room("Circulation Desk")
describe(_,"The circulation desk wraps around this work area on the east, west, and south sides. Papers and unshelved books lie on carts here, as well as the desk itself. Gaps in the counter contain gates to the south, northeast, and west. The circulation librarian's office is north.")
Exit("EXIT","south",circDesk, westWing)
Exit("EXIT","west",circDesk, multimediaShelves)

_ = circOffice = Room("Circulation Librarian's Office")
describe(_,"Just a boring office. Desk, chair, computer, papers, etc. I dont know why you even bothered coming in here, really.")
Exit("EXIT","south",circOffice, circDesk)

_ = westOfStairs = Room("West of Stairs")
describe(_,"This passage runs between the black marble expanse of the circulation desk's counter to the west and the staircase to the east.")
Exit("EXIT","southeast",westOfStairs,frontOfLibrary)
Exit("EXIT","southwest",westOfStairs,westWing)

_ = eastWing = Room("East Wing")
describe(_,"Nine tall bookshelves run the length of this wing, east to west, housing the A through G sections. Offices lie to the north; couches and tables line the south wall, under the windows.")
addTodo(_,"research detail, figure out bookshelves, add offices")
Exit("EXIT","west",eastWing,frontOfLibrary)

_ = eastOfStairs = Room("East of Stairs")
describe(_,"A couch and a pair of chairs are arranged around a coffee table here.")
addTodo(_,"make this not suck!")
Exit("EXIT","southwest",eastOfStairs,frontOfLibrary)
Exit("EXIT","southeast",eastOfStairs,eastWing)

_ = westStairwell = Room("West Stairwell")
describe(_,"Institutional-green wall tiles and a greenish-blue terrazzo floor lend a vaguely submarine air to this stairwell. Doors lie to the east and north. As for stairs, you can go up, or west and down.")
addTodo(_,"dont forget the intercom!")
Exit("EXIT","northwest", westStairwell, westWing)
Exit("EXIT","northeast",westStairwell,frontOfLibrary)
Exit("EXIT","north",westStairwell,westOfStairs)
Exit("EXIT","east",westStairwell,antechamber,twoway=0)

_ = eastStairwell = Room("East Stairwell")
describe(_,"Institutional-green wall tiles and a greenish-blue terrazzo floor lend a vaguely submarine air to this stairwell. Doors lie to the west and north. As for stairs, you can go up, or east and down.")
Exit("EXIT","northwest",eastStairwell,frontOfLibrary)
Exit("EXIT","northeast",eastStairwell,eastWing)
Exit("EXIT","west",eastStairwell,antechamber, twoway=0)

_ = behindStairs = Room("Behind Stairs")
describe(_,"Six catalog computers line a table here. A copier sits at the south wall. Elevators lie to the west. The library's back door is to the west. North is a shelf of books for sale, and access to the periodicals section.")
addTodo(_,"this description sucks and doesn't match the topology very well")
Exit("EXIT","southeast",behindStairs,eastOfStairs)
Exit("EXIT","southwest",behindStairs,westOfStairs)

_ = periodicals = Room("Periodicals Archive")
describe(_,"A couple shelves running east-west are visible here, but beyond that, the other shelves fade into a dense gray fog.")
Exit("EXIT","south",periodicals,behindStairs)

bob = Player("Patron")
bob.moveTo(antechamber)
application = simpleTRServer(bob, debug=1, web=1)

if __name__ == '__main__':
    import sys
    from twisted.python import log
    log.startLogging(sys.stdout, 0)
    application.run()
