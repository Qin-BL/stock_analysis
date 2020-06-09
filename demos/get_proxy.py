import os
import sys
sys.path.append(os.getcwd())
from tornado.options import options, define
define('port', default=8888)
define('debug', default=False)
options.parse_command_line()

import requests
from lxml import etree
from mysql.stock import multi_add
from mysql.models import Proxys
import logging


url = 'http://www.66ip.cn/%s.html'
i = 1
res = []
logging.info('starting...')
while i<2003:
    html = etree.HTML(requests.get(url % str(i)).content.decode('gbk'))
    tr_list = html.xpath('//div[@id="main"]//table//tr')[1:]
    logging.info(tr_list)
    if not len(tr_list):
        i += 1
        continue
    for tr in tr_list:
        ip = tr.xpath('.//text()')[0]
        port = tr.xpath('.//text()')[1]
        proxies = {
            'http': 'http://%s:%s' % (ip, port),
            'https': 'http://%s:%s' % (ip, port)
        }
        try:
            if requests.get('http://www.baidu.com', proxies=proxies, timeout=20).status_code == 200:
                res.append({
                    'ip': ip,
                    'port': port
                })
        except:
            pass
    if len(res) > 100:
        multi_add(Proxys, res)
        res = []
    i += 1
logging.info('ending...')
multi_add(Proxys, res)


