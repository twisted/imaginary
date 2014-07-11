.. image:: https://travis-ci.org/twisted/imaginary.png
  :target: https://travis-ci.org/twisted/imaginary

.. image:: https://coveralls.io/repos/twisted/imaginary/badge.png
  :target: https://coveralls.io/r/twisted/imaginary

Imaginary is an experimental simulation-construction toolkit.

Be warned!  We aren't kidding when we say "experimental".  Many features are
not implemented yet and documentation is incomplete.  We think there are some
pretty cool ideas here, but if you are intending to use this system, be
prepared to participate heavily in its development.

Imaginary can be used to build both single-player interactive fiction, text
adventures for small groups of friends, or large multiplayer games.

To get it installed, you will need to install some dependencies.  Due to a
series of unfortunate events, you need to run ``pip`` manually a couple of
times, rather than simply installing the package directly.  (We're working on
fixing this.)

.. code-block:: console

   $ pip install twisted
   $ pip install epsilon

At this point, you may just do:

.. code-block:: console

   ~/Projects/Imaginary$ pip install . ExampleGame

... but if you want to develop Imaginary itself (and you probably do, because
as we explained above, it's still in a very early state), you can set up an
*editable* install with:

.. code-block:: console

   ~/Projects/Imaginary$ pip install -e . -e ExampleGame

To get started, first you'll need a world file.  There's an example world in
``doc/examples/example_world.py``.

To load that world, run

.. code-block:: console

   $ python -m imaginary docs/examples/example_world.py

A "world" for a single-player game is simply a Python file with a function
called ``world`` in it, that returns an instance of an ``ImaginaryWorld``.  The
example contains several useful items, and until there is more thorough
documentation you should be able to construct your own example by modifying it.

If you're interested in setting up a multi-player Imaginary server, see
``MULTIPLAYER.rst``.
