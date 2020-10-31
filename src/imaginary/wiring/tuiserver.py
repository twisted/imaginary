# -*- test-case-name: imaginary.test -*-

from twisted.conch.insults import insults, window

from imaginary.wiring import faucet

connections = []

class WidgetyServer(insults.TerminalProtocol):
    width = 80
    height = 24

    name = 'nobody'

    def _draw(self):
        self.window.draw(self.width, self.height, self.terminal)

    def _redraw(self):
        self.window.redraw(self.width, self.height, self.terminal)

    def connectionMade(self):
        self.things = []
        self.faucet = faucet.Faucet(self.lineReceived)
        self.window = window.TopWindow(self._draw)
        self.window.addChild(self.faucet)
        self.terminalSize(self.width, self.height)
        connections.append(self)
        for c in connections:
            self.things.append(c)
            if c is not self:
                c.newThing(self)
        self.faucet.setThings('\n'.join([o.name for o in self.things]))
        self.faucet.setPlace('Yo welcome to Faucet demo.  Tab to switch '
                             'between input and output.  "set name <name>" '
                             'to give yourself a name.  Anything else to '
                             'chat it up.')

    def connectionLost(self, reason):
        connections.remove(self)
        for c in connections:
            c.thingGone(self)

    def terminalSize(self, width, height):
        self.width = min(80, width)
        self.height = min(24, height)
        self.terminal.eraseDisplay()
        self._redraw()

    def keystrokeReceived(self, keyID, modifier):
        self.window.keystrokeReceived(keyID, modifier)
        self._draw()

    def newThing(self, thing):
        self.things.append(thing)
        self.faucet.setThings('\n'.join([o.name for o in self.things]))
        self._draw()

    def thingGone(self, thing):
        self.things.remove(thing)
        self.faucet.setThings('\n'.join([o.name for o in self.things]))
        self._draw()

    def message(self, who, what):
        self.faucet.addOutputLine(who.name + ':' + what)
        self._draw()

    def lineReceived(self, line):
        if line.startswith("set name "):
            self.name = line[9:]
            for c in connections:
                c.faucet.setThings('\n'.join([o.name for o in c.things]))
                c._draw()
        else:
            for c in connections:
                c.message(self, line)
