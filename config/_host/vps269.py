
#coding:utf-8

def pre_config(o):
    o.HOST = '42qu.co'
    o.MYSQL_USER = 'work'
    o.MYSQL_PASSWD = '42qudev'
    o.DEBUG = True
    pass

def post_config(o):
    o.HOST_CSS_JS = 's.%s'%o.HOST

