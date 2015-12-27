
#coding:utf-8

def pre_config(o):
    o.HOST = 'dev.cn'
    o.MYSQL_USER = 'work'
    o.MYSQL_PASSWD = '42qu'
    o.MYSQL_DB = 'work_notepad'
    o.DEBUG = True
    pass

def post_config(o):
    o.HOST_CSS_JS = 's.%s'%o.HOST

