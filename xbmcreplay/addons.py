# -*- coding: utf8 -*-
"""
    xbmc-replay
    Copyright (C) 2013, Guillaume Bour <guillaume@bour.cc>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, version 3.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
__author__  = "Guillaume Bour <guillaume@bour.cc>"


import sys
import os
import os.path
from lxml import objectify


class Addons(object):
    def __init__(self, path):
        self.init(path)

    def init(self, path):
        self.path = path
        self.addons = {}
        #TODO: check if writable

        for name in os.listdir(path):
            addon = Addon(os.path.join(path, name))
            self.addons[addon.id] = addon

        #print self.addons


class Addon(object):
    def __init__(self, path):
        #print path, "addon"
        self.path = path

        xml = os.path.join(path, 'addon.xml')
        if not os.path.exists(xml):
            print "%s is not an xbmc addon" % path; return

        root = objectify.parse(file(xml, 'r')).getroot()
        #print objectify.dump(root)

        self.__stub__ = dict(root.attrib)
        ep = [ex for ex in root.iter('extension')
                if ex.attrib.get('point') == 'xbmc.python.pluginsource']

        if ep:
            ep = ep[0]
            self.__stub__['entry'] = ep.attrib['library']
            self.__stub__['type']  = ep.getchildren()[0]

        print self.__stub__

    def __getattr__(self, name):
        if name in self.__stub__:
            return self.__stub__[name]

        raise AttributeError

