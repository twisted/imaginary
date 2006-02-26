
from imagination import simulacrum, architecture, containment, building, scrutinize
from imagination.templates import basic
from imagination.text.english import INoun

room = basic.Room.fill(
    INoun,
    name="Alpha",
    description=("Not much to see here.  Bare concrete walls and "
                 "floor glare in the light of a single exposed "
                 "bulb in the center of the ceiling.")).new()

room2 = basic.Room.fill(
    INoun,
    name="Omega",
    description=("This room is rather cramped. Illumination comes "
                 "from the room to the south.")).new()

room3 = basic.Room.fill(
    INoun, name="The Abyss",
    description="All dark and shit.").new()

room4 = basic.Room.fill(
    INoun,
    name="Gamma",
    description=("This room is visible through a transparent door.")).new()

passage = basic.Portal.apply(architecture.IExit, 'between', room, room2).fill(
    INoun, name="Fancy Passageway Between Alpha and Omega").new()

door = basic.Door.fill(
    INoun, name="Door"
    ).apply(architecture.IExit, 'between', room3, room3).new()

door2 = basic.Door.fill(INoun, name="glass door"
                        ).fill(
    architecture.IExit, transparent=True).apply(
    architecture.IExit, 'between', room, room4).new()


book1 = basic.Book.fill(containment.ILocatable, location=room).fill(
    INoun,
    name="fancy book",
    description="_Simulation And Simulacra_, by Baudrillard.").new()

book2 = basic.Book.fill(containment.ILocatable, location=room).fill(
    INoun,
    name="trashy book",
    description="A Piers Anthony paperback novel.").new()

book3 = basic.Book.fill(containment.ILocatable, location=room3).fill(
    INoun,
    name="dark book",
    description="_Necronomicon_, by Abdul Alhazred").new()

book4 = basic.Book.fill(containment.ILocatable, location=room4).fill(
    INoun, name="tantalizing book", description=
    "You can see this book, but you can't pick it up without opening that glass door.").new()

ActorTemplate = basic.Actor.fill(
    containment.ILocatable,
    location=room)
