"""
每天17点分析业绩预告数据，数据源是同花顺，分析后删除pre表中对应的数据
http://d.10jqka.com.cn/v2/realhead/hs_000962/last.js
http://stockpage.10jqka.com.cn/realHead_v2.html
6: "36.39"昨收
7: "36.99"今开
8: "37.40"最高
9: "35.83"最低
10: "36.43"今收
12: "1"
13: "5568228.00"
14: "2651148.00"
15: "2688480.00"
17: "73272.00"
19: "203787960.00"
22: ""
23: ""
24: "36.43"
25: "7800.00"
30: "36.44"
31: "14500.00"
37: "-1"
38: "-1"
39: "-1"
49: "48600.00"
51: ""
66: ""
69: "40.03"涨停
70: "32.75"跌停
74: ""
75: ""
85: ""
90: ""
92: ""
95: ""
96: ""
127: ""
223: "11349897.50"
224: "8382353.10"
225: "11658183.00"
226: "20156498.00"
237: "54260183.00"
238: "54691445.00"
254: ""
259: "19484136.00"
260: "23805310.00"
271: "-1"
273: "-1"
274: ""
276: ""
277: ""
278: ""
402: "495500000.00"
407: "49550000.00"
2942: "96.502"
134152: "120.657"
199112: "0.11"
264648: "0.040"
395720: "11300.000"
461256: "16.259"
526792: "4.314"
527198: "2917080.000"
592920: "10.481"
1378761: "36.598"
1771976: "0.690"
1968584: "11.238"
2034120: "96.502"
3475914: "1805106500.000"
3541450: "18051065000.000"
marketType: ""
marketid: "33"
name: "三角防务"
stockStatus: "闭市"
stop: 0
time: "2019-10-23 17:59:56 北京时间"
updateTime: "2019-10-23 15:00"
"""
import os
import sys
sys.path.append(os.getcwd())
from tornado.options import options, define
define('port', default=8888)
define('debug', default=False)
options.parse_command_line()

import time, random, logging
import requests
from mysql.stock import get_all_pre_data, multi_add, del_pre_data, del_all_pre_data
from mysql.models import AnalysisedStocks
from lib.send_mail import mail


url = 'http://d.10jqka.com.cn/v2/realhead/hs_%s/last.js'
header = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Cookie': 'vvvv=1; v=Ardm1T-ZphfLuSKbWEGtBwF8RqACfIveZVAPUglk0wbtuNlWEUwbLnUgn6Ma',
    'Referer': 'http://stockpage.10jqka.com.cn/realHead_v2.html'
}


def get_last_price(code):
    data = requests.get(url % str(code), headers=header).content.decode()
    res = eval(data.split('_last(')[-1][:-1])
    return {
        'heighest_price': res['items']['8'],  # 最高
        'mini_price': res['items']['9'],  # 最低 
        'finish_price': res['items']['10'],  # 收盘
        'begin_price': res['items']['7'],  # 开盘
        'yes_finish_price': res['items']['6'],  # 昨收
        'limit_up': res['items']['69']  # 涨停
    }


all_data = get_all_pre_data()
data_jump = []
data_up = []
res_set = set()
for i in all_data:
    code = str(i['code'])
    logging.info(code)
    if code in res_set:
        continue
    try:
        last_price = get_last_price(code)
    except Exception as e:
        logging.error(code)
        logging.error(e)
        res_set.add(code)
        continue
    try:
       float(last_price['mini_price'])
       float(last_price['finish_price'])
       float(last_price['yes_finish_price'])
    except:
       logging.error(last_price['mini_price'])
       logging.error(last_price['yes_finish_price'])
       res_set.add(code)
       continue
    if float(last_price['mini_price']) > float(last_price['yes_finish_price']):
        data_jump.append({
            'code': code,
            'name': i['name'],
            'detials': i['detials'],
            'extent': i['extent'],
            'mark': 0,
            'notice_time': i['notice_time'],
            "range": (float(last_price['mini_price'])-float(last_price['yes_finish_price'])) / float(last_price['yes_finish_price'])
        })
        continue
    if float(last_price['finish_price']) > float(last_price['yes_finish_price']):
        data_up.append({
            'code': code,
            'name': i['name'],
            'detials': i['detials'],
            'extent': i['extent'],
            'mark': 0,
            'notice_time': i['notice_time'],
            "range": (float(last_price['finish_price'])-float(last_price['yes_finish_price'])) / float(last_price['yes_finish_price'])
        })
    time.sleep(random.choice(range(2, 6)))
    res_set.add(code)
logging.warning('finish,all is %d' % len(data_jump))
# multi_add(AnalysisedStocks, data_jump)
data_jump.sort(key=lambda x: x["range"], reverse=True)
data_up.sort(key=lambda x: x["range"], reverse=True)
res = '跳空：' + '\n'.join(['\n%s，%s；' % (i['code'], i['name']) for i in data_jump]) + \
      '\n上涨：' + '\n'.join(['\n%s，%s；' % (i['code'], i['name']) for i in data_up])
mail(res)
del_all_pre_data()

