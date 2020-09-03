# 目标：数据遗漏时进行补充
# 改动：输入时间跨度来进行一次基于分钟的数据获取，对于每日的状况需要手动改动

import re
import time
import csv

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


# 获取粉丝数
def get_num_fans(url):
    # 获取粉丝数，初始化为0
    # i 表示尝试次数
    num = 0
    i = 0
    test_num = 5
    # 尝试直到成功获取 num 值

    while int(num) == 0 and int(i) != test_num:
        # 初始化driver
        driver = webdriver.Chrome('./chromedriver.exe')

        driver.get(url)
        source = driver.page_source
        try:
            # 正则表达式获取粉丝数
            big = re.findall('/fans/fans" class="text router-link(.*?)class="num">', source, re.S)[0]
            num = re.findall('title="(.*?)"', big, re.S)[0]

            # 关闭selenium浏览器
            driver.quit()
            break
        except IndexError:
            driver.quit()
            i += 1
            continue
    if int(i) == test_num or int(num) == 0 :
        return '获取失败'
    else:
        return num

# 把字典写入csv文件
def csv_write(dict,time_str):
    # 写入csv文件，需要先判断第一行是否存在数据，若存在则继续写入，不存在则写入标题
    # dict 表示存放数据的字典， str 表示相应的时间跨度
    # key_list当中已经存放了fieldnames所需要的值
    with open(f'kano_{time_str}_粉丝数.csv','r+',newline = '',encoding = 'utf-8') as f:
        key_list = []
        for key in dict.keys():
            key_list.append(key)

        writer = csv.DictWriter(f,fieldnames = key_list)
        if f.readline() == '':
            writer.writeheader()
        writer.writerow(dict)
    return 0

# 根据时间来写入相应的csv文件
def time_do (num, time_str):
    # 获取日期和时间
    # 根据时间和日期分别处理成相应csv文件
    # 需要在其中创建dict，需要切片处理
    dict = {}

    dict['日期'] = f'{time_list[0]}  {time_list[1]}:{time_list[2]}'
    dict['粉丝数'] = num
    csv_write(dict,time_str)
    print(f"{dict['日期']}时，粉丝数为：{dict['粉丝数']}")
    return 0




# 在主程序中设置程序，使爬虫不间断运行
url = 'https://space.bilibili.com/316381099/fans/fans'
time_str = input(f'请输入时间跨度（分钟 / 小时 / 每日）： ')

while True:
    time_0 = time.strftime('%d-%H-%M-%S', time.localtime())
    time_list = time_0.split('-')
    # 每分钟
    if not int(time_list[-1]):
        with open(f'kano_{time_str}_粉丝数.csv', 'a', encoding='utf-8')as f:
            pass
        num = get_num_fans(url)
        time_do(num,time_str)
