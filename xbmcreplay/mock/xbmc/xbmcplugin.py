#!/usr/bin/env python
# -*- coding: UTF8 -*-

import xbmc

SORT_METHOD_UNSORTED=0
SORT_METHOD_LABEL=1
SORT_METHOD_DATE=2
SORT_METHOD_VIDEO_RUNTIME=3

def setPluginCategory(handle, category):
    return ''

def endOfDirectory(handle, *args, **kwargs):
    pass

def addDirectoryItem(handle, url, listitem, isFolder=False, totalItems=1):
    #print "addDirectoryItem:", handle, url, listitem
    xbmc.CONTEXT.addEntry(listitem.label.strip(), url)
    return True

def addSortMethod(handle, sortMethod):
    pass

def setContent(handle, content):
    #print "setContent:", handle, content
    pass

def setResolvedUrl(handle, succeeded, listitem):
    #print "setResolvedUrl:", listitem
    xbmc.CONTEXT.setUrl(listitem.path)
