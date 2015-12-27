#coding:utf-8

import _env
from os.path import join, dirname, abspath, exists
from os import walk, mkdir, remove, makedirs
from collections import defaultdict
from hashlib import md5
from glob import glob
from base64 import urlsafe_b64encode
import envoy
import zweb
import os
from tempfile import mktemp
from config import HOST_CSS_JS
#,   JS_CONST 
from json import dumps
#from misc.config.cid import CID
#
#
#with open(join(_env.PREFIX, "js/%s"%JS_CONST[0]),"w") as const:
#    result = dict((k,v) for k,v in CID.__dict__.iteritems() if k[0]!="_")
#    const.write("CID = %s\n"%dumps(result, indent=4))
#    const.write("CONST = %s"%dumps(JS_CONST[1],indent=4))

BULID = join(_env.PREFIX, 'build')
BULID_EXIST = set(glob(BULID+'/*'))
PATH2HASH = {}
if not exists(BULID):
    mkdir(BULID)

def dirwalk(dirname):
    base = join(_env.PREFIX, dirname)
    merge = []
    file = []
    suffix = '.%s'%dirname
    for dirpath, dirnames, filenames in walk(base, followlinks=True):
        for i in filenames:
            path = abspath(join(dirpath, i))
            if i == 'merge.conf':
                merge.append((path, merge_conf(path, base)))
            if i.endswith(suffix):
                file.append(path)
    return file , merge


def merge_conf(file, base):
    ft = defaultdict(list)
    p = None
    dirpath = dirname(file)
    with open(file) as f:
        for line in f:
            line = line.strip()
            if line.startswith('#') or not line:
                continue
            if line[0] == '/':
                path = base+line
            else:
                path = join(dirpath, line)
            if line.endswith(':'):
                p = path[:-1].strip()
            elif line and p:
                ft[p].append(path)
    return ft

#@import url(ctrl/main.css);
#@import url(ctrl/zsite.css);
#@import url(ctrl/feed.css);


def merge_css( src_list):
    result = [ ]
    for i in src_list:
        result.append("""@import url(%s);"""%(i[len(_env.PREFIX)+4:]))
    return result

def merge_js( src_list):
    result = [
        '''function LOAD(js){ document.write('<script src="'+js+'"></'+"script>") }'''
    ]

    for i in src_list:
        result.append("""LOAD('http://%s/js%s')"""%( HOST_CSS_JS, i[len(_env.PREFIX)+3:]))
    return result


def run(suffix):
    file_list , merge_list = dirwalk(suffix)
    file_set = set(file_list)

    to_merge = defaultdict(list)
    for merge_conf, merge in merge_list:
        for to_file, src_list in merge.iteritems():
            if to_file in file_set:
                file_set.remove(to_file)
            for i in src_list:
                if exists(i):
                    to_merge[to_file].append(i)
                else:
                    print merge_conf , 'ERROR'
                    print '\t', i , 'NOT EXIST'

    if suffix == 'css':
        merger = merge_css
        cmd = 'java -jar %s --charset=utf-8 --type css  -o %%s %%s'% join(dirname(abspath(zweb.__file__)), 'utils/yuicompressor.jar')
    else:
        merger = merge_js
        cmd = 'uglifyjs -nc -o %s %s '

    for i in file_set:
        base = join(_env.PREFIX, suffix)
        with open(i) as infile:
            hash = hash_name(infile.read(), i)
            path = join(BULID, hash)+'.'+suffix
            if path not in BULID_EXIST:
                t = cmd%(path, i)
                print t
                envoy.run(t)


    for to_file, src_list, in to_merge.iteritems():

        dirpath = dirname(to_file)
        if not exists(dirpath):
            makedirs(dirpath)

        r = merger( src_list)
        with open(to_file, 'w') as to:
            r = '\n'.join(r)
            to.write(r)

        r = []
        for i in src_list:
            with open(join(BULID, PATH2HASH[i])) as t:
                r.append(t.read())
        r = '\n'.join(r)
        hash = hash_name(r, to_file)
        path = join(BULID, hash)+'.'+suffix
        #print path
        if path not in BULID_EXIST:
            tmp = mktemp()
            with open(tmp, 'w') as f:
                f.write(r)

            t = cmd%(path, tmp)
            print t
            envoy.run(t)


def hash_name(content, path):
    hash = urlsafe_b64encode(md5(content).digest()).rstrip('=')
    PATH2HASH[path] = hash+'.'+path.rsplit('.', 1)[-1]
    return hash

run('css')
run('js')

for i in BULID_EXIST-set(BULID+'/'+i for i in PATH2HASH.itervalues()):
    if i.endswith('.css') or i.endswith('.js'):
        print 'remove', i
        remove(i)

init = defaultdict(list)
for file_name, hash in  PATH2HASH.iteritems():
    dirname, file_name = file_name[len(_env.PREFIX)+1:].split('/', 1)
    init[dirname].append(( file_name, hash ))

for suffix, flist in init.iteritems():
    with open(join(_env.PREFIX, suffix, '_hash_.py'), 'w') as h:
        h.write("""#coding:utf-8\n
import _env

__HASH__ =  {
""")
        for name, hash in flist:
            h.write(
                """    "%s" : '%s', #%s\n"""%(
                    name,
                    hash,
                    name.rsplit('.', 1)[0].replace('.', '_').replace('-', '_').replace('/', '_')
                )
            )
        h.write('}')

        h.write("""


from config import DEBUG, HOST, HOST_CSS_JS
from os.path import dirname,basename
__vars__ = vars()

for file_name, hash in __HASH__.iteritems():
    
    if DEBUG:
        value = "http://%s/%s/%s"%(HOST_CSS_JS, basename(dirname(__file__)),   file_name)
    else:
        value = "http://%s/build/%s"%(HOST_CSS_JS, hash) 
    
    name = file_name.rsplit('.', 1)[0].replace('.', '_').replace('-', '_').replace('/', '_')
    
    __vars__[name] = value
                            
""")



