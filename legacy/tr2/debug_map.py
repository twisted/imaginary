#!/usr/bin/env python
import sys
from pdb import run
from twisted import reality
from twisted.ui import ConsoleIntelligence
ci=ConsoleIntelligence()
from cPickle import load

reality.default_reality=load(open(sys.argv[1]))
player=reality.default_reality[sys.argv[2]]
player.intelligence=ci
# run('ci.run_input()')

commands = ['$from divunal.builder import PlayerCreationMachine',
			'$x=PlayerCreationMachine("x")',
			'$x.place=self.place',
			'$x.create()',
			'take x',
			'drop x']

run('map(player.execute,commands)')
