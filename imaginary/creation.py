# -*- test-case-name: imaginary.test.test_create -*-
"""
This module contains code associated with creating objects in game.
"""

from zope.interface import implements

from twisted import plugin

from axiom.dependency import installOn

import imaginary

from imaginary import objects
from imaginary import events
from imaginary import language

from imaginary.iimaginary import IThingType
from imaginary.eimaginary import ActionFailure, DoesntFit

from imaginary.action import NoTargetAction, insufficientSpace
from imaginary.action import targetString

from imaginary.pyparsing import Literal, White, Optional, restOfLine


def getPlugins(iface, package):
    """
    Get plugins. See L{twisted.plugin.getPlugins}.

    This is in place only so the tests specifically for creation can replace
    it.  Please use L{twisted.plugin.getPlugins} instead.
    """
    # XXX the tests should not need to do that, make it per-instance or
    # something...
    return plugin.getPlugins(iface, package)


def createCreator(*powerups):
    """
    Create and return a function which can create objects in the game world.

    This is a utility function to make it easy to define factories for certain
    configurations of power-ups to be used with Imaginary.  It doesn't do
    anything magical; you can replicate its effects simply by writing a
    function that instantiates various powerups and calls L{installOn}
    repeatedly with those created powerups.  L{createCreator} exists because
    you will frequently need to do that, and it can be tedious.

    @param powerups: The arguments to this function are a list of 2-tuples of
    (powerup-class, keyword arguments to powerup-class constructor).

    @return: a function which takes keyword arguments that will be passed on to
    L{objects.Thing}'s constructor, and will return a Thing with an instance of
    each class in 'powerups' installed on it.
    """
    def create(**kw):
        store = kw['store']
        o = objects.Thing(**kw)
        for pup, pupkw in powerups:
            installOn(pup(store=store, **pupkw or {}), o)
        return o
    return create


class CreationPluginHelper(object):
    """
    A helper for creating plugins for the 'Create' command.

    Create will search for L{IThingType} plugins and allow users to
    instantiate a new L{objects.Thing} using the one with the name which
    matches what was supplied to the action.
    """

    implements(plugin.IPlugin, IThingType)

    def __init__(self, typeName, typeObject):
        """
        @type typeName: C{unicode}
        @param typeName: A short string describing the kind of object this
        plugin will create.

        @param typeObject: A factory for creating instances of
        L{objects.Thing}.  This will be invoked with four keyword arguments:
        store, name, description, and proper.  See attributes of
        L{objects.Thing} for documentation of these arguments.
        """
        self.type = typeName
        self.typeObject = typeObject


    def getType(self):
        return self.typeObject



def creationSuccess(player, creation):
    """
    Create and return an event describing that an object was successfully
    created.
    """
    return events.Success(
        actor=player,
        target=creation,
        actorMessage=language.Sentence([creation, " created."]),
        targetMessage=language.Sentence([player, " creates you."]),
        otherMessage=language.Sentence([player, " creates ", creation, "."]))


class Create(NoTargetAction):
    """
    An action which can create items by looking at the L{IThingType} plugin
    registry.
    """
    expr = (Literal("create") +
            White() +
            targetString("typeName") +
            White() +
            targetString("name") +
            Optional(White() +
                     restOfLine.setResultsName("description")))

    def do(self, player, line, typeName, name, description=None):
        """
        Create an item, and notify everyone present that it now exists.
        """
        if not description:
            description = u'an undescribed object'
        for plug in getPlugins(IThingType, imaginary.plugins):
            if plug.type == typeName:
                o = plug.getType()(store=player.store, name=name,
                                   description=description, proper=True)
                break
        else:
            raise ActionFailure(
                events.ThatDoesntMakeSense(
                    actor=player.thing,
                    actorMessage=language.ExpressString(
                        u"Can't find " + typeName + u".")))

        creationSuccess(player.thing, o).broadcast()
        try:
            o.moveTo(player.thing)
        except DoesntFit:
            raise insufficientSpace(player.thing)



