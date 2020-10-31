# -*- test-case-name: imaginary.test.test_garments -*-

from imaginary.creation import CreationPluginHelper
from imaginary.garments import (createShirt, createPants, createUnderwear)

shirtPlugin = CreationPluginHelper('shirt', createShirt)
pantsPlugin = CreationPluginHelper('pants', createPants)
underwearPlugin = CreationPluginHelper('underwear', createUnderwear)
