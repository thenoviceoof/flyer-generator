#!/usr/bin/env python
##################################################
# A first example
##################################################

import cherrypy

class HelloWorld():
    def index(self):
        return "hello world"
    index.exposed = True

cherrypy.quickstart(HelloWorld())
