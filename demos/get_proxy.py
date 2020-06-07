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


url = 'http://www.66ip.cn/%s.html'
i = 1
res = []
while True:
    html = etree.HTML(requests.get(url % str(i)).content.decode('gbk'))
    tr_list = html.xpath('//*[@id="main"]/div/div[1]/table/tbody/tr')[1:]
    if not len(tr_list):
        break
    for tr in tr_list:
        ip = tr.xpath('./td[1]/text()')
        port = tr.xpath('./td[2]/text()')
        proxies = {
            'http': 'http://%s:%s' % (ip, port),
            'https': 'http://%s:%s' % (ip, port)
        }
        if requests.get('http://www.baidu.com', proxies=proxies, timeout=20).status_code == 200:
            res.append({
                'ip': ip,
                'port': port
            })
    i += 1
multi_add(Proxys, res)
