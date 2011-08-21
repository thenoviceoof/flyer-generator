#!/usr/bin/python
################################################################################
# First iteration flyer gen
################################################################################

# ZE WEB THINGIE
import cherrypy

# templating engine
import jinja2
from jinja2 import Environment, FileSystemLoader

# utility modules
import os
import subprocess

# cherrypy class
class Flyer():
    def __init__(self):
        self.env = Environment(loader = FileSystemLoader('templates'))
	
	_cp_config = {
        'tools.staticdir.on': True,
        'tools.staticdir.dir' : os.getcwd()
        }
    def index(self):
        # grab the front page template from file
        # replace with FileLoader
        temp = self.env.get_template('front.html')
        return temp.render()
    def render(self, title="", subtitle="", content=""):
        # convert the template
        temp = self.env.get_template('adi-1.html')
        # write it out to a temporary file
        return temp.render(title=title, subtitle=subtitle, content=content)
    def flyer(self, title="", subtitle="", content=""):
        # convert the template
        temp = self.env.get_template('adi-1.html')
        # write it out to a temporary file
        f = open("tmp/adi.html","w")
        f.write(temp.render(title=title, subtitle=subtitle, content=content))
        f.close()
        # now convert it
        subprocess.call([os.getcwd()+"/wkhtmltopdf","tmp/adi.html","tmp/adi.pdf"])
        raise cherrypy.HTTPRedirect("/tmp/adi.pdf")
    index.exposed = True
    render.exposed = True
    flyer.exposed = True

# start the engine on 8080
cherrypy.quickstart(Flyer())
