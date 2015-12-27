#coding:utf-8
import _env
import time
import urllib
import json
import bz2
import tornado.web
import tornado.auth
from _view import View, LoginView, login, logout
from model.account import account_new, user_by_id
from model.index import url_random, txt_save, txt_by_url, url_new, url_by_id,txt_touch, txt_get, txt_view_id_state
from model.history import history_get, history_count
from config import HOST
from lib.page import page_limit_offset
from _route import route

@route('/\:')
class History(LoginView):
    def get(self):
        if not self.current_user_id:
            return self.redirect("/:help")
        name = user_by_id(self.current_user_id)[0]
        self.render('/history.html', name=name)

@route('/\:auth/logout')
class Logout(LoginView):
    def get(self):
        self.check_xsrf_cookie()
        logout(self)
        self.redirect('/:help')

@route('/\:help')
class Help(View):
    def get(self):
        self.render('/help.html')

@route('/\:api/txt/(.*)')
class Api(View):
    def get(self, url=''):
        if not url:
            self.finish('')
        else:
            self.finish(txt_by_url(url))

    def post(self, url=''):
        files = self.request.files
        txt = files.get('file')
        if txt:
            txt = txt[0]['body']
        if txt:
            url = url.strip()
            if not url:
                url = url_random()
            txt = bz2.decompress(str(txt))
            txt_save(self.current_user_id, url, txt)
            self.finish(url)
        self.finish('')

@route('/\:auth/oauth')
class GoogleHandler(tornado.web.RequestHandler, tornado.auth.GoogleMixin):
    
    _OPENID_ENDPOINT = "https://www.google.com.hk/accounts/o8/ud"
    _OAUTH_ACCESS_TOKEN_URL = "https://www.google.com.hk/accounts/OAuthGetAccessToken"

    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("openid.mode", None):
            user = self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        ax_attrs=["name", "email", "language", "username"]
        callback_uri = "http://%s%s"%(HOST,self.request.path) 
        args = self._openid_args(callback_uri, ax_attrs=ax_attrs)
        self.redirect(self._OPENID_ENDPOINT + "?hl=zh-CN&" + urllib.urlencode(args))

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Google auth failed")
        else:
            name = user['name']
            email = user['email']
            user_id = account_new(name, email)
            login(self, user_id)
            self.redirect('/:')

@route('/\:j/history')
@route('/\:j/history-(\d+)')
class J_History(LoginView):
    def get(self, n=1):
        #[timestamp,content, url , count ]
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        user_id = self.current_user_id
        count = history_count(user_id)
        page , limit , offset = page_limit_offset(
            '/history-%s',
            count,
            n,
            15
        )
        _history = history_get(user_id, offset, limit)
        self.finish(json.dumps(_history + [[count, int(n), limit]]))
        
@route('/\:id/(\d+)')
class UrlJump(LoginView):
    def get(self, id=0):
        user_id = self.current_user_id
        if txt_view_id_state(user_id, id):
            url = url_by_id(id)
            self.redirect('/%s' % url)
        else:
            self.redirect("/:help")

@route('/(.*)')
class Index(View):
    def get(self, url):
#        return self.finish(self.request.path)
        if not url:
            url = url_random()
            self.redirect(url)
        else:
            user_id = self.current_user_id
            id = url_new(url)
            txt = txt_get(id)
            if txt:
                txt_touch(user_id, id)
            self.render('/index.html', txt=txt, url=url)

    def post(self, url):
        if url:
            txt = self.get_argument('txt', '').rstrip()
            txt_save(self.current_user_id, url, txt)
        self.finish({'time':int(time.time())})

if __name__ == '__main__':
    pass
    #print url_random()
