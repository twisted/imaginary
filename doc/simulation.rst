Simulation in Imaginary
=======================

Overview
--------

The core functionality provided by Imaginary is a generalized framework for implementing domain-specific simulations.
One of the primary goals of this framework is to make it easier for different simulation systems to co-exist and even interact.
Several programming tools have been selected to achieve this goal:

  - Explicit interfaces so boundaries between different simulations are well-defined
  - Composition to aggregate simulation behaviors to make this aggregation possible dynamically

Speaking in slightly more concrete terms, Imaginary implements a very generic graph representation and tools for traversing that graph.
The graph is used to represent the simulation and simulation behavior is mostly implemented in terms of different kinds of graph traversal.

Graph Nodes
-----------

Roughly speaking, a node in the simulation graph corresponds to something that exists in the simulation.
Put another way, nodes are nouns.
During traversal, nodes are represented by instances of `imaginary.idea.Idea`.
Some examples of what you might represent with an `Idea` are typical game entities, such as people, places, vehicles, garments, or food.
An `Idea` itself is simply a point in the graph, though, and implements no logic directly.
In other words, you don't need to subclass `Idea` at any point; when you want to implement a portion of a simulation, you write your own class and attach it to an `Idea`.
An `Idea` may also represent something more abstract, such as a character's state of mind.
For example, in a game like Call of Cthulu, a player may need to calm their character down to retain sanity points, like so:

.. code::

   The corners of this room are unsettling.
   The hairs on the back of your neck bristle as you feel an odd sort of pressure.
   {Sanity: 4}
   > examine corners
   The otherworldly geometry of the corners is too horrible to contemplate.
   You break out in a cold sweat.
   {Sanity: 3}
   > use hideous dagger on corners
   Your hands shake too violently to weild the dagger.
   You have dropped the dagger.
   You have dropped your rope.
   You can feel your mind going.
   {Sanity: 1}
   > reflect on my childhood
   You center yourself by recalling pleasant memories of afternoons by the seashore.
   Your hands shake somewhat less.
   {Sanity: 2}

In this transcript, "my childhood" is a simulated concept which the ``reflect`` verb acts upon, and, as such, must be represented by an `Idea`.
However, this particular `Idea` has no simulated *physical* representation.

Things
''''''

The representation of an object's physical presence in Imaginary is an instance of `imaginary.objects.Thing`.
`Thing` is a persistent representation of a physical object which is stored in the underlying Axiom database.
`Things` represent the physical presence of *any* kind of object, including players, tools, clothing, decorations, environmental features, and so on.

The simulation graph doesn't directly contain `Thing` instances, though: they are always wrapped up in an `Idea`.
Importantly, an `Idea` may be created without a `Thing` instance to support creating parts of the simulation graph without relying on state persisted in a database.

Delegates
'''''''''

Whatever an `Idea` is wrapped around -- be it a `Thing` instance or something non-persistent, generated on the fly -- is called the idea's *delegate*.
While `Idea` contains all of the generalized simulation graph logic and implements traversal and other features, the delegate is what actually ties this together with the implementations for domain-specific simulations.

Graph Edges
-----------

Edges are just as important as nodes in the simulation graph.
An edge represents a way in which one node can be reached from another node.
During traversal, edges are represented by instances of `imaginary.idea.Link`.
Some examples of what you might represent with a `Link` are the containment relationship between a person and the location where that person exists, a box and each item contained by that box, or the relationship between a location and an exit from that location.

Traversal
---------

Most of the interesting things that can happen in the simulation involve traversing the simulation graph in one or more ways.
For example, when a player observes their surroundings using the `look` action, the graph is traversed starting at the `Idea` representing the player's location and stopping at any edge that leads to a node that is not in the same location.

Apart from `Idea`\ s and `Link`\ s, traversal of the simulation graph involves several more objects:

  - a retriever, an object which controls how to interpret `Idea`\ s encountered in the graph and also when to stop traversal
  - any number of annotators, objects which can alter the nature of `Link`\ s along the traversal path

The entrypoint for graph traversal is `Idea.obtain`.
This begins traversal from the `Idea` it is called on.
The retriever to use for the traversal is accepted as the only argument.
The return value is an iterator of things found by the traversal, as interpreted by the retriever.

Traversal Path
''''''''''''''

The traversal path, mentioned in passing above, is an important concrete concept in the traversal process.
As `Idea`\ s are found by graph traversal a sequence of `Link`\ s leading from the `Idea` where traversal began up to each of those found `Idea`\ s.
This sequence is represented explicitly as an `imaginary.idea.Path` instance and is made available to the retreiver used for the traversal.
It is important to remember that the same `Idea` might be found by the traversal process via *multiple* paths.
For example, consider a box with two holes in it or a mirror reflecting an image of other objects.
The IRetriever_ section below goes into more details about how a `Path` is useful.

ILinkContributor
''''''''''''''''

