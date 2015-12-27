#coding:utf-8
import _env
import json
from tornado import web
from config import render
from model.session import session_new, session_rm, id_by_session
import css, js
from model._db import mc
from model.user import User
import datetime

class View(web.RequestHandler):
    def render(self, template_name=None, **kwds):
	print css, js
        if not self._finished:
            current_user = self.current_user
            kwds['request'] = self.request
            kwds['this'] = self
            kwds['css'] = css
            kwds['js'] = js
            kwds['_xsrf'] = self._xsrf
            kwds['current_user'] = self.current_user
            kwds['current_user_id'] = self.current_user_id
            self.finish(render(template_name, **kwds))



    @property
    def current_user_id(self):
        if not hasattr(self, '_current_user_id'):
            current_user = self.current_user
            if current_user:
                self._current_user_id = current_user.id
            else:
                self._current_user_id = 0
        return self._current_user_id


    def get_current_user(self):
        s = self.get_cookie('S')
        if s:
            user_id = id_by_session(s)
            if not user_id:
                self.clear_cookie('S')
            else:
                return User(user_id)
        return None 

    def prepare(self):
        super(View, self).prepare()
        mc.reset()

    @property
    def _xsrf(self):
        return '_xsrf=%s'%self.xsrf_token


class LoginView(View):
    def prepare(self):
        super(LoginView, self).prepare()
        if not self.current_user_id:
            self.redirect('/:help')

def login(self, user_id):
    user_id = int(user_id)
    session = session_new(user_id)
    expires = datetime.datetime.utcnow() + datetime.timedelta(days=3650)
    self.set_cookie('S', session, expires=expires)

def logout(self):
    if self.current_user_id:
        session_rm(self.current_user_id)
    self.clear_cookie('S')
    
