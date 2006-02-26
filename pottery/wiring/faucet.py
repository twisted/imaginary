
from twisted.conch.insults import window

class Faucet(window.ContainerWidget):
    _outputText = ''
    _toBottom = False

    def __init__(self, onInput):
        window.ContainerWidget.__init__(self)

        self._inputCallback = onInput

        place = window.TextOutputArea()
        things = window.TextOutputArea()
        place_things = window.HBox()
        place_things.addChild(window.Border(place))
        place_things.addChild(window.Border(things))

        output = window.TextOutputArea()
        scrolledOutput = window.ScrolledArea(output)
        input = window.TextInput(78, self._onInput)
        output_input = window.VBox()
        output_input.addChild(scrolledOutput)
        output_input.addChild(input)

        detail_interaction = window.VBox()
        detail_interaction.addChild(place_things)
        detail_interaction.addChild(output_input)

        self.addChild(detail_interaction)

        self._place = place
        self._things = things
        self._output = output
        self._scroll = scrolledOutput
        self._input = input

    def render(self, width, height, terminal):
        self._input.maxwidth = width - 2
        if self._toBottom:
            self._toBottom = False
            n = self._outputText.count('\n')
            m = ((height - 4) / 2 - 1)
            self._scroll._viewport.yOffset = max(0, n - m)

        return window.ContainerWidget.render(self, width, height, terminal)

    def _onInput(self, text):
        self._input.setText('')
        self.addOutputLine('> ' + text)
        self._inputCallback(text)

    def setPlace(self, text):
        self._place.setText(text)

    def setThings(self, text):
        self._things.setText(text)

    def addOutputLine(self, text):
        self._outputText += text + '\n'
        self._output.setText(self._outputText)
        self._toBottom = True
