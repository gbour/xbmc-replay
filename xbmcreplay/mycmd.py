#!/usr/bin/env python
# -*- coding: UTF8 -*-

import cmd

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

        self.dyn_completion = []

    def run(self):
        self.prompt = '$[\033[34m' + self.addon.id.split('.')[-1] + '\033[0m]> '
        self.cmdloop()

    def do_back(self, *args):
        return True

    def complete(self, text, state):
        ret = cmd.Cmd.complete(self, text, state)
        if state == 0 and len(self.dyn_completion) == 0:
            menu = {}
            try:
                # default url '/' or '' ??? => 2d is better
                menu = self.addon.execute('', self.xcontext)
            except Exception, e:
                print e
            print "menu=",menu
            if 'menu' in menu:
                self.dyn_completion = [l for l,p in menu['menu']]

            #print self.dyn_completion

        if ret is None:
            ret = [x for x in self.dyn_completion if x.lower().startswith(text.lower())]
            if len(ret) > (state-len(self.completion_matches)):
                ret = ret[state-len(self.completion_matches)]
            else:
                ret=None
        return ret

    def default(self, line):
        print "default=", line
