# Copyright 2009 Divmod, Inc.  See LICENSE for details
# -*- test-case-name: imaginary.test.test_illumination -*-
"""
This module contains code that administrators can invoke to directly manipulate
Things.

@see: L{imaginary.iimaginary.IManipulator}, the interface which this module
    provides implementations of.
"""

from zope.interface import implements

from twisted.python.components import registerAdapter

from epsilon.structlike import record

from axiom.item import Item
from axiom.attributes import reference

from imaginary.iimaginary import IManipulator, IThing
from imaginary.objects import LocationLighting, Thing

from imaginary.eimaginary import ActionFailure
from imaginary.events import ThatDoesntWork



class NonManipulator(record("thing")):
    """
    A L{NonManipulator} is the ephemeral actor, implementing the responses that
    normal users will see when they attempt to perform administrative actions.
    """

    implements(IManipulator)

    def setIllumination(self, candelas):
        """
        Don't actually set the illumination of the manipulator.
        """
        raise ActionFailure(ThatDoesntWork(
            actor=self.thing,
            actorMessage=
            "You are insufficiently brilliant to do that directly."))


registerAdapter(NonManipulator, IThing, IManipulator)



class Manipulator(Item):
    """
    A L{Manipulator} is the actor for actions which can directly change the
    properties of objects in an Imaginary world.
    """
    implements(IManipulator)

    powerupInterfaces = [IManipulator]

    thing = reference(allowNone=False,
                      doc="""
                      The L{IThing} for the underlying actor.
                      """,
                      reftype=Thing, whenDeleted=reference.CASCADE)

    def setIllumination(self, candelas):
        """
        Set the ambient illumination of this L{Manipulator}'s C{thing}'s
        location.

        @return: the location's previous ambient illumination in candelas.
        """
        ll = self.thing.store.findOrCreate(
            LocationLighting,
            lambda ll: self.thing.location.powerUp(ll),
            thing=self.thing.location)
        oldCandelas = ll.candelas
        otherMessage = None
        ll.candelas = candelas
        return oldCandelas



