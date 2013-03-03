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
import inspect
from lxml import objectify


class Addons(object):
    def __init__(self, path):
        self.init(path)

    def init(self, path):
        self.path = path
        self.addons = {}
        #TODO: check if writable

        for name in os.listdir(path):
            addon = Addon(os.path.join(path, name), self)
            self.addons[addon.id] = addon

        # fake addon
        base = os.path.dirname(inspect.getmodule(self).__file__)
        self.addons['xbmc.python'] = BaseAddon(path=os.path.join(base, 'mock', 'xbmc'))

        #print self.addons

    def get(self, addid):
        return self.addons.get(addid)


class BaseAddon(object):
    def __init__(self, path):
        self.path = os.path.abspath(path)

    def getpath(self):
        return None


class Addon(BaseAddon):
    def __init__(self, path, db):
        #print path, "addon"
        super(Addon, self).__init__(path)
        self.db   = db

        xml = os.path.join(path, 'addon.xml')
        if not os.path.exists(xml):
            print "%s is not an xbmc addon" % path; return

        root = objectify.parse(file(xml, 'r')).getroot()
        #print objectify.dump(root)

        self.__stub__ = dict(root.attrib)
        for ext in root.findall('extension'):
            pt = ext.get('point')

            if pt == 'xbmc.python.pluginsource':
                self.__stub__['entry'] = ext.get('library')
                self.__stub__['type']  = ext.findtext('provides')
            elif pt == 'xbmc.python.module':
                self.__stub__['entry'] = ext.get('library')
                self.__stub__['type']  = 'module'
            elif pt == 'xbmc.addon.metadata':
                pass

            else:
                raise Exception("Unknown addon type: %s" %
                    ext.get('point'))

        requires = root.find('requires')
        if requires is not None:
            self.__stub__['dependencies'] = dict([
                (i.attrib['addon'], i.attrib) \
                for i in requires.iter('import')
            ])

        #import pprint; pprint.pprint(self.__stub__)

    def getpath(self):
        path = self.path

        if self.type == 'module':
            path = os.path.join(path, self.entry)
        return path

    def execute(self, param='/', context=None):
        #print sys.argv
        #print sys.path

        old_sys = (sys.argv, sys.path, os.getcwd(), sys.stdout)
        sys.argv = [self.entry, 0, param]

        base = os.path.dirname(inspect.getmodule(self).__file__)

        syspath = []
        for dep in self.dependencies.iterkeys():
            addon = self.db.get(dep)
            if addon is None:
                print "%s dependency not found" % dep; continue

            path = addon.getpath()
            if path is not None:
                syspath.append(path)

        sys.path = syspath + [
            os.path.join(base, 'mock', 'xbmc'),
            os.path.join(base, 'mock', 'swift2'),
            '',
        ] + sys.path
        os.chdir(self.path)
       
        sys.stdout = open('/dev/null', 'w')
        #print sys.argv, sys.path

        import xbmc
        xbmc.CONTEXT = context

        context._result = {}
        execfile(self.entry, {'sys': sys, '__name__': '__main__'})
    
        # restore sys values
        sys.argv = old_sys[0]
        sys.path = old_sys[1]
        os.chdir(old_sys[2])
        sys.stdout.close()
        sys.stdout = old_sys[3]
        ###

        return context.result()

    def __getattr__(self, name):
        if name in self.__stub__:
            return self.__stub__[name]

        raise AttributeError

    def __str__(self):
        return "<addon(%s)>" % self.id


class ExecutionContext(object):
    def __init__(self, settings):
        self._result   = {}
        self._settings = settings
        #print settings

    def result(self, result=None):
        if result is not None:
            self._result = result
        return self._result

    def setting(self, key):
        #print "context::setting=", key
        return str(self._settings.get(key)).lower()

    def addEntry(self, label, path):
        if 'menu' not in self._result:
            self._result['menu'] = []

        if '?' in path:
            path = path.split('?')[1]
        self._result['menu'].append((label, path))

    def setUrl(self, path):
        self._result['video'] = path


