#!/usr/bin/env python
# -*- coding: UTF8 -*-

class ListItem(object):
    def __init__(self, label=None, thumbnailImage=None,
                 path=None, iconImage=None, **kwargs):
        print "item", label, kwargs, path
        try:
            self.label = label.decode('utf8',errors='ignore') if label is not None else None
        except:
            self.label = label

        self.thumb = thumbnailImage
        self.path  = path

        self.properties = dict()

    def addContextMenuItems(self, menu, replaceItems=False):
        pass

    def setInfo(self, type, infoLabels):
        print "%s / %s" % (type, infoLabels)

    def setProperty(self, key, value):
        print "%s: property(%s=%s)" % (self.label, key, value)
        self.properties[key] = value

    def __str__(self):
        return (u"ListItem(%s, %s)" % (self.label, self.path)).encode('utf8')

class WindowXMLDialog(object):
    pass
