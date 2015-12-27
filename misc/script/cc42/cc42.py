#!/usr/bin/env python
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib
import requests 
import urllib2
import sys
import bz2
from os.path import join
HOST = 'p.pe.vc'
HOST_HTTP = 'http://%s'%HOST
API_URL = '%s/:api/txt/'%HOST_HTTP

def help():
    print """
1.Paste file to 42qucc
  hi@Mars ~$ 42cc < foo.txt  
  http://42qu.cc/xa47qt471
2.Custom url 
  hi@Mars ~$ 42qucc hi < foo.txt
  http://42qu.cc/hi
3.Save web page to local file
  hi@Mars ~$ 42cc  http://42qu.cc/xa47qt471  >  foo.txt
    """

def post(url=''):
    data = ''.join(sys.stdin.readlines())
    files = {'file': ('txt', bz2.compress(data) )}
    r = requests.post(API_URL+url, files=files, timeout=300)
    print HOST_HTTP+"/"+r.text

def main():
    argv = sys.argv
    url = ''
    if len(argv) > 1:
        if len(argv) > 2:
            help()
            return
        url = argv[1]
        if url.startswith(HOST_HTTP):
            url = url[len(HOST_HTTP)+1:] 
            r = requests.get(API_URL+url, timeout=300) 
            print r.text
            return
        else:
            url = argv[1].lstrip("/")

    post(url)

if __name__ == '__main__':
    main()
