# C266打印机计数
# Author: 2997@YBZN
# -*- coding: utf-8 -*-

# 参考 https://www.jianshu.com/p/1531e12f8852
# 浏览器驱动,放到python目录
# chrome
# https://chromedriver.storage.googleapis.com/index.html
# firefox
# https://github.com/mozilla/geckodriver/releases
# pip install selenium lxml requests DingtalkChatbot python-dateutil

import os
import time
import locale
import calendar
import datetime
import requests
import configparser
from lxml import etree
from selenium import webdriver
from monthscalculation import calmonths
from dateutil.relativedelta import relativedelta
from dingtalkchatbot.chatbot import DingtalkChatbot

locale.setlocale(locale.LC_ALL, 'en')
locale.setlocale(locale.LC_CTYPE, 'chinese')


def get_printer_count(year, month, day, cycle, black_start_num, black_month_num, color_start_num, color_month_num):
    list = []
    all_count = ''
    chrome_options = webdriver.ChromeOptions()
    # 使用headless无界面浏览器模式
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    # 启动浏览器，获取网页源代码，读取 http://192.168.2.254/wcd/system_counter.xml 页面 总计，黑色，彩色的计数器数量
    browser = webdriver.Chrome(chrome_options=chrome_options)
    mainUrl = "http://192.168.2.254/wcd/system_counter.xml"
    browser.get(mainUrl)
    time.sleep(15)
    # print(f"browser text = {browser.page_source}")
    webdata = browser.page_source
    # print(webdata)
    html = etree.HTML(webdata)
    # html_data = html.xpath('//th[@width="260px"]')
    html_data = html.xpath('//td//div[@align="right"]')
    for i in html_data:
        list.append(i.text)
    browser.quit()

    # 打印机当前总计、黑色、彩色的计数器数量
    all_cur_count = int(str(list[103]))
    black_cur_count = int(str(list[104]))
    color_cur_count = int(str(list[105]))

    start_date = datetime.date(year, month, day)
    end_date = start_date + \
        relativedelta(months=cycle) + datetime.timedelta(days=-1)
    current_date = datetime.date.today()
    if day == 1:
        monthrange = '当月1日至当月' + \
            str(calendar.monthrange(
                year, datetime.datetime.now().month)[1]) + '日'
    else:
        monthrange = '当月' + str(day) + '日至下月' + str(day-1) + '日'

    count_cycle = int(calmonths(start_date, current_date)[0]) + 1
    black_limit = black_start_num + black_month_num * count_cycle
    color_limit = color_start_num + color_month_num * count_cycle
    black_all_num = black_month_num * cycle
    color_all_num = color_month_num * cycle
    black_color_all_count = black_start_num + \
        color_start_num + black_all_num + color_all_num

    black_all_count = black_start_num + black_all_num
    color_all_count = color_start_num + color_all_num

    black_month_remain = black_limit - black_cur_count
    color_month_remain = color_limit - color_cur_count
    black_remain = black_start_num + black_all_num - black_cur_count
    color_remain = color_start_num + color_all_num - color_cur_count

    print('\n''***柯尼卡美能C266打印机计数器***')
    print('打印机当前计数器数_总计:', all_cur_count)
    print('打印机当前计数器数_黑色:', black_cur_count)
    print('打印机当前计数器数_彩色:', color_cur_count, '\n')

    print('***柯尼卡美能C266打印统计***')
    print('开始计算时间:', start_date)
    print('结束计算时间:', end_date)
    print('当前计算时间:', current_date)
    print('已经使用月数:', count_cycle)
    print(str(cycle) + '个月计划总量_黑色:', black_all_num)
    print(str(cycle) + '个月计划总量_彩色:', color_all_num)
    print('打印机计数器数_黑色:', black_all_count)
    print('打印机计数器数_彩色:', color_all_count)
    print('本月剩余数量_黑色:', black_month_remain)
    print('本月剩余数量_彩色:', color_month_remain)
    print('截止', end_date, '剩余数量_黑色:', black_remain)
    print('截止', end_date, '剩余数量_彩色:', color_remain, '\n')

    print_lite = 'C266打印数统计\n' + monthrange + '\n截止本月剩余' + '\n黑色：' + str(black_month_remain) + '\n彩色：' + str(color_month_remain) + '\n' + '\n******************' + '\n截止' + str(end_date) + '剩余' + '\n黑色：' + str(
        black_remain) + '\n彩色：' + str(color_remain)
    print(print_lite)
    '''
    if (black_cur_count >= (black_limit-500)) or ((current_date.day > 1) and (current_date.day < 5)):
        black_command = 'msg /server:192.168.2.15 * "c226打印机本月黑色上限' + str(black_limit) + ',已使用' + str(list[104]) + '",本月剩余"' + str(black_month_remain)
        os.system(black_command)
    if (color_cur_count >= (color_limit-50)) or ((current_date.day > 1) and (current_date.day < 5)):
        color_command = 'msg /server:192.168.2.15 * "c226打印机本月彩色上限' + str(color_limit) + ',已使用' + str(list[105]) + '",本月剩余"' + str(color_month_remain)
        os.system(color_command)
    '''
    with open('c266_printer.txt', 'r+', encoding="utf-8") as fp:
        fp.read()
        fp.write('\n' + time.strftime('%Y年%m月%d日') + '   ' + str(all_cur_count) + '   ' + str(black_cur_count) + '    ' + str(
            black_month_remain) + '         ' + str(color_cur_count) + '     ' + str(color_month_remain))

    # Synology_Chat(print_all)
    # Ding_Bot(print_lite)


# 发送到群晖Chat
def Synology_Chat(count):
    chat_url = "http://192.168.2.241:5000/webapi/entry.cgi?api=SYNO.Chat.External&method=incoming&version=2&token=%22Z6iYpGndUs3oq9MRmhcNJZuefJNEVGaFDpHxeKxdrIrGWUdjE6fjUBzdNsWDKGJJ%22"
    payload = 'payload={"text": "' + count + '"}'
    payload = payload.encode("utf-8").decode("latin1")
    r = requests.post(chat_url, payload).text


def Ding_Bot(count):
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=token'
    secret = 'secret'
    xiaoding = DingtalkChatbot(webhook, secret=secret)
    at_mobiles = ['186612345678']
    #xiaoding.send_text(msg = count, at_mobiles=at_mobiles)
    xiaoding.send_text(msg=count, is_at_all=False)


if __name__ == '__main__':
    curpath = os.path.dirname(os.path.realpath(__file__))
    inipath = os.path.join(curpath, "c266_printer.ini")
    conf = configparser.ConfigParser()
    conf.read(inipath, encoding="utf-8")
    sections = conf.sections()
    items = conf.items('count')
    year = int(items[0][1])
    month = int(items[1][1])
    day = int(items[2][1])
    cycle = int(items[3][1])
    black_start_num = int(items[4][1])
    black_month_num = int(items[5][1])
    color_start_num = int(items[6][1])
    color_month_num = int(items[7][1])
    get_printer_count(year, month, day, cycle,
                      black_start_num, black_month_num, color_start_num, color_month_num)
