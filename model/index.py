#coding:utf-8

import _env
import time
from random import choice
from _db import connection, kv, McCache
from lib.txt_diff import diff_get
from model.history import mc_txt_brief, mc_url_id_list_by_user_id, KV_TXT_SAVE_TIME, history_count, txt_get, txt_set, USER_NOTE


URL_ENCODE = 'abcdefghijklmnopqrstuvwxyz0123456789'

        
 
def txt_by_url(url):
    url_id = url_new(url)
    r = txt_get(url_id)
    return r

def url_random():
    while True:
        url = ''.join(choice(URL_ENCODE) for i in xrange(choice((6,7,8,9,10))))
        if not txt_by_url(url):
            break
    return url

mc_url_by_id = McCache("UrlById:%s")

@mc_url_by_id('{id}')
def url_by_id(id):
    cursor = connection.cursor()
    cursor.execute(
        'select url from url where id=%s',
        id
    )
    url = cursor.fetchone()
    return url[0] if url else None

mc_url_new = McCache("UrlNew:%s")

@mc_url_new("{url}")
def url_new(url):
    url = str(url.lower())
    cursor = connection.cursor()
    cursor.execute('select id from url where url="%s"' % url)
    id = cursor.fetchone()
    if id:
        return id[0]
    else:
        cursor.execute('insert into url (url) values("%s")' %  url)
        return cursor.lastrowid

def txt_rstrip(txt):
    if isinstance(txt, unicode):
        txt = txt.encode('utf-8',"ignore")
    return '\n'.join(
        map(
            str.rstrip,
            txt.replace('\r\n', '\n')\
               .replace('\r', '\n').rstrip('\n ')\
               .split('\n')
        )
    ).rstrip()

def txt_save(user_id, url, txt):
    url_id = url_new(url)
    txt=txt_rstrip(txt)

    if not txt:
        txt_hide(user_id, url_id)

    txt_old = txt_get(url_id) or ''
    if txt_old == txt:
        return
    mc_txt_brief.delete(url_id)
    txt_set(url_id, txt_rstrip(txt))
    now = int(time.time())

    if txt:
        txt_touch(user_id, url_id)

    txt_log_save(user_id, url_id, txt, txt_old)
    kv.set(KV_TXT_SAVE_TIME+str(url_id), now) 

def txt_hide(user_id, url_id):
    cursor = connection.cursor()
    cursor.execute('select state from user_note where url_id=%s and user_id=%s' % (url_id, user_id))
    r = cursor.fetchone()
    cursor.execute('update user_note set state=%s where url_id=%s and user_id=%s' % (USER_NOTE.RM,url_id, user_id))
    if r and r[0] > USER_NOTE.RM:
        _mc_flush(user_id) 

def txt_view_id_state(user_id, url_id):
    cursor = connection.cursor()
    cursor.execute('select id,state from user_note where url_id=%s and user_id=%s' % (url_id, user_id))
    r = cursor.fetchone()
    return r

def txt_touch(user_id, url_id):
    if not user_id:return
    now = int(time.time())
    cursor = connection.cursor()
    r = txt_view_id_state(user_id, url_id) 
    if r:
        id, state = r
        if state < USER_NOTE.DEFAULT or id != txt_last_id(user_id):
            cursor.execute('update user_note set view_time="%s" , state=%s where id=%s' % (now,USER_NOTE.DEFAULT, id))
            mc_url_id_list_by_user_id.delete(user_id)
            mc_txt_last_id.set(user_id, url_id)
            if state < USER_NOTE.DEFAULT:
                history_count.delete(user_id)
    else:
        cursor.execute(
            'insert into user_note (user_id, url_id, view_time, state) values '
            '(%s,%s,"%s",%s) ON DUPLICATE KEY UPDATE view_time="%s", state=%s' % 
            (user_id, url_id, now, USER_NOTE.DEFAULT, now, USER_NOTE.DEFAULT)
        )
        history_count.delete(user_id)
        mc_url_id_list_by_user_id.delete(user_id)
        mc_txt_last_id.set(user_id, url_id)

mc_txt_last_id =  McCache("TxtLastId:%s")

@mc_txt_last_id("{user_id}")
def txt_last_id(user_id):
    cursor = connection.cursor()
    cursor.execute('select id from user_note where user_id=%s and state>=%s order by view_time desc limit 1' % ( user_id, USER_NOTE.DEFAULT))
    r = cursor.fetchone()
    if r:
        return r[0]
    return 0

def _mc_flush(user_id, url_id):
    history_count.delete(user_id)
    mc_url_id_list_by_user_id.delete(user_id)



def txt_log_last_time(url_id):
    t = kv.get(KV_TXT_SAVE_TIME+str(url_id))
    if not t:
        return 0
    return int(t) 

def txt_log_save(user_id, url_id, txt, txt_old):
    now = int(time.time())
    if txt_old and now - txt_log_last_time(url_id) > 600:
        cursor = connection.cursor()
        cursor.execute(
            'insert into txt_log (url_id, user_id, time) values (%s,%s,%s)' % (url_id, user_id, int(time.time()))
        )
        id = cursor.lastrowid
        kv.set('TxtLog:%s' % id, txt_old)
        diff = diff_get(txt_old, txt)
        kv.set('TxtDiff:%s' % id, diff)

 
        kv.set(KV_TXT_SAVE_TIME+str(url_id), now)

if __name__ == "__main__":
    print url_new('sssafes')


