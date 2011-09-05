#!/usr/bin/python
################################################################################
# flyer.py generator
################################################################################

# ZE WEB THINGIE
import cherrypy

# templating engine
import jinja2
from jinja2 import Environment, FileSystemLoader

# utility modules
import os
import subprocess
import time
import json
import urllib

# google calendar client
import gdata.calendar.client

################################################################################

# right now, just hardcoded
calendar_url = "https://www.google.com/calendar/feeds/adicu.com_tud5etmmo5mfmuvdfb54u733i4%40group.calendar.google.com/public/full"

# rfc3339 is the time/date format gcal uses
def rfc3339(t):
    """Convert a time struct to an rfc3339 string"""
    # ex: 2011-09-03T22:00:00.000-04:00
    st = time.strftime("%Y-%m-%dT%H:%M:%S.000",t)
    st += ("-%02d:00" % time.timezone/3600)
    return st
def cfr3339(s):
    """Convert an rfc3339 string to a time struct"""
    # ex: 2011-09-03T22:00:00.000-04:00
    t = time.mktime(time.strptime(s[0:23], "%Y-%m-%dT%H:%M:%S.000"))
    # probably want to ignore this
    #tz = 3600*int(s[23:26])
    #t += tz
    return time.localtime(t)

cwd = os.path.dirname(os.path.abspath(__file__))

# cherrypy class
class Flyer():
    # config options
    _cp_config = {
        'tools.staticdir.on': True,
        # this is very unsafe, will have to fix this eventually
        'tools.staticdir.dir' : cwd+"/static/"
        }

    def __init__(self):
        # no sense in 
        self.env = Environment(loader = FileSystemLoader('templates'))
	
    @cherrypy.expose
    def index(self):
        """Grabs google calendar events and displays them, with links to
        a template pre-populated with the event information"""
        # grab google calendar events
        client = gdata.calendar.client.CalendarClient()
        # but only get upcoming events
        t = time.localtime()
        start_date = "%d-%02d-%02d" % (t[0],t[1],t[2])
        # we need to handle getting upcoming days
        et = time.localtime(time.mktime((t[0],t[1],t[2]+14, 0,0,0, 0,0,-1)))
        end_date = "%d-%02d-%02d" % (et[0],et[1],et[2])
        # build the calendar event query
        query = gdata.calendar.client.CalendarEventQuery()
        query.start_min = start_date
        # actually get the feed
        feed = client.get_calendar_event_feed(uri=calendar_url, q=query)
        # and put it into a sane structure
        events = [{"title":event.title.text,
                   "datetime": event.when[0].start,
                   "description": event.content.text,
                   "location": event.where[0].value,
                   }
                  for event in feed.entry]
        events = [[event, json.dumps(event)] for event in events]
        # grab the front page template from file
        temp = self.env.get_template('front.html')
        return temp.render(events=events)

    @cherrypy.expose
    def template(self):
        """This displays a template filled with dumb values"""
        # grab the front page template from file
        temp = self.env.get_template('lolhawk.html')
        return temp.render(static_path = "",
                           tagline="Tagline", description="Description",
                           date="Today", time="9PM",
                           location="Location")
    @cherrypy.expose
    def event(self, data=""):
        """This displays a template populated with event data from gcal"""
        # convert it back from uri format
        event = json.loads(data)
        # and now handle the time stuff
        datetime = cfr3339(event["datetime"])
        date = "%s %d" % (time.strftime("%b",datetime), datetime[2])
        h = datetime[3]%12
        if h==0:
            h = 12
        t    = "%d %s" % (h, time.strftime("%p",datetime))
        # grab the front page template from file
        temp = self.env.get_template('lolhawk.html')
        return temp.render(static_path = "",
                           tagline=event["title"],
                           description=event["description"],
                           date=date, time=t,
                           location=event["location"])

    @cherrypy.expose
    def flyer(self, tagline="", description="", date="", time="",
               location="", format=""):
        """Actually render the pdf from the template html"""
        # get the template
        temp = self.env.get_template('lolhawk.html')
        # render template output
        html = temp.render(static_path=cwd+"/static", tagline=tagline,
                           description=description, date=date, time=time,
                           location=location)
        # now, convert it
        ### need to do error handling
        proc = subprocess.Popen([cwd+"/wkhtmltopdf","-","-"],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        outdata, errdata = proc.communicate(input=html)
        cherrypy.response.headers['Content-Type'] = 'application/pdf'
        ### maybe save pdf, also
        return outdata

################################################################################

if __name__ == "__main__":
    # replace this eventually with non-quickstart
    cherrypy.quickstart(Flyer(), '/', 'site.conf')
