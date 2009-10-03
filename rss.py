# what rss.py
# who  nate smith
# when oct 2009
# why  python script for use in independent study

import pyext
import urllib2
import xml.dom.minidom

class rss(pyext._class):
    current_item_index = 0
    items              = []
    url                = ""

    def __init__(self,*args):
        if len(args) > 0:
            self.url = args[0]
            self._regen_dom()
            self._populate_items()
    
    def bang_0(self):
        self._outlet(1, "Hello world")

    def url_0(self, arg):
        arg = str(arg)
        print "Setting URL to " + arg
        self.url = arg
        self._regen_dom()
        self._populate_items()

    def _regen_dom(self):
        self.dom = xml.dom.minidom.parseString(urllib2.urlopen(self.url).read())

    def _populate_items(self):
        self.current_item_index = 0
        self.items = self.dom.getElementsByTagName("description")

    def _fetch_next(self):
        if self.current_item_index >= len(self.items):
            self.current_item_index = 0
        self._outlet(1, items[self.current_item_index])
        self.current_item_index += 1
        

#import sys
#
#print "Script init'd"
#
#URL = ""
#
#try:
#    URL = sys.argv[1]
#except:
#    print "no default args"
#
#def fetch_next():
#    return URL
#
#def set_url(url):
#    URL = url


