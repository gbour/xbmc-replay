#!/usr/bin/env python
# -*- coding: UTF8 -*-

#IMPORTANT: is replaced by ExecutionContext() instance at execution
CONTEXT = None

def translatePath(path):
    path = path.replace('special:/', '/tmp')
    return path

def getCacheThumbName(path):
    print "getCacheThumbName:", path
    return "/tmp/video.avi"

def executebuiltin(function, wait=False):
    print "executebuiltin:", function, wait

