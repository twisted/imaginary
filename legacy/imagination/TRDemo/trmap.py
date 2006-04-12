
from twisted.python import components

from imagination.text import english
from imagination.templates import basic
from imagination import simulacrum, containment

from templates import RoomTemplate, TrinketTemplate
import actions

demoMetaRoom = RoomTemplate.fill(
    english.INoun,
    name='Demo',
    description=('This is the Twisted Reality Demo Center.  '
                 'Thanks for playing!  This meta-room is accessible '
                 "only to authors, and will give you a bird's eye "
                 "view of what's going on in the game.  You can "
                 'look at any room, and even interact with objects '
                 'in those rooms, although that may produce bizarre '
                 'effects.  See the development documentation for '
                 'more details.')
    ).fill(containment.ILocatable, location=None).new()


DemoRoomTemplate = RoomTemplate.fill(containment.ILocatable, location=demoMetaRoom)

startRoom = DemoRoomTemplate.fill(
    english.INoun,
    name='Twisted Reality Corporate Demo Center',
    description=('A spacious, open room with a high, arched ceiling.  '
                 'The walls are an almost gleaming, immaculate white, '
                 'contrasting sharply with the polished black marble '
                 'floor.  The room becomes wider as it continues on to '
                 'the north, and is dotted with bright green potted '
                 'plants at regular intervals.  The southern wall is '
                 'covered by a ten-foot-tall billboard labelled with '
                 'the legend: "\'look at board\' for help!"')
    ).new()

ActorTemplate = basic.Actor[
    actions.IWindActor: actions.Winder,
    actions.IDrinkActor: actions.Drinker,
    actions.IPushActor: actions.Pusher,
    actions.ITypeActor: actions.Typer,
].fill(containment.ILocatable, location=startRoom)

demoRoom = DemoRoomTemplate.fill(
    english.INoun,
    name='Demo Center Waiting Room',
    description=('This is a comfortable waiting room with high-backed '
                 'leather chairs and wooden-paneled walls.  There is a '
                 'solid oak coffee table here, with a tasteful gold '
                 'inlay.  To the northeast, there is a gold-lined '
                 'archway leading into a room with white walls and a '
                 'black floor.')
    ).new()

DemoTrinketTemplate = TrinketTemplate.fill(
    containment.ILocatable,
    location=demoRoom)

DemoTrinketTemplate.fill(
    english.INoun,
    name='bauble',
    description='omg I can not write this'
    ).new()

DemoTrinketTemplate.fill(
    english.INoun,
    name='billboard',
    description=('This is a ten-foot-tall gleaming white billboard, with '
                 'clear, black, sans-serif writing that begins in huge '
                 'three-foot-tall letters and proceeds down to a small '
                 'ten-point font.  It reads:'
                 '\n\n'
                 '"Welcome to the Twisted Reality Demo Center!  A few basic '
                 'commands that will guide you through this magical land of '
                 'corporation fun are: '
                 '\n\n'
                 'LOOK: this lets you look at stuff.  Try it on objects '
                 'both in the room\'s description and in the object-list '
                 'in the upper right hand corner.'
                 '\nSAY: This command is macro-bound to your \' key.  You '
                 'can use this to interact with other players.'
                 '\n\n'
                 'GO: This lets you move.  You can also use the numeric '
                 'keypad (with NUM-LOCK on) to move in the cardinal and '
                 'secondary compass directions - also, 0 is \'up\' and 5 is '
                 '\'down\'.'
                 '\n\n'
                 'SMILE: it\'s polite.  You can just SMILE or SMILE AT someone.'
                 '\n\n'
                 'These are not all of the verbs you can use, by any stretch of '
                 'the imagination.  Some situations may also call for OPEN, CLOSE, '
                 'TURN or SIT.  If the game says something snide to you, it\'s '
                 'likely that the verb you\'re looking for doesn\'t work in that '
                 'context.  Another good rule to keep in mind is that the parser will '
                 'understand you in the form: "verb [direct-object] [preposition '
                 'indirect-object] so sentences like "slowly use the tongs to give '
                 'bob the fish", "north, please" or "I\'d sure like to go north right '
                 'now, wouldn\'t you?" are not going to work quite right.  Try instead '
                 '"give fish to bob with tongs" or "go north".'
                 '\n\n'
                 'Thanks for playing, and we hope you enjoy the demo!'),
    ).new()
RoachTemplate = DemoTrinketTemplate[
    actions.IWindTarget: actions.Roach]

RoachTemplate.fill(
    english.INoun,
    name="brass cockroach",
    description=('A small mechanical cockroach, intricately designed with '
                 'all of the parts and details of a real insect, made '
                 'entirely of polished brass.  There is a small hexagonal '
                 'keyhole between two of the plates of its thorax.')
    ).new()

DemoTrinketTemplate[
    actions.IWindTool: actions.Winder
].fill(
    english.INoun,
    name="small brass key"
).new()

DemoTrinketTemplate[
    (actions.IPushTarget, actions.IDrinkTarget): actions.Fountain
].fill(
    english.INoun,
    name="fountain"
).new()
    
DemoTrinketTemplate[
    actions.IPushTarget: actions.GenderChanger
].fill(
    english.INoun,
    name="gender changer"
).new()

DemoTrinketTemplate[
    (actions.IPushTarget, actions.ITypeTarget): actions.Register
].fill(
    english.INoun,
    name="register",
).new()
