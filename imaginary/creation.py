# -*- test-case-name: imaginary.test.test_create -*-
"""
This module contains code associated with creating objects in game.
"""

from zope.interface import implements

from twisted import plugin

import imaginary.plugins

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


def createCreator(*enhancements):
    """
    Create and return a function which can create objects in the game world.

    This is a utility function to make it easy to define factories for certain
    configurations of power-ups to be used with Imaginary.  It doesn't do
    anything magical; you can replicate its effects simply by writing a
    function that calls L{Enhancement.createFor} on the set of L{Enhancement}s.
    L{createCreator} exists because you will frequently need to do that, and it
    can be tedious.

    @param enhancements: The arguments to this function are a list of 2-tuples
        of (L{Enhancement}-subclass, keyword arguments to that class's
        constructor).

    @return: a function which takes keyword arguments that will be passed on to
        L{objects.Thing}'s constructor, and will return a L{Thing} with an
        instance of each class in C{enhancements} installed, via C{createFor},
        on it.

    @rtype: L{Thing}
    """
    def create(**kw):
        o = objects.Thing(**kw)
        for enhancementClass, enhancementKeywords in enhancements:
            enhancementClass.createFor(o, **(enhancementKeywords or {}))
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
    phrase = language.Noun(creation).nounPhrase()
    return events.Success(
        actor=player,
        target=creation,
        actorMessage=language.Sentence(["You create ", phrase, "."]),
        targetMessage=language.Sentence([player, " creates you."]),
        otherMessage=language.Sentence([player, " creates ", phrase, "."]))


class Create(NoTargetAction):
    """
    An action which can create items by looking at the L{IThingType} plugin
    registry.
    """
    expr = (Literal("create") +
            Optional(White() +
                     (Literal("an") | Literal("a") | Literal("the")).setResultsName("article")) +
            White() +
            targetString("typeName") +
            White() +
            Literal("named") +
            White() +
            targetString("name") +
            Optional(White() +
                     restOfLine.setResultsName("description")))

    def do(self, player, line, typeName, name, description=None, article=None):
        """
        Create an item, and notify everyone present that it now exists.
        """
        if not description:
            description = u'an undescribed object'
        for plug in getPlugins(IThingType, imaginary.plugins):
            if plug.type == typeName:
                proper = (article == "the")
                o = plug.getType()(store=player.store, name=name,
                                   description=description, proper=proper)
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




def listThingTypes():
    """
    Return a list of C{unicode} strings each of which gives the name of a type
    which can be created with the create command.
    """
    return sorted([type.type for type in getPlugins(IThingType, imaginary.plugins)])



class ListThingTypes(NoTargetAction):
    """
    An action which tells the invoker what thing types exist to be created with
    the L{Create} command.
    """
    expr = Literal("list thing types")

    def do(self, player, line):
        """
        Tell the player the thing types which exist.
        """
        events.Success(
            actor=player.thing,
            actorMessage=[(t, "\n") for t in listThingTypes()]).broadcast()
