
                   **** READ THIS FIRST ***
                   **** VERY IMPORTANT! ***

The examples contained in this directory are awful, terrible code.  They are
provided for _HISTORICAL INTEREST ONLY_.  Most depend on incredibly ancient
versions of other software which are not included, conflict with reasonable
modern versions of similar software, and no effort has been made to update them
or even verify that they are complete or still run.  Many of them come from
projects whose documentation has been lost or destroyed or was never written in
the first place.  The copyright on many of them is highly dubious and many
original contributors are not available for comment.

The primary purpose of this is to share some of our inside jokes with the
world, and provide examples of the kinds of things we have tried to do in these
games in the past.  Ideally we would like to re-implement all the unfinished
functionality here on top of modern infrastructure, and go far beyond the false
starts and half-measures contained in this directory.

Some of this code was written when the authors were obnoxious teenagers with no
sense of software security issues or good software development practices such
as testing.  A few of these packages are even now known to contain ****SEVERE
SECURITY PROBLEMS**** including crashes, deadlocks, and ****REMOTE ARBITRARY
CODE EXECUTION****.


             **** THIS CODE WAS NOT WRITTEN BY DIVMOD ****
 **** DO NOT EXPECT ANY HELP OR SUPPORT WITH ANY OF THESE PACKAGES ****
  **** DO NOT ATTEMPT TO COMPILE, RUN OR USE ANY OF THIS SOFTWARE ****
                **** YOU HAVE BEEN WARNED!!!!!!! ****


That said, Imaginary is a framework with a long and storied history.

Its current incarnation (and attendant momentum) is derived from a prototype
MUD codebase called "pottery", which owes much to JP Calderone.  However,
pottery (and therefore Imaginary) is the latest in a very long series of
frameworks attempting to deal with complex simulation integration issues.

The timeline is approximately as follows:

 * 1999: the original "Reality Pump" java game server and "Reality Faucet"
   client, hereinafter referred to as "TRJ".  The saga of this codebase begins
   even earlier, in about 1997, when Glyph learned Java and started writing
   this on his mac in his spare time.  This framework was originally developed
   in support of the game "Divunal", a sprawling multiplayer text-based
   adventure.  The final version was written in equal parts by by Glyph, Tenth
   (AKA David Sturgis), and James Knight, with the map comprising contributions
   from almost a dozen other contributors.  Divunal's design has since
   undergone a major overhaul and it's barely recognizable.  However, certain
   stylistic elements of the original and references to the original exist in
   the present-day documentation.  TRJ here includes the final, raw attempt at
   a C/GTK+ implementation of the client, as that was perceived by the authors
   at the time to be far harder to implement, but superior UI experience.

   Divunal was extremely hard to implement, so in TRJ's last days, another,
   smaller, self-contained game (designed to be played by small groups of
   players rather than an MMP) was developed as a technology demo, a
   lovecraftian survival-horror game called "Inheritance".  This made a poor
   online demo as the ambiance was ruined by people wandering around and
   talking about java programming, so a small, but extremely campy
   demonstration area was developed called simply "TRDemo".

 * 2000: Uncomfortable with limitations of Java on client and server, both on
   TRJ and at work, Glyph learns Python, and nearly completely rewrites both
   TRJ's client and server in less than a week.  The result is the unreleased
   predecessor to the present-day Twisted framework, available in the "tr2"
   directory here.  This included a "reality" package, as well as a protocol
   called "gloop", replete with RPC bindings for Java for legacy integration so
   that the existing Swing-based Faucet client could be used.  However, Glyph
   rapidly discovered PyGTK and rewrote the faucet from scratch, obviating the
   need for a cross-language interoperable RPC, and "gloop" was unrecognizable
   before the first release of Twisted.

   tr2 also included a nearly fully functional rewrite in Python of Divunal and
   Inheritance, as well as several tools for reading the Java version's
   mapfiles.

 * 2001: the original version of Twisted included a "twisted.reality" package -
   not included here because it was extremely similar to the following
   "reality" package...

 * 2002: the "reality" package -- twisted.reality after it was disembodied from
   Twisted.  This was the beginning of a long winter for Imaginary's ancestry -
   almost no work was done after it was removed from Twisted.  Versions of
   TRDemo, Inheritance, and Divunal were updated to work with the new naming
   scheme, but little code was added.

 * 2003: the resurrection of that package, "NewReality" or sometimes simply
   "capital-R-Reality", which attempted a much grander simulation kernel.  JP
   Calderone's SOpera, or "Space Opera" was an attempt at a game based on this
   codebase.  Due to limited time and lofty ambitions, it begins to resemble a
   research project more than a functional codebase, Allen Short writes a
   paper, "Twisted Reality: a Flexible Framework for Virtual Worlds", which
   details some of the new directions being taken here.  JP Calderone
   implements SOpera based on this codebase.

 * 2004: "Imagination" casts off much of the cruft that had accumulated in
   NewReality, and expresses the simulation-integration concepts covered in
   Allen's paper much more concisely in code, but with no supporting examples
   and little documentation.  This resulted in a brilliant but fantastically
   obscure simulation kernel, so unbearably complex that nothing recognizable
   as an online world was ever implemented to use it.  It does contain a TRDemo
   which almost worked.

 * 2005: JP Calderone tries for several weeks to get Imagination to do various
   simple game-related tasks, and gives up in frustration, rewriting a simpler
   version of the same concepts in an entirely new codebase called "pottery".
   One distinguishing feature of Pottery is extensive test coverage, which
   allows it to keep making progress despite the usual pattern of months at a
   time of no activity.

 * 2006: Pottery gains Axiom support, and becomes Divmod Imaginary.
   Imagination, and all its predecessors, are officially deprecated.

 * 2007: Robot warriors enslave the human race in giant code factories, leaving
   tinkering with Imaginary the last refuge of the terminally insane.

