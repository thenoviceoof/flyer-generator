#!/usr/bin/env python
################################################################################
# wsgi wrapper for dotcloud

import cherrypy
import flyer

application = cherrypy.tree.mount(flyer.Flyer(), "/")
