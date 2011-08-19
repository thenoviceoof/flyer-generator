#!/usr/bin/python
################################################################################
# First iteration flyer gen
################################################################################

import cherrypy

import jinja2
from jinja2 import Template

import os
import subprocess

class Flyer():
    _cp_config = {
        'tools.staticdir.on': True,
        'tools.staticdir.dir' : os.getcwd()+'/tmp'
        }
    def index(self):
        f = open("static/front.html")
        s = f.read()
        temp = Template(s)
        return temp.render()
    def flyer(self, title="", subtitle="", content=""):
        f = open("static/adi-1.html")
        s = f.read()
        f.close()
        temp = Template(s)
        # write it out
        f = open("tmp/adi.html","w")
        f.write(temp.render(title=title, subtitle=subtitle, content=content))
        f.close()
        # now convert it
        subprocess.call([os.getcwd()+"/wkhtmltopdf","tmp/adi.html","tmp/adi.pdf"])
        raise cherrypy.HTTPRedirect("/adi.pdf")
    index.exposed = True
    flyer.exposed = True

cherrypy.quickstart(Flyer())
