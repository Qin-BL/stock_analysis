import os
import sys
sys.path.append(os.getcwd())
from tornado.options import options, define
define('port', default=8888)
define('debug', default=False)
options.parse_command_line()
import datetime, time, random
import requests
from lxml import etree
from mysql.stock import multi_add
from mysql.models import PreAnalysisStocks
import logging


yjyg_url = 'http://data.10jqka.com.cn/ajax/yjyg/date/%s/board/ALL/field/enddate/order/desc/page/%s/ajax/1/free/1/'
yjgg_url = 'http://data.10jqka.com.cn/ajax/yjgg/date/%s/board/ALL/field/DECLAREDATE/order/desc/page/%s/ajax/1/free/1/'
yjkb_url = 'http://data.10jqka.com.cn/ajax/yjkb/date/%s/board/ALL/field/declaredate/order/desc/page/%s/ajax/1/free/1/'
index_url = 'http://data.10jqka.com.cn/financial/yjyg/'
header = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Cookie': 'vvvv=1; v=Ardm1T-ZphfLuSKbWEGtBwF8RqACfIveZVAPUglk0wbtuNlWEUwbLnUgn6Ma'
}

# proxies = []
versions = []
this_year = time.strftime('%Y')
this_mouth = time.strftime('%m')
if int(this_mouth) <= 3:
    versions = ['%s-12-31' % str(int(this_year) - 1), '%s-03-31' % this_year]
elif 3 < int(this_mouth) <= 6:
    versions = ['%s-12-31' % str(int(this_year) - 1), '%s-03-31' % this_year, '%s-06-30' % this_year]
elif 6 < int(this_mouth) <= 9:
    versions = ['%s-06-30' % this_year, '%s-09-30' % this_year]
else:
    versions = ['%s-09-30' % this_year, '%s-12-31' % this_year]
logging.info(versions)
for version in versions:
    now = datetime.datetime.strptime(time.strftime('%Y-%m-%d'), '%Y-%m-%d')
    # if now > datetime.datetime.strptime(version, '%Y-%m-%d'): continue
    page = 1
    data = []
    singal = True

    index_html = etree.HTML(requests.get(index_url, headers=header).content.decode('gbk'))
    time.sleep(random.choice(range(3, 8)))
    today = index_html.xpath('//*[@id="J-ajax-main"]/table/tbody/tr[1]/td[8]')[0].text
    yesterday = datetime.datetime.strptime(today, '%Y-%m-%d')-datetime.timedelta(days=1)
    logging.info(today)

    while singal:
        res = requests.get(yjyg_url % (version, page), headers=header)
        time.sleep(random.choice(range(3, 8)))
        html = etree.HTML(res.content.decode('gbk'))
        tr_list = html.xpath('/html/body/table/tbody/tr')
        logging.info(yjyg_url % (version, page))
        logging.info(len(tr_list))
        if len(tr_list) == 0:
            multi_add(PreAnalysisStocks, data)
            logging.info(res.text)
            break
        for tr in tr_list:
            tmp = [i.strip() for i in tr.xpath('.//text()') if i.strip()]
            tmp_day = datetime.datetime.strptime(tmp[-1], '%Y-%m-%d')
            if tmp_day < yesterday:
                multi_add(PreAnalysisStocks, data)
                singal = False
                break
            data.append({
                'code': tmp[1],
                'name': tmp[2],
                'detials': tmp[4],
                'extent': tmp[5],
                'notice_time': tmp[-1],
                'status': 1
            })
            if len(data) > 100:
                multi_add(PreAnalysisStocks, data)
                data = []
        page += 1
        time.sleep(random.choice(range(3, 8)))

    page = 1
    singal = True
    data = []
    while singal:
        res = requests.get(yjgg_url % (version, page), headers=header)
        time.sleep(random.choice(range(3, 8)))
        html = etree.HTML(res.content.decode('gbk'))
        tr_list = html.xpath('/html/body/table/tbody/tr')
        logging.info(yjgg_url % (version, page))
        logging.info(len(tr_list))
        if len(tr_list) == 0:
            multi_add(PreAnalysisStocks, data)
            logging.info(res.text)
            break
        for tr in tr_list:
            tmp = [i.strip() for i in tr.xpath('.//text()') if i.strip()]
            tmp_day = datetime.datetime.strptime(tmp[3], '%Y-%m-%d')
            if tmp_day < yesterday:
                multi_add(PreAnalysisStocks, data)
                singal = False
                break
            data.append({
                'code': tmp[1],
                'name': tmp[2],
                'detials': '',
                'extent': tmp[8],
                'notice_time': tmp[3],
                'status': 1
            })
            if len(data) > 100:
                multi_add(PreAnalysisStocks, data)
                data = []
        page += 1
        time.sleep(random.choice(range(3, 8)))

    page = 1
    singal = True
    data = []
    while singal:
        res = requests.get(yjkb_url % (version, page), headers=header)
        time.sleep(random.choice(range(3, 8)))
        html = etree.HTML(res.content.decode('gbk'))
        tr_list = html.xpath('/html/body/table/tbody/tr')
        logging.info(yjkb_url % (version, page))
        logging.info(len(tr_list))
        if len(tr_list) == 0:
            multi_add(PreAnalysisStocks, data)
            logging.info(res.text)
            break
        for tr in tr_list:
            tmp = [i.strip() for i in tr.xpath('.//text()') if i.strip()]
            tmp_day = datetime.datetime.strptime(tmp[3], '%Y-%m-%d')
            if tmp_day < yesterday:
                multi_add(PreAnalysisStocks, data)
                singal = False
                break
            data.append({
                'code': tmp[1],
                'name': tmp[2],
                'detials': '',
                'extent': tmp[8],
                'notice_time': tmp[3],
                'status': 1
            })
            if len(data) > 100:
                multi_add(PreAnalysisStocks, data)
                data = []
        page += 1
        time.sleep(random.choice(range(3, 8)))
