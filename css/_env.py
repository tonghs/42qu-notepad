#coding:utf-8

import sys
from os.path import dirname, abspath, exists, join
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')


PREFIX = dirname(abspath(__file__))
def _():
    global PREFIX 
    PWD = abspath(__file__)
    while True and len(PWD) > 1:
        PWD = dirname(PWD)
        if exists('%s/model'%PWD) and exists('%s/lib'%PWD) and exists('%s/view'%PWD):
            PREFIX = PWD
    for path in (PREFIX, join(PREFIX,".site-packages")):
        if path and path not in sys.path:
            sys.path.insert(0, path)

_()