Traversal finds `Link`\ s in the graph using implementations of `imaginary.iimaginary.ILinkContributor`.
In addition to a delegate, an `Idea` also consists of a list of providers of this interface.
Each is consulted in turn to contribute to the `Link`\ s that connect that `Idea` to other `Idea`\ s.
The use of an arbitrary number of link contributors is related directly to the choice to use composition in the implementation of simulations in Imaginary.
Consider that a bare object with no interesting behavior is probably linked only to its location.
If the object is then turned into a container, it gains links to all of its contents.
And if the object is again changed, perhaps turned from a mundane container into a magic portal, it gains a link to the location to which it has become a portal.
The same physical object can take on all of these behaviors in turn merely by having the list of `ILinkContributor`\ s on its `Idea` changed.
`Thing` supports persistent, data-driven changes to the list of `ILinkContributor`\ s using Axiom's *powerup* functionality.
`Idea`\ s created some other way or with some other delegate may have their own schemes for determining the `ILinkContributor` list.

IRetriever
''''''''''

The `IRetriever` passed to `Idea.obtain` plays an intimate role in the traversal and its results.

`shouldKeepGoing`
~~~~~~~~~~~~~~~~~

The `shouldKeepGoing` method provides the only means by which a traversal will ever complete (short of visiting every single `Idea` in the simulation graph).
This method is called with a `Path` instance and must return `True` if traversal should continue further down that `Path` or `False` if it should not.
One use of this feature is to simply limit traversals to the immediate physical area of the `Idea` where traversal begins.
This is implemented by `imaginary.idea.Proximity`: this `IRetriever` can be composed with any other `IRetriever` and automatically adds a distance limit to the traversal.
It passes other method calls through to the `IRetriever` with which it is composed.
Another example is `imaginary.idea.CanSee`.
This `IRetriever` allows traversal to continue until encountering an `ILink` which is opaque to visible light.
Like `Proximity` it is composable and implements the rest of the methods of `IRetriever` as pass-through methods that call the composed retriever's method.

`retrieve`
~~~~~~~~~~

Each `Path` through the simulation graph considered during a call to `Idea.obtain` is passed to `IRetriever.retrieve`.
This method is responsible for returning the object that will become an element in the generator returned by `Idea.obtain`.
It may also eliminate a `Path` from the result by returning `None`.
`imaginary.idea.ProviderOf` is one of the few `IRetriever` implementations currently included with Imaginary.
This implementation is initialized with an interface.
Its `retrieve` method adapts the *delegate* of the last `Idea` in the `Path` to that interface (if the adaption fails, it removes the `Path` from the result).
This is convenient for simulation systems that want to deal with a particular aspect of the behavior of objects discovered during traversal.
For example, the *look at* action uses a `ProviderOf` instance so that it only need consider objects that can be seen - objects that are adaptable to `imaginary.iimaginary.IVisible`.

Annotations
'''''''''''

ILinkAnnotator
~~~~~~~~~~~~~~

An `Idea` has a collection of `ILinkAnnotator`\ s which are each called upon to yield annotations on links.
Each `ILinkAnnotator` may annotate either links *from* an `Idea` (those which have a *source* of that `Idea`) or *to* an `Idea` (those which have a *target* of that `Idea`).
`Thing` uses this same interface as a powerup interface; any `ILinkAnnotator` powerups become `ILinkAnnotator`\ s for that `Thing`\ 's idea.

These annotations can then be accessed by the `Path.of` method.

It is then the responsibility of any action which must consider the way in which an `Idea` was accessed to honor the annotators.

For example, consider combat damage and armor.
The `Hit` action needs to resolve a target, then do damage to that target.
Armor needs to be able to mitigate that damage somehow, and in the case of armor enchanted with Thorns, it needs to be able to *reverse* that damage.

This would be represented by a link annotation.

Unlike other simulation systems, Imaginary does not provide totally general-purpose action-processing hooks.
Actions may be physical (like `Hit`) or purely mental (like the earlier example about ``reflect on my childhood``).
Therefore, it doesn't make sense to have a generic "before you take an action" event, so Thorns can't be implemented as such a hook; the combat system needs to explicitly account for things like damage mitigation and reversal.

ILocationLinkAnnotator
~~~~~~~~~~~~~~~~~~~~~~

This is a powerup interface used with `Thing` which allows a container to add annotations to the links of all of the things it contains.

This doesn't change the way annotators and annotations work at the basic level.
Rather, it provides an implementation convenience for effects which are meant to apply to everyone and everything in a certain area.

For example, consider a burning room.
The intent is to simulate the walls, floor, and ceiling having caught fire.
Using this powerup interface, a single annotator can apply annotations to links between all of the `Idea`\ s in the room.
