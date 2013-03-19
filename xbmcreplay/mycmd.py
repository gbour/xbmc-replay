#!/usr/bin/env python
# -*- coding: UTF8 -*-

import cmd
from downloader import *

MNGR = DownloadManager()

class Cmd(cmd.Cmd):
    def __init__(self, addons, xcontext):
        cmd.Cmd.__init__(self)

        self.quit    = False
        self.addons  = addons
        # addons execution contet
        self.xcontext = xcontext

        self.context  = self
        self.contexts = {
            'addons': AddonsCmd(self.addons)
        }

    def run(self):
        while not self.quit:
            self.prompt = '$> '
            self.cmdloop()

            if self.context != self:
                self.context.run()

    def switch_context(self, name=None, subcmd=None):
        self.context = self.contexts[name] if subcmd is None else subcmd
        return True # stop cmdloop

    def do_quit(self, *args):
        print 'Bye...'
        self.quit = True
        return True

    def do_addons(self, subs, **kwargs):
        #print 'addons', args, kwargs
        if len(subs) == 0:
            return self.switch_context('addons')

        self.contexts['addons'].onecmd(subs)

    def complete_addons(self, *args, **kwargs):
        #print 'complete', args, kwargs
        return ('list',)

    def completedefault(self, *args):
        print "completedefault", args

    def default(self, command):
        (cmd, args) = (command+' ').split(' ', 1)
        
        # try to match addon
        addons = [a for a in self.addons.addons.values() if cmd.lower() in a.id.lower()]
        if len(addons) == 0:
            print "No addon matching '%s'" % cmd; return

        if len(addons) > 1:
            print "More than 1 addon matching '%', please precise" % cmd; return

        if len(args) == 0:
            return self.switch_context(subcmd=AddonCmd(addons[0], self.xcontext))

        return False


    # override complete()
    def complete(self, text, state):
        ret = cmd.Cmd.complete(self, text, state)
        if state == 0:
            self.dyn_completion = [a.id.split('.')[-1] for a in self.addons.addons.values() if 'video'
                    in a.id and text.lower() in a.id.lower()]

        if ret is None:
            ret = self.dyn_completion[state-len(self.completion_matches)]
        return ret

class AddonsCmd(cmd.Cmd):
    def __init__(self, addons):
        cmd.Cmd.__init__(self)
        self.addons = addons

    def do_list(self, filter):
        addons = self.addons.addons.values()
        if len(filter) > 0:
            addons = [a for a in addons if filter.lower() in a.name.lower() or filter.lower() in a.id.lower()]

        for addon in addons:
            print u" . {0:35s} ({1})".format(addon.name, addon.id)

        
    def run(self):
        self.prompt = '$[\033[34maddons\033[0m]> '
        self.cmdloop()

    def do_back(self, *args):
        return True

class AddonCmd(cmd.Cmd):
    def __init__(self, addon, xcontext):
        cmd.Cmd.__init__(self)
        self.addon = addon
        self.xcontext = xcontext

        self.stack = [('','')]
        self.dyn_completion = []

    def update_prompt(self):
        self.prompt = '$[\033[34m' + self.addon.id.split('.')[-1] + '\033[0m:'
        for label, url in self.stack[1:]:
            self.prompt += '\033[34m' + label + '\033[0m>'
        self.prompt = self.prompt[:-1] + ']> '

    def run(self):
        self.update_prompt()
        self.cmdloop()

    def do_back(self, *args):
        #print "back", args
        self.stack.pop()
        self.update_prompt()
        del self.dyn_completion[:]

        return (len(self.stack) == 0)

    def _init_completion(self):
        """

            \xc2\xa0 == unicode non-breaking space
        """
        menu = {}
        self.dyn_completion = []
        try:
            # default url '/' or '' ??? => 2d is better
            #print "url=", self.stack[-1][1]
            menu = self.addon.execute(self.stack[-1][1], self.xcontext)
        except Exception, e:
            print e
        #print "menu=",menu
        if 'menu' in menu:
            try:
                self.menu = dict([(l.encode('utf8').replace(' ','\xc2\xa0'), p) for l,p in menu['menu']])
                self.dyn_completion = self.menu.keys()
            except Exception, e:
                print e
            #print "::",self.dyn_completion,",",self.menu
        else:
            #print menu
            try:
                self.video = menu['video']
                self.dyn_completion = ['download','show']
            except Exception, e:
                print e

    def complete(self, text, state):
        #print 'complete=', text, state
        ret = cmd.Cmd.complete(self, text, state)
        if state == 0 and len(self.dyn_completion) == 0:
            self._init_completion()

        if ret is None:
            ret = [x for x in self.dyn_completion if x.lower().startswith(text.lower())]
            if len(ret) > (state-len(self.completion_matches)):
                ret = ret[state-len(self.completion_matches)]
            else:
                ret=None
        return ret

    def default(self, line):
        #print 'default=', line
        if line not in self.menu:
            return

        curmenu = self.menu[line]
        self.stack.append((line, curmenu))
        self.update_prompt()

        # read menu content
        self._init_completion()

    def do_show(self, *args):
        print 'url =', self.video

    def do_download(self, *args):
        print 'downloading...', self.video
        if self.video is None:
            return

        dwn = MNGR.select(self.video, instanciate=True)
        print "downloader= ", dwn
        if dwn is None:
            return

        opts = dwn.options()
        print opts




