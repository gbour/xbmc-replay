# -*- coding: UTF8 -*-

import m3u8
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
    def __init__(self, uri):
        self.uri = uri

    @staticmethod
    def do_i_know(uri):
        return False

    def options(self):
        return {}


class M3u8Downloader(AbstractDownloader):
    def __init__(self, uri):
        super(M3u8Downloader, self).__init__(uri)
        self.target = m3u8.load(uri)
        self.opts   = {}

    @staticmethod
    def do_i_know(uri):
        return uri.endswith('m3u8')

    def options(self):
        if self.target.is_variant:
            self.opts['bandwidth'] = {
                'choices': [s.stream_info.bandwidth for s in self.target.playlists]+['max','min'],
                'default': 'max'
            }

        return self.opts

class RTMPDownloader(AbstractDownloader):
    @staticmethod
    def do_i_know(uri):
        scheme = uri.split(':',1)[0]

        return scheme.startswith('rtmp')
    
