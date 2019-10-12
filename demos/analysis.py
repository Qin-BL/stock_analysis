"""
每天17点分析业绩预告数据，数据源是同花顺，分析后删除pre表中对应的数据
http://d.10jqka.com.cn/v2/realhead/hs_000962/last.js
http://stockpage.10jqka.com.cn/realHead_v2.html
"""
import os
import sys
sys.path.append(os.getcwd())
from tornado.options import options, define
define('port', default=8888)
define('debug', default=False)
options.parse_command_line()

import datetime, time, random
import requests
from mysql.stock import get_all_pre_data, multi_add, del_pre_data
from mysql.models import AnalysisedStocks


url = 'http://d.10jqka.com.cn/v2/realhead/hs_%s/last.js'
header = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Cookie': 'vvvv=1; v=Ardm1T-ZphfLuSKbWEGtBwF8RqACfIveZVAPUglk0wbtuNlWEUwbLnUgn6Ma',
    'Referer': 'http://stockpage.10jqka.com.cn/realHead_v2.html'
}


def get_last_price(code):
    data = requests.get(url % code, headers=header).content.decode()
    res = eval(data.split('_last(')[-1][:-1])
    return {
        'heighest_price': res['items']['8'],
        'mini_price': res['items']['9'],
        'finish_price': res['items']['10'],
        'begin_price': res['items']['7'],
        'yes_finish_price': res['items']['6']
    }


all_data = get_all_pre_data()
res_data = []
for i in all_data:
    code = i['code']
    try:
        last_price = get_last_price(code)
    except Exception as e:
        print(code)
        print(e)
        del_pre_data(i['id'])
        continue
    if last_price['mini_price'] > last_price['yes_finish_price']:
        res_data.append({
            'code': code,
            'name': i['name'],
            'detials': i['detials'],
            'extent': i['extent'],
            'mark': 0,
            'notice_time': i['notice_time']
        })
    time.sleep(random.choice(range(2, 6)))
    del_pre_data(i['id'])
multi_add(AnalysisedStocks, res_data)
