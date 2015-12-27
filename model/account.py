#coding:utf-8

import time
import string
from _db import connection, McCache


def account_new(name, email):
    name, email = map(string.strip, (name, email))
    user_id = user_id_by_email(email)
    if not user_id:
        cursor = connection.cursor()
        if email:
            cursor.execute(
                '''insert into `account` (name, email) values (%s,%s)''', (name, email)
            )
        user_id = user_id_by_email(email)
    return user_id
    
def user_by_id(user_id):
    cursor = connection.cursor()
    cursor.execute('select name, email from account where id=%s', user_id)
    user = cursor.fetchone()
    return user


mc_user_mail = McCache("UserMail:%s")

@mc_user_mail("{user_id}")
def user_mail(user_id):
    cursor = connection.cursor()
    cursor.execute('select email from account where id=%s', user_id)
    r = cursor.fetchone()
    if r:
        return r[0]

def user_id_by_email(email):
    cursor = connection.cursor()
    cursor.execute('select id from account where email=%s',email)
    user_id = cursor.fetchone()
    if user_id:
        user_id = user_id[0]
    else:
        user_id = 0
    return user_id

if __name__ == "__main__":
    account_new('Lerry', 'lerry@test.com')
    print user_id_by_email('lerry@test.com')
