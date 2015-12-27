#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 初始化python的查找路径
import _env
import sys
from lib.config_loader import load 

_ARGS = [
    'default',
]

try:
    import socket
except ImportError:
    pass
else:
    _ARGS.append(
        '_host.%s' % socket.gethostname(),
    )

import getpass
try:
    _ARGS.append(
        '_user.%s' % getpass.getuser(),
    )
except ImportError:
    pass

load(
    vars(), *_ARGS
)
