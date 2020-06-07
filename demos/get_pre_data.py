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
from mysql.proxy import get_all_proxys, del_proxy
import logging, traceback
from settings import user_agents


yjyg_url = 'http://data.10jqka.com.cn/ajax/yjyg/date/%s/board/ALL/field/enddate/order/desc/page/%s/ajax/1/free/1/'
yjgg_url = 'http://data.10jqka.com.cn/ajax/yjgg/date/%s/board/ALL/field/DECLAREDATE/order/desc/page/%s/ajax/1/free/1/'
yjkb_url = 'http://data.10jqka.com.cn/ajax/yjkb/date/%s/board/ALL/field/declaredate/order/desc/page/%s/ajax/1/free/1/'
index_url = 'http://data.10jqka.com.cn/financial/yjyg/'


def gen_header():
    return {
        'user-agent': random.choice(user_agents),
        'Cookie': 'vvvv=1; v=Ardm1T-ZphfLuSKbWEGtBwF8RqACfIveZVAPUglk0wbtuNlWEUwbLnUgn6Ma'
    }


# def gen_proxy():
#     return random.choice(get_all_proxys())
    # ip = proxy.ip
    # port = proxy.port
    # return {
    #     'http': 'http://%s:%s' % (ip, port),
    #     'https': 'http://%s:%s' % (ip, port)
    # }


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
    for proxy in get_all_proxys():
        proxies = {
            'http': 'http://%s:%s' % (proxy.ip, proxy.port),
            'https': 'http://%s:%s' % (proxy.ip, proxy.port)
        }
        try:
            index_html = etree.HTML(requests.get(index_url, headers=gen_header(), proxies=proxies, timeout=30).content.decode('gbk'))
            if 'Nginx forbidden' not in index_html:
                break
            else:
                del_proxy(proxy.id)
        except:
            logging.error(traceback.format_exc())
            del_proxy(proxy.id)
    time.sleep(random.choice(range(2, 6)))
    today = index_html.xpath('//*[@id="J-ajax-main"]/table/tbody/tr[1]/td[8]')[0].text
    yesterday = datetime.datetime.strptime(today, '%Y-%m-%d')-datetime.timedelta(days=1)
    logging.info(today)

    while singal:
        for proxy in get_all_proxys():
            proxies = {
                'http': 'http://%s:%s' % (proxy.ip, proxy.port),
                'https': 'http://%s:%s' % (proxy.ip, proxy.port)
            }
            try:
                res = requests.get(yjyg_url % (version, page), headers=gen_header(), proxies=proxies, timeout=30)
                if 'Nginx forbidden' not in index_html:
                    break
                else:
                    del_proxy(proxy.id)
            except:
                logging.error(traceback.format_exc())
                del_proxy(proxy.id)
        time.sleep(random.choice(range(2, 6)))
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
        time.sleep(random.choice(range(2, 6)))

    page = 1
    singal = True
    data = []
    while singal:
        for proxy in get_all_proxys():
            proxies = {
                'http': 'http://%s:%s' % (proxy.ip, proxy.port),
                'https': 'http://%s:%s' % (proxy.ip, proxy.port)
            }
            try:
                res = requests.get(yjgg_url % (version, page), headers=gen_header(), proxies=proxies, timeout=30)
                if 'Nginx forbidden' not in index_html:
                    break
                else:
                    del_proxy(proxy.id)
            except:
                logging.error(traceback.format_exc())
                del_proxy(proxy.id)
        time.sleep(random.choice(range(2, 6)))
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
        time.sleep(random.choice(range(2, 6)))

    page = 1
    singal = True
    data = []
    while singal:
        for proxy in get_all_proxys():
            proxies = {
                'http': 'http://%s:%s' % (proxy.ip, proxy.port),
                'https': 'http://%s:%s' % (proxy.ip, proxy.port)
            }
            try:
                res = requests.get(yjkb_url % (version, page), headers=gen_header(), proxies=proxies, timeout=30)
                if 'Nginx forbidden' not in index_html:
                    break
                else:
                    del_proxy(proxy.id)
            except:
                logging.error(traceback.format_exc())
                del_proxy(proxy.id)
        time.sleep(random.choice(range(2, 6)))
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
        time.sleep(random.choice(range(2, 6)))
