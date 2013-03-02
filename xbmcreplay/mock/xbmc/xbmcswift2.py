#!/usr/bin/env python
# -*- coding: UTF8 -*-

import re
import sys
import xbmcaddon

class SortMethod(object):
    LABEL=1
    DATE=2

class Log(object):
    def debug(self, msg):
        print "LOGGER::debug=", msg

    def info(self, msg):
        print "LOGGER::info=", msg

class Plugin(object):
    def __init__(self):
        self.addon = xbmcaddon.Addon(0)
        self.routes = {}
        self.log = Log()

    def get_setting(self, key):
        print "get_setting", key

        if key == 'cached_ttl':
            return 255
        if key == 'swf_verify':
            return True
        if key == 'channels':
            return 0 #all
        if key== 'show_by':
            return 0 #genre

        return None

    def cached(self, ttl):
        def _cached(fun):
            print "_cached=", fun
            return fun
        return _cached

    def route(self, path):
        def matchargs(m):
            return "(?P<%s>\w+)" % m.group(1)
            
        regex = "^%s$" % re.sub("<([^>]+)>", matchargs, path)
        #print "route= %s / %s" % (path, regex)

        def _route(fun):
            self.routes[regex] = (path, fun)
            print "FN", fun.__name__
            return fun
        return _route
       
    def run(self):
        print "route", self.routes
        path = sys.argv[2]
        print "path=", path

        m = None
        for r in self.routes.iterkeys():
            m = re.match(r, path)
            if m is not None:
                break

        if m is None:
            print "no match"; return

        (path, clb) = self.routes[r]
        print "match=", m.groupdict(), path, clb
        print clb(**m.groupdict())


    def finish(self, items, sort=None, sort_methods=None):
        print "finish"
        import pprint
        pprint.pprint(items)

    def url_for(self, key, **args):
        if key == 'show_channel':
            return "/channel/%s" % args['channel']
        if key == "show_programs":
            return "/programs/%s/%s" % (args['channel'], args['genre'])
        if key == "show_clips":
            return "/clips/%s/%s" % (args['channel'], args['program'])
        if key == 'play_clip':
            return "/play/%s/%s" % (args['channel'], args['clip'])


        return None

    def set_resolved_url(self, url):
        print "set_resolved_url:", url
