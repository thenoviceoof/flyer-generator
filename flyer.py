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
    @cherrypy.expose
    def index(self):
        # grab the front page template from file
        # replace with FileLoader
        temp = self.env.get_template('front.html')
        return temp.render()
    
    @cherrypy.expose
    def render(self, title="", subtitle="", content=""):
        # convert the template
        temp = self.env.get_template('adi-1.html')
        # write it out to a temporary file
        return temp.render(title=title, subtitle=subtitle, content=content)
    
    @cherrypy.expose
    def flyer(self, title="", subtitle="", content=""):
        # convert the template
        temp = self.env.get_template('adi-1.html')
        # write it out to a temporary file
        html = temp.render(title=title, subtitle=subtitle, content=content)
        # now convert it
        proc = subprocess.Popen([os.getcwd()+"/wkhtmltopdf","-","-"],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        outdata, errdata = proc.communicate(input=html)
        cherrypy.response.headers['Content-Type'] = 'application/pdf'
        return outdata

if __name__ == "__main__":
    # start the engine on 8080
    cherrypy.quickstart(Flyer(), '/', 'site.conf')
