#!/usr/bin/env python
# -*- coding: UTF8 -*-

import cmd

class Cmd(cmd.Cmd):
    def __init__(self, addons):
        cmd.Cmd.__init__(self)

        self.addons  = addons
        self.context = self

        self.contexts = {
            'addons': AddonCmd(self.addons)
        }

    def run(self):
        while True:
            self.prompt = '$> '
            self.cmdloop()

            if self.context != self:
                self.context.run()

    def switch_context(self, name):
        self.context = self.contexts[name]
        return True # stop cmdloop

    def do_addons(self, subs, **kwargs):
        #print 'addons', args, kwargs
        if len(subs) == 0:
            return self.switch_context('addons')

        self.contexts['addons'].onecmd(subs)

    def complete_addons(self, *args, **kwargs):
        #print 'complete', args, kwargs
        return ('list',)


class AddonCmd(cmd.Cmd):
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
