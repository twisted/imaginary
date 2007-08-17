
from imaginary.creation import CreationPluginHelper
from examplegame.mice import createMouse, createHiraganaMouse

mouse = CreationPluginHelper(u'mouse', createMouse)
hiraganaMouse = CreationPluginHelper(u'hiragana mouse', createHiraganaMouse)
