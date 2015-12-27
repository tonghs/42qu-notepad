#coding:utf-8

import _env

__HASH__ =  {
    "index.js" : '3qSAB17e0XfX2HnVt_94Sw.js', #index
    "ext.js" : 'fYbDzFtJEhehMZhJPy1i6Q.js', #ext
    "cookie.js" : '_Lb6EAwJZk7RNUjbJJmXFw.js', #cookie
    "base.js" : 'ZmKE7RScKu03QCIA4YVbgQ.js', #base
    "history.js" : 'FHTxqtEHu0xrCgEpevJHYA.js', #history
    "all.js" : 'L7bpd9RsP_cslOgSz1U2mA.js', #all
    "paging.js" : 'HV6PX0oDIW5R2pqlIMActw.js', #paging
}


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
                            
