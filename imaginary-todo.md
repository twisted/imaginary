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

The problem with doing it this way is that LookAt then needs to know explicitly
about clothing, and about carrying, and if it needs to know about clothing and
carrying then how is it to be extended to support things like carrying
invisible, enchanted objects, and so on?  The idea that something you're
carrying would be hidden in some way (simple example; you're holding a gun
behind your back) really ought to be expressable without monkeying with the
core logic in language.py every time.

Actually there's a more serious problem.

We pass 'observer' to the 'vt102' method of DescriptionConcept, but this comes
from the 'visualize' method of Thing directly.

Which means DescriptionConcept has a *direct* reference to the name, the
description, the exits, and the IDescriptionContributor powerups present on
itself.

So if I 'look at' you, I call a method on you and get "your" description, as
tailored to me; but by that point, the ability to customize that description
has been curtailed significantly, because the only consideration of the *whole
path* that goes between the "looker" and the "lookee" is done in the CanSee
delgating retriever.  In other words, if I can see you, I can see _all_ of you.

Better would be to do the visibility query in the action, then do the
UI-centric assembly and ordering of strings on the results of doing that.

Notes:

- clothing actions can't find clothing that you're wearing, because the
  clothing system currently conceals everything; _DisregardYourWearingIt needs
  to change (possibly die?)
- most actions need to not use CanSee; they need to use a smarter retriever.
  For example: you have a concealed gun; you know what it is, you can reach for
  it. But you can't see it.  *Other* people probably can't reach for it (unless
  they pass a Perception check of course)
- we need to implement the logic that actually orders and presents stuff in
DescriptionWithContents.
- DescriptionWithContents is actually DescriptionWithContext
- reinstate location support (add exits logic back)
    - this should be accomplished by making exits visible things that get
      included in the query result as items in their own right (maybe they
      already are in the graph somewhere, just need to make sure)


# Punch List #

- remove visualize() everywhere, the only method on IVisible should be visualizeWithContents

- similarly, remove DescriptionConcept, the only object that performs this task
should be DescriptionWithContents
