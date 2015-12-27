#coding:utf-8
from server import run 




if __name__ == "__main__":
    from reloader.reload_server import auto_reload
    auto_reload(run)

