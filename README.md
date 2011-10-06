 Flyer-Generator
================================================================================

ABOUT
================================================================================

It's a web-interface for creating flyers quickly and easily. 

User Stories
--------------------------------------------------------------------------------

Use story #1:
 - Person is doing workshop, wants flyer
 - selects event from calendar
 - tweaks the tagline
 - hits the big red button
 - downloads awesome pdf

Use story #2:
 - wants to make an event not on the calendar
 - fill out details
 - hit the big red button
 - download pdf


INSTALL
================================================================================

You have to get it from github:

    git clone git://github.com/thenoviceoof/flyer-generator.git

You'll need these python libraries:

 * Cherrypy
 * Jinja2
 * Google Calendar <http://code.google.com/p/gdata-python-client/downloads/list>

And you also need in the top level of the git repo (next to flyer.py):

 * A copy of wkhtmltopdf from <http://code.google.com/p/wkhtmltopdf/>
 * A copy of site.conf: if you don't have one, just
       touch site.conf
 * A tmp directory (run `mkdir tmp`)


DOTCLOUD INSTALL
================================================================================

So you want to upload this to dotcloud?

 * Sign up for a dotcloud account
 * Install the dotcloud client side CLI
 * Register your API key with your client
 * Find a copy of libXrender.so.1 for linux - under Ubuntu 11.04, this sits under

    /usr/lib/x86_64-linux-gnu/libXrender.so.1

   Copy it here, so that wkhtmltopdf actually runs under dotcloud

 * Then, do this:

    dotcloud push --all flyergen .

 * The --all option pushes your wkhtmltopdf along with everything else


USAGE
================================================================================

To run:

    ./flyer.py


Real Usage
--------------------------------------------------------------------------------

To write your own templates:

  * Be sure to target webkit, since that's what wkhtmltopdf uses


BUGS
================================================================================

Bugs aren't cool, telling us about bugs is. Report issues/suggestions on github:

https://github.com/thenoviceoof/flyer-generator/issues


