# -*- test-case-name: imaginary.test.test_text -*-

import sys

from zope.interface import implements

from twisted.cred.portal import IRealm
from twisted.python import util
from twisted import copyright as tcopyright

from axiom.item import Item
from axiom.dependency import dependsOn

from xmantissa.ixmantissa import ITerminalServerFactory
from xmantissa.terminal import ShellAccount
from xmantissa.sharing import asAccessibleTo, itemFromProxy

from imaginary import __version__ as imaginaryVersion
from imaginary import resources
from imaginary.objects import Thing
from imaginary.world import ImaginaryWorld
from imaginary.wiring.terminalui import TextServerBase
from imaginary.wiring.player import Player


class CharacterSelectionTextServer(TextServerBase):
    """
    L{CharacterSelectionTextServer} presents a simple text menu for selecting
    or creating a character and then enters the selected or created character
    into an Imaginary simulation.

    @ivar motd: Some text which will be displayed at connection setup time.

    @ivar role: The L{Role} which will own any new characters created.

    @ivar world: The L{ImaginaryWorld} which the selected character will be
        entered into.

    @ivar choices: A list of L{Thing}s which represent existing characters
        which may be selected.
    """

    motd = file(util.sibpath(resources.__file__, 'motd')).read() % {
        'pythonVersion': sys.version,
        'twistedVersion': tcopyright.version,
        'imaginaryVersion': imaginaryVersion}

    state = 'SELECT'

    def __init__(self, role, world, choices):
        self.role = role
        self.world = world
        self.choices = choices


    def connectionMade(self):
        TextServerBase.connectionMade(self)
        self.terminal.reset()
        self.write(self.motd)
        self.write('Choose a character: \n')
        self.write('  0) Create\n')
        for n, actor in enumerate(self.choices):
            self.write('  %d) %s\n' % (n + 1, actor.name.encode('utf-8')))
        self.write('> ')


    def line_SELECT(self, line):
        which = int(line)
        if which == 0:
            self.write('Name? ')
            return 'USERNAME'
        else:
            return self.play(self.choices[which - 1])


    def play(self, character):
        self.player = Player(character)
        self.player.setProtocol(self)
        self.world.loggedIn(character)
        self._prepareDisplay()
        return 'COMMAND'


    def line_USERNAME(self, line):
        """
        Handle a username supplied in response to a prompt for one when
        creating a new character.

        This will create a user with the name given by C{line}, made available
        to the role indicated by C{self.role}, and entered into play.
        """
        actor = self.world.create(line)
        self.role.shareItem(actor)
        return self.play(actor)



class ImaginaryApp(Item):
    """
    A terminal application which presents an Imaginary game session.
    """
    powerupInterfaces = (ITerminalServerFactory,)
    implements(*powerupInterfaces)

    shell = dependsOn(ShellAccount)

    name = 'imaginary'

    def _charactersForViewer(self, store, role):
        """
        Find the characters the given role is allowed to play.

        This will load any L{Thing}s from C{store} which are shared to C{role}.
        It then unwraps them from their sharing wrapper and returns them (XXX
        there should really be a way for this to work without the unwrapping,
        no?  See #2909. -exarkun).
        """
        characters = []
        things = store.query(Thing)
        actors = asAccessibleTo(role, things)
        characters.extend(map(itemFromProxy, actors))
        return characters


    def buildTerminalProtocol(self, viewer):
        """
        Create and return a L{TextServer} using a L{Player} owned by the store
        this item is in.

        This implementation is certainly wrong.  It probably reflects some
        current limitations of Mantissa.  Primarily, the limitation is
        interaction between different stores, in this case a user store and an
        application store.
        """
        # XXX Get the Imaginary app store.  Eventually this should just be
        # self.store.  See #2908.
        imaginary = IRealm(self.store.parent).accountByAddress(u'Imaginary', None).avatars.open()

        role = viewer.roleIn(imaginary)
        characters = self._charactersForViewer(imaginary, role)

        world = imaginary.findUnique(ImaginaryWorld)
        return CharacterSelectionTextServer(role, world, characters)
