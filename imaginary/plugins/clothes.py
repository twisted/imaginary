# -*- test-case-name: imaginary.test.test_garments -*-

from imaginary import action, garments

shirtPlugin = action.ObjectPluginHelper('shirt', garments.createShirt)
pantsPlugin = action.ObjectPluginHelper('pants', garments.createPants)
underwearPlugin = action.ObjectPluginHelper('underwear', garments.createUnderwear)
