# -*- coding: utf-8 -*-

class Route(object):
    def __init__(self):
        self.handlers = []

    def __call__(self, url, **kwds):
        def _(cls):
            self.handlers.append((url, cls, kwds))
            return cls
        return _

route = Route()
