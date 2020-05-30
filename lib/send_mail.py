#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
import traceback
import logging
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header
from mysql.user import get_all_receiver, update_user_time

my_sender = '2528756899@qq.com'  # 发件人邮箱账号
my_pass = 'gwzsdcguoxgudife'  # 发件人邮箱密码
my_user = '2528756899@qq.com'  # 收件人邮箱账号
to_addrs = get_all_receiver()


def mail(text, tomaster=True):
    ret = True
    try:
        msg = MIMEText(text, 'html', 'utf-8')
        # msg['From'] = formataddr(["stock_analysis", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['From'] = Header("业绩分析", 'utf-8')  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['Subject'] = "因业绩公告上涨的股票"  # 邮件的主题，也可以说是标题
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        if tomaster:
            msg['To'] = formataddr(["my", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        else:
            for addr in to_addrs:
                msg['To'] = formataddr(["my", addr.email])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
                server.sendmail(my_sender, [addr, ], msg.as_string())
                update_user_time(addr)
        server.quit()  # 关闭连接
    except Exception as e:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        logging.error(traceback.format_exc())
        ret = False
    return ret
