# what rss.py
# who  nate smith
# when oct 2009
# why  python class for use in independent study

import pyext
import urllib2
import xml.dom.minidom
from unescape import unescape
import re

class rss(pyext._class):
    index = 0
    items = []
    url   = ""

    _inlets  = 1 # tried leaving this out, wouldn't let me specify callbacks for inlet 0...
    _outlets = 1 # tried leaving this out, wouldn't let me access 0th or 1st outlet...

    def __init__(self,*args):
        print "No init args"
        if len(args) > 0:
            self.url = args[0]
            self._repopulate()
    
    def bang_1(self):
        self._outlet(1, str(self._fetch_next()))

    def url_1(self, arg):
        arg = str(arg)
        print "Setting URL to " + arg
        self.url = arg
        self._repopulate()

    def _repopulate(self):
        print "Regenerating DOM"
        self.dom = xml.dom.minidom.parseString(urllib2.urlopen(self.url).read())

        print "Repopulating items array"
        self.index = 0
        # this monster achieves:
        #   - slice the first description node off (it's a channel desc)
        #   - crop each string to a max of 300 chars
        #   - URI decode text
        #   - unescape HTML entities
        self.items = map( lambda x: unescape( urllib2.unquote( x.firstChild.data))[0:300], \
                          self.dom.getElementsByTagName("description")[1:]
        )

        # No unicode support in puredata (at least not via pyext. It claims it can't convert) 
        print "Filtering unicode characters..."
        def maybe_delete(c):
            try:    return str(c)
            except: return " "
        self.items = map(lambda x: ''.join(x), map(lambda y: map(maybe_delete, y), self.items))
        
        print "Items now has %s entries" % len(self.items)

    def _fetch_next(self):
        if self.index >= len(self.items):
            self._repopulate()
        print "Trying to fetch item at index %s" % self.index
        ret = self.items[self.index]
        print "Fetched: %s" % ret
        self.index += 1
        return ret
