
Imaginary is an experimental simulation-construction toolkit.

Be warned!  We aren't kidding when we say "experimental".  Many features are
not implemented yet and documentation is incomplete.  We think there are some
pretty cool ideas here, but if you are intending to use this system, be
prepared to participate heavily in its development.

This document is mainly concerned with getting an Imaginary server up and
running, to the point where you can edit the code and see things change.  Some
familiarity with Python, Twisted, Nevow, Axiom, and Mantissa are all helpful,
but we will try to make sure they aren't really required just to get started.

While we have tried to make it possible to get a taste of what is possible
here, if you want to make any serious progress, you will want to join the IRC
channel "#imagination" on chat.freenode.net and start asking questions.  If you
are curious about what needs to be done, have a look here:

    http://tinyurl.com/2tuo9o

The first step in configuring a new installation of Imaginary will normally be
creating a new Mantissa database.

(This is assuming you have already set up Combinator, installed Twisted, and
all necessary Divmod dependencies. If not, see
http://divmod.org/trac/wiki/CombinatorTutorial for more information.)

First run the following command:

      axiomatic mantissa

And answer the prompts appropriately. Please take note of the new password you
enter for the "admin" user, as you will need it in a few steps.

This should create a directory called "mantissa.axiom", containing the server
for a web interface that will allow you to install "offerings" (plugins for
Mantissa, in this case, Imaginary), create users, and grant them
privileges. You can start this webserver with the following command: (the -n
option will run it in the foreground on the current terminal)

    axiomatic start -n

You should now be able to access this server at http://localhost:8080 in your
web browser.

Click the "Sign In" link in the upper right hand corner, and log in as "admin"
with the password you chose previously while configuring Mantissa.

If you logged in successfully, you should now be presented with a list of
"offerings" that can be installed. Click on "Imaginary" to install it; Note
that you will most likely see an error window appear when you do this, but it's
purely cosmetic, so just click the "Close this window" link and ignore it.

Next, click on the purple Divmod icon in the upper left corner of the window to
open the menu, and then click the "Admin" option and then the "Ports" sub-menu.

In the "New Service" area at the bottom of the screen, enter the port number
you'd like to use for Imaginary (such as 4023), choose "Telnet" in the
"Protocol Factory" pulldown, leave the rest of the options untouched for now,
and click the "createPort" button. You will hopefully be presented with a green
confirmation dialog to confirm your success. Hooray!

Ideally, you will now be able to telnet into your Imaginary server. In a new
terminal, telnet to localhost on the port you've chosen for Imaginary. For
example:

         telnet localhost 4023

At the Imaginary username prompt, choose a new username (e.g. not "admin") and
enter a new password. You will be prompted as to whether you would like to
create this new user (answer (y)es), and then confirm your new password.

You should now be logged into Imaginary, and see a row of dashes along the
bottom of the display.  To confirm your new MUDness, try typing "look" and hit
enter; You should see some indication of the generic place that you are in, the
available exits, and other players in the area, though initially you won't see
much more than "[The Place]".

You can enter "actions" for a list of actions, and use "help" along with one of
them ("help dig") for specific information on how to use them. You can even log
in via other telnet windows, create additional accounts, and interact with your
initial user (for example, beating them to death with "hit").

When you've tired of self-abuse, you can stop your Imaginary server by hitting
control-c in the terminal where you ran "axiomatic start -n".
