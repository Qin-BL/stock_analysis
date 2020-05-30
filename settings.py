#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from tornado.options import options


# 静态资源路径
STATIC_PATH = os.path.join(sys.path[0], 'static')
# tornado 模板路径
TEMPLATE_PATH = os.path.join(sys.path[0], 'static/template')
# 默认redis
DEFAULT_REDIS = {
    'host': '127.0.0.1',
    'port': 6379,
    'db': 0
}
# 默认mysql
mysql_master = {
    'user': 'root',
    'password': 'qinbilei888',
    'host': '127.0.0.1',
    'port': 3306,
    # 'db': 'test'
    'db': 'stock'
}

# 2020年周一至周五所有假期
all_holiday = ['2020-06-25', '2020-06-26', '2020-10-01', '2020-10-02', '2020-10-05', '2020-10-06', '2020-10-07',
               '2020-10-08', ]

# 请放在结尾
if options.debug:
    from settings_debug import *
