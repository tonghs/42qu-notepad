#coding:utf-8
from jsdict import JsDict
from os.path import dirname
import sys
from _import import _import

CONFIG_LOADED = []

def load(self, *args):
    self = JsDict(self)

    prepare_list = [ ]
    finish_list = [ ]

    sys.path.insert(0, dirname(self.__file__))
    global CONFIG_LOADED

    def _load(name):
        #print name
        try:
            mod = _import(name)
        except ImportError:
            return

        if mod is None:
            return

        if mod in CONFIG_LOADED:
            CONFIG_LOADED.pop(CONFIG_LOADED.index(mod))
        CONFIG_LOADED.append(mod)

        mod.__file__.rsplit(".",1)[0]
 
        prepare = getattr(mod, 'pre_config', None)
        if prepare:
            prepare_list.append(prepare)

        finish = getattr(mod, 'post_config', None)
        if finish:
            finish_list.append(finish)
        
    for i in args:
        _load(i)

    funclist = prepare_list+list(reversed(finish_list))
    for _ in funclist:
        _(self)

    sys.path.pop(0)
    return self



