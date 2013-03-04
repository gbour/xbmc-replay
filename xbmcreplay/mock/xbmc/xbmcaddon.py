#!/usr/bin/env python
# -*- coding: UTF8 -*-

"""Mocked xbmcaddon module
"""
import os
import xbmc

class Addon(object):
    def __init__(self, id):
        self.id = id

    def getLocalizedString(self, id):
        return ''

    def getAddonInfo(self, id):
        if id == 'path':
            return os.getcwd()

        return None

    def getSetting(self, key):
        ret = xbmc.CONTEXT.setting(key)
        if ret != 'none':
            print "%s=%s" % (key, ret)
            return ret

        if key == 'autoplatform':
            return 'false'
        if key == 'ostype':
            return 4 #Linux
        if key == 'cputype':
            return 0 #32bit
        if key == 'catalog_refresh_rate':
            return 60*10 #10 minues, in seconds
        if key == 'debug':
            #return True
            return 'true'
            #return 'false'
        if key == 'rtmpdump':
            return 'rtmpdump'
        if key == 'downloadMode':
            return 'false'
        if key == 'downloadPath':
            return '/tmp'
        if key == 'server':
            return 1

        # tf1
        if key == 'preferhd':
            return 'true'

        print "%s setting not found!" % key
        return None
