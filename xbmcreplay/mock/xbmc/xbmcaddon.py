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
        return xbmc.CONTEXT.setting(key)

        """
        if id == 'autoplatform':
            return False
        if id == 'ostype':
            return 4 #Linux
        if id == 'cputype':
            return 0 #32bit
        if id == 'catalog_refresh_rate':
            return 60*10 #10 minues, in seconds
        if id == 'debug':
            #return True
            return 'true'
            #return 'false'
        if id == 'rtmpdump':
            return 'rtmpdump'
        if id == 'downloadMode':
            return 'false'
        if id == 'downloadPath':
            return '/tmp'
        if id == 'server':
            return 1

        # tf1
        if id == 'preferhd':
            return 'true'
        """

