
#coding:utf-8

def pre_config(o):
    o.HOST = 'shanshui.me'
    o.MYSQL_USER = 'jack'
    o.MYSQL_PASSWD = 'awdz!@#'
    o.MYSQL_DB = 'work_notepad'
    o.DEBUG = True
    pass

def post_config(o):
    o.HOST_CSS_JS = 's.%s'%o.HOST

