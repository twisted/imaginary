# -*- test-case-name: imaginary.test -*-
# Copyright (c) The Authors.
# See LICENSE for details.

"""
Functionality related to seeing and being seen.
"""

from zope.interface import implementer
from imaginary.idea import Proximity
from imaginary.iimaginary import IRetriever
from imaginary.iimaginary import ILitLink
from imaginary.idea import Path
from imaginary.iimaginary import IThing
from imaginary.idea import CanSee
from imaginary.idea import DelegatingRetriever
from imaginary.idea import ProviderOf
from imaginary.iimaginary import IVisible

@implementer(IRetriever)
class _PathSatisfiesPredicate(DelegatingRetriever):
    """
    Retrieve the paths that satisfy the given predicate.
    """

    def __init__(self, predicate, retriever):
        """
        Create a L{PathSatisfiesPredicate} with the given predicate.
        """
        self.predicate = predicate
        super(_PathSatisfiesPredicate, self).__init__(retriever)


    def retrieve(self, path):
        """
        Return the suitable object described by C{path}, or None if the path is
        unsuitable for this retriever's purposes.  Any path for which
        C{predicate} returns L{True} will be retrieved.

        @param path: See L{IRetriever.retrieve}
        """
        if self.predicate(path):
            return path



def visualizations(viewingThing, predicate, withinDistance=3.0):
    """
    C{viewingThing} wants to look at something; it might know the name, or
    description, or placement of "something".  For example, if a player types
    C{"look at elephant"}, then "something" would be defined as "anything named
    'elephant'".

    L{visualizations} takes the thing doing the looking and a function to
    determine if a path to a thing-being-looked-at qualifies as, for example, a
    thing that C{viewingThing} might refer to as 'elephant' called
    C{predicate}, which takes a L{Path} whose target is something which may or
    may not be interesting, and returns L{True} if so and L{False} if not.

    L{visualizations} locates all of the options (for example, if there are
    multiple elephants, you might get multiple results) and returns a L{list}
    of L{IConcept} providers, each of which represents the description of one
    thing-that-can-be-looked-at which L{viewingThing} can see.

    @param viewingThing: The observer
    @type viewingThing: L{IThing}

    @param predicate: A callable which takes a L{Path} and returns L{True} if
        the targe tof that L{Path} is relevant as a focus of this
        visualization, L{False} otherwise.
    @type predicate: L{callable} taking L{Path} returning L{bool}

    @param withinDistance: Only search within the distance of this given number
        of meters.
    @type withinDistance: L{float}

    @return: a L{list} of L{IConcept}
    """
    # First, get all the things meeting the predicate's criteria that we can
    # see.
    startPaths = viewingThing.obtainOrReportWhyNot(
        _PathSatisfiesPredicate(
            predicate,
            Proximity(withinDistance,
                      CanSee(ProviderOf(IVisible),
                             viewingThing)
            )
        )
    )

    choices = []

    # Now, for each of those "visual targets", we need to gather a set of
    # related objects which might show up in its description.
    for startPath in startPaths:
        visualTargetIdea = startPath.links[-1].target

        # Now we need to apply lighting to the path, getting the IVisible (or
        # modified IVisible, if it's too dark to see it properly) that we are
        # in fact looking at.
        visible = _lightingApplied(startPath)
        if visible is not None:
            # For each visual target, query outwards from *it*, not the
            # observer, looking for other objects which may be "part" of that
            # visual target - visible along with it.  This is stuff like the
            # contents of a container, the exits from a room, et cetera.  This
            # obtain() begins from the visual target rather than the player,
            # because some of the paths the player wants to see may fold back
            # on themselves.  For example, if a player is seated on a table,
            # and there is a gun next to them on the table and they look at the
            # room, they should still be able to see the gun as part of the
            # room, despite the fact that the path goes player -> chair -> room
            # -> chair -> gun.  The chair -> room -> chair path would be
            # disallowed by the cycle-detection in obtain().
            #
            # Use of a distance predicate here is a temporary solution.  It is
            # necessary to avoid collecting all the objects in the entire
            # simulation graph but it doesn't necessarily set the bounds of
            # this obtain call correctly.  How much stuff around the target is
            # worth returning here?  How much is relevant to the thing you're
            # looking at?  Mere proximity doesn't really answer that question.
            # At some point, we should figure out what rules we want to use to
            # define "related to" for the purposes of the vision system and
            # replace this Proximity with them somehow.
            subPaths = visualTargetIdea.obtain(
                _PathSatisfiesPredicate(
                    lambda p: True,
                    Proximity(withinDistance, ProviderOf(IVisible))
                )
            )

            # However, since visual obstructions which may obscure or transform
            # the appearance of the objects related to the object being
            # observed begin from the viewer, and *not* from the object being
            # observed, we must re-introduce the viewer.
            paths = [
                Path(links=startPath.links + subPath.links)
                for subPath in subPaths

                # Hide the viewer from themselves - random objects that you
                # look at shouldn't function as mirrors.
                if not subPath.targetAs(IThing) is viewingThing
            ]
            paths.sort(key=lambda x: len(x.links))
            paths = list(path for path in paths if _isIlluminated(path))
            choices.append(visible.visualizeWithContents(paths))
    return choices



def _isIlluminated(path):
    """
    Is the given path illuminated?

    This presently checks for L{ILitLink} annotations.

    @param path: The path to check for illumination.
    @type path: L{Path}

    @return: L{True} if the path is illuminated (is bright enough to be
        visually identified) L{False} otherwise.
    @rtype: L{bool}
    """
    litlinks = list(path.of(ILitLink))
    if not litlinks:
        return True
    for litlink in litlinks:
        if litlink.isItLit(path):
            return True
        else:
            return False



def _lightingApplied(path):
    """
    Treat the given path as a path identifying a visual object, and apply
    lighting to it.

    @param path: The path to the visual object to which to apply lighting.
        L{IVisible} annotations along this path may influence the lighting
        results.
    @type path: L{Path}

    @return: an L{IConcept} provider which can render an appropriate
        description for the target of the given C{path}, dependent upon the
        level of lighting conferred by the given C{path}; or L{None} if the
        target of the given path does not adapt to L{IVisible}, or if the given
        path is not L{illuminated <_isIlluminated>}.
    @rtype: L{IConcept} or L{types.NoneType}
    """
    thing = path.targetAs(IVisible)
    if not _isIlluminated(path):
        return None
    litPath = list(path.of(ILitLink))
    if not litPath:
        return thing
    litThing = list(path.eachTargetAs(IVisible))[-1]
    thing = litPath[-1].applyLighting(litThing, thing, IVisible)
    return thing



