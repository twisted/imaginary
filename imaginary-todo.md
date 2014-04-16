# What To Do To Fix Visibility In Imaginary #

The bug is: the model of the world (as implemented by the current garments and
containment system - but not, say, Idea or Thing) is not sufficiently
expressive because you can find the same thing through a couple of different
paths, but you don't know what those paths are about (for example, you don't
know that the garment path is a dude wearing a thing).

Garments need to express that this is a link to a thing that is being worn.  It
should express this by adding an annotation to the links from the garments to
the clothes.  It already sort of does this!  But what it does is that it puts a
_`DisregardYourWearingIt` annotation (an opaque `IElectromagneticMedium`
annotation) that prevents anyone from seeing the clothes via the link that
comes from you-as-a-`Container` (by being an `ILinkAnnotator`), and then
*re-creates* all of those links by being an `ILinkContributor`.

However, what it should be doing instead is it should *stop* being an
`ILinkContributor`, since all the links it wishes to annotate are those that
already exist from the container; it can (and should) do what it needs to do by
being an `ILinkAnnotator`.  It should then *always* introduce a new `IWornBy`
annotation that indicates who is wearing the clothing, and only introduce an
(opaque) `IElectromagneticMedium` onto the *obscured* elements of clothing.

Then, just for code clarity reasons, the implementation of `LookAround` should
be modified to be a thin wrapper (perhaps even just a parse expression?) for
"look at here".

`LookAt` should then have a bunch of extra logic.  It needs to first accumulate
all the things that you *can* see by looking at a particular thing, then make
some decisions about how to present the things that you can see.

