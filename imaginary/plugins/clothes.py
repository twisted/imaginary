# -*- test-case-name: imaginary.test.test_garments -*-

from imaginary.plugins.quiche import _ObjectPluginHelper

from imaginary import garments

shirtPlugin = _ObjectPluginHelper('shirt', garments.createShirt)
pantsPlugin = _ObjectPluginHelper('pants', garments.createPants)
underwearPlugin = _ObjectPluginHelper('underwear', garments.createUnderwear)
