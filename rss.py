# what rss.py
# who  nate smith
# when oct 2009
# why  python class for use in independent study

import pyext
import urllib2
import xml.dom.minidom

class rss(pyext._class):
    index = 0
    items = []
    url   = ""

    _inlets  = 1 # tried leaving this out, wouldn't let me specify callbacks for outlet 0...
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
        self.items = map(lambda x: x.firstChild.data, self.dom.getElementsByTagName("description"))

        # XXX I want unicode support, but for some reason python makes it hard. Filter unicode strings for now.
        print "Items now has %s entries. Filtering unicode..." % len(self.items)
        def can_decode(t):
            try:
                str(t)
                return True
            except:
                return False
        self.items = filter(can_decode, self.items)

        print "Items now has %s entries" % len(self.items)

    def _fetch_next(self):
        if self.index >= len(self.items):
            self._repopulate()
        print "Trying to fetch item at index %s" % self.index
        ret = self.items[self.index]
        self.index += 1
        return ret
