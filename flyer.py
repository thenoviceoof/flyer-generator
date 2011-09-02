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

################################################################################

# cherrypy class
class Flyer():
    # config options
    _cp_config = {
        'tools.staticdir.on': True,
        # this is very unsafe, will have to fix this eventually
        'tools.staticdir.dir' : os.getcwd()+"/static/"
        }

    def __init__(self):
        self.env = Environment(loader = FileSystemLoader('templates'))
	
    @cherrypy.expose
    def index(self):
        # grab the front page template from file
        # replace with FileLoadern
        temp = self.env.get_template('front.html')
        return temp.render()
    
    @cherrypy.expose
    def render(self, title="", subtitle="", content=""):
        # convert the template
        temp = self.env.get_template('adi-1.html')
        # write it out to a temporary file
        return temp.render(title=title, subtitle=subtitle, content=content)

    # experimental: shoving the lolhawk stuff into this
    @cherrypy.expose
    def lolhawk(self):
        # grab the front page template from file
        temp = self.env.get_template('lolhawk.html')
        return temp.render(static_path = "",
                           tagline="Tagline", description="Description",
                           date="Today", time="9PM",
                           location="Location", contact="Contact")
    @cherrypy.expose
    def render_lolhawk(self, tagline="", description="", date="", time="",
                       location="", contact="", format=""):
        # get the template
        temp = self.env.get_template('lolhawk.html')
        # render template output
        html = temp.render(static_path=os.getcwd()+"/static", tagline=tagline,
                           description=description, date=date, time=time,
                           location=location, contact=contact)
        # now, convert it
        ### need to do error handling
        proc = subprocess.Popen([os.getcwd()+"/wkhtmltopdf","-","-"],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        outdata, errdata = proc.communicate(input=html)
        cherrypy.response.headers['Content-Type'] = 'application/pdf'
        ### maybe save pdf, also
        return outdata
    
    @cherrypy.expose
    def flyer(self, title="", subtitle="", content=""):
        # convert the template
        temp = self.env.get_template('adi-1.html')
        # render template output
        html = temp.render(title=title, subtitle=subtitle, content=content)
        # now convert it
        proc = subprocess.Popen([os.getcwd()+"/wkhtmltopdf","-","-"],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        outdata, errdata = proc.communicate(input=html)
        cherrypy.response.headers['Content-Type'] = 'application/pdf'
        return outdata

if __name__ == "__main__":
    # start the engine on 8080
    # if you don't have a site.conf, just do a `touch site.conf`
    cherrypy.quickstart(Flyer(), '/', 'site.conf')
