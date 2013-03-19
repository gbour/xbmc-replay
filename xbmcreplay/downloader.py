# -*- coding: UTF8 -*-

import inspect
import threading

class DownloadManager(object):
    def __init__(self):
        self.threads = []

        self.handlers = dict(inspect.getmembers(inspect.getmodule(self), 
            lambda x: inspect.isclass(x) and issubclass(x, AbstractDownloader) and not x == AbstractDownloader)
        ).values()
        print self.handlers

    def download(self, uri, **kwargs):
        match = [h for h in self.handlers if h.do_i_know(uri)]
        if len(match) == 0:
            # no match
            return False
        elif len(match)> 1:
            # more than 1 handler found
            return False

        t = threading.Thread(target=getattr(match[0], 'download'), kwargs=kwargs)
        t.start()

        self.threads[t.ident] = t
        return True

    def select(self, uri, instanciate=False):
        match = [h for h in self.handlers if h.do_i_know(uri)]
        if len(match) == 0:
            # no match
            return None
        elif len(match)> 1:
            # more than 1 handler found
            return None

        m = match[0]
        if instanciate:
            m = m(uri)
        return m


class AbstractDownloader(object):
    def __init__(self):
        pass

    @staticmethod
    def do_i_know(uri):
        return False

    @staticmethod
    def options(uri):
        opts = {}
        
        target = m3u8.load(uri)
        if target.is_variant:
            opts


    @staticmethod(uri, bandwidth='higher'):



class M3u8Downloader(AbstractDownloader):
    @staticmethod
    def do_i_know(self, uri):
        return uri.endswith('m3u8')

class RTMPDownloader(AbstractDownloader):
    @staticmethod
    def do_i_know(uri):
        scheme = uri.split(':',1)[0]

        return scheme.startswith('rtmp')
    
