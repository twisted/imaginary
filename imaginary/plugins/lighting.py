
from imaginary.objects import LightSource
from imaginary.creation import CreationPluginHelper, createCreator

theTorchPlugin = CreationPluginHelper(
    u"torch", createCreator((LightSource, {"candelas": 80})))
