# C266打印机计数
# Author: 2997@YBZN
# -*- coding: utf-8 -*-
from selenium import webdriver
import datetime
import time
import locale
import os
import configparser
import requests
from lxml import etree
from dingtalkchatbot.chatbot import DingtalkChatbot

# 参考 https://www.jianshu.com/p/1531e12f8852
# 览器驱动,放到python目录
# chrome
# https://chromedriver.storage.googleapis.com/index.html

# firefox
# https://github.com/mozilla/geckodriver/releases


def get_printer_count(year, month, day, cycle, black_start_num, black_num, color_start_num, color_num):
    list = []
    all_count = ''
    chrome_options = webdriver.ChromeOptions()
    # 使用headless无界面浏览器模式
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    # 启动浏览器，获取网页源代码
    browser = webdriver.Chrome(chrome_options=chrome_options)
    mainUrl = "http://192.168.2.254/wcd/system_counter.xml"
    browser.get(mainUrl)
    time.sleep(15)
    #print(f"browser text = {browser.page_source}")
    webdata = browser.page_source
    # print(webdata)
    html = etree.HTML(webdata)
    #html_data = html.xpath('//th[@width="260px"]')
    html_data = html.xpath('//td//div[@align="right"]')
    for i in html_data:
        list.append(i.text)
    browser.quit()

    start_date = datetime.date(year, month, day)
    #end_date = datetime.date(2021,12,31)
    current_date = datetime.date.today()
    #black_start_num = 63029
    #color_start_num = 7811
    #black_num = 5000
    #color_num = 300
    delta = current_date - start_date
    count_cycle = delta.days // 30 + 1
    black_limit = black_start_num + black_num * count_cycle
    color_limit = color_start_num + color_num * count_cycle
    black_all_count = black_num * cycle
    color_all_count = color_num * cycle
    black_color_all_count = black_start_num + \
        color_start_num + black_all_count + color_all_count
    print(start_date)
    print(current_date)
    print(delta.days)
    print('计数周期',count_cycle)
    print(black_limit)
    print(color_limit)

    black_count = int(str(list[104]))
    color_count = int(str(list[105]))
    locale.setlocale(locale.LC_ALL, 'en')
    locale.setlocale(locale.LC_CTYPE, 'chinese')
    print('\n', "柯尼卡美能C266打印统计", '\n', time.strftime('%Y年%m月%d日%H时%M分%S秒'), '\n', '总计', str(
        list[103]), '\n', '黑色', str(list[104]), '\n', '彩色', str(list[105]), '\n')
    first_count = '本期结算数量' + ' ' + '截止2021年12月31日' + '\n' + '打印机计数范围内' + str(black_color_all_count) + '    黑色' + str(
        black_start_num + black_all_count) + '    彩色' + str(color_start_num + color_all_count) + '\n'
    all_count = '当前数量统计  ' + time.strftime('%Y年%m月%d日%H时%M分') + '\n' + '当前使用计数' + str(
        list[103]) + '    ' + '黑色' + str(list[104]) + '    ' + '彩色' + str(list[105])
    remainder1 = '本月剩余数量  ' + '本月1号至下月30号' + '\n' + '本月剩余总计' + str((black_limit-black_count) + (
        color_limit-color_count)) + '     ' + '黑色' + str(black_limit-black_count) + '     ' + '彩色' + str(color_limit-color_count)
    remainder2 = '半年剩余数量  ' + '截止2021年12月31日' + '\n' + '半年剩余总计' + str(black_color_all_count - int(str(list[103]))) + '     ' + '黑色' + str(
        black_start_num + black_all_count - int(str(list[104]))) + '     ' + '彩色' + str(color_start_num + color_all_count - int(str(list[105])))

    print_all = '\n' + first_count + '\n' + all_count + \
        '\n\n' + remainder1 + '\n\n' + remainder2
    print_lite = 'C266打印数本月剩余' + '\n黑色' + str(black_limit - black_count) + '\n彩色' + str(color_limit - color_count) + '\n' + '\n>>>>>>>>>>>>>>>>' + '\n截止2021年12月31日剩余' + '\n黑色' + str(
        black_start_num + black_all_count - int(str(list[104]))) + '\n彩色' + str(color_start_num + color_all_count - int(str(list[105])))
    print(print_all)
    '''
    if (black_count >= (black_limit-500)) or ((current_date.day > 1) and (current_date.day < 5)):
        black_command = 'msg /server:192.168.2.15 * "c226打印机本月黑色上限' + str(black_limit) + ',已使用' + str(list[104]) + '",本月剩余"' + str(black_limit-black_count)
        os.system(black_command)
    if (color_count >= (color_limit-50)) or ((current_date.day > 1) and (current_date.day < 5)):
        color_command = 'msg /server:192.168.2.15 * "c226打印机本月彩色上限' + str(color_limit) + ',已使用' + str(list[105]) + '",本月剩余"' +  str(color_limit-color_count)
        os.system(color_command)
    '''
    c226_file = open('c266_printer.txt', 'r+', encoding="utf-8")
    c226_file.read()
    #c226_file.write('\n' + time.strftime('%Y年%m月%d日%H时%M分%S秒'))
    #c226_file.write('\n' + 'C226打印机复印总数量')
    #c226_file.write('\n' + '         ' + '日期' + '              ' + '总计' +'    ' + '黑色' + '    ' + '彩色')
    c226_file.write('\n' + time.strftime('%Y年%m月%d日') + '   ' + str(list[103]) + '   ' + str(list[104]) + '    ' + str(
        black_limit-black_count) + '         ' + str(list[105]) + '     ' + str(color_limit-color_count))
    c226_file.close()

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
    black_num = int(items[5][1])
    color_start_num = int(items[6][1])
    color_num = int(items[7][1])
    get_printer_count(year, month, day, cycle,
                      black_start_num, black_num, color_start_num, color_num)
