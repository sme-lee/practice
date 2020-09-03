# 还可以增加的功能：使用多进程来增加速度、输出播放量最高的作品及播放量
# 已增加的功能：加入了空间网址，音乐作品数和总作品数
import requests
import re
import time
import random

# 多线程队列一般放入 run 函数中执行

# 1、获取必要的元素
def get_headers(head):
    return dict([line.split(': ', 1) for line in head.split('\n')])


headers = '''accept: application/json, text/plain, */*
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6
cookie: _uuid=7D23CC0B-197E-64CC-540A-CEDE839CDA7230306infoc; buvid3=7C6277D6-F37B-42E8-9498-ACC5143D7A4E70380infoc; sid=5jf4it0f; CURRENT_FNVAL=16; rpdid=|(kmJY~|Rm0J'ulml|mkJm~; DedeUserID=444191179; DedeUserID__ckMd5=ba58c3fbac61ccd8; SESSDATA=58d9e8c0%2C1612055480%2C1acea*81; bili_jct=66672efc976c24ebb6fefddaf221c176; bp_t_offset_444191179=424047348110754854; CURRENT_QUALITY=80; bp_video_offset_444191179=423455093597952029; LIVE_BUVID=AUTO9715976692153703; PVID=3; bfe_id=463d72211d8612b93e1aed57df2ab3d4
origin: https://space.bilibili.com
referer: https://space.bilibili.com/11073/video?tid=3&keyword=&order=pubdate
sec-fetch-dest: empty
sec-fetch-mode: cors
sec-fetch-site: same-site
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'''

url_1 = 'https://api.bilibili.com/x/space/arc/search?mid='
i = 1
url_2 = '&ps=30&tid=0&pn=1&keyword=&order=click&jsonp=jsonp'

# 求空间网址时需要用到的 html 代码
html_space = 'https://space.bilibili.com/'


# 2、定义获取全部需要的信息的函数，返回一个字典
def get_info(i):
    url = url_1 + str(i) + url_2
    # 音乐类投稿和总投稿数任一为空时，返回 0 ，不为空时，返回带信息的字典
    info = {}
    content = requests.get(url).content.decode()

    # 进行一段时间的休息避免被拦截
    time.sleep(random.randint(0, 2) + random.random())

    # 求总稿件数
    try:
        big = re.findall('"page":{(.*?)}', content, re.S)[0]
        t_num = int(re.findall('"count":(.*?),', big, re.S)[0])
    except Exception as e:
        t_num = 0
        return 0

    # 求音乐稿件数
    try:
        big = re.findall('"list":(.*?)"vlist"', content, re.S)[0]
        content_1 = re.findall('"3":{(.*?)}', big, re.S)[0]
        m_num = int(re.findall('"count":(.*?),', content_1, re.S)[0])
    except Exception as e:
        m_num = 0
        return 0

    # 判断是否是音乐区 up 主
    if not t_num / m_num <= 3:
        return 0
    else:
        # 求 up 主的用户名
        try:
            name = re.findall('"author":"(.*?)"', content, re.S)[0]
        except Exception as e:
            name = '无法获取'
            print('无法获取的uid为：', i, e)

        try:
            # 求播放量最高的作品及播放量
            big = re.findall('"vlist":(.*?)"page"', content, re.S)[0]
            play = re.findall('"play":(.*?),', big, re.S)[0]
            title = re.findall('"title":"(.*?)"', big, re.S)[0]
            info['音乐稿件数    '] = m_num
            info['总稿件数     '] = t_num
            info['uid         '] = str(i)
            info['用户名       '] = name
            info['空间网址     '] = html_space + str(i)
            info['播放最高的作品'] = title
            info['最高播放量    '] = play
        except Exception as e:
            print(big)[0]
            print(e)
        return info


# 3、计数并输出相关信息
def print_info(i,count):
    up_music_dict = get_info(i)
    if up_music_dict:
        count += 1
        up_music_list.append(up_music_dict)
    return count



# 建立多线程
import threading
import queue as Queue

start = time.time()
class myThread(threading.Thread):
    def __init__(self, q):
        threading.Thread.__init__(self)
        self.q = q
    def run(self):
        count = 0
        while not self.q.empty():
            i = self.q.get()
            count = print_info(i, count)



up_music_list = []
ts = []
up_num_1 = int(input('请输入uid下限：'))
up_num_2 = int(input('请输入uid上限：'))
thr_num = 10
thr_num = 35
# 建立队列
workqueue = Queue.Queue(up_num_2+ 1- up_num_1)
for i in range(up_num_1, up_num_2 + 1):
    workqueue.put(i)

for i in range(35):
    t = myThread(workqueue)
    t.start()
    ts.append(t)
for t in ts:
    t.join()
end = time.time()
print(f'前{up_num_1}到{up_num_2}名up中有{len(up_music_list)}个音乐区up主。')
for up in up_music_list:
    for key, value in up.items():
        print(key, value)
    print(' ')
print(f'花费的时间为{end - start}')


