# -*- test-case-name: imaginary.test.test_create -*-

"""
Imaginary-supplied plugins for simple built-in functionality.
"""

from imaginary.creation import CreationPluginHelper, createCreator

thingPlugin = CreationPluginHelper("thing", createCreator())
