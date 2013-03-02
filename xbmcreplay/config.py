#!/usr/bin/env python
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


import re
import yaml


class Config(object):
    def __init__(self, settings):
        self.settings = settings

    def load(self, stream):
        self._config = yaml.load(stream)
        return self._dispatch(self._config)

    def _dispatch(self, item):
        return getattr(self, "_do_%s" % type(item).__name__)(item)

    def _do_dict(self, item):
        return dict([(k, self._dispatch(v)) for k, v in item.items()])

    def _do_list(self, item):
        return [self._dispatch(v) for v in item]

    def _do_int(self, item):
        return item

    def _do_bool(self, item):
        return item

    def _do_str(self, item):
        def subst(m):
            if m.group(1) in self.settings:
                return self.settings[m.group(1)]
            if m.group(1) in self._config:
                return self._config[m.group(1)]

            raise Exception("Unknown '%s' setting" % m.group(1))

        return re.sub('\${([^}]+)}', subst, item)

