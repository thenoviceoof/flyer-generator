#!/usr/bin/python
################################################################################
# First iteration flyer gen
################################################################################

# ZE WEB THINGIE
import cherrypy

# templating engine
import jinja2
from jinja2 import Template

# utility modules
import os
import subprocess

class Flyer():
    _cp_config = {
        'tools.staticdir.on': True,
        'tools.staticdir.dir' : os.getcwd()+'/tmp'
        }
    def index(self):
        # grab the front page template from file
        # replace with FileLoader
        f = open("static/front.html")
        s = f.read()
        temp = Template(s)
        return temp.render()
    def flyer(self, title="", subtitle="", content=""):
        # convert the template
        f = open("static/adi-1.html")
        s = f.read()
        f.close()
        temp = Template(s)
        # write it out to a temporary file
        f = open("tmp/adi.html","w")
        f.write(temp.render(title=title, subtitle=subtitle, content=content))
        f.close()
        # now convert it
        subprocess.call([os.getcwd()+"/wkhtmltopdf","tmp/adi.html","tmp/adi.pdf"])
        raise cherrypy.HTTPRedirect("/adi.pdf")
    index.exposed = True
    flyer.exposed = True

# start the engine on 8080
cherrypy.quickstart(Flyer())
