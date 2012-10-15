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
from datetime import datetime
from datetime import timedelta
import json
import urllib

# google calendar client
import gdata.calendar.client

################################################################################

# right now, just hardcoded
CALENDAR_URL = ("https://www.google.com/calendar/feeds/adicu.com_"
                "tud5etmmo5mfmuvdfb54u733i4%40group.calendar.google.com"
                "/public/full")

# rfc3339 is the time/date format gcal uses
def rfc3339(t):
    '''
    Convert a time struct to an rfc3339 string
    '''
    # ex: 2011-09-03T22:00:00.000-04:00
    st = time.strftime("%Y-%m-%dT%H:%M:%S.000",t)
    st += ("-%02d:00" % time.timezone/3600)
    return st
def cfr3339(s):
    '''
    Convert an rfc3339 string to a time struct
    '''
    # ex: 2011-09-03T22:00:00.000-04:00
    try:
        t = time.mktime(time.strptime(s[0:23], "%Y-%m-%dT%H:%M:%S.000"))
    except ValueError:
        t = time.mktime(time.strptime(s[0:23], "%Y-%m-%d"))
    # probably want to ignore this
    #tz = 3600*int(s[23:26])
    #t += tz
    return time.localtime(t)

cwd = os.path.dirname(os.path.abspath(__file__))

def fetch_events(url=CALENDAR_URL, start_time=None, end_time=None):
    '''
    Init a gdata calendar, get some events from it, and put the events
    in dicts
    '''
    client = gdata.calendar.client.CalendarClient()
    # but only get upcoming events
    if not start_time:
        start_time = time.localtime()
    start_date = "%d-%02d-%02d" % (start_time[0],start_time[1],start_time[2])
    # we need to handle getting upcoming days
    if not end_time:
        end_time = datetime.now() + timedelta(weeks=2)
        end_time = end_time.timetuple()
    end_date = "%d-%02d-%02d" % (end_time[0],end_time[1],end_time[2])
    # build the calendar event query
    query = gdata.calendar.client.CalendarEventQuery()
    query.start_min = start_date
    query.start_max = end_date
    # actually get the feed
    feed = client.get_calendar_event_feed(uri=url, q=query)

    # and put it into a sane structure
    events = [{'id': feed.entry[0].id.text.split('/')[-1],
               'title': event.title.text,
               'datetime': event.when[0].start,
               'description': event.content.text,
               'location': event.where[0].value,}
              for event in feed.entry]
    return events

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
        '''
        Grabs google calendar events and displays them, with links to
        a template pre-populated with the event information
        '''
        events = fetch_events()
        # sort of event time
        events = sorted(events,key=lambda x: time.mktime(cfr3339(x["datetime"])))
        events = [[event, json.dumps(event)] for event in events]
        # grab the front page template from file
        temp = self.env.get_template('front.html')
        return temp.render(events=events)

    @cherrypy.expose
    def event(self, data=''):
        '''
        Serve up json detailing the event
        '''
        event = json.loads(data)
        # and now handle the time stuff
        datetime = cfr3339(event["datetime"])
        date = "%s %s %d" % (time.strftime("%a",datetime), 
                          time.strftime("%b",datetime), datetime[2])
        h = datetime[3] % 12
        if h==0:
            h = 12
        t = "%d %s" % (h, time.strftime("%p",datetime))
        # grab the front page template from file
        d = {
            'tagline': event['title'],
            'description': event['description'],
            'date': date,
            'time': t,
            'location': event['location']
            }
        return json.dumps()

    @cherrypy.expose
    def template(self, style=None):
        '''
        This displays a template filled with dumb values
        '''
        # grab the front page template from file
        if style is None:
            style = 'lolhawk.html'
        temp = self.env.get_template(style)
        return temp.render(static_path = "")

    @cherrypy.expose
    def flyer(self, tagline="", description="", date="", time="",
               location="", format=""):
        '''
        Actually render the pdf from the template html
        '''
        # get the template
        temp = self.env.get_template('lolhawk.html')
        # render template output
        html = temp.render(static_path=cwd+"/static", tagline=tagline,
                           description=description, date=date, time=time,
                           location=location)
        # now, convert it
        ### need to do error handling
        proc = subprocess.Popen([cwd+"/wkhtmltopdf",
                                 "--page-size","Letter",
                                 "-","-"],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                # to get wkhtmltopdf to stop complaining
                                # about a missing libXrender.so.1
                                env={"LD_LIBRARY_PATH":
                                         "%s" % cwd},
                                shell=False)
        outdata, errdata = proc.communicate(input=html)
        cherrypy.log("Outdata: "+str(len(str(outdata))))
        cherrypy.log("Errdata: "+str(errdata))
        if not(errdata is None):
            cherrypy.log("Error: "+errdata)
            return "Error: "+errdata
        cherrypy.response.headers['Content-Type'] = 'application/pdf'
        ### maybe save pdf, also
        return outdata

################################################################################

if __name__ == "__main__":
    # replace this eventually with non-quickstart
    cherrypy.quickstart(Flyer(), '/', 'site.conf')
