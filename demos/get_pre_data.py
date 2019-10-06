import os
import sys
sys.path.append(os.getcwd())
import time, datetime
import requests
from lxml import etree
from mysql.stock import multi_add
from mysql.models import PreAnalysisStocks
from tornado.options import options, define
define('port', default=8888)
define('debug', default=False)
options.parse_command_line()


page_url = 'http://data.10jqka.com.cn/ajax/yjyg/date/%s/board/ALL/field/enddate/order/desc/page/%s/ajax/1/free/1/'
index_url = 'http://data.10jqka.com.cn/financial/yjyg/'
header = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Cookie': 'vvvv=1; v=Ardm1T-ZphfLuSKbWEGtBwF8RqACfIveZVAPUglk0wbtuNlWEUwbLnUgn6Ma'
}
page = 1
data = []

index_html = etree.HTML(requests.get(index_url, headers=header).content.decode('gbk'))
today = index_html.xpath('//*[@id="J-ajax-main"]/table/tbody/tr[1]/td[8]')[0].text
yesterday = datetime.datetime.strptime(today, '%Y-%m-%d')-datetime.timedelta(days=1)
singal = True

while singal:
    res = requests.get(page_url % (today, page), headers=header)
    html = etree.HTML(res.content.decode('gbk'))
    tr_list = html.xpath('/html/body/table/tbody/tr')
    for tr in tr_list:
        tmp = [i.strip() for i in tr.xpath('.//text()') if i.strip()]
        tmp_day = datetime.datetime.strptime(tmp[-1], '%Y-%m-%d')
        if tmp_day < yesterday:
            multi_add(PreAnalysisStocks, data)
            singal = False
            break
        data.append({
            'code': int(tmp[1]),
            'name': tmp[2],
            'detials': tmp[4],
            'extent': tmp[5],
            'status': 1
        })
        if len(data) > 100:
            multi_add(PreAnalysisStocks, data)
            data = []
